"""The number check is the last guard against a wrong sum, so it has to read numbers the way the law writes them."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag import language  # noqa: E402
from rag.numbers import unsupported, values  # noqa: E402


def test_words_and_digits_are_one_fact():
    assert 21.0 in values("yigirma bir kalendar kunni tashkil etadi")
    assert 21.0 in values("21 kalendar kun")
    assert 21.0 in values("двадцать один день")


def test_uzbek_with_every_apostrophe():
    assert 14.0 in values("oʻn toʻrt kalendar kun")
    assert 14.0 in values("o'n to'rt kun")


def test_endings():
    assert 3.0 in values("uch oydan oshmasligi kerak")
    assert 16.0 in values("oʻn olti yoshdan")
    assert 40.0 in values("haftasiga qirq soatdan")


def test_half():
    assert 1.5 in values("bir yarim baravar miqdorida")
    assert 1.5 in values("1,5 koeffitsiyent")
    assert 1.5 in values("полтора раза")


def test_thousands():
    assert 1500.0 in values("bir ming besh yuz")
    assert 1000000.0 in values("1 000 000 soʻm")


def test_labels_are_not_claims():
    assert values("217-modda 1-qismga koʻra [3]") == set()
    assert values("Статья 150") == set()


def test_answer_in_digits_passes_against_words():
    assert unsupported("Eng kam taʼtil 21 kalendar kun [1].", "davomiyligi yigirma bir kalendar kunni tashkil etadi") == []


def test_russian_answer_passes_against_uzbek_law():
    assert unsupported("Срок составляет три года [1].", "Umumiy daʼvo muddati — uch yil.") == []


def test_invented_number_is_caught():
    assert unsupported("Eng kam taʼtil 24 kalendar kun [1].", "yigirma bir kalendar kunni tashkil etadi") == [24.0]


def test_words_that_only_look_like_numbers_are_not_claims():
    evidence = "aliment toʻrtdan bir qismi miqdorida undiriladi"
    assert unsupported("Bir bola uchun toʻrtdan bir qismi [1].", evidence) == []
    assert unsupported("Ikkinchi qismiga koʻra aliment toʻrtdan bir [1].", evidence) == []


def test_digit_one_is_still_checked():
    assert unsupported("Muddat 1 yil [1].", "Muddat uch yil.") == [1.0]
    assert unsupported("Muddat 1 yil [1].", "Muddat bir yil.") == []


def test_ordinary_text_has_no_numbers():
    assert values("Xodim ish beruvchini yozma shaklda ogohlantiradi") == set()


def test_languages():
    assert language.detect("Yillik ta'til necha kun?") == "uz-Latn"
    assert language.detect("Ҳар йилги меҳнат таътили қанча?") == "uz-Cyrl"
    assert language.detect("Умумий даъво муддати канча?") == "uz-Cyrl"
    assert language.detect("Какой срок исковой давности?") == "ru"
    assert language.detect("Какая ставка НДС установлена?") == "ru"
