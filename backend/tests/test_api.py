from fastapi.testclient import TestClient

from qalqon.api import app
from qalqon.presentation import anonymize

client = TestClient(app)


def test_health():
    body = client.get("/api/health").json()
    assert body["status"] == "ok"


def test_scan_refuses_private_targets():
    response = client.post("/api/scans", json={"url": "http://127.0.0.1:22"})
    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]


def test_scan_id_cannot_escape_scans_dir():
    assert client.get("/api/scans/../../etc").status_code in (400, 404)


def test_anonymize_hides_domains_everywhere():
    report = {"site": "https://shop.example.uz", "findings": [{"evidence": [{"summary": "Form on https://shop.example.uz/order"}]}]}
    result = anonymize(report, ["example.uz"], "Marketplace A")
    text = str(result)
    assert "example.uz" not in text and "marketplace-a" in text and result["label"] == "Marketplace A"


def _fake_scan(root, scan_id, when, score, rules):
    import json as _json
    d = root / scan_id
    d.mkdir(parents=True)
    report = {"scan_id": scan_id, "site": "https://shop.example.uz", "scanned_at": when, "status": "ok", "score": score,
              "levels": {"violation": 0, "risk": len(rules), "recommendation": 0}, "stats": {"pages": 1, "requests": 1},
              "findings": [{"rule_id": r, "level": "risk", "title": {"en": r}, "evidence": []} for r in rules],
              "flows": [], "not_evaluated": []}
    (d / "report.json").write_text(_json.dumps(report), encoding="utf-8")
    (d / "facts.json").write_text(_json.dumps({"site": report["site"], "site_domains": ["example.uz"]}), encoding="utf-8")


def test_site_history_diff_delta_and_share(tmp_path, monkeypatch):
    import qalqon.api as api_module
    monkeypatch.setattr(api_module, "SCANS_DIR", tmp_path)
    monkeypatch.setattr(api_module, "SHARES_FILE", tmp_path / ".shares.json")
    _fake_scan(tmp_path, "s1", "2026-11-20T10:00:00+00:00", 80, ["PD-TRK-01", "PD-CNS-01"])
    _fake_scan(tmp_path, "s2", "2026-11-21T10:00:00+00:00", 90, ["PD-TRK-01", "PD-REC-01"])

    rows = client.get("/api/scans").json()
    assert rows[0]["scan_id"] == "s2" and rows[0]["delta"] == 10 and rows[0]["domain"] == "example.uz"

    site = client.get("/api/sites/example.uz").json()
    assert [s["scan_id"] for s in site["scans"]] == ["s1", "s2"]
    assert [f["rule_id"] for f in site["diff"]["new"]] == ["PD-REC-01"]
    assert [f["rule_id"] for f in site["diff"]["fixed"]] == ["PD-CNS-01"]

    token = client.post("/api/scans/s2/share").json()["token"]
    assert client.post("/api/scans/s2/share").json()["token"] == token  # stable token
    shared = client.get(f"/api/shared/{token}").json()
    assert shared["report"]["score"] == 90 and shared["scan_id"] == "s2"
    assert client.get("/api/shared/not-a-token").status_code == 404


def test_anonymize_hides_brand_aliases_in_quotes():
    report = {"quote": "Uzum Market maʼlumotlarni uchinchi shaxslarga bermaydi. UZUM Bank ham."}
    result = anonymize(report, ["uzum.uz"], "Marketplace A", ["Uzum Market", "Uzum Bank", "Uzum"])
    assert "uzum" not in result["quote"].lower()
    assert result["quote"].startswith("Marketplace A")
