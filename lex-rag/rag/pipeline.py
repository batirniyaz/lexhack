"""One question from start to finish. The model reads and words; code finds, checks and holds the truth.

The model sees sources under short names and answers with those names. It never writes a document number, an article,
a status or a date: code puts those in from the index. So a source cannot be invented, only cited wrongly, and that is checked.
"""
import hashlib
import html
import json
import os
import re
import sqlite3
import threading
import time
from contextlib import contextmanager

from lexuz import store
from lexuz.translit import to_cyrillic, to_latin
from rag import language
from rag.llm import ModelError
from rag.numbers import unsupported

MARK = re.compile(r"\[C(\d+)\]")
CANDIDATES = 20        # sources read by the model, before whole articles are filled in
MAX_SOURCES = 44
MAX_CHARS = 40000
SPACES = re.compile(r"\s+")
LANGUAGE_NAMES = {"uz-Latn": "Uzbek in Latin script", "uz-Cyrl": "Uzbek in Latin script", "ru": "Russian"}
CACHE_PATH = store.DATA / "answers.sqlite"
SEARCHES = threading.BoundedSemaphore(max(1, (os.cpu_count() or 2) - 1))   # a search fills a core: one core always stays free for whatever else lives on the machine
NOT_FOUND = {"uz-Latn": "Mavjud qonun hujjatlarida bu savolga javob topilmadi.", "uz-Cyrl": "Мавжуд қонун ҳужжатларида бу саволга жавоб топилмади.",
             "ru": "В законодательстве, доступном системе, ответ на этот вопрос не найден."}


def squeeze(text):
    return SPACES.sub(" ", text).strip()


def verbatim(quote, text):
    """The span as it stands in the source, or None when the model changed it."""
    if not quote:
        return None
    if quote in text:
        return quote
    flat = squeeze(text)
    wanted = squeeze(quote)
    return wanted if wanted in flat else None


def best_sentence(text, answer):
    """When the model's quote is not exact: the source sentence closest to what the answer says, unchanged."""
    words = set(re.findall(r"\w{4,}", answer.lower()))
    sentences = [s.strip() for s in re.split(r"(?<=[.;:])\s+|\n+", text) if s.strip()]
    return max(sentences, key=lambda s: (len(words & set(re.findall(r"\w{4,}", s.lower()))), -len(s)), default=text[:300])[:400]


def place(row):
    parts = [p for p in (row["appendix"], row["article"], row["part"]) if p]
    return ", ".join(parts) or "matn"


def render(sources):
    blocks = []
    for name, row in sources.items():
        attributes = f'id="{name}" act="{html.escape(row["doc_title"], quote=True)}" type="{row["doc_type"]}" status="{row["doc_status"]}" adopted="{row["adopted"] or ""}" place="{html.escape(place(row), quote=True)}"'
        heading = row["article_title"] and row["part"] in (None, "1-qism") and row["article_title"] not in row["text"][:200]
        title = f'{row["article_title"]}\n' if heading else ""
        text = row["text"].replace("</source", "< /source")   # a text must not be able to end its own block
        blocks.append(f"<source {attributes}>\n{title}{text}\n</source>")
    return "\n".join(blocks)


class Cache:
    """Finished answers: the same question on the same index gives the same sources, whatever the model would say today."""

    def __init__(self, path=CACHE_PATH):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.Lock()
        self.con.execute("CREATE TABLE IF NOT EXISTS answers (key TEXT PRIMARY KEY, value TEXT)")

    def get(self, key):
        with self.lock:
            row = self.con.execute("SELECT value FROM answers WHERE key = ?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, key, value):
        with self.lock:
            self.con.execute("INSERT OR REPLACE INTO answers VALUES (?, ?)", (key, json.dumps(value, ensure_ascii=False)))
            self.con.commit()


class Trace:
    """Where one answer's time went and what the search was asked. The page and /logs read it; the answer does not depend on it."""

    def __init__(self, on_step=None):
        self.on_step, self.spans = on_step, {}
        self.plan, self.found, self.reason, self.cached = None, 0, None, False

    @contextmanager
    def span(self, name):
        if self.on_step:
            self.on_step(name)
        began = time.perf_counter()
        try:
            yield
        finally:
            self.spans[name] = round((time.perf_counter() - began) * 1000)


class Pipeline:
    def __init__(self, search, model, index_version="dev", cache=None):
        self.search, self.model, self.index_version = search, model, index_version
        self.cache = cache

    def key(self, question, language_code, options):
        fields = (squeeze(question), language_code, options.get("top_k", 5), options.get("as_of_date"), options.get("answer_language", "auto"), self.index_version)
        return hashlib.sha256(json.dumps(fields, ensure_ascii=False).encode()).hexdigest()

    def answer(self, item, options, trace=None):
        """One result object of the spec. Never raises: one bad question must not take the batch down."""
        started = time.time()
        trace = trace or Trace()
        code = item.get("language") or language.detect(item["question"])
        if self.cache and (saved := self.cache.get(self.key(item["question"], code, options))):
            trace.cached = True
            return {**saved, "id": item["id"], "debug": {**(saved.get("debug") or {}), "cached": True}}
        try:
            result = self._run(item, code, options, started, trace)
        except ModelError as e:
            return failure(item["id"], e.code, str(e), e.retryable)
        except sqlite3.Error as e:
            return failure(item["id"], "RETRIEVAL_FAILED", str(e), True)
        if self.cache:
            self.cache.put(self.key(item["question"], code, options), result)
        return result

    def _run(self, item, code, options, started, trace):
        target = code if options.get("answer_language", "auto") == "auto" else options["answer_language"]
        question = item["question"]
        usage = {"input_tokens": 0, "output_tokens": 0}

        with trace.span("read"):
            plan, spent = self.model.read(question)
        add(usage, spent)
        trace.plan = plan
        read_done = time.time()
        if not plan["is_legal"]:
            return self.no_answer(item, target, [], options, usage, started, read_done, read_done, trace, "outside the law")

        latin = to_latin(question) if code != "ru" else ""
        with trace.span("search"), SEARCHES:
            rows = self.search.retrieve(f"{plan['query']} {latin}", terms=plan["terms"] + [plan["query_ru"]], act_names=plan["acts"],
                                        as_of=options.get("as_of_date"), old=plan["asks_about_past"], limit=60)
        retrieved = time.time()
        trace.found = len(rows)
        if not rows:
            return self.no_answer(item, target, [], options, usage, started, retrieved, retrieved, trace, "nothing found")

        sources = self.sources(rows)
        prompt = f"Question: {question}\nWrite the answer in {LANGUAGE_NAMES[target]}.\n\n{render(sources)}"
        with trace.span("answer"):
            reply, raw, spent = self.model.answer(prompt)
        add(usage, spent)
        problems = check(reply, sources, question)
        retried = False
        if problems:
            retried = True
            with trace.span("correct"):
                reply, raw, spent = self.model.correct(prompt, raw, problems)
            add(usage, spent)
            problems = check(reply, sources, question)
        generated = time.time()
        if reply["verdict"] == "no_answer" or problems:
            reason = "; ".join(problems) if problems else reply["reason"]
            return self.no_answer(item, target, rows, options, usage, started, retrieved, generated, trace, reason, reply["ranking"], sources)
        return self.finish(item, target, reply, rows, sources, options, usage, started, retrieved, generated, plan, retried)

    def sources(self, rows):
        """The best candidates, each with the rest of its article: a part often only makes sense next to the others."""
        chosen, total = {}, 0
        for row in rows[:CANDIDATES]:
            family = self.search.parts_of(row["doc_id"], row["article"], row["appendix"])[:6] if row["article"] and row["part"] else [row]
            for member in family or [row]:
                if member["chunk_id"] in chosen or len(chosen) >= MAX_SOURCES or total + len(member["text"]) > MAX_CHARS:
                    continue
                member.setdefault("retrieval_score", row["retrieval_score"] * 0.8)
                chosen[member["chunk_id"]] = member
                total += len(member["text"])
        return {f"C{n}": row for n, row in enumerate(chosen.values(), 1)}

    def finish(self, item, target, reply, rows, sources, options, usage, started, retrieved, generated, plan, retried):
        answer = reply["answer"]
        order = list(dict.fromkeys(f"C{n}" for n in MARK.findall(answer)))
        refs = {name: n for n, name in enumerate(order, 1)}
        answer = MARK.sub(lambda m: f"[{refs['C' + m.group(1)]}]", answer)
        quotes = {q["source"]: q["quote"] for q in reply["quotes"]}
        citations = []
        for name in order:
            row = sources[name]
            quote = verbatim(quotes.get(name), row["text"]) or best_sentence(row["text"], reply["answer"])
            citations.append({**citation_fields(row), "ref": refs[name], "quote": quote})
        if target == "uz-Cyrl":
            answer = to_cyrillic(answer)
        contexts = self.contexts(rows, sources, reply["ranking"], order, options)
        return {
            "id": item["id"], "status": "ok", "answer": answer, "answer_language": target, "no_answer": False,
            "confidence": round(max(0.0, min(1.0, reply["confidence"])) * (0.9 if retried else 1.0), 2),
            "citations": citations, "contexts": contexts if options.get("return_contexts", True) else keep_cited(contexts, citations),
            "debug": debug(plan, rows, retried) if options.get("return_debug") else None,
            "timing": timing(started, retrieved, generated), "usage": usage, "error": None,
        }

    def contexts(self, rows, sources, ranking, used, options):
        """Top k for the tester, the model's reading first: it has seen the text and the search has only matched it."""
        by_name = {name: row for name, row in sources.items()}
        ordered = [by_name[n] for n in dict.fromkeys([*used, *ranking]) if n in by_name]
        seen = {r["chunk_id"] for r in ordered}
        ordered += [r for r in rows if r["chunk_id"] not in seen]
        limit = max(options.get("top_k", 5), len(used))
        top = max((r.get("retrieval_score", 0) for r in rows), default=1) or 1
        names = {row["chunk_id"]: name for name, row in sources.items()}
        result = []
        for rank, row in enumerate(ordered[:limit], 1):
            name = names.get(row["chunk_id"])
            result.append({
                "rank": rank, "chunk_id": row["chunk_id"], "doc_id": f"lex:{row['number']}", "article": row["article"], "text": row["text"],
                "retrieval_score": round(min(1.0, row.get("retrieval_score", 0) / top), 4),
                "rerank_score": round(1 - (rank - 1) / (limit + 1), 4) if name in ranking or name in used else None,
                "used_in_answer": name in used,
            })
        return result

    def no_answer(self, item, target, rows, options, usage, started, retrieved, generated, trace, reason, ranking=(), sources=None):
        trace.reason = reason
        contexts = self.contexts(rows, sources or {}, list(ranking), [], options) if rows else []
        return {
            "id": item["id"], "status": "no_answer", "answer": NOT_FOUND[target], "answer_language": target, "no_answer": True, "confidence": 0.0,
            "citations": [], "contexts": contexts if options.get("return_contexts", True) else [],
            "debug": {**debug(trace.plan, rows, False), "reason": reason} if options.get("return_debug") else None,
            "timing": timing(started, retrieved, generated), "usage": usage, "error": None,
        }


def check(reply, sources, question=""):
    """What code will not let through. Empty means the answer may go out. A number from the question is the asker's own fact, not a claim about the law."""
    if reply["verdict"] == "no_answer":
        return []
    answer = reply["answer"]
    marks = MARK.findall(answer)
    if not answer.strip() or not marks:
        return ["The answer has no source marks."]
    problems = [f"[C{n}] is not one of the sources." for n in dict.fromkeys(marks) if f"C{n}" not in sources]
    if problems:
        return problems
    cited = [sources[f"C{n}"] for n in dict.fromkeys(marks)]
    evidence = " ".join(f"{row['text']} {row['article_title'] or ''}" for row in cited)
    wrong = unsupported(MARK.sub(" ", answer), f"{evidence} {question}")
    if wrong:
        problems.append(f"These numbers are not in the cited sources: {wrong}.")
    return problems


def citation_fields(row):
    return {
        "doc_id": f"lex:{row['number']}", "doc_title": row["doc_title"], "doc_type": row["doc_type"], "url": row["url"], "article": row["article"], "part": row["part"],
        "edition_date": row["edition_date"], "doc_status": row["doc_status"], "chunk_id": row["chunk_id"],
    }


def keep_cited(contexts, citations):
    cited = {c["chunk_id"] for c in citations}
    return [c for c in contexts if c["chunk_id"] in cited]


def add(total, spent):
    total["input_tokens"] += spent["input_tokens"]
    total["output_tokens"] += spent["output_tokens"]


def debug(plan, rows, retried):
    return {"rewritten_query": plan["query"], "terms": plan["terms"], "acts": plan["acts"], "retrieved_total": len(rows), "retried": retried, "cached": False}


def timing(started, retrieved, generated):
    now = time.time()
    return {"retrieval_ms": round((retrieved - started) * 1000), "rerank_ms": 0, "generation_ms": round((generated - retrieved) * 1000), "total_ms": round((now - started) * 1000)}


def failure(item_id, code, message, retryable):
    return {"id": item_id, "status": "timeout" if code == "LLM_TIMEOUT" else "error", "answer": None, "no_answer": False, "citations": [], "contexts": [],
            "error": {"code": code, "message": message, "retryable": retryable}}


