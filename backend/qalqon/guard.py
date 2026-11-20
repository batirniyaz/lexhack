"""Abuse protection for the public deployment: every scan costs LLM money and machine time.

- Per-IP limit (PROBO_SCANS_PER_IP_HOUR, default 6) and a global daily limit (PROBO_SCANS_PER_DAY, default 100).
- Optional access key (PROBO_SCAN_KEY): if set, starting a scan needs the header X-Probo-Key with that value.
Behind Cloudflare the client address comes from the CF-Connecting-IP header.
In-memory counters: they reset when the service restarts, which is acceptable for a demo.
"""

from __future__ import annotations

import hmac
import os
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

PER_IP_HOUR = int(os.environ.get("PROBO_SCANS_PER_IP_HOUR", "6"))
PER_DAY = int(os.environ.get("PROBO_SCANS_PER_DAY", "100"))
SCAN_KEY = os.environ.get("PROBO_SCAN_KEY", "")

_by_ip: dict[str, deque] = defaultdict(deque)
_all: deque = deque()


def client_ip(request: Request) -> str:
    return request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "unknown")


def _trim(queue: deque, window: float, now: float) -> None:
    while queue and now - queue[0] > window:
        queue.popleft()


def check_scan_allowed(request: Request) -> None:
    """Raise 403 / 429 when a new scan must not start. Call before starting the job."""
    if SCAN_KEY:
        given = request.headers.get("x-probo-key", "")
        if not hmac.compare_digest(given, SCAN_KEY):
            raise HTTPException(403, "access key required")
    now = time.time()
    ip = client_ip(request)
    _trim(_by_ip[ip], 3600, now)
    _trim(_all, 86400, now)
    if len(_by_ip[ip]) >= PER_IP_HOUR:
        raise HTTPException(429, f"limit: {PER_IP_HOUR} scans per hour from one address")
    if len(_all) >= PER_DAY:
        raise HTTPException(429, "daily scan limit reached")
    _by_ip[ip].append(now)
    _all.append(now)


def reset() -> None:
    """For tests."""
    _by_ip.clear()
    _all.clear()
