"""The model names an act from memory, so a name only has to come close to a title."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag import pipeline as p  # noqa: E402
from rag.search import GENERIC, MIN_FIT, fit  # noqa: E402
from rag.text import tokens  # noqa: E402


def stems(name):
    return [t for t in dict.fromkeys(tokens(name)) if t not in GENERIC]


def test_the_word_law_in_a_name_does_not_hide_the_act():
    assert fit(stems("Mediatsiya toʻgʻrisida qonun"), "Mediatsiya toʻgʻrisida") == 1


def test_stems_of_different_length_still_meet():
    assert fit(stems("Bandlik toʻgʻrisida qonun"), "Aholi bandligi toʻgʻrisida") >= MIN_FIT


def test_the_act_itself_fits_better_than_a_long_title_that_mentions_it():
    name = stems("Mediatsiya toʻgʻrisida qonun")
    assert fit(name, "Mediatsiya toʻgʻrisida") > fit(name, "Oʻzbekiston Respublikasining ayrim qonun hujjatlariga nizolarni hal etishning muqobil usullari va mediatsiya tartibini joriy etish munosabati bilan")


def test_a_title_with_no_word_of_the_name_does_not_fit():
    assert fit(stems("Kosmik kema qonuni"), "Oila kodeksi") < MIN_FIT


def test_a_number_from_the_question_is_the_askers_fact_and_not_a_claim():
    reply = {"verdict": "answer", "answer": "Ikki yil oldin sotib olingan uy sotilsa, daromad soliqqa tortiladi [C1]."}
    sources = {"C1": {"text": "Uy-joy sotishdan olingan daromad soliqqa tortiladi.", "article_title": None}}
    assert p.check(reply, sources)
    assert p.check(reply, sources, "Kvartiramni ikki yil oldin sotib olganman") == []


def test_a_number_nobody_said_is_still_stopped():
    reply = {"verdict": "answer", "answer": "Muddat yetti yil [C1]."}
    sources = {"C1": {"text": "Muddat uch yil.", "article_title": None}}
    assert p.check(reply, sources, "Kvartiramni ikki yil oldin sotib olganman")
