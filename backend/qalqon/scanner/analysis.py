"""Pure-Python analysis of what the page JS returned: personal-data field types, legal documents, backends in code."""

from __future__ import annotations

import re
from typing import Optional

# Field -> personal-data category. Order matters: first match wins.
_FIELD_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("password", re.compile(r"password|parol|пароль", re.I)),
    ("otp", re.compile(r"\b(otp|sms[- ]?kod|sms[- ]?code|код из sms|tasdiqlash kodi|verification code)\b", re.I)),
    ("pinfl", re.compile(r"pinfl|пинфл|jshshir|jshir|жшшир|personal identification number", re.I)),
    ("passport", re.compile(r"pasport|passport|паспорт|seriya|серия", re.I)),
    ("card", re.compile(r"cc-number|card ?number|karta raqami|номер карты|\bkarta\b|\bкарт", re.I)),
    ("birth_date", re.compile(r"birth|tug.ilgan|дата рождения|день рождения|bday|dob\b", re.I)),
    ("email", re.compile(r"e-?mail|pochta|почта|электронн", re.I)),
    ("phone", re.compile(r"phone|telefon|телефон|\btel\b|mobile|raqam|номер", re.I)),
    ("address", re.compile(r"address|manzil|адрес|street|ko.cha|улица", re.I)),
    ("name", re.compile(r"\bname\b|first.?name|last.?name|full.?name|fio|фио|имя|фамилия|отчество|\bism\b|familiya|sharif|ismingiz", re.I)),
    ("photo", re.compile(r"selfi|селфи|photo|rasm|фото|yuz|лицо|face", re.I)),
]
_SEARCH = re.compile(r"search|qidir|поиск|izla|\bq\b|query", re.I)
PD_CATEGORIES = {"name", "phone", "email", "passport", "pinfl", "birth_date", "address", "card", "photo"}
SENSITIVE_CATEGORIES = {"passport", "pinfl", "card", "photo"}


_SITE_ADDRESS = re.compile(r"sayt manzil|veb[- ]?sayt|web[- ]?site|website|адрес сайта|веб[- ]?сайт|\burl\b|havola|ссылк|link", re.I)


def classify_field(field: dict) -> Optional[str]:
    ftype = field.get("type", "")
    if ftype in ("checkbox", "radio", "range", "color"):
        return None
    if ftype == "search" or _SEARCH.search(f"{field.get('name', '')} {field.get('id', '')} {field.get('placeholder', '')}"):
        return None
    # A website address is not personal data. "Sayt manzili" (manzil = address) was read as a postal address and
    # raised PD-CNS-01 on a plain URL field (seen on our own site, 21.11).
    if ftype == "url" or _SITE_ADDRESS.search(" ".join(str(field.get(k) or "") for k in ("name", "id", "placeholder", "label"))):
        return None
    if ftype == "password":
        return "password"
    if ftype == "email":
        return "email"
    if ftype == "tel":
        return "phone"
    if ftype == "file":
        accept = field.get("accept", "")
        text = f"{field.get('label', '')} {field.get('name', '')}"
        if field.get("capture") is not None or (("image" in accept or not accept) and re.search(r"selfi|селфи|yuz|лицо|face|photo|rasm|фото", text, re.I)):
            return "photo"
        return None
    if (field.get("autocomplete") or "").startswith("cc-"):
        return "card"
    haystack = " ".join(str(field.get(k) or "") for k in ("name", "id", "placeholder", "label", "autocomplete"))
    for category, pattern in _FIELD_PATTERNS:
        if pattern.search(haystack):
            return category
    if field.get("maxlength") == 14 and (field.get("inputmode") == "numeric" or field.get("pattern")):
        return "pinfl"
    return None


def analyze_form(form: dict) -> dict:
    categories = []
    for field in form["fields"]:
        category = classify_field(field)
        field["pd"] = category
        if category in PD_CATEGORIES and category not in categories:
            categories.append(category)
    form["pd_categories"] = categories
    form["collects_pd"] = bool(categories)
    consent = form.get("consent") or {}
    form["has_consent"] = bool(consent.get("checkbox") or consent.get("sentence"))
    return form


_DOC_KINDS = [
    ("pd_policy", re.compile(r"shaxsiy ma.lumot|shaxsga doir|персональн|personal.?data|personal-data", re.I)),
    ("privacy", re.compile(r"maxfiylik|konfiden|конфиденц|privacy", re.I)),
    ("offer", re.compile(r"oferta|оферт|public.?offer", re.I)),
    ("terms", re.compile(r"shartlar|условия|terms|agreement|соглашени|foydalanish", re.I)),
    ("cookies", re.compile(r"cookie", re.I)),
]


def document_kind(url: str, title: str) -> Optional[str]:
    haystack = f"{url} {title}"
    for kind, pattern in _DOC_KINDS:
        if pattern.search(haystack):
            return kind
    return None


# Backends visible in client code. We never store secrets: tokens / IDs are redacted.
_BACKEND_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("firebase-realtime-db", re.compile(r"https?://([a-z0-9-]+)\.firebaseio\.com", re.I)),
    ("firebase-realtime-db", re.compile(r"([a-z0-9-]+)\.([a-z0-9-]+)\.firebasedatabase\.app", re.I)),
    ("firestore", re.compile(r"firestore\.googleapis\.com", re.I)),
    ("supabase", re.compile(r"https?://([a-z0-9]{12,})\.supabase\.co", re.I)),
    ("aws-s3", re.compile(r"([a-z0-9.-]*)s3[.-]([a-z0-9-]+)\.amazonaws\.com", re.I)),
    ("google-cloud-storage", re.compile(r"storage\.googleapis\.com/([a-z0-9._-]+)", re.I)),
    ("telegram-bot-api", re.compile(r"api\.telegram\.org/bot", re.I)),
    ("google-apps-script", re.compile(r"script\.google\.com/macros/s/", re.I)),
    ("bitrix24-webhook", re.compile(r"[a-z0-9-]+\.bitrix24\.(?:ru|com|uz|kz)/rest", re.I)),
    ("amocrm", re.compile(r"[a-z0-9-]+\.amocrm\.(?:ru|com)", re.I)),
]
_WEBVISOR = re.compile(r"webvisor\s*:\s*(?:true|!0|1)", re.I)


def find_backends(text: str, source: str) -> list[dict]:
    found = []
    for kind, pattern in _BACKEND_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        item = {"kind": kind, "source": source[:300]}
        if kind == "aws-s3":
            item["region"] = match.group(2)
        elif kind == "firebase-realtime-db" and match.lastindex and match.lastindex >= 2:
            item["region"] = match.group(2)
        found.append(item)
    return found


def has_webvisor(text: str) -> bool:
    return bool(_WEBVISOR.search(text))
