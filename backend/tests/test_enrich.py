import pytest

from qalqon.enrich.entities import identify
from qalqon.enrich.geo import geodb
from qalqon.scanner.crawler import _challenge, _key


def test_identify_known_owners():
    assert identify("mc.yandex.ru") == {"entity": "Yandex", "company_country": "RU", "dpf": None, "category": "analytics"}
    meta = identify("connect.facebook.net")
    assert meta["entity"] == "Meta" and meta["company_country"] == "US" and meta["category"] == "advertising"
    assert identify("fonts.gstatic.com")["category"] == "fonts"
    assert identify("challenges.cloudflare.com")["category"] == "captcha"
    assert identify("api.telegram.org")["company_country"] == "AE"
    assert identify("example-unknown-host.com") is None


def test_identify_does_not_match_partial_labels():
    assert identify("notfacebook.net") is None


@pytest.mark.skipif(not geodb().available, reason="DB-IP files not downloaded (python -m qalqon.enrich.geo --download)")
def test_geo_lookup():
    google_dns = geodb().lookup("8.8.8.8")
    assert google_dns["server_country"] == "US"
    assert google_dns["asn"] == 15169
    cloudflare = geodb().lookup("1.1.1.1")
    assert cloudflare["is_cdn"] is True
    assert geodb().lookup("192.168.1.1")["server_country"] == "LOCAL"


def test_challenge_detection():
    assert _challenge("https://express24.uz/showcaptcha?cc=1", "") == "captcha"
    assert _challenge("https://site.uz/", "Just a moment...") == "cloudflare-challenge"
    assert _challenge("https://site.uz/", "Главная") is None


def test_page_key_dedup():
    assert _key("https://Kapitalbank.uz/") == _key("https://kapitalbank.uz")
    assert _key("https://a.uz/x/#top") == _key("https://a.uz/x")
    assert _key("https://a.uz/x?b=1") != _key("https://a.uz/x")


def test_website_address_field_is_not_personal_data():
    """'Sayt manzili' (website address) is not a postal address (false PD-CNS-01 on our own site, 21.11)."""
    from qalqon.scanner.analysis import classify_field
    assert classify_field({"label": "Sayt manzili", "type": "url"}) is None
    assert classify_field({"label": "Sayt manzili", "type": "text"}) is None
    assert classify_field({"label": "Yashash manzili", "type": "text"}) == "address"
