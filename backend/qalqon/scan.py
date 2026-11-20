"""CLI: run one scan and save scans/<id>/facts.json (+ scan.har).

Usage (from backend/):
    .venv/Scripts/python -m qalqon.scan https://example.uz
    .venv/Scripts/python -m qalqon.scan https://example.uz --events      # one JSON event per line (for the API/SSE)
    .venv/Scripts/python -m qalqon.scan http://127.0.0.1:5500 --allow-private   # local demo site
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime

from .config import SCANS_DIR
from .enrich import enrich_event, enrich_facts
from .rules_engine import evaluate, format_report
from .scanner.crawler import crawl
from .urls import TargetNotAllowed, check_target, host_of, normalize_url


def new_scan_id(url: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", host_of(url))[:40].strip("-")
    return f"{stamp}-{slug}"


def _summary(facts: dict) -> str:
    stats = facts["stats"]
    lines = [
        f"site: {facts['site']}  (domains: {', '.join(facts['site_domains'])})",
        f"pages: {stats['pages']}  requests: {stats['requests']}  "
        f"third-party requests: {stats['third_party_requests']}  cookies: {stats['cookies']}  "
        f"hanging: {stats['pending_requests']}  challenge pages: {stats.get('challenge_pages', 0)}",
    ]
    if facts.get("blocked"):
        lines.append(f"!! BLOCKED by bot protection ({facts['blocked']}) — results are not about the site itself")
    lines.append("pages:")
    for p in facts["pages"]:
        mark = f"  [challenge: {p['challenge']}]" if p.get("challenge") else ""
        lines.append(f"  {p['status']}  {p['final_url'][:70]}  | {(p['title'] or '')[:40]}{mark}")
    lines.append("third-party hosts (server country / network → owner, company country, category):")
    for row in facts.get("hosts", []):
        if not row["third_party"]:
            continue
        server = "CDN" if row["is_cdn"] else (row["server_country"] or "?")
        owner = f"{row['entity']} ({row['company_country']}), {row['category']}" if row["entity"] else "unknown owner"
        mark = "  [landing]" if row["on_landing"] else ""
        lines.append(f"  {row['host'][:42]:42s} {server:4s} {(row['org'] or '')[:22]:22s} → {owner}{mark}")
    if facts.get("flows"):
        lines.append("data flows by country: " + ", ".join(f"{c}: {len(h)}" for c, h in facts["flows"].items()))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qalqon.scan", description="Passive scan of one website.")
    parser.add_argument("url")
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--events", action="store_true", help="print one JSON event per line")
    parser.add_argument("--allow-private", action="store_true", help="allow local/private targets (demo site)")
    parser.add_argument("--scan-id", default=None)
    parser.add_argument("--no-har", action="store_true")
    args = parser.parse_args(argv)

    sys.stdout.reconfigure(encoding="utf-8")
    url = normalize_url(args.url)

    def emit(event: dict) -> None:
        if args.events:
            print(json.dumps(enrich_event(event), ensure_ascii=False), flush=True)

    try:
        check_target(url, allow_private=args.allow_private)
    except TargetNotAllowed as exc:
        emit({"type": "error", "message": str(exc)})
        if not args.events:
            print(f"refused: {exc}", file=sys.stderr)
        return 2

    scan_id = args.scan_id or new_scan_id(url)
    out_dir = SCANS_DIR / scan_id
    out_dir.mkdir(parents=True, exist_ok=True)
    emit({"type": "start", "scan_id": scan_id, "url": url})

    facts = asyncio.run(crawl(url, max_pages=args.max_pages, har_path=None if args.no_har else out_dir / "scan.har", emit=emit))
    facts["scan_id"] = scan_id
    enrich_facts(facts)
    (out_dir / "facts.json").write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    report = evaluate(facts)
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for finding in report["findings"]:
        emit({"type": "finding", "rule_id": finding["rule_id"], "level": finding["level"],
              "title": finding["title"], "evidence": [e["summary"] for e in finding["evidence"][:5]]})
    emit({"type": "done", "scan_id": scan_id, "status": report["status"], "score": report["score"],
          "levels": report.get("levels"), "stats": facts["stats"]})
    if not args.events:
        print(_summary(facts))
        print()
        print(format_report(report))
        print(f"\nsaved: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
