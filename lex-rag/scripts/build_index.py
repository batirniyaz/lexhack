"""Parquet into data/index/lex.sqlite: acts, chunks and their word index. Safe to run again: it builds aside and swaps at the end."""
import datetime as dt
import itertools
import sqlite3
import sys
import time
from pathlib import Path

import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from lexuz import store  # noqa: E402
from rag import chunking, text  # noqa: E402

PARQUET = store.DATA / "parquet"
OUT = store.DATA / "index"
STATUS = {"y": "amalda", "r": "kuchini yo'qotgan", "n": "amalda emas"}
SCHEMA = """
CREATE TABLE acts (doc_id TEXT PRIMARY KEY, number TEXT, title TEXT, doc_type TEXT, rank INT, amending INT, section TEXT, status TEXT,
                   adopted TEXT, edition TEXT, url TEXT, lang TEXT, year INT, meta TEXT);
CREATE TABLE chunks (id INTEGER PRIMARY KEY, chunk_id TEXT, doc_id TEXT, seq INT, piece INT, text TEXT, article TEXT, part TEXT,
                     article_title TEXT, appendix TEXT, headers TEXT, element_ids TEXT, is_table INT);
CREATE VIRTUAL TABLE fts_force USING fts5(title, head, body, content='', columnsize=1, detail=full);
CREATE VIRTUAL TABLE fts_old USING fts5(title, head, body, content='', columnsize=1, detail=full);
CREATE VIRTUAL TABLE fts_acts USING fts5(title, content='', detail=none);
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
"""


def iso(date):
    """DD.MM.YYYY into YYYY-MM-DD."""
    return f"{date[6:]}-{date[3:5]}-{date[:2]}" if date and len(date) == 10 else None


def load_acts(con):
    table = pq.read_table(PARQUET / "acts.parquet", columns=[
        "doc_id", "title", "list_title", "list_meta", "list_state", "section", "adopted", "edition", "text_lang", "text_page", "year"])
    acts = {}
    for row in table.to_pylist():
        title = row["list_title"] or row["title"]
        kind = chunking.doc_type(title, row["list_meta"])
        number = chunking.number_of(row["doc_id"])
        amending = int(bool(chunking.AMENDING.search(title)))
        acts[row["doc_id"]] = {"status": row["list_state"], "title": title}
        con.execute("INSERT INTO acts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            row["doc_id"], number, title, kind, chunking.rank_of(kind, row["list_meta"], row["section"]), amending, row["section"],
            STATUS.get(row["list_state"]), iso(row["adopted"]), iso(row["edition"]) or iso(row["adopted"]),
            f"https://lex.uz/docs/{row['text_page']}", row["text_lang"], row["year"], row["list_meta"]))
    con.executemany("INSERT INTO fts_acts (rowid, title) SELECT rowid, ? FROM acts WHERE doc_id = ?",
                    [(" ".join(text.tokens(a["title"])), d) for d, a in acts.items()])
    return acts


def documents():
    """One document at a time, straight from the row groups, so memory stays flat however big the base gets."""
    source = pq.ParquetFile(PARQUET / "elements.parquet")
    columns = ["element_id", "doc_id", "seq", "kind", "is_body", "text", "headers", "appendix", "article", "article_title", "part", "band"]
    rows = (row for batch in source.iter_batches(batch_size=20000, columns=columns) for row in batch.to_pylist())
    for doc_id, elements in itertools.groupby(rows, key=lambda r: r["doc_id"]):
        yield doc_id, sorted(elements, key=lambda r: r["seq"])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    temp = OUT / "lex.building.sqlite"
    temp.unlink(missing_ok=True)
    con = sqlite3.connect(temp)
    con.executescript("PRAGMA journal_mode = OFF; PRAGMA synchronous = OFF; PRAGMA cache_size = -200000;" + SCHEMA)
    acts = load_acts(con)
    started, total, chars = time.time(), 0, 0
    for n, (doc_id, elements) in enumerate(documents(), 1):
        act = acts.get(doc_id)
        if act is None:
            continue
        table = "fts_force" if act["status"] == "y" else "fts_old"
        title = " ".join(text.tokens(act["title"]))
        for chunk in chunking.chunks_of(doc_id, elements):
            total += 1
            chars += len(chunk["text"])
            con.execute("INSERT INTO chunks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                total, chunk["chunk_id"], chunk["doc_id"], chunk["seq"], chunk["piece"], chunk["text"], chunk["article"], chunk["part"],
                chunk["article_title"], chunk["appendix"], chunk["headers"], chunk["element_ids"], int(chunk["is_table"])))
            head = " ".join(filter(None, (chunk["article"], chunk["article_title"], chunk["headers"])))
            con.execute(f"INSERT INTO {table} (rowid, title, head, body) VALUES (?,?,?,?)",
                        (total, title, " ".join(text.tokens(head)), " ".join(text.tokens(chunk["text"]))))
        if n % 5000 == 0:
            con.commit()
            print(f"{n} documents, {total} chunks, {chars / 1e6:.0f}M chars, {time.time() - started:.0f}s", flush=True)
    snapshot = store.connect().execute("SELECT max(substr(fetched_at, 1, 10)) FROM docs").fetchone()[0]
    con.executemany("INSERT INTO meta VALUES (?, ?)", [("index_version", f"lex-idx-{dt.date.today().isoformat()}"), ("lex_snapshot_date", snapshot)])
    print("indexes", flush=True)
    con.executescript("""CREATE UNIQUE INDEX chunks_id ON chunks (chunk_id);
                         CREATE INDEX chunks_doc ON chunks (doc_id, seq, piece);
                         CREATE INDEX acts_type ON acts (doc_type, status);
                         CREATE TABLE spans AS SELECT doc_id, min(id) first, max(id) last FROM chunks GROUP BY doc_id;
                         CREATE UNIQUE INDEX spans_doc ON spans (doc_id);
                         INSERT INTO fts_force (fts_force) VALUES ('optimize');
                         INSERT INTO fts_old (fts_old) VALUES ('optimize');""")
    con.commit()
    con.close()
    temp.replace(OUT / "lex.sqlite")
    print("chunks", total, "size GB", round((OUT / "lex.sqlite").stat().st_size / 1e9, 2), f"{time.time() - started:.0f}s")


if __name__ == "__main__":
    main()
