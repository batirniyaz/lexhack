# Implementation brief for Role 1: what the code has, what the product needs

- Author: [name], research team; prepared with Claude Code
- Date/time: 21.11 01:10
- Passport version: 0.11 (repo at commit `4eb5428`)
- Confidence: **high** for "what the code does" (read from the repo on 21.11); **medium** for the designs (proposals, Role 1 decides)
- Read together with: `research/service-catalog.md` (services M1–M16, sector packs, audit access), `research/business-model.md` (price formula)

> **For Role 1's Claude Code.** Everything below is a proposal. Rules from `CLAUDE.md` and the passport still apply: don't rename contracts (`facts.json`, `report.json`, API paths); add fields instead. New detectors are proposals until Role 1 accepts them (§5). Decisions D-008, D-009, D-010, D-013 bound every item; where an item touches a decision, it says so.

## Conclusions

1. **Already right:** the LLM only ever sees the site URL and the **public** legal documents (`llm/policy.py`), every quote is checked by code, and contradictions are computed by code (D-010, D-021). No credentials exist in the system yet, so none can leak to the LLM today.
2. **Planned in ARCHITECTURE.md but not built:** `legal/lexrag.py` (lex-rag quotes) and `legal/monitor.py` (lex.uz RSS + article hashes). `LEXRAG_URL` / `LEXRAG_API_KEY` are only read in `config.py` and reported by `/api/health`.
3. **Missing, and asked for by the team:** (a) a **project profile** (what the site or app does) that drives **lex-rag queries**, and an **AI-assisted legal review** against the acts lex-rag returns; (b) **free re-checks when a new act appears**, using the stored scan, by sector; (c) **AI provider and SDK detection**, and whether personal data reaches them masked or in plain form; (d) **sector packs**; (e) a **credential and evidence firewall** before active mode exists; (f) **scope statement and report hash**.
4. **Suggested order:** before the checkpoint only the cheap, demoable item W1 (AI providers). For the final: W2 lex-rag client, W3 project profile + legal review, W4 law-change re-check demo, W5 sector packs. After the hackathon: W6–W9.

## Data

### 1. Requirement → what the code has → gap

| # | Requirement (team) | In the code today | Gap |
|---|---|---|---|
| R1 | The LLM never receives credentials or private data | `llm/policy.py` sends `facts["site"]` + document texts only. `facts.json` stores raw `post_data` (truncated) and the HAR keeps request headers and post data (`record_har_content="omit"` drops only response bodies); the HAR is served by `GET /api/scans/{id}/har` to anyone with the id | No single "safe view" function that every prompt must go through; no redaction of HAR/`post_data` (needed before active mode, M4/M5) |
| R2 | The agent understands the project, asks lex-rag for the right acts, and checks against them | Not built. Policy analysis is the only LLM step | W2, W3 |
| R3 | When lex.uz publishes a new act, clients in the affected sector are told, and their saved context is re-checked for free | `rescore.py` re-evaluates saved scans without crawling (the cheap part exists). No monitor, no sector, no notifications | W4, W5 |
| R4 | Check AI APIs and SDKs: does personal data go to them, masked or not | `entities.yaml` has no AI providers; `analysis.py` backend patterns and `page_js.py` `INTERESTING` have none | W1 (passive), W7 (canary, active) |
| R5 | The client picks a sector; the sector decides the legal pack and the services | No sector anywhere except labels in `reference_sites.yaml` | W5 |
| R6 | Price depends on how often checks run; law-change re-checks are free | No scheduler, no per-site frequency | W8 (data model now, pricing later) |
| R7 | Audit-only access; client can verify our traffic and our report | Passive only; normal browser user agent; no report hash | W6, W9 |

### 2. Work items

Each item: goal → legal basis → design → files → done when → priority.

---

#### W1 · AI providers and SDKs (passive) — **P0, before the checkpoint (~1–2 h)**

**Goal.** Show which AI services the site talks to from the browser, where those companies are, and whether the policy names them.

**Legal basis (ZRU-547, titles read on lex.uz 21.11):** art. 15 «Трансграничная передача персональных данных», art. 27¹ (conditions for storage abroad, CMR No. 415 list), art. 22 (the policy must say who receives data), art. 25 if a health or HR chat sends special data, art. 24 if the AI decides about a person.

**Design.**
1. `backend/data/entities.yaml`: new category `ai` (add it to the header comment) and entities, `country` and `dpf` marked `NOT VERIFIED` like the others:

| Entity | Domains (host match) |
|---|---|
| OpenAI | `api.openai.com`, `chatgpt.com` |
| Microsoft Azure OpenAI | `openai.azure.com` |
| Anthropic | `api.anthropic.com` |
| Google Gemini / Vertex AI | `generativelanguage.googleapis.com`, `aiplatform.googleapis.com` |
| Mistral AI | `api.mistral.ai` |
| DeepSeek | `api.deepseek.com` |
| Cohere | `api.cohere.com`, `api.cohere.ai` |
| Groq | `api.groq.com` |
| OpenRouter | `openrouter.ai` |
| Hugging Face | `api-inference.huggingface.co`, `router.huggingface.co` |
| Yandex Cloud AI (YandexGPT) | `llm.api.cloud.yandex.net` |
| Sber GigaChat | `gigachat.devices.sberbank.ru` |
| Alibaba Qwen (DashScope) | `dashscope.aliyuncs.com` |
| Voice/speech AI | `api.elevenlabs.io`, `api.deepgram.com`, `api.assemblyai.com` |
| AI chat widgets | `chatbase.co`, `botpress.cloud`, `voiceflow.com`, `tidio.co` (category `chat` + `ai: true` flag) |

2. `scanner/analysis.py` `_BACKEND_PATTERNS`: add kinds `openai-api` (`api\.openai\.com`), `azure-openai` (`\.openai\.azure\.com`), `anthropic-api` (`api\.anthropic\.com`), `gemini-api` (`generativelanguage\.googleapis\.com`), plus SDK signatures in script bodies: `dangerouslyAllowBrowser` (OpenAI JS SDK flag for browser use), `anthropic-dangerous-direct-browser-access`, `GoogleGenerativeAI`. Same rule as today: **never store the key or token**, only the kind and the script URL.
3. `scanner/page_js.py` `INTERESTING`: add `openai|anthropic|generativelanguage|deepseek|mistral|gigachat` so inline scripts are read too.
4. New detector `ai_services` (`detectors/locality.py` or new `detectors/ai.py`, registered in `detectors/__init__.py`): evidence per AI host or backend kind, with entity, company country, `country_status()` from `legal_lists.py`, `before_consent`, and whether a form or chat on the same page collects personal data (`forms[].pd_categories`). Passive mode can't see what the user would type, so the evidence says "AI provider contacted from pages that collect: phone, name" — not "data was sent" (D-019).
5. Draft rule `backend/rules_draft/PD-AI-01.yaml`: "The site sends data from the browser to an AI provider outside the adequate-protection list", level `risk`, `verified: false`, legal basis art. 15 + 27¹. Role 2 will add quotes.
6. `detectors/documents.py`: treat category `ai` like tracking categories when checking "services the policy never names" (PD-POL-02), so an unnamed AI provider shows up.

**Done when:** a fixture `facts.json` with a request to `api.openai.com` gives a PD-AI-01 finding and a PD-POL-02 item "policy doesn't name OpenAI"; `test_rules.py` covers it; a key-like string in a script body never appears in `facts.json`.

---

#### W2 · `legal/lexrag.py` client — **P1, for the final**

**Goal.** One small client every legal feature uses (D-013: lex-rag stays an external service).

**Design.** `backend/qalqon/legal/lexrag.py`:
- `query(question: str, *, filters: dict | None = None) -> RagAnswer` → `POST {LEXRAG_URL}/v1/rag/query` with Bearer `LEXRAG_API_KEY` (verified working in ARCHITECTURE §4: art. 27¹ returned with citation and edition date in ~7 s). Map the response to `{answer, citations: [{act, article, url, edition_date, lang, text}]}`. Exact field names: from lex-rag's own API docs (Role 1 owns it).
- Disk cache like `llm/client.py` (key = question + filters + lex-rag version); timeout and a clear `LegalError` like `LLMError`.
- **Privacy rule:** questions are generic legal questions. They never contain the client's name, domain, URLs or any field values.
- First use: fill `legal_basis[].quote_uz / quote_ru / edition_date` for findings whose rule has `quote_*: null` (ARCHITECTURE §2.6 plan), marked "quote from lex-rag, not yet verified by lawyer".

**Done when:** `python -m qalqon.legal.lexrag "ZRU-547 27-1 modda"` prints the article with link and edition date; with `LEXRAG_URL` empty everything else still works.

---

#### W3 · Project profile → lex-rag → AI-assisted legal review — **P1**

**Goal (team's idea).** The agent learns what the product is and does, asks lex-rag for the acts that apply, and checks the product against those acts carefully, without credentials ever reaching the model.

**Decision boundary (D-010).** Today only the rules engine decides violations. To keep D-010, the review produces **observations for the lawyer**, shown in a separate report block, **not scored**. A lawyer can turn an observation into a YAML rule. If the team wants the review to create scored findings, that needs a new decision-log entry.

**Design.**
1. **`legal/profile.py` → `facts["project_profile"]`**, built by **code** from facts (deterministic, testable):
   - `sectors`: declared (W5) + classifier hints (card forms, appointment forms, loan calculator, catalog/cart, school words);
   - `data_categories`: union of `forms[].pd_categories`, plus `photo` / camera permission → `biometric_possible`;
   - `features`: login, registration, payments (entities Click / Payme / Uzum), chat, AI providers (W1), file upload, geolocation, Webvisor, cloud databases (`backends`);
   - `recipients`: third-party entities with company country and `country_status`;
   - `documents`: which exist; policy elements present/missing.
   - Optional short LLM summary "what this business does" from **public page titles and text only**, through the safe view below.
2. **Safe view (the credential firewall), `llm/safe_view.py`:** the **only** function allowed to build prompt input from facts. Whitelisted keys only; drops cookies, headers, storage values, `post_data`, URL query strings, HAR content, any value that looks like a token (long base64/hex, `sk-…`, JWT); replaces personal-data values with their category ("phone", "name"). Test: plant fake secrets in a fixture and assert they never appear in any prompt or cache file.
3. **Query plan, `legal/queries.py`:** deterministic templates per profile feature, so results are reproducible, e.g.
   - `biometric_possible` → "biometric data processing consent and storage in Uzbekistan (ZRU-547 art. 26, 27¹, 20)";
   - health sector → "special personal data health written consent (art. 25)";
   - bank / MFO → "bank secrecy disclosure to third parties", "automated decision objection (art. 24)";
   - e-commerce → "electronic commerce buyer personal data obligations (ZRU-792)";
   - AI provider abroad → "cross-border transfer conditions art. 27¹ part 3".
   The LLM may add at most N (e.g. 3) extra questions; every question passes the privacy rule from W2.
4. **Review, `legal/review.py`:** prompt = safe-view profile + the acts lex-rag returned. Answer schema: `[{act, article, quote, observation, evidence_refs[], status: "possible_gap" | "looks_ok" | "cannot_tell_from_outside", question_for_lawyer}]`. **Code drops every item whose quote is not found in the lex-rag text** (same technique as `policy.quote_found`). Disk-cached.
5. **Report:** new top-level `report["legal_review"]` (additive), shown under "AI-assisted legal review — not verified by a lawyer", never in the score.

**Done when:** on a cached scan with a camera upload, the review lists art. 26 / 27¹ observations with verified quotes; a planted secret never reaches the prompt; with lex-rag down the scan still finishes.

---

#### W4 · Law-change re-check, free, by sector — **P1 demo, P2 production**

**Goal (team's idea).** Crawling a site is the expensive part; re-checking a **stored** scan against a new act is cheap. So: new act → find clients in affected sectors → re-check their last stored context → tell them "affects you / doesn't / what to change", **at no charge**.

**Design.**
1. `legal/monitor.py` (planned in ARCHITECTURE §2.6): poll `https://lex.uz/ru/rss` hourly (title, link `/ru/docs/<id>`, act type, number, dates — passport §6); keep seen ids; daily article-hash diff of tracked acts (ZRU-547, CMR No. 415, CMR No. 71, Administrative Code, Criminal Code, ZRU-764, consumer protection law).
2. **Relevance:** keywords from ZRU-547 vocabulary first (personal data, consent, biometric, cross-border, operator…), then an LLM yes/no with `sectors_affected[]` and `articles_changed[]`.
3. **On a relevant act:** (a) rules citing a changed article → `verified: false` + lawyer alert (planned); (b) for every monitored site whose sector is affected: load its latest `facts.json` + `project_profile`, run W3's review with the **new act's text** from lex-rag, run `rescore` → a "law change notice" `{act, effective_date, affects: yes/no/maybe, observations, what_to_change}`.
4. **Cost:** no crawl; one cached LLM review (~$0.15) per affected site per act. This is why it can be free (pricing turn).
5. **Demo for the final (F-16):** CLI `python -m qalqon.legal.recheck --act <lex.uz url> --scans ../scans/batch-…` prints the notice for each cached site. Showing the real 2026 change (ZRU-1125, new art. 27¹) on a stored scan tells the story: "the law changed, your status changed".

**Done when:** the CLI produces notices for the cached batch without network crawling; with no relevant act it prints nothing.

---

#### W5 · Sector packs — **P1**

**Goal.** The client picks one or more sectors; the sector decides which rules and services apply (`service-catalog.md` §2).

**Design.**
- `backend/data/sectors.yaml` (draft) / `rules/sectors.yaml` (Role 2 overrides, same pattern as countries): per sector `rules: [...]`, `services_required: [M…]`, `services_recommended: [...]`, `lexrag_queries: [...]`.
- Optional rule field `sectors: [bank, mfo, …]`; a rule without it applies to everyone (backward compatible). `rules_engine.evaluate(facts)` filters by `facts["sectors"]`.
- `POST /api/scans {url, max_pages?, sectors?: [..]}` (additive); stored in `facts["sectors_declared"]`; W3's classifier writes `facts["sectors_detected"]`; a mismatch is shown, and the stricter pack applies.
- Frontend: a sector picker under the URL field (UZ/RU/EN labels).

**Done when:** the same facts give a different finding set for `sectors=[bank]` and `sectors=[ecommerce]`, and no sector = today's behavior.

---

#### W6 · Evidence and credential firewall (before any active mode) — **P2, required before M4/M5**

**Goal.** Clients give audit-only access (`service-catalog.md` §5); nothing they give ends up in logs, the HAR, the LLM, or a share link.

**Design.** Redact `Authorization`, `Cookie`, `Set-Cookie`, `X-Api-Key`-like headers and all `post_data` values in the HAR and `facts.json` before writing (keep field **names** and categories); never put canary values or test-account data into `facts` (store a hash); secrets in a separate encrypted store with expiry; `GET /api/scans/{id}/har` behind the share token or an access key; `safe_view` (W3) used by every LLM call. Test: a fixture HAR with a bearer token → no token after the scan.

---

#### W7 · AI data-flow test with canaries (active) — **P2, clients only (D-009)**

**Goal.** Answer "does personal data reach the AI provider, and is it masked?".
**Design.** Type canary values (fake name, phone, email, PINFL) into forms and chat widgets on a client's site; search requests to `ai`-category hosts for the canaries in plain, URL-encoded, base64 and SHA-256 forms (F-11). Result per provider: `plain` → finding, `hashed/masked` → OK with note, `not_sent` → OK. Server-side AI calls (backend → OpenAI) are invisible from outside: cover them via M6 (API map), M7 (questionnaire), M13 (code scan with Privado/Bearer), M9.

---

#### W8 · Monitored sites and frequency — **P2 (data model now, billing later)**

**Goal.** Monthly price depends on how often scans run; law-change re-checks (W4) are free.
**Design.** `monitored_sites` table: `site_id, owner, sectors, services[], frequency (monthly | weekly | daily), last_scan_id, next_run_at`; a scheduler runs only the ticked services at that frequency; W4 writes notices without touching the schedule. Store per-scan usage (pages, requests, LLM tokens from `policy.usage`, minutes) for P-F23.

---

#### W9 · Scope, report hash, identifiable agent — **P2**

- `report["scope"]`: pages scanned, hosts, mode, sectors, services, rules version, prompt versions, lex-rag version (additive).
- `report["sha256"]` of the canonical report + `GET /api/verify/{sha256}` → scope, date, rules version (QR in the PDF).
- Active mode only: sign agent requests (RFC 9421 HTTP Message Signatures, as Cloudflare's Web Bot Auth does) with an engagement-id header; publish our IPs and key. Passive mode keeps the normal browser user agent (ARCHITECTURE §2.1) — question 3 below.

### 3. Already-correct parts worth keeping

| What | Where | Why it matters for the new items |
|---|---|---|
| Verbatim-quote check | `llm/policy.py` `quote_found` | Reuse for lex-rag quotes in W3 |
| Disk cache by model + prompt version + input | `llm/client.py` | Makes W4 re-checks free and repeatable |
| Re-evaluation without crawl | `rescore.py` | The base of W4 |
| Backends found without storing secrets | `scanner/analysis.py` | Same rule for AI keys in W1 |
| One browser context per scan | `scanner/crawler.py` `new_context` | Isolation needed for W6 |
| Abuse limits and optional access key | `guard.py` | Extend to the HAR endpoint (W6) |

## Features for the product (§10 format)

These map the work items to the feature bank. IDs continue from `service-catalog.md` (P-F33…P-F40).

| ID | Feature | What it gives | Complexity | Who proposed | Status |
|---|---|---|---|---|---|
| P-F41 | AI provider and SDK detection (W1) + rule PD-AI-01 | New check that every jury member understands: "your site sends data to ChatGPT in the US" | S | Team idea (Role 3) | Proposal (MVP if time) |
| P-F42 | Project profile + lex-rag queries + AI-assisted legal review (W3) | The agent checks the product against the acts that apply, with verified quotes | M | Team idea | Proposal (Final) |
| P-F43 | Free law-change re-check by sector (W4) | Subscription value without extra crawl cost; F-16 demo | M | Team idea | Proposal (Final demo) |
| P-F44 | Safe view / evidence firewall (W3 step 2, W6) | No credentials or personal data in prompts, HAR or share links | S | Team idea | Proposal (before active mode) |
| P-F45 | Monitored sites with frequency (W8) | Frequency-based pricing; scheduler | M | Team idea | Proposal (Roadmap) |

## Questions for the team / contradictions with the passport

1. **D-010:** the team wants the LLM to "check things with the acts served by RAG". This brief keeps D-010 by showing the review as unscored observations for the lawyer. Should the review ever create scored findings? That needs a new decision.
2. **D-008:** an AI API key visible in a site's JavaScript (`sk-…`) is a security exposure. W1 only records "AI provider called from the browser" and never the key. Should we mention "a key is exposed" at all, or is that vulnerability reporting under D-008?
3. **Identifying our scanner:** passive scans use a normal user agent (ARCHITECTURE §2.1). Signed, identifiable traffic (W9) is proposed for active mode only. Role 2 (R-08): is an unidentified passive crawler acceptable?
4. **Company countries and DPF flags for AI providers** in W1 are `NOT VERIFIED` (same as V-19); Role 2 checks them before the pitch.
5. **lex.uz terms (V-17):** W4 polls RSS and hashes articles, which is what ARCHITECTURE §2.6 already plans; storing full new-act texts may need the Ministry of Justice access that is among the prizes.
6. **PASSPORT.md §5 / §10:** if accepted, PD-AI-01 and P-F41…P-F45 need rows there (Role 1 edits the passport).

## Sources

- Repo at commit `4eb5428` (21.11.2026): `backend/qalqon/llm/client.py`, `backend/qalqon/llm/policy.py`, `backend/qalqon/rules_engine.py`, `backend/qalqon/rescore.py`, `backend/qalqon/legal_lists.py`, `backend/qalqon/scanner/analysis.py`, `backend/qalqon/scanner/crawler.py`, `backend/qalqon/scanner/page_js.py`, `backend/qalqon/enrich/entities.py`, `backend/data/entities.yaml`, `backend/qalqon/api.py`, `backend/qalqon/guard.py`, `backend/qalqon/config.py`, `ARCHITECTURE.md` §2.6 and §4, `README.md`
- https://lex.uz/ru/docs/4396428 — ZRU-547 article titles (read 21.11.2026)
- https://lex.uz/ru/rss — lex.uz "New in legislation" feed (passport §6)
- https://www.rfc-editor.org/rfc/rfc9421 ; https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/
- https://github.com/privado-inc/privado ; https://docs.bearer.com/explanations/reports/
- `research/service-catalog.md`, `research/business-model.md`
