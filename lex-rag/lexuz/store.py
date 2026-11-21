"""Crawl state in SQLite and raw pages on disk, so a stopped crawl continues where it ended."""
import gzip
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW = DATA / "raw"

SCHEMA = """
CREATE TABLE IF NOT EXISTS lists(
  section TEXT, year INTEGER, expected INTEGER, found INTEGER DEFAULT 0, pages INTEGER DEFAULT 0, done INTEGER DEFAULT 0,
  PRIMARY KEY(section, year));
CREATE TABLE IF NOT EXISTS docs(
  doc_id TEXT PRIMARY KEY, section TEXT, year INTEGER, title TEXT, meta TEXT, state TEXT, seen INTEGER DEFAULT 1,
  pilot INTEGER DEFAULT 0, doc_status TEXT DEFAULT 'pending', card_status TEXT DEFAULT 'pending', fetched_at TEXT);
CREATE TABLE IF NOT EXISTS requests(ts REAL, kind TEXT, status INTEGER, seconds REAL, bytes INTEGER, rate REAL);
CREATE INDEX IF NOT EXISTS docs_status ON docs(doc_status);
"""


def connect():
    DATA.mkdir(exist_ok=True)
    con = sqlite3.connect(DATA / "crawl.sqlite")
    con.executescript(SCHEMA)
    con.execute("PRAGMA journal_mode=WAL")
    return con


def raw_path(kind, doc_id):
    """Sharded, because one folder with fifty thousand files is slow on Windows."""
    number = str(doc_id).lstrip("-")
    return RAW / kind / number[-2:].zfill(2) / f"{doc_id}.html.gz"


def save_raw(kind, doc_id, content):
    path = raw_path(kind, doc_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_bytes(gzip.compress(content, 6))
    temp.replace(path)   # a crash mid-write must not leave half a page that looks finished


def load_raw(kind, doc_id):
    return gzip.decompress(raw_path(kind, doc_id).read_bytes()).decode("utf-8", "replace")


def logger(con):
    def log(kind, status, seconds, size, rate):
        con.execute("INSERT INTO requests VALUES (?,?,?,?,?,?)", (time.time(), kind, status, seconds, size, rate))
    return log
