"""Which of the three languages a question is in, when the client did not say."""
import re

UZBEK_LETTERS = re.compile("[ўқғҳ]")
UZBEK_WORDS = re.compile(r"\b(неча|нечта|қанча|канча|йил\w*|бўйича|ёшда\w*|муддат\w*|қонун\w*|кодекс\w+|ҳақ\w*|учун|керак|мумкин|нима\w*|қандай|кандай)\b")


def detect(question):
    """"uz-Latn", "uz-Cyrl" or "ru". An act's name in capitals says nothing about the sentence around it."""
    low = re.sub(r"\b[А-ЯЁЎҚҒҲ]{2,}\b", " ", question).lower()
    cyrillic = len(re.findall("[а-яёўқғҳ]", low))
    if not cyrillic:
        return "uz-Latn"
    if UZBEK_LETTERS.search(low) or UZBEK_WORDS.search(low):
        return "uz-Cyrl"
    latin = len(re.findall("[a-z]", low))
    return "uz-Latn" if latin > cyrillic else "ru"
