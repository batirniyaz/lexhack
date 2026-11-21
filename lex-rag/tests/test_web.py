"""The public page, its limits, and the journal behind /logs. A fake pipeline: no index, no model, no money."""
import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import main  # noqa: E402
from api.journal import Journal, cost  # noqa: E402
from rag.pipeline import Trace  # noqa: E402

KEY = "test-key"
AUTH = {"Authorization": f"Bearer {KEY}"}
SYSTEM = {"pipeline_version": "0", "llm_model": "claude-haiku-5-5", "embedding_model": "e", "reranker": None, "index_version": "i", "lex_snapshot_date": "2026-11-06"}
CITATION = {"ref": 1, "doc_title": "Mehnat kodeksi", "url": "https://lex.uz/docs/-6257288", "article": "219-modda", "part": None, "quote": "yigirma bir", "doc_status": "amalda", "chunk_id": "c"}


class Fake:
    def answer(self, item, options, trace=None):
        trace = trace or Trace()
        if item["question"] == "kesh":
            trace.cached = True
        with trace.span("read"):
            trace.plan = {"query": "taʼtil", "terms": ["taʼtil"], "acts": []}
        with trace.span("search"):
            trace.found = 60
        with trace.span("answer"):
            pass
        return {"id": item["id"], "status": "ok", "answer": "21 kun [1]", "answer_language": "uz-Latn", "no_answer": False, "citations": [CITATION], "contexts": [{"text": "x"}],
                "usage": {"input_tokens": 1000, "output_tokens": 100}, "error": None}


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "RATE_PER_SECOND", 1000)
    journal = Journal(tmp_path / "l.sqlite")
    app = main.create_app(pipeline=Fake(), system=SYSTEM, key=KEY, batches=main.Batches(tmp_path / "b.sqlite"), journal=journal,
                          facts={"with_text": 45892, "in_force": 31488})
    with TestClient(app) as client:
        yield client, journal


def ask(client, question="savol", address="1.1.1.1"):
    return client.post("/api/ask", json={"question": question}, headers={"cf-connecting-ip": address})


def lines(reply):
    return [json.loads(line) for line in reply.text.splitlines()]


def batch(run_id="r1"):
    return {"run_id": run_id, "batch_id": f"{run_id}-b1", "batch_index": 1, "total_batches": 1, "items": [{"id": "f01", "question": "savol"}]}


def test_the_page_and_its_files_need_no_key(setup):
    client, _ = setup
    page = client.get("/")
    assert page.status_code == 200 and "text/html" in page.headers["content-type"] and 'id="ask"' in page.text
    assert client.get("/style.css").status_code == 200
    assert client.get("/app.js").status_code == 200


@pytest.mark.parametrize("path", ["/", "/logs", "/v1/health"])
def test_a_check_of_the_headers_finds_the_site_up(setup, path):
    client, _ = setup
    assert client.head(path).status_code == 200


def test_the_docs_list_every_route_once_in_order_and_ask_for_the_key(setup):
    client, _ = setup
    assert client.get("/docs").status_code == 200
    spec = client.get("/openapi.json").json()
    assert [t["name"] for t in spec["tags"]] == ["Проверка", "Сайт", "Журнал"]
    assert list(spec["paths"])[:5] == ["/v1/rag/batch", "/v1/rag/batch/{batch_id}", "/v1/rag/query", "/v1/meta", "/v1/health"]
    assert "/" not in spec["paths"] and "/logs" not in spec["paths"]
    assert spec["paths"]["/v1/rag/batch"]["post"]["security"] and "requestBody" in spec["paths"]["/v1/rag/batch"]["post"]
    assert "security" not in spec["paths"]["/v1/health"]["get"]
    assert all(route.get("summary") and route.get("tags") for path in spec["paths"].values() for route in path.values())


def test_the_key_button_changes_nothing_about_the_checks(setup):
    client, _ = setup
    assert client.post("/v1/rag/batch", json=batch()).status_code == 401
    assert client.post("/v1/rag/batch", json=batch(), headers={"Authorization": "Bearer wrong"}).status_code == 403


def test_the_readme_page_opens_and_the_home_page_leads_to_it(setup):
    client, _ = setup
    page = client.get("/readme")
    assert page.status_code == 200 and "<h1>Как устроена система</h1>" in page.text
    assert client.head("/readme").status_code == 200
    assert 'href="readme"' in client.get("/").text
    assert "/readme" not in client.get("/openapi.json").json()["paths"]


def test_nothing_on_the_page_holds_a_key():
    for path in main.WEB.glob("*.*"):
        text = path.read_text(encoding="utf-8")
        assert "Bearer" not in text and "LEX_API_KEY" not in text, path.name


def test_about_gives_only_the_public_numbers(setup):
    client, _ = setup
    assert client.get("/api/about").json() == {"with_text": 45892, "in_force": 31488, "snapshot": "2026-11-06"}


def test_a_question_streams_its_steps_and_then_the_answer(setup):
    client, _ = setup
    reply = ask(client)
    assert reply.status_code == 200 and reply.headers["content-type"].startswith("application/x-ndjson")
    events = lines(reply)
    assert [e["step"] for e in events[:-1]] == ["read", "search", "answer"]
    answer = events[-1]["answer"]
    assert answer["answer"] == "21 kun [1]" and answer["citations"][0]["article"] == "219-modda"


def test_the_page_gets_no_contexts_and_no_counts(setup):
    client, _ = setup
    assert set(lines(ask(client))[-1]["answer"]) == {"status", "answer", "language", "citations"}


@pytest.mark.parametrize("body", [{}, {"question": "   "}, {"question": 5}, {"question": "x" * 501}, []])
def test_a_wrong_question_is_400(setup, body):
    client, _ = setup
    assert client.post("/api/ask", json=body).status_code == 400


def test_one_address_is_stopped_and_another_is_not(setup, monkeypatch):
    monkeypatch.setattr(main, "ASK_PER_MINUTE", 2)
    client, _ = setup
    assert ask(client).status_code == 200 and ask(client).status_code == 200
    stopped = ask(client)
    assert stopped.status_code == 429 and stopped.json()["error"]["code"] == "RATE_LIMIT" and stopped.headers["retry-after"] == "60"
    assert ask(client, address="2.2.2.2").status_code == 200


def test_the_day_has_a_limit_for_everyone_together(setup, monkeypatch):
    monkeypatch.setattr(main, "ASK_PER_DAY", 2)
    client, _ = setup
    assert ask(client, address="1.1.1.1").status_code == 200 and ask(client, address="2.2.2.2").status_code == 200
    stopped = ask(client, address="3.3.3.3")
    assert stopped.status_code == 429 and stopped.json()["error"]["code"] == "DAILY_LIMIT"


def test_a_finished_answer_from_the_cache_does_not_count_for_the_day(setup, monkeypatch):
    monkeypatch.setattr(main, "ASK_PER_DAY", 1)
    client, _ = setup
    assert ask(client, "kesh").status_code == 200 and ask(client, "kesh").status_code == 200


def test_a_test_batch_does_not_use_up_the_questions_of_the_day(setup, monkeypatch):
    monkeypatch.setattr(main, "ASK_PER_DAY", 1)
    client, _ = setup
    assert client.post("/v1/rag/batch", json=batch(), headers=AUTH).status_code == 200
    assert ask(client).status_code == 200


@pytest.mark.parametrize("path", ["/logs", "/api/logs/summary", "/api/logs/runs"])
def test_logs_open_without_a_password(setup, path):
    client, _ = setup
    assert client.get(path).status_code == 200


def test_the_logs_page_stays_out_of_search(setup):
    client, _ = setup
    assert 'name="robots" content="noindex"' in client.get("/logs").text


def test_the_journal_keeps_every_way_in_and_no_address(setup):
    client, journal = setup
    ask(client)
    client.post("/v1/rag/query", json={"question": "savol"}, headers=AUTH)
    client.post("/v1/rag/batch", json=batch(), headers=AUTH)
    rows = client.get("/api/logs/runs").json()["rows"]
    assert sorted(r["source"] for r in rows) == ["api", "batch", "web"]
    assert "1.1.1.1" not in json.dumps(journal.detail(rows[-1]["id"]))


def test_one_answer_opens_with_its_sources_plan_and_price(setup):
    client, _ = setup
    ask(client)
    row = client.get("/api/logs/runs").json()["rows"][0]
    found = client.get(f"/api/logs/runs/{row['id']}").json()
    assert found["citations"][0]["quote"] == "yigirma bir" and found["plan"]["query"] == "taʼtil" and found["found"] == 60
    assert found["tokens_in"] == 1000 and found["cost_usd"] == cost("claude-haiku-5-5", 1000, 100) == 0.00015
    assert client.get("/api/logs/runs/999").status_code == 404


def test_an_answer_from_the_cache_costs_nothing_in_the_journal(setup):
    client, _ = setup
    ask(client, "kesh")
    row = client.get("/api/logs/runs").json()["rows"][0]
    assert row["cached"] == 1 and row["cost_usd"] == 0


def test_filters_narrow_the_list(setup):
    client, _ = setup
    ask(client, "taʼtil haqida")
    client.post("/v1/rag/batch", json=batch(), headers=AUTH)
    assert client.get("/api/logs/runs?source=web").json()["total"] == 1
    assert client.get("/api/logs/runs?q=haqida").json()["total"] == 1
    assert client.get("/api/logs/runs?outcome=error").json()["total"] == 0


def test_a_control_run_leaves_its_grades(setup):
    client, _ = setup
    client.post("/v1/rag/batch", json=batch(), headers=AUTH)
    marks = {"run_id": "r1", "verdicts": [{"id": "f01", "ok": False, "why": "нет ключа", "expected": "21 kun", "category": "faktik"}]}
    assert client.post("/api/logs/verdicts", json=marks).status_code == 401
    assert client.post("/api/logs/verdicts", json=marks, headers=AUTH).json() == {"marked": 1}
    row = client.get("/api/logs/runs?verdict=fail").json()["rows"][0]
    assert row["ok"] == 0 and row["expected"] == "21 kun" and row["why"] == "нет ключа"
    group = client.get("/api/logs/summary").json()["groups"][0]
    assert group["run_id"] == "r1" and group["judged"] == 1 and group["correct"] == 0


def test_the_summary_keeps_runs_apart_and_leaves_the_cache_out_of_the_timings(setup):
    client, _ = setup
    ask(client, "kesh")
    client.post("/v1/rag/batch", json=batch("r1"), headers=AUTH)
    client.post("/v1/rag/batch", json=batch("r2"), headers=AUTH)
    groups = {(g["source"], g["run_id"]): g for g in client.get("/api/logs/summary").json()["groups"]}
    assert set(groups) == {("web", None), ("batch", "r1"), ("batch", "r2")}
    assert groups[("web", None)]["cached"] == 1 and groups[("web", None)]["median_ms"] is None and groups[("web", None)]["times"] == []
    assert len(groups[("batch", "r1")]["times"]) == 1


def test_a_journal_that_fails_does_not_cost_the_answer(setup):
    client, journal = setup
    journal.con.execute("DROP TABLE runs")
    reply = client.post("/v1/rag/query", json={"question": "savol"}, headers=AUTH)
    assert reply.status_code == 200 and reply.json()["result"]["status"] == "ok"
