"""Search quality alone, no model involved: spec metrics on the gold questions.

  python eval/run_retrieval.py              words only, or words + vectors when the vector index exists
  python eval/run_retrieval.py --show       also lists what was found for every miss
  python eval/run_retrieval.py --plans      with eval/plans_simulated.jsonl in place of the model's reading of the question;
                                            they were written by hand, so this is a rough estimate and not a measurement
  python eval/run_retrieval.py --live       with the model's real plans of the last paid run, on both question sets: what a search change
                                            is worth, for free. "read by the model" is the share of questions with the article in the sources it gets
"""
import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")
from lexuz.translit import to_latin  # noqa: E402
from rag import vectors  # noqa: E402
from rag import pipeline  # noqa: E402
from rag.search import Search  # noqa: E402


def load_gold():
    lines = (ROOT / "eval" / "gold.jsonl").read_text(encoding="utf-8").splitlines()
    return [g for g in map(json.loads, filter(str.strip, lines)) if g.get("answerable", True)]


def load_plans():
    lines = (ROOT / "eval" / "plans_simulated.jsonl").read_text(encoding="utf-8").splitlines()
    return {p["id"]: p for p in map(json.loads, filter(str.strip, lines))}


def load_live():
    """The real plans, and every answerable question they belong to."""
    plans = {p["id"]: p for p in map(json.loads, filter(str.strip, (ROOT / "eval" / "plans_live.jsonl").read_text(encoding="utf-8").splitlines()))}
    gold = []
    for name in ("gold.jsonl", "hard.jsonl"):
        gold += [g for g in map(json.loads, filter(str.strip, (ROOT / "eval" / name).read_text(encoding="utf-8").splitlines())) if g.get("answerable", True)]
    return gold, plans


def replay(gold, search, plans):
    """The search as the pipeline runs it, on the plans the model really wrote."""
    rows = []
    for item in gold:
        plan = plans[item["id"]]
        found = []
        started = time.time()
        if plan.get("is_legal"):
            latin = to_latin(item["question"]) if item["language"] != "ru" else ""
            found = search.retrieve(f"{plan['query']} {latin}", terms=plan["terms"] + [plan["query_ru"]], act_names=plan["acts"], as_of="2026-11-01", old=plan["asks_about_past"], limit=60)
        place = next((n for n, r in enumerate(found, 1) if r["doc_id"] == item["doc"] and r["article"] in item["articles"]), None)
        rows.append({"item": item, "found": found, "place": place, "seconds": time.time() - started, "act": next((n for n, r in enumerate(found, 1) if r["doc_id"] == item["doc"]), None)})
    return rows


def was_read(row, reader):
    """Is the article among the sources the model would really get? The limit on characters can stop them before the limit on candidates."""
    item = row["item"]
    return any(r["doc_id"] == item["doc"] and r["article"] in item["articles"] for r in reader.sources(row["found"]).values())


def report_live(rows, search):
    n = len(rows)
    reader = pipeline.Pipeline(search, None)
    read = [r for r in rows if was_read(r, reader)]
    sizes = [sum(len(s["text"]) for s in reader.sources(r["found"]).values()) for r in rows if r["found"]]
    print(f"questions {n}")
    print(f"read by the model {len(read)} ({len(read) / n:.1%}), {pipeline.CANDIDATES} candidates, {pipeline.MAX_CHARS} characters, median {statistics.median(sizes):.0f} used")
    print(f"found at all      {sum(bool(r['place']) for r in rows)} (first 60)")
    print(f"time per search   median {statistics.median(r['seconds'] for r in rows):.2f}s, max {max(r['seconds'] for r in rows):.2f}s")
    print(f"act found         {sum(bool(r['act']) for r in rows)} (first 60)")
    for r in rows:
        if r not in read:
            print(f"  {r['item']['id']:5} {r['item']['category']:10} article {r['place']}, act {r['act']}")


def score(gold, search, plans=None, top=5):
    rows, times = [], []
    for item in gold:
        started = time.time()
        plan = (plans or {}).get(item["id"])
        if plan:
            latin = to_latin(item["question"]) if item["language"] != "ru" else ""
            found = search.retrieve(f"{plan['query']} {latin}", terms=plan["terms"], act_names=plan["acts"])[:top]
        else:
            found = search.retrieve(item["question"])[:top]
        times.append(time.time() - started)
        place = next((n for n, r in enumerate(found, 1) if r["doc_id"] == item["doc"] and r["article"] in item["articles"]), None)
        doc_hit = any(r["doc_id"] == item["doc"] for r in found)
        rows.append({"item": item, "found": found, "place": place, "doc_hit": doc_hit})
    return rows, times


def report(rows, times, show=False):
    n = len(rows)
    print(f"questions {n}")
    print(f"Hit@5 document {sum(r['doc_hit'] for r in rows) / n:.1%}   (spec: 90%)")
    print(f"Hit@5 article  {sum(bool(r['place']) for r in rows) / n:.1%}   (spec: 80%)")
    print(f"MRR            {sum(1 / r['place'] for r in rows if r['place']) / n:.3f}    (spec: 0.70)")
    print(f"time per question: median {statistics.median(times):.2f}s, max {max(times):.2f}s")
    categories = sorted({r["item"]["category"] for r in rows})
    for category in categories:
        part = [r for r in rows if r["item"]["category"] == category]
        print(f"  {category:11} {sum(bool(r['place']) for r in part)}/{len(part)}")
    if show:
        for r in rows:
            if not r["place"]:
                print("MISS", r["item"]["id"], r["item"]["question"][:70], "want", r["item"]["doc"], r["item"]["articles"])
                for hit in r["found"][:5]:
                    print("    ", hit["doc_id"], hit["article"], hit["doc_type"], hit["doc_title"][:50], "|", hit["text"][:50].replace("\n", " "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--plans", action="store_true")
    ap.add_argument("--live", action="store_true")
    args = ap.parse_args()
    meaning = vectors.Vectors() if vectors.FAISS.exists() else None
    print("vectors:", meaning.index.ntotal if meaning else "none")
    if args.live:
        gold, plans = load_live()
        search = Search(vectors=meaning)
        report_live(replay(gold, search, plans), search)
        return
    rows, times = score(load_gold(), Search(vectors=meaning), load_plans() if args.plans else None)
    report(rows, times, args.show)


if __name__ == "__main__":
    main()
