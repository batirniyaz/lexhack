"""The checker itself: a reply built by the real pipeline and API passes, and each way of breaking the spec is caught."""
import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(ROOT / "tests"))
import run_eval  # noqa: E402
import structure  # noqa: E402
from api.journal import Journal  # noqa: E402
from api.main import Batches, create_app  # noqa: E402
from rag.llm import Model  # noqa: E402
from rag.pipeline import Pipeline  # noqa: E402
from test_api import SYSTEM  # noqa: E402
from test_pipeline import LAW, OTHER, FakeModel, FakeSearch, reply, row  # noqa: E402

KEY = "k"


class Always(FakeModel):
    """Answers every question it is shown, and says "no answer" to the one that asks for it."""

    def __init__(self):
        super().__init__([])

    def answer(self, prompt):
        wanted = "palov" not in prompt
        self.replies = [reply("Eng kam taʼtil yigirma bir kalendar kun [C1].", [("C1", "yigirma bir kalendar kunni tashkil etadi")]) if wanted else reply("", verdict="no_answer", ranking=())]
        return super().answer(prompt)


def request():
    items = [{"id": "q001", "question": "Yillik taʼtil qancha?", "language": "uz-Latn"}, {"id": "q002", "question": "palov qanday pishiriladi?", "language": "uz-Latn"}]
    return {"run_id": "r1", "batch_id": "r1-b01", "batch_index": 1, "total_batches": 1, "options": {"top_k": 5, "return_debug": True}, "items": items}


@pytest.fixture
def client(tmp_path):
    pipeline = Pipeline(FakeSearch([row(1, LAW), row(2, OTHER, article="130-modda")]), Always())
    app = create_app(pipeline=pipeline, system=SYSTEM, key=KEY, batches=Batches(tmp_path / "b.sqlite"), journal=Journal(tmp_path / "l.sqlite"), facts={"documents": 1})
    with TestClient(app, headers={"Authorization": f"Bearer {KEY}"}) as test:
        yield test


@pytest.fixture
def sent(client):
    body = request()
    return body, client.post("/v1/rag/batch", json=body).json()


def good(reply_body):
    return copy.deepcopy(reply_body)


def test_a_reply_of_the_api_holds(sent):
    body, reply = sent
    assert structure.check(body, reply) == []
    assert [r["status"] for r in reply["results"]] == ["ok", "no_answer"]


def test_rules_around_a_batch_hold(client, sent):
    body, reply = sent
    assert structure.protocol(client, body, reply) == []


def answered(reply):
    return next(r for r in reply["results"] if r["status"] == "ok")


@pytest.mark.parametrize("damage, word", [
    (lambda r: r.pop("system"), "no system"),
    (lambda r: r["system"].pop("index_version"), "no index_version"),
    (lambda r: r["results"].pop(), "ids"),
    (lambda r: r["summary"].update(ok=99), "summary"),
    (lambda r: answered(r)["contexts"].clear(), "not in contexts"),
    (lambda r: answered(r)["citations"][0].update(quote="boshqa matn"), "quote"),
    (lambda r: answered(r)["citations"][0].update(doc_id="6257288"), "doc_id"),
    (lambda r: answered(r)["citations"][0].update(url="https://lex.uz/docs/1"), "url"),
    (lambda r: answered(r)["citations"][0].update(edition_date="06.11.2026"), "edition_date"),
    (lambda r: answered(r).update(answer="Javob [7]."), "marks"),
    (lambda r: answered(r).update(no_answer=True), "no_answer"),
    (lambda r: answered(r)["contexts"][0].update(rank=3), "rank"),
    (lambda r: answered(r)["contexts"][0].update(used_in_answer=False), "used_in_answer"),
    (lambda r: answered(r).pop("timing"), "timing"),
])
def test_a_broken_reply_is_caught(sent, damage, word):
    body, reply = sent
    broken = good(reply)
    damage(broken)
    assert any(word in line for line in structure.check(body, broken)), word


def test_a_failed_question_needs_its_error():
    failed = {"id": "q", "status": "error", "answer": None, "no_answer": False, "citations": [], "contexts": [], "error": {"code": "LLM_ERROR", "message": "x", "retryable": True}}
    assert structure.check_result(failed, 5) == []
    assert structure.check_result({**failed, "error": {"code": "LLM_ERROR", "message": "x"}}, 5)


def test_fingerprint_follows_the_model():
    base = Model("a", "low", client=object())
    assert base.fingerprint == Model("a", "low", client=object()).fingerprint
    assert base.fingerprint != Model("b", "low", client=object()).fingerprint
    assert base.fingerprint != Model("a", "high", client=object()).fingerprint


def scored(answer, **item):
    return run_eval.correct({"keys": [["21", "yigirma bir"]], **item}, {"answer": answer, "no_answer": False})


def test_digits_and_words_are_one_fact():
    assert scored("Taʼtil 21 kalendar kun.") and scored("Taʼtil yigirma bir kalendar kun.")


def test_a_year_is_not_the_number_asked_for():
    assert not scored("Kodeks 2021-yilda qabul qilingan.")


def test_every_group_has_to_be_there():
    assert not scored("Taʼtil 21 kun.", keys=[["21"], ["kalendar"]])
    assert scored("Taʼtil 21 kalendar kun.", keys=[["21"], ["kalendar"]])


def test_the_stale_value_fails_the_answer():
    assert not scored("Taʼtil 15 ish kuni, yaʼni 21 emas.", must_not=["15"])


def test_a_year_does_not_trip_the_stale_value():
    assert scored("Kodeks 2015-yildan keyin 21 kun deydi.", must_not=["15"])


def test_russian_and_cyrillic_answers():
    assert run_eval.correct({"keys": [["три года"]]}, {"answer": "Срок составляет три года.", "no_answer": False})
    assert run_eval.correct({"keys": [["21"]]}, {"answer": "Двадцать один календарный день.", "no_answer": False})
    assert run_eval.correct({"keys": [["kalendar"]]}, {"answer": "Йигирма бир календарь кун.", "no_answer": False})


def test_the_old_gold_format_still_works():
    assert run_eval.correct({"key": "yigirma bir"}, {"answer": "Yigirma bir kun.", "no_answer": False})
