"""Pieces must carry a citation a tester can check."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag import chunking  # noqa: E402


def element(seq, text, kind="ACT_TEXT", article=None, part=None, band=None, appendix=None, body=True):
    return {"element_id": f"-{seq}", "seq": seq, "kind": kind, "is_body": body, "text": text, "headers": "I bob", "appendix": appendix,
            "article": article, "article_title": "Sarlavha" if article else None, "part": part, "band": band}


def test_article_part_gets_the_id_from_the_spec():
    chunks = list(chunking.chunks_of("-6257288", [
        element(1, "217-modda. Sarlavha", kind="CLAUSE_DEFAULT", article="217-modda"),
        element(2, "Birinchi qism matni.", article="217-modda", part="1-qism"),
        element(3, "Ikkinchi qism matni.", article="217-modda", part="2-qism"),
    ]))
    assert [c["chunk_id"] for c in chunks] == ["lex:6257288#art-217#p1", "lex:6257288#art-217#p2"]
    assert chunks[0]["text"].startswith("217-modda")
    assert (chunks[1]["article"], chunks[1]["part"]) == ("217-modda", "2-qism")


def test_points_of_a_resolution_are_cited_by_number():
    long = "Matn " * 60
    chunks = list(chunking.chunks_of("-5", [element(1, "1. " + long, band="1"), element(2, "2. " + long, band="2")]))
    assert [c["chunk_id"] for c in chunks] == ["lex:5#band-1", "lex:5#band-2"]
    assert chunks[1]["article"] == "2-band"


def test_tiny_points_travel_together():
    chunks = list(chunking.chunks_of("-5", [element(1, "1. Qisqa.", band="1"), element(2, "2. Qisqa.", band="2")]))
    assert len(chunks) == 1


def test_tiny_articles_never_merge():
    chunks = list(chunking.chunks_of("-5", [element(1, "Qisqa.", article="1-modda", part="1-qism"), element(2, "Qisqa.", article="2-modda", part="1-qism")]))
    assert len(chunks) == 2


def test_appendix_is_in_the_id():
    chunks = list(chunking.chunks_of("-5", [element(1, "5-modda matni", article="5-modda", part="1-qism", appendix="2-ilova")]))
    assert chunks[0]["chunk_id"] == "lex:5#ilova-2#art-5#p1"


def test_long_text_is_cut_with_the_same_citation():
    sentences = "Bu uzun jumla matni shu yerda davom etadi. " * 80
    chunks = list(chunking.chunks_of("-5", [element(1, sentences, article="1-modda", part="1-qism")]))
    assert len(chunks) > 1
    assert all(len(c["text"]) <= chunking.MAX_CHARS for c in chunks)
    assert {c["article"] for c in chunks} == {"1-modda"}
    assert chunks[1]["chunk_id"] == "lex:5#art-1#p1#c2"


def test_repeated_numbers_stay_unique():
    chunks = list(chunking.chunks_of("-5", [
        element(1, "Bir", article="1-modda", part="1-qism"), element(2, "Boshqa", article="2-modda", part="1-qism"), element(3, "Yana", article="1-modda", part="1-qism")]))
    assert len({c["chunk_id"] for c in chunks}) == 3


def test_notes_and_footnotes_stay_out():
    chunks = list(chunking.chunks_of("-5", [element(1, "Izoh", body=False), element(2, "PDF", kind="FOOTNOTE"), element(3, "Matn", article="1-modda", part="1-qism")]))
    assert len(chunks) == 1


def test_kind_of_act():
    assert chunking.doc_type("Oʻzbekiston Respublikasining Mehnat kodeksi", "Oʻzbekiston Respublikasi qonuni") == "kodeks"
    assert chunking.doc_type("Mehnat kodeksiga oʻzgartirishlar kiritish toʻgʻrisida", "Oʻzbekiston Respublikasining qonuni, 01.01.2020 yildagi 1-son") == "qonun"
    assert chunking.doc_type("Biror tadbir", "Vazirlar Mahkamasining qarori, 01.01.2020") == "qaror"


def test_constitutional_law_is_a_law():
    assert chunking.doc_type("Raqamli texnologiyalar xalqaro markazi toʻgʻrisida", "Oʻzbekiston Respublikasining Konstitutsiyaviy qonuni, 01.01.2026 yildagi 1-son") == "qonun"


def test_a_chamber_of_parliament_does_not_make_a_law():
    assert chunking.doc_type("Biror masala", "Oliy Majlis Qonunchilik palatasining qarori, 01.01.2020 yildagi 5-son") == "qaror"


def test_constitution():
    assert chunking.doc_type("Oʻzbekiston Respublikasi Konstitutsiyasi", "") == "konstitutsiya"
    assert chunking.doc_type("Konstitutsiyaga oʻzgartirish kiritish toʻgʻrisida", "Oʻzbekiston Respublikasining Qonuni, 01.01.2020 yildagi 1-son") == "qonun"


def test_civil_code_in_two_parts():
    assert chunking.doc_type("Oʻzbekiston Respublikasining Fuqarolik kodeksi (birinchi qism)", "") == "kodeks"


def test_approving_a_code_is_not_the_code():
    assert chunking.doc_type("Oʻzbekiston Respublikasining Mehnat kodeksini tasdiqlash toʻgʻrisida", "Oʻzbekiston Respublikasining Qonuni, 28.10.2022 yildagi 1-son") == "qonun"


def test_rank():
    assert chunking.rank_of("qaror", "Oʻzbekiston Respublikasi Prezidentining qarori, 01.01.2020", "nat") == chunking.RANK["farmon"]
    assert chunking.rank_of("qaror", "Vazirlar Mahkamasining qarori, 01.01.2020", "nat") == chunking.RANK["qaror"]
    assert chunking.rank_of("qaror", "Hokimning qarori, 01.01.2020", "loc") > chunking.RANK["qaror"]

