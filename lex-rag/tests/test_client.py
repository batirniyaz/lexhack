"""The rules that keep the crawler from hammering a site that is already struggling."""
import asyncio
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lexuz import client as client_module  # noqa: E402
from lexuz.client import Blocked, Client, PageFailed, Pace, SiteDown  # noqa: E402


def run_with(handler, url="/x", rate=1000):
    """One fetch against a fake site; returns (result, number of requests that reached the site)."""
    calls = []

    def counted(request):
        calls.append(request)
        return handler(len(calls))

    async def go():
        client = Client(rate)
        await client.http.aclose()
        client.http = httpx.AsyncClient(base_url="https://lex.uz", transport=httpx.MockTransport(counted))
        try:
            return await client.fetch("doc", url), client
        finally:
            await client.close()

    return asyncio.run(go()), len(calls)


def fetch_each(handler, urls):
    """Several fetches on one client, as a crawl makes them: each result is the reply, None or what was raised."""
    async def go():
        client = Client(1000)
        await client.http.aclose()
        client.http = httpx.AsyncClient(base_url="https://lex.uz", transport=httpx.MockTransport(handler))
        results = []
        try:
            for url in urls:
                try:
                    results.append(await client.fetch("doc", url))
                except SiteDown as e:
                    results.append(e)
        finally:
            await client.close()
        return results

    return asyncio.run(go())


@pytest.fixture(autouse=True)
def no_waiting(monkeypatch):
    monkeypatch.setattr(client_module, "RETRY_WAITS", (0, 0, 0))
    monkeypatch.setattr(client_module, "OFFLINE_CHECK", 0)
    monkeypatch.setattr(client_module, "online", lambda: True)


def test_trouble_halves_the_pace():
    pace = Pace(4)
    pace.slow_down()
    assert pace.rate == 2


def test_pace_never_falls_below_the_floor():
    pace = Pace(1, floor=0.5)
    for _ in range(5):
        pace.slow_down()
    assert pace.rate == 0.5


def test_pace_recovers_but_never_exceeds_what_was_asked():
    pace = Pace(4)
    pace.slow_down()
    for _ in range(client_module.RECOVER_AFTER * 6):
        pace.record("doc", 0.1)
    assert pace.rate == 4


def test_a_site_that_gets_slow_lowers_the_pace():
    pace = Pace(4)
    for _ in range(client_module.WINDOW):
        pace.record("doc", 0.1)
    for _ in range(client_module.WINDOW):
        pace.record("doc", 2.0)
    assert pace.rate < 4


def test_heavy_pages_are_compared_with_their_own_kind():
    pace = Pace(4)
    for _ in range(client_module.WINDOW):
        pace.record("card", 0.1)
    for _ in range(client_module.WINDOW):
        pace.record("doc", 2.0)
    assert pace.rate == 4


def test_a_network_that_stays_slower_is_accepted_in_the_end():
    pace = Pace(4)
    for _ in range(client_module.WINDOW):
        pace.record("doc", 0.1)
    for _ in range(client_module.WINDOW * 50):
        pace.record("doc", 2.0)
    assert pace.rate == 4


def test_ok_page_comes_back():
    (reply, _), calls = run_with(lambda n: httpx.Response(200, text="hello"))
    assert reply.text == "hello"
    assert calls == 1


def test_missing_page_is_a_redirect_and_is_not_retried():
    (reply, _), calls = run_with(lambda n: httpx.Response(302, headers={"Location": "/Pages/404.aspx"}))
    assert reply is None
    assert calls == 1


def test_plain_404_is_a_missing_page():
    (reply, _), calls = run_with(lambda n: httpx.Response(404))
    assert reply is None
    assert calls == 1


@pytest.mark.parametrize("status, headers", [(403, {}), (401, {}), (302, {"Location": "/captcha"})])
def test_a_refusal_is_never_taken_for_a_missing_page(status, headers):
    with pytest.raises(PageFailed):
        run_with(lambda n: httpx.Response(status, headers=headers))


def test_overload_is_retried_and_lowers_the_pace():
    (reply, client), calls = run_with(lambda n: httpx.Response(503) if n == 1 else httpx.Response(200, text="ok"), rate=1000)
    assert reply.text == "ok"
    assert calls == 2
    assert client.pace.rate == 500


def test_one_bad_page_does_not_stop_the_crawl():
    results = fetch_each(lambda r: httpx.Response(500 if r.url.path == "/bad" else 200, text="ok"), ["/bad", "/good"])
    assert isinstance(results[0], PageFailed)
    assert results[1].text == "ok"


def test_failing_everywhere_means_the_site_is_down(monkeypatch):
    monkeypatch.setattr(client_module, "STOP_AFTER", 3)
    with pytest.raises(SiteDown) as stopped:
        run_with(lambda n: httpx.Response(429))
    assert type(stopped.value) is SiteDown


def test_refused_everywhere_means_blocked(monkeypatch):
    monkeypatch.setattr(client_module, "STOP_AFTER", 3)
    with pytest.raises(Blocked):
        run_with(lambda n: httpx.Response(403))


def test_connection_errors_count_as_failures():
    def broken(_):
        raise httpx.ConnectError("no route")

    with pytest.raises(SiteDown):
        run_with(broken)


def test_lost_internet_is_waited_out_and_not_blamed_on_the_site(monkeypatch):
    looks = iter([False, False, False, True])
    monkeypatch.setattr(client_module, "online", lambda: next(looks))

    def dropped_once(n):
        if n == 1:
            raise httpx.ConnectError("no route")
        return httpx.Response(200, text="ok")

    (reply, client), calls = run_with(dropped_once)
    assert reply.text == "ok"
    assert calls == 2
    assert client.pace.rate == 1000
    assert client.failed_in_a_row == 0
