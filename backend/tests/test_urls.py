import pytest

from qalqon.urls import TargetNotAllowed, check_target, normalize_url, registrable_domain, same_site


def test_registrable_domain():
    assert registrable_domain("www.lex.uz") == "lex.uz"
    assert registrable_domain("connect.facebook.net") == "facebook.net"
    assert registrable_domain("www.bbc.co.uk") == "bbc.co.uk"
    assert registrable_domain("142.250.130.100") == "142.250.130.100"
    assert registrable_domain("") == ""


def test_same_site():
    assert same_site("cdn.lex.uz", "lex.uz")
    assert not same_site("www.googletagmanager.com", "lex.uz")


def test_normalize_url():
    assert normalize_url("lex.uz") == "https://lex.uz"
    assert normalize_url(" https://lex.uz/ru#top ") == "https://lex.uz/ru"


@pytest.mark.parametrize("url", ["http://127.0.0.1/", "http://localhost:8000", "http://10.0.0.5", "ftp://example.com"])
def test_check_target_refuses(url):
    with pytest.raises(TargetNotAllowed):
        check_target(url)


def test_check_target_allows_private_for_demo():
    check_target("http://127.0.0.1:5500", allow_private=True)
