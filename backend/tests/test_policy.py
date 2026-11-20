"""Quote verification and policy-vs-behaviour logic, without calling the LLM."""

from qalqon.detectors.documents import policy_content, policy_vs_behavior
from qalqon.llm.policy import _norm, quote_found

POLICY_TEXT = ("Shaxsga doir maʼlumotlar faqat Oʻzbekiston Respublikasi hududidagi serverlarda saqlanadi. "
               "Biz maʼlumotlaringizni uchinchi shaxslarga bermaymiz. Saytda Google Analytics ishlatiladi.")


def test_quote_found_tolerates_quote_styles_and_whitespace():
    text = _norm(POLICY_TEXT)
    assert quote_found("Shaxsga doir ma'lumotlar faqat O'zbekiston  Respublikasi hududidagi serverlarda saqlanadi", text)
    assert quote_found("Shaxsga doir maʼlumotlar faqat … serverlarda saqlanadi", text)
    assert not quote_found("Maʼlumotlar Germaniyada saqlanadi", text)
    assert not quote_found(None, text)


def _facts(claims):
    return {
        "pages": [{"final_url": "https://shop.example.uz/", "challenge": None}],
        "uploads": [],
        "documents": [{"url": "https://shop.example.uz/privacy", "kind": "privacy", "visited": True, "text": POLICY_TEXT}],
        "hosts": [
            {"host": "shop.example.uz", "third_party": False, "server_country": "UZ", "is_cdn": False},
            {"host": "connect.facebook.net", "third_party": True, "category": "advertising", "entity": "Meta",
             "country": "US", "on_landing": True},
            {"host": "www.google-analytics.com", "third_party": True, "category": "analytics", "entity": "Google",
             "country": "US", "on_landing": True},
        ],
        "policy": {
            "status": "ok", "is_personal_data_policy": True,
            "documents": [{"url": "https://shop.example.uz/privacy", "kind": "privacy"}],
            "elements": {name: {"present": name != "retention", "label": name} for name in
                         ["operator", "purposes", "data_categories", "retention", "recipients", "cross_border",
                          "subject_rights", "contact"]},
            "claims": claims,
        },
    }


def test_contradictions_found_from_explicit_claims():
    claims = [
        {"type": "data_stored_in_uzbekistan", "quote": "faqat Oʻzbekiston Respublikasi hududidagi serverlarda saqlanadi",
         "statement_en": "Data stored only in Uzbekistan", "services": [], "countries": []},
        {"type": "no_third_party_sharing", "quote": "uchinchi shaxslarga bermaymiz",
         "statement_en": "No sharing", "services": [], "countries": []},
    ]
    evidence = policy_vs_behavior(_facts(claims), {})
    kinds = {e["data"]["claim_type"] for e in evidence}
    assert kinds == {"data_stored_in_uzbekistan", "no_third_party_sharing"}
    assert all("Policy says" in e["summary"] for e in evidence)


def test_promise_with_exceptions_is_downgraded():
    from qalqon.rules_engine import DOWNGRADE
    claims = [{"type": "no_third_party_sharing", "statement_en": "No sharing", "services": [], "countries": [],
               "quote": "Maʼlumotlar uchinchi shaxslarga berilmaydi, qonunchilikda nazarda tutilgan holatlar bundan mustasno."}]
    evidence = policy_vs_behavior(_facts(claims), {})
    assert evidence and all(e["data"]["downgrade"] for e in evidence)
    assert DOWNGRADE["violation"] == "risk"


def test_policy_content_reports_missing_elements_and_undisclosed_services():
    evidence = policy_content(_facts([]), {})
    summaries = " ".join(e["summary"] for e in evidence)
    assert "how long" not in summaries or "retention" in str(evidence)
    undisclosed = next(e for e in evidence if "never mentions" in e["summary"])
    assert [u["entity"] for u in undisclosed["data"]["undisclosed"]] == ["Meta"]  # Google is named in the text


def test_not_evaluated_without_policy_analysis():
    facts = _facts([])
    facts["policy"] = {"status": "no_document"}
    assert policy_vs_behavior(facts, {}) is None
    assert policy_content(facts, {}) is None
