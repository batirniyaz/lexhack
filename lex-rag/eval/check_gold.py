"""A wrong answer key would make every score wrong: checks that each key phrase really stands in the expected article."""
import json
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def main():
    gold = [json.loads(line) for line in (ROOT / "eval" / "gold.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    answerable = [g for g in gold if g.get("answerable", True)]
    con = duckdb.connect()
    con.execute("SET memory_limit = '2GB'")
    docs = sorted({g["doc"] for g in answerable})
    elements = ROOT / "data" / "parquet" / "elements.parquet"
    con.execute(f"""CREATE TEMP TABLE a AS SELECT doc_id, article, string_agg(text, ' ' ORDER BY seq) body FROM '{elements}'
                    WHERE is_body AND article IS NOT NULL AND appendix IS NULL AND doc_id IN ({','.join(repr(d) for d in docs)}) GROUP BY 1, 2""")
    bodies = {(d, a): b for d, a, b in con.execute("SELECT doc_id, article, body FROM a").fetchall()}
    bad = 0
    for item in answerable:
        texts = [bodies.get((item["doc"], a)) for a in item["articles"]]
        if None in texts:
            print("NO ARTICLE", item["id"], item["doc"], item["articles"])
            bad += 1
        elif not any(item["key"].lower() in t.lower() for t in texts):
            print("KEY NOT FOUND", item["id"], item["key"], "|", texts[0][:160].replace("\n", " "))
            bad += 1
    print(f"{len(gold)} questions, {len(answerable)} answerable, {bad} problems")


if __name__ == "__main__":
    main()
