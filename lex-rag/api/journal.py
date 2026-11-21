"""Every answer the service gives: where its time went, what it rested on and what it cost. The page /logs reads this.

The page is open, as the owner asked, so no visitor address is kept here.
"""
import json
import sqlite3
import statistics
import threading

from lexuz import store

PATH = store.DATA / "logs.sqlite"
PRICES = {"claude-haiku-5-5": (0.10, 0.50)}   # USD per million tokens, for prompts of 100K tokens or fewer; ours stay far below that
SCHEMA = """CREATE TABLE IF NOT EXISTS runs (
  id INTEGER PRIMARY KEY, started_at TEXT, source TEXT, run_id TEXT, item_id TEXT, question TEXT, language TEXT, status TEXT, answer TEXT,
  citations TEXT, model TEXT, cached INTEGER, total_ms INTEGER, read_ms INTEGER, search_ms INTEGER, answer_ms INTEGER, correct_ms INTEGER,
  tokens_in INTEGER, tokens_out INTEGER, cost_usd REAL, plan TEXT, found INTEGER, reason TEXT, error TEXT,
  ok INTEGER, why TEXT, expected TEXT, category TEXT)"""
LIST = ("id, started_at, source, run_id, item_id, question, status, answer, model, cached, total_ms, read_ms, search_ms, answer_ms, correct_ms, "
        "cost_usd, ok, why, expected, category")
FILTERS = {"source": "source = ?", "run_id": "run_id = ?"}
OUTCOMES = {"ok": "status = 'ok'", "no_answer": "status = 'no_answer'", "error": "status IN ('error', 'timeout')"}
VERDICTS = {"ok": "ok = 1", "fail": "ok = 0"}


def cost(model, tokens_in, tokens_out):
    price = PRICES.get(model)
    return round((tokens_in * price[0] + tokens_out * price[1]) / 1e6, 6) if price else None


def totals(rows):
    """One line of the summary. Finished answers from the cache took no time, so they stay out of the timings."""
    timed = [r for r in rows if not r["cached"] and r["status"] in ("ok", "no_answer")]
    spent = sorted(r["total_ms"] for r in timed)
    judged = [r for r in rows if r["ok"] is not None]

    def middle(key):
        return statistics.median(r[key] or 0 for r in timed) if timed else None

    return {
        "questions": len(rows), "answered": sum(r["status"] == "ok" for r in rows), "no_answer": sum(r["status"] == "no_answer" for r in rows),
        "errors": sum(r["status"] in ("error", "timeout") for r in rows), "cached": sum(bool(r["cached"]) for r in rows),
        "judged": len(judged), "correct": sum(r["ok"] for r in judged),
        "median_ms": statistics.median(spent) if spent else None, "p95_ms": spent[int(len(spent) * .95)] if spent else None, "max_ms": spent[-1] if spent else None,
        "read_ms": middle("read_ms"), "search_ms": middle("search_ms"), "answer_ms": middle("answer_ms"),
        "cost_usd": round(sum(r["cost_usd"] or 0 for r in rows), 4), "times": spent,
    }


class Journal:
    def __init__(self, path=PATH):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        self.con.execute(SCHEMA)
        self.con.execute("CREATE INDEX IF NOT EXISTS runs_item ON runs(run_id, item_id)")
        self.con.commit()

    def add(self, moment, source, run_id, item, result, trace, total_ms, model):
        """Writes one answer down. A journal that fails must not take the answer with it."""
        usage, error = result.get("usage") or {}, result.get("error") or {}
        tokens_in, tokens_out = (0, 0) if trace.cached else (usage.get("input_tokens", 0), usage.get("output_tokens", 0))
        row = {
            "started_at": moment, "source": source, "run_id": run_id, "item_id": item["id"], "question": item["question"], "language": result.get("answer_language"),
            "status": result["status"], "answer": result.get("answer"), "citations": json.dumps(result.get("citations") or [], ensure_ascii=False), "model": model,
            "cached": int(trace.cached), "total_ms": total_ms, "read_ms": trace.spans.get("read"), "search_ms": trace.spans.get("search"),
            "answer_ms": trace.spans.get("answer"), "correct_ms": trace.spans.get("correct"), "tokens_in": tokens_in, "tokens_out": tokens_out,
            "cost_usd": cost(model, tokens_in, tokens_out), "plan": json.dumps(trace.plan, ensure_ascii=False) if trace.plan else None, "found": trace.found,
            "reason": trace.reason, "error": error.get("message"),
        }
        try:
            with self.lock:
                self.con.execute(f"INSERT INTO runs ({', '.join(row)}) VALUES ({', '.join('?' * len(row))})", tuple(row.values()))
                self.con.commit()
        except sqlite3.Error as e:
            print("journal:", e, flush=True)

    def asked_today(self, day):
        """Questions from the site that reached the model today: those are the ones that cost money."""
        with self.lock:
            return self.con.execute("SELECT count(*) FROM runs WHERE source = 'web' AND cached = 0 AND started_at >= ?", (day,)).fetchone()[0]

    def mark(self, run_id, verdicts):
        """A control run adds its verdict and the expected answer to what it was given."""
        with self.lock:
            marked = sum(self.con.execute("UPDATE runs SET ok = ?, why = ?, expected = ?, category = ? WHERE run_id = ? AND item_id = ?",
                                          (int(v["ok"]), v.get("why"), v.get("expected"), v.get("category"), run_id, v["id"])).rowcount for v in verdicts)
            self.con.commit()
        return marked

    def summary(self):
        with self.lock:
            rows = self.con.execute("SELECT * FROM runs ORDER BY id DESC").fetchall()
        groups = {}
        for row in rows:
            groups.setdefault((row["source"], row["run_id"] if row["source"] == "batch" else None), []).append(row)
        return {"groups": [{"source": source, "run_id": run_id, **totals(items)} for (source, run_id), items in groups.items()], "total": len(rows)}

    def runs(self, args, limit=100, offset=0):
        where = [sql for key, sql in FILTERS.items() if args.get(key)]
        params = [args[key] for key in FILTERS if args.get(key)]
        where += [table[args[key]] for key, table in (("outcome", OUTCOMES), ("verdict", VERDICTS)) if args.get(key) in table]
        if args.get("q"):
            where.append("question LIKE ?")
            params.append(f"%{args['q']}%")
        clause = " WHERE " + " AND ".join(where) if where else ""
        with self.lock:
            total = self.con.execute(f"SELECT count(*) FROM runs{clause}", params).fetchone()[0]
            rows = self.con.execute(f"SELECT {LIST} FROM runs{clause} ORDER BY id DESC LIMIT ? OFFSET ?", [*params, limit, offset]).fetchall()
        return {"total": total, "rows": [dict(r) for r in rows]}

    def detail(self, row_id):
        with self.lock:
            row = self.con.execute("SELECT * FROM runs WHERE id = ?", (row_id,)).fetchone()
        if row is None:
            return None
        return {**dict(row), "citations": json.loads(row["citations"] or "[]"), "plan": json.loads(row["plan"]) if row["plan"] else None}
