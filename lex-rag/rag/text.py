"""Words as the search sees them: one spelling for every way of writing an apostrophe, and no case endings.

Uzbek glues endings on, so "ta'tilning" and "ta'tili" must meet at one stem. The stemmer only has to be consistent:
the same word has to land on the same stem in the law and in the question, it does not have to be a dictionary form.
"""
import functools
import re

from lexuz.translit import to_latin

APOSTROPHES = re.compile("[ʻʼ‘’'`´]")
TOKEN = re.compile(r"[a-zа-яё0-9]+(?:\.[0-9]+)*")
SUPERSCRIPTS = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")
UZBEK_ONLY = re.compile("[ўқғҳ]", re.I)

# Longest first. Each pass strips one ending; words carry up to three of them: yil-lar-i-ning.
ENDINGS = ("larning", "laridan", "lariga", "larida", "larini", "lardan", "larga", "larda", "larni", "lari", "lar",
           "ning", "dagi", "gacha", "dan", "dir", "siz", "lik", "ga", "ka", "qa", "da", "ni", "si", "gi", "ki", "im", "ng", "i")
MIN_STEM = 3
RUSSIAN_ENDINGS = ("иями", "ями", "ами", "ого", "его", "ому", "ему", "ыми", "ими", "ией", "ия", "ие", "ий", "ый", "ой", "ая", "яя", "ое",
                   "ее", "ые", "ие", "ых", "их", "ую", "юю", "ов", "ев", "ей", "ом", "ем", "ах", "ях", "ам", "ям", "а", "я", "о", "е", "ы", "и", "у", "ю", "ь")

STOP = {
    "va", "ham", "yoki", "bilan", "uchun", "bu", "shu", "ushbu", "u", "ular", "bir", "biror", "har", "qaysi", "kim", "nima", "nimalar", "qanday",
    "qancha", "necha", "nechta", "qachon", "qayerda", "nega", "mi", "esa", "agar", "lekin", "ammo", "hamda", "kerak", "mumkin", "boʻladi", "boladi",
    "etib", "deb", "kabi", "oʻz", "oz", "bor", "yoʻq", "yoq", "emas", "edi", "ekan", "tomonidan", "boʻyicha", "boyicha", "toʻgʻrisida", "togrisida",
    "и", "в", "во", "на", "по", "с", "со", "к", "ко", "о", "об", "от", "до", "из", "за", "для", "при", "или", "а", "но", "как", "какой", "какая", "какие",
    "каков", "что", "кто", "где", "когда", "сколько", "ли", "же", "это", "этот", "быть", "есть",
}


def fold(text):
    """One spelling: lower case, no apostrophes, superscripts as digits. Uzbek Cyrillic turns Latin, Russian stays as it is."""
    text = text.translate(SUPERSCRIPTS)
    if UZBEK_ONLY.search(text):
        text = to_latin(text)
    return APOSTROPHES.sub("", text.lower())


@functools.lru_cache(maxsize=1000000)
def stem(word):
    if word.isdigit() or not word.isascii():
        return _russian_stem(word) if not word.isascii() else word
    for _ in range(3):
        for ending in ENDINGS:
            if word.endswith(ending) and len(word) - len(ending) >= MIN_STEM:
                word = word[:-len(ending)]
                break
        else:
            break
    return word


def _russian_stem(word):
    for ending in RUSSIAN_ENDINGS:
        if word.endswith(ending) and len(word) - len(ending) >= 3:
            return word[:-len(ending)]
    return word


def tokens(text):
    """Stems of everything worth searching for, in order."""
    words = TOKEN.findall(fold(text))
    return [stem(w) for w in words if w not in STOP and (len(w) > 1 or w.isdigit())]
