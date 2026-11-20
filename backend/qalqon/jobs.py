"""Scan jobs: each scan runs as a separate process (`python -m qalqon.scan --events`), events are relayed to SSE.

Why a subprocess (D-015): Playwright fails inside uvicorn's event loop on Windows (`--reload` / selector loop),
and a crashed browser must not take the API down. A reader thread forwards stdout lines into the asyncio loop,
so this works with any event-loop policy.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

from .config import BACKEND_DIR, SCANS_DIR

MAX_PARALLEL_SCANS = 2


@dataclass
class ScanJob:
    scan_id: str
    url: str
    max_pages: Optional[int]
    allow_private: bool = False
    status: str = "queued"          # queued | running | done | error
    events: list[dict] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    error: Optional[str] = None
    _changed: Optional[asyncio.Event] = None

    def attach(self) -> None:
        self._changed = asyncio.Event()

    def add_event(self, event: dict) -> None:
        event = {"seq": len(self.events), **event}
        self.events.append(event)
        if event.get("type") == "start":
            self.status = "running"
        self._changed.set()
        self._changed = asyncio.Event()

    async def wait_for_change(self, timeout: float = 15.0) -> None:
        changed = self._changed
        try:
            await asyncio.wait_for(changed.wait(), timeout)
        except asyncio.TimeoutError:
            pass

    @property
    def finished(self) -> bool:
        return self.status in ("done", "error")


class JobManager:
    def __init__(self) -> None:
        self.jobs: dict[str, ScanJob] = {}
        self._slots: Optional[asyncio.Semaphore] = None

    def _semaphore(self) -> asyncio.Semaphore:
        if self._slots is None:
            self._slots = asyncio.Semaphore(MAX_PARALLEL_SCANS)
        return self._slots

    def start(self, job: ScanJob) -> ScanJob:
        job.attach()
        self.jobs[job.scan_id] = job
        asyncio.get_running_loop().create_task(self._run(job))
        return job

    async def _run(self, job: ScanJob) -> None:
        async with self._semaphore():
            loop = asyncio.get_running_loop()
            done = asyncio.Event()
            command = [sys.executable, "-m", "qalqon.scan", job.url, "--events", "--scan-id", job.scan_id]
            if job.max_pages:
                command += ["--max-pages", str(job.max_pages)]
            if job.allow_private:
                command.append("--allow-private")
            out_dir = SCANS_DIR / job.scan_id
            out_dir.mkdir(parents=True, exist_ok=True)

            def reader() -> None:
                stderr_tail: list[str] = []
                try:
                    process = subprocess.Popen(
                        command, cwd=BACKEND_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        text=True, encoding="utf-8", errors="replace",
                    )
                    with open(out_dir / "events.jsonl", "w", encoding="utf-8") as log:
                        for line in process.stdout:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                event = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            log.write(line + "\n")
                            log.flush()
                            loop.call_soon_threadsafe(job.add_event, event)
                    stderr_tail = process.stderr.read().splitlines()[-5:]
                    code = process.wait()
                except Exception as exc:  # could not start the process at all
                    code, stderr_tail = -1, [f"{type(exc).__name__}: {exc}"]

                def finish() -> None:
                    ok = code == 0 and (out_dir / "report.json").exists()
                    job.status = "done" if ok else "error"
                    if not ok:
                        job.error = "\n".join(stderr_tail) or f"exit code {code}"
                    job.add_event({"type": "end", "status": job.status, "error": job.error})
                    done.set()

                loop.call_soon_threadsafe(finish)

            threading.Thread(target=reader, name=f"scan-{job.scan_id}", daemon=True).start()
            await done.wait()


jobs = JobManager()
