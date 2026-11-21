"""The tester's scenario against a running API: batches of ten, one after another, every answer saved, then the metrics of the spec.

  python eval/run_eval.py --url http://127.0.0.1:8000 [--run-id my-run] [--gold eval/hard.jsonl] [--limit 10] [--protocol]

Every reply is checked against the spec, see eval/structure.py. --limit sends one small sample first, --protocol also tries the rules around a batch.
Answer correctness here is a rough stand-in for the 0-1-2 grade of the spec: the key phrases or their numbers have to be in the answer.
"""
import argparse
import functools
import json
import os
import sqlite3
import statistics
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(ROOT / "eval"))
import structure  # noqa: E402
from lexuz.translit import to_latin  # noqa: E402
from rag.numbers import values  # noqa: E402
from rag.text import fold  # noqa: E402


def load_gold(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return list(map(json.loads, filter(str.strip, lines)))


def request(run_id, index, total, items):
    return {"run_id": run_id, "batch_id": f"{run_id}-b{index:02}", "batch_index": index, "total_batches": total,
            "options": {"top_k": 5, "return_contexts": True, "return_debug": True, "temperature": 0, "seed": 42, "as_of_date": "2026-11-01", "answer_language": "auto"},
            "items": [{"id": g["id"], "question": g["question"], "language": g["language"]} for g in items]}


def send(client, body):
    index = body["batch_index"]
    for wait in (0, 5, 15, 45):
        time.sleep(wait)
        reply = client.post("/v1/rag/batch", json=body, timeout=130)
        if reply.status_code == 202:
            while True:
                time.sleep(3)
                reply = client.get(f"/v1/rag/batch/{body['batch_id']}", timeout=30)
                if reply.json().get("status") != "processing":
                    return reply.json()
        if reply.status_code == 200:
            return reply.json()
        print("batch", index, "status", reply.status_code, reply.text[:200])
    raise SystemExit(f"batch {index} did not go through")


def stated(form, answer):
    """A plain number has to be that number: "15" must not pass on "2015". Anything else counts by its words, or by the numbers in them."""
    numbers = values(answer) | values(to_latin(answer))
    wanted = values(form)
    if form.replace(" ", "").replace(",", "").replace(".", "").isdigit():
        return wanted <= numbers
    return fold(to_latin(form)) in fold(to_latin(answer)) or (bool(wanted) and wanted <= numbers)


def correct(item, result):
    if not result.get("answer") or result.get("no_answer"):
        return False
    answer = result["answer"]
    if any(stated(form, answer) for form in item.get("must_not", [])):
        return False
    return all(any(stated(form, answer) for form in group) for group in item.get("keys") or [[item["key"]]])


@functools.cache
def russian_pages():
    """An act with text only in Russian is known by the number of its Russian page, see rag/search.py."""
    con = sqlite3.connect(f"file:{(ROOT / 'data' / 'index' / 'lex.sqlite').as_posix()}?mode=ro", uri=True)
    return {doc: url.rsplit("/", 1)[-1].lstrip("-") for doc, url in con.execute("SELECT doc_id, url FROM acts WHERE lang = 'ru'")}


def lex(doc):
    return "lex:" + russian_pages().get(doc, doc.lstrip("-"))


def coverage(item, contexts):
    """Share of the needed sources found in the top five: a question over two acts is not answered by one of them."""
    needed = {(lex(s["doc"]), s["article"]) for s in item.get("sources", [])}
    found = {(c["doc_id"], c["article"]) for c in contexts[:5]}
    return len(needed & found) / len(needed) if needed else None


def verdicts(gold, rows, by_id):
    """The grades for /logs. They are as rough as the check itself, and the page says so."""
    marks = []
    for row in rows:
        item = row["item"]
        why = None if row["correct"] else "В ответе нет ключевых слов эталона"
        if not row["place"]:
            why = ", ".join(filter(None, [why, "нужной статьи нет в первых пяти"]))
        keys = [" или ".join(group) for group in item.get("keys") or [[item["key"]]]]
        marks.append({"id": item["id"], "ok": row["correct"], "why": why, "expected": item.get("answer") or "; ".join(keys), "category": item["category"]})
    for item in gold:
        if not item.get("answerable", True):
            silent = by_id[item["id"]].get("no_answer") is True
            marks.append({"id": item["id"], "ok": silent, "why": None if silent else "Ответа быть не должно, система ответила", "expected": "В законах ответа нет", "category": item["category"]})
    return marks


def grade(gold, results):
    by_id = {r["id"]: r for r in results}
    answerable = [g for g in gold if g.get("answerable", True)]
    silent = [g for g in gold if not g.get("answerable", True)]
    hits_doc = hits_article = 0
    reciprocal = 0.0
    rows = []
    for item in answerable:
        result = by_id[item["id"]]
        contexts = result.get("contexts") or []
        doc_hit = any(c["doc_id"] == lex(item["doc"]) for c in contexts[:5])
        place = next((c["rank"] for c in contexts[:5] if c["doc_id"] == lex(item["doc"]) and c["article"] in item["articles"]), None)
        hits_doc += doc_hit
        hits_article += bool(place)
        reciprocal += 1 / place if place else 0
        rows.append({"item": item, "result": result, "doc_hit": doc_hit, "place": place, "correct": correct(item, result), "coverage": coverage(item, contexts)})
    fabricated = stale = 0
    for result in results:
        chunks = {c["chunk_id"] for c in result.get("contexts") or []}
        for citation in result.get("citations") or []:
            fabricated += citation["chunk_id"] not in chunks
            stale += citation["doc_status"] != "amalda"
    times = [r["timing"]["total_ms"] / 1000 for r in results if r.get("timing") and not (r.get("debug") or {}).get("cached")]
    n = max(1, len(answerable))
    print(f"\nanswerable {len(answerable)}, unanswerable {len(silent)}")
    print(f"Hit@5 document   {hits_doc / n:6.1%}   (spec 90%)")
    print(f"Hit@5 article    {hits_article / n:6.1%}   (spec 80%)")
    print(f"MRR              {reciprocal / n:6.3f}   (spec 0.70)")
    covered = [r["coverage"] for r in rows if r["coverage"] is not None]
    if covered:
        print(f"sources in top 5 {sum(covered) / len(covered):6.1%}   (every source a question needs)")
    print(f"answers correct  {sum(r['correct'] for r in rows) / n:6.1%}   (key phrase in the answer)")
    print(f"no-answer        {sum(by_id[g['id']].get('no_answer') is True for g in silent)}/{len(silent)}     (spec 9/10)")
    spent = [r["usage"] for r in results if r.get("usage")]
    if spent:
        print(f"tokens           {sum(u['input_tokens'] for u in spent)} in, {sum(u['output_tokens'] for u in spent)} out")
    print(f"fabricated       {fabricated}        (spec 0)")
    print(f"stale norms      {stale}        (spec 0)")
    print(f"errors           {sum(r['status'] in ('error', 'timeout') for r in results) / len(results):6.1%}   (spec 2%)")
    if times:
        ordered = sorted(times)
        print(f"latency          p50 {statistics.median(times):.1f}s, p95 {ordered[int(len(ordered) * .95)]:.1f}s   (spec 5s / 12s)")
    for category in sorted({g["category"] for g in answerable}):
        part = [r for r in rows if r["item"]["category"] == category]
        print(f"  {category:11} article {sum(bool(r['place']) for r in part)}/{len(part)}, answer {sum(r['correct'] for r in part)}/{len(part)}")
    for row in rows:
        if not row["correct"] or not row["place"]:
            result = row["result"]
            cause = "retrieval" if not row["place"] else "generation"
            print(f"[{cause}] {row['item']['id']} {row['item']['question'][:60]} -> {result['status']}: {(result.get('answer') or '')[:110]}")
    for item in silent:
        if by_id[item["id"]].get("no_answer") is not True:
            print(f"[made up] {item['id']} {item['question'][:60]} -> {(by_id[item['id']].get('answer') or '')[:110]}")
    return verdicts(gold, rows, by_id)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    ap.add_argument("--run-id", default=f"eval-{time.strftime('%Y%m%d-%H%M%S')}")
    ap.add_argument("--gold", default=ROOT / "eval" / "gold.jsonl")
    ap.add_argument("--limit", type=int, help="send only this many questions, spread over the file")
    ap.add_argument("--protocol", action="store_true", help="also try the rules around a batch: 400, 401, 409, 429, idempotency")
    args = ap.parse_args()
    load_dotenv(ROOT / ".env")
    gold = load_gold(args.gold)
    if args.limit:
        gold = gold[::max(1, len(gold) // args.limit)][:args.limit]
    count = -(-len(gold) // 10)
    batches = [gold[i::count] for i in range(count)]   # every category in every batch, as the spec asks
    folder = ROOT / "eval" / "runs" / args.run_id
    folder.mkdir(parents=True, exist_ok=True)
    results, wrong_shape = [], []
    with httpx.Client(base_url=args.url, headers={"Authorization": f"Bearer {os.environ['LEX_API_KEY']}"}) as client:
        for index, items in enumerate(batches, 1):
            body = request(args.run_id, index, len(batches), items)
            response = send(client, body)
            (folder / f"b{index:02}.json").write_text(json.dumps(response, ensure_ascii=False, indent=1), encoding="utf-8")
            wrong_shape += structure.check(body, response)
            results += response["results"]
            print(f"b{index:02}: {response['summary']} in {response['timing']['total_ms'] / 1000:.1f}s", flush=True)
            time.sleep(1)
        rules = structure.protocol(client, body, response) if args.protocol else None
    print("system", response["system"])
    print(f"\nreply shape: {len(wrong_shape)} problems")
    for line in wrong_shape[:40]:
        print("  ", line)
    if rules is not None:
        print(f"rules around a batch: {len(rules)} problems")
        for line in rules:
            print("  ", line)
    marks = grade(gold, results)
    with httpx.Client(base_url=args.url, headers={"Authorization": f"Bearer {os.environ['LEX_API_KEY']}"}) as client:
        reply = client.post("/api/logs/verdicts", json={"run_id": args.run_id, "verdicts": marks}, timeout=30)
    print(f"\ngrades on /logs: {reply.text[:80]}")


if __name__ == "__main__":
    main()
