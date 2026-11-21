"""Uzbek between scripts, against spellings taken from lex.uz."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lexuz.translit import to_cyrillic, to_latin  # noqa: E402


def test_uzbek_letters():
    assert to_latin("Ўзбекистон Республикасининг Меҳнат кодекси") == "Oʻzbekiston Respublikasining Mehnat kodeksi"
    assert to_latin("ғалла қўшимча") == "gʻalla qoʻshimcha"


def test_e_depends_on_its_place():
    assert to_latin("ер ва мева") == "yer va meva"
    assert to_latin("маъмурий иерархия") == "maʼmuriy iyerarxiya"


def test_ts_depends_on_its_place():
    assert to_latin("цех ва лицей") == "sex va litsey"


def test_capitals():
    assert to_latin("ШАРТНОМА Шартнома") == "SHARTNOMA Shartnoma"


def test_article_number_survives():
    assert to_latin("217-модда. Ҳар йилги") == "217-modda. Har yilgi"


def test_markup_is_left_alone():
    assert to_latin('<div id="divCont" class="ACT_TEXT">Қонун</div>') == '<div id="divCont" class="ACT_TEXT">Qonun</div>'


def test_back_to_cyrillic():
    assert to_cyrillic("Oʻzbekiston Respublikasining Mehnat kodeksi") == "Ўзбекистон Республикасининг Меҳнат кодекси"
    assert to_cyrillic("yigirma bir kalendar kun [1]") == "йигирма бир календар кун [1]"
    assert to_cyrillic("217-modda") == "217-модда"


def test_every_apostrophe_means_the_same():
    assert to_cyrillic("o'quv") == to_cyrillic("oʻquv") == to_cyrillic("o‘quv") == "ўқув"
    assert to_cyrillic("ma'muriy") == to_cyrillic("maʼmuriy") == "маъмурий"


def test_e_at_the_start_is_not_ye():
    assert to_cyrillic("elektron yer") == "электрон ер"
