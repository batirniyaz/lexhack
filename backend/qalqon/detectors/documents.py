"""Legal documents: is there a policy, is it complete, does it contradict what the site actually does.

The LLM (llm/policy.py) only extracts elements and promises with verified quotes into facts['policy'].
Everything below is deterministic code over those quotes and the scan facts (D-010).
"""

from __future__ import annotations

import re

from ..urls import host_of
from . import TRACKING_CATEGORIES, detector

# Services the policy must name: trackers + AI services that receive what visitors type (F-32).
NAMED_CATEGORIES = TRACKING_CATEGORIES | {"ai"}

# A promise with exceptions ("…except when…") is not a clean contradiction: the finding is downgraded one level.
EXCEPTION_MARKERS = re.compile(r"mustasno|istisno|исключени|кроме случа|except|unless", re.I)

REQUIRED_ELEMENTS = ["operator", "purposes", "data_categories", "retention", "recipients",
                     "cross_border", "subject_rights", "contact"]

# How an owner may be named in a policy (lower-case substrings).
ENTITY_ALIASES = {
    "Google": ["google", "gtag", "doubleclick", "firebase"],
    "Meta": ["meta", "facebook", "instagram", "fb pixel", "pixel"],
    "Yandex": ["yandex", "яндекс", "metrika", "метрик", "metrica"],
    "Microsoft": ["microsoft", "clarity", "bing"],
    "VK / Mail.ru Group": ["vk.com", "vkontakte", "вконтакте", "mail.ru", "mytarget"],
    "TikTok / ByteDance": ["tiktok", "bytedance"],
    "AppsFlyer": ["appsflyer"],
    "Hotjar": ["hotjar"],
    "Amplitude": ["amplitude"],
    "Mixpanel": ["mixpanel"],
    "GrowthBook": ["growthbook"],
    "Telegram": ["telegram"],
    "Cloudflare": ["cloudflare"],
    "Amazon Web Services": ["amazon", "aws"],
    "Criteo": ["criteo"],
}


# Policy coverage per service in 4 levels (F-17, after WhoGetsMyData): the product is named / only the company /
# only the kind of service / nothing. The finding logic is unchanged: a service counts as undisclosed when neither
# its product nor its company is named (ENTITY_ALIASES = products + companies); the levels add detail for the lawyer.
PRODUCTS = {
    "Google": ["google analytics", "google tag manager", "gtag", "doubleclick", "google ads", "adsense", "firebase"],
    "Meta": ["facebook pixel", "meta pixel", "pixel"],
    "Yandex": ["yandex.metrika", "yandex metrika", "yandex metrica", "metrika", "metrica", "яндекс.метрика",
               "яндекс метрика", "метрик", "webvisor", "вебвизор"],
    "Microsoft": ["clarity", "bing"],
    "VK / Mail.ru Group": ["mytarget", "vk pixel", "top.mail.ru"],
}
COMPANIES = {
    "Google": ["google"], "Meta": ["meta", "facebook", "instagram"], "Yandex": ["yandex", "яндекс"],
    "Microsoft": ["microsoft"], "VK / Mail.ru Group": ["vk.com", "vkontakte", "вконтакте", "mail.ru"],
}
KIND_WORDS = {
    "analytics": ["analitik", "аналитич", "analytic", "statistik", "статистик", "statistic"],
    "advertising": ["reklama", "реклам", "advertis"],
    "marketing": ["marketing", "маркетинг"],
    "session_replay": ["seans", "сеанс", "session record", "запись действий"],
    "social": ["ijtimoiy tarmoq", "социальн", "social network"],
    "ab_testing": ["a/b", "тестирован", "experiment"],
    "ai": ["sunʼiy intellekt", "sun'iy intellekt", "искусственн", "artificial intelligence"],
}
COVERAGE_LEVELS = ("named", "company", "kind", "none")


# A kind word counts only next to words about services or recipients: "reklama joylashtirish" (placing ads on the
# platform) or "reklama aksiyasi" (a promo campaign) must not count as "advertising services receive data"
# (both seen in real policies on 21.11).
# Generic "third parties / partners" is not enough: "advertising SMS, including from third parties" (seen 21.11)
# is about mailings, not about advertising services that receive visitor data.
RECIPIENT_CONTEXT = ["xizmat", "servis", "сервис", "service", "provayder", "провайдер", "provider", "cookie", "куки",
                     "kuki", "hisoblagich", "счетчик", "счётчик", "counter", "pixel", "piksel", "пиксел"]
# Clause boundaries: ";", line breaks, sentence ends, numbered items like "5.4.6.".
_CLAUSE = re.compile(r"[;\n]|(?<=[.!?])\s+(?=\S)|\b\d+(?:\.\d+)+\.?\s")


def _mentions_any(text: str, words: list[str]) -> bool:
    """A kind word (stem) in the same clause as a word about services or recipients."""
    for clause in _CLAUSE.split(text):
        if any(word in clause for word in words) and any(context in clause for context in RECIPIENT_CONTEXT):
            return True
    return False


def policy_coverage(facts: dict) -> list[dict] | None:
    """For each tracking or AI service the site uses: how the policy names it. None if there is no analysed policy."""
    policy = _policy(facts)
    if policy is None:
        return None
    text = _policy_text(facts, policy)
    if not text:
        return None
    rows = []
    for name, row in _by_entity(_tracking_hosts(facts)).items():
        products = PRODUCTS.get(name) or ENTITY_ALIASES.get(name) or []
        companies = COMPANIES.get(name) or [name.lower()]
        if products and _mentions(text, products):
            level = "named"
        elif _mentions(text, companies):
            level = "company"
        elif any(_mentions_any(text, KIND_WORDS.get(cat, [])) for cat in row["categories"]):
            level = "kind"
        else:
            level = "none"
        rows.append({"entity": name, "country": row["country"], "categories": sorted(row["categories"]),
                     "level": level, "hosts": row["hosts"][:5]})
    rows.sort(key=lambda r: (COVERAGE_LEVELS.index(r["level"]) * -1, r["entity"]))
    return rows


def _mentions(text: str, aliases: list[str]) -> bool:
    """Whole-word match, so 'meta' does not hit 'metamaʼlumot' and 'aws' does not hit 'laws'."""
    return any(re.search(rf"(?<!\w){re.escape(alias)}(?!\w)", text) for alias in aliases)


def _policy(facts: dict):
    policy = facts.get("policy") or {}
    return policy if policy.get("status") == "ok" else None


def _policy_text(facts: dict, policy: dict) -> str:
    urls = {d["url"] for d in policy.get("documents", [])}
    return " ".join((d.get("text") or "") for d in facts.get("documents", []) if d.get("url") in urls).lower()


def _tracking_hosts(facts: dict) -> list[dict]:
    return [h for h in facts.get("hosts", []) if h["third_party"] and h.get("category") in NAMED_CATEGORIES]


def _by_entity(hosts: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for host in hosts:
        key = host.get("entity") or host["host"]
        row = result.setdefault(key, {"entity": key, "country": host.get("country"), "hosts": [], "on_landing": False,
                                      "categories": set()})
        row["hosts"].append(host["host"])
        if host.get("category"):
            row["categories"].add(host["category"])
        row["on_landing"] = row["on_landing"] or host.get("on_landing", False)
    return result


def _describe(entities: list[dict], limit: int = 5) -> str:
    text = ", ".join(f"{e['entity']} ({e['country'] or '?'})" for e in entities[:limit])
    return text + (f" and {len(entities) - limit} more" if len(entities) > limit else "")


@detector("privacy_policy_present")
def privacy_policy_present(facts: dict, params: dict):
    docs = [d for d in facts.get("documents", []) if d.get("kind") in ("privacy", "pd_policy")]
    policy = facts.get("policy") or {}
    if docs or (policy.get("status") == "ok" and policy.get("is_personal_data_policy")):
        return []
    return [{"summary": f"No privacy or personal-data policy found on {len(facts.get('pages', []))} scanned pages",
             "data": {"pages_scanned": len(facts.get("pages", [])),
                      "other_documents": [d["url"] for d in facts.get("documents", [])][:10]}}]


@detector("policy_content")
def policy_content(facts: dict, params: dict):
    policy = _policy(facts)
    if policy is None or not policy.get("is_personal_data_policy"):
        return None  # nothing to judge: no analysed policy (PD-POL-01 covers a missing one)
    required = params.get("required") or REQUIRED_ELEMENTS
    elements = policy.get("elements", {})
    missing = [name for name in required if name in elements and not elements[name]["present"]]
    evidence = []
    if missing:
        evidence.append({"summary": "The policy does not cover: " + "; ".join(elements[m]["label"] for m in missing),
                         "data": {"missing": missing}})
    # Services the site really uses but the policy never names.
    text = _policy_text(facts, policy)
    undisclosed = [
        row for name, row in _by_entity(_tracking_hosts(facts)).items()
        if name in ENTITY_ALIASES and not _mentions(text, ENTITY_ALIASES[name])
    ]
    if undisclosed and text:
        evidence.append({"summary": f"The policy never mentions services the site uses: {_describe(undisclosed)}",
                         "data": {"undisclosed": [{"entity": u["entity"], "country": u["country"]} for u in undisclosed]}})
    # Transfers abroad named explicitly (a foreign country), while the site also sends data to other countries.
    named = {c.upper() for claim in policy.get("claims", []) if claim["type"] == "cross_border_transfer_disclosed"
             for c in claim.get("countries", []) if c and c.upper() != "UZ"}
    if named:
        foreign = [row for row in _by_entity(_tracking_hosts(facts)).values()
                   if row["country"] and row["country"] not in ("UZ", *named)]
        if foreign:
            evidence.append({
                "summary": f"The policy names cross-border transfer to {', '.join(sorted(named))}, "
                           f"but the site also sends visitor identifiers to: {_describe(foreign)}",
                "data": {"named": sorted(named), "observed": [{"entity": e["entity"], "country": e["country"]} for e in foreign]},
            })
    return evidence


@detector("policy_vs_behavior")
def policy_vs_behavior(facts: dict, params: dict):
    policy = _policy(facts)
    if policy is None:
        return None
    entities = _by_entity(_tracking_hosts(facts))
    foreign = [e for e in entities.values() if e["country"] and e["country"] != "UZ"]
    landing = [e for e in entities.values() if e["on_landing"]]
    # Only the landing page's own host: static subdomains often sit on CDNs we cannot tell from hosting (e.g. CloudFront).
    pages = [p for p in facts.get("pages", []) if not p.get("challenge")]
    landing_host = host_of(pages[0]["final_url"]) if pages else None
    own_hosting_abroad = sorted({
        h["server_country"] for h in facts.get("hosts", [])
        if h["host"] == landing_host and not h.get("is_cdn") and h.get("server_country") not in (None, "UZ", "LOCAL")
    })
    biometric = [u for u in facts.get("uploads", []) if u.get("pd") == "photo" or u.get("capture") is not None]

    evidence, seen = [], set()

    def add(claim: dict, observed: str, data: dict) -> None:
        if (claim["type"], observed) in seen:
            return
        seen.add((claim["type"], observed))
        has_exceptions = bool(EXCEPTION_MARKERS.search(claim["quote"]))
        note = " (the promise has exceptions — a lawyer must judge whether they cover this)" if has_exceptions else ""
        evidence.append({
            "summary": f"Policy says «{claim['quote']}» — but {observed}{note}",
            "data": {"claim_type": claim["type"], "quote": claim["quote"], "claim_en": claim["statement_en"],
                     "downgrade": has_exceptions, **data},
        })

    for claim in policy.get("claims", []):
        kind = claim["type"]
        if kind in ("data_stored_in_uzbekistan", "no_cross_border_transfer"):
            if foreign:
                add(claim, f"the site sends visitor data abroad: {_describe(foreign)}",
                    {"observed": [{"entity": e["entity"], "country": e["country"]} for e in foreign]})
            if own_hosting_abroad:
                add(claim, f"the site itself is hosted abroad ({', '.join(own_hosting_abroad)})",
                    {"observed_hosting": own_hosting_abroad})
        elif kind == "no_third_party_sharing" and entities:
            rows = list(entities.values())
            add(claim, f"{len(rows)} third-party tracking services receive visitor identifiers (IP, cookies): {_describe(rows)}",
                {"observed": [{"entity": e["entity"], "country": e["country"]} for e in rows],
                 "caveat": "Whether online identifiers are personal data under ZRU-547 is open (V-08)."})
        elif kind == "tracking_only_with_consent" and landing:
            add(claim, f"trackers load on the first visit before any consent: {_describe(landing)}",
                {"observed": [{"entity": e["entity"], "country": e["country"]} for e in landing]})
        elif kind == "no_biometric_data" and biometric:
            add(claim, f"the site asks for a photo/selfie on {biometric[0]['page']}", {"observed": biometric[:3]})
        # "cross_border_transfer_disclosed" is NOT a contradiction source: a disclosure of one transfer is not a promise
        # that there are no others (verified false positive on 20.11). Incompleteness is reported by policy_content.
    return evidence
