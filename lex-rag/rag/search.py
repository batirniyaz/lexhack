"""Finding chunks: by act and article when the question names them, by words and by meaning otherwise.

Filters come before ranking: an act that lost force is not in the main index at all, so no ranking mistake can bring it back.
"""
import datetime as dt
import functools
import json
import re
import sqlite3
import threading

from lexuz import store
from lexuz.translit import to_latin
from rag.text import TOKEN, fold, tokens

INDEX = store.DATA / "index" / "lex.sqlite"
TITLE_WEIGHT, HEAD_WEIGHT, BODY_WEIGHT = 2.0, 6.0, 1.0
AUTHORITY = {0: 1.8, 1: 1.7, 2: 1.45, 3: 1.15, 4: 1.0, 5: 0.85, 6: 0.7}   # by acts.rank; local acts sit lower still
LOCAL = 0.45
AMENDING = 0.5      # "changes to the Labor Code" quotes norms that the code itself states better
RECENCY = 0.01      # per year after 2016: between acts of one level a newer one wins a close match, so last year's amount does not push out this year's
RRF = 60
MIN_FIT = 0.2       # below this a title shares a word with the name and little else
CLOSE_FIT = 0.5     # a title this close ends the looking
TITLE_FIT = 0.8     # a search term this close to the title of a law is that law
COMMON_DOCS = 50000 # a word in this many chunks of a million says little about which one, and the search has to read its whole list
MIN_WORDS = 4       # a question made of common words only still needs some
PER_ARTICLE = 2     # top results should cover several articles, not one article's parts
CODE_NAMED = re.compile(r"(\w+\s+kodeks)", re.I)
GENERIC = {"ozbekiston", "respublika", "respublikasi", "respublikas", "qonun", "togr"}   # words every title or name may carry, as stems
AMENDS = re.compile(r"ozgartir|ozgartish|qoshimcha")
ARTICLE_NAMED = re.compile(r"(\d+[⁰¹²³⁴⁵⁶⁷⁸⁹]*)\s*-?\s*modda|стать\w*\s+(\d+[⁰¹²³⁴⁵⁶⁷⁸⁹]*)", re.I)
FIELDS = """c.id, c.chunk_id, c.doc_id, c.text, c.article, c.part, c.article_title, c.appendix, c.headers, c.element_ids, c.is_table,
            a.title, a.doc_type, a.rank, a.amending, a.section, a.status, a.edition, a.url, a.number, a.lang, a.adopted"""
NAMES = ("id", "chunk_id", "doc_id", "text", "article", "part", "article_title", "appendix", "headers", "element_ids", "is_table",
         "doc_title", "doc_type", "rank", "amending", "section", "doc_status", "edition_date", "url", "number", "lang", "adopted")


def weight(row):
    """How much a match in this act counts: a question that names no act should land on the highest one that answers it."""
    value = AUTHORITY.get(min(row["rank"], 6), 0.7)
    if row["section"] == "loc":
        value *= LOCAL
    if row["amending"]:
        value *= AMENDING
    if row["adopted"]:
        value *= 1 + RECENCY * max(0, int(row["adopted"][:4]) - 2016)
    return value


@functools.lru_cache(maxsize=60000)
def title_stems(title):
    return [t for t in tokens(title) if t not in GENERIC]


def fit(wanted, title):
    """How well a title is this name: 1 when it says the same and no more. Stems differ in length ("band", "bandl"), so a shared start counts."""
    have = title_stems(title)
    same = sum(any(a.startswith(b) or b.startswith(a) for b in have) for a in wanted)
    return same / len(wanted) * min(1.0, same / max(len(have), 1))


def record(values):
    """One result as a dict. The public number is the one in the link: an act with text only in Russian has it on another page than its empty Latin one."""
    row = dict(zip(NAMES, values))
    row["number"] = row["url"].rsplit("/", 1)[-1].lstrip("-")
    row["chunk_id"] = f"lex:{row['number']}#{row['chunk_id'].partition('#')[2]}"
    return row


class Search:
    def __init__(self, path=INDEX, vectors=None):
        self.path = path
        self.vectors = vectors
        self.local = threading.local()
        starts = path.with_name("starts.json")
        self.starts = json.loads(starts.read_text(encoding="utf-8")) if starts.exists() else {}

    @property
    def con(self):
        """SQLite connections stay in the thread that opened them, and the API answers from several."""
        if not hasattr(self.local, "con"):
            self.local.con = sqlite3.connect(f"file:{self.path.as_posix()}?mode=ro", uri=True)
        return self.local.con

    @functools.cached_property
    def common(self):
        """The commonest words with their counts. Nine tenths of a search went on them, for almost no help in telling chunks apart."""
        con = sqlite3.connect(f"file:{self.path.as_posix()}?mode=ro", uri=True)
        con.execute("CREATE VIRTUAL TABLE temp.vocabulary USING fts5vocab(main, fts_force, row)")
        return dict(con.execute("SELECT term, doc FROM temp.vocabulary WHERE doc > ?", (COMMON_DOCS,)))

    def rare(self, words):
        """The words worth a search over everything. Inside one act all of them still count, there it is cheap."""
        stems = list(dict.fromkeys(words))
        kept = [w for w in stems if w not in self.common]
        return kept + sorted((w for w in stems if w in self.common), key=self.common.get)[:max(0, MIN_WORDS - len(kept))]

    def rows(self, ids):
        if not ids:
            return []
        marks = ",".join("?" * len(ids))
        found = self.con.execute(f"SELECT {FIELDS} FROM chunks c JOIN acts a USING (doc_id) WHERE c.id IN ({marks})", list(ids)).fetchall()
        by_id = {r[0]: record(r) for r in found}
        return [by_id[i] for i in ids if i in by_id]

    def words(self, terms, limit=120, table="fts_force", span=None):
        """Chunk ids with a BM25 score, best first. A span keeps the search inside one act: its chunks are neighbours."""
        terms = list(dict.fromkeys(terms))
        if not terms:
            return []
        query = " OR ".join(f'"{t}"' for t in terms)
        where, args = f"{table} MATCH ?", [query]
        if span:
            where += " AND rowid BETWEEN ? AND ?"
            args += list(span)
        sql = f"SELECT rowid, -bm25({table}, {TITLE_WEIGHT}, {HEAD_WEIGHT}, {BODY_WEIGHT}) s FROM {table} WHERE {where} ORDER BY s DESC LIMIT ?"
        return self.con.execute(sql, args + [limit]).fetchall()

    def find_acts(self, name, limit=3):
        """Acts by name, best fit first. The model names an act from memory: "Pensiya taʼminoti toʻgʻrisidagi qonun" is titled
        "Fuqarolarning davlat pensiya taʼminoti toʻgʻrisida", so a name needs no word-for-word match, only a title close to it.
        A wrong act costs little here: it only opens one more place to search.

        An act carrying the name as one phrase beats one that only has the same words: "Fuqarolik kodeksi" is not "Fuqarolik protsessual kodeksi".
        """
        wanted = [t for t in dict.fromkeys(tokens(name)) if t not in GENERIC]
        if not wanted:
            return []
        found = self.titles(" AND ".join(f'"{t}"*' for t in wanted))
        if not any(fit(wanted, act["title"]) >= CLOSE_FIT for act in found):
            found += self.titles(" OR ".join(f'"{t}"*' for t in wanted))
        phrase = " ".join(t for t in TOKEN.findall(fold(name)) if t not in ("qonun", "qonuni"))

        def order(act):
            title = " ".join(TOKEN.findall(fold(act["title"])))
            changes = bool(act["amending"] or AMENDS.search(title))
            closeness = fit(wanted, act["title"]) * AUTHORITY.get(min(act["rank"], 6), 0.7) * (2 if phrase in title else 1)
            return act["status"] != "amalda", changes, -closeness, len(title)

        chosen = {act["doc_id"]: act for act in found if fit(wanted, act["title"]) >= MIN_FIT}
        return sorted(chosen.values(), key=order)[:limit]

    def titles(self, query, extra=""):
        rows = self.con.execute(f"""SELECT a.doc_id, a.title, a.doc_type, a.rank, a.amending, a.status, s.first, s.last
            FROM fts_acts f JOIN acts a ON a.rowid = f.rowid JOIN spans s USING (doc_id) WHERE fts_acts MATCH ? {extra}
            ORDER BY a.status != 'amalda', a.amending, a.rank, length(a.title) LIMIT 300""", (query,)).fetchall()
        return [dict(zip(("doc_id", "title", "doc_type", "rank", "amending", "status", "first", "last"), r)) for r in rows]

    def titled(self, terms, known):
        """A search term that is the title of a law opens that law, even when the model did not name it: "vasiylik va homiylik"."""
        seen, acts = {act["doc_id"] for act in known}, []
        for term in terms:
            wanted = [t for t in dict.fromkeys(tokens(term)) if t not in GENERIC]
            if not wanted:
                continue
            for act in self.titles(" AND ".join(f'"{t}"*' for t in wanted), "AND a.rank <= 2 AND a.status = 'amalda' AND a.amending = 0"):
                if act["doc_id"] not in seen and fit(wanted, act["title"]) >= TITLE_FIT:
                    seen.add(act["doc_id"])
                    acts.append(act)
        return acts[:2]

    def article(self, doc_id, article):
        ids = [r[0] for r in self.con.execute(
            "SELECT id FROM chunks WHERE doc_id = ? AND article = ? AND appendix IS NULL ORDER BY seq, piece", (doc_id, article))]
        return ids

    def parts_of(self, doc_id, article, appendix):
        """The whole article, for the model to read around the part that matched."""
        rows = self.con.execute(f"""SELECT {FIELDS} FROM chunks c JOIN acts a USING (doc_id)
            WHERE c.doc_id = ? AND c.article = ? AND c.appendix IS ? ORDER BY c.seq, c.piece""", (doc_id, article, appendix)).fetchall()
        return [record(r) for r in rows]

    def started(self, row, moment):
        start = self.starts.get(row["doc_id"]) or row["adopted"]
        return not start or start <= moment

    def rank(self, lists):
        """Reciprocal rank fusion. Each list is (weight, [(id, score), ...]); the authority of the act is applied at the end."""
        scores = {}
        for list_weight, hits in lists:
            for place, (chunk, _) in enumerate(hits):
                scores[chunk] = scores.get(chunk, 0.0) + list_weight / (RRF + place + 1)
        ordered = sorted(scores, key=lambda c: (-scores[c], c))[:300]
        rows = self.rows(ordered)
        for row in rows:
            row["fused"] = scores[row["id"]]
            row["retrieval_score"] = scores[row["id"]] * weight(row)
        rows.sort(key=lambda r: (-r["retrieval_score"], r["id"]))
        return rows

    def retrieve(self, question, terms=(), act_names=(), limit=30, as_of=None, old=False):
        """The candidates for one question. `terms` and `act_names` come from the model's reading of the question, when there is one.

        `old` also opens the index of acts no longer in force, for questions about the past. Acts that do not work yet on `as_of`, today by default, are dropped.
        """
        text = to_latin(question)
        words = tokens(text) + [t for term in terms for t in tokens(term)]
        lists = [(1.0, self.scored_words(words))]
        if self.vectors:
            lists.append((1.0, self.vectors.search(text)))
        named = [*act_names, *CODE_NAMED.findall(text)]
        found = [act for name in named for act in self.find_acts(name)[:2]]
        found += self.titled(terms, found)
        acts = [act for act in found if act["status"] == "amalda"]
        if old:
            lists.append((0.7, self.words(self.rare(words), limit=60, table="fts_old")))
            lists += [(1.5, self.words(words, limit=20, span=(act["first"], act["last"]), table="fts_old")) for act in found if act["status"] != "amalda"]
        for act in acts:
            span = (act["first"], act["last"])
            lists.append((2.0, self.words(words, limit=60, span=span)))
            if self.vectors:
                lists.append((2.0, self.vectors.search(text, span=span)))
            for match in ARTICLE_NAMED.finditer(text):
                number = (match.group(1) or match.group(2)) + "-modda"
                lists.append((6.0, [(i, 1.0) for i in self.article(act["doc_id"], number)]))
        moment = as_of or dt.date.today().isoformat()
        rows = [r for r in self.rank(lists) if self.started(r, moment)]
        return diversify(rows)[:limit]

    def scored_words(self, words):
        """Global word search. BM25 alone would fill the list with whatever act repeats a word most, so authority reorders it first."""
        hits = self.words(self.rare(words), limit=600)
        rows = self.rows([h[0] for h in hits])
        score = dict(hits)
        ranked = sorted(rows, key=lambda r: (-score[r["id"]] * weight(r), r["id"]))
        return [(r["id"], score[r["id"]]) for r in ranked[:150]]


def diversify(rows):
    """At most PER_ARTICLE pieces of one article near the top; the rest wait at the end instead of disappearing."""
    seen, first, rest = {}, [], []
    for row in rows:
        key = (row["doc_id"], row["appendix"], row["article"]) if row["article"] else row["id"]
        seen[key] = seen.get(key, 0) + 1
        (first if seen[key] <= PER_ARTICLE else rest).append(row)
    return first + rest
