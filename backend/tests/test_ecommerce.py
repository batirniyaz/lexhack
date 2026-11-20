"""E-commerce pilot (D-027): only stores are judged; missing text means "cannot evaluate", not a finding."""

from qalqon.detectors.ecommerce import offer_and_returns, seller_identity, state_language_version, store_signals

STORE_TEXT = "Savatga qoʻshish 120 000 soʻm 85 000 soʻm 40 000 soʻm. Buyurtma berish."


def _facts(text: str, *, lang: str = "uz", docs=None, payments: bool = True) -> dict:
    return {
        "pages": [{"final_url": "https://shop.uz/", "status": 200, "text": text, "lang": lang,
                   "alternates": [], "lang_links": []}],
        "documents": docs if docs is not None else [{"kind": "offer", "url": "https://shop.uz/oferta", "text": ""}],
        "hosts": [{"host": "checkout.paycom.uz", "third_party": True, "category": "payments"}] if payments else [],
    }


def test_not_a_store_is_not_judged():
    facts = _facts("Biz haqimizda. Kompaniya yangiliklari.", docs=[], payments=False)
    assert store_signals(facts) == []
    assert seller_identity(facts, {}) == [] and offer_and_returns(facts, {}) == [] and state_language_version(facts, {}) == []


def test_seller_details_found_in_footer():
    text = STORE_TEXT + ' © "SHOP UZ" MChJ, STIR 301234567, manzil: Toshkent sh., Chilonzor tumani, +998 71 123 45 67'
    assert seller_identity(_facts(text), {}) == []


def test_missing_seller_name_is_a_finding_missing_address_only_is_downgraded():
    finding = seller_identity(_facts(STORE_TEXT + " +998 90 123 45 67"), {})
    assert "legal_name" in finding[0]["data"]["missing"] and finding[0]["data"]["downgrade"] is False
    only_address = seller_identity(_facts(STORE_TEXT + " SHOP MChJ, +998 90 123 45 67"), {})
    assert only_address[0]["data"]["missing"] == ["address"] and only_address[0]["data"]["downgrade"] is True


def test_offer_not_opened_means_cannot_evaluate_returns():
    assert offer_and_returns(_facts(STORE_TEXT), {}) is None
    with_returns = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u", "text": "Tovarni qaytarish 10 kun ichida"}])
    assert offer_and_returns(with_returns, {}) == []
    no_offer = _facts(STORE_TEXT, docs=[])
    assert offer_and_returns(no_offer, {})[0]["data"]["offer_found"] is False


def test_uzbek_version_signals():
    russian_only = _facts("Добавить в корзину 120 000 сум 85 000 сум 40 000 сум. Оформить заказ.", lang="ru")
    assert state_language_version(russian_only, {})[0]["data"]["langs"] == ["ru"]
    with_switch = _facts("Добавить в корзину 120 000 сум 85 000 сум 40 000 сум.", lang="ru")
    with_switch["pages"][0]["lang_links"] = [["https://shop.uz/uz/", "Oʻzbekcha", ""]]
    assert state_language_version(with_switch, {}) == []
    assert state_language_version(_facts(STORE_TEXT, lang=""), {}) is not None  # Uzbek words alone: may pass or not
