"""The search must see one word where the law and the question spell it differently."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag.text import fold, stem, tokens  # noqa: E402


def test_every_apostrophe_is_one_spelling():
    assert fold("ta'til") == fold("taʼtil") == fold("ta’til") == "tatil"
    assert fold("oʻzbek") == fold("o'zbek") == fold("o‘zbek") == "ozbek"


def test_uzbek_cyrillic_meets_latin():
    assert tokens("Меҳнат таътили") == tokens("Mehnat ta'tili")


def test_endings_fall_off():
    assert stem("tatilning") == stem("tatili") == stem("tatil")
    assert stem("soliqlarning") == stem("soliqlar") == stem("soliq")
    assert stem("kunni") == stem("kun")


def test_yillik_meets_har_yilgi():
    assert stem("yillik") == stem("yilgi") == "yil"


def test_short_words_stay_whole():
    assert stem("sud") == "sud"
    assert stem("ish") == "ish"


def test_stop_words_are_dropped():
    assert tokens("mehnat va ta'til qancha") == ["mehnat", "tatil"]


def test_numbers_stay():
    assert tokens("217-modda 2.1") == ["217", stem("modda"), "2.1"]
    assert tokens("13¹-modda") == ["131", stem("modda")]


def test_russian_endings():
    assert tokens("срок исковой давности") == tokens("сроки исковая давность")
