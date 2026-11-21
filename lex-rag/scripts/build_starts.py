"""Finds acts that start later than the day they were adopted and writes them next to the index. Takes a minute, needs no rebuild of the index.

  python scripts/build_starts.py
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from rag.search import INDEX  # noqa: E402
from rag.starts import start_of  # noqa: E402

SINCE = "2023-01-01"   # no act here waits longer than that


def main():
    con = sqlite3.connect(f"file:{INDEX.as_posix()}?mode=ro", uri=True)
    acts = con.execute("SELECT doc_id, adopted FROM acts WHERE status = 'amalda' AND adopted >= ? AND section != 'loc'", (SINCE,)).fetchall()
    starts = {}
    for doc_id, adopted in acts:
        for (text,) in con.execute("SELECT text FROM chunks WHERE doc_id = ? AND text LIKE '%kuchga kir%' ORDER BY seq DESC", (doc_id,)):
            start = start_of(adopted, text)
            if start:
                if start.isoformat() > adopted:
                    starts[doc_id] = start.isoformat()
                break
    INDEX.with_name("starts.json").write_text(json.dumps(starts, indent=0, sort_keys=True), encoding="utf-8")
    print(f"{len(acts)} acts read, {len(starts)} start later than adopted")


if __name__ == "__main__":
    main()
