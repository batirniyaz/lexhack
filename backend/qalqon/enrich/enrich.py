"""Add server country / ASN / CDN flag / owning company to every request, and build per-host and per-country summaries."""

from __future__ import annotations

from collections import defaultdict

from .entities import identify
from .geo import ATTRIBUTION, geodb


def _host_facts(host: str, ip: str | None) -> dict:
    facts = {"server_country": None, "asn": None, "org": None, "is_cdn": False}
    if ip:
        facts.update(geodb().lookup(ip))
    owner = identify(host)
    facts.update(owner or {"entity": None, "company_country": None, "dpf": None, "category": None})
    # The country that matters legally is not settled yet (V-16): we keep both and expose the best guess.
    if facts["is_cdn"]:
        facts["server_country"] = None
    facts["country"] = facts["company_country"] or facts["server_country"]
    return facts


def enrich_event(event: dict) -> dict:
    """Live feed: add country/company to a 'host' event as soon as it is seen."""
    if event.get("type") == "host":
        event.update(_host_facts(event["host"], event.get("ip")))
    return event


def enrich_facts(facts: dict) -> dict:
    db = geodb()
    hosts: dict[str, dict] = {}
    for record in facts["requests"]:
        host = record["host"]
        if host not in hosts or (record["ip"] and not hosts[host].get("_ip")):
            info = _host_facts(host, record["ip"])
            info["_ip"] = record["ip"]
            hosts[host] = info
        info = hosts[host]
        for key in ("server_country", "asn", "org", "is_cdn", "entity", "company_country", "dpf", "category", "country"):
            record[key] = info[key]

    summary: dict[str, dict] = {}
    for record in facts["requests"]:
        host = record["host"]
        row = summary.setdefault(host, {
            "host": host,
            "third_party": record["third_party"],
            "ips": set(),
            "requests": 0,
            "on_landing": False,
            "methods": set(),
            **{k: hosts[host][k] for k in ("server_country", "asn", "org", "is_cdn", "entity",
                                             "company_country", "dpf", "category", "country")},
        })
        row["requests"] += 1
        row["on_landing"] = row["on_landing"] or record["phase"] == "landing"
        row["methods"].add(record["method"])
        if record["ip"]:
            row["ips"].add(record["ip"])
    host_rows = []
    for row in summary.values():
        row["ips"] = sorted(row["ips"])
        row["methods"] = sorted(row["methods"])
        host_rows.append(row)
    host_rows.sort(key=lambda r: (not r["third_party"], -r["requests"]))

    flows: dict[str, list[str]] = defaultdict(list)
    for row in host_rows:
        if row["third_party"]:
            flows[row["country"] or "?"].append(row["host"])

    facts["hosts"] = host_rows
    facts["flows"] = dict(sorted(flows.items(), key=lambda kv: -len(kv[1])))
    facts["enrichment"] = {"geo_db": db.files, "geo_attribution": ATTRIBUTION, "geo_available": db.available}
    return facts
