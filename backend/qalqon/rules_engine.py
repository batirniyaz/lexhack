"""Rules engine: YAML rules + detectors -> findings + score (ARCHITECTURE.md §2.4, §2.10).

Rule sources (same `id` -> the later one wins):
  1. backend/rules_draft/*.yaml — Role 1 drafts, verified: false
  2. rules/*.yaml               — Role 2 (lawyer), the authoritative version
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import yaml

from .legal.citations import attach_quotes
from .config import BACKEND_DIR, RULES_DIR
from .detectors import DETECTORS
from .legal_lists import country_status, list_info

DRAFT_RULES_DIR = BACKEND_DIR / "rules_draft"
PENALTY = {"violation": 15, "risk": 5, "recommendation": 1}
DOWNGRADE = {"violation": "risk", "risk": "recommendation"}
LEVEL_ORDER = {"violation": 0, "risk": 1, "recommendation": 2}
NON_RULE_FILES = {"countries.yaml"}


def _load_dir(directory: Path, source: str) -> dict[str, dict]:
    rules = {}
    if not directory.exists():
        return rules
    for path in sorted(directory.glob("*.yaml")):
        if path.name in NON_RULE_FILES:
            continue
        rule = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if "id" in rule and "detector" in rule:
            rule["_source"] = f"{source}/{path.name}"
            rules[rule["id"]] = rule
    return rules


def load_rules() -> list[dict]:
    merged = {**_load_dir(DRAFT_RULES_DIR, "rules_draft"), **_load_dir(RULES_DIR, "rules")}
    return sorted(merged.values(), key=lambda r: (LEVEL_ORDER.get(r.get("level"), 9), r["id"]))


def _counts_for_score(evidence: list[dict]) -> bool:
    """Findings whose every piece of evidence has an undetermined country are shown but do not lower the score."""
    statuses = [e.get("data", {}).get("status") for e in evidence]
    return not (statuses and all(s == "unknown" for s in statuses))


def _flows_status(facts: dict) -> list[dict]:
    flows: dict[str, dict] = defaultdict(lambda: {"hosts": [], "entities": set()})
    dpf_by_country: dict[str, list] = defaultdict(list)
    for host in facts.get("hosts", []):
        if not host["third_party"]:
            continue
        country = host.get("country") or "?"
        flows[country]["hosts"].append(host["host"])
        if host.get("entity"):
            flows[country]["entities"].add(host["entity"])
        dpf_by_country[country].append(host.get("dpf"))
    result = []
    for country, flow in flows.items():
        dpf = all(dpf_by_country[country]) if dpf_by_country[country] else None
        result.append({"country": country, "status": country_status(None if country == "?" else country, dpf),
                       "hosts": len(flow["hosts"]), "entities": sorted(flow["entities"])})
    return sorted(result, key=lambda r: -r["hosts"])


def evaluate(facts: dict) -> dict:
    base = {
        "scan_id": facts.get("scan_id"),
        "site": facts.get("site"),
        "scanned_at": facts.get("scanned_at"),
        "countries_list": list_info(),
        "stats": facts.get("stats"),
    }
    if facts.get("blocked"):
        return {**base, "status": "blocked", "blocked": facts["blocked"], "score": None,
                "findings": [], "not_evaluated": [], "flows": []}

    findings, not_evaluated = [], []
    for rule in load_rules():
        detect = DETECTORS.get(rule["detector"])
        if detect is None:
            not_evaluated.append({"rule_id": rule["id"], "reason": f"unknown detector {rule['detector']}"})
            continue
        evidence = detect(facts, rule.get("params") or {})
        if evidence is None:
            not_evaluated.append({"rule_id": rule["id"], "reason": "prerequisites missing (e.g. LLM policy analysis)"})
            continue
        if not evidence:
            continue
        level = rule["level"]
        downgraded = all((e.get("data") or {}).get("downgrade") for e in evidence)
        if downgraded:
            level = DOWNGRADE.get(level, level)  # detector is unsure for every piece of evidence (D-019)
        findings.append({
            "rule_id": rule["id"],
            "level": level,
            "rule_level": rule["level"],
            "downgraded": downgraded,
            "title": rule.get("title", {}),
            "evidence": evidence,
            "legal_basis": attach_quotes(rule.get("legal_basis", [])),  # + verbatim lex.uz text (F-34)
            "sanction": rule.get("sanction"),
            "fix": rule.get("fix", {}),
            "verified": bool(rule.get("verified")),
            "counts_for_score": _counts_for_score(evidence),
            "source": rule["_source"],
        })

    penalty = sum(PENALTY.get(f["level"], 0) for f in findings if f["counts_for_score"])
    levels = {level: sum(1 for f in findings if f["level"] == level) for level in PENALTY}
    return {**base, "status": "ok", "score": max(0, 100 - penalty), "levels": levels,
            "findings": findings, "not_evaluated": not_evaluated, "flows": _flows_status(facts)}


LEVEL_ICON = {"violation": "🔴", "risk": "🟡", "recommendation": "⚪"}


def format_report(report: dict) -> str:
    if report["status"] == "blocked":
        return f"CLOSED TO THE CHECK: bot protection ({report['blocked']}) — no findings produced."
    lines = [f"score: {report['score']}/100   " + "  ".join(f"{LEVEL_ICON[k]} {v}" for k, v in report["levels"].items())]
    for finding in report["findings"]:
        title = finding["title"].get("en") or finding["title"].get("ru") or finding["rule_id"]
        flag = "" if finding["verified"] else "  (norm not verified by lawyer)"
        lines.append(f"{LEVEL_ICON[finding['level']]} {finding['rule_id']}: {title}{flag}")
        for item in finding["evidence"][:4]:
            lines.append(f"     - {item['summary']}")
        if len(finding["evidence"]) > 4:
            lines.append(f"     … +{len(finding['evidence']) - 4} more")
    if report["not_evaluated"]:
        lines.append("not evaluated: " + ", ".join(n["rule_id"] for n in report["not_evaluated"]))
    lines.append("data flows: " + ", ".join(f"{f['country']} {f['hosts']} ({f['status']})" for f in report["flows"]))
    lines.append(f"country list: {report['countries_list']['file']} (verified: {report['countries_list']['verified']})")
    return "\n".join(lines)
