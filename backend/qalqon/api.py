"""HTTP API (ARCHITECTURE.md §2.7).

Run from backend/:  .venv/Scripts/python -m uvicorn qalqon.api:app --port 8000
"""

from __future__ import annotations

import asyncio
import json
import secrets
from collections import Counter
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from . import __version__
from .config import REPO_ROOT, SCANS_DIR, settings
from .guard import check_scan_allowed
from .jobs import ScanJob, jobs
from .presentation import aliases_for, anonymize, label_for, replay_events
from .scan import new_scan_id
from .urls import TargetNotAllowed, check_target, host_of, normalize_url, registrable_domain

app = FastAPI(title="Probo", version=__version__)
SHARES_FILE = SCANS_DIR / ".shares.json"
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_methods=["*"],
    allow_headers=["*"],
)

REPLAY_DELAY_S = 0.12


class ScanRequest(BaseModel):
    url: str
    max_pages: Optional[int] = Field(default=None, ge=1, le=50)


def _scan_dir(scan_id: str) -> Path:
    path = (SCANS_DIR / scan_id).resolve()
    if SCANS_DIR.resolve() not in path.parents:
        raise HTTPException(400, "bad scan id")
    return path


def _read_json(path: Path) -> Optional[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "version": __version__,
        "llm_configured": bool(settings.anthropic_api_key),
        "lexrag_configured": bool(settings.lexrag_url),
    }


@app.post("/api/scans", status_code=202)
async def create_scan(body: ScanRequest, request: Request) -> dict:
    url = normalize_url(body.url)
    try:
        check_target(url)
    except TargetNotAllowed as exc:
        raise HTTPException(400, f"target not allowed: {exc}") from exc
    check_scan_allowed(request)  # rate limits / access key (public deployment)
    job = jobs.start(ScanJob(scan_id=new_scan_id(url), url=url, max_pages=body.max_pages))
    return {"scan_id": job.scan_id, "status": job.status, "events": f"/api/scans/{job.scan_id}/events"}


def _all_reports() -> list[dict]:
    """Every finished scan (single and batch) as a small index row, oldest first."""
    rows = []
    for report_path in SCANS_DIR.rglob("report.json"):
        report = _read_json(report_path) or {}
        site = report.get("site") or ""
        rows.append({
            "scan_id": report_path.parent.relative_to(SCANS_DIR).as_posix(),
            "site": site,
            "domain": registrable_domain(host_of(site)),
            "label": label_for(site),
            "status": report.get("status"),
            "score": report.get("score"),
            "levels": report.get("levels"),
            "scanned_at": report.get("scanned_at") or "",
            "_findings": [{"rule_id": f["rule_id"], "level": f["level"], "title": f.get("title", {})}
                          for f in report.get("findings", [])],
        })
    rows.sort(key=lambda r: r["scanned_at"])
    return rows


@app.get("/api/scans")
def list_scans(limit: int = 50) -> list[dict]:
    """Finished scans, newest first, with the score change against the previous scan of the same site."""
    rows = _all_reports()
    last_score: dict[str, Optional[int]] = {}
    for row in rows:
        previous = last_score.get(row["domain"])
        row["delta"] = row["score"] - previous if (row["score"] is not None and previous is not None) else None
        if row["status"] == "ok":
            last_score[row["domain"]] = row["score"]
    return [{k: v for k, v in r.items() if not k.startswith("_")} for r in reversed(rows)][:limit]


@app.get("/api/sites/{domain}")
def site_history(domain: str, anon: bool = False) -> dict:
    """All scans of one site: score trend + what changed between the last two successful scans."""
    scans = [r for r in _all_reports() if r["domain"] == domain.lower()]
    if not scans:
        raise HTTPException(404, "no scans for this site")
    ok = [r for r in scans if r["status"] == "ok"]
    diff = None
    if len(ok) >= 2:
        before = {f["rule_id"]: f for f in ok[-2]["_findings"]}
        after = {f["rule_id"]: f for f in ok[-1]["_findings"]}
        diff = {
            "from": ok[-2]["scan_id"], "to": ok[-1]["scan_id"],
            "new": [after[k] for k in after if k not in before],
            "fixed": [before[k] for k in before if k not in after],
            "unchanged": [after[k] for k in after if k in before],
        }
    result = {
        "domain": domain.lower(),
        "label": scans[-1]["label"],
        "scans": [{k: v for k, v in r.items() if not k.startswith("_") and k != "domain"} for r in scans],
        "diff": diff,
    }
    if anon:
        site = scans[-1]["site"]
        result = anonymize(result, [domain.lower()], label_for(site), aliases_for(site))
    return result


def _shares() -> dict[str, str]:
    return _read_json(SHARES_FILE) or {}


@app.post("/api/scans/{scan_id:path}/share")
def share_scan(scan_id: str) -> dict:
    """Read-only link for a finished report. The token is random; the same scan keeps its token."""
    if not (_scan_dir(scan_id) / "report.json").exists():
        raise HTTPException(404, "scan not found")
    shares = _shares()
    token = next((t for t, sid in shares.items() if sid == scan_id), None) or secrets.token_urlsafe(12)
    shares[token] = scan_id
    SHARES_FILE.parent.mkdir(parents=True, exist_ok=True)
    SHARES_FILE.write_text(json.dumps(shares, indent=1), encoding="utf-8")
    return {"token": token, "path": f"/r/{token}"}


@app.get("/api/shared/{token}")
def shared_scan(token: str, anon: bool = False) -> dict:
    scan_id = _shares().get(token)
    if not scan_id:
        raise HTTPException(404, "link not found")
    return {**scan_result(scan_id, anon=anon, facts=True), "scan_id": scan_id}


@app.get("/api/scans/{scan_id:path}/events")
async def scan_events(scan_id: str, request: Request, replay: bool = False):
    """Live feed (SSE). For finished scans, or with ?replay=1, the saved results are replayed with a short delay."""
    job = jobs.jobs.get(scan_id)
    if job is None or replay:
        scan_dir = _scan_dir(scan_id)
        if not (scan_dir / "report.json").exists():
            raise HTTPException(404, "scan not found")

        async def replayed():
            for event in replay_events(scan_dir):
                if await request.is_disconnected():
                    return
                yield {"event": event["type"], "data": json.dumps(event, ensure_ascii=False)}
                await asyncio.sleep(REPLAY_DELAY_S)

        return EventSourceResponse(replayed())

    async def live():
        sent = 0
        while True:
            while sent < len(job.events):
                event = job.events[sent]
                sent += 1
                yield {"event": event["type"], "id": str(event["seq"]), "data": json.dumps(event, ensure_ascii=False)}
            if job.finished and sent >= len(job.events):
                return
            if await request.is_disconnected():
                return
            await job.wait_for_change()

    return EventSourceResponse(live())


@app.get("/api/scans/{scan_id:path}/har")
def scan_har(scan_id: str):
    path = _scan_dir(scan_id) / "scan.har"
    if not path.exists():
        raise HTTPException(404, "no HAR for this scan")
    return FileResponse(path, media_type="application/json", filename=f"{Path(scan_id).name}.har")


@app.get("/api/scans/{scan_id:path}")
def scan_result(scan_id: str, anon: bool = False, facts: bool = False) -> dict:
    """Report (+ optional facts). ?anon=1 hides the site's domain behind its sector label (presentation mode)."""
    job = jobs.jobs.get(scan_id)
    scan_dir = _scan_dir(scan_id)
    report = _read_json(scan_dir / "report.json")
    if report is None:
        if job is not None:
            return {"scan_id": scan_id, "status": job.status, "error": job.error}
        raise HTTPException(404, "scan not found")
    result: dict = {"report": report}
    if facts:
        raw = _read_json(scan_dir / "facts.json") or {}
        result["facts"] = {k: raw.get(k) for k in ("site", "site_domains", "pages", "hosts", "flows", "forms",
                                                    "documents", "cookies", "backends", "stats", "enrichment",
                                                    "policy", "uploads", "permissions", "session_replay", "blocked")}
        for doc in result["facts"].get("documents") or []:
            doc.pop("text", None)  # large; served separately later if needed
    site = report.get("site") or ""
    if anon:
        domains = (_read_json(scan_dir / "facts.json") or {}).get("site_domains") or []
        result = anonymize(result, domains, label_for(site), aliases_for(site))
    # Set after anonymizing: the frontend needs it for the site-history link (in presentation mode use full screen,
    # so the address bar with the domain is not visible).
    result["domain"] = registrable_domain(host_of(site))
    return result


@app.get("/api/stats")
def stats() -> dict:
    """Anonymized aggregate over the latest batch scan — numbers for the pitch, no site names."""
    batches = sorted(SCANS_DIR.glob("batch-*"))
    if not batches:
        raise HTTPException(404, "no batch scans yet")
    reports = [r for r in (_read_json(p) for p in batches[-1].glob("*/report.json")) if r and r["status"] == "ok"]
    total = len(reports)
    rule_counts = Counter(f["rule_id"] for r in reports for f in r["findings"])
    country_counts = Counter(flow["country"] for r in reports for flow in r.get("flows", []))
    return {
        "batch": batches[-1].name,
        "sites": total,
        "average_score": round(sum(r["score"] for r in reports) / total, 1) if total else None,
        "sites_with_rule": {rule: count for rule, count in rule_counts.most_common()},
        "sites_sending_to_country": dict(country_counts.most_common()),
        "note": "Anonymized: no site names. Passive scan; findings are signs of violation, not legal conclusions.",
    }


# --- Built frontend (one container, one port). Declared last so every /api route above wins. ---
FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def frontend(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(404, "not found")
        candidate = (FRONTEND_DIST / full_path).resolve()
        if full_path and FRONTEND_DIST.resolve() in candidate.parents and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")  # SPA routes: /scan/…, /history, /sites/…, /r/…
