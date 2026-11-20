"""Presentation helpers: anonymized names for public demos (D-003, D-017) and replaying a finished scan as a live feed."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

import yaml

from .config import DATA_DIR
from .urls import host_of, registrable_domain


@lru_cache(maxsize=1)
def _sites() -> dict[str, dict]:
    path = DATA_DIR / "reference_sites.yaml"
    if not path.exists():
        return {}
    sites = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("sites", [])
    return {registrable_domain(host_of(s["url"])): s for s in sites if s.get("label")}


def label_for(site_url: str) -> str:
    return _sites().get(registrable_domain(host_of(site_url)), {}).get("label", "Site")


def aliases_for(site_url: str) -> list[str]:
    """Brand names of a reference site — they appear inside policy quotes and must be hidden too."""
    return list(_sites().get(registrable_domain(host_of(site_url)), {}).get("aliases", []))


def anonymize(obj: Any, domains: list[str], label: str, aliases: list[str] | None = None) -> Any:
    """Replace the site's domains (with a slug) and brand aliases (with the label) everywhere, recursively."""
    tag = label.lower().replace(" ", "-")
    domain_list = sorted(set(domains), key=len, reverse=True)
    alias_patterns = [re.compile(re.escape(a), re.IGNORECASE) for a in sorted(set(aliases or []), key=len, reverse=True)]

    def fix(value: Any) -> Any:
        if isinstance(value, str):
            for domain in domain_list:
                value = value.replace(domain, tag)
            for pattern in alias_patterns:
                value = pattern.sub(label, value)
            return value
        if isinstance(value, list):
            return [fix(v) for v in value]
        if isinstance(value, dict):
            return {k: fix(v) for k, v in value.items()}
        return value

    result = fix(obj)
    if isinstance(result, dict):
        result["label"] = label
    return result


def anonymize_other_references(obj: Any, site_url: str) -> Any:
    """Hide every OTHER reference site too: a policy of one site can name another one ("affiliates … including
    Kapitalbank"), which would identify both. Each is replaced by its own label."""
    own = registrable_domain(host_of(site_url))
    label = obj.get("label") if isinstance(obj, dict) else None
    for domain, site in _sites().items():
        if domain == own:
            continue
        obj = anonymize(obj, [domain, domain.replace(".", "-")], site["label"], site.get("aliases", []))
    if isinstance(obj, dict) and label is not None:
        obj["label"] = label
    return obj


def replay_events(scan_dir: Path) -> Iterator[dict]:
    """Rebuild a live feed from saved results (demo fallback when the network is down)."""
    events_file = scan_dir / "events.jsonl"
    if events_file.exists():
        for line in events_file.read_text(encoding="utf-8").splitlines():
            if line.strip():
                yield json.loads(line)
        yield {"type": "end", "status": "done", "replay": True}
        return
    facts = json.loads((scan_dir / "facts.json").read_text(encoding="utf-8"))
    report = json.loads((scan_dir / "report.json").read_text(encoding="utf-8"))
    yield {"type": "start", "scan_id": facts.get("scan_id") or scan_dir.name, "url": facts["site"], "replay": True}
    hosts = {h["host"]: h for h in facts.get("hosts", [])}
    announced: set[str] = set()
    for n, page in enumerate(facts.get("pages", []), start=1):
        yield {"type": "page", "url": page["final_url"], "n": n, "max": len(facts["pages"])}
        for request in facts.get("requests", []):
            host = request["host"]
            if request.get("page") == page["url"] and host not in announced and host in hosts:
                announced.add(host)
                info = hosts[host]
                yield {"type": "host", "host": host, "ip": (info.get("ips") or [None])[0],
                       "third_party": info["third_party"], "phase": request["phase"],
                       **{k: info.get(k) for k in ("server_country", "org", "is_cdn", "entity",
                                                    "company_country", "category", "country")}}
        for form in facts.get("forms", []):
            if form.get("collects_pd") and form["pages"][0] == page["final_url"]:
                yield {"type": "form", "page": page["final_url"], "pd": form["pd_categories"], "consent": form["has_consent"]}
        for doc in facts.get("documents", []):
            if doc.get("visited") and doc.get("url") == page["final_url"]:
                yield {"type": "document", "kind": doc.get("kind"), "url": doc["url"]}
    policy = facts.get("policy") or {}
    if policy:
        yield {"type": "policy_start"}
        yield {"type": "policy", "status": policy.get("status"), "reason": policy.get("reason"),
               "documents": policy.get("documents"), "claims": len(policy.get("claims", [])), "cached": True}
    for finding in report.get("findings", []):
        yield {"type": "finding", "rule_id": finding["rule_id"], "level": finding["level"],
               "title": finding["title"], "evidence": [e["summary"] for e in finding["evidence"][:5]]}
    yield {"type": "done", "scan_id": report.get("scan_id"), "status": report["status"], "score": report["score"],
           "levels": report.get("levels"), "stats": facts.get("stats")}
    yield {"type": "end", "status": "done", "replay": True}
