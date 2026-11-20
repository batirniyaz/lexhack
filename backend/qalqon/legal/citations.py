"""Verbatim law citations for findings (F-34).

Each rule lists the article numbers it relies on (`legal_basis[].articles`). This tool asks lex-rag for every
(act, article) once, keeps only quotes that code finds verbatim in the retrieved lex.uz text, and writes
backend/data/law_quotes.json. Scans read that file, so a report never waits for lex-rag and works offline.
The article choice per rule is still Role 2's call: quotes are marked "not verified by a lawyer".

    python -m qalqon.legal.citations            # refresh (uses the lex-rag disk cache)
    python -m qalqon.legal.citations --no-cache
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from functools import lru_cache
from typing import Optional

from ..config import DATA_DIR
from .lexrag import LegalSourceError, normalize, query, verified_citations

QUOTES_FILE = DATA_DIR / "law_quotes.json"

# Acts we can cite: our short name → lex.uz document id in lex-rag and the question wording (Uzbek, the official text).
ACTS = {
    "ZRU-547": {"doc_id": "lex:4396419",
                "question": "Shaxsga doir maʼlumotlar toʻgʻrisidagi Qonunning {article}-moddasida nima belgilangan?"},
    # E-commerce pilot (D-027); law numbers are not shown by lex-rag, so the rules use the official titles.
    "ECOM": {"doc_id": "lex:6213382",
             "question": "Elektron tijorat toʻgʻrisidagi Qonunning {article}-moddasida nima belgilangan?"},
    "CONSUMER": {"doc_id": "lex:4704",
                 "question": "Isteʼmolchilarning huquqlarini himoya qilish toʻgʻrisidagi Qonunning {article}-moddasida nima belgilangan?"},
}


def _article_key(label: str) -> str:
    """'27¹-modda' / '27-1-modda' → '27¹'; '21-modda' → '21'."""
    match = re.match(r"\D*(\d+)(¹|-1(?=\D*modda))?", label or "")
    if not match:
        return ""
    return match.group(1) + ("¹" if match.group(2) else "")


def _part_order(citation: dict) -> int:
    match = re.search(r"\d+", citation.get("part") or "")
    return int(match.group()) if match else 99


def fetch_article(act: str, article: str, *, use_cache: bool = True) -> Optional[dict]:
    """article is "21" (the first parts of the article) or "5:5" (only part 5 of article 5)."""
    spec = ACTS[act]
    number, _, part = article.partition(":")
    question = spec["question"].format(article=number)
    if part:
        question = question.replace(f"{number}-moddasida", f"{number}-moddasining {part}-qismida")
    data = query(question, use_cache=use_cache)
    citations = [c for c in verified_citations(data)
                 if c.get("doc_id") == spec["doc_id"] and _article_key(c.get("article", "")) == number]
    if part:
        citations = [c for c in citations if _part_order(c) == int(part)]
    if not citations:
        return None
    citations.sort(key=_part_order)
    first = citations[0]
    heading = (first.get("chunk_text") or "").split("\n", 1)[0].strip()
    if not normalize(heading).startswith(normalize(number.replace("¹", ""))[:2]):
        heading = ""
    seen, parts = set(), []
    for c in citations[:3]:
        if c["quote"] in seen:
            continue
        seen.add(c["quote"])
        text = c["quote"]
        chunk = c.get("chunk_text") or ""
        start = chunk.find(text)
        if part and start >= 0:
            # One specific part was asked for: show the whole part as lex.uz has it (the quote is inside it).
            lines = chunk.strip().split("\n")
            if lines and normalize(lines[0]).startswith(f"{number}-modda"):
                lines = lines[1:]  # drop the article heading line
            text = "\n".join(lines).strip()
        elif text.rstrip().endswith(":") and start >= 0:
            # A part that introduces a list ("…shart:"): keep the list items from the same lex.uz chunk.
            text = chunk[start:].strip()
        if len(text) > 1500:  # very long list: cut at a line end, never mid-word
            cut = text.rfind("\n", 0, 1500)
            text = text[:cut if cut > 0 else 1500].rstrip() + "\n…"
        parts.append({"part": c.get("part"), "text": text})
    if part:
        heading = heading or f"{number}-modda"
    system = data.get("system") or {}
    return {
        "act": act,
        "article": article,
        "heading": heading,
        "parts": parts,
        "lang": "uz-Latn",
        "url": first.get("url"),
        "edition_date": first.get("edition_date"),
        "doc_status": first.get("doc_status"),
        "doc_title": first.get("doc_title"),
        "source": "lex-rag",
        "index_version": system.get("index_version"),
        "verified_by_lawyer": False,
    }


def wanted_articles() -> list[tuple[str, str]]:
    from ..rules_engine import load_rules  # local import: rules_engine imports this module
    pairs = set()
    for rule in load_rules():
        for basis in rule.get("legal_basis") or []:
            act = basis.get("act_id") or ("ZRU-547" if "ZRU-547" in (basis.get("act") or "") else None)
            for article in basis.get("articles") or []:
                if act in ACTS:
                    pairs.add((act, str(article)))
    return sorted(pairs)


def refresh(use_cache: bool = True) -> dict:
    quotes, missing = {}, []
    for act, article in wanted_articles():
        try:
            found = fetch_article(act, article, use_cache=use_cache)
        except LegalSourceError as exc:
            print(f"  {act} art. {article}: lex-rag error: {exc}", file=sys.stderr)
            found = None
        if found:
            quotes[f"{act}:{article}"] = found
            print(f"  {act} art. {article}: {found['heading'][:70]!r}, {len(found['parts'])} part(s), ed. {found['edition_date']}")
        else:
            missing.append(f"{act}:{article}")
            print(f"  {act} art. {article}: no verified quote", file=sys.stderr)
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "note": "Verbatim text from lex.uz via lex-rag; quotes checked by code against the retrieved text. "
                       "Not verified by a lawyer.",
               "quotes": quotes, "missing": missing}
    QUOTES_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    return payload


@lru_cache(maxsize=1)
def law_quotes() -> dict:
    if not QUOTES_FILE.exists():
        return {}
    return json.loads(QUOTES_FILE.read_text(encoding="utf-8")).get("quotes") or {}


def attach_quotes(legal_basis: list[dict]) -> list[dict]:
    """Copy of the rule's legal basis with verbatim quotes added where we have them."""
    out = []
    quotes = law_quotes()
    for basis in legal_basis or []:
        act = basis.get("act_id") or ("ZRU-547" if "ZRU-547" in (basis.get("act") or "") else None)
        found = [quotes[f"{act}:{a}"] for a in basis.get("articles") or [] if f"{act}:{a}" in quotes]
        out.append({**basis, "citations": found} if found else dict(basis))
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    payload = refresh(use_cache=not args.no_cache)
    print(f"{len(payload['quotes'])} articles quoted, missing: {payload['missing']} → {QUOTES_FILE}")


if __name__ == "__main__":
    main()
