"""Reading a search page, on markup copied from lex.uz."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lexuz import listing  # noqa: E402

ROW = """<td>
  <span class="lx_act_state"><i class="fa fa-check-circle status_code_{state}"></i></span>
  <div class="dd-table__main-left-desc"><a class="lx_link " href="/uz/docs/{doc}" target="_blank">{title}</a></div>
  <div class="dd-table__main-extra"><div><span class="badge badge-pill badge-nine">{meta}</span></div>
  <div><a class="lx_link" href="/uz/pdfs/{doc}" target="_blank" title="PDF"></a></div></div>
</td>"""


def page(*rows, extra=""):
    return f"<html><body><form><input type='hidden' name='__VIEWSTATE' value='abc'/><input type='hidden' value='nameless'/></form><table><tr>{''.join(rows)}</tr></table>{extra}</body></html>"


def test_row_fields():
    rows = listing.rows_of(page(ROW.format(state="r", doc="-85", title="Nom", meta="Qaror, 01.01.2020 yildagi 5-son")))
    assert rows == [{"doc_id": "-85", "title": "Nom", "meta": "Qaror, 01.01.2020 yildagi 5-son", "state": "r"}]


def test_pdf_link_is_not_a_document():
    assert len(listing.rows_of(page(ROW.format(state="y", doc="1", title="A", meta="B")))) == 1


def test_positive_and_negative_ids_are_both_documents():
    rows = listing.rows_of(page(ROW.format(state="y", doc="-1", title="A", meta="B"), ROW.format(state="y", doc="2", title="C", meta="D")))
    assert [r["doc_id"] for r in rows] == ["-1", "2"]


def test_total():
    assert listing.total_of("<div>Izlash</div> <span>28499</span> hujjat topildi") == 28499


def test_years_from_the_filter():
    html = '<option value="&fyear=2022">2022 (1175)</option><option value="&amp;fyear=2021">2021 (1260)</option>'
    assert listing.years_of(html) == {2022: 1175, 2021: 1260}


def test_hidden_fields_need_a_name():
    assert listing.form_fields(page()) == {"__VIEWSTATE": "abc"}


def test_next_page_link():
    link = """<a href="javascript:__doPostBack(&#39;ucFoundActsControl$LinkButton1&#39;,&#39;&#39;)">Keyingisi</a>"""
    assert listing.has_next(page(extra=link))
    assert not listing.has_next(page())


def test_url_with_and_without_a_year():
    assert listing.list_url("nat") == "/uz/search/nat?lang=4"
    assert listing.list_url("nat", 2019) == "/uz/search/nat?lang=4&fyear=2019"
