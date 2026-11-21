"""E-commerce pilot (D-027): only stores are judged; missing text means "cannot evaluate", not a finding."""

from qalqon.detectors.ecommerce import offer_and_returns, seller_identity, state_language_version, store_signals

STORE_TEXT = "Savatga qoʻshish 120 000 soʻm 85 000 soʻm 40 000 soʻm. Buyurtma berish."


def _facts(text: str, *, lang: str = "uz", docs=None, payments: bool = True) -> dict:
    return {
        "pages": [{"final_url": "https://shop.uz/", "status": 200, "text": text, "lang": lang,
                   "alternates": [], "lang_links": []}],
        "documents": docs if docs is not None else [{"kind": "offer", "url": "https://shop.uz/oferta", "text": ""}],
        "hosts": [{"host": "checkout.paycom.uz", "third_party": True, "category": "payments", "on_landing": False}] if payments else [],
    }


def test_not_a_store_is_not_judged():
    facts = _facts("Biz haqimizda. Kompaniya yangiliklari.", docs=[], payments=False)
    assert store_signals(facts) == []
    assert seller_identity(facts, {}) == [] and offer_and_returns(facts, {}) == [] and state_language_version(facts, {}) == []


OFFER = [{"kind": "offer", "url": "https://shop.uz/oferta", "text": "Ommaviy oferta. Tovarni qaytarish 10 kun."}]


def test_seller_details_found_in_footer():
    text = STORE_TEXT + ' © "SHOP UZ" MChJ, STIR 301234567, manzil: Toshkent sh., Chilonzor tumani, +998 71 123 45 67'
    assert seller_identity(_facts(text, docs=OFFER), {}) == []
    school = STORE_TEXT + ' "NAJOT TAʼLIM MARKAZI" direktori. Tel: 78 888 9 888. Manzil: Chilonzor tumani'
    assert seller_identity(_facts(school, docs=OFFER), {}) == []   # quoted name + grouped phone (real case 21.11)


def test_seller_check_needs_the_offer_text():
    assert seller_identity(_facts(STORE_TEXT), {}) is None  # offer not read: cannot say the details are missing


def test_missing_seller_name_is_a_finding_missing_address_only_is_downgraded():
    finding = seller_identity(_facts(STORE_TEXT + " +998 90 123 45 67", docs=OFFER), {})
    assert "legal_name" in finding[0]["data"]["missing"] and finding[0]["data"]["downgrade"] is False
    only_address = seller_identity(_facts(STORE_TEXT + " SHOP MChJ, +998 90 123 45 67", docs=OFFER), {})
    assert only_address[0]["data"]["missing"] == ["address"] and only_address[0]["data"]["downgrade"] is True


def test_offer_not_opened_means_cannot_evaluate_returns():
    assert offer_and_returns(_facts(STORE_TEXT), {}) is None
    with_returns = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u", "text": "Tovarni qaytarish 10 kun ichida"}])
    assert offer_and_returns(with_returns, {}) == []
    no_offer = _facts(STORE_TEXT, docs=[])
    assert offer_and_returns(no_offer, {})[0]["data"]["offer_found"] is False
    services = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u", "text": "Aloqa xizmatlari ko'rsatish shartlari"}])
    assert offer_and_returns(services, {}) == []  # an offer for services is not judged on returns of goods
    goods = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u", "text": "tovar tovar tovar yetkazib berish"}])
    assert offer_and_returns(goods, {})[0]["data"]["downgrade"] is True


def test_uzbek_version_signals():
    russian_only = _facts("Добавить в корзину 120 000 сум 85 000 сум 40 000 сум. Оформить заказ.", lang="ru")
    assert state_language_version(russian_only, {})[0]["data"]["langs"] == ["ru"]
    with_switch = _facts("Добавить в корзину 120 000 сум 85 000 сум 40 000 сум.", lang="ru")
    with_switch["pages"][0]["lang_links"] = [["https://shop.uz/uz/", "Oʻzbekcha", ""]]
    assert state_language_version(with_switch, {}) == []
    assert state_language_version(_facts(STORE_TEXT, lang=""), {}) is not None  # Uzbek words alone: may pass or not


def test_future_rule_12_12_2026_for_paid_offers_only():
    """F-51: from 12.12.2026 a paid offer without return terms becomes a finding; a free platform agreement does not."""
    paid = "Ommaviy oferta. Xizmat narxi va toʻlov tartibi. Toʻlov karta orqali. Tarif narxi. Toʻlov muddati."
    free = "Platformadan bepul foydalanish kelishuvi. Toʻlov yoʻq. Narx yoʻq. Toʻlov. Tarif."
    store_paid = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u", "text": paid}])
    store_free = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u", "text": free}])
    assert offer_and_returns(store_paid, {}) == []                       # today: services, not judged
    future = offer_and_returns(store_paid, {"returns_required": True})
    assert future and future[0]["data"]["future_rule"] is True
    assert offer_and_returns(store_free, {"returns_required": True}) == []  # free agreement is not a sale


def test_law_change_has_the_upcoming_edition():
    from qalqon.rules_engine import evaluate
    facts = _facts(STORE_TEXT, docs=[{"kind": "offer", "url": "u",
                                      "text": "Ommaviy oferta. Narx va toʻlov. Toʻlov karta orqali. Tarif narxi. Toʻlov."}])
    facts.update({"site": "https://shop.uz", "scanned_at": "2026-11-21T00:00:00+00:00", "stats": {}})
    upcoming = evaluate(facts)["law_change"]["next"]
    assert upcoming["in_force"]["from"] == "2026-12-12"
    assert any(c["rule_id"] == "EC-02" and c["after"] == "risk" for c in upcoming["changes"])
