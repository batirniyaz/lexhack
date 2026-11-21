# Qalqon — alternative MVP architecture (proposal)

- Author: [name], research team; prepared with Claude Code
- Date/time: 20.11, evening; updated the same evening with the organizers' slides and the Ministry of Justice presentation (§0.1)
- Based on passport version: 0.1 (the repo is now at 0.4, see the box below)
- Confidence: high for the stack and structure; medium for time estimates; legal parameters of the detectors stay drafts until R-01 and R-03
- Status: **proposal for Role 1 (batirniyaz).** The team's architecture is `ARCHITECTURE.md` in the repo root. This file does not replace it

> **Read first: conflicts with passport v0.4**
> 1. **The team's architecture is the root `ARCHITECTURE.md`.** Use this file only as a list of suggestions.
> 2. **Localization rules changed.** Sections 7–8 assume `allowed_countries: [UZ]`. That is outdated: art. 27-1 was rewritten by ZRU-1125 (passport §2). Mandatory storage in Uzbekistan now covers only biometric, genetic and telecom-user data; other data may go abroad under conditions. Allowed countries come from `rules/countries.yaml` (CMR No. 415, R-10).
> 3. **Legal citations come from lex.uz;** rules, not the LLM, decide violations (D-010).
> 4. **Live feed:** v0.4 uses SSE (D-012); this file proposes polling.
> 5. **Canary form probe:** v0.4 allows it only on clients' sites with written consent, plus our demo site (D-009).
> 6. **New checks in v0.4** (PD-BIO-01, PD-LEAK-01, PD-REC-01, PD-DB-01, PD-MAIL-01) are not covered in §7.
> 7. **IDs renamed to avoid clashes:** the proposals in §19 are now P-D1…P-D5 and P-F1…P-F2, because D-008…D-013 and F-11…F-16 are already taken in the passport. Role 1 assigns real IDs to anything accepted.
>
> **Suggestions not yet in the root `ARCHITECTURE.md`, worth a look:**
> - Scanner in a separate worker process: Playwright fails under uvicorn `--reload` on Windows (§1).
> - Collect once, evaluate many times: `rescore` re-runs rules on a saved scan in a second (§2, §8).
> - Score counts triggered rules, not individual requests; "undetermined" findings don't lower the score (§8).
> - SSRF guard for the scan API (§10.4).
> - Demo site in a "bad" and a "fixed" version, plus a golden test on both (§12, §14).
> - Hackathon context and the Ministry B2G angle (§0.1), and 30-second explanations for each role (§18).

> This document describes **how** to build what `PASSPORT.md` §4–§6 (v0.1) describes, in about 20 hours before the checkpoint, with one developer working with Claude Code. It does not change any decision in passport §15. Its own proposals are listed in §19.

---

## 0. Summary

1. **One repository, two processes.** A FastAPI API and a Playwright scan worker. SQLite sits between them as both the queue and the store. No Redis, Celery or Kubernetes.
2. **Collect once, evaluate as often as you like.** A scan saves every raw fact to `scan.json`. Detectors, rules, the score and the report are recalculated from that file in about a second, without crawling the site again. When Role 2 edits a YAML rule, the report updates right away.
3. **Detectors are code; rules are YAML.** A detector finds a fact, for example "the form sends a phone number to a host in NL". A rule in `rules/*.yaml` decides whether that is a violation and at what level, and adds the article of law and the "how to fix" text.
4. **The LLM only extracts; code compares.** Claude reads the privacy policy and returns structured claims with verbatim quotes. Code checks that every quote really appears in the text. Deterministic code computes the "policy vs behavior" contradiction (PD-MIS-01). That way the demo cannot hallucinate (D-002).
5. **The demo must not fail.** The geo database is local, LLM answers are cached, and a ready-made report of the demo site opens instantly if a live scan fails.

### 0.1 Hackathon context and what it means for the build

Sources: the organizers' slides (scoring criteria, checkpoint processing, the post-checkpoint schedule) and the Ministry of Justice infographic `taqdimot.pdf` shown at the hackathon.

| Fact | What it means for us |
|---|---|
| Each mentor scores 5 criteria from 1 to 10. Final score = (Technical + Business + Legal) / 3 | Tech is only a third of the score. The build must also feed the other two thirds: batch statistics for B1, legal citations in every finding for S1/S4, generated fix documents for S3. Don't spend hours polishing infrastructure |
| Checkpoint scores are processed on 21.11, 17:00–17:30. Results come out at 19:00 in the "LexHackathon" Telegram group. The top 10 of each of the two legal tracks (20 teams) go to the final | Matches passport §9.1. After the checkpoint we only have 19:00–22:00 and the morning of 22.11, so post-checkpoint scope stays small (§16) |
| T4 "team knowledge" is scored | Every team member must be able to explain the system in 30 seconds. Scripts are in §18 |
| The Ministry's legal service centers run the "E-huquqshunos" system. They serve 21,292 organizations, including schools, kindergartens and polyclinics. Since 2021 they have built 600+ document templates, automatic document drafts and 10+ system integrations | A natural B2G pilot: the centers' lawyers could check the websites of the organizations they already serve, many of which may collect children's and patients' data. For the architecture this means: API-first with OpenAPI (already in §10), scans grouped per client (P-F1 in §19), and document generation built from templates (§9.4), not free-form LLM text |
| "E-qaror" is integrated with 19 information systems. "Yurist-adliya" is integrated with diplom.edu.uz and my.mehnat.uz | The Ministry thinks in integrations. Our answer for the "pilot in Ministry systems" prize: a REST API and webhooks that another system can call (P-F2 in §19) |

- These numbers come from the organizers' presentation, not from lex.uz. They can be quoted in the pitch with the source "LexHackathon 2026 presentation, Ministry of Justice".
- The legal acts on the slide must be checked on lex.uz before we cite them (D-006): Presidential resolutions PQ-5168 (29.06.2021) and PQ-173 (18.03.2022), Cabinet of Ministers resolutions VMQ-218 (14.04.2020) and VMQ-390 (22.06.2021).
- D-003 still applies. We don't scan or name these organizations' websites in the demo. The pilot idea is about checking sites under an agreement.

---

## 1. Diagram

```
 User's browser
   │  React SPA (built to static files, served by the same FastAPI)
   ▼
┌──────────────────────────────┐        ┌────────────────────────────────────────────┐
│ API  · FastAPI · uvicorn     │        │ WORKER · python -m backend.worker           │
│                              │ SQLite │                                            │
│ POST /api/scans  → queued    │◄──────►│ takes a queued scan and runs the pipeline: │
│ GET  /api/scans/{id}         │  (WAL) │                                            │
│ GET  /api/scans/{id}/report  │        │ 1 COLLECT  scanner/  Playwright    ~30–45 s│
│ POST /api/scans/{id}/rescore │        │ 2 ENRICH   enrich/   geo, CDN, trackers ~1 s│
│ frontend static, screenshots │        │ 3 READ     llm/      policy (cached) 10–25 s│
└──────────────────────────────┘        │ 4 EVALUATE detectors/ + rules_engine/  <1 s│
                                        └───────────────┬────────────────────────────┘
                                                        ▼
                         data/scans/<id>/  scan.json · llm.json · report.json
                                           screenshots/*.png · trace.har · manifest.json
```

- Steps 1–3 do I/O: network, browser, API. Step 4 is pure functions with no network, so it can be re-run at any time (`rescore`).
- Step 3 can start as soon as the policy text is found, in parallel with crawling the remaining pages. That is a later optimization.

### Why the worker is a separate process
- Playwright starts the browser as a subprocess. On Windows that needs `ProactorEventLoop`, but uvicorn with `--reload` switches to `SelectorEventLoop`, which does not support subprocesses. Playwright then fails with `NotImplementedError`. A separate process avoids the problem. Source: the asyncio documentation for Windows (§21).
- A browser crash does not take down the API.
- The same scan code runs from the CLI for the top-100 batch scan (F-03).

---

## 2. Architecture principles

| # | Principle | What it gives us at the hackathon |
|---|---|---|
| P1 | A monolith of two processes + SQLite | No infrastructure; everything runs on a laptop |
| P2 | Collection is separate from evaluation | Rescore in a second. Detectors are written and tested on a fixture before the scanner is ready. The overnight batch does not need re-running after a rule change |
| P3 | Contracts first (`backend/core/models.py` + JSON fixtures) | Scanner, detectors and frontend can be built in parallel in separate Claude Code sessions |
| P4 | Detector = code, rule = YAML | Role 2 changes levels, parameters and texts without a programmer (§13: "what if the law changes?") |
| P5 | The LLM extracts with quotes; code draws the conclusion | Reproducible, no hallucinations, easy to explain to the mentor (T3) |
| P6 | Honesty is built into the data: `certainty: confirmed / undetermined` | These are "signs of violation" (D-004). Behind a CDN the country is "undetermined" (§4) |
| P7 | Demo safety | Local geo database, LLM cache, report replay, time limit per scan |

---

## 3. Repository layout

This refines passport §6. New folders are marked NEW.

```
lexhack/
  PASSPORT.md  CLAUDE.md  ARCHITECTURE.md  README.md
  pyproject.toml                ← Python dependencies; all commands run from the root
  .env.example
  backend/
    core/                       ← NEW: shared by all modules
      models.py                 ← data contracts (§4); change only by agreement
      config.py                 ← settings from .env (pydantic-settings)
      db.py                     ← SQLite: tables scans, llm_cache
      storage.py                ← paths data/scans/<id>/…, JSON writing, manifest with SHA-256
      catalog.py                ← loads reference data from catalog/
    scanner/
      browser.py                ← Chromium launch, context, HAR
      crawl.py                  ← phases A–E (§5), time limit
      network.py                ← request/response capture → RequestRecord
      consent.py                ← find the consent banner and click it
      forms.py                  ← form extraction + "canary" probe
      policy.py                 ← find and extract privacy policy and offer text
      links.py                  ← choose the next pages to crawl
    enrich/                     ← NEW: geo, CDN, trackers, personal-data field classification
      hosts.py  geo.py  cdn.py  trackers.py  pd_fields.py
    llm/
      client.py                 ← Anthropic SDK wrapper + cache
      policy_extract.py         ← main call: policy items + claims
      quotes.py                 ← verbatim quote verification
      fixes.py                  ← (Final) document generation, F-04
      prompts/policy_extract_v1.md
    detectors/
      __init__.py               ← registry @detector("name")
      facts.py                  ← shared computations: foreign recipients, form destinations…
      form_submit_destination.py   foreign_requests.py      site_hosting_country.py
      trackers_before_consent.py   form_consent.py          form_pd_fields.py
      privacy_policy_present.py    policy_content.py        policy_vs_behavior.py
      https.py                     security_headers.py
    rules_engine/
      schema.py                 ← pydantic model of the YAML schema in §11.2
      loader.py                 ← load and validate rules/*.yaml
      engine.py                 ← rule → detector → Finding
      scoring.py                ← score 0–100
      report.py                 ← builds the Report and the flows for the map
    api/
      main.py  routes_scans.py  routes_stats.py  security.py (SSRF guard)
    pipeline.py                 ← collect → enrich → llm → evaluate (one function)
    worker.py                   ← loop: take queued → pipeline
    cli.py                      ← scan / evaluate / batch / stats / validate-rules
    tests/
      fixtures/  scan_demo.json  llm_demo.json  report_demo.json
      test_detectors.py  test_rules.py  test_golden_demo.py
  catalog/                      ← NEW: reference data; non-programmers edit it too
    trackers.yaml               ← domains → company, jurisdiction, category
    services_uz.yaml            ← Uzbek services (our moat against competitors, §6)
    cdn_asn.yaml                ← ASNs of CDN providers
    pd_fields.yaml              ← personal-data field dictionaries in uz / ru / en
    consent_patterns.yaml       ← consent button and banner texts
    policy_items.yaml           ← list of required policy items (owner: Role 2)
  rules/                        ← Role 2, schema §11.2; plus _scoring.yaml with weights
  frontend/                     ← React + Vite + TypeScript
  demo-site/
    bad/   fixed/               ← "before" and "after" for the demo
  scripts/  dev.ps1  dev.sh  get_geo_db.py  warm_demo.py
  data/                         ← in .gitignore: qalqon.db, geo/*.mmdb, scans/<id>/
  research/  pitch/
```

---

## 4. Data contracts

This is the main seam between modules. `backend/core/models.py` is created in the first hour. Adding fields is fine; renaming or removing them needs agreement. Abridged:

```python
from typing import Any, Literal
from pydantic import BaseModel

Phase = Literal["before_consent", "after_consent", "crawl", "form_probe"]
Certainty = Literal["confirmed", "undetermined"]
Level = Literal["violation", "risk", "recommendation"]          # 🔴 🟡 ⚪
PdCategory = Literal["name", "phone", "email", "passport", "pinfl",
                     "birthdate", "address", "card", "other"]

# ---------- 1. COLLECT + 2. ENRICH  →  scan.json ----------
class RequestRecord(BaseModel):
    id: int
    url: str
    host: str
    site: str                       # eTLD+1 (tldextract): tells first-party from third-party
    method: str
    resource_type: str              # document, script, xhr, fetch, image, ping…
    phase: Phase
    page_url: str
    t_ms: int                       # milliseconds since scan start
    status: int | None = None
    failed: bool = False            # the request happened but did not finish (offline, blocked) — still evidence
    aborted_by_us: bool = False     # we cancelled it during the form probe
    server_ip: str | None = None    # from Response.server_addr()
    third_party: bool
    id_params: list[str] = []       # identifiers found: _ga, cid, fbp, _ym_uid, uid…
    has_cookie_header: bool = False
    carries_form_data: bool = False # the form-probe "canary" was found in the URL or body

class CookieRecord(BaseModel):
    name: str
    domain: str
    phase: Phase
    third_party: bool
    expires_days: float | None
    tracker_id: str | None          # _ga → google_analytics (via catalog/trackers.yaml)

class FormField(BaseModel):
    name: str | None
    input_type: str
    label: str | None
    placeholder: str | None
    pd_category: PdCategory | None

class FormRecord(BaseModel):
    id: str
    page_url: str
    action: str | None
    method: str
    fields: list[FormField]
    has_consent_checkbox: bool
    consent_text: str | None
    policy_link: str | None
    probed: bool = False
    destinations: list[str] = []    # hosts the browser tried to send the form data to
    screenshot: str | None

class HostInfo(BaseModel):
    host: str
    ip: str | None
    server_country: str | None      # ISO-2 from the IP; None if unknown; "LOCAL" for private IPs
    asn: int | None
    as_org: str | None
    is_cdn: bool = False
    company: str | None = None      # from catalog/trackers.yaml or services_uz.yaml
    company_country: str | None = None   # recipient's jurisdiction
    category: str | None = None     # analytics, advertising, chat, crm, payments, hosting, cdn…
    geo_source: Literal["server_addr", "dns", "catalog", "none"]

class PolicyDoc(BaseModel):
    url: str
    kind: Literal["privacy", "offer", "cookies"]
    text: str
    chars: int
    sha256: str

class ConsentInfo(BaseModel):
    banner_found: bool
    banner_text: str | None
    accept_clicked: bool

class PageRecord(BaseModel):
    url: str
    status: int | None
    title: str | None
    kind: str                       # home, policy, offer, contact, checkout, other
    screenshot: str | None

class ScanData(BaseModel):
    scan_id: str
    target_url: str
    final_url: str
    site: str
    started_at: str
    finished_at: str
    scanner_version: str
    options: dict[str, Any]
    pages: list[PageRecord]
    requests: list[RequestRecord]
    cookies: list[CookieRecord]
    local_storage_keys: list[str]
    forms: list[FormRecord]
    hosts: dict[str, HostInfo]      # filled by enrich/
    policies: list[PolicyDoc]
    consent: ConsentInfo
    main_response_headers: dict[str, str]
    errors: list[str]

# ---------- 3. READ (LLM)  →  llm.json ----------
class Quote(BaseModel):
    text: str
    verified: bool = False          # set by llm/quotes.py, never by the model

class PolicyItem(BaseModel):
    key: str                        # key from catalog/policy_items.yaml: operator, purposes, retention…
    present: bool
    quote: Quote | None

class PolicyClaim(BaseModel):
    kind: Literal["storage_location", "cross_border", "third_parties", "cookies_analytics"]
    value: str                      # only_uz | denied | none | not_used | allowed | unspecified
    countries: list[str] = []
    parties: list[str] = []
    quote: Quote

class PolicyExtraction(BaseModel):
    policy_url: str
    model: str
    prompt_version: str
    items: list[PolicyItem]
    claims: list[PolicyClaim]

# ---------- 4. EVALUATE  →  report.json ----------
class Evidence(BaseModel):
    kind: Literal["request", "cookie", "form", "header", "policy_quote", "screenshot", "host"]
    ref: str                        # request id, cookie name, form id, file path
    text: str                       # technical and language-neutral: "POST api.telegram.org → NL · +14.2 s"

class Hit(BaseModel):               # what a detector returns
    subject: str                    # dedup key: host, form id…
    facts: dict[str, Any]           # {"host": …, "country": "NL", "fields": ["phone"]}
    evidence: list[Evidence]
    certainty: Certainty = "confirmed"

class Finding(BaseModel):           # detector + rule
    rule_id: str
    level: Level
    title: dict[str, str]           # {"ru": …, "uz": …}
    hits: list[Hit]
    certainty: Certainty            # undetermined if all hits are undetermined
    legal_basis: list[dict]
    sanction: str | None
    fix: dict[str, str]
    rule_verified: bool             # `verified` from the YAML: "legal basis confirmed by Role 2"

class Flow(BaseModel):              # one country on the map
    country: str | None             # None = "undetermined"
    hosts: list[str]
    companies: list[str]
    data: list[Literal["form_pd", "identifiers", "page_visit"]]
    worst_level: Level | None

class Report(BaseModel):
    scan_id: str
    url: str
    score: int
    counts: dict[str, int]          # violation / risk / recommendation
    findings: list[Finding]         # confirmed
    undetermined: list[Finding]     # "needs review" block
    flows: list[Flow]
    policy_vs_behavior: list[dict]  # {claim, quote, contradicting_evidence[]}
    limitations: list[str]          # limits from passport §4, added automatically
    rules_version: str              # sha256 of the rules/ folder
    generated_at: str
```

---

## 5. Scanner (`backend/scanner/`)

### 5.1 Phases of one scan

| Phase | What we do | What we record |
|---|---|---|
| **A. First visit** | Fresh context with no cookies. Open the URL, wait for `load` plus up to 5 s of network quiet. **Click nothing.** | All requests with `phase=before_consent`, cookies, localStorage keys, document response headers, a screenshot |
| **B. Consent** | Find the banner using `catalog/consent_patterns.yaml` ("Принять", "Qabul qilish", "Roziman", "Accept", "Согласен"…), click "accept", wait 3 s | `consent.*`, new requests with `after_consent` |
| **C. Crawl** | Up to `max_pages` internal pages (demo: 8, batch: 3–5), 3 tabs in parallel. Order: policy and offer → contact, order, sign-up, cart → everything else | `crawl` requests, pages, forms |
| **D. Policy** | Links matching patterns (privacy, konfidensial, maxfiylik, политика, оферта, offer, shartnoma) plus guessed paths `/privacy`, `/policy`. Text = `innerText` of the main content | `policies[]` |
| **E. Form probe** | For forms with personal-data fields: fill them with "canaries", press submit, **intercept and cancel** every request that contains a canary | `forms[].destinations`, `form_probe` requests with `aborted_by_us=true` |

### 5.2 The "canary" form probe — the key technical feature
- Each scan generates a unique token, for example `qq7f3a`. It fills text fields and the email (`qq7f3a@qalqon.test`); the phone gets a fixed test number with recognizable digits.
- `page.route("**/*", handler)`: if the token appears in the URL or the request body (raw, URL-decoded or base64-decoded), we record the request and call `route.abort()`. All other requests go through with `route.continue_()`.
- The result: we see **where the browser would send the data** (the site's own backend, a Telegram bot, a foreign CRM), but **nothing is sent** — not to the site owner and not to third parties.
- Bonus: the same mechanism catches scripts that send typed values before the button is pressed (session recorders, "webvisor"-style tools). If they compress the data we won't see the canary, and we state that limitation openly.
- By default `probe_forms=true` only for the demo site and for clients under contract. **It is off in the batch scan**: there we only look at the static `action` (question for R-08).

### 5.3 Network and identifiers
- Requests are recorded on the `request` event, not only on the response. That way failed and offline requests count as evidence too. `requestfinished` adds the status and `server_addr()`; `requestfailed` sets `failed=true`.
- Identifiers are searched in query keys and in the body using the `id_params` list from `catalog/trackers.yaml`: `_ga`, `cid`, `fbp`, `_fbp`, `fbc`, `_ym_uid`, `uid`, `gclid`, `yclid`, `client_id`…
- `site` and `third_party` are computed with `tldextract` using its bundled public-suffix snapshot (`suffix_list_urls=()`) so it works offline.

### 5.4 Evidence (basis for F-06)
- Screenshots of the home page (full page) and of every form with personal data.
- HAR via `record_har_path`, without response bodies (`record_har_content="omit"`) to keep the file small.
- `manifest.json`: start and end time, scanner version, SHA-256 of every file. For a lawyer this shows the files were not altered.

### 5.5 Reliability
- Overall scan limit `SCAN_TIMEOUT_S=90`, 15 s per navigation. On timeout we keep what we have and write the error to `errors`. If the home page loaded, the scan does not count as failed.
- Regular Chromium, `locale="ru-RU"`, `timezone_id="Asia/Tashkent"`, a calm pace. We never bypass CAPTCHAs. If a site blocks us we say so plainly: "the site restricted automated access". Clients can allowlist us (§13).
- Forms without a `<form>` tag (common in SPAs): group input fields around a submit button.

---

## 6. Enrichment (`backend/enrich/`)

### 6.1 How we determine a host's country — the chain
1. `server_ip` from `Response.server_addr()` — the real IP the browser connected to.
2. If there is no response (the request failed or we cancelled it), use DNS: `socket.getaddrinfo`.
3. IP → country and ASN from a local mmdb database: GeoLite2 Country + ASN. Without a MaxMind key, DB-IP Lite works in the same format. Both are read with the `maxminddb` library, work offline, and a lookup takes microseconds.
4. If the ASN is in `catalog/cdn_asn.yaml`, set `is_cdn=true` and `server_country=None` ("undetermined").
5. If the host is in `catalog/trackers.yaml` or `services_uz.yaml`, add `company` and `company_country` — the recipient's jurisdiction. This works offline and behind a CDN.

**"Foreign recipient" rule** (`detectors/facts.py`): `server_country ∉ allowed` **or** `company_country ∉ allowed`. Status is `confirmed` if at least one of the two is known, `undetermined` if both are `None`. The UI always shows both values as "server: <country by IP> · company: <name> (<jurisdiction>)". Jurisdictions in the catalog are filled in only with a source, see §6.2.

During the crawl, enrichment runs for each new host as it appears. That lets the progress screen show "countries found: 4" live.

### 6.2 Tracker and service catalog

```yaml
# catalog/trackers.yaml
- id: meta_pixel
  company: "Meta Platforms, Inc."
  company_country: US
  category: advertising
  domains: [facebook.com, facebook.net]        # matched by host suffix
  cookies: [_fbp, _fbc]
  id_params: [fbp, fbc]
  source: "https://…"                            # proof of ownership; without a source, verified: false
  verified: false
```

- To start, add about 30 of the most common trackers and widgets by hand: Google Analytics/GTM/Ads, Meta, Yandex Metrica, VK, TikTok, Hotjar, Microsoft Clarity, Jivo, Tawk.to, Bitrix24, amoCRM, Telegram Bot API and others. **Each company's jurisdiction is filled in only with a source.**
- `services_uz.yaml` — local payment services, SMS gateways, hosting providers and CRMs, with `company_country: UZ` and `stores_in_uz: true | unknown`. Role 3 or Role 2 fill it, with sources. This is the "database of local services" from passport §6 and §8.
- The long tail comes later, from DuckDuckGo Tracker Radar. Its license is CC BY-NC-SA, so commercial use is **NOT VERIFIED**: the MVP uses only our own catalog.

### 6.3 Personal-data field classification
Regex dictionaries in uz / ru / en in `catalog/pd_fields.yaml`, matched against `name`, `id`, `label`, `placeholder`, `autocomplete` and `type`. Examples: `pinfl: [pinfl, jshshir, жшшир, пинфл]`, `passport: [passport, pasport, паспорт, seriya]`, `phone: [type=tel, phone, telefon, тел]`. Simple and explainable; no LLM needed here.

---

## 7. Detectors (`backend/detectors/`)

### 7.1 Interface

```python
# backend/detectors/__init__.py
from typing import Callable
from pydantic import BaseModel
from backend.core.catalog import Catalog
from backend.core.models import Hit, PolicyExtraction, ScanData

class EvalContext(BaseModel):
    scan: ScanData
    policy: PolicyExtraction | None    # None — no policy, or the LLM was unavailable
    catalog: Catalog

REGISTRY: dict[str, Callable[[EvalContext, dict], list[Hit]]] = {}

def detector(name: str):
    def wrap(fn):
        REGISTRY[name] = fn
        return fn
    return wrap

# backend/detectors/trackers_before_consent.py
@detector("trackers_before_consent")
def run(ctx: EvalContext, params: dict) -> list[Hit]:
    ...
```

Rules for detectors: **pure functions**, no network and no files. A detector never calls another detector: shared computations live in `facts.py`. Every detector has a test on the fixture.

### 7.2 Detector catalog (matches passport §5)

| Detector | Rule | Logic | YAML parameters (Role 2 decides) | When `undetermined` |
|---|---|---|---|---|
| `form_submit_destination` | PD-LOC-01 | Forms with personal-data fields → `destinations` (after the probe) or `action` (without it) → foreign recipient per §6.1 | `allowed_countries: [UZ]`, `pd_categories: [...]` | CDN with no catalog entry; probe off and the action points to the site's own domain |
| `foreign_requests` | PD-LOC-02 | Third-party requests to foreign recipients, grouped by company and host | `allowed_countries`, `require_identifier: true` — count only requests carrying identifiers or cookies. This is the direct answer to V-08 | Country and company both unknown |
| `site_hosting_country` | PD-HOST-01 | Server of the main document → country | `allowed_countries` | CDN; `LOCAL` |
| `trackers_before_consent` | PD-TRK-01 | Requests to catalog trackers and their cookies in phase A. If there is no banner, add the fact "no consent mechanism found" | `categories: [advertising, analytics]` | — |
| `form_consent` | PD-CNS-01 | A personal-data form with no consent checkbox and no consent text nearby | `min_pd_fields: 1`, `accept_text_only: false` — whether "by clicking the button you agree…" counts | — |
| `form_pd_fields` | PD-PII-01 | Fields from sensitive categories are present | `sensitive: [passport, pinfl, birthdate, card]` | — |
| `privacy_policy_present` | PD-POL-01 | No `policies` entry with `kind=privacy` | — | The crawl stopped early |
| `policy_content` | PD-POL-02 | A required item has `present=false` | `required_items: [operator, purposes, retention, subject_rights, cross_border, …]` | The item exists but its quote failed verification |
| `policy_vs_behavior` | PD-MIS-01 | Deterministic comparisons (§7.3) | `checks: [storage_vs_flows, third_parties_vs_trackers, …]` | Never: no verified quote means no finding |
| `https` | SEC-01 | Home page not on HTTPS; no http→https redirect; a form posts to `http://`; mixed content | `ignore_hosts: []` | — |
| `security_headers` | SEC-02 | Missing HSTS, CSP, X-Content-Type-Options, X-Frame-Options or frame-ancestors, Referrer-Policy | `required: [...]` | — |

### 7.3 PD-MIS-01 — "the policy contradicts the site's behavior"

| Policy claim (extracted by the LLM, quote verified) | Behavior fact (`facts.py`) | Result |
|---|---|---|
| `storage_location = only_uz` | Form data goes to a foreign recipient, or identifiers go to foreign companies | contradiction |
| `cross_border = denied` | same | contradiction |
| `third_parties = none` | There are third-party recipients: trackers, CRM, chat | contradiction |
| `cookies_analytics = not_used` | There are analytics cookies or requests | contradiction |
| the policy doesn't mention it | trackers are present | **not** a contradiction — it's a missing item (PD-POL-02) |

Each finding is a pair: "quote from the policy" and "list of evidence". The rule sets the level. If Role 2 wants different levels for different comparisons, they create two rules (PD-MIS-01 and PD-MIS-02) with the same detector and different `checks`.

---

## 8. Rules engine and scoring (`backend/rules_engine/`)

- **loader:** reads `rules/*.yaml` and validates them against the §11.2 schema. On startup it fails with a clear error for an unknown detector, an invalid `level`, or missing ru or uz text. This is the safeguard against "invented detectors". Check with `python -m backend.cli validate-rules`.
- **engine:** `for rule in rules: hits = REGISTRY[rule.detector](ctx, rule.params)`. If `hits` is not empty, one `Finding` is created per rule, holding all its hits.
- **Score (refines the §5 draft):** start at 100. Per **triggered rule**, not per request: 🔴 −15, 🟡 −5, ⚪ −1, minimum 0. `undetermined` findings **do not** lower the score; they appear in a "needs review" block. Otherwise 40 requests to one tracker would zero the score, and a CDN would be penalized for something we don't know. Weights live in `rules/_scoring.yaml`, and Role 2 can change them.
- **Rules version:** `rules_version` is the SHA-256 of the contents of `rules/`. It goes into the report so the report is reproducible.
- **Draft rules:** from the first hour, Role 1 adds draft YAML files for all 11 checks (`verified: false`, `legal_basis: []`) so the pipeline works. Role 2 completes them. In the UI a rule with `verified: false` gets a "legal basis being confirmed" badge, and we claim nothing (§14).
- **Rescore:** `POST /api/scans/{id}/rescore` and `python -m backend.cli evaluate data/scans/<id>` re-run only step 4.

---

## 9. LLM layer (`backend/llm/`)

### 9.1 One main call per policy
- **Input:** the whole policy text. The model's context is 1M tokens, so no chunking and no silent truncation. There is a 200k-character cap, and the report says so if it is exceeded.
- **System prompt:** instructions plus the item list from `catalog/policy_items.yaml` and the claim types. It is static, so it gets cached.
- **Output:** `PolicyExtraction` via structured outputs (`messages.parse` + a pydantic model). The schema guarantees valid JSON.
- **Rules in the prompt:** a quote is copied character for character, in the original language. If an item is missing, then `present=false` and no quote. Infer nothing.

```python
# backend/llm/policy_extract.py — skeleton
import anthropic

client = anthropic.Anthropic()               # key from ANTHROPIC_API_KEY

resp = client.beta.messages.parse(
    model=settings.llm_model,                # "claude-sonnet-5-5"; batch: "claude-haiku-5-5"
    max_tokens=16000,
    system=SYSTEM_PROMPT,                    # static text + item list
    messages=[{"role": "user",
               "content": f'<policy url="{doc.url}">\n{doc.text}\n</policy>'}],
    output_format=PolicyExtractionLLM,       # pydantic model without the verified / model fields
    betas=["server-side-fallback-2026-07-01"],
    fallbacks="default",                     # if the model refuses, the server retries on a fallback model
)
if resp.stop_reason == "refusal":
    return None                              # the report shows "AI analysis unavailable"
extraction = resp.parsed_output
```

The server-side fallback is enabled following Anthropic's guidance for Sonnet 5.5. If you don't want it, or the installed SDK doesn't support it, switch to `client.messages.parse` without `betas` and `fallbacks`.

### 9.2 Hallucination safeguards
1. `quotes.verify()`: normalize the text (whitespace, quotes «»“”, Uzbek Latin apostrophes ʻ ‘ ’ → ', case) and check for an exact match. Fallback: `rapidfuzz.partial_ratio ≥ 95`. If the check fails, set `verified=false`.
2. An item whose quote is unverified → `undetermined`. A claim whose quote is unverified **does not take part** in PD-MIS-01.
3. Code, not the model, decides whether there is a contradiction (§7.3).

### 9.3 Cache, models, resilience
- **Cache:** key = `sha256(policy text + model + prompt version + item-list hash)` in the `llm_cache` table. A repeat scan is instant, and the demo gives the same result every time.
- **Models (passport §6):** `claude-sonnet-5-5` for live scans, `claude-haiku-5-5` for the batch. Tune the `effort` parameter on the demo policy and 3 real ones: start at `low` so a scan fits in a minute.
- **If the LLM is unavailable** (no key or network, refusal, error): `policy=None`, the `policy_*` detectors stay silent, and the report says "AI policy analysis unavailable; rule-based checks completed". This backs up the §13 answer to "Do you depend on Claude?".
- **Cost per scan, for B4 (Role 3):** at Anthropic's prices as of 03.11.2026, Sonnet 5.5 costs $2 per 1M input tokens and $10 per 1M output tokens; Haiku 5.5 costs $0.10 and $0.50. A policy of about 10k tokens plus about 2k for the answer comes to roughly **$0.05 on Sonnet** and **under $0.01 on Haiku**. A cache hit is free. This is an estimate: measure it from `usage` in the responses and check against the pricing page (§21).

### 9.4 Document generation (F-04, after the checkpoint)
`llm/fixes.py`: Role 2's templates (`catalog/templates/*.md.j2`) plus the **real facts from the scan** (recipients, countries, data categories) → a draft policy and consent text in RU/UZ. The cookie-banner code is a static template, no LLM. Every document is marked "draft, to be checked by a lawyer".

---

## 10. API, worker, storage

### 10.1 Endpoints

| Method | Path | What it does |
|---|---|---|
| POST | `/api/scans` | `{url, max_pages?, probe_forms?, click_consent?}` → `{id}`. Validates the URL and the SSRF guard, queues the scan |
| GET | `/api/scans/{id}` | `{status, stage, progress: {pages, requests, third_parties, countries}, events[], error}` — the frontend polls once per second |
| GET | `/api/scans/{id}/report` | `Report`. It holds both languages; the frontend picks one |
| GET | `/api/scans/{id}/files/{path}` | Screenshots and HAR, only inside the scan's folder |
| POST | `/api/scans/{id}/rescore` | Re-runs step 4 |
| GET | `/api/scans` | Last N scans (demo menu) |
| GET | `/api/rules` | Rules with their `verified` status |
| GET | `/api/stats?batch=…` | Anonymized batch statistics (F-03) |
| GET | `/api/scans/{id}/report.pdf` | (Final) Playwright prints `/print/{id}` to PDF with `page.pdf()`. No separate PDF library |
| GET | `/health` | Checks the LLM key, geo database, catalog and rules |

Every response is declared with `response_model`, so `/openapi.json` is accurate and the frontend's TypeScript types are generated from it.

### 10.2 SQLite

```sql
PRAGMA journal_mode = WAL;
CREATE TABLE scans (
  id TEXT PRIMARY KEY, url TEXT NOT NULL,
  status TEXT NOT NULL,                 -- queued | running | done | failed
  options TEXT NOT NULL,                -- JSON
  stage TEXT, progress TEXT,            -- JSON for the progress screen
  score INTEGER, error TEXT, batch_id TEXT,
  created_at TEXT, started_at TEXT, finished_at TEXT
);
CREATE TABLE llm_cache (
  key TEXT PRIMARY KEY, model TEXT, prompt_version TEXT, response TEXT, created_at TEXT
);
```

Large data (`scan.json`, `report.json`, files) lives on disk in `data/scans/<id>/`. SQLite holds only the index and the status.

### 10.3 Worker
- Loop every 0.5 s: `BEGIN IMMEDIATE` → take the oldest `queued` → `running` → `COMMIT` → `pipeline.run()`.
- `WORKER_CONCURRENCY=2` scans at a time: one Chromium, a separate context per scan.
- On startup, every `running` scan becomes `failed` with the error "worker restarted".
- Progress: stages `opening → collecting (page x/N) → consent → forms → policy → ai → evaluating → done`, plus the last 20 events for the live feed on screen.

### 10.4 Security of our own service
- **SSRF:** http and https only. The target IP is checked: private, loopback and link-local addresses are refused unless `ALLOW_PRIVATE_TARGETS=true` (dev and the local demo site).
- Queue limit: at most 10 `queued`.
- We don't store cookie values, only names and domains. Canaries are not personal data. We don't store other people's personal data (§13).

---

## 11. Frontend (`frontend/`)

**Decision (closes the open choice in §6, proposal P-D1; passport v0.4 chose the same stack in D-012): React 18 + Vite + TypeScript + Tailwind.** No Next.js: the demo needs no SSR or SEO, and it would add a Node process and App Router complexity. Vite builds static files, FastAPI serves them — one tab and one port for the demo.

| Screen | Contents |
|---|---|
| `/` | URL field, "Check" / "Tekshirish" button, RU/UZ switch, recent scans, "Demo site" button |
| `/scan/:id` | While scanning, a live feed: "Opening the site → Collecting requests (214) → Third-party services (17) → Countries (5) → Reading the policy (AI) → Comparing". This fills the minute of waiting on stage. After `done`, the report |
| `/stats` | Anonymized top-100 statistics for the pitch (F-03) |
| `/print/:id` | Print version of the report for PDF (Final) |

**Report components:**
- `ScoreGauge` — the 0–100 score and 🔴🟡⚪ counters.
- `FlowMap` — world map. `d3-geo` + `topojson-client` + `world-atlas` (110m). Arcs run from the site to each country; color = worst level, thickness = type of data (form data or identifiers). A tooltip shows hosts and companies. Fallback if time runs out: a table of countries with flags.
- `FindingCard` — level, `certainty` badge, evidence (requests, cookies, form screenshot), legal basis (quote, lex.uz link, edition date), sanction, "how to fix" in RU/UZ, "legal basis being confirmed" badge.
- `PolicyVsBehavior` — **the main block of the demo**. Two columns: "The policy says" (verbatim quote) and "The site does" (evidence).
- `Limitations` + the disclaimer from R-08.

**Types:** `npx openapi-typescript http://localhost:8000/openapi.json -o src/api/schema.ts`. Types are never written by hand, so the frontend and backend can't drift apart.
**UI texts:** `src/i18n/ru.json` and `uz.json`. Rule texts come from the report.
**Development:** Vite proxy `/api` → `:8000`. **Demo:** `npm run build` → `frontend/dist` is mounted in FastAPI.

---

## 12. Demo site (`demo-site/`)

A fictional shop with a clear "Qalqon training site" banner. It must not resemble any real site (D-003). Plain static files: HTML, CSS and a little JS.

| Violation in `bad/` | How it's built | What should fire |
|---|---|---|
| Trackers before consent | Real GA4, Meta Pixel and Yandex Metrica snippets with fake IDs. The banner exists, but trackers load before the click | PD-TRK-01, PD-LOC-02 |
| Order form without consent | Full name, phone, address, passport series, PINFL; no checkbox | PD-CNS-01, PD-PII-01 |
| Form data goes abroad | JS `fetch` to an external API (for example the Telegram Bot API with a fake token). The probe cancels the request, so nothing is sent | PD-LOC-01 |
| A false policy | Role 2 writes the text: "data is stored exclusively on servers in the Republic of Uzbekistan and is not shared with third parties"; no retention periods or data-subject rights | **PD-MIS-01**, PD-POL-02 |
| No security headers | — | SEC-02 |

- `fixed/` is the same site, fixed: the banner blocks trackers until consent, there is a checkbox and a policy link, no passport or PINFL fields, the form posts to the site's own domain, and the policy is complete and honest. **The demo story: "bad" ≈ 20–30 points → "fixed" ≈ 85+.**
- **Hosting:** primary is a public HTTPS static host (GitHub Pages, Netlify or similar). Fallback is local (`python -m http.server 8081` + `ALLOW_PRIVATE_TARGETS=true`). The local copy runs over http, so SEC-01 fires there, which is expected.
- How often businesses in Uzbekistan send leads to Telegram bots is **NOT VERIFIED**. The batch scan can produce that number. Don't claim it in the pitch without data.

---

## 13. Top-100 batch scan (F-03)

```powershell
python -m backend.cli batch research/top100.txt --pages 3 --no-probe-forms --concurrency 3 --model claude-haiku-5-5
python -m backend.cli stats --batch <id> --out research/uz-privacy-2026-stats.md
```

- Role 3 prepares the site list and its source. Raw scans stay in `data/`: it's in `.gitignore` and never published.
- `stats` computes **aggregates only**, with no site names (D-003): share of sites with trackers before consent, with foreign recipients of identifiers, with personal-data forms lacking consent, with no policy; top recipient jurisdictions and companies.
- Ethics (confirm in R-08): form probe off, pauses between sites, robots.txt respected.
- Time estimate: 100 sites × ~25 s / 3 workers ≈ 15 minutes. It doesn't need the night; an evening is enough.

---

## 14. Tests and quality (T2)

- `tests/fixtures/scan_demo.json` is written by hand in the first hour, then replaced with a real scan of the demo site.
- `test_detectors.py` — each detector produces the expected hits on the fixture.
- `test_rules.py` — every YAML file is valid, every detector exists, ru and uz texts are present.
- `test_golden_demo.py` — the full pipeline on `demo-site/bad` produces the expected set of `rule_id`s; on `fixed` only the expected ones fire. **Mandatory before the checkpoint.**
- `ruff` + `pytest`. GitHub Actions is optional but helps T2.

---

## 15. Running it

**.env.example**
```
ANTHROPIC_API_KEY=
LLM_MODEL=claude-sonnet-5-5
LLM_MODEL_BATCH=claude-haiku-5-5
GEO_COUNTRY_DB=data/geo/country.mmdb
GEO_ASN_DB=data/geo/asn.mmdb
DATA_DIR=data
MAX_PAGES=8
SCAN_TIMEOUT_S=90
WORKER_CONCURRENCY=2
ALLOW_PRIVATE_TARGETS=true
```

**Python dependencies:** `fastapi`, `uvicorn[standard]`, `playwright`, `pydantic>=2`, `pydantic-settings`, `pyyaml`, `maxminddb`, `tldextract`, `anthropic`, `rapidfuzz`, `jinja2`, `typer`; for development, `pytest` and `ruff`.
**Frontend:** `react`, `react-router-dom`, `tailwindcss`, `d3-geo`, `topojson-client`, `world-atlas`.

```powershell
pip install -e .                       # or: uv sync
playwright install chromium
python scripts/get_geo_db.py           # downloads the mmdb files into data/geo/
cd frontend; npm install; cd ..
./scripts/dev.ps1                      # API (uvicorn --reload) + worker + Vite
```

- **Demo mode:** `npm run build`, uvicorn without `--reload`, plus the worker. Everything is available at one address, `http://localhost:8000`.
- **Docker (optional, for a VPS):** one image based on the official `mcr.microsoft.com/playwright/python` (image version = `playwright` package version), two services in compose sharing the `data/` volume.
- **The main stand is the laptop.** Only tracker requests and the LLM depend on the venue Wi-Fi. Backup: a phone hotspot.

---

## 16. Hour-by-hour build plan

Only Role 1 writes code. The contracts (§4) make it possible to run 2–3 Claude Code sessions in parallel, each in its own folder.

| Time | Stream A — scanner | Stream B — evaluation | Stream C — frontend and demo | Roles 2 and 3 |
|---|---|---|---|---|
| **20.11 17:00–18:00** | **Shared start:** repo skeleton, `pyproject.toml`, `models.py`, fixtures `scan_demo.json` and `report_demo.json`, draft `rules/*.yaml`, CLI stubs. **M0: contracts frozen** | | | Role 2: the "false" policy text for the demo. Role 3: shop copy |
| **18:00–21:00** | browser, network, crawl, `server_addr`, cookies, forms (static), policy, screenshots → `cli scan URL` | geo + cdn + `trackers.yaml` (~30), detectors PD-LOC-01, PD-TRK-01, PD-CNS-01, engine, scoring → `cli evaluate` | `demo-site/bad`, report on the fixture: score, findings, map | R-01, R-02; R-04; top-100 list |
| **21:00–22:00** | **M1: integration.** API + worker + pipeline. Live scan of the demo site → 3 findings in the UI (the passport's 21:00 target) | | | |
| **22:00–night** | Canary form probe, banner click | Remaining detectors: HOST-01, LOC-02, PII-01, POL-01, SEC-01/02 | Progress screen | Top-100 batch scan without the LLM → statistics |
| **21.11 08:00–11:00** | — | LLM: `policy_extract`, `quotes`, PD-POL-02, **PD-MIS-01** | "Policy vs behavior" block, UZ/RU | Role 2: final YAML → rescore the demo |
| **11:00–12:30** | **M2: feature freeze.** Golden test, cache warm-up (`scripts/warm_demo.py`), replay report, `demo-site/fixed` if time allows | | | Role 3: batch numbers into the pitch |
| **12:30–14:00** | Rehearsal with a "villain mentor": live scan of 3 different sites, answers from §18 | | | |
| **21.11 14:00–17:00** | **Checkpoint:** 10 minutes with each of the three mentors, one at a time. The owner of each role leads their mentor's conversation | | | |
| **17:00–19:00** | While scores are processed (17:00–17:30) and before results: start F-04 anyway. Don't wait for the announcement | | | Role 3: draft final slides |
| **19:00** | Results in the "LexHackathon" Telegram group (top 10 per track) | | | |
| **19:00–22:00** | Final prep: F-04 document generation, `demo-site/fixed` for the before/after story, PDF only if time allows | | Final demo flow: bad → report → generated fixes → fixed | Role 2: fix texts in UZ/RU. Role 3: final slides |
| **22.11 before 10:00** | Rehearsal: 3 min pitch + 2 min demo + 2 min Q&A. Code freeze, cache warm-up, replay report checked | | | |

F-05 Telegram alerts and the full F-06 evidence pack won't fit before the final. They stay on the roadmap slide (passport §10).

**What to cut if we fall behind (in order):** HAR → banner click (keep detection only) → d3 map (replace with a country table) → PD-POL-02 → form probe (keep the static `action`).
**Never cut:** live scan of any URL, PD-LOC-01, PD-TRK-01, PD-CNS-01, PD-MIS-01, the replay report.

---

## 17. Risks and fallbacks

| Risk | Likelihood | What we do |
|---|---|---|
| Venue Wi-Fi | high | Local demo site, local geo database, LLM cache, replay, phone hotspot |
| A mentor asks to scan a site that blocks bots or loads slowly | medium | 90 s limit, partial report, honest explanation about allowlisting |
| The LLM is slow or refuses | medium | Cache, `effort=low`, "AI unavailable" fallback; rule-based checks still run |
| Wrong country because of a CDN | high | `undetermined` + company jurisdiction from the catalog |
| Legal bases not ready by the checkpoint | medium | `verified: false` → "legal basis being confirmed"; we claim nothing |
| Playwright + uvicorn on Windows | high | Separate worker process (§1) |
| SPA forms without `<form>` | medium | Group inputs around the submit button |
| Frontend and backend types drift | medium | Generate types from OpenAPI |

---

## 18. Answers for the technical mentor (T1–T5)

- **T1 "Show me."** A live scan of any URL in about a minute. The report states its own limitations (passport §4).
- **T2 "The code."** Structure in §3, README, tests, `validate-rules`, the demo golden test.
- **T3 "Where's the AI?"** Claude reads the whole policy (long context, RU and UZ) and returns strict JSON against a schema. Code checks every quote is verbatim. Deterministic code computes the contradiction, so the result is reproducible and explainable. The cache keeps the demo stable. Next step: generating corrected documents from the scan's real facts.
- **T5 "Why this stack?"**
  - **Playwright:** trackers and form submissions are only visible in a real browser, `server_addr()` gives the real IP, and HAR is evidence.
  - **FastAPI:** async, pydantic, OpenAPI → frontend types.
  - **GeoLite2 / DB-IP:** offline and free.
  - **SQLite:** zero administration; we move to Postgres for multi-user mode.
  - **Claude:** structured outputs, the whole document in one request.
  - We don't train our own model (D-005).
- **Scale.** Workers scale horizontally. The queue moves to Postgres or Redis as load grows. Cost per scan: about $0.05 for the LLM (under $0.01 on Haiku) plus 30–60 s of browser time.

### T4 "team knowledge" — a 30-second explanation for each role

Each person should be able to say their version from memory, in Uzbek or Russian.

- **Role 1 (tech):** "A real browser opens the site like a visitor and records every request, cookie and form. We find out which country and which company each piece of data goes to. Rules written by our lawyer turn those facts into findings. Claude reads the privacy policy and pulls out what it promises, with exact quotes, and our code checks whether the site keeps those promises."
- **Role 2 (lawyer):** "Each check is a rule file that I edit myself. It holds the level, the article of the law with a verbatim quote from lex.uz, and the fix text in Uzbek and Russian. The code only finds facts; my rule decides whether a fact is a violation. When the law changes, I change the file and every report is recalculated."
- **Role 3 (business):** "Qalqon shows a business, in a minute, where its website really sends customers' data and whether that matches the law and its own policy. AI costs about 5 cents per scan (an estimate). Websites change all the time, so the value is in regular rescans, which is why the main revenue is a monthly subscription."

---

## 19. Proposals for the decision log (proposed IDs; Role 1 assigns real ones)

| ID | Decision | Why | Status in passport v0.4 |
|---|---|---|---|
| P-D1 | Frontend: React + Vite + TS + Tailwind, served by the same FastAPI | Closes the open choice in §6; no SSR needed; one entry point for the demo | Same stack decided in D-012 (with SSE) |
| P-D2 | Architecture "API + worker + SQLite"; collection separate from evaluation (rescore) | Development speed, parallel work, a stable demo, Windows compatibility | Not decided |
| P-D3 | The LLM only extracts items and claims with quotes; code computes PD-MIS-01; unverified quotes are discarded | D-002 "the demo doesn't hallucinate", criterion T3 | Covered by D-010 |
| P-D4 | Score counts triggered rules, not individual requests; `undetermined` doesn't lower the score | Otherwise the score depends on request counts and penalizes CDNs | Not decided |
| P-D5 | Canary form probe with the send cancelled; only for the demo and clients under contract, off in the batch | We see the real destination and send nothing (R-08) | Covered by D-009 (written consent) |

**Feature proposals for the bank of ideas (passport §10 format)** — both come from the Ministry presentation (§0.1):

| ID | Feature | What it gives | Complexity | Proposed by | Status |
|---|---|---|---|---|---|
| P-F1 | Portfolio mode: one client (a legal service center or law firm) uploads the list of domains it serves and gets a summary across all of them | A ready-made B2G pilot for legal service centers and a law-firm tier. Built on the batch scan (`batch_id` becomes the client's portfolio) | M | Role 1 | Roadmap (can be shown with the `/stats` screen) |
| P-F2 | Integration API + webhooks: documented REST API (OpenAPI) plus a webhook when new findings appear | Ministry systems, CRMs and law-firm tools can call Qalqon. Our answer for the "pilot in Ministry systems" prize | S (the API already exists) | Role 1 | Roadmap |

Also add to the structure in passport §6: `backend/core/`, `backend/enrich/`, `catalog/`, `scripts/`, `ARCHITECTURE.md`. In §5, note that detectors take parameters (`require_identifier`, `accept_text_only`, etc.) through which Role 2 answers the legal questions (V-08 and others).

---

## 20. Questions for the team

1. **Role 1:** who has the Anthropic API key, and what is the hackathon budget?
2. **Role 1:** does anyone have a MaxMind account for GeoLite2, or do we go straight to DB-IP Lite?
3. **Role 3:** where does the top-100 .uz site list come from (source for the pitch)?
4. **Role 2:** does "by clicking the button you agree…" without a checkbox count as consent (`accept_text_only`)?
5. **Role 2:** are IP addresses and cookie IDs personal data (V-08)? `require_identifier` in PD-LOC-02 depends on the answer.
6. **Role 2 (R-08):** is the canary form probe with a cancelled send acceptable on client sites? Do we respect robots.txt in the batch?
7. **Role 2:** confirm the list of required policy items in `catalog/policy_items.yaml` against the text of ZRU-547 (R-01). It's a draft for now.
8. **Everyone:** where do we host the public copy of the demo site?

---

## 21. Sources

- LexHackathon 2026 organizers' slides: scoring criteria, checkpoint processing, post-checkpoint schedule (shared in the team chat)
- Ministry of Justice infographic "Yuridik xizmatlar faoliyatini muvofiqlashtirish sohasida amalga oshirilgan ishlar" (`taqdimot.pdf`, LexHackathon 2026)

- Playwright Python, `Response.server_addr()`: https://playwright.dev/python/docs/api/class-response#response-server-addr
- Playwright Python, intercepting and aborting requests: https://playwright.dev/python/docs/network
- Playwright Python, HAR recording (`record_har_path`): https://playwright.dev/python/docs/api/class-browser#browser-new-context
- Playwright in Docker: https://playwright.dev/python/docs/docker
- asyncio on Windows (SelectorEventLoop doesn't support subprocesses): https://docs.python.org/3/library/asyncio-platforms.html#windows
- MaxMind GeoLite2: https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
- DB-IP Lite: https://db-ip.com/db/lite.php
- maxminddb library: https://github.com/maxmind/MaxMind-DB-Reader-python
- tldextract: https://github.com/john-kurkowski/tldextract
- DuckDuckGo Tracker Radar: https://github.com/duckduckgo/tracker-radar
- Anthropic, structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Anthropic, pricing: https://platform.claude.com/docs/en/about-claude/pricing
- d3-geo: https://github.com/d3/d3-geo · world-atlas: https://github.com/topojson/world-atlas
- openapi-typescript: https://github.com/openapi-ts/openapi-typescript
