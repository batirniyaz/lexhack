"""Uzbek between its two scripts. lex.uz writes oʻ and gʻ with U+02BB and the tutuq belgisi with U+02BC, so this does too."""
import re

TO_LATIN = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ё": "yo", "ж": "j", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l",
    "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "x", "ч": "ch", "ш": "sh",
    "щ": "sh", "ы": "i", "э": "e", "ю": "yu", "я": "ya", "ў": "oʻ", "қ": "q", "ғ": "gʻ", "ҳ": "h", "ъ": "ʼ", "ь": "",
}
TO_CYRILLIC = (
    ("sh", "ш"), ("ch", "ч"), ("yo", "ё"), ("yu", "ю"), ("ya", "я"), ("ye", "е"), ("a", "а"), ("b", "б"), ("d", "д"), ("f", "ф"),
    ("g", "г"), ("h", "ҳ"), ("i", "и"), ("j", "ж"), ("k", "к"), ("l", "л"), ("m", "м"), ("n", "н"), ("o", "о"), ("p", "п"),
    ("q", "қ"), ("r", "р"), ("s", "с"), ("t", "т"), ("u", "у"), ("v", "в"), ("x", "х"), ("y", "й"), ("z", "з"),
)
VOWELS = "аеёиоуўэюяы"
CYRILLIC_WORD = re.compile("[а-яёўқғҳА-ЯЁЎҚҒҲ]+")
APOSTROPHE = "ʻʼ‘’'`´"
LATIN_WORD = re.compile(f"[A-Za-z][A-Za-z{APOSTROPHE}]*")


def _word_to_latin(match):
    word = match.group()
    low = word.lower()
    capitals = len(word) > 1 and word.isupper()
    out = []
    for i, letter in enumerate(low):
        before = low[i - 1] if i else ""
        if letter == "е":
            latin = "ye" if not before or before in VOWELS + "ъь" else "e"
        elif letter == "ц":
            latin = "ts" if before and before in VOWELS else "s"
        else:
            latin = TO_LATIN[letter]
        if capitals:
            latin = latin.upper()
        elif word[i].isupper():
            latin = latin[:1].upper() + latin[1:]
        out.append(latin)
    return "".join(out)


def to_latin(text):
    """Only Cyrillic letters change, so a whole HTML page can go through it with its markup intact."""
    return CYRILLIC_WORD.sub(_word_to_latin, text)


def _word_to_cyrillic(match):
    word = match.group()
    low = word.lower()
    capitals = len(word) > 1 and word.replace("ʻ", "").replace("ʼ", "").isupper()
    out, i = [], 0
    while i < len(low):
        letter = low[i]
        turned = i + 1 < len(low) and low[i + 1] in APOSTROPHE
        if letter in "og" and turned:
            cyrillic, step = ("ў" if letter == "o" else "ғ"), 2
        elif letter in APOSTROPHE:
            cyrillic, step = "ъ", 1
        elif letter == "e":
            cyrillic, step = ("э" if i == 0 or low[i - 1] in "aeiou" else "е"), 1
        else:
            cyrillic, step = next(((c, len(lat)) for lat, c in TO_CYRILLIC if low.startswith(lat, i)), (letter, 1))
        out.append(cyrillic.upper() if capitals or word[i].isupper() else cyrillic)
        i += step
    return "".join(out)


def to_cyrillic(text):
    return LATIN_WORD.sub(_word_to_cyrillic, text)
