"""Client for lex-rag, our external search over lex.uz (D-013).

Privacy rule: questions are generic legal questions. They never contain a client's name, domain, URL or field
values. lex-rag answers with citations (verbatim quotes, article, edition date, lex.uz link) and the retrieved
chunks; `verified_citations` keeps only citations whose quote really appears in a retrieved chunk.

    python -m qalqon.legal.lexrag "Shaxsga doir maʼlumotlar toʻgʻrisidagi qonun 21-modda"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from typing import Optional

import httpx

from ..config import SCANS_DIR, settings

CACHE_DIR = SCANS_DIR / ".lexrag_cache"   # git-ignored with scans/
TIMEOUT_S = 90
RETRIES = 2


class LegalSourceError(Exception):
    """lex-rag is not configured, unreachable, or returned an unusable answer."""


def _endpoint() -> str:
    if not settings.lexrag_url or not settings.lexrag_api_key:
        raise LegalSourceError("LEXRAG_URL / LEXRAG_API_KEY are not set")
    return settings.lexrag_url.rstrip("/") + "/v1/rag/query"


def query(question: str, *, use_cache: bool = True) -> dict:
    """Ask lex-rag one question. Cached on disk by the question text."""
    key = hashlib.sha256(question.encode("utf-8")).hexdigest()[:32]
    cache_file = CACHE_DIR / f"{key}.json"
    if use_cache and cache_file.exists():
        return json.loads(cache_file.read_text(encoding="utf-8"))
    last_error: Optional[Exception] = None
    for attempt in range(RETRIES + 1):
        try:
            response = httpx.post(_endpoint(), json={"question": question}, timeout=TIMEOUT_S,
                                  headers={"Authorization": f"Bearer {settings.lexrag_api_key}"})
            response.raise_for_status()
            data = response.json()
            if (data.get("result") or {}).get("status") != "ok":
                raise LegalSourceError(f"lex-rag status: {(data.get('result') or {}).get('status')}")
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
            return data
        except (httpx.HTTPError, ValueError, LegalSourceError) as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise LegalSourceError(f"lex-rag failed: {last_error}")


_APOSTROPHES = re.compile(r"[ʼʻ’‘'`´]")


def normalize(text: str) -> str:
    """Compare texts robustly: one kind of apostrophe, single spaces, no case."""
    return re.sub(r"\s+", " ", _APOSTROPHES.sub("'", text or "")).strip().lower()


def verified_citations(data: dict) -> list[dict]:
    """Citations whose quote is found verbatim (after normalization) in one of the retrieved chunks."""
    result = data.get("result") or {}
    chunks = {c.get("chunk_id"): c.get("text") or "" for c in result.get("contexts") or []}
    all_text = normalize(" ".join(chunks.values()))
    out = []
    for citation in result.get("citations") or []:
        quote = normalize(citation.get("quote") or "")
        if len(quote) >= 20 and quote in all_text:
            chunk_text = chunks.get(citation.get("chunk_id")) or ""
            out.append({**citation, "chunk_text": chunk_text})
    return out


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Ask lex-rag a legal question (generic, no client data).")
    parser.add_argument("question")
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()
    data = query(args.question, use_cache=not args.no_cache)
    result = data.get("result") or {}
    print(result.get("answer"))
    print(f"\nindex: {(data.get('system') or {}).get('index_version')}")
    for c in verified_citations(data):
        print(f"- {c.get('doc_title')} | {c.get('article')} {c.get('part') or ''} | {c.get('edition_date')} | {c.get('url')}")
        print(f"  «{c.get('quote')}»")


if __name__ == "__main__":
    main()
