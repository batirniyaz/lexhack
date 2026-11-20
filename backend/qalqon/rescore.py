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
from .llm.policy import analyze_policy
from .rules_engine import evaluate, format_report


def rescore_file(facts_path: Path, re_enrich: bool, llm: bool = False, llm_force: bool = False) -> dict:
    facts = json.loads(facts_path.read_text(encoding="utf-8"))
    changed = False
    if re_enrich or "hosts" not in facts:
        enrich_facts(facts)
        changed = True
    if llm_force or (llm and (facts.get("policy") or {}).get("status") != "ok"):
        analyze_policy(facts)  # disk-cached: re-running costs nothing
        changed = True
    if changed:
        facts_path.write_text(json.dumps(facts, ensure_ascii=False, indent=2), encoding="utf-8")
    report = evaluate(facts)
    (facts_path.parent / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qalqon.rescore")
    parser.add_argument("path", help="scan directory, batch directory or facts.json")
    parser.add_argument("--re-enrich", action="store_true", help="recompute countries/owners (after entities.yaml changes)")
    parser.add_argument("--llm", action="store_true", help="run the LLM policy analysis where it is missing")
    parser.add_argument("--llm-force", action="store_true", help="re-run the LLM analysis (e.g. after a prompt change)")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    path = Path(args.path)
    files = [path] if path.is_file() else sorted(path.rglob("facts.json"))
    for facts_path in files:
        report = rescore_file(facts_path, args.re_enrich, args.llm, args.llm_force)
        policy = (json.loads(facts_path.read_text(encoding="utf-8")).get("policy") or {})
        if policy:
            print(f"\n[policy] {policy.get('status')}  {policy.get('reason') or ''}  claims={len(policy.get('claims', []))} "
                  f"dropped={policy.get('dropped_unverified_quotes')} cached={policy.get('cached')} usage={policy.get('usage')}")
        print(f"\n=== {report['site']}  ({facts_path.parent.name})")
        print(format_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
