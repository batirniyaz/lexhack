"""The checklist of the spec, against a fake pipeline: no index and no model needed."""
import sys
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import main  # noqa: E402

KEY = "test-key"
AUTH = {"Authorization": f"Bearer {KEY}"}
SYSTEM = {"pipeline_version": "0", "llm_model": "m", "embedding_model": "e", "reranker": None, "index_version": "i", "lex_snapshot_date": "2026-11-05"}


class Fake:
    def __init__(self):
        self.calls = []
        self.fail_once = set()

    def answer(self, item, options, trace=None):
        self.calls.append(item["id"])
        if item["question"] == "boom":
            raise RuntimeError("boom")
        if item["id"] in self.fail_once:
            self.fail_once.discard(item["id"])
            return {"id": item["id"], "status": "error", "answer": None, "no_answer": False, "citations": [], "contexts": [],
                    "error": {"code": "LLM_TIMEOUT", "message": "x", "retryable": True}}
        if item["question"] == "yoq":
            return {"id": item["id"], "status": "no_answer", "answer": "topilmadi", "no_answer": True, "citations": [], "contexts": [], "error": None}
        return {"id": item["id"], "status": "ok", "answer": item["question"], "no_answer": False, "citations": [], "contexts": [], "error": None}


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "RATE_PER_SECOND", 1000)
    fake = Fake()
    app = main.create_app(pipeline=fake, system=SYSTEM, key=KEY, batches=main.Batches(tmp_path / "b.sqlite"), journal=main.Journal(tmp_path / "l.sqlite"), facts={"documents": 1})
    with TestClient(app) as client:
        yield client, fake


def batch(n=2, batch_id="b1", **extra):
    items = [{"id": f"q{i:03}", "question": f"savol {i}", "language": "uz-Latn"} for i in range(1, n + 1)]
    return {"run_id": "r1", "batch_id": batch_id, "batch_index": 1, "total_batches": 10, "items": items, **extra}


def test_batch_returns_every_question_once(setup):
    client, _ = setup
    reply = client.post("/v1/rag/batch", json=batch(10), headers=AUTH)
    assert reply.status_code == 200
    body = reply.json()
    assert [r["id"] for r in body["results"]] == [f"q{i:03}" for i in range(1, 11)]
    assert body["status"] == "completed" and body["system"] == SYSTEM
    assert body["summary"] == {"total": 10, "ok": 10, "no_answer": 0, "error": 0}
    assert {"received_at", "completed_at", "total_ms"} <= set(body["timing"])


def test_content_type_says_utf8(setup):
    client, _ = setup
    assert "charset=utf-8" in client.post("/v1/rag/batch", json=batch(), headers=AUTH).headers["content-type"]


def test_apostrophes_survive(setup):
    client, _ = setup
    body = batch(1)
    body["items"][0]["question"] = "Ta'til oʻgʻil gʻ ʻ qancha?"
    assert client.post("/v1/rag/batch", json=body, headers=AUTH).json()["results"][0]["answer"] == "Ta'til oʻgʻil gʻ ʻ qancha?"


@pytest.mark.parametrize("change", [
    lambda b: b.update(items=b["items"] * 6),
    lambda b: b.update(items=[]),
    lambda b: b["items"].append(dict(b["items"][0])),
    lambda b: b["items"][0].update(question="   "),
    lambda b: b["items"][0].update(question="x" * 2001),
    lambda b: b.pop("batch_id"),
    lambda b: b.pop("batch_index"),
    lambda b: b.update(options={"top_k": 0}),
    lambda b: b.update(options={"answer_language": "en"}),
    lambda b: b.update(options={"as_of_date": "01.11.2026"}),
])
def test_bad_requests_are_400(setup, change):
    client, _ = setup
    body = batch(2)
    change(body)
    assert client.post("/v1/rag/batch", json=body, headers=AUTH).status_code == 400


def test_eleven_questions_are_400(setup):
    client, _ = setup
    assert client.post("/v1/rag/batch", json=batch(11), headers=AUTH).status_code == 400


def test_broken_json_is_400(setup):
    client, _ = setup
    assert client.post("/v1/rag/batch", content=b"{nope", headers=AUTH).status_code == 400


def test_no_key_and_wrong_key(setup):
    client, _ = setup
    assert client.post("/v1/rag/batch", json=batch()).status_code == 401
    assert client.post("/v1/rag/batch", json=batch(), headers={"Authorization": "Bearer nope"}).status_code == 403
    assert client.get("/v1/meta").status_code == 401


def test_same_batch_is_not_computed_again(setup):
    client, fake = setup
    first = client.post("/v1/rag/batch", json=batch(), headers=AUTH).json()
    calls = len(fake.calls)
    second = client.post("/v1/rag/batch", json=batch(), headers=AUTH).json()
    assert second == first
    assert len(fake.calls) == calls


def test_same_id_with_other_content_is_409(setup):
    client, _ = setup
    client.post("/v1/rag/batch", json=batch(2), headers=AUTH)
    assert client.post("/v1/rag/batch", json=batch(3), headers=AUTH).status_code == 409


def test_stored_batch_can_be_read_back(setup):
    client, _ = setup
    first = client.post("/v1/rag/batch", json=batch(), headers=AUTH).json()
    assert client.get("/v1/rag/batch/b1", headers=AUTH).json() == first
    assert client.get("/v1/rag/batch/nothing", headers=AUTH).status_code == 404


def test_one_crash_stays_in_its_question(setup):
    client, _ = setup
    body = batch(3)
    body["items"][1]["question"] = "boom"
    reply = client.post("/v1/rag/batch", json=body, headers=AUTH)
    assert reply.status_code == 200
    statuses = [r["status"] for r in reply.json()["results"]]
    assert statuses == ["ok", "error", "ok"]
    assert reply.json()["results"][1]["error"]["code"]
    assert reply.json()["summary"]["error"] == 1


def test_no_answer_is_counted(setup):
    client, _ = setup
    body = batch(2)
    body["items"][0]["question"] = "yoq"
    assert client.post("/v1/rag/batch", json=body, headers=AUTH).json()["summary"] == {"total": 2, "ok": 1, "no_answer": 1, "error": 0}


def test_wrong_language_is_that_questions_error(setup):
    client, _ = setup
    body = batch(2)
    body["items"][0]["language"] = "fr"
    reply = client.post("/v1/rag/batch", json=body, headers=AUTH)
    assert reply.status_code == 200
    assert reply.json()["results"][0]["error"]["code"] == "INVALID_LANGUAGE"
    assert reply.json()["results"][1]["status"] == "ok"


def test_retry_after_a_retryable_error_computes_again(setup):
    client, fake = setup
    fake.fail_once = {"q001"}
    first = client.post("/v1/rag/batch", json=batch(), headers=AUTH).json()
    assert first["results"][0]["status"] == "error"
    second = client.post("/v1/rag/batch", json=batch(), headers=AUTH).json()
    assert second["results"][0]["status"] == "ok"


def test_slow_batch_turns_async(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "SYNC_LIMIT", 0.05)
    monkeypatch.setattr(main, "RATE_PER_SECOND", 1000)

    class Slow(Fake):
        def answer(self, item, options, trace=None):
            time.sleep(0.4)
            return super().answer(item, options, trace)

    app = main.create_app(pipeline=Slow(), system=SYSTEM, key=KEY, batches=main.Batches(tmp_path / "b.sqlite"), journal=main.Journal(tmp_path / "l.sqlite"))
    with TestClient(app) as client:
        reply = client.post("/v1/rag/batch", json=batch(), headers=AUTH)
        assert reply.status_code == 202
        assert reply.json() == {"batch_id": "b1", "status": "processing"}
        assert client.get("/v1/rag/batch/b1", headers=AUTH).json()["status"] == "processing"
        time.sleep(0.8)
        assert client.get("/v1/rag/batch/b1", headers=AUTH).json()["status"] == "completed"


def test_too_fast_is_429_with_retry_after(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "RATE_PER_SECOND", 1)
    app = main.create_app(pipeline=Fake(), system=SYSTEM, key=KEY, batches=main.Batches(tmp_path / "b.sqlite"), journal=main.Journal(tmp_path / "l.sqlite"))
    with TestClient(app) as client:
        assert client.post("/v1/rag/batch", json=batch(batch_id="x1"), headers=AUTH).status_code == 200
        reply = client.post("/v1/rag/batch", json=batch(batch_id="x2"), headers=AUTH)
        assert reply.status_code == 429
        assert reply.headers["retry-after"] == "1"


def test_app_key_has_no_batch_limit_and_its_own_source(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "RATE_PER_SECOND", 1)
    journal = main.Journal(tmp_path / "l.sqlite")
    app = main.create_app(pipeline=Fake(), system=SYSTEM, key=KEY, app_key="app-key", batches=main.Batches(tmp_path / "b.sqlite"), journal=journal)
    mine = {"Authorization": "Bearer app-key"}
    with TestClient(app) as client:
        for n in range(4):
            assert client.post("/v1/rag/batch", json=batch(batch_id=f"a{n}"), headers=mine).status_code == 200
        assert client.post("/v1/rag/batch", json=batch(batch_id="t1"), headers=AUTH).status_code == 200   # the app did not use up the tester's second
        assert client.post("/v1/rag/batch", json=batch(batch_id="t2"), headers=AUTH).status_code == 429
        assert client.post("/v1/rag/query", json={"question": "savol"}, headers=mine).status_code == 200
        assert client.get("/v1/meta", headers=mine).status_code == 200
    sources = [r["source"] for r in journal.runs({}, limit=100)["rows"]]
    assert sources.count("app") == 4 * 2 + 1 and sources.count("batch") == 2


def test_without_an_app_key_an_empty_one_opens_nothing(setup):
    client, _ = setup
    assert client.post("/v1/rag/query", json={"question": "savol"}, headers={"Authorization": "Bearer "}).status_code in (401, 403)
    assert client.post("/v1/rag/query", json={"question": "savol"}, headers={"Authorization": "Bearer None"}).status_code == 403


def test_meta_and_health(setup):
    client, _ = setup
    assert client.get("/v1/health").json()["status"] == "ok"
    meta = client.get("/v1/meta", headers=AUTH).json()
    assert meta["index_version"] == "i" and meta["lex_snapshot_date"] == "2026-11-05" and meta["documents"] == 1


def test_single_question(setup):
    client, _ = setup
    reply = client.post("/v1/rag/query", json={"question": "savol"}, headers=AUTH)
    assert reply.status_code == 200 and reply.json()["result"]["status"] == "ok"
    assert client.post("/v1/rag/query", json={"question": ""}, headers=AUTH).status_code == 400
