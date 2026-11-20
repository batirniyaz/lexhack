"""Batch scan: many sites in parallel, one facts.json each, plus a summary table.

Usage (from backend/):
    .venv/Scripts/python -m qalqon.batch data/reference_sites.yaml --max-pages 3 --parallel 4
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import yaml

from .config import SCANS_DIR
from .scanner.crawler import crawl
from .urls import TargetNotAllowed, check_target, host_of, normalize_url


async def _scan_one(entry: dict, out_root: Path, max_pages: int, sem: asyncio.Semaphore) -> dict:
    url = normalize_url(entry["url"])
    row = {"sector": entry.get("sector"), "label": entry.get("label"), "url": url, "ok": False}
    try:
        check_target(url)
    except TargetNotAllowed as exc:
        row["error"] = str(exc)
        return row
    async with sem:
        try:
            facts = await crawl(url, max_pages=max_pages, observe_first_ms=7000, observe_ms=3000)
        except Exception as exc:  # one broken site must not stop the batch
            row["error"] = f"{type(exc).__name__}: {str(exc).splitlines()[0][:150]}"
            return row
    out_dir = out_root / host_of(url).replace(".", "-")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    third = [r for r in facts["requests"] if r["third_party"]]
    landing_hosts = sorted({r["host"] for r in third if r["phase"] == "landing"})
    row.update(
        ok=facts["stats"]["pages"] > 0 and any(p["status"] for p in facts["pages"]),
        pages=facts["stats"]["pages"],
        page_status=[p["status"] for p in facts["pages"]],
        third_party_hosts=facts["stats"]["third_party_hosts"],
        landing_third_party_hosts=landing_hosts,
        cookies=facts["stats"]["cookies"],
        third_party_cookies=sum(1 for c in facts["cookies"] if c["third_party"]),
        top_hosts=[h for h, _ in Counter(r["host"] for r in third).most_common(8)],
        facts=str(out_dir / "facts.json"),
    )
    return row


async def run(entries: list[dict], max_pages: int, parallel: int) -> tuple[Path, list[dict]]:
    out_root = SCANS_DIR / f"batch-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out_root.mkdir(parents=True, exist_ok=True)
    sem = asyncio.Semaphore(parallel)
    rows = await asyncio.gather(*(_scan_one(e, out_root, max_pages, sem) for e in entries))
    (out_root / "summary.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_root, rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qalqon.batch")
    parser.add_argument("sites", help="YAML file with a 'sites' list of {sector, label, url}")
    parser.add_argument("--max-pages", type=int, default=3)
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    entries = yaml.safe_load(Path(args.sites).read_text(encoding="utf-8"))["sites"]
    out_root, rows = asyncio.run(run(entries, args.max_pages, args.parallel))
    for row in rows:
        if not row.get("ok"):
            print(f"[FAIL] {row['sector']:14s} {row['url']}  {row.get('error') or row.get('page_status')}")
            continue
        print(
            f"[ok]   {row['sector']:14s} {row['url']:28s} pages={row['pages']} 3p-hosts={row['third_party_hosts']:3d} "
            f"cookies={row['cookies']:3d} (3p {row['third_party_cookies']})"
        )
        print(f"       landing 3p: {', '.join(row['landing_third_party_hosts'][:12])}")
    print(f"\nsaved: {out_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
