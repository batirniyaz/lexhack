"""Numbers in legal text. Laws spell them out ("yigirma bir kalendar kun"), answers often use digits, and a wrong one must not pass.

Every number becomes its value, so "21", "yigirma bir" and "двадцать один" are one fact. Labels of the citation itself
("217-modda", "1-qism", "[3]") are not claims, they are checked elsewhere.
"""
import re

from rag.text import fold

UZ_UNITS = {"nol": 0, "bir": 1, "ikki": 2, "uch": 3, "tort": 4, "besh": 5, "olti": 6, "yetti": 7, "sakkiz": 8, "toqqiz": 9}
UZ_TENS = {"on": 10, "yigirma": 20, "ottiz": 30, "qirq": 40, "ellik": 50, "oltmish": 60, "yetmish": 70, "sakson": 80, "toqson": 90}
RU_UNITS = {"ноль": 0, "один": 1, "одна": 1, "одно": 1, "одного": 1, "одной": 1, "два": 2, "две": 2, "двух": 2, "три": 3, "трех": 3, "трёх": 3, "четыре": 4,
            "четырех": 4, "четырёх": 4, "пять": 5, "пяти": 5, "шесть": 6, "шести": 6, "семь": 7, "семи": 7, "восемь": 8, "восьми": 8, "девять": 9, "девяти": 9}
RU_TEENS = {"десять": 10, "десяти": 10, "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14, "четырнадцати": 14, "пятнадцать": 15, "пятнадцати": 15,
            "шестнадцать": 16, "шестнадцати": 16, "семнадцать": 17, "восемнадцать": 18, "восемнадцати": 18, "девятнадцать": 19}
RU_TENS = {"двадцать": 20, "двадцати": 20, "тридцать": 30, "тридцати": 30, "сорок": 40, "сорока": 40, "пятьдесят": 50, "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80, "девяносто": 90}
SCALES = {"yuz": 100, "ming": 1000, "million": 10**6, "milliard": 10**9, "сто": 100, "тысяч": 1000, "тысячи": 1000, "тысяча": 1000, "миллион": 10**6, "миллиард": 10**9}
ENDINGS = re.compile(r"(inchi|nchi|lab|tadan|dan|ta|ga|da|ni|ning|si|i)$")
LABEL = re.compile(r"\[\d+\]|\[C\d+\]|\d+[⁰¹²³⁴⁵⁶⁷⁸⁹]*\s*-?\s*(?:modda|qism|band|bob|bo.lim|ilova|moddasi|moddaning)\w*|(?:стать\w*|часть|части|пункт\w*)\s+\d+|\b(?:KODEKS|PQ|PF|ORQ|VMQ|O.RQ)\s*-?\s*\d+", re.I)
DIGITS = re.compile(r"\d[\d\s]*(?:[.,]\d+)?")
WORD = re.compile(r"[a-zа-яё]+")


def _word_value(word):
    """Value of one number word, with its Uzbek endings gone. None for an ordinary word."""
    for table in (UZ_UNITS, UZ_TENS, RU_UNITS, RU_TEENS, RU_TENS, SCALES):
        if word in table:
            return table[word]
    short = ENDINGS.sub("", word)
    if len(short) >= 2:
        for table in (UZ_UNITS, UZ_TENS, SCALES):
            if short in table:
                return table[short]
    return None


def values(text, claims_only=False):
    """Every number the text states, as a set of values. "bir yarim" is 1.5, and so is "полтора".

    With `claims_only`, words that only look like numbers stay out: "bir bola" means "a child", "ikkinchi qism" names a part.
    """
    text = LABEL.sub(" ", text)
    found = set()
    for match in DIGITS.finditer(text):
        raw = re.sub(r"\s", "", match.group()).replace(",", ".")
        try:
            found.add(float(raw))
        except ValueError:
            pass
    words = WORD.findall(fold(text))
    total, current, active = 0, 0, False
    for position, word in enumerate(words):
        if word == "yarim" and position and _word_value(words[position - 1]) is not None:
            found.add(current + total + 0.5)
            continue
        if word in ("полтора", "полторы"):
            found.add(1.5)
            continue
        value = None if claims_only and word.endswith(("inchi", "nchi")) else _word_value(word)
        if value is None:
            if active and not (claims_only and total + current == 1):
                found.add(float(total + current))
            total, current, active = 0, 0, False
        elif value >= 1000:
            total += (current or 1) * value
            current, active = 0, True
        elif value == 100:
            current = (current or 1) * 100
            active = True
        else:
            current += value
            active = True
    if active and not (claims_only and total + current == 1):
        found.add(float(total + current))
    return found


def unsupported(answer, evidence):
    """Numbers the answer states and the cited text does not."""
    return sorted(values(answer, claims_only=True) - values(evidence))
