"""What the parsed sample looks like: losses, gaps, odd markup, and the size of the whole base.

Run after scripts/build_parquet.py.
"""
import re
import statistics
import sys
from pathlib import Path

import duckdb
from selectolax.lexbor import LexborHTMLParser

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from lexuz import parse, store  # noqa: E402

P = store.DATA / "parquet"
ALL_LATIN = 55282
INTERFACE = re.compile(r"Hujjatga taklif yuborish|Audioni tinglash|Hujjat elementidan havola olish|LexUZ sharhi")


def table(con, title, sql):
    print(f"\n== {title}")
    cur = con.execute(sql)
    print(" | ".join(d[0] for d in cur.description))
    for row in cur.fetchall():
        print(" | ".join("" if v is None else str(v)[:70] for v in row))


def page_text_size(html):
    """Every visible letter inside the document body, without the hover menu and the classifier lines."""
    start = html.rfind("<div", 0, html.find('id="divCont"'))
    tree = LexborHTMLParser(parse._prepare(html[max(start, 0):]))
    root = tree.css_first("#divCont")
    if root is None:
        return 0
    for selector in (".lx_elem2", ".INDEXES_ON_REF", ".COMMENTLEXUZ", "script", "style"):
        for node in root.css(selector):
            node.decompose()
    return len(re.sub(r"\s", "", INTERFACE.sub("", root.text(separator=""))))


def completeness(con):
    """Compares the page with what was kept. A low share means text sits outside the markup the parser knows."""
    rows = con.execute(f"""SELECT a.doc_id, a.form, sum(length(regexp_replace(e.text, '\\s', '', 'g')))
                           FROM '{P}/acts.parquet' a JOIN '{P}/elements.parquet' e USING (doc_id) GROUP BY 1, 2""").fetchall()
    shares = []
    for doc_id, form, kept in rows:
        page = store.raw_path("docs", doc_id)
        size = page_text_size(store.load_raw("docs", doc_id)) if page.exists() else 0
        if size:
            shares.append((round(kept / size, 3), doc_id, form, size))
    shares.sort()
    values = [s[0] for s in shares]
    print("\n== kept text as a share of the page text")
    print("documents", len(values), "median", statistics.median(values), "below 0.98:", sum(v < .98 for v in values),
          "above 1.02:", sum(v > 1.02 for v in values))
    print("worst:", shares[:8])
    print("highest:", shares[-3:])


def main():
    con = duckdb.connect()
    con.execute("SET memory_limit = '3GB'")
    acts, els = f"'{P}/acts.parquet'", f"'{P}/elements.parquet'"
    table(con, "documents", f"""SELECT count(*) docs, sum(pdf_only::int) pdf_only, sum(ru_only::int) ru_only, sum((text_chars = 0)::int) no_body,
        sum((text_chars = 0 AND NOT pdf_only AND NOT ru_only)::int) empty_unexplained, sum((text_chars BETWEEN 1 AND 300)::int) under_300, sum((script = 'cyrl')::int) cyrillic, sum((status IS NULL)::int) no_status,
        sum((form IS NULL)::int) no_form, sum((ru_id IS NULL)::int) no_ru_id, sum((other_uz_id IS NULL)::int) no_other_uz,
        sum((len(okoz) > 0)::int) with_okoz, sum((edition IS NOT NULL)::int) with_edition FROM {acts}""")
    table(con, "list icon against the card status", f"SELECT list_state, status, count(*) n FROM {acts} GROUP BY 1, 2 ORDER BY 1, 3 DESC")
    table(con, "by section", f"""SELECT section, count(*) docs, round(avg(text_chars)) mean_chars, median(text_chars) median_chars,
        round(avg(raw_bytes)) mean_raw, round(avg(len(editions)), 1) editions FROM {acts} GROUP BY 1 ORDER BY 2 DESC""")
    table(con, "paragraph kinds", f"""SELECT kind, any_value(is_body) body, any_value(is_note) note, count(*) n,
        sum(length(text)) chars, any_value(substr(text, 1, 50)) example FROM {els} GROUP BY 1 ORDER BY 4 DESC""")
    table(con, "where body text sits, by form", f"""SELECT a.form, count(DISTINCT a.doc_id) docs, count(*) paragraphs,
        round(100.0 * count(e.article) / count(*), 1) in_article, round(100.0 * count(e.band) / count(*), 1) in_band,
        round(100.0 * sum((e.article IS NULL AND e.band IS NULL)::int) / count(*), 1) neither
        FROM {els} e JOIN {acts} a USING (doc_id) WHERE e.is_body GROUP BY 1 ORDER BY 3 DESC LIMIT 14""")
    table(con, "article numbers in codes and laws: found against highest", f"""WITH n AS (
          SELECT doc_id, appendix, article, count(*) c, try_cast(regexp_extract(article, '^\\d+') AS int) num
          FROM {els} WHERE kind = 'CLAUSE_DEFAULT' AND article IS NOT NULL GROUP BY 1, 2, 3)
        SELECT a.form, substr(a.title, 1, 48) title, count(*) articles, max(num) highest, sum((c > 1)::int) repeated
        FROM n JOIN {acts} a USING (doc_id) WHERE a.form IN ('Кодекс', 'Закон') AND n.appendix IS NULL
        GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 16""")
    table(con, "article-like paragraphs the parser did not treat as articles", f"""SELECT kind, count(*) n, any_value(substr(text, 1, 60)) example
        FROM {els} WHERE article IS NULL AND regexp_matches(text, '^\\s*\\d+[-–]?\\s*modda\\b', 'i') GROUP BY 1""")
    table(con, "warnings", f"SELECT substr(warnings, 1, 70) warning, count(*) n FROM {acts} WHERE warnings IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 8")
    completeness(con)

    mean = con.execute(f"SELECT avg(raw_bytes), avg(text_chars), sum(text_chars) FROM {acts} WHERE NOT pdf_only").fetchone()
    weighted = con.execute(f"""WITH s AS (SELECT section, avg(text_chars) m, avg(raw_bytes) r FROM {acts}
                                          WHERE lower(title) NOT LIKE '%kodeksi' GROUP BY 1)
        SELECT sum(m * w), sum(r * w) FROM s JOIN (VALUES ('nat',28499),('loc',13085),('oliy',10680),('int',1662),('tech',792),('court',564))
        t(section, w) USING (section)""").fetchone()
    print("\n== whole base, from section means without the codes (they were all taken on purpose)")
    print("clean text GB:", round(weighted[0] / 1e9, 2), "| raw HTML GB:", round(weighted[1] / 1e9, 1), "| documents:", ALL_LATIN)
    print("sample means: raw bytes", round(mean[0]), "text chars", round(mean[1]))
    for name in ("acts", "elements", "links"):
        print(name, "parquet MB:", round((P / f"{name}.parquet").stat().st_size / 1e6, 2))


if __name__ == "__main__":
    main()
