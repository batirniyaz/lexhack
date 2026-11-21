"""Validate eval/hard.jsonl against the index (read-only).

Run from the project root:  .venv/Scripts/python eval/check_hard.py
Exit code 0 means 0 problems.
"""
import json
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
HARD = ROOT / "eval" / "hard.jsonl"
DB = (ROOT / "data" / "index" / "lex.sqlite").as_posix()

CATEGORIES = {
    "faktik": 10, "raqam": 10, "kop_manba": 10, "ozgargan": 8,
    "til": 8, "ogzaki": 4, "javobsiz": 10,
}
LANGUAGES = {"uz-Latn", "uz-Cyrl", "ru"}
MAX_PER_ACT = 8
MIN_NON_CODE = 12

CYR = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "j",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ц": "s",
    "ч": "ch", "ш": "sh", "щ": "sh", "ъ": "'", "ы": "i", "ь": "", "э": "e", "ю": "yu",
    "я": "ya", "ў": "o'", "қ": "q", "ғ": "g'", "ҳ": "h",
}


def ws(text):
    """Whitespace normalisation only: the quote check must stay this strict."""
    return re.sub(r"\s+", " ", text).strip()


def fold(text):
    """Lower-case and unify apostrophes; used only for keys and must_not."""
    text = text.lower()
    for ch in "ʻʼ’‘`":
        text = text.replace(ch, "'")
    return text


def cyr_to_lat(text):
    return "".join(CYR.get(ch, ch) for ch in text.lower())


def main():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.execute("PRAGMA query_only=1")
    items = [json.loads(line) for line in HARD.read_text(encoding="utf-8").splitlines() if line.strip()]
    problems = []

    def bad(item, msg):
        problems.append(f"{item.get('id', '?')}: {msg}")

    def act(doc):
        return conn.execute("SELECT status, doc_type FROM acts WHERE doc_id=?", (doc,)).fetchone()

    seen = Counter(i.get("id") for i in items)
    for ident, n in seen.items():
        if n > 1:
            problems.append(f"{ident}: duplicate id ({n} times)")

    per_act = Counter()
    non_code = 0

    for it in items:
        for field in ("id", "category", "language", "question", "answerable", "must_not", "answer", "trap"):
            if field not in it:
                bad(it, f"missing field {field}")
        if it.get("category") not in CATEGORIES:
            bad(it, f"unknown category {it.get('category')}")
        if it.get("language") not in LANGUAGES:
            bad(it, f"unknown language {it.get('language')}")

        answer = it.get("answer", "")
        folded = fold(answer)
        if it.get("language") == "uz-Cyrl":
            folded = fold(cyr_to_lat(answer))

        if it.get("answerable") is False:
            if it.get("category") != "javobsiz":
                bad(it, "answerable=false outside javobsiz")
            for field in ("doc", "articles", "keys", "sources"):
                if field in it:
                    bad(it, f"javobsiz item must not have {field}")
            if not it.get("proof"):
                bad(it, "javobsiz item needs proof")
            continue

        if it.get("category") == "javobsiz":
            bad(it, "javobsiz item must be answerable=false")

        doc = it.get("doc")
        articles = it.get("articles")
        sources = it.get("sources") or []
        if not sources:
            bad(it, "no sources")
        if not articles:
            bad(it, "no articles")

        docs_used = set()
        for src in sources:
            row = conn.execute(
                "SELECT doc_id, article, text FROM chunks WHERE chunk_id=?", (src.get("chunk_id"),)
            ).fetchone()
            if row is None:
                bad(it, f"chunk not found: {src.get('chunk_id')}")
                continue
            if row[0] != src.get("doc"):
                bad(it, f"{src['chunk_id']}: doc_id {row[0]} != {src.get('doc')}")
            if row[1] != src.get("article"):
                bad(it, f"{src['chunk_id']}: article {row[1]} != {src.get('article')}")
            if ws(src.get("quote", "")) not in ws(row[2]):
                bad(it, f"{src['chunk_id']}: quote is not a span of the chunk: {src.get('quote')[:60]}")
            status = act(row[0])
            if status is None:
                bad(it, f"act not found: {row[0]}")
            elif status[0] != "amalda":
                bad(it, f"{row[0]}: status is {status[0]}")
            docs_used.add(row[0])

        pairs = {(s.get("doc"), s.get("article")) for s in sources}
        if doc not in docs_used:
            bad(it, f"doc {doc} not among sources")
        for art in articles or []:
            if (doc, art) not in pairs:
                bad(it, f"article {art} of {doc} not among sources")
        if it.get("category") == "kop_manba" and len(pairs) < 2:
            bad(it, "kop_manba needs two articles or acts")

        keys = it.get("keys")
        if not keys or any(not group for group in keys):
            bad(it, "keys missing or empty group")
        for group in keys or []:
            if not any(fold(k) in folded for k in group):
                bad(it, f"reference answer does not match key group {group[:3]}")
        for word in it.get("must_not", []):
            if fold(word) in folded:
                bad(it, f"reference answer contains must_not string: {word}")

        for d in docs_used:
            per_act[d] += 1
        info = act(doc)
        if info and info[1] not in ("kodeks", "konstitutsiya"):
            non_code += 1

        if it.get("category") == "ozgargan":
            stale = it.get("stale")
            if not stale:
                bad(it, "ozgargan without stale evidence")
                continue
            info = act(stale["doc"])
            if info is None:
                bad(it, f"stale act not found: {stale['doc']}")
            elif info[0] == "amalda":
                bad(it, f"stale act {stale['doc']} is in force")
            rows = conn.execute(
                "SELECT text FROM chunks WHERE doc_id=? AND article=?", (stale["doc"], stale["article"])
            ).fetchall()
            if not rows:
                bad(it, f"stale article not found: {stale['doc']} {stale['article']}")
            elif not any(ws(stale["quote"]) in ws(r[0]) for r in rows):
                bad(it, f"stale quote not found in {stale['doc']} {stale['article']}")
            if not it.get("must_not"):
                bad(it, "ozgargan needs must_not")
        elif "stale" in it:
            bad(it, "stale field outside ozgargan")

    counts = Counter(i.get("category") for i in items)
    for cat, want in CATEGORIES.items():
        print(f"{cat:10} {counts.get(cat, 0):3} (target {want})")
    print(f"{'total':10} {len(items):3}")
    print("languages:", dict(Counter(i.get("language") for i in items)))
    print("not from a code (main act):", non_code)
    print("busiest acts:", per_act.most_common(5))

    for doc, n in per_act.items():
        if n > MAX_PER_ACT:
            problems.append(f"act {doc}: used by {n} questions (limit {MAX_PER_ACT})")
    if non_code < MIN_NON_CODE:
        problems.append(f"only {non_code} questions from non-code acts (minimum {MIN_NON_CODE})")
    til = [i for i in items if i.get("category") == "til"]
    for lang in ("ru", "uz-Cyrl"):
        if sum(i.get("language") == lang for i in til) != 4:
            problems.append(f"til: expected 4 questions in {lang}")
    ru_only = False
    for it in til:
        if it.get("language") == "ru":
            row = conn.execute("SELECT lang, status FROM acts WHERE doc_id=?", (it.get("doc"),)).fetchone()
            ru_only = ru_only or row == ("ru", "amalda")
    if not ru_only:
        problems.append("til: no Russian question targets a Russian-only act")

    for p in problems:
        print("PROBLEM", p)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
