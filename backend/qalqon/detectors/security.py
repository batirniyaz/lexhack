"""Basic transport security of pages and forms (passive: only what the visitor's browser receives)."""

from __future__ import annotations

from urllib.parse import urlparse

from . import detector

RECOMMENDED_HEADERS = {
    "strict-transport-security": "HSTS",
    "content-security-policy": "Content-Security-Policy",
    "x-content-type-options": "X-Content-Type-Options",
}


@detector("https")
def https(facts: dict, params: dict):
    evidence = []
    for page in facts.get("pages", []):
        if urlparse(page.get("final_url") or "").scheme == "http":
            evidence.append({"summary": f"Page served without HTTPS: {page['final_url']}", "data": {"page": page["final_url"]}})
    for form in facts.get("forms", []):
        if form.get("collects_pd") and (form.get("action") or "").startswith("http://"):
            evidence.append({"summary": f"Personal-data form posts over plain HTTP: {form['action']}",
                             "data": {"page": form["pages"][0], "action": form["action"]}})
    return evidence


@detector("security_headers")
def security_headers(facts: dict, params: dict):
    pages = [p for p in facts.get("pages", []) if not p.get("challenge") and p.get("status")]
    if not pages:
        return None
    headers = pages[0].get("headers") or {}
    missing = [label for key, label in RECOMMENDED_HEADERS.items() if key not in headers]
    if not missing:
        return []
    return [{"summary": f"Home page response lacks: {', '.join(missing)}", "data": {"missing": missing}}]
