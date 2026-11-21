"""Puts the real pipeline together. Kept apart so that tests of the API need neither the index nor a model."""
import os
import sqlite3

from api.main import VERSION
from rag import vectors
from rag.llm import Model
from rag.pipeline import Cache, Pipeline
from rag.search import INDEX, Search


def load():
    """Returns the pipeline, the `system` object of every answer, and the facts for /v1/meta."""
    con = sqlite3.connect(f"file:{INDEX.as_posix()}?mode=ro", uri=True)
    values = dict(con.execute("SELECT key, value FROM meta"))
    documents = con.execute("SELECT count(*) FROM acts").fetchone()[0]
    chunks = con.execute("SELECT count(*) FROM chunks").fetchone()[0]
    with_text = con.execute("SELECT count(DISTINCT doc_id) FROM chunks").fetchone()[0]
    in_force = con.execute("SELECT count(*) FROM acts a WHERE status = 'amalda' AND EXISTS (SELECT 1 FROM chunks c WHERE c.doc_id = a.doc_id)").fetchone()[0]
    con.close()
    meaning = vectors.Vectors() if vectors.FAISS.exists() else None
    model = Model()
    version = values["index_version"] + (f"+v{meaning.index.ntotal}" if meaning else "+words")   # half the vectors is another index: runs must not be compared as one
    system = {
        "pipeline_version": VERSION, "llm_model": model.name, "embedding_model": vectors.MODEL[0] if meaning else None,
        "reranker": f"{model.name} (reads the candidates while answering)", "index_version": version, "lex_snapshot_date": values["lex_snapshot_date"],
    }
    facts = {"documents": documents, "with_text": with_text, "in_force": in_force, "chunks": chunks, "vectors": meaning.index.ntotal if meaning else 0, "languages": ["uz-Latn", "uz-Cyrl", "ru"]}
    search = Search(vectors=meaning)
    search.common   # takes seconds, so it happens here and not during the first question
    pipeline = Pipeline(search, model, f"{version} {model.fingerprint}", Cache())
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    return pipeline, system, facts
