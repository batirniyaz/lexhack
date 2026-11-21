"""Walks the search lists. Paging works only through ASP.NET postbacks: `?page=` is ignored by the site."""
import asyncio
import re

from selectolax.lexbor import LexborHTMLParser as HTMLParser

SECTIONS = ("nat", "loc", "oliy", "int", "tech", "court")   # their totals add up to the whole Latin base
LANG_LATIN = 4
NEXT_PAGE = "ucFoundActsControl$LinkButton1"
ANY_YEAR = 0


def list_url(section, year=ANY_YEAR):
    return f"/uz/search/{section}?lang={LANG_LATIN}" + (f"&fyear={year}" if year else "")


def total_of(html):
    found = re.search(r"([\d\s]+?)\s*hujjat topildi", re.sub(r"<[^>]+>", " ", html))
    return int(re.sub(r"\s", "", found.group(1))) if found else 0


def years_of(html):
    """{year: documents} from the filter on the first page."""
    return {int(y): int(n) for y, n in re.findall(r'value="&(?:amp;)?fyear=(\d+)"[^>]*>\s*\d+\s*\((\d+)\)', html)}


def rows_of(html):
    rows = []
    for link in HTMLParser(html).css("a.lx_link"):
        found = re.fullmatch(r"/uz/docs/(-?\d+)", link.attributes.get("href") or "")
        if not found:
            continue
        cell = link.parent.parent
        icon = cell.css_first(".lx_act_state i")
        badge = cell.css_first(".dd-table__main-extra .badge")
        state = re.search(r"status_code_(\w+)", icon.attributes.get("class") or "") if icon else None
        rows.append({"doc_id": found.group(1), "title": link.text(strip=True),
                     "meta": badge.text(strip=True) if badge else None, "state": state.group(1) if state else None})
    return rows


def form_fields(html):
    fields = {}
    for field in HTMLParser(html).css("input[type=hidden]"):
        name = field.attributes.get("name")
        if name:
            fields[name] = field.attributes.get("value") or ""
    return fields


def has_next(html):
    return f"__doPostBack(&#39;{NEXT_PAGE}&#39;" in html


async def walk(client, con, section, year):
    """All pages of one list. Stops on the last page or when a page brings nothing new."""
    url = list_url(section, year)
    reply = await client.fetch("list", url)
    html, seen, pages = reply.text, set(), 0
    while True:
        rows = rows_of(html)
        fresh = [r for r in rows if r["doc_id"] not in seen]
        seen.update(r["doc_id"] for r in fresh)
        pages += 1
        con.executemany(
            """INSERT INTO docs(doc_id, section, year, title, meta, state) VALUES (?,?,?,?,?,?)
               ON CONFLICT(doc_id) DO UPDATE SET seen = seen + 1""",
            [(r["doc_id"], section, year, r["title"], r["meta"], r["state"]) for r in fresh])
        con.execute("UPDATE lists SET found = ?, pages = ? WHERE section = ? AND year = ?", (len(seen), pages, section, year))
        con.commit()
        if not fresh or not has_next(html):
            break
        fields = {**form_fields(html), "__EVENTTARGET": NEXT_PAGE, "__EVENTARGUMENT": ""}
        html = (await client.fetch("list", url, data=fields)).text
    con.execute("UPDATE lists SET done = 1 WHERE section = ? AND year = ?", (section, year))
    con.commit()
    return len(seen)


async def plan(client, con, sections):
    """Splits every section by year: a short list that fails costs little to repeat."""
    for section in sections:
        html = (await client.fetch("list", list_url(section))).text
        total, years = total_of(html), years_of(html)
        if not years or sum(years.values()) != total:
            print(f"{section}: years add up to {sum(years.values())} of {total}, walking the whole list instead")
            years = {ANY_YEAR: total}
        for year, expected in years.items():
            con.execute("INSERT OR IGNORE INTO lists(section, year, expected) VALUES (?,?,?)", (section, year, expected))
        con.commit()
        print(f"{section}: {total} documents in {len(years)} lists", flush=True)


async def walk_all(client, con, parallel=4):
    todo = con.execute("SELECT section, year FROM lists WHERE done = 0 ORDER BY expected DESC").fetchall()
    gate = asyncio.Semaphore(parallel)

    async def one(section, year):
        async with gate:
            await walk(client, con, section, year)

    await asyncio.gather(*(one(s, y) for s, y in todo))
