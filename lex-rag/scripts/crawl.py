"""Crawler commands.

  python scripts/crawl.py list                       find every Latin document
  python scripts/crawl.py pick --n 400               mark a mixed sample for the pilot
  python scripts/crawl.py fetch --pilot --limit 120  download pilot documents with their cards
  python scripts/crawl.py fetch --rate 4 --no-cards  download everything still pending
  python scripts/crawl.py cards --rate 4             cards of the acts no longer in force
  python scripts/crawl.py all --rate 4               documents, then cards, left alone for hours
  python scripts/crawl.py ru --rate 4                Russian pages of acts that have no Uzbek text
  python scripts/crawl.py report                     what has been found and fetched so far

Every command can be stopped and run again: it continues where it ended.
"""
import argparse
import asyncio
import ctypes
import datetime as dt
import math
import random
import statistics
import sys
from pathlib import Path

import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")
from lexuz import listing, store  # noqa: E402
from lexuz.client import Blocked, Client, PageFailed, SiteDown  # noqa: E402

PAUSE = 1800     # seconds to leave the site alone after it stopped answering
PATIENCE = 8     # such pauses before the unattended run gives up
TEXT_BLOCK = b'id="divCont"'   # a new act's Latin page can be an empty 200 shell until its Latin text is posted


async def run_list(args):
    con = store.connect()
    client = Client(args.rate, store.logger(con))
    try:
        await listing.plan(client, con, args.sections.split(","))
        await listing.walk_all(client, con)
    except SiteDown as e:
        print("STOPPED:", e)
    finally:
        con.commit()
        await client.close()
    report(args)


def pick(args):
    """Every code and constitution, because they are the longest and matter most, plus a random share of each section."""
    con = store.connect()
    con.execute("UPDATE docs SET pilot = 0")
    key = con.execute("""SELECT doc_id FROM docs WHERE state = 'y'
                         AND (lower(title) LIKE '%kodeksi' OR lower(title) LIKE '%konstitutsiyasi')""").fetchall()
    chosen = {r[0] for r in key}
    rng = random.Random(args.seed)
    total = con.execute("SELECT count(*) FROM docs").fetchone()[0]
    left = args.n - len(chosen)
    for section, size in con.execute("SELECT section, count(*) FROM docs GROUP BY 1").fetchall():
        ids = sorted(r[0] for r in con.execute("SELECT doc_id FROM docs WHERE section = ?", (section,)))
        chosen.update(rng.sample(ids, min(len(ids), max(5, round(left * size / total)))))
    con.executemany("UPDATE docs SET pilot = 1 WHERE doc_id = ?", [(d,) for d in chosen])
    con.commit()
    print("picked", len(chosen), "of which codes and constitutions", len(key))


async def run_pool(client, con, todo, job, rate):
    """Works through the list until it ends or something stops it, and returns what did, if anything.

    Whatever was finished stays finished. A skipped item stays pending, so the next run tries it again.
    """
    queue = iter(todo)
    stop = asyncio.Event()
    done = skipped = 0
    stopped_by = None

    async def worker():
        nonlocal done, skipped, stopped_by
        for item in queue:
            if stop.is_set():
                return
            try:
                await job(item)
                done += 1
                if done % 25 == 0:
                    con.commit()
            except PageFailed as e:
                print("SKIPPED:", e, flush=True)
                skipped += 1
                continue
            except Exception as e:   # a full disk stops the run the same way a dead site does
                print("STOPPED:", repr(e), flush=True)
                stopped_by = e
                stop.set()
                return
            if done % 500 == 0:
                print(f"{dt.datetime.now():%H:%M:%S} {done}/{len(todo)} pace {client.pace.rate:.2f}/s "
                      f"slowdowns {client.pace.slowdowns} skipped {skipped}", flush=True)

    try:
        await asyncio.gather(*(worker() for _ in range(math.ceil(rate) + 1)))
    finally:
        con.commit()
        await client.close()
    print(f"done {done} of {len(todo)}, skipped {skipped}, pace at the end {client.pace.rate:.2f}/s, "
          f"slowdowns {client.pace.slowdowns}", flush=True)
    return stopped_by


async def fetch_card(client, number):
    card = await client.fetch("card", f"/uz/actinfo/card1/{number}")
    if card is None:
        return "missing"
    store.save_raw("cards", number, card.content)
    return "ok"


async def run_fetch(args):
    con = store.connect()
    # "missing" goes round again: the site once answered 404 to every request for 38 seconds, real pages included
    where = "doc_status IN ('pending', 'missing')" + (" AND pilot = 1" if args.pilot else "")
    todo = [r[0] for r in con.execute(f"SELECT doc_id FROM docs WHERE {where}")]
    random.Random(args.seed).shuffle(todo)   # keeps every stretch of the run a fair mix of light and heavy pages
    todo = todo[:args.limit] if args.limit else todo
    client = Client(args.rate, store.logger(con))

    async def job(doc_id):
        page = await client.fetch("doc", f"/uz/docs/{doc_id}")
        state = "missing"
        if page is not None and TEXT_BLOCK in page.content:
            store.save_raw("docs", doc_id, page.content)
            state = "ok"
        card_state = await fetch_card(client, doc_id.lstrip("-")) if args.cards else None
        con.execute("UPDATE docs SET doc_status = ?, card_status = coalesce(?, card_status), fetched_at = ? WHERE doc_id = ?",
                    (state, card_state, dt.datetime.now().isoformat(timespec="seconds"), doc_id))

    return await run_pool(client, con, todo, job, args.rate)


async def run_cards(args):
    """Cards only for acts that are no longer in force: the list icon gives the status, the card adds the end date."""
    con = store.connect()
    todo = [r[0] for r in con.execute("SELECT doc_id FROM docs WHERE state IN ('r', 'n') AND card_status != 'ok'")]
    todo = todo[:args.limit] if args.limit else todo
    client = Client(args.rate, store.logger(con))

    async def job(doc_id):
        con.execute("UPDATE docs SET card_status = ? WHERE doc_id = ?", (await fetch_card(client, doc_id.lstrip("-")), doc_id))

    return await run_pool(client, con, todo, job, args.rate)


async def run_russian(args):
    """Some acts exist only in Russian: the Uzbek page says so and the text is on the Russian one. Needs the parquet built first."""
    keep_awake()
    rows = pq.read_table(store.DATA / "parquet" / "acts.parquet", columns=["doc_id", "ru_id", "ru_only"]).to_pylist()
    todo = [(r["doc_id"], r["ru_id"]) for r in rows if r["ru_only"] and r["ru_id"] and not store.raw_path("ru", r["doc_id"]).exists()]
    con = store.connect()
    client = Client(args.rate, store.logger(con))

    async def job(item):
        doc_id, ru_id = item
        page = await client.fetch("ru", f"/uz/docs/{ru_id}")
        if page is not None and TEXT_BLOCK in page.content:
            store.save_raw("ru", doc_id, page.content)

    return await run_pool(client, con, todo, job, args.rate)


def keep_awake():
    """Asks Windows not to sleep on idle. Seen on this laptop: on battery it still sleeps about 5 minutes after the screen goes off."""
    if sys.platform == "win32":
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED


async def run_all(args):
    """Documents, then cards, with nobody watching: a silent site gets a long pause and another try, a refusal ends the run."""
    keep_awake()
    for job in (run_fetch, run_cards) * 2:   # the second round is short: only what was skipped or answered 404
        for _ in range(PATIENCE + 1):
            stopped_by = await job(args)
            if stopped_by is None:
                break
            if isinstance(stopped_by, Blocked):
                print("ENDED: the site is refusing us, not trying again", flush=True)
                return
            print(f"{dt.datetime.now():%H:%M:%S} pausing for {PAUSE // 60} minutes", flush=True)
            await asyncio.sleep(PAUSE)
        else:
            print("ENDED: out of patience, run it again later", flush=True)
            return
    print("FINISHED", flush=True)
    report(args)


def percentile(values, share):
    return sorted(values)[min(len(values) - 1, int(len(values) * share))]


def report(_):
    con = store.connect()
    print("section   expected    found   lists  unfinished  short")
    for row in con.execute("""SELECT section, sum(expected), sum(found), count(*), sum(done = 0), sum(found < expected)
                              FROM lists GROUP BY 1 ORDER BY 2 DESC"""):
        print("{:8}{:>10}{:>9}{:>8}{:>12}{:>7}".format(*row))
    print("documents:", con.execute("SELECT count(*), sum(seen > 1) FROM docs").fetchone(), "(total, seen in more than one list)")
    print("list icons:", con.execute("SELECT state, count(*) FROM docs GROUP BY 1").fetchall())
    print("fetched:", con.execute("SELECT doc_status, card_status, count(*) FROM docs GROUP BY 1, 2").fetchall())
    print("kind  pace   requests  not200  median  p95    per_second")
    groups = {}
    rows = con.execute("SELECT ts, kind, status, seconds, rate FROM requests ORDER BY ts").fetchall()
    for ts, kind, status, seconds, rate in rows:
        groups.setdefault((kind, round(rate, 1)), []).append((ts, status, seconds))
    for (kind, rate), items in sorted(groups.items()):
        times = [i[2] for i in items]
        span = max(items[-1][0] - items[0][0], 1)
        print(f"{kind:5} {rate:<6} {len(items):<9} {sum(i[1] != 200 for i in items):<7} "
              f"{statistics.median(times):<7.2f} {percentile(times, .95):<6.2f} {len(items) / span:.2f}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("list")
    p.add_argument("--rate", type=float, default=3)
    p.add_argument("--sections", default=",".join(listing.SECTIONS))
    p = sub.add_parser("pick")
    p.add_argument("--n", type=int, default=400)
    p.add_argument("--seed", type=int, default=7)
    p = sub.add_parser("fetch")
    p.add_argument("--rate", type=float, default=2)
    p.add_argument("--limit", type=int)
    p.add_argument("--pilot", action="store_true")
    p.add_argument("--no-cards", dest="cards", action="store_false")
    p.add_argument("--seed", type=int, default=7)
    p = sub.add_parser("cards")
    p.add_argument("--rate", type=float, default=2)
    p.add_argument("--limit", type=int)
    p = sub.add_parser("ru")
    p.add_argument("--rate", type=float, default=4)
    p = sub.add_parser("all")
    p.add_argument("--rate", type=float, default=4)
    p.set_defaults(limit=None, pilot=False, cards=False, seed=7)
    sub.add_parser("report")
    args = ap.parse_args()
    if args.command == "list":
        asyncio.run(run_list(args))
    elif args.command == "pick":
        pick(args)
    elif args.command == "fetch":
        asyncio.run(run_fetch(args))
    elif args.command == "cards":
        asyncio.run(run_cards(args))
    elif args.command == "all":
        asyncio.run(run_all(args))
    elif args.command == "ru":
        asyncio.run(run_russian(args))
    else:
        report(args)


if __name__ == "__main__":
    main()
