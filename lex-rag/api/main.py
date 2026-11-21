"""The test API from the spec: batches of up to ten questions, stored results, and one question's failure stays that question's.
Next to it the public page, which asks without a key under its own limits, and the journal at /logs.

  uvicorn api.main:app --port 8000      needs LEX_API_KEY and ANTHROPIC_API_KEY, for example in a .env file

Two keys open the API. LEX_API_KEY is the tester's. LEX_APP_KEY, if set, is the owner's other project: no batch rate limit,
and its questions go to the journal under their own source, apart from the test runs.
"""
import asyncio
import collections
import datetime as dt
import hashlib
import json
import os
import secrets
import sqlite3
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles

from api import docs
from api.journal import Journal
from lexuz import store
from rag.pipeline import Trace

VERSION = "0.1.0"
SYNC_LIMIT = 90           # seconds before a batch turns async: the spec allows 120, but Cloudflare cuts a reply off at 100
MAX_ITEMS, MAX_QUESTION = 10, 2000
LANGUAGES = {"uz-Latn", "uz-Cyrl", "ru"}
ANSWER_LANGUAGES = LANGUAGES | {"auto"}
PARALLEL = 5
RATE_PER_SECOND = 2       # the spec asks for at least one batch per second
TASHKENT = dt.timezone(dt.timedelta(hours=5))
BATCHES_PATH = store.DATA / "batches.sqlite"
WEB = Path(__file__).resolve().parent.parent / "web"
ASK_CHARS = 500
ASK_PER_MINUTE = 6        # from one address, and the page has no key: these limits are all that stands between it and the model bill
ASK_PER_DAY = 300         # from everyone together, finished answers from the cache not counted
PAGE_HEADERS = {"Cache-Control": "no-cache"}
bearer = HTTPBearer(auto_error=False, description="API-ключ, без слова Bearer")   # only for the Authorize button of /docs; `refused` does the checking


class Json(JSONResponse):
    media_type = "application/json; charset=utf-8"


def now():
    return dt.datetime.now(TASHKENT).isoformat(timespec="seconds")


def problem(status, code, message, headers=None):
    return Json({"error": {"code": code, "message": message}}, status_code=status, headers=headers)


class Batches:
    """Results stay here for good; the spec asks for at least thirty days."""

    def __init__(self, path=BATCHES_PATH):
        self.con = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.Lock()
        self.con.execute("CREATE TABLE IF NOT EXISTS batches (batch_id TEXT PRIMARY KEY, digest TEXT, status TEXT, response TEXT, created_at TEXT)")
        self.con.execute("UPDATE batches SET status = 'failed' WHERE status = 'processing'")   # a restart ended them
        self.con.commit()

    def get(self, batch_id):
        with self.lock:
            row = self.con.execute("SELECT digest, status, response FROM batches WHERE batch_id = ?", (batch_id,)).fetchone()
        return {"digest": row[0], "status": row[1], "response": json.loads(row[2]) if row[2] else None} if row else None

    def begin(self, batch_id, digest):
        with self.lock:
            self.con.execute("INSERT OR REPLACE INTO batches VALUES (?, ?, 'processing', NULL, ?)", (batch_id, digest, now()))
            self.con.commit()

    def finish(self, batch_id, status, response):
        with self.lock:
            self.con.execute("UPDATE batches SET status = ?, response = ? WHERE batch_id = ?", (status, json.dumps(response, ensure_ascii=False), batch_id))
            self.con.commit()


def validate(body):
    """The first thing wrong with a request, or None. A wrong language is not here: the spec makes it one question's error."""
    if not isinstance(body, dict):
        return "the body must be a JSON object"
    for field in ("run_id", "batch_id"):
        if not isinstance(body.get(field), str) or not body[field].strip():
            return f"{field} is required"
    for field in ("batch_index", "total_batches"):
        if not isinstance(body.get(field), int) or isinstance(body.get(field), bool):
            return f"{field} must be an integer"
    items = body.get("items")
    if not isinstance(items, list) or not 1 <= len(items) <= MAX_ITEMS:
        return f"items must hold 1 to {MAX_ITEMS} questions"
    seen = set()
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            return "every item needs a string id"
        if item["id"] in seen:
            return f"duplicate id {item['id']}"
        seen.add(item["id"])
        question = item.get("question")
        if not isinstance(question, str) or not question.strip():
            return f"empty question in {item['id']}"
        if len(question) > MAX_QUESTION:
            return f"question {item['id']} is longer than {MAX_QUESTION} characters"
    return validate_options(body.get("options") or {})


def validate_options(options):
    if not isinstance(options, dict):
        return "options must be an object"
    top_k = options.get("top_k", 5)
    if not isinstance(top_k, int) or isinstance(top_k, bool) or not 1 <= top_k <= 50:
        return "options.top_k must be between 1 and 50"
    if options.get("answer_language", "auto") not in ANSWER_LANGUAGES:
        return "options.answer_language is not one of auto, uz-Latn, uz-Cyrl, ru"
    date = options.get("as_of_date")
    if date is not None:
        try:
            dt.date.fromisoformat(date)
        except (TypeError, ValueError):
            return "options.as_of_date must be YYYY-MM-DD"
    return None


def digest_of(body):
    fields = {k: body.get(k) for k in ("run_id", "options", "items")}
    return hashlib.sha256(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def answer_one(pipeline, item, options, trace=None):
    if item.get("language") and item["language"] not in LANGUAGES:
        return {"id": item["id"], "status": "error", "answer": None, "no_answer": False, "citations": [], "contexts": [],
                "error": {"code": "INVALID_LANGUAGE", "message": f"language {item['language']} is not supported", "retryable": False}}
    try:
        return pipeline.answer(item, options, trace)
    except Exception as e:   # the batch has to survive anything one question does
        return {"id": item["id"], "status": "error", "answer": None, "no_answer": False, "citations": [], "contexts": [],
                "error": {"code": "LLM_ERROR", "message": f"{type(e).__name__}: {e}"[:300], "retryable": True}}


def has_retryable(response):
    return any((r.get("error") or {}).get("retryable") for r in response.get("results", []))


def visitor(request):
    """The tunnel is the only way in, so every connection is local and Cloudflare names the real address."""
    return request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")


def for_page(result):
    """A visitor reads the answer and its sources. Contexts, counts and the wording of an error stay out."""
    return {"status": result["status"], "answer": result.get("answer"), "language": result.get("answer_language"), "citations": result.get("citations") or []}


def create_app(pipeline=None, system=None, key=None, batches=None, facts=None, journal=None, app_key=None):
    """Tests pass their own parts. Without them the real pipeline loads once at startup."""

    @asynccontextmanager
    async def lifespan(app):
        if pipeline is None:
            load_dotenv()
            from api.loader import load
            app.state.pipeline, app.state.system, app.state.facts = load()
            app.state.keys = {"test": os.environ["LEX_API_KEY"], "app": os.environ.get("LEX_APP_KEY")}
        else:
            app.state.pipeline, app.state.system, app.state.facts, app.state.keys = pipeline, system, facts or {}, {"test": key, "app": app_key}
        app.state.batches = batches or Batches()
        app.state.journal = journal or Journal()
        app.state.gate = asyncio.Semaphore(PARALLEL)
        app.state.recent = collections.deque()
        app.state.asked = collections.deque()
        yield

    app = FastAPI(title="Вопросы по законам Узбекистана", version=VERSION, description=docs.DESCRIPTION, openapi_tags=docs.TAGS, lifespan=lifespan, default_response_class=Json,
                  swagger_ui_parameters={"docExpansion": "list", "defaultModelsExpandDepth": -1, "persistAuthorization": True, "displayRequestDuration": True, "tryItOutEnabled": True})

    @app.exception_handler(RequestValidationError)
    async def bad_request(_, error):
        return problem(400, "VALIDATION", str(error)[:300])

    def refused(request):
        """None when the key is one of ours; whose it is stays in request.state.holder."""
        header = request.headers.get("authorization", "")
        if not header.lower().startswith("bearer "):
            return problem(401, "UNAUTHORIZED", "Authorization: Bearer <API_KEY> is required")
        given = header[7:].strip().encode()
        for holder, key in request.app.state.keys.items():
            if key and secrets.compare_digest(given, key.encode()):
                request.state.holder = holder
                return None
        return problem(403, "FORBIDDEN", "wrong API key")

    def mine(request):
        return request.state.holder == "app"

    def too_fast(request):
        recent, moment = request.app.state.recent, time.monotonic()
        while recent and moment - recent[0] > 1:
            recent.popleft()
        if len(recent) >= RATE_PER_SECOND:
            return problem(429, "RATE_LIMIT", "too many batches", headers={"Retry-After": "1"})
        recent.append(moment)
        return None

    async def read_json(request):
        try:
            return json.loads(await request.body())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    async def ask_one(state, source, run_id, item, options, on_step=None):
        """One question through the gate, written down wherever it came from. The total counts the wait for the gate: a tester waits it out too."""
        moment, began, trace = now(), time.time(), Trace(on_step)
        async with state.gate:
            result = await asyncio.to_thread(answer_one, state.pipeline, item, options, trace)
        await asyncio.to_thread(state.journal.add, moment, source, run_id, item, result, trace, round((time.time() - began) * 1000), state.system["llm_model"])
        return result

    async def run(request_app, body, source="batch"):
        state, options = request_app.state, body.get("options") or {}
        started, received = time.time(), now()
        results = await asyncio.gather(*(ask_one(state, source, body["run_id"], item, options) for item in body["items"]))
        count = collections.Counter(r["status"] for r in results)
        response = {
            "run_id": body["run_id"], "batch_id": body["batch_id"], "status": "completed", "system": state.system,
            "timing": {"received_at": received, "completed_at": now(), "total_ms": round((time.time() - started) * 1000)},
            "summary": {"total": len(results), "ok": count["ok"], "no_answer": count["no_answer"], "error": count["error"] + count["timeout"]},
            "results": list(results),
        }
        state.batches.finish(body["batch_id"], "completed", response)
        return response

    @app.post("/v1/rag/batch", tags=[docs.SPEC], summary="Отправить батч", description="До 10 вопросов. Ответ приходит сразу, а если считается дольше 90 секунд, приходит 202.",
              dependencies=[Depends(bearer)], openapi_extra=docs.BATCH_BODY, responses=docs.replies(200, 202, 400, 401, 403, 409, 429, example=docs.BATCH_REPLY))
    async def post_batch(request: Request):
        if denied := refused(request):
            return denied
        if not mine(request) and (slow := too_fast(request)):   # the owner's project is not held to the tester's pace and does not use it up
            return slow
        body = await read_json(request)
        if (wrong := validate(body)) if body is not None else "the body is not valid JSON":
            return problem(400, "VALIDATION", wrong if body is not None else "the body is not valid JSON")
        state, batch_id, digest = request.app.state, body["batch_id"], digest_of(body)
        stored = state.batches.get(batch_id)
        if stored:
            if stored["digest"] != digest:
                return problem(409, "BATCH_CONFLICT", "this batch_id was sent with other content")
            if stored["status"] == "completed" and not has_retryable(stored["response"]):
                return Json(stored["response"])
            if stored["status"] == "processing":
                return Json({"batch_id": batch_id, "status": "processing"}, status_code=202)
        state.batches.begin(batch_id, digest)   # first time, or a retry after a retryable error: finished questions come from the cache
        task = asyncio.create_task(run(request.app, body, "app" if mine(request) else "batch"))
        try:
            return Json(await asyncio.wait_for(asyncio.shield(task), SYNC_LIMIT))
        except asyncio.TimeoutError:
            return Json({"batch_id": batch_id, "status": "processing"}, status_code=202)

    @app.get("/v1/rag/batch/{batch_id}", tags=[docs.SPEC], summary="Получить результат батча", description="Результаты хранятся и не считаются заново.",
             dependencies=[Depends(bearer)], responses=docs.replies(200, 401, 403, 404, example=docs.BATCH_REPLY))
    async def get_batch(batch_id: str, request: Request):
        if denied := refused(request):
            return denied
        stored = request.app.state.batches.get(batch_id)
        if stored is None:
            return problem(404, "NOT_FOUND", "no such batch_id")
        if stored["status"] == "completed":
            return Json(stored["response"])
        return Json({"batch_id": batch_id, "status": stored["status"]})

    @app.post("/v1/rag/query", tags=[docs.SPEC], summary="Задать один вопрос", dependencies=[Depends(bearer)], openapi_extra=docs.QUERY_BODY,
              responses=docs.replies(200, 400, 401, 403, example={"system": docs.SYSTEM, "result": docs.RESULT}))
    async def post_query(request: Request):
        if denied := refused(request):
            return denied
        body = await read_json(request)
        if not isinstance(body, dict) or not isinstance(body.get("question"), str) or not body["question"].strip():
            return problem(400, "VALIDATION", "question is required")
        if len(body["question"]) > MAX_QUESTION:
            return problem(400, "VALIDATION", f"question is longer than {MAX_QUESTION} characters")
        options = body.get("options") or {}
        if wrong := validate_options(options):
            return problem(400, "VALIDATION", wrong)
        item = {"id": body.get("id", "q"), "question": body["question"], "language": body.get("language")}
        result = await ask_one(request.app.state, "app" if mine(request) else "api", None, item, options)
        return Json({"system": request.app.state.system, "result": result})

    @app.get("/v1/meta", tags=[docs.SPEC], summary="Версии и размер базы", dependencies=[Depends(bearer)], responses=docs.replies(200, 401, 403, example=docs.META))
    async def meta(request: Request):
        if denied := refused(request):
            return denied
        return Json({**request.app.state.system, **request.app.state.facts})

    @app.head("/v1/health", include_in_schema=False)
    @app.get("/v1/health", tags=[docs.SPEC], summary="Жив ли сервис", description="Без ключа.",
             responses=docs.replies(200, example={"status": "ok", "time": "2026-11-06T15:00:00+05:00", "pipeline_version": "0.1.0"}))
    async def health(request: Request):
        return Json({"status": "ok", "time": now(), "pipeline_version": request.app.state.system["pipeline_version"]})

    def asked_too_often(state, address):
        recent, moment = state.asked, time.monotonic()
        while recent and moment - recent[0][0] > 60:
            recent.popleft()
        if sum(seen == address for _, seen in recent) >= ASK_PER_MINUTE:
            return True
        recent.append((moment, address))
        return False

    @app.post("/api/ask", tags=[docs.SITE], summary="Вопрос с главной страницы", openapi_extra=docs.ASK_BODY, responses=docs.replies(200, 400, 429),
              description="Без ключа: 6 вопросов в минуту с адреса и 300 в день на всех. Отвечает построчно (NDJSON): сначала строки `{\"step\": \"read\"}`, в конце `{\"answer\": {...}}`.")
    async def post_ask(request: Request):
        """The page's way in. Answers line by line, so that the page can say which step is running."""
        state, body = request.app.state, await read_json(request)
        question = body.get("question") if isinstance(body, dict) else None
        if not isinstance(question, str) or not question.strip():
            return problem(400, "VALIDATION", "question is required")
        if len(question) > ASK_CHARS:
            return problem(400, "VALIDATION", f"question is longer than {ASK_CHARS} characters")
        if asked_too_often(state, visitor(request)):
            return problem(429, "RATE_LIMIT", "too many questions in a minute", headers={"Retry-After": "60"})
        if await asyncio.to_thread(state.journal.asked_today, now()[:10]) >= ASK_PER_DAY:
            return problem(429, "DAILY_LIMIT", "the questions for today have run out")
        events, loop = asyncio.Queue(), asyncio.get_running_loop()

        def step(name):
            loop.call_soon_threadsafe(events.put_nowait, {"step": name})

        async def work():
            try:
                result = await ask_one(state, "web", None, {"id": "web", "question": question.strip()}, {}, step)
                await events.put({"answer": for_page(result)})
            finally:
                await events.put(None)

        task = asyncio.create_task(work())

        async def lines():
            while (event := await events.get()) is not None:
                yield json.dumps(event, ensure_ascii=False) + "\n"
            await task

        return StreamingResponse(lines(), media_type="application/x-ndjson", headers={"Cache-Control": "no-store"})

    @app.get("/api/about", tags=[docs.SITE], summary="Цифры базы для главной страницы", responses=docs.replies(200, example={"with_text": 45892, "in_force": 31488, "snapshot": "2026-11-06"}))
    async def about(request: Request):
        facts = request.app.state.facts
        return Json({"with_text": facts.get("with_text"), "in_force": facts.get("in_force"), "snapshot": request.app.state.system["lex_snapshot_date"]})

    @app.api_route("/logs", methods=["GET", "HEAD"], include_in_schema=False)
    def logs_page():
        return FileResponse(WEB / "logs.html", headers=PAGE_HEADERS)

    @app.api_route("/readme", methods=["GET", "HEAD"], include_in_schema=False)
    def readme_page():
        return FileResponse(WEB / "readme.html", headers=PAGE_HEADERS)

    @app.get("/api/logs/summary", tags=[docs.JOURNAL], summary="Итоги по прогонам", description="Время, ошибки, цена и оценки по каждому прогону.")
    def logs_summary(request: Request):
        return Json(request.app.state.journal.summary())

    @app.get("/api/logs/runs", tags=[docs.JOURNAL], summary="Список ответов",
             description="Фильтры в адресе: `source` (web, api, batch, app), `run_id`, `outcome` (ok, no_answer, error), `verdict` (ok, fail), `q`.")
    def logs_runs(request: Request, limit: int = 100, offset: int = 0):
        return Json(request.app.state.journal.runs(dict(request.query_params), min(limit, 300), max(offset, 0)))

    @app.get("/api/logs/runs/{row_id}", tags=[docs.JOURNAL], summary="Один ответ целиком", description="С источниками, планом поиска, токенами и ценой.", responses=docs.replies(200, 404))
    def logs_run(row_id: int, request: Request):
        found = request.app.state.journal.detail(row_id)
        return Json(found) if found else problem(404, "NOT_FOUND", "no such answer")

    @app.post("/api/logs/verdicts", tags=[docs.JOURNAL], summary="Записать оценки прогона", description="Нужен ключ. Этим пользуется `eval/run_eval.py`.",
              dependencies=[Depends(bearer)], openapi_extra=docs.VERDICTS_BODY, responses=docs.replies(200, 400, 401, 403))
    async def post_verdicts(request: Request):
        """A control run leaves its grades here, so that /logs shows them next to the answers."""
        if denied := refused(request):
            return denied
        body = await read_json(request)
        if not isinstance(body, dict) or not isinstance(body.get("run_id"), str) or not isinstance(body.get("verdicts"), list):
            return problem(400, "VALIDATION", "run_id and verdicts are required")
        return Json({"marked": await asyncio.to_thread(request.app.state.journal.mark, body["run_id"], body["verdicts"])})

    @app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)   # a checker that only asks for the headers must not get a 404 and call the site down
    def index():
        return FileResponse(WEB / "index.html", headers=PAGE_HEADERS)

    app.mount("/", StaticFiles(directory=WEB), name="web")
    return app


app = create_app()
