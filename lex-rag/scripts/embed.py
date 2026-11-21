"""Turns chunks into vectors, strongest acts first. Stop it at any time: the next run continues, and what is done already works.

  python scripts/embed.py --threads 8 [--tier 2]     tier: up to which acts.rank to go, 2 is codes and laws
  python scripts/embed.py --pack                     pack what is done into the index the API reads
"""
import argparse
import ctypes
import sqlite3
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from rag import vectors  # noqa: E402
from rag.search import INDEX  # noqa: E402

BATCH = 32


def order(con, tier):
    """Chunk ids, strongest acts first. Amending acts and tables stay out: they repeat other acts or hold numbers no sentence can find."""
    return [r[0] for r in con.execute("""SELECT c.id FROM chunks c JOIN acts a USING (doc_id)
        WHERE a.status = 'amalda' AND a.amending = 0 AND c.is_table = 0 AND length(c.text) >= 40 AND a.rank <= ? AND a.section != 'loc'
        ORDER BY a.rank, length(c.text), c.id""", (tier,))]


def texts(con, ids):
    """Only one batch of text in memory at a time: the whole set would not fit next to everything else on a laptop."""
    marks = ",".join("?" * len(ids))
    found = {r[0]: r[1:] for r in con.execute(f"""SELECT c.id, a.title, c.headers, c.article_title, c.text FROM chunks c JOIN acts a USING (doc_id)
        WHERE c.id IN ({marks})""", ids)}
    return [vectors.passage(*found[i]) for i in ids]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--tier", type=int, default=6)
    ap.add_argument("--pack", action="store_true")
    args = ap.parse_args()
    if args.pack:
        print("packed", vectors.build_faiss())
        return
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
    done = set(np.fromfile(vectors.IDS, dtype=np.int32).tolist()) if vectors.IDS.exists() else set()
    con = sqlite3.connect(f"file:{INDEX.as_posix()}?mode=ro", uri=True)
    encoder = vectors.Encoder(threads=args.threads)
    rows = [i for i in order(con, args.tier) if i not in done]
    print("to embed", len(rows), "already done", len(done), flush=True)
    started = time.time()
    with open(vectors.VECTORS, "ab") as out, open(vectors.IDS, "ab") as ids:
        for start in range(0, len(rows), BATCH):
            batch = rows[start:start + BATCH]
            matrix = encoder.encode(texts(con, batch), "passage: ")
            out.write(matrix.astype(np.float16).tobytes())
            ids.write(np.array(batch, dtype=np.int32).tobytes())
            out.flush()
            ids.flush()
            if (start // BATCH) % 300 == 0 and start:
                pace = start / (time.time() - started)
                print(f"{time.strftime('%H:%M:%S')} {start}/{len(rows)} {pace:.0f}/s, {(len(rows) - start) / pace / 3600:.1f} h left", flush=True)
    print("finished", len(rows), flush=True)


if __name__ == "__main__":
    main()
