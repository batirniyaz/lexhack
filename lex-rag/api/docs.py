"""What /docs shows. Only words and examples: the routes in api/main.py read and check requests themselves."""

SPEC, SITE, JOURNAL = "Проверка", "Сайт", "Журнал"

DESCRIPTION = """Ответы на вопросы о законах Узбекистана по текстам lex.uz. Учебный проект, с lex.uz не связан.

**Как начать.** Нажмите **Authorize** и вставьте API-ключ без слова `Bearer`. Ключ нужен для раздела «Проверка». Разделы «Сайт» и чтение журнала работают без него.

**Порядок проверки.** `POST /v1/rag/batch`, а если пришёл `202`, то `GET /v1/rag/batch/{batch_id}`, пока статус не станет `completed`.

**Ошибки.** Всегда в одном виде: `{"error": {"code": "...", "message": "..."}}`. Сбой одного вопроса не ломает батч: у него будет свой `status` и `error`.
"""

TAGS = [
    {"name": SPEC, "description": "API из спецификации теста. Нужен ключ."},
    {"name": SITE, "description": "То, чем пользуется главная страница. Без ключа, но с лимитами."},
    {"name": JOURNAL, "description": "Данные страницы `/logs`: все ответы, время и цена."},
]

CITATION = {
    "doc_id": "lex:6257288", "doc_title": "Oʻzbekiston Respublikasining Mehnat kodeksi", "doc_type": "kodeks", "url": "https://lex.uz/docs/-6257288",
    "article": "217-modda", "part": "1-qism", "edition_date": "2026-08-07", "doc_status": "amalda", "chunk_id": "lex:6257288#art-217#p1", "ref": 1,
    "quote": "yigirma bir kalendar kundan kam boʻlmagan muddat",
}
RESULT = {
    "id": "q001", "status": "ok", "answer": "Yillik asosiy mehnat taʼtili kamida 21 kalendar kun [1].", "answer_language": "uz-Latn", "no_answer": False, "confidence": 0.95,
    "citations": [CITATION],
    "contexts": [{"rank": 1, "chunk_id": "lex:6257288#art-217#p1", "doc_id": "lex:6257288", "article": "217-modda", "text": "...", "retrieval_score": 1.0, "rerank_score": 0.83, "used_in_answer": True}],
    "debug": None, "timing": {"retrieval_ms": 2600, "rerank_ms": 0, "generation_ms": 3100, "total_ms": 5700}, "usage": {"input_tokens": 9000, "output_tokens": 400}, "error": None,
}
SYSTEM = {
    "pipeline_version": "0.1.0", "llm_model": "claude-haiku-5-5", "embedding_model": "intfloat/multilingual-e5-small", "reranker": "claude-haiku-5-5 (reads the candidates while answering)",
    "index_version": "lex-idx-2026-11-06+v667192", "lex_snapshot_date": "2026-11-06",
}
BATCH = {
    "run_id": "run-1", "batch_id": "run-1-b01", "batch_index": 1, "total_batches": 1,
    "options": {"top_k": 5, "return_contexts": True, "return_debug": False, "as_of_date": "2026-11-01", "answer_language": "auto"},
    "items": [{"id": "q001", "question": "Yillik asosiy mehnat taʼtilining eng kam muddati qancha?", "language": "uz-Latn"}],
}
BATCH_REPLY = {
    "run_id": "run-1", "batch_id": "run-1-b01", "status": "completed", "system": SYSTEM,
    "timing": {"received_at": "2026-11-06T15:00:00+05:00", "completed_at": "2026-11-06T15:00:06+05:00", "total_ms": 5800},
    "summary": {"total": 1, "ok": 1, "no_answer": 0, "error": 0}, "results": [RESULT],
}
META = {**SYSTEM, "documents": 55277, "with_text": 45892, "in_force": 31488, "chunks": 1391358, "vectors": 667192, "languages": ["uz-Latn", "uz-Cyrl", "ru"]}

CODES = {
    200: "Готово", 202: "Батч ещё считается, спросите позже через GET", 400: "Неверный запрос", 401: "Нет ключа", 403: "Неверный ключ", 404: "Не найдено",
    409: "Этот batch_id уже приходил с другим содержимым", 429: "Слишком часто, смотрите заголовок Retry-After",
}


def replies(*codes, example=None):
    """The answers of one route, for the page. The example goes under 200."""
    found = {code: {"description": CODES[code]} for code in codes}
    if example is not None:
        found[200]["content"] = {"application/json": {"example": example}}
    return found


def body(example, properties, required):
    """The request of one route. Routes take the raw body, so the page learns its shape from here."""
    schema = {"type": "object", "required": required, "properties": properties}
    return {"requestBody": {"required": True, "content": {"application/json": {"schema": schema, "example": example}}}}


TEXT, NUMBER = {"type": "string"}, {"type": "integer"}
OPTIONS = {
    "type": "object", "description": "Необязательно",
    "properties": {
        "top_k": {"type": "integer", "minimum": 1, "maximum": 50, "default": 5, "description": "Сколько контекстов вернуть"},
        "return_contexts": {"type": "boolean", "default": True},
        "return_debug": {"type": "boolean", "default": False, "description": "Показать план поиска"},
        "as_of_date": {"type": "string", "format": "date", "description": "Убирает акты, которые на эту дату ещё не вступили в силу"},
        "answer_language": {"type": "string", "enum": ["auto", "uz-Latn", "uz-Cyrl", "ru"], "default": "auto"},
    },
}
LANGUAGE = {"type": "string", "enum": ["uz-Latn", "uz-Cyrl", "ru"], "description": "Если не указан, определится сам"}
BATCH_BODY = body(BATCH, {
    "run_id": TEXT, "batch_id": {"type": "string", "description": "Повтор с тем же содержимым вернёт сохранённый результат"}, "batch_index": NUMBER, "total_batches": NUMBER, "options": OPTIONS,
    "items": {"type": "array", "minItems": 1, "maxItems": 10, "items": {"type": "object", "required": ["id", "question"], "properties": {
        "id": TEXT, "question": {"type": "string", "maxLength": 2000}, "language": LANGUAGE}}},
}, ["run_id", "batch_id", "batch_index", "total_batches", "items"])
QUERY_BODY = body({"question": "Yillik asosiy mehnat taʼtilining eng kam muddati qancha?", "options": {"top_k": 5}},
                  {"id": TEXT, "question": {"type": "string", "maxLength": 2000}, "language": LANGUAGE, "options": OPTIONS}, ["question"])
ASK_BODY = body({"question": "Yillik asosiy mehnat taʼtilining eng kam muddati qancha?"}, {"question": {"type": "string", "maxLength": 500}}, ["question"])
VERDICTS_BODY = body({"run_id": "run-1", "verdicts": [{"id": "q001", "ok": True, "why": None, "expected": "21 kalendar kun", "category": "faktik"}]},
                     {"run_id": TEXT, "verdicts": {"type": "array", "items": {"type": "object", "required": ["id", "ok"], "properties": {
                         "id": TEXT, "ok": {"type": "boolean"}, "why": TEXT, "expected": TEXT, "category": TEXT}}}}, ["run_id", "verdicts"])
