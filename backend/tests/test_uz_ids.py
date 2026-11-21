"""Uzbek identifiers (F-33): valid formats with a matching parameter name are found; random IDs are not."""

import random

from qalqon.enrich.entities import identify
from qalqon.uz_ids import find_in_url, is_card, is_pinfl, luhn_ok


def _luhn_complete(prefix15: str) -> str:
    for d in "0123456789":
        if luhn_ok(prefix15 + d):
            return prefix15 + d
    raise AssertionError


def test_pinfl_structure():
    assert is_pinfl("31503901234567")       # man, born 15.03.1990
    assert not is_pinfl("31513901234567")   # month 13
    assert not is_pinfl("71503901234567")   # first digit out of range
    assert not is_pinfl("3150390123456")    # 13 digits


def test_cards_need_luhn_and_uzbek_prefix_or_name():
    uzcard = _luhn_complete("860012345678901")
    assert is_card(uzcard, hinted=False)
    visa = _luhn_complete("411111111111111")
    assert not is_card(visa, hinted=False) and is_card(visa, hinted=True)
    assert not is_card(uzcard[:-1] + str((int(uzcard[-1]) + 1) % 10), hinted=True)  # broken check digit


def test_find_in_url_requires_names_for_ids():
    url = ("https://t.example.com/c?pinfl=31503901234567&passport_no=AA1234567&id=31503901234567"
           "&ref=AB1234567&phone=998901234567&email=a.b@mail.uz&card=" + _luhn_complete("986012345678901"))
    kinds = {(f["kind"], f["param"]) for f in find_in_url(url)}
    assert ("pinfl", "pinfl") in kinds and ("passport", "passport_no") in kinds
    assert ("pinfl", "id") not in kinds and ("passport", "ref") not in kinds  # no hint → ignored
    assert ("phone", "phone") in kinds and ("email", "email") in kinds and ("card", "card") in kinds
    assert all("***" in f["sample"] for f in find_in_url(url))  # never the full value


def test_random_ids_are_not_personal_data():
    rng = random.Random(7)
    hits = 0
    for _ in range(2000):
        value = "".join(rng.choice("0123456789") for _ in range(rng.choice([14, 16])))
        hits += len(find_in_url(f"https://t.example.com/p?uid={value}&cid={value}"))
    assert hits <= 4  # only a valid Uzcard/Humo number could match (prefix 8600/9860 + Luhn: ~0.002%)


def test_ai_services_are_in_the_catalog():
    assert identify("api.openai.com")["category"] == "ai"
    assert identify("generativelanguage.googleapis.com")["category"] == "ai"
    assert identify("fonts.googleapis.com")["category"] == "fonts"


def test_redaction_before_llm_keeps_numbers_that_are_not_personal_data():
    """F-48: e-mails, phones, PINFL, passport and card numbers never reach the LLM; prices, dates, STIR stay."""
    from qalqon.uz_ids import redact
    text = ("Murojaat: dpo@shop.uz, +998 71 123-45-67, 78 888 9 888. PINFL 31503901234567, pasport AA1234567. "
            "Narx 1 800 000 soʻm, 05.11.2026, STIR 301234567.")
    out, counts = redact(text)
    assert "dpo@shop.uz" not in out and "31503901234567" not in out and "AA1234567" not in out
    assert counts["PHONE"] == 2 and counts["EMAIL"] == 1
    assert "1 800 000" in out and "05.11.2026" in out and "301234567" in out


def test_policy_prompt_is_redacted(monkeypatch):
    from qalqon.llm import policy
    sent = {}

    class Result:
        data = {"language": "uz", "is_personal_data_policy": True, "elements": {}, "claims": []}
        model = "test"
        cached = False
        usage = {}

    def fake_call(system, user, schema, version):
        sent["user"] = user
        return Result()

    monkeypatch.setattr(policy, "structured_call", fake_call)
    monkeypatch.setattr(policy, "configured", lambda: True)
    facts = {"site": "https://s.uz", "documents": [{"kind": "privacy", "url": "https://s.uz/p", "visited": True,
                                                   "text": "Maxfiylik siyosati. Masʼul shaxs: ali@s.uz, +998 90 123 45 67. " * 60}]}
    result = policy.analyze_policy(facts)
    assert "ali@s.uz" not in sent["user"] and "[EMAIL]" in sent["user"]
    assert result.get("redacted_before_llm", {}).get("EMAIL", 0) >= 1
