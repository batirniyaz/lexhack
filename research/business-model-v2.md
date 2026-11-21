# Business model v2: audit categories, monthly tokens, free first audit

- Author: batirniyaz, Role 1 (team decision of 21.11, written with Claude Code)
- Date/time: 21.11 03:40
- Based on passport version: 0.13 (decision D-026)
- Confidence: **high** for the structure (team decision); **low** for the prices (hypotheses to test in R-06 interviews)
- **Update 21.11 10:40 (D-031, D-032):** accounts, registration and the token wallet are **not built for the hackathon**;
  they return only if the project continues. The categories below map to the difficulty groups in
  `checks-by-difficulty.md`: I = Easy, II = Medium (includes Easy), III = Hard-A, IV = Hard-B. Prices: Role 3 sets them per group.
- Replaces: `business-model.md` (v1) §5 "Price formula" and §6 "Worked examples" as the **public** pricing.
  v1 stays valid for: global and local comparables (§1–§2), cost inputs (§7), the trust model (§4), channels (§10).
  The v1 formula "price = 4 × our cost" is kept **inside the team only**, as a floor check (section 6 below).

## Conclusions

1. **Free first look, no account:** the home page shows an anonymized example report of a real Uzbek site
   (already live: `GET /api/sample`, D-024).
2. **Free first audit, with an account:** after registration the user gets **one** free Express audit (category I)
   with a **partial** report: score, counts and the titles of **all** findings, one finding fully open. No evidence
   details, no law quotes, no fix steps, no PDF, no share link.
3. **Paid use = monthly tokens per audit category.** Four categories, by what the client must give us and what an
   audit costs us. One token = one audit of one site. The user buys any mix (for example 3 × category I + 1 ×
   category IV) — **hybrid**, no plan locks.
4. **Volume discount inside each category, per month:** 1 audit = 100%, the 2nd adds 50%, the 3rd adds 40%, each
   next one adds 35% (automated categories). Example for category I: 1 → 100k, 2 → 150k, 3 → 190k UZS.
   Categories with staff work use a softer curve (75% / 65% / 60%), otherwise volume would sell below cost.
5. **Free without tokens:** (a) re-checking the user's saved scans when the law changes — our main reason to stay
   subscribed; (b) one re-check of the same site within 14 days after a paid audit, to confirm fixes.
6. **Only categories I and II are sold at the hackathon.** III and IV are shown as "on request / roadmap": they need
   the client's consent or access and staff time (passport §4 levels 2–3, D-009).

## Data

### 1. The four audit categories

Grouped by **what the client gives** (nothing / consent and a test account / access from inside) and **our cost per
audit** (machine seconds / LLM / staff hours). Service IDs M1–M16 are from `service-catalog.md`; the full mapping is in
`service-catalog-v2.md`.

| Category | What one audit includes | What the client gives | Our cost per audit | Status 21.11 | Price of 1 audit / month (hypothesis) |
|---|---|---|---|---|---|
| **I. Tezkor / Express** | Passive technical scan of one site (up to 30 pages): data flows and server countries vs the CMR 415 list, trackers before consent, session replay, forms (personal-data fields, consent, where data goes), personal data and Uzbek IDs in URLs, cloud databases and AI services in page code, biometric capture, HTTPS and headers, policy present or not | nothing (any public URL) | seconds of a browser; no LLM | built | **100,000 UZS** (~$8.4) |
| **II. To'liq / Full legal audit** | Everything in I (up to 50 pages) + reading the privacy policy and offer (LLM extracts, code verifies quotes), "policy says vs site does", per-service coverage in the policy, e-commerce transparency checks (pilot, D-027), verbatim law citations from lex.uz (via lex-rag), signed evidence pack, PDF, fine range when verified | nothing | + one LLM call (~$0.15–0.34, v1 §7) | built / being built 21.11 | **250,000 UZS** (~$20.9) |
| **III. Faol / Active** | Canary form test, consent-banner Accept / Reject runs, logged-in area with a test account, API personal-data map, KYC / biometric flow, data-subject request test (M4, M5, M6, M14, M16, F-18) | written consent, domain ownership proof, test account | + analyst hours (setup, manual logins) | roadmap | **from 1,500,000 UZS** (~$125) |
| **IV. Ekspert / Expert** | Record of processing, mobile app check, inside scan of storage regions, launch check for a new app, automated-decision review, partner-lawyer review, fixed documents (M7, M8, M9, M13, M15, M12, M11) | documents, test builds, read-only access from inside | days of analyst and lawyer work | roadmap | **from 5,000,000 UZS** (~$418); anchor: Pactum charges from 5,000,000 UZS for a privacy policy alone (v1 §2) |

### 2. Monthly price by number of audits (computed, UZS; in brackets: per audit)

Curve for I–II: +100% / +50% / +40% / +35% for each next audit. Curve for III–IV: +100% / +75% / +65% / +60%.

| Audits in a month | I. Express | II. Full | III. Active | IV. Expert |
|---|---|---|---|---|
| 1 | 100,000 | 250,000 | 1,500,000 | 5,000,000 |
| 2 | 150,000 (75,000) | 375,000 (187,500) | 2,625,000 (1,312,500) | 8,750,000 (4,375,000) |
| 3 | 190,000 (63,333) | 475,000 (158,333) | 3,600,000 (1,200,000) | 12,000,000 (4,000,000) |
| 4 | 225,000 (56,250) | 562,500 (140,625) | 4,500,000 (1,125,000) | 15,000,000 (3,750,000) |
| 5 | 260,000 (52,000) | 650,000 (130,000) | 5,400,000 (1,080,000) | 18,000,000 (3,600,000) |
| 10 | 435,000 (43,500) | 1,087,500 (108,750) | 9,900,000 (990,000) | 33,000,000 (3,300,000) |

The discount counts **within one category**. Categories add up: 3 × II + 1 × III = 475,000 + 1,500,000 =
**1,975,000 UZS** in that month.

### 3. Typical buyers (examples, not forecasts)

| Buyer | What they take in a month | Price, UZS |
|---|---|---|
| Small online shop | 1 × II (full audit once a month) | 250,000 |
| Shop with weekly monitoring | 1 × II + 4 × I (weekly Express runs) | 475,000 |
| Web studio / IT Park resident checking 10 client sites before release | 10 × I | 435,000 (43,500 per site) |
| Microfinance company (when III exists) | 3 × II (3 domains) + 1 × III | 1,975,000 |
| Bank, telecom, Ministry of Justice pilot | contract by scope (v1 formula as a floor) | by agreement |

### 4. Tokens: rules

| Rule | Value | Why |
|---|---|---|
| What one token buys | one audit of one site (registrable domain), one run; I: up to 30 pages, II: up to 50 pages | clear unit for the buyer, bounded cost for us |
| How tokens are bought | in the profile, per category, for the coming month; the discount curve is applied to the quantity | "pay only for what you use" |
| Unused tokens | carry over to the next month once, then expire | fair to the buyer, no endless liability for us |
| Mixing | any number of any category | the hybrid the team asked for |
| Monitoring | a schedule (weekly, monthly) that spends the user's tokens automatically | monitoring = buying more Express tokens at the volume price |
| Always free | law-change re-check of saved scans; one re-check within 14 days after a paid audit | no new crawl for the first; keeps users fixing, costs us one scan |
| Payment | demo: manual top-up; then Payme / Click (UZS) | roadmap (F-38) |

### 5. The free audit: what the user sees

| Part of the report | Free (after registration) | Paid (category I or II) |
|---|---|---|
| Score 0–100 and counts 🔴🟡⚪ | yes | yes |
| Titles and levels of **all** findings | yes (we never hide that a violation sign exists) | yes |
| One finding fully open (the most severe) | yes | all |
| Evidence (hosts, requests, form fields), law quotes, how to fix | no | yes |
| World map of data flows | countries only, no hosts | full |
| PDF, share link, HAR | no | yes (II: signed evidence pack) |
| Number of free audits | 1 per account | — |

### 6. Floor check (internal): price must stay above cost

Cost inputs from v1 §5 and §7 (assumptions where marked there). The lowest per-audit price is at 10+ audits.

| Category | Lowest price per audit | Main cost per audit (v1 rate card) | Result |
|---|---|---|---|
| I | 35,000 (35% of 100k) | browser ~0.0006 $ per page → about 30 pages ≈ 220 UZS + support share | large margin |
| II | 87,500 (35% of 250k) | + document analysis 1,676 UZS (LLM) | large margin |
| III | 900,000 (60% of 1.5M) | test-account setup 131,548 + manual logins 9,376 per run + analyst hour 131,548 → roughly 300,000 (assumption) | about 3× cost |
| IV | 3,000,000 (60% of 5M) | launch report 400,630 + per-screen and per-table work + lawyer hours → roughly 1–1.5M (assumption) | about 2–3× cost |

### 7. What registration means for Probo itself

Registration makes Probo an **operator of personal data** under ZRU-547. Before accounts go live:
- our own privacy policy and terms (R-08, Role 2); consent checkbox not pre-ticked;
- minimum data: e-mail and a password hash; no phone number unless SMS login is added;
- the server already runs in Uzbekistan (egress IP: Uzbektelekom, AS8193, checked 21.11) — not required for e-mails
  under the new art. 27¹, but a good answer to "where do you store our data?";
- **we scan probo.aicenterkk.tech with Probo and publish the result** — a pitch line and an honesty test.

## Features for the product (§10 format)

| ID | Feature | What it gives | Complexity | Proposed by | Status |
|---|---|---|---|---|---|
| F-36 | Registration (e-mail) + one free Express audit with a partial report | The funnel: sample → account → first audit | M | Team (Role 1) | Final (screens to agree first) |
| F-37 | Token wallet per category with the volume curve; monitoring spends tokens | The pricing model of this file | M | Team (Role 1) | Final (demo top-up, no real payments) |
| F-38 | Payme / Click payments in UZS | Real revenue | M | Team | Roadmap |

## Questions for the team

1. **Role 3 (R-06):** test the four prices and the curve in interviews. Main questions: is 250,000 UZS per full audit
   acceptable for a small shop; do web studios want 10 × I at 435,000; is "tokens" understandable, or should the UI
   say "audits"?
2. **Role 3:** recompute TAM / SAM / SOM in `market.md` with these prices (v1 used the formula prices).
3. **Role 2 (R-08):** our own policy and terms for accounts; the disclaimer for partial (free) reports.
4. **Team:** should the free audit renew every month (lead magnet) or stay one per account (as decided now)?

## Sources

- `research/business-model.md` v1: comparables (§1–§2), cost inputs (§7), rate card (§5), trust model (§4)
- https://pactum.uz/services ; https://pactum.uz/ceny — local price anchors (read by research 20.11.2026)
- https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/ — 1 USD = 11,971.64 UZS
- Prices in section 2 computed with code from the curves above (21.11.2026)
