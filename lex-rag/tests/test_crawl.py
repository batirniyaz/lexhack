"""What an unattended run does when things go wrong."""
import asyncio
import itertools
import sqlite3
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lexuz.client import Blocked, PageFailed, SiteDown  # noqa: E402
from scripts import crawl  # noqa: E402


class FakeClient:
    pace = SimpleNamespace(rate=4, slowdowns=0)

    async def close(self):
        pass


def pool(job, items):
    return asyncio.run(crawl.run_pool(FakeClient(), SimpleNamespace(commit=lambda: None), items, job, rate=1))


def test_a_skipped_item_does_not_end_the_pool():
    finished = []

    async def job(item):
        if item == 2:
            raise PageFailed("bad page")
        finished.append(item)

    assert pool(job, [1, 2, 3, 4]) is None
    assert sorted(finished) == [1, 3, 4]


def test_the_pool_reports_what_stopped_it_and_takes_nothing_more():
    started = []

    async def job(item):
        started.append(item)
        raise OSError("disk full")

    stopped_by = pool(job, [1, 2, 3, 4, 5, 6])
    assert isinstance(stopped_by, OSError)
    assert len(started) <= 2


def fetch_from(monkeypatch, docs, page):
    """Runs the document pass against a fake site that gives the same page every time; returns the urls tried and the database."""
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE docs (doc_id TEXT, doc_status TEXT, pilot INT, card_status TEXT, fetched_at TEXT)")
    con.executemany("INSERT INTO docs (doc_id, doc_status) VALUES (?, ?)", docs)
    tried = []

    class Site(FakeClient):
        def __init__(self, *_):
            pass

        async def fetch(self, _, url):
            tried.append(url)
            return page

    monkeypatch.setattr(crawl.store, "connect", lambda: con)
    monkeypatch.setattr(crawl.store, "logger", lambda _: None)
    monkeypatch.setattr(crawl.store, "save_raw", lambda *_: None)
    monkeypatch.setattr(crawl, "Client", Site)
    asyncio.run(crawl.run_fetch(SimpleNamespace(pilot=False, seed=7, limit=None, rate=1, cards=False)))
    return tried, con


def test_documents_marked_missing_are_tried_again(monkeypatch):
    tried, _ = fetch_from(monkeypatch, [("1", "ok"), ("2", "missing"), ("3", "pending")], None)
    assert sorted(tried) == ["/uz/docs/2", "/uz/docs/3"]


def test_an_empty_shell_is_not_counted_as_a_document(monkeypatch):
    _, con = fetch_from(monkeypatch, [("1", "pending")], SimpleNamespace(content=b"<html>requisites only</html>"))
    assert con.execute("SELECT doc_status FROM docs").fetchone() == ("missing",)


def test_a_page_with_the_text_block_is_kept(monkeypatch):
    _, con = fetch_from(monkeypatch, [("1", "pending")], SimpleNamespace(content=b'<div id="divCont">text</div>'))
    assert con.execute("SELECT doc_status FROM docs").fetchone() == ("ok",)


def run_all_with(monkeypatch, fetch_results):
    """Plays an unattended run with scripted outcomes, all clean once they run out, and returns the steps it took."""
    steps = []
    fetches, cards = itertools.chain(fetch_results, itertools.repeat(None)), itertools.repeat(None)

    async def fetch(_):
        steps.append("fetch")
        return next(fetches)

    async def fetch_cards(_):
        steps.append("cards")
        return next(cards)

    monkeypatch.setattr(crawl, "run_fetch", fetch)
    monkeypatch.setattr(crawl, "run_cards", fetch_cards)
    monkeypatch.setattr(crawl, "report", lambda _: steps.append("report"))
    monkeypatch.setattr(crawl, "keep_awake", lambda: None)
    monkeypatch.setattr(crawl, "PAUSE", 0)
    asyncio.run(crawl.run_all(None))
    return steps


def test_a_clean_run_makes_two_rounds_of_documents_and_cards(monkeypatch):
    assert run_all_with(monkeypatch, []) == ["fetch", "cards", "fetch", "cards", "report"]


def test_a_silent_site_gets_another_try(monkeypatch):
    assert run_all_with(monkeypatch, [SiteDown("down")]) == ["fetch", "fetch", "cards", "fetch", "cards", "report"]


def test_a_refusal_ends_the_run(monkeypatch):
    assert run_all_with(monkeypatch, [Blocked("no")]) == ["fetch"]


def test_patience_runs_out(monkeypatch):
    steps = run_all_with(monkeypatch, [SiteDown("down")] * (crawl.PATIENCE + 1))
    assert steps == ["fetch"] * (crawl.PATIENCE + 1)
