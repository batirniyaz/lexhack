"""Where personal data goes: countries of trackers, form destinations, backends seen in client code."""

from __future__ import annotations

from ..legal_lists import country_status
from ..urls import host_of, registrable_domain
from . import TRACKING_CATEGORIES, detector

DEFAULT_FLAG = ["not_listed", "not_in_known_list", "conditional_unknown"]

# Backends seen in code -> (owner, company country, dpf). Regions do not change the company's country.
BACKEND_OWNERS = {
    "firebase-realtime-db": ("Google", "US", True),
    "firestore": ("Google", "US", True),
    "google-cloud-storage": ("Google", "US", True),
    "google-apps-script": ("Google", "US", True),
    "supabase": ("Supabase", "US", None),
    "aws-s3": ("Amazon Web Services", "US", True),
    "telegram-bot-api": ("Telegram", "AE", None),
    "bitrix24-webhook": ("Bitrix24", "RU", None),
    "amocrm": ("amoCRM / Kommo", "RU", None),
}


@detector("foreign_requests")
def foreign_requests(facts: dict, params: dict):
    categories = set(params.get("categories") or TRACKING_CATEGORIES)
    flag = set(params.get("flag_statuses") or DEFAULT_FLAG)
    groups: dict[str, dict] = {}
    for host in facts.get("hosts", []):
        if not host["third_party"] or host.get("category") not in categories:
            continue
        status = country_status(host.get("country"), host.get("dpf"))
        if status not in flag:
            continue
        key = host.get("entity") or host["host"]
        group = groups.setdefault(key, {"entity": host.get("entity"), "country": host.get("country"),
                                        "status": status, "category": host.get("category"), "hosts": []})
        group["hosts"].append(host["host"])
    return [
        {"summary": f"{key} ({g['country'] or '?'}, {g['category']}) receives visitor identifiers — country status: {g['status']}",
         "data": g}
        for key, g in groups.items()
    ]


@detector("form_submit_destination")
def form_submit_destination(facts: dict, params: dict):
    flag = set(params.get("flag_statuses") or DEFAULT_FLAG)
    site_domains = set(facts.get("site_domains", []))
    hosts = {h["host"]: h for h in facts.get("hosts", [])}
    evidence = []
    pd_forms = [f for f in facts.get("forms", []) if f.get("collects_pd")]
    for form in pd_forms:
        action = form.get("action")
        if not action:
            continue
        host = host_of(action)
        if registrable_domain(host) in site_domains:
            continue
        info = hosts.get(host, {})
        status = country_status(info.get("country"), info.get("dpf"))
        if status in flag or status == "unknown":
            evidence.append({
                "summary": f"Form on {form['pages'][0]} ({', '.join(form['pd_categories'])}) is sent to {host} — country status: {status}",
                "data": {"page": form["pages"][0], "action_host": host, "country": info.get("country"), "status": status,
                         "pd": form["pd_categories"]},
            })
    # Passive mode rarely sees where JS forms post. Client code that calls a messenger/CRM API is a strong sign.
    if pd_forms:
        for backend in facts.get("backends", []):
            if backend["kind"] not in ("telegram-bot-api", "google-apps-script", "bitrix24-webhook", "amocrm"):
                continue
            owner, country, dpf = BACKEND_OWNERS[backend["kind"]]
            status = country_status(country, dpf)
            if status in flag:
                evidence.append({
                    "summary": f"Site has personal-data forms and its client code calls {owner} ({country}) — {backend['kind']}; country status: {status}",
                    "data": {"backend": backend["kind"], "owner": owner, "country": country, "status": status,
                             "source": backend.get("source")},
                })
    return evidence


@detector("baas_detect")
def baas_detect(facts: dict, params: dict):
    flag = set(params.get("flag_statuses") or DEFAULT_FLAG + ["conditional_met"])
    evidence = []
    for backend in facts.get("backends", []):
        if backend["kind"] not in ("firebase-realtime-db", "firestore", "supabase", "aws-s3", "google-cloud-storage"):
            continue
        owner, country, dpf = BACKEND_OWNERS[backend["kind"]]
        status = country_status(country, dpf)
        if status in flag:
            region = f", region {backend['region']}" if backend.get("region") else ""
            evidence.append({
                "summary": f"Client code connects to {backend['kind']} ({owner}, {country}{region}) — check whether personal data is stored there",
                "data": {**backend, "owner": owner, "country": country, "status": status},
            })
    return evidence
