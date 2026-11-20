"""Read the site's privacy / personal-data policy: required elements + concrete promises, each with a verbatim quote.

The model only extracts. Code then checks that every quote really occurs in the document; anything that cannot be
found is dropped. Contradictions with the scan are computed by code (detectors/documents.py), never by the model.
"""

from __future__ import annotations

import re
from typing import Optional

from .client import LLMError, configured, structured_call

PROMPT_VERSION = "policy-v2"
DOC_PRIORITY = {"pd_policy": 0, "privacy": 1, "cookies": 2, "offer": 3, "terms": 4}
MIN_DOC_CHARS = 500
MAX_TOTAL_CHARS = 150_000
MAX_DOCS = 2

ELEMENTS = {
    "operator": "who the operator (data controller) is: company name / legal details",
    "purposes": "purposes of processing personal data",
    "data_categories": "which categories of personal data are collected",
    "consent": "how consent is given and withdrawn",
    "retention": "how long data is kept",
    "recipients": "third parties / processors that receive data",
    "cross_border": "transfer of data abroad / where data is stored",
    "subject_rights": "rights of the data subject (access, correction, deletion)",
    "contact": "contact for personal-data requests",
    "cookies": "use of cookies / analytics / tracking",
}

CLAIM_TYPES = [
    "data_stored_in_uzbekistan",        # data is stored / processed only in Uzbekistan
    "no_cross_border_transfer",         # data is not transferred abroad
    "cross_border_transfer_disclosed",  # transfer abroad is mentioned (fill countries)
    "no_third_party_sharing",           # data is not shared with third parties
    "third_party_services_listed",      # names concrete services (fill services)
    "tracking_only_with_consent",       # cookies / analytics only after consent
    "no_biometric_data",                # biometric data is not collected
    "other",
]

_ELEMENT_SCHEMA = {
    "type": "object",
    "properties": {"present": {"type": "boolean"}, "quote": {"type": ["string", "null"]}},
    "required": ["present", "quote"],
    "additionalProperties": False,
}
SCHEMA = {
    "type": "object",
    "properties": {
        "language": {"type": "string", "enum": ["uz", "ru", "en", "mixed", "other"]},
        "is_personal_data_policy": {"type": "boolean"},
        "elements": {
            "type": "object",
            "properties": {name: _ELEMENT_SCHEMA for name in ELEMENTS},
            "required": list(ELEMENTS),
            "additionalProperties": False,
        },
        "claims": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": CLAIM_TYPES},
                    "statement_en": {"type": "string"},
                    "quote": {"type": "string"},
                    "services": {"type": "array", "items": {"type": "string"}},
                    "countries": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["type", "statement_en", "quote", "services", "countries"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["language", "is_personal_data_policy", "elements", "claims"],
    "additionalProperties": False,
}

SYSTEM = """You read website legal documents (privacy policy, personal-data policy, public offer, terms) from Uzbekistan.
They may be in Uzbek (Latin or Cyrillic), Russian or English.

Return JSON that matches the schema. Rules:
1. Quotes must be copied VERBATIM from the document, in its original language, one continuous fragment of up to 500
   characters. Quote the WHOLE sentence, including any exceptions or conditions in it ("bundan mustasno",
   "за исключением", "except"), so that a reader sees the full meaning. Never translate, paraphrase or merge fragments.
   If you cannot quote it, it does not exist.
2. elements: for each element set present=true only if the document explicitly covers it, and give the quote; otherwise
   present=false and quote=null.
3. claims: list only explicit promises or statements the site makes about its own handling of data that can be checked
   against its behaviour: where data is stored, whether it goes abroad, whether it is shared with third parties, which
   services (e.g. Google Analytics, Yandex.Metrica, Meta Pixel, Telegram) are used, whether tracking needs consent,
   biometrics. Put service names in `services` and ISO-3166 alpha-2 country codes in `countries` when the claim names
   them, else empty arrays. statement_en is a one-sentence English summary of the claim. Do not invent claims.
4. is_personal_data_policy: true if the text actually describes how personal data is processed."""


def _norm(text: str) -> str:
    text = text.lower().replace("­", "")
    text = re.sub(r"[ʼʻ’‘`´']", "'", text)
    text = re.sub(r"[«»“”„\"]", '"', text)
    text = re.sub(r"[‐-‒–—−]", "-", text)
    return re.sub(r"\s+", " ", text).strip()


def quote_found(quote: Optional[str], normalized_text: str) -> bool:
    """True if the quote occurs in the text (ignoring case, whitespace and quote styles; '…' splits allowed)."""
    if not quote:
        return False
    parts = [p.strip() for p in re.split(r"…|\.\.\.", _norm(quote)) if p.strip()]
    if not parts:
        return False
    position = 0
    for part in parts:
        if len(part) < 12 and len(parts) > 1:
            continue
        index = normalized_text.find(part, position)
        if index < 0:
            return False
        position = index + len(part)
    return True


def _select_documents(facts: dict) -> list[dict]:
    docs = [d for d in facts.get("documents", []) if d.get("visited") and len(d.get("text") or "") >= MIN_DOC_CHARS]
    docs.sort(key=lambda d: DOC_PRIORITY.get(d.get("kind"), 9))
    chosen, total = [], 0
    for doc in docs:
        if len(chosen) >= MAX_DOCS or total + len(doc["text"]) > MAX_TOTAL_CHARS:
            continue
        chosen.append(doc)
        total += len(doc["text"])
    return chosen


def analyze_policy(facts: dict) -> dict:
    """Fill facts['policy'] with the LLM extraction (verified quotes only). Never raises."""
    if facts.get("blocked"):
        facts["policy"] = {"status": "skipped", "reason": "site blocked the scanner"}
        return facts["policy"]
    docs = _select_documents(facts)
    if not docs:
        facts["policy"] = {"status": "no_document", "reason": "no legal document text was collected"}
        return facts["policy"]
    if not configured():
        facts["policy"] = {"status": "skipped", "reason": "ANTHROPIC_API_KEY is not set"}
        return facts["policy"]

    combined = "\n\n".join(f"=== DOCUMENT {i + 1}: {d['kind']} — {d['url']} ===\n{d['text']}" for i, d in enumerate(docs))
    user = f"Site: {facts.get('site')}\n\n{combined}"
    try:
        result = structured_call(SYSTEM, user, SCHEMA, PROMPT_VERSION)
    except LLMError as exc:
        facts["policy"] = {"status": "error", "reason": str(exc), "documents": [d["url"] for d in docs]}
        return facts["policy"]

    normalized = _norm(combined)
    data = result.data
    elements, dropped = {}, 0
    for name, item in data["elements"].items():
        verified = bool(item["present"] and quote_found(item["quote"], normalized))
        if item["present"] and not verified:
            dropped += 1
        # A claimed-but-unverifiable element is NOT reported as missing (precision over recall, D-019).
        elements[name] = {"present": item["present"], "quote": item["quote"] if verified else None,
                          "verified": verified, "label": ELEMENTS[name]}
    claims = []
    for claim in data["claims"]:
        if quote_found(claim["quote"], normalized):
            claims.append(claim)
        else:
            dropped += 1

    facts["policy"] = {
        "status": "ok",
        "documents": [{"url": d["url"], "kind": d["kind"], "chars": len(d["text"])} for d in docs],
        "language": data["language"],
        "is_personal_data_policy": data["is_personal_data_policy"],
        "elements": elements,
        "claims": claims,
        "dropped_unverified_quotes": dropped,
        "model": result.model,
        "cached": result.cached,
        "usage": result.usage,
        "prompt_version": PROMPT_VERSION,
    }
    return facts["policy"]
