"""Re-evaluate saved scans without crawling again (after a rule or detector change).

Usage (from backend/):
    .venv/Scripts/python -m qalqon.rescore ../scans/<scan_id>            # one scan
    .venv/Scripts/python -m qalqon.rescore ../scans/batch-<stamp>        # every facts.json inside
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .enrich import enrich_facts
from .rules_engine import evaluate, format_report


def rescore_file(facts_path: Path, re_enrich: bool) -> dict:
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    if re_enrich or "hosts" not in facts:
        enrich_facts(facts)
        facts_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    report = evaluate(facts)
    (facts_path.parent / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qalqon.rescore")
    parser.add_argument("path", help="scan directory, batch directory or facts.json")
    parser.add_argument("--re-enrich", action="store_true", help="recompute countries/owners (after entities.yaml changes)")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    path = Path(args.path)
    files = [path] if path.is_file() else sorted(path.rglob("facts.json"))
    for facts_path in files:
        report = rescore_file(facts_path, args.re_enrich)
        print(f"\n=== {report['site']}  ({facts_path.parent.name})")
        print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
