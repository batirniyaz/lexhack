"""Trackers that load before any consent, session recording, personal data leaking in URLs."""

from __future__ import annotations

import re

from . import TRACKING_CATEGORIES, detector

_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+(?:@|%40)[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Only clear phone numbers: an explicit +998 prefix, or a phone-like parameter name. A bare "998…" digit run is
# usually a random ID (verified false positive on 20.11).
_UZ_PHONE = re.compile(
    r"(?:(?:\+|%2B)998(?:[\s\-]|%20)*\d{2}(?:[\s\-]|%20)*\d{3}(?:[\s\-]|%20)*\d{2}(?:[\s\-]|%20)*\d{2}(?!\d))"
    r"|(?:[?&](?:phone|tel|mobile|telefon|msisdn)=(?:%2B|\+)?998\d{9}(?!\d))",
    re.I,
)


@detector("trackers_before_consent")
def trackers_before_consent(facts: dict, params: dict):
    categories = set(params.get("categories") or TRACKING_CATEGORIES)
    groups: dict[str, dict] = {}
    for host in facts.get("hosts", []):
        if not (host["third_party"] and host["on_landing"] and host.get("category") in categories):
            continue
        key = host.get("entity") or host["host"]
        group = groups.setdefault(key, {"entity": host.get("entity"), "country": host.get("country"), "categories": set(), "hosts": []})
        group["categories"].add(host["category"])
        group["hosts"].append(host["host"])
    landing_cookies = [c["name"] for c in facts.get("cookies", []) if c["set_on_landing"] and c["third_party"]]
    evidence = []
    for key, group in groups.items():
        group["categories"] = sorted(group["categories"])
        evidence.append({
            "summary": f"{key} ({group['country'] or '?'}; {', '.join(group['categories'])}) loads on the first visit, before any consent",
            "data": group,
        })
    if evidence and landing_cookies:
        evidence.append({"summary": f"{len(landing_cookies)} third-party cookies are set on the first visit",
                         "data": {"cookies": landing_cookies[:30]}})
    return evidence


@detector("session_replay")
def session_replay(facts: dict, params: dict):
    evidence = []
    for host in facts.get("hosts", []):
        if host["third_party"] and host.get("category") == "session_replay":
            evidence.append({"summary": f"Session recording service {host.get('entity') or host['host']} ({host.get('country') or '?'})",
                             "data": {"host": host["host"], "entity": host.get("entity"), "country": host.get("country")}})
    pages = (facts.get("session_replay") or {}).get("webvisor_pages") or []
    if pages:
        evidence.append({"summary": "Yandex Metrica Webvisor (records clicks and form input) is enabled",
                         "data": {"pages": pages[:5], "entity": "Yandex", "country": "RU"}})
    return evidence


def _mask(value: str) -> str:
    return value[:3] + "***" + value[-2:] if len(value) > 6 else "***"


@detector("url_pii")
def url_pii(facts: dict, params: dict):
    evidence, seen = [], set()
    for request in facts.get("requests", []):
        if not request["third_party"]:
            continue
        for kind, pattern in (("email", _EMAIL), ("phone", _UZ_PHONE)):
            match = pattern.search(request["url"])
            if match and (request["host"], kind) not in seen:
                seen.add((request["host"], kind))
                evidence.append({"summary": f"A {kind} appears in a request URL sent to {request['host']}",
                                 "data": {"host": request["host"], "kind": kind, "sample": _mask(match.group(0))}})
    return evidence
