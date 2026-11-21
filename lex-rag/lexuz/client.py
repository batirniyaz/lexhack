"""HTTP for lex.uz: one shared pace for every request, and it slows down by itself when the site struggles."""
import asyncio
import collections
import datetime as dt
import math
import socket
import statistics
import time

import httpx

BASE = "https://lex.uz"
USER_AGENT = "lex-rag-edu-crawler/0.1"
RETRY_WAITS = (5, 15, 45)
STOP_AFTER = 15        # requests failed in a row: the site is down or has blocked us, so stop instead of hammering it
WINDOW = 40            # recent requests of one kind compared with the first ones
SLOW_FACTOR = 3        # this many times slower than the start counts as the site struggling
RECOVER_AFTER = 100    # good requests in a row before the pace goes back up
PROBES = (("1.1.1.1", 443), ("8.8.8.8", 443))   # opened and closed, nothing is sent: tells our own outage from the site's
OFFLINE_CHECK = 30     # seconds between looks at the connection while it is gone


class SiteDown(Exception):
    """The site as a whole is not answering."""


class Blocked(SiteDown):
    """The site keeps refusing us outright. Trying again later would be pushing past a clear no."""


class PageFailed(SiteDown):
    """This one page keeps failing while the rest of the site answers."""


def online():
    for address in PROBES:
        try:
            socket.create_connection(address, timeout=5).close()
            return True
        except OSError:
            pass
    return False


def is_missing(reply):
    """A page that does not exist is a plain 404, on some paths a redirect to 404.aspx. Any other refusal is not an answer."""
    return reply.status_code == 404 or (reply.is_redirect and "404" in reply.headers.get("Location", ""))


class Pace:
    """Spaces requests evenly. Halves on trouble, climbs back slowly, never above the rate that was asked for."""

    def __init__(self, rate, floor=0.5):
        self.ceiling, self.rate, self.floor = rate, rate, floor
        self.next_slot = 0.0
        self.good = 0
        self.recent = collections.defaultdict(lambda: collections.deque(maxlen=WINDOW))
        self.normal = {}
        self.slowdowns = 0

    async def slot(self):
        now = time.monotonic()
        start = max(now, self.next_slot)
        self.next_slot = start + 1 / self.rate
        if start > now:
            await asyncio.sleep(start - now)

    def hold(self, seconds):
        self.next_slot = max(self.next_slot, time.monotonic() + seconds)

    def slow_down(self):
        self.rate = max(self.floor, self.rate / 2)
        self.good = 0
        self.slowdowns += 1

    def record(self, kind, seconds):
        window = self.recent[kind]
        window.append(seconds)
        self.good += 1
        if len(window) == WINDOW:
            median = statistics.median(window)
            if kind not in self.normal:
                self.normal[kind] = median
            elif median > SLOW_FACTOR * self.normal[kind] + 0.2:
                if self.rate == self.floor:   # as gentle as it gets and still slow, so it is not us: a slower network, say
                    self.normal[kind] = median
                self.slow_down()
                window.clear()
        if self.good >= RECOVER_AFTER and self.rate < self.ceiling:
            self.rate = min(self.ceiling, self.rate * 1.25)
            self.good = 0


class Client:
    def __init__(self, rate, on_request=None):
        self.pace = Pace(rate)
        self.on_request = on_request or (lambda *_: None)
        self.failed_in_a_row = 0
        self.in_flight = asyncio.Semaphore(math.ceil(rate) + 1)
        self.http = httpx.AsyncClient(
            base_url=BASE, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"},
            timeout=httpx.Timeout(60, connect=15), follow_redirects=False,
        )

    async def close(self):
        await self.http.aclose()

    async def lost_connection(self):
        """Waits out an outage on our side and says whether there was one: it tells nothing about the site."""
        if await asyncio.to_thread(online):
            return False
        print(dt.datetime.now().strftime("%H:%M:%S"), "no internet, waiting", flush=True)
        while not await asyncio.to_thread(online):
            await asyncio.sleep(OFFLINE_CHECK)
        print(dt.datetime.now().strftime("%H:%M:%S"), "internet is back", flush=True)
        return True

    async def fetch(self, kind, url, data=None):
        """Returns the response, or None when the page does not exist. Raises PageFailed, SiteDown or Blocked otherwise."""
        waits = iter(RETRY_WAITS)
        while True:
            await self.pace.slot()
            started = time.monotonic()
            status, size = 0, 0
            try:
                async with self.in_flight:
                    reply = await (self.http.post(url, data=data) if data else self.http.get(url))
                status, size = reply.status_code, reply.num_bytes_downloaded
            except httpx.TransportError:
                reply = None
            seconds = time.monotonic() - started
            self.on_request(kind, status, seconds, size, self.pace.rate)

            if reply is None and await self.lost_connection():
                continue
            if reply is not None and (status == 200 or is_missing(reply)):
                self.failed_in_a_row = 0
                self.pace.record(kind, seconds)
                return reply if status == 200 else None

            self.failed_in_a_row += 1
            self.pace.slow_down()
            if self.failed_in_a_row >= STOP_AFTER:
                stop = Blocked if status == 403 else SiteDown
                raise stop(f"{self.failed_in_a_row} failures in a row, last status {status}")
            wait = next(waits, None)
            if wait is None:
                raise PageFailed(f"gave up on {url}, last status {status}")
            retry_after = reply.headers.get("Retry-After", "") if reply is not None else ""
            self.pace.hold(int(retry_after) if retry_after.isdigit() else wait)
