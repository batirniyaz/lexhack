# Qalqon — project passport

> **Working name:** Qalqon ("shield")
> **Hackathon:** LexHackathon 2026, TSUL, Tashkent, 20–22 November
> **Track:** 1 — "Huquqiy xizmatlarni ko'rsatish" (legal services)
> **Passport version:** 0.5 · 20.11.2026, 19:20
> **Document owner:** Role 1 (Tech/AI lead). Others send changes in the formats from §11.

---

## 0. Instructions for the AI assistant — read first

You are helping one of three team members. This document is the **single source of truth** for the whole team and for every AI assistant it works with. The other members' assistants read this same file, so follow the rules below. Then the results will merge without rework.

1. **The decisions in §15 "Decision log" are final.** Don't propose changing the track, the product or the business model. Frame improvements as a "Feature" (§10).
2. **Ask your person which role they have (§3),** and work on that role's tasks (§9). Ready-made tasks for you are in §9.2.
3. **Every fact needs a source (URL).** If no source is found, write `NOT VERIFIED`. Don't invent numbers, article numbers, prices or company names.
4. **Take Uzbek laws only from lex.uz.** Quote verbatim and give a link to the document and the edition date.
5. **Deliver results in the formats from §11** and in the files named in §9.2. Then Role 1 can put them into the repository as is.
6. **Language:** documents in English. Interface and pitch texts additionally in Uzbek (Latin script) and Russian.
7. **If you find a contradiction with this document,** don't fix it silently. Put it in the "Questions for the team" section of your file.
8. **Check the passport version** in the header. If your person has a newer one, work with it. In the header of each of your files, write which passport version it is based on.

---

## 1. The idea in one sentence

**EN:** In one minute, Qalqon shows where a website **actually** sends its users' personal data, and checks this against Uzbek law and against what the site itself wrote in its privacy policy.

**UZ:** Saytingiz foydalanuvchilarning shaxsiy ma'lumotlarini aslida qayerga yuboryapti? Qalqon buni bir daqiqada ko'rsatadi va qonunga solishtiradi.

**How we fit track 1:** it is a digital legal service for businesses. It matches the track example "Hujjat tahlili" (document analysis): we analyze a site's legal documents (privacy policy, public offer) and check them against the site's real behavior.

---

## 2. Problem

- **The law exists, and in 2026 it changed twice.** The Law of Uzbekistan "On Personal Data" (ZRU-547) requires consent to processing and regulates cross-border transfer.
  - **March 2026, ZRU-1125:** article 27-1 on localization was rewritten. ✅ Checked against lex.uz on 20.11 (the Russian text is an unofficial translation; the official text is Uzbek).
    - Storage in Uzbekistan is mandatory only for: (1) **biometric** data, (2) **genetic** data, (3) data of **users of telecom operators** operating in Uzbekistan.
    - Other data may be stored and processed abroad if **one of these conditions** is met: (a) the country is recognized as providing adequate protection (the list is approved by the Cabinet of Ministers); (b) the operator has adopted and complies with **standard contractual clauses or binding corporate rules** per the authorized body's requirements; (c) the operator complies with **international standards** for managing and storing PD (the list is approved by the authorized body).
    - **What this means for the product:** conditions (b) and (c) can't be seen from outside. So a transfer to a country outside the list is 🟡 "the legal basis must be confirmed", not automatically 🔴. 🔴 only for biometrics, genetics and telecom operators.
  - **August 2026, CMR No. 415:** a list of 49 countries with "equivalent protection" was approved. It includes Russia, the EU, the UK, Korea and Japan. The US only for companies in the EU-US DPF. Kazakhstan, the UAE, Turkey and mainland China are not on it.
  - The source is secondary for now (pactum.uz, gazeta.uz); check against lex.uz: V-02, V-12, V-13.
- **Businesses can't keep up with the changes.** What was a violation may now be legal, and the other way round. Example: a form sends leads to a Telegram bot, and Telegram the company is registered in the UAE, which is not on the list. How to determine the recipient's country still needs checking (V-16). Tracking such changes is exactly our job: rules get updated and the client gets a notification.
- **There is a gap between the lawyer and the website.** The lawyer checks *documents*. But data leaks through the *site's code*: Meta pixels, Google Analytics, Yandex Metrica, chat widgets, form submissions to foreign CRMs. Marketers and developers install all of this, and the lawyer often doesn't know about it.
- **Manual checking is slow and needs technical skills.** A mid-size business has neither a lawyer nor a person responsible for PD (DPO).
- **Consequences:** fines (V-05, V-06), blocking (the 2021 precedent, V-07), reputation, problems raising investment.

---

## 3. Team and roles

| # | Role | Who | Responsible for | Leads the talk with the mentor |
|---|---|---|---|---|
| 1 | **Tech/AI lead** | [name] | Scanner, detectors, rules engine, AI analysis, report, demo | Technical (T) |
| 2 | **Legal researcher** | [name] | Norms, rule catalog (YAML), violation levels, "how to fix" texts, our own legal risks | Legal (S) |
| 3 | **Business and pitch** | [name] | Competitors, market, prices, customer interviews, presentation, final pitch | Business (B) |

At the checkpoint the team visits each mentor separately. The owner of the role leads the conversation; the others help.

---

## 4. How the product works

```
Site URL
  → Crawler (Playwright, a real browser, up to N pages)
  → Collect: network requests · cookies/localStorage · forms and their fields · where form submissions go · policy/offer texts
  → Enrich: IP → server country/ASN · tracker recognition from lists · CDN detection
  → Rules engine (rules/*.yaml) → findings 🔴 / 🟡 / ⚪
  → LLM: policy analysis (are the required items there) + "written vs does" check
  → Report: score 0–100 · findings with law articles · map of data flows by country · "how to fix" · evidence (screenshots, HAR, time)
```

### What we see and what we don't (we say it honestly)

| We see (as an ordinary visitor) | We don't see |
|---|---|
| All browser requests and the countries of their servers | Where the site's database physically is |
| Cookies and identifiers before and after consent | Where the site's server passes data next |
| Form fields (phone, passport, PINFL…) and whether there is consent | Personal accounts (only with the client's test account) |
| Where form data is sent | Mobile apps (on the roadmap) |
| Site hosting, HTTPS, security headers | Whether the database is registered in the State Register (if there is no public search, V-04) |
| Policy and offer text | |

That is why findings are called **"signs of violation"**, not "violations". The lawyer makes the final call. If the server country is inaccurate because of a CDN, the finding is marked "undetermined".

### Three levels of check depth

| Level | How | For whom | What we learn |
|---|---|---|---|
| **1. Outside, passive** (MVP) | We open the site as an ordinary visitor + DNS and certificates | Any site, mass scan | Where the browser sends data; server countries and providers; trackers; forms; documents; cloud databases in the page code |
| **2. Outside, active** | We fill forms with test "canary" data and log in to a test account | **Only clients' sites, with written consent** (D-009) | Exactly which personal data goes to whom — precise evidence |
| **3. From inside** (roadmap) | Read-only access to the client's cloud, an agent scans the database schema, a questionnaire | Corporate clients | Where the database physically is and which columns hold PD |

### How to tell where the database is without server access (level 1)
- **IP and ASN of the servers** that the site's own forms and API requests go to. AWS, Hetzner, Google, DigitalOcean are foreign providers. Uztelecom, UNICON and the like are local. We keep our own list of Uzbek ASNs.
- **Cloud databases (BaaS) in the page code.** Firebase, Supabase and similar addresses are visible right in the JS, sometimes with the region.
- **File links.** Addresses like `s3.<region>.amazonaws.com` and `storage.googleapis.com` show where documents uploaded by users are stored.
- **DNS:**
  - MX — whose mail: Google, Yandex, Mail.ru;
  - SPF — which mailing services and CRMs are connected;
  - certificates in crt.sh — subdomains like `crm.` and `api.`.
- **Response headers:** signs of Cloudflare, AWS, nginx and so on.
- **Site platform.** If the site runs on Tilda, Wix, Bitrix24 or Shopify, form data is stored by the platform.
- **If the site is behind a CDN and the backend is hidden,** we set "undetermined" and say so honestly in the report.

### Sites with login and personal accounts

| Stage | What we do |
|---|---|
| **MVP** | The public part + login, registration and password recovery pages: which fields, whether there is consent, which trackers see the input |
| **Stage 2 (clients)** | The client gives us a test account; Playwright logs in and saves the session; the account area is scanned by the same detectors. We know the test account's data, so we look for it in traffic to third parties. If there is an SMS code or OneID: either a test account without two-factor authentication, or a person logs in manually in our browser and we save the session |
| **Stage 3** | Recording mode (F-14): a client employee walks through the scenarios themselves while we record the traffic |
| **Mobile apps** | Emulator + proxy (mitmproxy) — roadmap (F-09) |

On sites that haven't hired us, **we don't register or log in** (D-009).

---

## 5. Check catalog (MVP)

**This is the main seam between the lawyer and the code.** Role 1 writes the detectors. Role 2 fills in the legal basis and the level using the schema in §11.2. The levels below are a draft until Role 2 confirms them.

| ID | What we detect | Detector (code) | Level (draft) | Legal basis (filled in by Role 2) |
|---|---|---|---|---|
| PD-LOC-01 | Form data goes to a country **outside the list of 49 countries** (CMR No. 415) | `form_submit_destination` + geo + `rules/countries.yaml` | 🟡 if bases (b)/(c) of part 3 of art. 27-1 are not confirmed; 🔴 for telecom operators | ZRU-547 art. 27-1 as amended by ZRU-1125 ✅, CMR No. 415 (V-12) |
| PD-LOC-02 | Third-party scripts in countries outside the list receive visitor identifiers (IP, cookie ID) | `foreign_requests` + geo + `rules/countries.yaml` | 🟡 | V-08, V-12 |
| PD-HOST-01 | The site itself is hosted abroad | `site_hosting_country` | 🟡 | art. 27-1? |
| PD-TRK-01 | Trackers and pixels (Meta, Google, Yandex…) load before consent | `trackers_before_consent` | 🟡 | V-08 |
| PD-CNS-01 | A form collects personal data without consent (checkbox or text) | `form_consent` | 🔴 | Article on consent (V-01) |
| PD-PII-01 | A form asks for excessive data (passport, PINFL) with no obvious purpose | `form_pd_fields` | 🟡 | Principle of proportionality / purposes? |
| PD-POL-01 | The site has no personal data processing policy | `privacy_policy_present` | 🔴/🟡 | ? |
| PD-POL-02 | The policy lacks required items (operator, purposes, retention periods, data subject rights, cross-border transfer) | LLM `policy_content` | 🟡 | ? |
| PD-MIS-01 | **The policy contradicts the site's behavior** ("we store data in Uzbekistan", but requests go abroad) | LLM `policy_vs_behavior` + detectors | 🔴 | **The product's key feature** |
| SEC-01 | No HTTPS, or forms are sent over HTTP | `https` | 🔴? | Personal data protection measures? |
| SEC-02 | No basic security headers | `security_headers` | ⚪ | Recommendation |
| PD-BIO-01 | The site asks for the camera, a selfie or a face scan (biometrics), and the upload goes abroad | `permissions` + `upload_destination` | 🔴 | Biometrics is on the closed list of mandatory localization (V-02) |
| PD-LEAK-01 | Personal data from forms or URLs goes to third parties (pixels, analytics), including in hashed form | `url_pii` (passive) + `canary_tracking` (only with the client's consent) | 🔴 | Transfer to third parties without consent? |
| PD-REC-01 | Session-recording scripts (Webvisor, Clarity, Hotjar) record what is typed into forms | `session_replay` | 🟡 | ? |
| PD-DB-01 | Database in a foreign cloud (Firebase, Supabase and the like are visible in the page code) | `baas_detect` | 🟡/🔴 | Depends on the data category and the country (V-12) |
| PD-MAIL-01 | The domain's mail (MX) is at a foreign provider: leads and emails with personal data are stored there | `dns_mx` | ⚪/🟡 | Depends on the country (V-12) |

**Score 0–100 (draft):** start at 100; −15 for each 🔴, −5 for each 🟡, −1 for each ⚪; minimum 0.

---

## 6. Architecture and stack

> The detailed architecture, the `facts.json` format, the API, the step-by-step build plan and the demo script are in **`ARCHITECTURE.md`**.

| Layer | Choice | Comment |
|---|---|---|
| Language / API | Python 3.11+, FastAPI | |
| Browser | Playwright (Chromium) | Network, cookies, form DOM, screenshots, HAR |
| Server geolocation | MaxMind GeoLite2 (Country + ASN), fallback ip-api | CDN signs are detected by ASN |
| Tracker lists | DuckDuckGo Tracker Radar / Disconnect + **our own list of Uzbek services** | Our own list is our barrier against competitors |
| Rules | YAML in `rules/` (schema in §11.2) | The lawyer edits rules without a programmer |
| LLM | Claude API: `claude-sonnet-5-5` for document analysis, `claude-haiku-5-5` for mass scans | Answers in structured JSON **with verbatim quotes** from the policy |
| Storage | SQLite | |
| Frontend | React + Vite + TypeScript + Tailwind (D-012) | Live scan feed (SSE) + report + data flow map |
| Export | PDF report | |

### Laws module (lex.uz) — checked on 20.11
- Document pages are served as plain HTML (≈300 KB), and articles are easy to split by the «Статья N.» ("Article N.") markers. The Russian text is an unofficial translation; **the official text is Uzbek**. Quote both, rely legally on the Uzbek one.
- There is an RSS feed `https://lex.uz/ru/rss` — "New in legislation": title, link `/ru/docs/<id>`, type of act, registration number, adoption date, date of entry into force.
- **Scheme:**
  1. Poll the RSS feed every hour. Filter new acts: do they concern personal data (keywords first, then the LLM). If they do, alert the lawyer and clients (F-16).
  2. Once a day, download the **tracked documents**: ZRU-547, CMR No. 415, CMR No. 71, the Code of Administrative Liability, the Criminal Code, ZRU-764, the consumer protection law. Compute a hash of each article and compare it with yesterday's. If an article changed, the rules that cite it get `verified: false` and the lawyer gets an alert.
  3. Corpus of tracked documents → RAG (D-010) → quotes and explanations in the report.

**Why we don't train our own model:** in 2 days there is neither a dataset nor time. The product's value is in the detectors, the rules and the LLM check. On the roadmap: a classifier of form fields and trackers that learns from accumulated scans. That way the data becomes our asset.

### Repository structure

```
lexhack/
  PASSPORT.md          ← this file
  CLAUDE.md            ← instructions for Claude Code
  backend/
    scanner/           ← Playwright crawler
    detectors/         ← one module per detector from §5
    rules_engine/      ← loads rules/*.yaml → findings
    llm/               ← policy analysis, checking, "how to fix" generation
    api/               ← FastAPI
  rules/               ← YAML rules (Role 2)
  frontend/
  demo-site/           ← our deliberately "violating" demo shop for the demo
  research/            ← research results (Roles 2 and 3)
  pitch/               ← pitch and slides
```

---

## 7. Business model

**The main revenue is a monthly subscription.** One-off payments are the way in. A site changes all the time (a marketer adds a new tracker and the violation is back), and laws change too, so a one-off check goes stale.

| Plan | What the client gets | Payment |
|---|---|---|
| Free | 1 scan, score 0–100, top 3 findings | 0 (lead generation) |
| Fix pack | Full report + generated policy, consent form, cookie banner code | One-off |
| Monitoring | Regular scans, Telegram alerts about new violations and law changes, a "Verified by Qalqon" badge | Monthly per domain (tiers by number of domains and frequency) |
| For law firms | The service under their brand: they sell audits to their own clients | Monthly per seat |
| B2G | Mass monitoring of top sites for the authorized body | Annual contract or pilot |

| Segment | Why they'll buy |
|---|---|
| Mid-size business (online shops, clinics, online schools, delivery, microfinance) | No in-house lawyer, and the fines are real |
| Large companies (banks, telecom, marketplaces) | Dozens of domains; the lawyer needs a tool and evidence |
| Law firms | They sell audits but can't check a site technically |
| Startups | Due diligence before investment. The free plan is the entry point |
| Channel: IT Park | Checks for residents (IT Park is one of the hackathon organizers) |

**Prices are a hypothesis for now.** We test them in interviews (R-06). Similar products with per-domain subscriptions: Cookiebot, Termly, OneTrust (check their prices in R-04).

---

## 8. Competitive landscape — starting point for research

Role 3 checks and extends this list and turns it into a table in the §11.3 format.

| Who | What they do | How we differ |
|---|---|---|
| Cookiebot (Usercentrics), OneTrust, Termly, iubenda, Didomi, CookieYes | Consent management + cookie scan, subscription | No Uzbek law, language or local services. No "policy vs behavior" check |
| Blacklight (The Markup) | Free check of trackers on a site | Trackers only, no legal part |
| EDPS Website Evidence Collector | Open-source tool of the European Data Protection Supervisor (EDPS) for collecting evidence of tracking on websites | EU regulators use this very approach: an argument for B2G |
| noyb | In 2021 its software recognized unlawful cookie banners and generated complaints (560 sites in the first wave) | Precedent: automation plus a legal outcome |
| Darrow | Finds legal violations in open data for law firms | Precedent for the "violations → clients for lawyers" business model |
| State Unitary Enterprise "Cybersecurity Center" (csec.uz, under the State Security Service) | Mandatory examination of **government bodies'** information resources under the Cybersecurity Law (ZRU-764). They look for **vulnerabilities** (OWASP). In 9 months of 2026: 225 web resource examinations; in Q1 2026: 252 vulnerabilities, 169 of them on government resources. Prices not published (R-09) | **Not a competitor but a neighboring area.** They answer "can the site be hacked", we answer "does the site handle data lawfully". They work mainly with the public sector, we work with private business. A partnership is possible |
| CIS / Central Asia | **UNKNOWN — the main question of R-04** | |

**Our advantage (draft):** Uzbek law and language, a database of local services (who stores data in the country), the "written vs does" check, generation of corrected documents, the data flow map.

---

## 9. Tasks and deadlines

### 9.1 Timeline

| When | Role 1 — Tech/AI | Role 2 — Lawyer | Role 3 — Business |
|---|---|---|---|
| **20.11 until 21:00** | Crawler, network, geo, 3 detectors (PD-LOC-01, PD-TRK-01, PD-CNS-01), demo site | R-01, R-02, draft R-03 | R-04 v1, list of 10 companies to interview, pitch skeleton (R-07) |
| **Night 20→21** | Batch scan of the top 100 .uz sites → anonymized statistics | | |
| **21.11 until 13:00** | LLM policy analysis, PD-MIS-01, report page, flow map | R-03 final, R-08, answers for the legal mentor (§13) | R-05, R-06 (interviews!), answers for the business mentor (§13) |
| **21.11 14:00–17:00** | **CHECKPOINT: qualifying for the final depends on it** | | |
| **21.11 19:00** | Results in the "LexHackathon" Telegram group (top 10 of the track) | | |
| **21.11 19:00–22:00** | Generation of corrected documents, polishing | "How to fix" texts in UZ/RU | Final slides |
| **22.11 until 10:00** | Rehearsal: 3 min pitch + 2 min demo + 2 min Q&A | | |

### 9.2 Ready-made tasks for AI assistants

Copy the task to your assistant together with this passport. Save the result to the file named in the task.

**R-01 · Role 2 · Norms → `research/legal-norms.md`**
> Find on lex.uz the current edition of the Law of Uzbekistan "On Personal Data" (ZRU-547). Copy verbatim (in Uzbek and Russian, if available) the articles on: the definition of personal data, data subject consent, purposes and proportionality, cross-border transfer, localization (art. 27-1), registration of databases in the State Register, protection measures, data subject rights, operator obligations. For each article give the number, the quote, the link and the edition date. Separately answer: are an IP address and a cookie identifier personal data under this law (V-08)? Close facts V-01…V-04, V-08, V-09 in the §11.4 format.

**R-02 · Role 2 · Liability and practice → `research/legal-liability.md`**
> Find the articles of Uzbekistan's Code of Administrative Liability and Criminal Code on liability for violating personal data legislation, the fine amounts (in BCA) and the current BCA value for 2026. Find practice: the 2021 restrictions on access to social networks for violating localization requirements (which services, when, who decided), known fines and inspections. Close V-05…V-07, V-11.

**R-03 · Role 2 · Rule catalog → `rules/*.yaml`**
> For each check in §5 of the passport, create a YAML file strictly following the §11.2 schema: level, legal basis with a verbatim quote and link, sanction, "how to fix" text in RU and UZ. If there is no basis for 🔴, set 🟡 or ⚪ and explain why. Propose missing checks as Features.

**R-04 · Role 3 · Competitors → `research/competitors.md`**
> Make a table in the §11.3 format: (a) the global players from §8 and others; (b) regulators' tools (EDPS Website Evidence Collector, CNIL tools and so on); (c) **similar services in Uzbekistan, Kazakhstan, Russia and other CIS countries**: who checks websites for compliance with personal data and localization laws. For each: country, what they do, model and prices, clients, investment, link. At the end: 3–5 features worth borrowing (§10 format), and how we differ from each.

**R-05 · Role 3 · Uzbek market → `research/market.md`**
> Find, with sources: the number of domains in the .uz zone, the number of online shops and e-commerce companies, the number of banks and microfinance organizations, the number of IT Park residents, e-commerce growth. Calculate TAM/SAM/SOM for the subscription with explicit assumptions. Close V-10.

**R-06 · Role 3 · Interviews and prices → `research/interviews.md`**
> Write an interview script of 5–7 questions in Uzbek and Russian for owners and marketers of businesses with websites: do they know about the law, have they checked their site, how much would they pay for a one-off audit and for monitoring. Prepare a table for recording the answers. Goal: interview 5–10 companies before 13:00 on 21.11.

**R-07 · Role 3 · Pitch → `pitch/pitch-v1.md`**
> Build the structure of a 3-minute pitch (+2 min demo, +2 min Q&A) for criteria B1–B5 and S5 from §12: problem → solution → how it works → business model → market → competitors → team → ask (pilot). Give the text in Uzbek and Russian. At the end, 10 likely jury questions with answers.

**R-08 · Role 2 · Our own legal risks → `research/legal-our-risks.md`**
> Assess the legality of what we do: scanning public pages as an ordinary visitor, storing results, publishing anonymized statistics. Write a disclaimer for the report ("not an official opinion…") in UZ and RU, and the main points of our own data processing policy and terms of service. Separately: does Qalqon itself process personal data, and what do we have to comply with? Close V-15: does checking websites for vulnerabilities require a license, and why we don't go into that area.

**R-09 · Role 3 · Cybersecurity Center and the audit market → `research/csec.md`**
> Find out about the State Unitary Enterprise "Cybersecurity Center" (csec.uz, Telegram t.me/cyber_csec_uz): what website checks it does, for whom, whether they are mandatory for private business, what exactly is checked (vulnerabilities only, or personal data too), what the report looks like, how much it costs. Prices aren't published, so it's better to call (+998 55 502 10 10) or ask the mentors. Separately: which private companies in Uzbekistan do information security or personal data audits, and at what price (for example, law firms like pactum.uz sell an "operator document kit"). Result: a "them / us" table and our difference in one sentence.

**R-10 · Role 2 · New art. 27-1 and the country list → `research/legal-27-1-2026.md` + `rules/countries.yaml`**
> Read on lex.uz ZRU-1125 of 26.03.2026 (new edition of art. 27-1 and art. 20 of ZRU-547) and CMR No. 415 of 29.07.2026. Copy verbatim: the closed list of categories with mandatory localization; the three conditions in part 3 of art. 27-1 for storage abroad; the list of 49 countries; the condition for the US (EU-US DPF); the breach notification deadlines. Answer V-16: is the recipient's country determined by where the servers are or by the company's jurisdiction? Format the country list like this:
> ```yaml
> source: "CMR No. 415 of 29.07.2026"
> url: "https://lex.uz/..."
> effective_from: "2026-08-03"
> adequate: [RU, DE, FR, GB, KR, JP]   # ISO 3166-1 alpha-2, the full list of 49
> conditional:
>   US: "only participants of the EU-US Data Privacy Framework"
> verified: false
> ```

---

## 10. Features — bank of ideas

Each new feature is written like this: `F-XX · name · what it gives · complexity (S/M/L) · who proposed it · status`.
Statuses: `MVP` (built before the checkpoint) · `Final` (by 22.11) · `Roadmap` (pitch only) · `Rejected`.

| ID | Feature | What it gives | Complexity | Status |
|---|---|---|---|---|
| F-01 | "Policy vs behavior" check | The main difference from all competitors | M | MVP |
| F-02 | Data flow map (site → servers by country on a world map) | Wow effect in the demo | S | MVP |
| F-03 | Mass scan of the top 100 .uz sites → anonymized report "Uz-net Privacy 2026" | A number for the pitch, PR, data accumulation | M | MVP |
| F-04 | Generation of corrected documents (policy, consent) in UZ/RU | Closes the whole "found → fixed" cycle | M | Final |
| F-05 | Telegram alerts (a new violation, or the law changed) | Keeps subscribers | S | Final |
| F-06 | Evidence pack for the lawyer (screenshots + HAR + time) | Value for law firms and B2G | S | Final |
| F-07 | "Verified by Qalqon" badge on the client's site | Viral growth | S | Roadmap |
| F-08 | Pre-release check (CI/CD) for developers | A product for development teams | M | Roadmap |
| F-09 | Mobile app scanner | Market expansion | L | Roadmap |
| F-10 | Other jurisdictions (KZ, RU, GDPR) | Growth beyond Uzbekistan | M | Roadmap |
| F-11 | "Canaries": we fill forms with test data and look for it in all outgoing traffic (plain text, URL-encoded, base64, SHA-256) | Proves exactly who received the personal data | M | Final (only with the client's consent) |
| F-12 | Detector of cloud databases and storage in the page code (Firebase, Supabase, S3 links with region) | Shows where the database is without server access | S | MVP |
| F-13 | DNS reconnaissance: MX, SPF, certificates (crt.sh) → which SaaS the company uses | Passive, no requests to the company's server | S | Final |
| F-14 | Recording mode: a client employee walks through the site (including the personal account) in our browser or extension, and we record the traffic | Solves logins, SMS codes, OneID and captchas | M | Roadmap |
| F-15 | Inside-out: read-only access to the client's cloud and a scan of the database schema for personal data columns (the agent runs at the client) | We know exactly where and what data is stored | L | Roadmap |
| F-16 | "The law changed — your status changed" alert (as with ZRU-1125 and CMR No. 415 in 2026) | The main reason to subscribe | S | Final |

---

## 11. Result formats (so that everything merges without rework)

### 11.1 Header of any research file

```markdown
# <Title>
- Author: <name>, Role <N>
- Date/time: <DD.MM HH:MM>
- Passport version: <0.x>
- Confidence: high / medium / low

## Conclusions (3–5 points, the most important ones)
## Data (tables; every row has a source)
## Features for the product (§10 format)
## Questions for the team / contradictions with the passport
## Sources (list of URLs)
```

### 11.2 Rule schema `rules/<ID>.yaml`

```yaml
id: PD-LOC-01
title:                  # interface texts: Russian and Uzbek (Latin)
  ru: "Данные из форм уходят на зарубежные серверы"
  uz: "Shakl ma'lumotlari xorijiy serverlarga yuborilmoqda"
level: violation        # violation (🔴) | risk (🟡) | recommendation (⚪)
detector: form_submit_destination   # detector name from §5; don't invent new ones without agreeing with Role 1
params:                 # optional, detector parameters
  allowed_countries: [UZ]
legal_basis:
  - act: "Law of Uzbekistan \"On Personal Data\" ZRU-547"
    article: "27-1"
    quote_uz: "..."
    quote_ru: "..."
    url: "https://lex.uz/docs/..."
    edition_date: "DD.MM.YYYY"
sanction: "Code of Administrative Liability art. ... — fine of ... BCA"   # or null
fix:                    # interface texts: Russian and Uzbek (Latin)
  ru: "Как исправить: ..."
  uz: "Qanday tuzatish kerak: ..."
verified: false         # true only after Role 2 has checked it against lex.uz
```

### 11.3 Competitor table

| Name | Country | What they do | Model and prices | Clients | Investment | What to borrow | How we differ | Link |
|---|---|---|---|---|---|---|---|---|

### 11.4 Fact check

| ID | Claim | Status (`CONFIRMED` / `REFUTED` / `NOT VERIFIED`) | Correct wording | Source |
|---|---|---|---|---|

---

## 12. Scoring criteria → what we show

Total = (T + B + S) / 3. Each mentor scores 5 criteria from 1 to 10, and the average is taken. The top 10 within the track go to the final.

| Criterion | What we show | Who |
|---|---|---|
| T1 Technical implementation | A live scan of any URL in front of the mentor | 1 |
| T2 Code readiness (MVP) | A clean repository, the §6 structure, a README | 1 |
| T3 AI and innovation | LLM document analysis with quotes + the "policy vs behavior" check + generation of fixes | 1 |
| T4 Team knowledge | Everyone explains their own part | all |
| T5 Tech stack | Playwright, FastAPI, GeoLite2, Claude API — why we chose them | 1 |
| B1 Relevance of the problem | The "lawyer vs code" gap, precedents, top-100 statistics | 3 |
| B2 Business model | The plans in §7 | 3 |
| B3 Competitive advantage | The R-04 table, our differences | 3 |
| B4 Financial sustainability | Monthly subscription, cost per scan, unit economics | 3 |
| B5 Growth potential | Law firms, B2G, mobile apps, other countries | 3 |
| S1 Legal relevance | ZRU-547, localization, the 2021 practice | 2 |
| S2 Deep understanding of the field | 3 levels of findings, the honest limitations in §4 | 2 |
| S3 Practical applicability | "How to fix" texts, document generation | 2 |
| S4 Compliance with legislation | R-08: legality of scanning, disclaimer, lex.uz only | 2 |
| S5 Scale of social impact | Protecting citizens' personal data, statistics for the country | 2 + 3 |

---

## 13. Mentor questions — our answers (short)

- **"Are your clients only startups?"** No. The main segments are mid-size businesses without a lawyer and large companies with dozens of domains. Law firms are a sales channel. A lawyer reads documents, not network traffic: we close that gap.
- **"Where does your data come from?"** We don't need anyone else's API. We look at the site as an ordinary visitor through a real browser; one check is 20–50 pages and hundreds of requests. We name our limitations ourselves (§4), which is why we write "signs of violation".
- **"Is scanning legal?"** We open only public pages, we hack nothing, and we don't store other people's personal data. We check clients' sites under a contract and publish statistics anonymized (R-08).
- **"What happens when the law changes?"** The opposite of a problem: every change is a reason to re-check the client. Rules are stored as settings, and the lawyer updates them without a programmer. Localization is one check among many.
- **"Don't sites block bots?"** We use a real browser and a slow pace. Clients add us to their allowlist themselves.
- **"Won't the government build its own?"** Then we become a contractor (B2G). EU regulators already use this approach (EDPS Website Evidence Collector).
- **"What if OneTrust or Cookiebot come?"** They don't have Uzbek law, the language or a database of local services.
- **"Do you depend on OpenAI/Claude?"** The main checks run on rules. The LLM is needed only for texts, and it can be replaced with an open model.
- **"Doesn't the Cybersecurity Center already do this?"** No. The Center looks for vulnerabilities, mostly on government sites: "can the site be hacked". We check legal compliance: "does the site collect and transfer data lawfully". We don't do pentests (D-008). These are neighboring areas, and a partnership is possible.
- **"How will you know where the database is?"** At level 1, from indirect signs: the ASNs of API servers, cloud databases in the page code, storage links, DNS. At level 2, with test data and the client's consent. At level 3, from inside. Whatever we can't see, we honestly mark "undetermined" (§4).
- **"The law was relaxed in 2026 — are you still needed?"** All the more. The rules got more complex: a closed list, a list of 49 countries, conditions for the US. Businesses don't know what is allowed now. Our rules engine updates in hours.

---

## 14. Facts to verify

Until the status is `CONFIRMED`, we **don't state** these facts in the pitch.

| ID | Claim | Status | Who |
|---|---|---|---|
| V-01 | The Law of Uzbekistan "On Personal Data" is ZRU-547 of 02.07.2019, in force since 01.10.2019. Consent — art. 21, cross-border transfer — art. 15, database registration — art. 20, biometrics — art. 26, liability — art. 33 | CONFIRMED (details and table of contents, lex.uz/ru/docs/4396428). The texts of articles 15/21/33 still have to be copied out (R-01) | 2 |
| V-02 | Art. 27-1 as amended by ZRU-1125 of 26.03.2026: mandatory localization covers biometrics, genetics and users of telecom operators; everything else may be stored abroad under one of three conditions (adequate country / standard contractual clauses or binding corporate rules / international standards) | CONFIRMED (lex.uz, unofficial Russian translation; the Uzbek text is official) | 2 |
| V-03 | The authorized body is the State Personalization Center under the Cabinet of Ministers (art. 8); it keeps the State Register of personal data databases. Model procedures were approved by Minister of Justice orders No. 19-mh and No. 20-mh of 14–15.11.2023 | CONFIRMED (lex.uz, art. 8 with the LexUz commentary) | 2 |
| V-04 | A State Register of personal data databases exists; is there a public search? | NOT VERIFIED | 2 |
| V-05 | The Code of Administrative Liability has an article on liability for violating personal data legislation; the fine amount | NOT VERIFIED | 2 |
| V-06 | The Criminal Code has an article on violating personal data legislation | NOT VERIFIED | 2 |
| V-07 | In 2021 Uzbekistan restricted access to several social networks for violating localization requirements | NOT VERIFIED | 2 |
| V-08 | An IP address and a cookie ID are personal data under Uzbek law | NOT VERIFIED | 2 |
| V-09 | Cross-border transfer rules (which article, what conditions) | NOT VERIFIED | 2 |
| V-10 | The number of domains in the .uz zone | NOT VERIFIED | 3 |
| V-11 | The BCA value for 2026 | NOT VERIFIED | 2 |
| V-12 | CMR No. 415 of 29.07.2026 (in force since 03.08.2026): a list of 49 countries with equivalent protection — Russia, the EU, the UK, Korea, Japan; the US only for EU-US DPF participants; KZ, AE, TR, CN are not on it. Breach notification — 24 h / 72 h | PARTIAL (pactum.uz); check against lex.uz | 2 |
| V-13 | Database registration in the State Register is now tied to the list in part 2 of art. 27-1 (new edition of art. 20). The procedure is CMR No. 71 of 08.02.2020: free, 5 working days | PARTIAL (pactum.uz) | 2 |
| V-14 | Cybersecurity Center (csec.uz, Presidential Resolution PP-4452 of 14.09.2019, under the State Security Service): examination of government bodies' information resources is mandatory (ZRU-764); 225 web resource examinations in 9 months of 2026; Q1 2026: 252 vulnerabilities, 169 of them on government resources. Prices not published | PARTIAL (lex.uz, csec.uz, 1prime.ru) | 3 |
| V-15 | Does checking websites for vulnerabilities require a license or permit? | NOT VERIFIED | 2 |
| V-16 | A Telegram bot as the recipient of leads: is the recipient's country determined by where the servers are or by the company's jurisdiction (UAE)? | NOT VERIFIED | 2 |
| V-17 | lex.uz terms of use: personal use only; copying for profit only with written permission. What may a commercial service do (quotes with a link?), and can we get official access from the Ministry of Justice? | NOT VERIFIED (this is what the lex-rag README says) | 2 |

---

## 15. Decision log

Assistants don't challenge these decisions. Only the team can change them, with a new entry in the log.

| ID | Date | Decision | Why |
|---|---|---|---|
| D-001 | 20.11 | Track 1 — "Huquqiy xizmatlarni ko'rsatish" | In track 2 the mentor called the idea "off topic"; in track 1 it fits as a service for businesses |
| D-002 | 20.11 | The product is a scanner of website compliance with the personal data law (Qalqon) | Not a chatbot; the demo doesn't hallucinate; clear B2B |
| D-003 | 20.11 | Public statistics only anonymized. In the demo we use **our own** demo site | Don't name specific (especially government) sites at a Ministry of Justice event |
| D-004 | 20.11 | Findings are "signs of violation", 3 levels 🔴🟡⚪ | We don't see the backend; the lawyer makes the final call |
| D-005 | 20.11 | We don't train our own model during the hackathon | No data and no time. AI = LLM analysis + checking |
| D-006 | 20.11 | The source of norms is lex.uz only, with verbatim quotes | Criterion S4, the legal mentor's trust |
| D-007 | 20.11 | The main revenue is a monthly subscription; a one-off fix pack is the way in | Sites and laws change, so checking has to be continuous |
| D-008 | 20.11 | We don't look for vulnerabilities and don't do pentests. Our area is the legal compliance of data processing | Vulnerabilities are the Cybersecurity Center's area and possibly a licensed activity (V-15). This way we complement the Center rather than compete with it |
| D-009 | 20.11 | For any site, passive mode only (as an ordinary visitor). Canaries, form submission and logging into personal accounts only on clients' sites with written consent | Legality (S4) and ethics |
| D-010 | 20.11 | Violations are determined by the **rules engine**, not by the LLM/RAG. RAG over laws is used only for quotes, plain-language explanations and helping the lawyer. The RAG was built by Role 1 before the hackathon — **we declare it to the jury** (clause 6.5 of the Regulations) | Against hallucinations; compliance with the hackathon rules |
| D-011 | 20.11 | We take laws from lex.uz: the "New in legislation" RSS feed + a daily article-by-article check of tracked documents (hash → changes) | lex.uz serves plain HTML and RSS — checked on 20.11 |
| D-012 | 20.11 | Frontend: React + Vite + TypeScript + Tailwind, one screen, live feed via SSE | Quick to build; the live feed is the wow effect of the demo |
| D-013 | 20.11 | lex-rag (55 thousand lex.uz acts, hybrid search, quotes checked by code) is called as an **external service** through its API; we don't copy its code into the repository | A clear "built before / during the hackathon" boundary (clause 6.5) |

---

## 16. Hackathon context (for assistants)

- **Checkpoint 21.11, 14:00–17:00:** three mentors, 10 minutes each, one at a time. Technical — code and architecture; business — model and market; legal — compliance with laws and practice.
- **Final 22.11:** 3 min pitch (idea, legal solution, business model) + 2 min demo + 2 min Q&A.
- **Rules:**
  - attendance at TSUL on 20–21 November is mandatory; coordinators check every 2 hours;
  - the team writes the core functionality itself; open source and ready-made AI models are allowed;
  - everything made before the hackathon has to be declared.
- **Prizes:** 60 / 40 / 25 million soums per track, plus a pilot in Ministry of Justice systems and incubation at IT Park.

---

## 17. Glossary

- **PD / shaxsga doir ma'lumotlar** — personal data.
- **Operator** — whoever processes personal data (the site owner).
- **Localization** — the requirement to store the personal data of Uzbek citizens on servers in Uzbekistan.
- **Cross-border transfer** — transfer of personal data abroad.
- **Tracker / pixel** — a third-party script that collects data about the visitor (Meta Pixel, Google Analytics, Yandex Metrica).
- **CDN** — content delivery network; because of it the server's country may be determined inaccurately.
- **HAR** — a file with all of a page's network requests; it serves as evidence.
- **BCA** (БРВ) — base calculation amount; fines are calculated in it.
- **DPO** — the person responsible for personal data protection in a company.
- **ZRU** (ЗРУ, O'RQ) — a Law of the Republic of Uzbekistan, followed by its number.
- **CMR** (ПКМ, VMQ) — a Resolution of the Cabinet of Ministers.
- **PP** (ПП, PQ) — a Resolution of the President.
- **TSUL** (ТГЮУ) — Tashkent State University of Law, the hackathon venue.

---

## Changelog

- **0.1** — 20.11 15:30 — passport created (Role 1).
- **0.2** — 20.11 17:00:
  - added the 2026 law changes (ZRU-1125, CMR No. 415, the list of 49 countries);
  - Cybersecurity Center (§8, V-14, D-008);
  - three levels of check depth, determining where the database is stored, working with logins (§4);
  - new checks PD-BIO, PD-LEAK, PD-REC, PD-DB, PD-MAIL (§5);
  - features F-11…F-16, tasks R-09 and R-10, decisions D-008 and D-009.
- **0.3** — 20.11 18:00:
  - art. 27-1 and art. 8 checked against lex.uz: V-01…V-03 confirmed;
  - the level of PD-LOC-01 adjusted;
  - the laws module added (§6), and decisions D-010, D-011.
- **0.4** — 20.11 19:00:
  - the architecture and build plan moved to `ARCHITECTURE.md`;
  - decisions D-012 (frontend) and D-013 (lex-rag as an external service);
  - new fact to verify V-17 (lex.uz terms).
- **0.5** — 20.11 19:20:
  - the passport translated into English; team documents are now written in English (§0.6, `CLAUDE.md`). Interface and pitch texts stay in Uzbek (Latin) and Russian. No other content changes;
  - abbreviations ZRU, CMR, PP and TSUL added to the glossary (§17).
