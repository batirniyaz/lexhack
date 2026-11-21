"""E-commerce transparency pilot (D-027): who the seller is, the offer with return terms, an Uzbek version.

Only for sites that look like online stores (two or more store signals). Precision first (D-019): when the text we
need was not collected (blocked page, offer not opened), the detector says "cannot evaluate" (None) instead of
guessing. Norms (via lex-rag, not yet verified by a lawyer): Law "On electronic commerce" art. 16 part 3 (the offer
names the seller, postal and e-mail address, phone; delivery and payment terms), art. 26–27 (returns); Law "On
protection of consumers' rights" art. 5 part 5 and art. 6 part 5 (information in the state language).
"""

from __future__ import annotations

import re

from . import detector

_CART = re.compile(r"savat|корзин|cart\b|checkout|buyurtma berish|оформить заказ|в корзину|savatga|xarid qilish|купить",
                   re.I)
_PRICE = re.compile(r"\d[\d\s.,]*\s?(?:so['ʻ’`]?m\b|сум\b|uzs\b)", re.I)

# Seller details. Legal forms: MChJ / XK / AJ / YaTT (uz), ООО / АО / ИП / ЧП (ru), LLC / JSC.
_LEGAL_FORM = re.compile(
    r"\b(?:mchj|m\.ch\.j|mas['ʻ’`]?uliyati cheklangan|aj|aksiyadorlik jamiyati|xk|qk|yatt|ooo|ооо|оао|ао|ип|чп|"
    r"мчж|ақ|хк|ятт|llc|jsc|ltd)\b", re.I)
# An organisation's name in quotes, e.g. "NAJOT TAʼLIM MARKAZI", «UZUM MARKET» — many sellers (schools, NTM) carry no
# MChJ-style legal form next to the name (false finding on 21.11 without this).
_QUOTED_ORG = re.compile(r"[«\"“„]\s*[A-ZА-ЯЁЎҚҒҲ][A-ZА-ЯЁЎҚҒҲ0-9ʻʼ'’`.\- ]{2,60}[»\"”]")
_STIR = re.compile(r"(?:stir|inn|инн|стир|soliq to['ʻ’`]?lovchi)[^0-9]{0,25}(\d{9})\b", re.I)
# Uzbek phone numbers in any grouping: "+998 71 123 45 67", "78 888 9 888", "(90) 1234567". Operator / city codes only,
# so prices and dates do not match.
_PHONE = re.compile(r"(?:\+?998[  \-()]*)?\(?\b(?:33|50|55|61|62|65|66|67|69|70|71|72|73|74|75|76|77|78|79|88|90|91|"
                    r"93|94|95|97|98|99)\)?(?:[  \-]*\d){7}(?!\d)")  # no line breaks inside a number
_GOODS = re.compile(r"tovar|товар|\bgoods\b", re.I)
_PAID = re.compile(r"to['ʻ’`]?lov|оплат|payment|narx|цен[аы]|price|haq to['ʻ’`]?la|тариф|tarif", re.I)
_FREE = re.compile(r"bepul|безвозмезд|бесплатн|free of charge", re.I)
_CONTACT = re.compile(r"contact|kontakt|aloqa|about|o-nas|biz-haqimizda|haqimizda|rekvizit|реквизит|контакт", re.I)
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# An address, not just the word "address": "manzil:", a street, a district or a city mark ("pochta manzillari" in a
# policy is not an address; seen on 21.11).
_ADDRESS = re.compile(r"(?:manzil|адрес|address)\s*:|ko['ʻ’`]?chasi|\bko['ʻ’`]?ch\.|улица|\bул\.|tumani\b|\bр-н\b|"
                      r"\bрайон\b|shahri\b|toshkent sh|г\.\s?ташкент|tashkent city|\bmahalla", re.I)
_RETURNS = re.compile(r"qaytar|возврат|вернуть|almashtir|обмен|return|refund", re.I)

# Uzbek: Latin letters and very common words, or the Cyrillic letters only Uzbek uses.
_UZ_LATIN = re.compile(r"oʻ|gʻ|o['’`]|g['’`]|\b(?:va|uchun|bilan|xarid|savat|buyurtma|narxi|yetkazib)\b", re.I)
_UZ_CYRILLIC = re.compile(r"[ўқғҳЎҚҒҲ]")


def _pages(facts: dict) -> list[dict]:
    return [p for p in facts.get("pages", []) if not p.get("challenge") and (p.get("status") or 0) < 400]


def _texts(facts: dict) -> str:
    page_text = " ".join(p.get("text") or "" for p in _pages(facts))
    doc_text = " ".join(d.get("text") or "" for d in facts.get("documents", []))
    return f"{page_text} {doc_text}"


def store_signals(facts: dict) -> list[str]:
    """Why we think the site is an online store (empty = not a store)."""
    signals = []
    landing_text = " ".join(p.get("text") or "" for p in _pages(facts)[:1])
    if _CART.search(landing_text):
        signals.append("cart or checkout on the landing page")
    if len(_PRICE.findall(landing_text)) >= 3:
        signals.append("prices in soʻm on the landing page")
    if any(h.get("category") == "payments" and h.get("third_party") for h in facts.get("hosts", [])):
        signals.append("payment service connected")
    if any(d.get("kind") == "offer" for d in facts.get("documents", [])):
        signals.append("public offer document")
    return signals


def _is_store(facts: dict) -> tuple[bool, list[str]]:
    signals = store_signals(facts)
    return len(signals) >= 2, signals


@detector("seller_identity")
def seller_identity(facts: dict, params: dict):
    store, signals = _is_store(facts)
    if not store:
        return []
    if not any(p.get("text") for p in _pages(facts)):
        return None  # the landing page text was not collected (older scan or blocked)
    # The law wants these details in the offer (art. 16). Without the offer text, "not shown" would only mean "not on
    # the pages we opened" — a thin support page on 21.11 (OLX) proved that — so: cannot evaluate.
    if not any(d.get("kind") in ("offer", "terms") and d.get("text") for d in facts.get("documents", [])):
        return None
    text = _texts(facts)
    found = {
        "legal_name": bool(_LEGAL_FORM.search(text) or _QUOTED_ORG.search(text)),
        "stir": bool(_STIR.search(text)),
        "phone": bool(_PHONE.search(text)),
        "email": bool(_EMAIL.search(text)),
        "address": bool(_ADDRESS.search(text)),
    }
    missing = [k for k in ("legal_name", "phone", "address") if not found[k]]
    if not found["phone"] and found["email"]:
        missing.remove("phone")  # any working contact satisfies "phone or e-mail"
    if not missing:
        return []
    serious = "legal_name" in missing  # without the seller's name the buyer can't know who they contract with
    return [{"summary": f"Online store ({', '.join(signals)}): the scanned pages and documents do not show "
                        f"{', '.join(m.replace('_', ' ') for m in missing)} of the seller",
             "data": {"missing": missing, "found": found, "store_signals": signals, "downgrade": not serious}}]


@detector("offer_and_returns")
def offer_and_returns(facts: dict, params: dict):
    store, signals = _is_store(facts)
    if not store:
        return []
    docs = [d for d in facts.get("documents", []) if d.get("kind") in ("offer", "terms")]
    if not docs:
        return [{"summary": f"Online store ({', '.join(signals)}): no public offer or terms of sale found on the scanned pages",
                 "data": {"store_signals": signals, "offer_found": False}}]
    texts = [d.get("text") or "" for d in docs if d.get("text")]
    if not texts:
        return None  # the offer exists but was not opened: we can't say what it contains
    if any(_RETURNS.search(t) for t in texts):
        return []
    goods = sum(len(_GOODS.findall(t)) for t in texts) >= 3
    if params.get("returns_required"):
        # Edition from 12.12.2026 (ZRU-1173, art. 16 part 3 new para 8): the offer itself must state how goods, works,
        # services or money are returned. Judged only for sales: goods, or a paid offer — a free platform agreement
        # (a telecom "use the platform free of charge" text, 21.11) is not a sale.
        paid = any(len(_PAID.findall(t)) >= 3 and not _FREE.search(t[:4000]) for t in texts)
        if not (goods or paid):
            return []
        return [{"summary": "The offer says nothing about returning goods or money — a direct requirement of the offer "
                            "from 12.12.2026 (art. 16 part 3, as amended by ZRU-1173)",
                 "data": {"documents": [d["url"] for d in docs][:5], "offer_found": True, "future_rule": True}}]
    # Art. 26–27 are about goods. An offer for services (telecom, courses) without the word "goods" is not judged:
    # a telecom /oferta page was flagged on 21.11 although returns of goods do not apply to it.
    if not goods:
        return []
    return [{"summary": "The offer / terms of sale say nothing about returning goods or money",
             "data": {"documents": [d["url"] for d in docs][:5], "offer_found": True, "downgrade": True}}]


@detector("state_language_version")
def state_language_version(facts: dict, params: dict):
    store, signals = _is_store(facts)
    if not store:
        return []
    pages = _pages(facts)
    if not any(p.get("text") for p in pages):
        return None
    langs = {(p.get("lang") or "").lower() for p in pages}
    alternates = {(hl or "").lower() for p in pages for hl, _ in p.get("alternates") or []}
    switch = [href for p in pages for href, text, hl in p.get("lang_links") or []
              if re.search(r"(^|[\/=_-])(uz|oz)([\/?&#_-]|$)", href, re.I) or re.match(r"(uz|oz|o.zbek|ўзбек|узбек)", text or "", re.I)
              or (hl or "").lower().startswith("uz")]
    text = " ".join(p.get("text") or "" for p in pages)
    uz_text = len(_UZ_LATIN.findall(text)) >= 15 or len(_UZ_CYRILLIC.findall(text)) >= 15
    if any(l.startswith("uz") for l in langs) or any(a.startswith("uz") for a in alternates) or switch or uz_text:
        return []
    return [{"summary": f"Online store ({', '.join(signals)}): no Uzbek-language version found "
                        f"(page language: {', '.join(sorted(l for l in langs if l)) or 'not set'}; no switch to Uzbek)",
             "data": {"langs": sorted(l for l in langs if l), "alternates": sorted(a for a in alternates if a),
                      "store_signals": signals}}]
