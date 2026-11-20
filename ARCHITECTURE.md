# Qalqon — architecture and build plan

> For Role 1 (code) and the technical mentor. The product and the decisions are described in `PASSPORT.md`; this file covers how it is built and in what order we build it.
> Version 0.2 · 20.11.2026 (version 0.1 translated into English, no content changes)

## 1. Overall scheme

```
                ┌──────────────── frontend (React + Vite) ────────────────┐
                │  URL input → live event feed (SSE) → report + map       │
                └───────────────▲──────────────────────────┬───────────────┘
                                │ SSE / JSON               │ POST /api/scans
┌───────────────────────────────┴──────────────────────────▼──────────────────────────────┐
│ backend (FastAPI)                                                                       │
│                                                                                         │
│  1. scanner/     Playwright: page crawl, request interception, cookies, forms, JS hooks │
│        │  raw observations                                                              │
│  2. enrich/      IP→country/ASN · domain→tracker owner · CDN · DNS (MX/SPF)             │
│        │  facts (facts.json)                                                            │
│  3. detectors/   one function per detector from passport §5 → evidence                  │
│        │                                                                                │
│  4. rules/       engine: rules/*.yaml (lawyer) + detectors → findings 🔴🟡⚪ + score       │
│        │                                                                                │
│  5. llm/         Claude: policy/offer parsing, "written vs does" check,                 │
│        │         plain-language explanation of a finding (UZ/RU)                        │
│  6. legal/       lex-rag API → quotes · lex.uz monitor (RSS + article hashes)           │
│        ▼                                                                                │
│  store (SQLite): scans, pages, requests, findings                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
          ▲                                             ▲
   demo-site/ (our "violator")                 lex-rag (external service, declared to the jury)
```

**Main principle:** code collects facts, rules decide, the LLM only reads texts and explains. The model never makes the decision about a violation (D-010).

## 2. Components

### 2.1 scanner/ — what the browser sees
- Playwright async, headless Chromium, a new context for every scan, locale `uz-UZ`, a normal user agent.
- **Site crawl:** home page → internal links of the same domain + `sitemap.xml`. We first visit pages whose URL or text contains `contact|aloqa|kontakt|register|ro'yxat|checkout|buyurtma|login|kirish|anketa`. Limit: `MAX_PAGES=20`, depth 2.
- **Interception:**
  - `page.on("request")`: URL, method, resource type, `post_data`, initiating page, timestamp;
  - `page.on("response")`: `response.server_addr()` gives the server's IP, plus the status and headers;
  - `record_har_path` → a HAR file as evidence.
- **"Before consent":** the first 5 seconds after the home page loads, with no clicks. Everything sent during that time is marked `before_consent=true`.
- **Hooks (`add_init_script`)** intercept calls to `getUserMedia`, `geolocation.getCurrentPosition`, `fetch`, `XMLHttpRequest.open`, `sendBeacon` and log them to `window.__qalqon`.
- **Forms:** fields (`name`, `id`, `type`, `placeholder`, `label`, `autocomplete`, `pattern`, `maxlength`), `action`, `method`, checkboxes and the text next to them, `input[type=file]` with `accept`/`capture`.
- **JS files:** script bodies → regexes for `firebaseio.com|firebasedatabase.app|supabase.co|amazonaws.com|storage.googleapis.com|api.telegram.org|script.google.com|amocrm|bitrix24`.
- **Documents:** links with the text `maxfiylik|siyosat|политик|конфиденц|privacy|oferta|оферт|shartlar|условия` → we download the text (HTML or PDF). The Cyrillic words in this pattern match Russian-language sites and stay as they are.
- **Mode 2 (clients and the demo site only):** filling forms with canaries and submitting them, logging in with a saved session (`storage_state`).

### 2.2 enrich/ — turning observations into facts
- **Geo and ASN:** offline DB-IP Lite databases (country + ASN, `.mmdb`, no registration needed). The files live in `data/geo/` and don't go into git. The ASNs of Cloudflare, Akamai, Fastly and CloudFront → `country="?"`, `is_cdn=true`.
- **Uzbek providers:** `data/uz_asn.yaml` — Uztelecom, UNICON.UZ, Sarkor, TPS, Beeline UZ, Ucell, Uzmobile… This is our own list, and it keeps growing.
- **Trackers:** Disconnect `services.json` + `data/uz_services.yaml` (local SaaS and CRMs, and where they store data) → `entity`, `category`, `company_country`.
- **DNS:** `dnspython` → MX, TXT/SPF. Certificates: `crt.sh` JSON (passive).

### 2.3 Fact model (`facts.json`) — the contract between the scanner and the detectors

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

### 2.4 detectors/ + rules/ — how a decision is made
- A detector is a pure function `detect(facts, params) -> list[Evidence]`. It is easy to cover with tests on fixtures.
- A rule (`rules/<ID>.yaml`, schema in passport §11.2) names the detector, the level, the legal basis and how to fix it.
- The engine calls the detector for each rule; if there is evidence, it creates a finding `{rule_id, level, evidence[], legal_basis[], fix}`.
- If a rule has `verified: false`, its finding in the report is marked "norm not confirmed by the lawyer".
- Score: 100 − 15·🔴 − 5·🟡 − 1·⚪, minimum 0.
- `rules/countries.yaml` (Role 2, R-10) sets the list of "adequate" countries under CMR No. 415.

### 2.5 llm/ — texts only
- `policy.py`: policy text → JSON with the fields `elements` (whether the policy names the operator, purposes, retention periods, data subject rights, cross-border transfer, a contact) and `claims` ("we store data in Uzbekistan", "we don't share with third parties", "we use Google Analytics"…). **Every item has a verbatim quote.** If the quote is not in the text, the code drops the item (a technique taken from lex-rag).
- `mismatch.py`: `claims` × facts → contradictions (PD-MIS-01). The code does the matching; the LLM only normalizes the wording of the promises.
- `explain.py`: finding → 2–3 plain-language sentences in UZ and RU.
- Models: `claude-sonnet-5-5` for documents, `claude-haiku-5-5` for mass scans and explanations. The key is `ANTHROPIC_API_KEY` in `.env`.

### 2.6 legal/ — laws
- `lexrag.py`: a client for the lex-rag API (`POST /v1/rag/query`, Bearer). Using a rule's `legal_basis`, it fetches the current quote and link. The variables `LEXRAG_URL` and `LEXRAG_API_KEY` go in `.env`.
- `monitor.py` (after the checkpoint): the RSS feed `lex.uz/ru/rss` every hour + a daily check of article hashes of the tracked acts → an alert and `verified:false` on the affected rules.
- **lex-rag was built before the hackathon,** so we declare it to the jury (clause 6.5). We don't copy its code into this repository; we call it as an external service.

### 2.7 API (FastAPI)

| Method | Path | What it does |
|---|---|---|
| POST | `/api/scans` | `{url, mode}` → `{scan_id}`; the scan runs in the background |
| GET | `/api/scans/{id}/events` | SSE: the live feed ("Meta tracker found → USA") |
| GET | `/api/scans/{id}` | The result: score, findings, facts |
| GET | `/api/scans/{id}/har` | Evidence |
| GET | `/api/stats` | Anonymized batch-scan statistics |

### 2.8 frontend/
React + Vite + TypeScript + Tailwind, one screen:
1. A URL field and a "Tekshirish" ("Check") button.
2. A **live feed** of scan events (SSE). This is the main wow moment of the demo.
3. The report: score 0–100, findings by level with law articles and "how to fix", a **data flow map** (Uzbekistan → countries), an "evidence" tab.
4. Languages: Uzbek (Latin) and Russian.

### 2.9 demo-site/
A static online shop, "Demo Market", built with violations on purpose. Each violation matches one rule:

| Violation | Rule |
|---|---|
| Meta Pixel and Google Analytics load before consent | PD-TRK-01, PD-LOC-02 |
| The "Buyurtma" (order) form (name, phone, PINFL) has no consent and is sent to `api.telegram.org` | PD-CNS-01, PD-PII-01, PD-LOC-01 |
| A "Selfie bilan tasdiqlash" (selfie verification) page that uses the camera | PD-BIO-01 |
| The policy says "ma'lumotlar faqat O'zbekistonda saqlanadi, uchinchi shaxslarga berilmaydi" ("data is stored only in Uzbekistan and is not passed to third parties") | PD-MIS-01 |
| Webvisor / Clarity | PD-REC-01 |

The tracker IDs are fake, so no real data goes anywhere, but the requests are visible. We show canaries (mode 2) on the same site.

## 3. Repository structure

```
lexhack/
  PASSPORT.md  ARCHITECTURE.md  CLAUDE.md  .env.example
  backend/
    qalqon/
      api.py  store.py  config.py  scan.py      ← scan.py: CLI "python -m qalqon.scan URL"
      scanner/  crawler.py  hooks.js  forms.py  documents.py
      enrich/   geo.py  trackers.py  dns.py
      detectors/  __init__.py (registry)  locality.py  trackers.py  forms.py  biometrics.py  backends.py  security.py
      rules_engine.py
      llm/      client.py  policy.py  mismatch.py  explain.py
      legal/    lexrag.py  monitor.py
    data/       uz_asn.yaml  uz_services.yaml  (geo/ — outside git)
    tests/      fixtures/ (facts.json)  test_detectors.py  test_rules.py
    requirements.txt
  rules/        *.yaml  countries.yaml         ← Role 2
  frontend/
  demo-site/
  research/  pitch/                            ← Roles 2 and 3
```

## 4. Build plan

Each step ends with a result we can check. After every step: commit → `git pull --rebase` → read the team's new research → push.

| # | When | Step | Done when |
|---|---|---|---|
| 0 | 20.11 ~19:00 | Skeleton: venv, requirements, `playwright install chromium`, `.env.example`, FastAPI `/health` | `uvicorn` starts and Chromium opens a page |
| 1 | by ~20:00 | **scanner**: crawl + interception + cookies + server IPs → `facts.json` | `python -m qalqon.scan https://lex.uz` prints the number of pages, requests and third-party hosts |
| 2 | by ~20:30 | **enrich**: geo/ASN/CDN + trackers. **demo-site** v1 | Requests in `facts.json` have `country` and `tracker`; the demo site opens locally |
| 3 | by 21:00 | **forms + hooks + JS parsing**, detectors and 3 rules (PD-LOC-01, PD-TRK-01, PD-CNS-01; draft YAML for now) | A scan of the demo site gives 3+ findings with levels and a score |
| 4 | evening/night | Batch scan over the list of sites from Role 3 → `/api/stats` (anonymized) | We have a number: "X% of N sites…" |
| 5 | 21.11 10:00–11:30 | **llm**: policy parsing + PD-MIS-01; Role 2's rules connected | A "policy vs behavior" contradiction with a quote is found on the demo site |
| 6 | 11:30–13:00 | **frontend**: URL → live feed → report (no map) | The full scenario runs in the browser in ~1 min |
| 7 | 13:00–14:00 | README, diagram, detector tests, a 10-minute rehearsal for each mentor | — |
| — | **14:00** | **CHECKPOINT** | |
| 8 | after | Flow map, canaries, lex-rag quotes, lex.uz monitor, PDF report, document generation | For the final |

**What we cut if we fall behind (in this order):** map → PDF → DNS/crt.sh → batch scan. **Never cut:** the live scan, findings with law articles, PD-MIS-01.

## 5. Demo script (2 minutes)
1. We enter the Demo Market address. Live feed: "Meta → USA, before consent", "form: phone and PINFL → api.telegram.org", "camera requested".
2. Report: score 23/100. Finding 🔴 "The policy promises to store data only in Uzbekistan, but leads go to Telegram" — we show the quote from the policy next to the request.
3. Click on the article: the quote of art. 27-1 from lex.uz (via lex-rag).
4. A slide with batch-scan statistics: "X% of N popular sites send data abroad before consent" (anonymized).

## 6. Technical risks

| Risk | What we do |
|---|---|
| Bot protection (Cloudflare challenge) | We mark the site "closed to checking"; the client adds us to their allowlist |
| IP behind a CDN | `country="?"`, and we say so honestly in the report |
| Pure-JS forms without an `action` | `fetch`/XHR hooks + JS file parsing; the full picture in mode 2 |
| The LLM gets confused by Uzbek | Quotes are mandatory, an item without a quote is dropped; the Sonnet model for documents |
| Network at the venue | The demo site runs locally; a pre-recorded demo video as a backup plan |
| Time | The cut order from §4 |
| lex.uz terms (personal use only) | In the product we store only article hashes, short quotes and links. We ask the Ministry of Justice for official data access (it is among the prizes) — V-17 |
