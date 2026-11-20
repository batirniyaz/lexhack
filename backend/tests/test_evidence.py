"""Evidence seal (F-19): a signed seal verifies, any change breaks it, and the server knows its own reports."""

import json

from fastapi.testclient import TestClient

from qalqon import evidence
from qalqon.api import app

client = TestClient(app)


def _scan(tmp_path, monkeypatch):
    monkeypatch.setattr(evidence, "KEY_FILE", tmp_path / ".signing_key")
    monkeypatch.setattr(evidence, "SCANS_DIR", tmp_path)
    monkeypatch.delenv("PROBO_SIGNING_KEY", raising=False)
    evidence._private_key.cache_clear()
    d = tmp_path / "s1"
    d.mkdir()
    report = {"scan_id": "s1", "site": "https://shop.example.uz", "scanned_at": "2026-11-21T08:00:00+00:00",
              "status": "ok", "score": 72, "levels": {"violation": 1}, "scope": {"rules_version": "abc"}}
    (d / "report.json").write_text(json.dumps(report), encoding="utf-8")
    (d / "facts.json").write_text("{}", encoding="utf-8")
    return d


def test_seal_verifies_and_detects_tampering(tmp_path, monkeypatch):
    d = _scan(tmp_path, monkeypatch)
    seal = evidence.write_seal(d)
    assert seal["statement"]["sha256"]["facts"] == evidence.sha256_bytes(b"{}")
    ok = evidence.verify(seal)
    assert ok["valid_signature"] and ok["our_key"] and ok["known_report"]

    forged = json.loads(json.dumps(seal))
    forged["statement"]["score"] = 100
    assert evidence.verify(forged)["valid_signature"] is False
    assert evidence.verify({"nonsense": True})["valid_signature"] is False
    evidence._private_key.cache_clear()


def test_same_report_same_hash():
    report = {"b": 1, "a": [1, 2], "c": {"y": "ʼ", "x": None}}
    assert evidence.report_hash(report) == evidence.report_hash(json.loads(json.dumps(report)))


def test_verify_endpoint(tmp_path, monkeypatch):
    d = _scan(tmp_path, monkeypatch)
    seal = evidence.write_seal(d)
    response = client.post("/api/verify", json=seal)
    assert response.status_code == 200 and response.json()["valid_signature"] is True
    assert client.get("/api/verify/key").json()["key_id"] == evidence.key_id()
    evidence._private_key.cache_clear()
