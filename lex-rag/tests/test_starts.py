"""Acts that are adopted now and start later: what counts as such a sentence, and what the search does with them."""
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from rag.search import Search, record, weight, NAMES  # noqa: E402
from rag.starts import add_months, start_of  # noqa: E402


def test_term_in_months():
    text = "43-modda. Ushbu Qonunning kuchga kirishi\nUshbu Qonun rasmiy eʼlon qilingan kundan eʼtiboran uch oy oʻtgach kuchga kiradi."
    assert start_of("2026-08-07", text) == dt.date(2026, 11, 7)


def test_term_in_words_with_two_parts():
    assert start_of("2026-01-31", "Ushbu Qonun oʻn ikki oy oʻtgach kuchga kiradi.") == dt.date(2027, 1, 31)


def test_term_in_years_and_days():
    assert start_of("2026-02-01", "Ushbu Kodeks bir yil oʻtgach kuchga kiradi.") == dt.date(2027, 2, 1)
    assert start_of("2026-02-01", "Mazkur qaror oʻn kun oʻtgach kuchga kiradi.") == dt.date(2026, 2, 11)


def test_named_date():
    assert start_of("2026-09-04", "5. Mazkur buyruq 2027-yil 1-yanvardan kuchga kiradi.") == dt.date(2027, 1, 1)


def test_starting_at_once_is_not_a_later_start():
    assert start_of("2026-09-04", "Ushbu Qonun rasmiy eʼlon qilingan kundan eʼtiboran kuchga kiradi.") is None


def test_one_article_does_not_move_the_whole_act():
    assert start_of("2026-09-04", "Ushbu Qonunning 5-moddasi 2027-yil 1-yanvardan kuchga kiradi.") is None


def test_another_act_in_the_sentence_is_not_this_one():
    assert start_of("2026-09-04", "Vazirlar Mahkamasining qarori olti oy oʻtgach kuchga kiradi.") is None


def test_month_end_stays_in_its_month():
    assert add_months(dt.date(2026, 11, 30), 3) == dt.date(2027, 2, 28)


def row(doc_id="-1", adopted="2026-08-07"):
    return {"doc_id": doc_id, "adopted": adopted}


def test_an_act_waiting_for_its_day_is_out_until_then():
    search = Search(path=Path("no-such-file.sqlite"))
    search.starts = {"-1": "2026-11-07"}
    assert not search.started(row(), "2026-11-06")
    assert search.started(row(), "2026-11-07")


def test_without_a_later_start_the_adoption_date_decides():
    search = Search(path=Path("no-such-file.sqlite"))
    assert search.started(row(), "2026-11-06")
    assert not search.started(row(adopted="2026-12-01"), "2026-11-06")
    assert search.started(row(adopted=None), "2026-11-06")


def fields(**values):
    base = dict.fromkeys(NAMES)
    base.update(chunk_id="lex:4672431#art-3#p1", url="https://lex.uz/docs/4672427", number="4672431", rank=2, section="nat", amending=0, adopted="2020-01-01")
    base.update(values)
    return tuple(base[name] for name in NAMES)


def test_the_public_number_is_the_one_in_the_link():
    found = record(fields())
    assert found["number"] == "4672427" and found["chunk_id"] == "lex:4672427#art-3#p1"


def test_the_minus_of_a_latin_page_is_not_part_of_the_number():
    found = record(fields(url="https://lex.uz/docs/-6257288", chunk_id="lex:6257288#art-217#p1", number="6257288"))
    assert found["number"] == "6257288" and found["chunk_id"] == "lex:6257288#art-217#p1"


def test_a_newer_act_wins_a_close_match_but_not_a_stronger_act():
    new, old = record(fields(adopted="2026-06-23")), record(fields(adopted="2024-08-12"))
    assert weight(new) > weight(old)
    assert weight(record(fields(rank=1, adopted="1995-12-21"))) > weight(record(fields(rank=3, adopted="2026-06-23")))
