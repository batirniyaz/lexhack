"""Uzbek personal identifiers in URLs (F-33): PINFL, passport, bank card, phone, e-mail.

Precision first (D-019): an ID-shaped value counts only if its format is valid AND the parameter name says what it
is (or, for cards, the number is a valid Uzcard / Humo number). Values are never stored, only masked samples.

- PINFL (JShShIR): 14 digits; 1st digit 3–6 (century and sex), then the birth date DDMMYY. The check-digit
  algorithm is NOT VERIFIED, so it is not used.
- Passport / ID card: two Latin letters + 7 digits (e.g. AA1234567), only with a passport-like parameter name.
- Bank card: 16 digits passing the Luhn check, with prefix 8600 (Uzcard) or 9860 (Humo), or a card-like name.
"""

from __future__ import annotations

import re
from datetime import date
from urllib.parse import parse_qsl, urlsplit

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"^\+?998[\s-]?\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}$")
PASSPORT = re.compile(r"^[A-Z]{2}\d{7}$")

HINTS = {
    "pinfl": re.compile(r"pinfl|pnfl|jshshir|jshir|personal_?id", re.I),
    "passport": re.compile(r"pass(port)?|pasport|seriya|series|doc(ument)?_?(no|num|number)", re.I),
    "card": re.compile(r"card|karta|pan\b|cc_?num", re.I),
    "phone": re.compile(r"phone|tel|mobile|telefon|msisdn", re.I),
}
UZ_CARD_PREFIXES = ("8600", "9860")


def luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def is_pinfl(value: str) -> bool:
    if not re.fullmatch(r"[3-6]\d{13}", value):
        return False
    day, month, year = int(value[1:3]), int(value[3:5]), int(value[5:7])
    century = 1900 if value[0] in "34" else 2000
    try:
        date(century + year, month, day)
    except ValueError:
        return False
    return True


def is_card(value: str, hinted: bool) -> bool:
    digits = re.sub(r"[\s-]", "", value)
    if not re.fullmatch(r"\d{16}", digits) or not luhn_ok(digits):
        return False
    return hinted or digits.startswith(UZ_CARD_PREFIXES)


def mask(value: str) -> str:
    return value[:3] + "***" + value[-2:] if len(value) > 6 else "***"


def find_in_url(url: str) -> list[dict]:
    """Personal identifiers in the query string of a URL: [{kind, param, sample}] (samples are masked)."""
    found = []
    try:
        query = urlsplit(url).query
    except ValueError:
        return found
    for name, raw in parse_qsl(query, keep_blank_values=False):
        value = raw.strip()
        if not value or len(value) > 200:
            continue
        kind = None
        if EMAIL.fullmatch(value):
            kind = "email"
        elif PHONE.match(value) and (value.startswith("+") or HINTS["phone"].search(name)):
            kind = "phone"
        elif is_pinfl(value) and HINTS["pinfl"].search(name):
            kind = "pinfl"
        elif PASSPORT.match(value) and HINTS["passport"].search(name):
            kind = "passport"
        elif is_card(value, bool(HINTS["card"].search(name))):
            kind = "card"
        if kind:
            found.append({"kind": kind, "param": name, "sample": mask(value)})
    return found
