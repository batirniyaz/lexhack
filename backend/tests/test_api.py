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


def test_anonymize_hides_brand_aliases_in_quotes():
    report = {"quote": "Uzum Market maʼlumotlarni uchinchi shaxslarga bermaydi. UZUM Bank ham."}
    result = anonymize(report, ["uzum.uz"], "Marketplace A", ["Uzum Market", "Uzum Bank", "Uzum"])
    assert "uzum" not in result["quote"].lower()
    assert result["quote"].startswith("Marketplace A")
