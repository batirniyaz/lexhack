# Qalqon — архитектура и план сборки

> Для Роли 1 (код) и технического ментора. Продукт и решения описаны в `PASSPORT.md`, здесь — как это устроено и в каком порядке собираем.
> Версия 0.1 · 20.11.2026

## 1. Общая схема

```
                ┌──────────────── frontend (React + Vite) ────────────────┐
                │  ввод URL → живая лента событий (SSE) → отчёт + карта    │
                └───────────────▲──────────────────────────┬───────────────┘
                                │ SSE / JSON               │ POST /api/scans
┌───────────────────────────────┴──────────────────────────▼──────────────────────────────┐
│ backend (FastAPI)                                                                       │
│                                                                                         │
│  1. scanner/     Playwright: обход страниц, перехват запросов, куки, формы, хуки JS      │
│        │  сырые наблюдения                                                              │
│  2. enrich/      IP→страна/ASN · домен→владелец трекера · CDN · DNS (MX/SPF)              │
│        │  факты (facts.json)                                                            │
│  3. detectors/   по одной функции на детектор из §5 паспорта → доказательства            │
│        │                                                                                │
│  4. rules/       движок: rules/*.yaml (юрист) + детекторы → находки 🔴🟡⚪ + оценка        │
│        │                                                                                │
│  5. llm/         Claude: разбор политики/оферты, сверка «написано vs делает»,            │
│        │         объяснение находки простым языком (UZ/RU)                              │
│  6. legal/       lex-rag API → цитаты · монитор lex.uz (RSS + хеши статей)               │
│        ▼                                                                                │
│  store (SQLite): scans, pages, requests, findings                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
          ▲                                             ▲
   demo-site/ (наш «нарушитель»)              lex-rag (внешний сервис, заявлен жюри)
```

**Главный принцип:** код собирает факты, правила решают, LLM только читает тексты и объясняет. Решение о нарушении никогда не принимает модель (D-010).

## 2. Компоненты

### 2.1 scanner/ — что видит браузер
- Playwright async, Chromium в фоне, новый контекст на каждый скан, локаль `uz-UZ`, обычный user-agent.
- **Обход сайта:** главная страница → внутренние ссылки того же домена + `sitemap.xml`. Сначала заходим на страницы, где в URL или тексте встречается `contact|aloqa|kontakt|register|ro'yxat|checkout|buyurtma|login|kirish|anketa`. Лимит: `MAX_PAGES=20`, глубина 2.
- **Перехват:**
  - `page.on("request")`: URL, метод, тип ресурса, `post_data`, страница-инициатор, метка времени;
  - `page.on("response")`: `response.server_addr()` даёт IP сервера, плюс статус и заголовки;
  - `record_har_path` → HAR-файл как доказательство.
- **«До согласия»:** первые 5 секунд после загрузки главной без кликов. Всё, что ушло за это время, помечается `before_consent=true`.
- **Хуки (`add_init_script`)** перехватывают вызовы `getUserMedia`, `geolocation.getCurrentPosition`, `fetch`, `XMLHttpRequest.open`, `sendBeacon` и логируют их в `window.__qalqon`.
- **Формы:** поля (`name`, `id`, `type`, `placeholder`, `label`, `autocomplete`, `pattern`, `maxlength`), `action`, `method`, чекбоксы и текст рядом с ними, `input[type=file]` с `accept`/`capture`.
- **JS-файлы:** тела скриптов → регулярки на `firebaseio.com|firebasedatabase.app|supabase.co|amazonaws.com|storage.googleapis.com|api.telegram.org|script.google.com|amocrm|bitrix24`.
- **Документы:** ссылки с текстом `maxfiylik|siyosat|политик|конфиденц|privacy|oferta|оферт|shartlar|условия` → скачиваем текст (HTML или PDF).
- **Режим 2 (только клиенты и демо-сайт):** заполнение форм канарейками и отправка, вход по сохранённой сессии (`storage_state`).

### 2.2 enrich/ — превращаем наблюдения в факты
- **Гео и ASN:** офлайн-базы DB-IP Lite (country + ASN, `.mmdb`, без регистрации). Файлы лежат в `data/geo/` и не попадают в git. ASN Cloudflare, Akamai, Fastly, CloudFront → `country="?"`, `is_cdn=true`.
- **Узбекские провайдеры:** `data/uz_asn.yaml` — Uztelecom, UNICON.UZ, Sarkor, TPS, Beeline UZ, Ucell, Uzmobile… Это наш список, пополняется.
- **Трекеры:** Disconnect `services.json` + `data/uz_services.yaml` (местные SaaS и CRM: где хранят данные) → `entity`, `category`, `company_country`.
- **DNS:** `dnspython` → MX, TXT/SPF. Сертификаты: `crt.sh` JSON (пассивно).

### 2.3 Модель фактов (`facts.json`) — контракт между scanner и detectors

```json
{
  "site": "https://example.uz", "scanned_at": "2026-11-20T19:00:00+05:00", "mode": "passive",
  "pages": [{"url": "...", "title": "...", "status": 200}],
  "requests": [{
    "url": "...", "host": "connect.facebook.net", "method": "GET", "type": "script",
    "page": "...", "ip": "157.240.1.35", "country": "US", "asn": 32934, "org": "Facebook",
    "is_cdn": false, "third_party": true, "before_consent": true,
    "tracker": {"entity": "Meta", "category": "advertising", "company_country": "US"},
    "post_fields": [], "pii_found": []
  }],
  "cookies": [{"name": "_fbp", "domain": ".example.uz", "before_consent": true}],
  "forms": [{
    "page": "...", "action": "https://api.telegram.org/bot.../sendMessage", "method": "POST",
    "action_country": "AE?", "fields": [{"name": "phone", "label": "Telefon", "pd": "phone"}],
    "consent": {"present": false, "text": null}
  }],
  "permissions": [{"api": "camera", "page": "..."}],
  "uploads": [{"page": "...", "accept": "image/*", "capture": "user", "destination": null}],
  "backends": [{"kind": "firebase", "url": "...", "region": null}],
  "dns": {"mx": ["aspmx.l.google.com"], "spf": ["include:_spf.google.com"]},
  "documents": [{"kind": "privacy", "url": "...", "lang": "uz", "text": "..."}],
  "policy": {"claims": [], "elements": {}}
}
```

### 2.4 detectors/ + rules/ — как принимается решение
- Детектор — чистая функция `detect(facts, params) -> list[Evidence]`. Её легко покрыть тестами на фикстурах.
- Правило (`rules/<ID>.yaml`, схема в §11.2 паспорта) называет детектор, уровень, правовое основание и способ исправления.
- Движок: для каждого правила вызывает детектор; если есть доказательства, создаётся находка `{rule_id, level, evidence[], legal_basis[], fix}`.
- Если у правила `verified: false`, в отчёте у находки стоит пометка «норма не подтверждена юристом».
- Оценка: 100 − 15·🔴 − 5·🟡 − 1·⚪, минимум 0.
- `rules/countries.yaml` (Роль 2, R-10) задаёт перечень «адекватных» стран по ПКМ № 415.

### 2.5 llm/ — только тексты
- `policy.py`: текст политики → JSON с полями `elements` (есть ли оператор, цели, сроки, права субъекта, трансграничная передача, контакт) и `claims` («храним в РУз», «не передаём третьим лицам», «используем Google Analytics»…). **У каждого пункта дословная цитата.** Если цитаты в тексте нет, код отбрасывает пункт (приём из lex-rag).
- `mismatch.py`: `claims` × факты → противоречия (PD-MIS-01). Сопоставление делает код, LLM только нормализует формулировки обещаний.
- `explain.py`: находка → 2–3 предложения простым языком на UZ и RU.
- Модели: `claude-sonnet-5-5` для документов, `claude-haiku-5-5` для массового скана и объяснений. Ключ — `ANTHROPIC_API_KEY` в `.env`.

### 2.6 legal/ — законы
- `lexrag.py`: клиент к API lex-rag (`POST /v1/rag/query`, Bearer). По `legal_basis` из правила достаёт актуальную цитату и ссылку. Переменные `LEXRAG_URL`, `LEXRAG_API_KEY` в `.env`.
- `monitor.py` (после чекпоинта): RSS `lex.uz/ru/rss` раз в час + ежедневная сверка хешей статей отслеживаемых актов → алерт и `verified:false` у затронутых правил.
- **lex-rag сделан до хакатона,** поэтому заявляем его жюри (п. 6.5). Его код в этот репозиторий не копируем, вызываем как внешний сервис.

### 2.7 API (FastAPI)

| Метод | Путь | Что делает |
|---|---|---|
| POST | `/api/scans` | `{url, mode}` → `{scan_id}`, скан запускается в фоне |
| GET | `/api/scans/{id}/events` | SSE: живая лента («найден трекер Meta → США») |
| GET | `/api/scans/{id}` | Итог: оценка, находки, факты |
| GET | `/api/scans/{id}/har` | Доказательства |
| GET | `/api/stats` | Обезличенная статистика батч-скана |

### 2.8 frontend/
React + Vite + TypeScript + Tailwind, один экран:
1. Поле URL и кнопка «Tekshirish».
2. **Живая лента** событий скана (SSE). Это главный вау-момент на демо.
3. Отчёт: оценка 0–100, находки по уровням со статьями и «как исправить», **карта потоков данных** (Узбекистан → страны), вкладка «доказательства».
4. Языки: узбекский (латиница) и русский.

### 2.9 demo-site/
Статичный интернет-магазин «Demo Market», специально с нарушениями. Каждое нарушение соответствует одному правилу:

| Нарушение | Правило |
|---|---|
| Meta Pixel и Google Analytics грузятся до согласия | PD-TRK-01, PD-LOC-02 |
| Форма «Buyurtma» (имя, телефон, ПИНФЛ) без согласия, отправка в `api.telegram.org` | PD-CNS-01, PD-PII-01, PD-LOC-01 |
| Страница «Selfie bilan tasdiqlash» (камера) | PD-BIO-01 |
| В политике написано «ma'lumotlar faqat O'zbekistonda saqlanadi, uchinchi shaxslarga berilmaydi» | PD-MIS-01 |
| Вебвизор / Clarity | PD-REC-01 |

ID трекеров фальшивые, реальные данные никуда не уходят, но запросы видны. Канарейки (режим 2) показываем на этом же сайте.

## 3. Структура репозитория

```
lexhack/
  PASSPORT.md  ARCHITECTURE.md  CLAUDE.md  .env.example
  backend/
    qalqon/
      api.py  store.py  config.py  scan.py      ← scan.py: CLI «python -m qalqon.scan URL»
      scanner/  crawler.py  hooks.js  forms.py  documents.py
      enrich/   geo.py  trackers.py  dns.py
      detectors/  __init__.py (реестр)  locality.py  trackers.py  forms.py  biometrics.py  backends.py  security.py
      rules_engine.py
      llm/      client.py  policy.py  mismatch.py  explain.py
      legal/    lexrag.py  monitor.py
    data/       uz_asn.yaml  uz_services.yaml  (geo/ — вне git)
    tests/      fixtures/ (facts.json)  test_detectors.py  test_rules.py
    requirements.txt
  rules/        *.yaml  countries.yaml         ← Роль 2
  frontend/
  demo-site/
  research/  pitch/                            ← Роли 2 и 3
```

## 4. План сборки

Каждый шаг заканчивается проверяемым результатом. После каждого шага: коммит → `git pull --rebase` → прочитать новый ресёрч ребят → push.

| # | Когда | Шаг | Готово, когда |
|---|---|---|---|
| 0 | 20.11 ~19:00 | Каркас: venv, requirements, `playwright install chromium`, `.env.example`, FastAPI `/health` | `uvicorn` поднимается, Chromium открывает страницу |
| 1 | до ~20:00 | **scanner**: обход + перехват + куки + IP серверов → `facts.json` | `python -m qalqon.scan https://lex.uz` печатает число страниц, запросов и сторонних хостов |
| 2 | до ~20:30 | **enrich**: гео/ASN/CDN + трекеры. **demo-site** v1 | В `facts.json` у запросов есть `country` и `tracker`; демо-сайт открывается локально |
| 3 | до 21:00 | **формы + хуки + JS-разбор**, детекторы и 3 правила (PD-LOC-01, PD-TRK-01, PD-CNS-01, пока черновые YAML) | Скан демо-сайта выдаёт 3+ находки с уровнями и оценкой |
| 4 | вечер/ночь | Батч-скан по списку сайтов от Роли 3 → `/api/stats` (обезличенно) | Есть цифра «X% из N сайтов…» |
| 5 | 21.11 10:00–11:30 | **llm**: разбор политики + PD-MIS-01; правила Роли 2 подключены | На демо-сайте находится противоречие «политика vs поведение» с цитатой |
| 6 | 11:30–13:00 | **frontend**: URL → живая лента → отчёт (без карты) | Полный сценарий в браузере за ~1 мин |
| 7 | 13:00–14:00 | README, схема, тесты детекторов, репетиция 10 минут для каждого ментора | — |
| — | **14:00** | **ЧЕКПОИНТ** | |
| 8 | после | Карта потоков, канарейки, lex-rag цитаты, монитор lex.uz, PDF-отчёт, генерация документов | Для финала |

**Что режем, если не успеваем (по порядку):** карта → PDF → DNS/crt.sh → батч. **Не режем никогда:** живой скан, находки со статьями, PD-MIS-01.

## 5. Сценарий демо (2 минуты)
1. Вводим адрес Demo Market. Живая лента: «Meta → США, до согласия», «форма: телефон и ПИНФЛ → api.telegram.org», «камера запрошена».
2. Отчёт: оценка 23/100. Находка 🔴 «Политика обещает хранить данные только в Узбекистане, а заявки уходят в Telegram» — показываем цитату из политики рядом с запросом.
3. Клик по статье: цитата ст. 27-1 с lex.uz (через lex-rag).
4. Слайд со статистикой батч-скана: «X% из N популярных сайтов передают данные за рубеж до согласия» (обезличенно).

## 6. Технические риски

| Риск | Что делаем |
|---|---|
| Защита от ботов (Cloudflare challenge) | Помечаем сайт «закрыт от проверки», клиент добавляет нас в белый список |
| IP за CDN | `country="?"`, честно пишем об этом в отчёте |
| Формы на чистом JS без `action` | Хуки `fetch`/XHR + разбор JS-файлов; полная картина — в режиме 2 |
| LLM путается на узбекском | Цитаты обязательны, без цитаты пункт отбрасывается; модель Sonnet для документов |
| Сеть на площадке | Демо-сайт работает локально; заранее записанное видео демо как запасной план |
| Время | Порядок урезания из §4 |
| Условия lex.uz (только личное использование) | В продукте храним только хеши статей, короткие цитаты и ссылки. Просим у Минюста официальный доступ к данным (это есть в призах) — V-17 |
