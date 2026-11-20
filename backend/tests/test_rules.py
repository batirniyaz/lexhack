"""Detectors + rules engine on small hand-made facts (no browser needed)."""

from qalqon.legal_lists import country_status
from qalqon.rules_engine import evaluate, load_rules
from qalqon.scanner.analysis import analyze_form, classify_field


def _host(host, entity, country, category, landing=True, dpf=None):
    return {"host": host, "third_party": True, "on_landing": landing, "entity": entity, "country": country,
            "company_country": country, "server_country": country, "category": category, "dpf": dpf,
            "requests": 1, "ips": [], "methods": ["GET"], "asn": None, "org": None, "is_cdn": False}


def _facts(**extra):
    base = {"site": "https://shop.example.uz", "site_domains": ["example.uz"], "pages": [
        {"url": "https://shop.example.uz", "final_url": "https://shop.example.uz/", "status": 200,
         "headers": {}, "challenge": None, "title": "Shop"}],
        "requests": [], "cookies": [], "forms": [], "uploads": [], "permissions": [], "backends": [],
        "documents": [], "hosts": [], "session_replay": {"webvisor_pages": []}, "policy": {}, "blocked": None}
    base.update(extra)
    return base


def test_country_status_uses_list():
    assert country_status("UZ") == "local"
    assert country_status("RU") == "adequate"
    assert country_status("AE") == "not_listed"
    assert country_status("US", dpf=True) == "conditional_met"
    assert country_status("US", dpf=None) == "conditional_unknown"
    assert country_status(None) == "unknown"


def test_field_classification():
    assert classify_field({"type": "tel", "name": "x"}) == "phone"
    assert classify_field({"type": "text", "name": "jshshir", "label": ""}) == "pinfl"
    assert classify_field({"type": "text", "name": "q", "placeholder": "Qidirish"}) is None
    assert classify_field({"type": "file", "accept": "image/*", "capture": "user", "label": ""}) == "photo"


def test_rules_load_all_drafts():
    ids = {r["id"] for r in load_rules()}
    assert {"PD-LOC-01", "PD-TRK-01", "PD-CNS-01", "PD-MIS-01", "SEC-02"} <= ids


def test_findings_and_score():
    form = analyze_form({"action": None, "fields": [
        {"type": "text", "name": "fio", "label": "Ism", "placeholder": "", "id": "", "autocomplete": ""},
        {"type": "tel", "name": "phone", "label": "Telefon", "placeholder": "", "id": "", "autocomplete": ""},
    ], "consent": {"checkbox": None, "sentence": None, "policy_links": []}})
    form["pages"] = ["https://shop.example.uz/order"]
    facts = _facts(
        hosts=[_host("mc.yandex.ru", "Yandex", "RU", "analytics"),
               _host("connect.facebook.net", "Meta", "US", "advertising", dpf=None)],
        forms=[form],
        backends=[{"kind": "telegram-bot-api", "source": "app.js"}],
    )
    report = evaluate(facts)
    ids = {f["rule_id"] for f in report["findings"]}
    assert "PD-CNS-01" in ids            # form without consent
    assert "PD-TRK-01" in ids            # trackers on landing
    assert "PD-LOC-01" in ids            # telegram (AE) + personal-data form
    assert "PD-POL-01" in ids            # no policy
    loc02 = next(f for f in report["findings"] if f["rule_id"] == "PD-LOC-02")
    assert all(e["data"]["entity"] != "Yandex" for e in loc02["evidence"])  # RU is on the list -> not flagged
    assert {n["rule_id"] for n in report["not_evaluated"]} >= {"PD-MIS-01", "PD-POL-02"}
    assert 0 <= report["score"] < 100


def test_url_pii_ignores_bare_digit_runs():
    from qalqon.detectors.trackers import url_pii
    facts = {"requests": [
        {"third_party": True, "host": "ads.example", "url": "https://ads.example/p?id=998123456717&t=1"},
        {"third_party": True, "host": "track.example", "url": "https://track.example/c?phone=%2B998901234567"},
    ]}
    hits = url_pii(facts, {})
    assert [h["data"]["host"] for h in hits] == ["track.example"]


def test_identifier_only_login_form_is_not_a_consent_finding():
    from qalqon.detectors.forms import form_consent
    otp = analyze_form({"action": None, "buttons": ["Kod olish"], "fields": [
        {"type": "tel", "name": "phone", "label": "Telefon", "placeholder": "", "id": "", "autocomplete": ""}],
        "consent": {"checkbox": None, "sentence": None, "policy_links": []}})
    lead = analyze_form({"action": None, "buttons": ["Ariza qoldirish"], "fields": [
        {"type": "tel", "name": "phone", "label": "Telefon", "placeholder": "", "id": "", "autocomplete": ""}],
        "consent": {"checkbox": None, "sentence": None, "policy_links": []}})
    otp["pages"], lead["pages"] = ["https://a.uz/login"], ["https://a.uz/"]
    hits = form_consent({"forms": [otp, lead]}, {})
    assert [h["data"]["pages"][0] for h in hits] == ["https://a.uz/"]


def test_blocked_site_has_no_findings():
    report = evaluate(_facts(blocked="captcha"))
    assert report["status"] == "blocked" and report["findings"] == [] and report["score"] is None


def test_policy_coverage_levels():
    """F-17: product named / only company / only the kind (in a clause about services) / not named."""
    from qalqon.detectors.documents import policy_coverage
    text = ("Biz Yandex.Metrika hisoblagichidan foydalanamiz. Meta kompaniyasi ham. "
            "Reklama joylashtirish shartlari; veb-tahlil va analitik xizmatlar provayderlari cookie oladi.")
    facts = {
        "policy": {"status": "ok", "documents": [{"url": "https://s.uz/p"}]},
        "documents": [{"url": "https://s.uz/p", "text": text}],
        "hosts": [
            {"host": "mc.yandex.ru", "third_party": True, "entity": "Yandex", "country": "RU", "category": "analytics"},
            {"host": "connect.facebook.net", "third_party": True, "entity": "Meta", "country": "US", "category": "advertising"},
            {"host": "www.google-analytics.com", "third_party": True, "entity": "Google", "country": "US", "category": "analytics"},
            {"host": "ads.tiktok.com", "third_party": True, "entity": "TikTok / ByteDance", "country": "CN", "category": "advertising"},
        ],
    }
    levels = {row["entity"]: row["level"] for row in policy_coverage(facts)}
    assert levels == {"Yandex": "named", "Meta": "company", "Google": "kind", "TikTok / ByteDance": "none"}
