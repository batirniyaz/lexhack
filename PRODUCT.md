# Qalqon — product spec (what the user sees)

> **Status: DRAFT v0.1 — for Role 1 review.** Items marked **OPEN** need a decision before coding.
> Architecture and backend: `ARCHITECTURE.md`. Product strategy and decisions: `PASSPORT.md`.
> Rule: we agree on this spec first, then build the frontend (CLAUDE.local.md).

---

## 1. Users and what they want

| User | What they want to do | What makes them come back |
|---|---|---|
| **Business owner / marketer** (main paying user later) | "Is my site OK with the personal-data law? What do I fix first?" | Re-scan after fixes; see the score go up |
| **In-house lawyer / compliance officer (DPO)** | Evidence they can show to developers and management; the article of law next to each finding | History, evidence file, report to share |
| **External lawyer / law firm** | Check a client's site and give the client a report | Many sites in one account (later) |
| **Jury / demo audience** | Understand the value in 2 minutes | — (presentation mode, replay) |

**The one thing the product must make obvious:** *what the site says* (policy quote) vs *what the site does*
(network evidence), plus the law that applies.

## 2. UX principles

1. **One input to start.** A URL field on the first screen. No sign-up needed for the first check.
2. **Show the work while it happens.** The live feed is part of the product, not a loading screen: people trust a
   finding more when they saw the request appear.
3. **Every finding = evidence + law + fix.** Never a verdict without the evidence that produced it.
4. **Honest wording.** "Signs of violation", "not verified by a lawyer yet", "country undetermined (CDN)".
5. **Uzbek first, Russian second.** Uzbek Latin is the default UI language; Russian is one click away.
6. **Calm, dense, professional.** An audit tool, not a marketing page. No gradients, no emoji icons, no decoration.

## 3. Site map

```
/                      Home: URL input, anonymized market stats, sample report
/scan/:id              Live scan → turns into the report when done
/scan/:id?tab=…        Report tabs: overview | findings | flows | policy | forms | evidence
/history               My scans (all sites), newest first
/sites/:id             One site: score trend, last scan, what changed since the previous scan
/login, /register      Email + password
/profile               Name, company, role, language, password, delete account
/r/:shareToken         Read-only shared report (no login)              [P1]
```

Header on every page: logo · "New check" · History · language UZ/RU · presentation-mode switch · account menu.

## 4. Screens

### 4.1 Home `/`
- **Hero:** one line — *"Saytingiz shaxsiy maʼlumotlarni aslida qayerga yuboryapti?"* (RU: "Куда ваш сайт на самом деле
  отправляет персональные данные?") · URL field · button **Tekshirish** (Check) · small print: "Passive check of
  public pages, ~1–2 minutes. Results are signs of violation, not a legal conclusion."
- **Market strip** (from `GET /api/stats`, anonymized): e.g. "Trackers before consent on 7 of 8 popular sites",
  "Webvisor records form input on 5 of 8", "Average score 84.6".
- **Sample report** link: a pre-scanned anonymized report ("Marketplace A") — lets anyone see the result without
  waiting.
- **How it works**: 3 steps (open like a visitor → read the policy → compare with the law).
- Input validation: normalize `site.uz` → `https://site.uz`; errors from the API (private address, unreachable) shown
  inline in plain words.

### 4.2 Live scan `/scan/:id` (status = running)
Three columns on desktop, stacked on mobile:
- **Left — stages** with progress: 1 Pages · 2 Network · 3 Forms & documents · 4 Policy (AI reads) · 5 Law check.
  Current page `3 / 10` and its URL.
- **Center — live log** (monospace, newest at the bottom, auto-scroll with a "pause" toggle). One line per event:
  `connect.facebook.net   Meta · US · advertising · first visit, no consent`
  `form  /order   name, phone   no consent text`
  `document  /privacy   personal-data policy found`
  `policy  5 promises extracted, 0 unverified quotes dropped`
  Lines are colored only by level (red/yellow/grey); everything else neutral.
- **Right — live counters**: third-party hosts · countries · forms with personal data · documents · and a small
  **world map** whose countries light up as hosts appear.
- States: `challenge` → banner "The site checks for bots… waiting"; `blocked` → final screen "Closed to the check
  (bot protection). No findings were produced." with an explanation; `error` → message + retry.
- When `done` arrives the page morphs into the report (same URL), scrolling to the score.

### 4.3 Report `/scan/:id` (status = done)
**Report header:** site (or its label in presentation mode) · scan date · pages scanned / requests · **score 0–100**
with 🔴/🟡/⚪ counts · badge "Rules not verified by a lawyer yet" while drafts are used.
**Actions:** Re-scan · Download evidence (HAR) · Copy link · Export PDF [P1] · Share read-only link [P1].

**Tabs**

| Tab | Content |
|---|---|
| **Overview** (Umumiy) | 1) The **"Says vs does"** card if there is a PD-MIS-01 finding: the policy quote in serif on the left, the network evidence in monospace on the right, the article of law below. 2) Top 3 findings by level. 3) Mini flow map + "data goes to N countries". 4) What we could not see (limits) in one line |
| **Findings** (Topilmalar) | All findings grouped 🔴 → 🟡 → ⚪, filter by level. Each finding expands to: evidence list · legal basis (article, quote UZ with RU translation, link to lex.uz) · how to fix (copy button) · "verified by lawyer: yes/no" · downgraded note if the promise had exceptions |
| **Data flows** (Maʼlumot oqimi) | World map: arcs from Uzbekistan to each country, colored by status (local · adequate · conditional · not on the list · undetermined). Table: host · owner company · company country · server country · category · on first visit · requests. Filter: trackers only / all |
| **Policy** (Siyosat) | Documents read (links). Checklist of the 10 policy elements: present ✓ (with quote) / missing ✗. Promises: each quote with its status — *kept* / *contradicted* (link to the finding) / *cannot be checked from outside*. Services the policy never names |
| **Forms** (Shakllar) | Each form: page, fields with detected type (name, phone, passport, PINFL…), consent: checkbox / text / none, where it is sent (if known) |
| **Evidence** (Dalillar) | Pages scanned (status, title) · cookies (first visit vs later, third-party) · backends seen in code · raw event log · HAR download · scan settings (mode, pages, model, rules version) |

### 4.4 History `/history`
Table: site · date · score (with ▲▼ vs previous scan of the same site) · 🔴🟡⚪ · status (done / blocked / error) ·
open. Filter by site, search. Empty state: "No checks yet" + URL field.

### 4.5 Site page `/sites/:id`
Score trend over time (small line chart) · last scan summary · **"What changed since the previous scan"**:
new findings / fixed findings / unchanged · Re-scan button. This is the "monitoring" story without a subscription.

### 4.6 Login / Register / Profile
- Register: email, password (min 8), name, company (optional), role (business / lawyer / other), language.
- Login: email + password. Logout. No social login, no OneID in the MVP (OneID = roadmap slide).
- Profile: edit name, company, role, language; change password; **delete account and all scans** (we are a privacy
  product — we must offer this).
- Anonymous scans are allowed; after login, scans made in the same browser session can be attached to the account
  **OPEN** (nice, not required).

## 5. What is stored (history) and for how long

| Table | Fields | Notes |
|---|---|---|
| `users` | id, email (unique), password_hash (argon2/bcrypt), name, company, role, lang, created_at | |
| `sessions` | token (random, 32 bytes), user_id, created_at, expires_at | HttpOnly, SameSite=Lax cookie |
| `sites` | id, user_id, url, registrable_domain, label, created_at | one row per site per user |
| `scans` | id (= scan_id), user_id (nullable), site_id (nullable), url, status, score, levels, stats, policy_status, rules_version, started_at, finished_at, share_token (nullable) | index only |
| files `scans/<id>/` | facts.json, report.json, scan.har, events.jsonl | already produced today |

- Anonymous scans: reachable only by their unguessable id; kept **7 days** **OPEN**.
- We store technical facts about public websites plus account data. Our own privacy policy and terms are task R-08.

## 6. Small features ("фишки")

| Feature | Value | When |
|---|---|---|
| "Says vs does" card (serif quote vs monospace evidence) | The core idea in one picture | P0 |
| Live world map that lights up during the scan | Demo wow | P0 (simple) |
| Presentation mode (domains → "Marketplace A") | Safe demo of real sites | P0 (API ready) |
| Replay of a finished scan as a live feed | Demo works without network | P0 (API ready) |
| "Copy fix" button on each finding | Developer can act at once | P0 |
| Score delta vs previous scan + "new / fixed" diff | Reason to re-scan; monitoring story | P1 |
| Read-only share link | Lawyer sends to client | P1 |
| PDF export of the report | Lawyers live in PDFs | P1 |
| Glossary tooltips (PINFL, CDN, DPF, Webvisor…) | Non-technical users understand | P1 |
| Telegram alert "your score changed / the law changed" | Monitoring, subscription driver | P2 (roadmap) |
| Scheduled re-scans, subscription, multi-site for law firms, OneID login | Business model | P2 (roadmap) |

## 7. Languages and texts
- UI strings in a dictionary (`uz`, `ru`); Uzbek Latin default. Rule titles and fixes already exist in `uz`/`ru`/`en`
  in the rule YAML; evidence summaries are English today → **OPEN**: translate the summary templates to uz/ru (P1) or
  show them in English for the checkpoint.
- Legal quotes: Uzbek official text + Russian (marked "unofficial translation" when it comes from lex.uz RU).

## 8. Visual direction
- **Concept: "what they say vs what they do".** Three type roles: **serif** for quotes from policies and laws
  (reads like a legal document), **monospace** for technical evidence (hosts, IPs, requests), **sans** for the UI.
  All three must support Uzbek Latin (oʻ gʻ ʼ) and Cyrillic.
- Palette: neutral (Astryx `theme-neutral`), one accent for actions, and level colors only for 🔴🟡⚪ and flow
  statuses. Dark mode: whatever the theme gives for free.
- Components: Astryx (pending the pilot). Charts and the map: our own SVG (Astryx charts are not stable).
- Quality gate before showing: UI UX Pro Max checklist (contrast ≥ 4.5:1, no emoji icons, focus states,
  reduced motion, 375 / 768 / 1024 / 1440 px).

## 9. Scope

| | P0 — checkpoint 21.11 14:00 | P1 — final 22.11 morning | P2 — roadmap slide |
|---|---|---|---|
| Screens | Home · Live scan · Report (Overview, Findings, Data flows, Policy) · History (no login) | Login / Register / Profile · Site page with trend + diff · Forms and Evidence tabs · Share link · PDF | Monitoring, alerts, subscription, multi-site, OneID |
| Backend | Ready today | Auth, users/sites/scans tables, history by user, diff between scans, share tokens | Scheduler, billing |

**OPEN — main decision:** login/profile in P0 or P1? Recommendation: **P1**. At the checkpoint mentors judge the
core value (scan → report), code quality and the business model; a login screen adds little there, and auth done in a
hurry is a security risk. History works without login in P0 (list of scans on this server).

## 10. Backend changes this spec needs
- P0: `GET /api/scans` already lists scans; add `site` filter and `previous_score` for ▲▼ (small).
- P1: `POST /api/auth/register|login|logout`, `GET /api/me`, `PATCH /api/me`, `DELETE /api/me`;
  `GET /api/sites`, `GET /api/sites/{id}` (trend + diff); SQLite tables from §5; scans linked to the user when
  logged in; `POST /api/scans/{id}/share` → token; `GET /api/shared/{token}`.

## 11. Open questions
1. Login in P0 or P1? (recommendation: P1)
2. Retention of anonymous scans (7 days?).
3. Evidence summaries language for the checkpoint: English or translated templates?
4. Product name stays "Qalqon" for the demo? (D-014)
5. Which sample report is public on Home (which sector)?
