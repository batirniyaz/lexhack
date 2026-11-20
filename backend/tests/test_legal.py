"""Law citations (F-34): only quotes found verbatim in lex.uz text survive; findings get the article text."""

from qalqon.legal.citations import _article_key, attach_quotes, law_quotes
from qalqon.legal.lexrag import verified_citations


def test_fabricated_quote_is_dropped():
    data = {"result": {
        "contexts": [{"chunk_id": "c1", "text": "21-modda. Rozilik\nSubyekt rozilikni har qanday shaklda beradi."}],
        "citations": [
            {"chunk_id": "c1", "quote": "Subyekt rozilikni har qanday shaklda beradi.", "article": "21-modda"},
            {"chunk_id": "c1", "quote": "Operator rozilikni olmasligi mumkin va bu qonuniy.", "article": "21-modda"},
        ]}}
    kept = verified_citations(data)
    assert [c["quote"] for c in kept] == ["Subyekt rozilikni har qanday shaklda beradi."]


def test_apostrophe_variants_do_not_break_the_check():
    data = {"result": {"contexts": [{"chunk_id": "c", "text": "Shaxsga doir maʼlumotlar Oʻzbekiston hududida saqlanadi."}],
                       "citations": [{"chunk_id": "c", "quote": "Shaxsga doir ma'lumotlar O‘zbekiston hududida saqlanadi."}]}}
    assert len(verified_citations(data)) == 1


def test_article_labels():
    assert _article_key("21-modda") == "21"
    assert _article_key("27¹-modda") == "27¹"
    assert _article_key("27-1-modda") == "27¹"


def test_rules_get_verbatim_article_text():
    if "ZRU-547:21" not in law_quotes():
        return  # law_quotes.json not generated in this environment
    basis = attach_quotes([{"act": "ZRU-547", "article": "21", "articles": ["21"]}])
    citation = basis[0]["citations"][0]
    assert citation["heading"].startswith("21-modda")
    assert citation["verified_by_lawyer"] is False and citation["url"].startswith("https://lex.uz/")
