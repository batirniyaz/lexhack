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
    # HTTP clients normalize "/api/scans/../../etc" to "/etc" (now served by the SPA), so test the guard directly.
    import pytest
    from fastapi import HTTPException
    import qalqon.api as api_module
    with pytest.raises(HTTPException) as err:
        api_module._scan_dir("../../backend")
    assert err.value.status_code == 400


def test_frontend_route_never_serves_files_outside_dist():
    import qalqon.api as api_module
    if not api_module.FRONTEND_DIST.exists():
        return  # frontend not built in this environment
    response = client.get("/%2e%2e/%2e%2e/.env")
    assert response.status_code in (200, 404)
    assert "ANTHROPIC_API_KEY" not in response.text
    assert client.get("/api/does-not-exist").status_code == 404


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


def test_scan_rate_limit_and_access_key(monkeypatch):
    import qalqon.api as api_module
    from qalqon import guard

    monkeypatch.setattr(api_module.jobs, "start", lambda job: job)  # no real scan
    monkeypatch.setattr(guard, "PER_IP_HOUR", 2)
    guard.reset()
    target = {"url": "http://8.8.8.8"}  # public IP literal: no DNS needed
    assert client.post("/api/scans", json=target).status_code == 202
    assert client.post("/api/scans", json=target).status_code == 202
    assert client.post("/api/scans", json=target).status_code == 429

    guard.reset()
    monkeypatch.setattr(guard, "SCAN_KEY", "secret-key")
    assert client.post("/api/scans", json=target).status_code == 403
    assert client.post("/api/scans", json=target, headers={"X-Probo-Key": "secret-key"}).status_code == 202
    guard.reset()


def test_anonymize_hides_brand_aliases_in_quotes():
    report = {"quote": "Uzum Market maʼlumotlarni uchinchi shaxslarga bermaydi. UZUM Bank ham."}
    result = anonymize(report, ["uzum.uz"], "Marketplace A", ["Uzum Market", "Uzum Bank", "Uzum"])
    assert "uzum" not in result["quote"].lower()
    assert result["quote"].startswith("Marketplace A")
