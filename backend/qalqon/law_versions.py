"""Law versions: re-evaluate saved facts under an earlier wording of the law (F-16, W4).

Crawling is the expensive part; evaluating stored facts under another rule set is free. The report gets a
`law_change` block: score and findings under the previous wording vs now, and what changed. No LLM, no new crawl.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Callable, Optional

import yaml

from .config import DATA_DIR

VERSIONS_FILE = DATA_DIR / "law_versions.yaml"


@lru_cache(maxsize=1)
def versions() -> list[dict]:
    if not VERSIONS_FILE.exists():
        return []
    return (yaml.safe_load(VERSIONS_FILE.read_text(encoding="utf-8")) or {}).get("versions") or []


def overrides_for(version_id: str) -> Optional[dict]:
    """Rule overrides for a version, each carrying that version's legal basis."""
    for version in versions():
        if version["id"] == version_id and not version.get("current"):  # past or future
            basis = version.get("basis")
            result = {}
            for rule_id, override in (version.get("overrides") or {}).items():
                result[rule_id] = {**override, **({"legal_basis": [basis]} if basis else {})}
            return result
    return None


def _summary(report: dict) -> dict:
    return {"score": report.get("score"), "levels": report.get("levels"),
            "findings": {f["rule_id"]: f["level"] for f in report.get("findings", [])}}


def law_change(facts: dict, current: dict, evaluate: Callable[..., dict]) -> Optional[dict]:
    """Compare the current report with the same facts under the previous version of the law."""
    if current.get("status") != "ok":
        return None
    previous = next((v for v in versions() if not v.get("current") and not v.get("future")), None)
    now = next((v for v in versions() if v.get("current")), None)
    upcoming = next((v for v in versions() if v.get("future")), None)
    overrides = overrides_for(previous["id"]) if previous else None
    if not previous or not now or not overrides:
        return None
    before = _summary(evaluate(facts, overrides=overrides, with_law_change=False))
    after = _summary(current)
    from .rules_engine import load_rules  # local import: rules_engine imports this module
    titles = {r["id"]: r.get("title", {}) for r in load_rules()}

    def diff(a: dict, b: dict) -> list[dict]:
        out = []
        for rule_id in sorted(set(a["findings"]) | set(b["findings"])):
            old, new = a["findings"].get(rule_id), b["findings"].get(rule_id)
            if old != new:
                out.append({"rule_id": rule_id, "before": old, "after": new, "title": titles.get(rule_id)})
        return out

    changes = diff(before, after)
    nxt = None
    if upcoming and overrides_for(upcoming["id"]):
        future = _summary(evaluate(facts, overrides=overrides_for(upcoming["id"]), with_law_change=False))
        nxt = {"id": upcoming["id"], "label": upcoming["label"], "in_force": upcoming["in_force"],
               "basis": upcoming.get("basis"), **future, "changes": diff(after, future)}
    return {
        "previous": {"id": previous["id"], "label": previous["label"], "in_force": previous["in_force"],
                     "basis": previous.get("basis"), **before},
        "current": {"id": now["id"], "label": now["label"], "in_force": now["in_force"], **after},
        "next": nxt,
        "changes": changes,
        "note": "Same saved facts evaluated under both wordings; no new scan. Texts from lex.uz, not verified by a lawyer.",
    }
