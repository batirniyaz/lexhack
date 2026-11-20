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


def test_scan_rate_limit_and_access_key(tmp_path, monkeypatch):
    import qalqon.api as api_module
    from qalqon import guard

    monkeypatch.setattr(api_module.jobs, "start", lambda job: job)  # no real scan
    monkeypatch.setattr(guard, "TOKENS_FILE", tmp_path / ".scan_tokens.json")
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


def test_public_mode_never_shows_real_site_names(tmp_path, monkeypatch):
    """D-003: in the public demo a visitor sees only scans they started; shared links and the sample are anonymized."""
    import json as _json
    import qalqon.api as api_module
    from qalqon import guard
    monkeypatch.setattr(api_module, "SCANS_DIR", tmp_path)
    monkeypatch.setattr(api_module, "SHARES_FILE", tmp_path / ".shares.json")
    monkeypatch.setattr(guard, "TOKENS_FILE", tmp_path / ".scan_tokens.json")
    monkeypatch.setattr(guard, "PUBLIC", True)
    monkeypatch.setattr(guard, "OWNER_KEY", "owner-key")
    monkeypatch.setattr(api_module.jobs, "start", lambda job: job)
    guard.reset()
    scan_id = "batch-1/uzum-uz"
    d = tmp_path / scan_id
    d.mkdir(parents=True)
    report = {"scan_id": scan_id, "site": "https://uzum.uz", "scanned_at": "2026-11-20T10:00:00+00:00",
              "status": "ok", "score": 79, "levels": {}, "stats": {}, "flows": [], "not_evaluated": [],
              "findings": [{"rule_id": "PD-MIS-01", "level": "violation", "title": {"en": "x"},
                            "evidence": [{"quote": "Uzum Market shares data only with Kapitalbank (kapitalbank.uz)",
                                          "url": "https://uzum.uz/privacy"}]}]}
    (d / "report.json").write_text(_json.dumps(report), encoding="utf-8")
    (d / "facts.json").write_text(_json.dumps({"site": "https://uzum.uz", "site_domains": ["uzum.uz", "www.uzum.uz"]}),
                                  encoding="utf-8")
    (d / "scan.har").write_text("{}", encoding="utf-8")
    owner = {"X-Probo-Key": "owner-key"}

    assert client.get("/api/scans").json() == []
    assert client.get("/api/scans", headers=owner).json()[0]["domain"] == "uzum.uz"
    assert client.get(f"/api/scans/{scan_id}").status_code == 404
    assert client.get(f"/api/scans/{scan_id}/har").status_code == 404
    assert client.get(f"/api/scans/{scan_id}/events").status_code == 404
    assert client.get("/api/sites/uzum.uz").status_code == 403
    assert client.post(f"/api/scans/{scan_id}/share").status_code == 404
    assert client.get(f"/api/scans/{scan_id}", headers=owner).json()["domain"] == "uzum.uz"
    assert client.get(f"/api/scans/{scan_id}/har?key=owner-key").status_code == 200
    assert client.get("/api/health").json()["owner"] is False
    assert client.get("/api/health", headers=owner).json()["owner"] is True

    token = client.post(f"/api/scans/{scan_id}/share", headers=owner).json()["token"]
    shared = client.get(f"/api/shared/{token}")
    assert shared.status_code == 200 and "uzum" not in shared.text.lower() and "kapitalbank" not in shared.text.lower()
    sample = client.get("/api/sample")
    assert sample.status_code == 200 and "uzum" not in sample.text.lower()
    assert "kapitalbank" not in sample.text.lower() and "Bank E" in sample.text  # other reference sites hidden too

    started = client.post("/api/scans", json={"url": "http://8.8.8.8"}).json()
    own = tmp_path / started["scan_id"]  # the job is stubbed: write its result by hand
    own.mkdir(parents=True)
    (own / "report.json").write_text(_json.dumps({**report, "scan_id": started["scan_id"], "site": "http://8.8.8.8"}),
                                     encoding="utf-8")
    assert client.get(f"/api/scans/{started['scan_id']}").status_code == 404  # no token: hidden
    mine = client.get(f"/api/scans/{started['scan_id']}", headers={"X-Scan-Token": started["token"]})
    assert mine.status_code == 200 and mine.json()["domain"] == "8.8.8.8"  # own scan: real name
    assert client.get(f"/api/scans/{started['scan_id']}", headers={"X-Scan-Token": "wrong"}).status_code == 404
    guard.reset()


def test_anonymize_hides_brand_aliases_in_quotes():
    report = {"quote": "Uzum Market maʼlumotlarni uchinchi shaxslarga bermaydi. UZUM Bank ham."}
    result = anonymize(report, ["uzum.uz"], "Marketplace A", ["Uzum Market", "Uzum Bank", "Uzum"])
    assert "uzum" not in result["quote"].lower()
    assert result["quote"].startswith("Marketplace A")
