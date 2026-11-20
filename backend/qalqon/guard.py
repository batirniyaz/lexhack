"""Abuse protection for the public deployment: every scan costs LLM money and machine time.

- Per-IP limit (PROBO_SCANS_PER_IP_HOUR, default 6) and a global daily limit (PROBO_SCANS_PER_DAY, default 100).
- Optional access key (PROBO_SCAN_KEY): if set, starting a scan needs the header X-Probo-Key with that value.
Behind Cloudflare the client address comes from the CF-Connecting-IP header.
In-memory counters: they reset when the service restarts, which is acceptable for a demo.

Public mode (PROBO_PUBLIC=1): real site names must never be public (passport D-003, D-017).
- The owner (header X-Probo-Key or query ?key= equal to PROBO_OWNER_KEY) sees everything.
- Everyone else sees only the scans they started: POST /api/scans returns a random token, and the browser sends it
  back (header X-Scan-Token or query ?t=). Other scans are "not found"; history and HAR are closed;
  shared links are always anonymized.
"""

from __future__ import annotations

import hmac
import json
import os
import secrets
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from .config import SCANS_DIR

PER_IP_HOUR = int(os.environ.get("PROBO_SCANS_PER_IP_HOUR", "6"))
PER_DAY = int(os.environ.get("PROBO_SCANS_PER_DAY", "100"))
SCAN_KEY = os.environ.get("PROBO_SCAN_KEY", "")
PUBLIC = os.environ.get("PROBO_PUBLIC", "") == "1"
OWNER_KEY = os.environ.get("PROBO_OWNER_KEY", "")
TOKENS_FILE = SCANS_DIR / ".scan_tokens.json"

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


def _given(request: Request, header: str, query: str) -> str:
    return request.headers.get(header) or request.query_params.get(query) or ""


def is_owner(request: Request) -> bool:
    """Outside public mode everyone is the owner (local development, tests)."""
    if not PUBLIC:
        return True
    return bool(OWNER_KEY) and hmac.compare_digest(_given(request, "x-probo-key", "key"), OWNER_KEY)


def _tokens() -> dict[str, str]:
    try:
        return json.loads(TOKENS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def issue_scan_token(scan_id: str) -> str:
    """A secret for the browser that started the scan: it may see its own scan with real names."""
    tokens = _tokens()
    tokens[scan_id] = secrets.token_urlsafe(16)
    TOKENS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKENS_FILE.write_text(json.dumps(tokens, indent=1), encoding="utf-8")
    return tokens[scan_id]


def can_view(request: Request, scan_id: str) -> bool:
    if is_owner(request):
        return True
    expected = _tokens().get(scan_id)
    return bool(expected) and hmac.compare_digest(_given(request, "x-scan-token", "t"), expected)


def require_view(request: Request, scan_id: str) -> None:
    """404 (not 403): a visitor must not learn which scans exist."""
    if not can_view(request, scan_id):
        raise HTTPException(404, "scan not found")


def require_owner(request: Request) -> None:
    if not is_owner(request):
        raise HTTPException(403, "owner only in the public demo")


def reset() -> None:
    """For tests."""
    _by_ip.clear()
    _all.clear()
