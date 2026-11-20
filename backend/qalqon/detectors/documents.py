"""Legal documents: is there a privacy / personal-data policy; LLM-based checks plug in here (step 5)."""

from __future__ import annotations

from . import detector


@detector("privacy_policy_present")
def privacy_policy_present(facts: dict, params: dict):
    docs = [d for d in facts.get("documents", []) if d.get("kind") in ("privacy", "pd_policy")]
    if docs:
        return []
    return [{"summary": f"No privacy or personal-data policy found on {len(facts.get('pages', []))} scanned pages",
             "data": {"pages_scanned": len(facts.get("pages", [])),
                      "other_documents": [d["url"] for d in facts.get("documents", [])][:10]}}]


@detector("policy_content")
def policy_content(facts: dict, params: dict):
    analysis = (facts.get("policy") or {}).get("elements")
    if analysis is None:
        return None  # not evaluated until the LLM step runs
    missing = [name for name, item in analysis.items() if not item.get("present")]
    if not missing:
        return []
    return [{"summary": f"The policy does not mention: {', '.join(missing)}", "data": {"missing": missing}}]


@detector("policy_vs_behavior")
def policy_vs_behavior(facts: dict, params: dict):
    contradictions = (facts.get("policy") or {}).get("contradictions")
    if contradictions is None:
        return None  # not evaluated until the LLM step runs
    return [{"summary": c["summary"], "data": c} for c in contradictions]
