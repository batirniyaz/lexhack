"""HTTP API (ARCHITECTURE.md §2.7).

Run from backend/:  .venv/Scripts/python -m uvicorn qalqon.api:app --port 8000
"""

from __future__ import annotations

import asyncio
import json
from collections import Counter
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from . import __version__
from .config import SCANS_DIR, settings
from .jobs import ScanJob, jobs
from .presentation import aliases_for, anonymize, label_for, replay_events
from .scan import new_scan_id
from .urls import TargetNotAllowed, check_target, normalize_url

app = FastAPI(title="Qalqon", version=__version__)
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
async def create_scan(body: ScanRequest) -> dict:
    url = normalize_url(body.url)
    try:
        check_target(url)
    except TargetNotAllowed as exc:
        raise HTTPException(400, f"target not allowed: {exc}") from exc
    job = jobs.start(ScanJob(scan_id=new_scan_id(url), url=url, max_pages=body.max_pages))
    return {"scan_id": job.scan_id, "status": job.status, "events": f"/api/scans/{job.scan_id}/events"}


@app.get("/api/scans")
def list_scans(limit: int = 50) -> list[dict]:
    """Finished scans (single and batch), newest first — the demo picks cached reports from here."""
    rows = []
    for report_path in sorted(SCANS_DIR.rglob("report.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]:
        report = _read_json(report_path) or {}
        scan_id = report_path.parent.relative_to(SCANS_DIR).as_posix()
        rows.append({"scan_id": scan_id, "site": report.get("site"), "label": label_for(report.get("site") or ""),
                     "status": report.get("status"), "score": report.get("score"), "levels": report.get("levels"),
                     "scanned_at": report.get("scanned_at")})
    return rows


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
    if anon:
        domains = (_read_json(scan_dir / "facts.json") or {}).get("site_domains") or []
        site = report.get("site") or ""
        result = anonymize(result, domains, label_for(site), aliases_for(site))
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
