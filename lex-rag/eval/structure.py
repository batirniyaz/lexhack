"""Does the server answer in the shape the tester expects: section 4 of the spec for a reply, sections 2 and 5 for its behaviour.

`check` reads one reply and costs nothing. `protocol` talks to a running server, but only with requests that never reach the model,
apart from the batch it is given, which should have been sent already.
"""
import re
import time

TOP = ("run_id", "batch_id", "status", "system", "timing", "summary", "results")
SYSTEM = ("pipeline_version", "llm_model", "embedding_model", "reranker", "index_version", "lex_snapshot_date")
BATCH_TIMING = ("received_at", "completed_at", "total_ms")
SUMMARY = ("total", "ok", "no_answer", "error")
RESULT = ("id", "status", "answer", "no_answer", "citations", "contexts", "error")
ANSWERED = ("answer_language", "confidence", "timing", "usage", "debug")
TIMING = ("retrieval_ms", "rerank_ms", "generation_ms", "total_ms")
USAGE = ("input_tokens", "output_tokens")
CITATION = ("ref", "doc_id", "doc_title", "doc_type", "url", "article", "part", "edition_date", "doc_status", "chunk_id", "quote")
CONTEXT = ("rank", "chunk_id", "doc_id", "article", "text", "retrieval_score", "rerank_score", "used_in_answer")
MAY_BE_EMPTY = {"article", "part", "rerank_score", "embedding_model", "reranker", "debug"}   # an act without articles, a source nobody ranked, a run without vectors

DOC_ID = re.compile(r"lex:\d+$")
CHUNK_ID = re.compile(r"lex:\d+#\S+$")
URL = re.compile(r"https://lex\.uz/docs/-?(\d+)$")   # the minus is the script of the page on lex.uz, not another document
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")
REF = re.compile(r"\[(\d+)\]")
STATUSES = {"ok", "no_answer", "error", "timeout"}
SPACES = re.compile(r"\s+")


def missing(where, record, fields):
    if not isinstance(record, dict):
        return [f"{where}: not an object"]
    return [f"{where}: no {name}" for name in fields if name not in record or (record[name] in (None, "") and name not in MAY_BE_EMPTY)]


def flat(text):
    return SPACES.sub(" ", text or "").strip()


def check_citation(where, citation, contexts):
    problems = missing(where, citation, CITATION)
    if problems:
        return problems
    if not DOC_ID.match(citation["doc_id"]):
        problems.append(f"{where}: doc_id {citation['doc_id']}")
    url = URL.match(citation["url"])
    if not url or url.group(1) != citation["doc_id"][4:]:
        problems.append(f"{where}: url {citation['url']} does not match {citation['doc_id']}")
    if not CHUNK_ID.match(citation["chunk_id"]):
        problems.append(f"{where}: chunk_id {citation['chunk_id']}")
    if not DATE.match(citation["edition_date"]):
        problems.append(f"{where}: edition_date {citation['edition_date']}")
    source = contexts.get(citation["chunk_id"])
    if source is None:
        problems.append(f"{where}: {citation['chunk_id']} is not in contexts")
    elif flat(citation["quote"]) not in flat(source["text"]):
        problems.append(f"{where}: the quote is not in the text of {citation['chunk_id']}")
    return problems


def check_result(result, top_k):
    name = result.get("id", "?")
    problems = missing(name, result, [f for f in RESULT if f not in ("answer", "error", "no_answer")])
    if "answer" not in result or "error" not in result or "no_answer" not in result:
        problems.append(f"{name}: answer, no_answer or error is absent")
    if problems:
        return problems
    status = result["status"]
    if status not in STATUSES:
        return [f"{name}: status {status}"]
    if status in ("error", "timeout"):
        error = result["error"] or {}
        return missing(f"{name} error", error, ("code", "message")) + ([] if "retryable" in error else [f"{name}: error has no retryable"]) + \
            ([f"{name}: failed but holds an answer"] if result["answer"] is not None else [])

    problems += missing(name, result, ANSWERED) + missing(f"{name} timing", result.get("timing"), TIMING) + missing(f"{name} usage", result.get("usage"), USAGE)
    if result["error"] is not None:
        problems.append(f"{name}: status {status} with an error")
    if not isinstance(result["answer"], str) or not result["answer"].strip():
        problems.append(f"{name}: empty answer")
    if not 0 <= (result.get("confidence") or 0) <= 1:
        problems.append(f"{name}: confidence {result.get('confidence')}")
    if (status == "no_answer") != (result["no_answer"] is True):
        problems.append(f"{name}: status {status}, no_answer {result['no_answer']}")

    contexts = {}
    for position, context in enumerate(result["contexts"], 1):
        trouble = missing(f"{name} context {position}", context, CONTEXT)
        problems += trouble
        if trouble:
            continue
        contexts[context["chunk_id"]] = context
        if context["rank"] != position:
            problems.append(f"{name}: context {position} has rank {context['rank']}")
        if not DOC_ID.match(context["doc_id"]) or not CHUNK_ID.match(context["chunk_id"]):
            problems.append(f"{name}: context {position} ids {context['doc_id']} {context['chunk_id']}")
        if not 0 <= context["retrieval_score"] <= 1:
            problems.append(f"{name}: context {position} retrieval_score {context['retrieval_score']}")
    if len(result["contexts"]) > max(top_k, len(result["citations"])):
        problems.append(f"{name}: {len(result['contexts'])} contexts for top_k {top_k}")

    if status == "no_answer":
        if result["citations"]:
            problems.append(f"{name}: no_answer with citations")
        return problems
    if not result["citations"]:
        problems.append(f"{name}: ok without citations")
    for citation in result["citations"]:
        problems += check_citation(f"{name} citation {citation.get('ref')}", citation, contexts)
    refs = [c.get("ref") for c in result["citations"]]
    marks = {int(m) for m in REF.findall(result["answer"] or "")}
    if len(set(refs)) != len(refs) or marks != set(refs):
        problems.append(f"{name}: marks {sorted(marks)} in the answer, refs {refs} in citations")
    used = {c for c, row in contexts.items() if row["used_in_answer"]}
    if used != {c.get("chunk_id") for c in result["citations"]}:
        problems.append(f"{name}: used_in_answer does not match the citations")
    return problems


def check(request, response):
    """Everything wrong with one batch reply, as lines a person can read. Empty means it holds."""
    problems = missing("reply", response, TOP)
    if problems:
        return problems
    problems += missing("system", response["system"], SYSTEM) + missing("timing", response["timing"], BATCH_TIMING) + missing("summary", response["summary"], SUMMARY)
    for field in ("run_id", "batch_id"):
        if response[field] != request[field]:
            problems.append(f"{field}: sent {request[field]}, got {response[field]}")
    if response["status"] != "completed":
        problems.append(f"status {response['status']}")
    results = response["results"]
    sent, got = sorted(i["id"] for i in request["items"]), sorted(r.get("id", "?") for r in results)
    if sent != got:
        problems.append(f"ids: sent {sent}, got {got}")
    summary = response["summary"]
    counted = {"total": len(results), "ok": sum(r.get("status") == "ok" for r in results), "no_answer": sum(r.get("status") == "no_answer" for r in results),
               "error": sum(r.get("status") in ("error", "timeout") for r in results)}
    if any(summary.get(k) != v for k, v in counted.items()):
        problems.append(f"summary {summary}, counted {counted}")
    top_k = (request.get("options") or {}).get("top_k", 5)
    for result in results:
        problems += check_result(result, top_k)
    return problems


def expect(problems, label, reply, *codes):
    if reply.status_code not in codes:
        problems.append(f"{label}: expected {codes}, got {reply.status_code} {reply.text[:120]}")


def protocol(client, sent, stored):
    """The rules around a batch, tried on a live server. `sent` and `stored` are a batch that already went through and its reply."""
    problems = []

    def post(body, **extra):
        time.sleep(1.1)   # the limit is tried on purpose at the end, not by accident here
        return client.post("/v1/rag/batch", json=body, **extra)

    item = sent["items"][0]
    fresh = {**sent, "batch_id": f"{sent['batch_id']}-protocol", "items": sent["items"]}

    expect(problems, "health", client.get("/v1/health"), 200)
    meta = client.get("/v1/meta")
    expect(problems, "meta", meta, 200)
    if meta.status_code == 200:
        problems += missing("meta", meta.json(), SYSTEM)
    expect(problems, "no key", client.post("/v1/rag/batch", json=sent, headers={"Authorization": ""}), 401, 403)
    expect(problems, "wrong key", client.post("/v1/rag/batch", json=sent, headers={"Authorization": "Bearer wrong"}), 401, 403)
    expect(problems, "eleven items", post({**fresh, "items": [{**item, "id": f"x{n}"} for n in range(11)]}), 400)
    expect(problems, "no items", post({**fresh, "items": []}), 400)
    expect(problems, "repeated id", post({**fresh, "items": [item, item]}), 400)
    expect(problems, "empty question", post({**fresh, "items": [{**item, "question": "  "}]}), 400)

    again = post(sent)
    expect(problems, "same batch_id", again, 200)
    if again.status_code == 200 and again.json()["timing"] != stored["timing"]:
        problems.append("same batch_id was computed again")
    if "charset=utf-8" not in again.headers.get("content-type", "").lower():
        problems.append(f"content-type {again.headers.get('content-type')}")
    expect(problems, "same batch_id, other content", post({**sent, "items": [{**item, "question": item["question"] + " ?"}]}), 409)
    saved = client.get(f"/v1/rag/batch/{sent['batch_id']}")
    expect(problems, "GET batch", saved, 200)
    if saved.status_code == 200 and saved.json()["results"] != stored["results"]:
        problems.append("GET batch differs from the reply")
    expect(problems, "GET unknown batch", client.get("/v1/rag/batch/no-such-batch"), 404)

    time.sleep(1.1)
    burst = [client.post("/v1/rag/batch", json={**fresh, "items": []}) for _ in range(6)]
    limited = [r for r in burst if r.status_code == 429]
    if not limited:
        problems.append(f"six batches at once: {[r.status_code for r in burst]}, no 429")
    elif "retry-after" not in limited[0].headers:
        problems.append("429 without Retry-After")
    return problems
