"""The day an act starts to work. lex.uz marks an adopted act as in force at once, even when its last article says "in three months",
and keeps the act it will replace as in force too. So the status alone cannot say which of the two is the law today.
"""
import calendar
import datetime as dt
import re

from rag.numbers import values
from rag.text import fold

MONTHS = {name: n for n, name in enumerate(("yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"), 1)}
WHOLE_ACT = re.compile(r"^\s*(?:ushbu|mazkur) (?:qonun|kodeks|farmon|qaror|buyruq|nizom|farmoyish)\b")
AFTER_TERM = re.compile(r"(\S+(?: \S+)?) (oy|yil|kun)\w* otgach")
ON_DATE = re.compile(r"(20\d\d)-yil (\d{1,2})-(" + "|".join(MONTHS) + r")")


def add_months(day, months):
    index = day.month - 1 + months
    year, month = day.year + index // 12, index % 12 + 1
    return dt.date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def start_of(adopted, text):
    """The start this text gives for the whole act, as a date, or None. "Ushbu Qonunning 5-moddasi ..." starts one article, not the act.

    A term runs from publication, which the base does not hold, so it is counted from adoption: a few days early at most.
    """
    day = dt.date.fromisoformat(adopted)
    for sentence in re.split(r"[.;\n]+", fold(text)):
        if not WHOLE_ACT.match(sentence) or "kuchga kiradi" not in sentence:
            continue
        if date := ON_DATE.search(sentence):
            return dt.date(int(date[1]), MONTHS[date[3]], int(date[2]))
        if term := AFTER_TERM.search(sentence):
            amount = max(values(term[1]), default=None)
            if amount is None:
                continue
            if term[2] == "kun":
                return day + dt.timedelta(days=int(amount))
            return add_months(day, int(amount) * (12 if term[2] == "yil" else 1))
    return None
