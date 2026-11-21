"""Parser rules on small pages written after the real lex.uz markup."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lexuz import parse  # noqa: E402


def block(kind, ident, text, marker="lx_elem"):
    menu = '<div class="lx_elem2"><div class="lx_elem3"><span>Hujjatga taklif yuborish</span></div></div>'
    return f'<div class="{kind} {marker}">{menu}<div name="{ident}" id="{ident}">{text}</div></div>'


def page(*blocks, head=""):
    return f'<html><head><title>&nbsp;PF-1-сон 01.02.2020.&nbsp;Test hujjati</title></head><body>{head}<div id="divCont">{"".join(blocks)}</div></body></html>'


def elements(*blocks):
    return parse.parse_doc(page(*blocks), -1)[1]


def test_interface_labels_never_reach_the_text():
    found = elements(block("ACT_TEXT", "-10", "Asosiy matn."))
    assert [e["text"] for e in found] == ["Asosiy matn."]


def test_negative_ids_are_kept():
    assert elements(block("ACT_TEXT", "-10", "Matn."))[0]["element_id"] == "-10"


def test_article_and_parts():
    found = elements(
        block("TEXT_HEADER_DEFAULT", "-1", "1-bob. Umumiy qoidalar"),
        block("CLAUSE_DEFAULT", "-2", "5-modda. Asosiy tushunchalar"),
        block("ACT_TEXT", "-3", "Birinchi qism."),
        block("ACT_TEXT", "-4", "Ikkinchi qism."),
    )
    assert found[1]["article"] == "5-modda"
    assert found[1]["article_title"] == "Asosiy tushunchalar"
    assert [e["part"] for e in found[2:]] == ["1-qism", "2-qism"]
    assert found[3]["headers"] == "1-bob. Umumiy qoidalar"


def test_list_items_stay_in_the_part_that_opened_them():
    found = elements(
        block("CLAUSE_DEFAULT", "-1", "7-modda. Huquqlar"),
        block("ACT_TEXT", "-2", "Xodim quyidagilarga haqli:"),
        block("ACT_TEXT", "-3", "dam olishga;"),
        block("ACT_TEXT", "-4", "ish haqiga."),
        block("ACT_TEXT", "-5", "Keyingi qism."),
    )
    assert [e["part"] for e in found[1:]] == ["1-qism", "1-qism", "1-qism", "2-qism"]


def test_superscript_article_number_stays_apart():
    found = elements(block("CLAUSE_DEFAULT", "-1", "13<sup>1</sup>-modda. Yangi modda"))
    assert found[0]["article"] == "13¹-modda"


def test_table_cells_do_not_merge():
    found = elements(block("ACT_TEXT", "-1", "<table><tr><td>Bir</td><td>Ikki</td></tr></table>"))
    assert "Bir | Ikki" in found[0]["text"]


def test_bands_in_a_document_without_articles():
    found = elements(
        block("ACT_TEXT", "-1", "1. Nizom tasdiqlansin."),
        block("ACT_TEXT", "-2", "davom etuvchi matn."),
        block("ACT_TEXT", "-3", "2. Nazorat yuklansin."),
    )
    assert [e["band"] for e in found] == ["1", "1", "2"]
    assert all(e["article"] is None for e in found)


def test_appendix_restarts_numbering():
    found = elements(
        block("ACT_TEXT", "-1", "5. Qaror matni."),
        block("ACT_TITLE_APPL", "-2", "Vazirlar Mahkamasi qaroriga 2-ILOVA"),
        block("ACT_TEXT", "-3", "1. Nizom bandi."),
    )
    assert found[2]["appendix"] == "2-ilova"
    assert found[2]["band"] == "1"


def test_higher_header_clears_lower_ones():
    found = elements(
        block("TEXT_HEADER_DEFAULT", "-1", "I BOʻLIM. BIRINCHI"),
        block("TEXT_HEADER_DEFAULT", "-2", "1-bob. Birinchi bob"),
        block("TEXT_HEADER_DEFAULT", "-3", "II BOʻLIM. IKKINCHI"),
        block("ACT_TEXT", "-4", "Matn."),
    )
    assert found[3]["headers"] == "II BOʻLIM. IKKINCHI"


def test_notes_are_kept_but_flagged():
    found = elements(
        block("ACT_TEXT", "-1", "Matn."),
        block("CHANGES_ORIGINS", "-2", "(Qonun tahririda)", "lx_no_select"),
    )
    assert found[1]["is_note"] and not found[1]["is_body"]


def test_links_keep_the_target_paragraph():
    html = page(block("ACT_TEXT", "-1", 'Qarang: <a href="/uz/docs/-7108715?ONDATE=21.09.2024 00#-7108833">Qonun</a>'))
    links = parse.parse_doc(html, -1)[2]
    assert links == [{"from_element": "-1", "doc_id": "-1", "to_doc": "-7108715", "to_element": "-7108833"}]


def test_block_without_the_usual_class_is_not_lost():
    warning = '<div class="COMMENT_FOR_WARNING"><div name="-2" id="-2">Hujjat <a href="/uz/files/99.zip">matni </a>PDF shaklda berilgan.</div></div>'
    act = parse.parse_doc(page(warning), -1)[0]
    assert act["pdf_only"] is True
    assert act["pdf_file"] == "99"


def test_pdf_notice_inside_an_ordinary_comment_counts_too():
    act = parse.parse_doc(page(block("COMMENT", "-2", "Hujjat matni PDF shaklda berilgan.", "lx_no_select")), -1)[0]
    assert act["pdf_only"] is True


def test_text_given_only_in_russian_is_flagged():
    warning = '<div class="COMMENT_FOR_WARNING"><div name="-2" id="-2">Hujjat matni rus tilida berilgan.</div></div>'
    act = parse.parse_doc(page(warning), -1)[0]
    assert (act["ru_only"], act["pdf_only"]) == (True, False)


def test_a_notice_next_to_a_full_text_does_not_hide_it():
    html = page(block("ACT_TEXT", "-1", "Matn. " * 1000), block("COMMENT", "-2", "Hujjat matni PDF shaklda berilgan.", "lx_no_select"))
    assert parse.parse_doc(html, -1)[0]["pdf_only"] is False


def test_a_block_type_nobody_has_seen_counts_as_text():
    assert elements(block("BRAND_NEW_KIND", "-1", "Muhim matn."))[0]["is_body"] is True


def test_requisites_are_not_text_of_the_law():
    assert elements(block("SIGNATURE", "-1", "Prezident Sh. Mirziyoyev"))[0]["is_body"] is False


def test_table_is_text_and_stays_in_its_part():
    found = elements(
        block("CLAUSE_DEFAULT", "-1", "3-modda. Stavkalar"),
        block("ACT_TEXT", "-2", "Stavkalar quyidagicha."),
        block("TABLE_STD", "-3", "<table><tr><td>Tamaki</td><td>5 foiz</td></tr></table>"),
    )
    assert found[2]["is_body"] is True
    assert (found[2]["article"], found[2]["part"]) == ("3-modda", "1-qism")


def test_article_written_as_a_header():
    found = elements(block("TEXT_HEADER_DEFAULT", "-1", "1-modda<br>Umumiy tariflar"), block("ACT_TEXT", "-2", "Matn."))
    assert found[0]["article"] == "1-modda"
    assert found[0]["article_title"] == "Umumiy tariflar"
    assert found[0]["headers"] is None
    assert found[1]["article"] == "1-modda"


def test_article_written_inside_a_long_paragraph():
    found = elements(block("ACT_TEXT", "-1", "1-modda. " + "Qonunga quyidagi oʻzgartirishlar kiritilsin. " * 10))
    assert (found[0]["article"], found[0]["part"]) == ("1-modda", "1-qism")


def test_mention_of_an_article_is_not_an_article():
    found = elements(block("ACT_TEXT", "-1", "5-modda talablariga muvofiq ish koʻriladi."))
    assert found[0]["article"] is None


def test_treaty_style_article():
    assert elements(block("CLAUSE_DEFAULT", "-1", "Modda 4. Ragʻbatlantirish"))[0]["article"] == "4-modda"


def test_number_date_and_title_come_from_the_page_title():
    act = parse.parse_doc(page(block("ACT_TEXT", "-1", "Matn.")), -1)[0]
    assert (act["number"], act["adopted"], act["title"]) == ("PF-1", "01.02.2020", "Test hujjati")


def test_other_language_ids():
    head = """<span onclick="openUrl('/uz/docs/5')" title="На русском">Рус</span><span onclick="openUrl('/uz/docs/1')" title="Ўзбекча">Ўзб</span>"""
    act = parse.parse_doc(page(block("ACT_TEXT", "-1", "Matn."), head=head), -1)[0]
    assert (act["ru_id"], act["other_uz_id"]) == ("5", "1")


def treaty_or_russian(kind, text, *after):
    rows = [f'<div class="{kind}"><div name="-1" id="-1">{text}</div></div>']
    rows += [f'<div class="ACT_TEXT"><div name="-{i}" id="-{i}">{t}</div></div>' for i, t in enumerate(after, 2)]
    return f'<html><head><title>T</title></head><body><div id="divCont">{"".join(rows)}</div></body></html>'


def test_treaties_mark_articles_with_other_blocks():
    for kind in ("TEXT_HEADER_AFTER_SRC", "TEXT_BOLD_CENTER", "TEXT_CENTER", "TEXT_BOLD"):
        _, elements, _ = parse.parse_doc(treaty_or_russian(kind, "1-MODDA", "Matn."), "-9")
        assert elements[1]["article"] == "1-modda", kind


def test_russian_article_heading():
    _, elements, _ = parse.parse_doc(treaty_or_russian("CLAUSE_DEFAULT", "Статья 12. Сроки", "Текст нормы."), "-9")
    assert (elements[1]["article"], elements[1]["article_title"], elements[1]["part"]) == ("12-modda", "Сроки", "1-qism")


def test_russian_article_inside_a_paragraph():
    _, elements, _ = parse.parse_doc(treaty_or_russian("ACT_TEXT", "Статья 3. Настоящий закон вступает в силу."), "-9")
    assert elements[0]["article"] == "3-modda"


def test_a_section_keeps_its_name_from_the_second_line():
    page = treaty_or_russian("TEXT_HEADER_DEFAULT", "X BOʻLIM.<br>QOʻSHILGAN QIYMAT SOLIGʻI", "Matn.")
    _, elements, _ = parse.parse_doc(page, "-9")
    assert elements[1]["headers"] == "X BOʻLIM. QOʻSHILGAN QIYMAT SOLIGʻI"
