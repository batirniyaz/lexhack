# Plans v8: four plans from 99,000 to 890,000 UZS, 3 audits a month, extra credits, business model, market from auditable services

- Author: [name], research team; prepared with Claude Code
- Date/time: 21.11.2026, 14:00 (v8: every plan 100,000 UZS cheaper than v7; Tezkor becomes self-serve to stay profitable. 14:00: problems rewritten as customer problems; TAM and SAM include small online businesses; CAC and LTV marked internal)
- Passport version: 0.16
- Confidence:
  - **high** for the arithmetic (one script) and the counts of named services (official or audit-firm sources);
  - **low** for prices, staff minutes, CAC, churn, the 5% share of small businesses that sell online, and client counts. These are assumptions for R-06.

> **What this file is.** A proposal for the public pricing. It builds on three sources:
> - `checks-by-difficulty.md` (D-031): 30 checks in four groups;
> - `business-model-v2.md` (D-026): categories and tokens;
> - the v4 cost rate card (`business-model.md` §5, `pricing.md` §4).
>
> It changes D-026 from tokens per category to plans + extra credits, so **Role 1 logs the decision**. Per D-032 there are no accounts or payments in the hackathon product, so the plans are for the pitch.
>
> Currency: 1 USD = 11,971.64 UZS (CBU, 20.11.2026, [cbu.uz](https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/)).

## Conclusions

1. **Four plans; the most expensive includes all 30 checks.** Every plan includes **3 audits a month**; more audits are paid with **extra credits**.

   | Plan (uz / ru) | For whom | Checks | Price / month | Our cost / month | Margin after 2% fees | Extra audit |
   |---|---|---|---|---|---|---|
   | **Tezkor / Экспресс** (self-serve) | small online businesses | 11 | **99,000 UZS** ($8.3) | 30,823 | 66.9% | 35,000 |
   | **To'liq / Полный** | clinics, schools, mid-size services | 19 | **299,000 UZS** ($25.0) | 52,673 | 80.4% | 79,000 |
   | **Faol / Активный** | lenders, online platforms, insurers | 25 | **590,000 UZS** ($49.3) | 128,768 | 76.2% | 99,000 |
   | **Ekspert / Эксперт** | banks, payment services, apps | all 30 | **890,000 UZS** ($74.3) | 249,697 | 69.9% | 149,000 |

2. **Tezkor is self-serve.** Without human support its cost falls from 48,890 to 30,823 UZS a month, so 99,000 still earns 67%. With support it would earn only 49%. Help comes from the report itself ("how to fix" under every finding) and from written answers.

3. **Ekspert keeps all 30 checks but runs the expensive expert work less often.**
   - The mobile app is checked in every audit, with a deep run each quarter.
   - The storage check and the automated-decision review run once a year.
   - The launch check runs once, at connection.

4. **No setup fee. Faol and Ekspert need a 12-month contract.**
   - **What connection costs us, once:** 621,093 UZS (Faol) and 2,286,395 UZS (Ekspert).
   - **First-year margin:** 67.4% (Faol) and 48.5% (Ekspert). From the second year, the full margin.

5. **Market, counted from services that collect personal data** (base case, per year):

   | Measure | UZS | USD | Who |
   |---|---|---|---|
   | TAM | **57.9 bn** | $4.8M | 7,050 named services (28.9 bn) + 24,455 small online businesses (29.1 bn, assumption: 5% of small companies) |
   | SAM | **46.1 bn** | $3.9M | those with a site or app that collects data: 17.1 bn named + 29.1 bn small |
   | SOM, year 3 | **2.89 bn** | $241k | 889 clients + one Ministry of Justice contract |
   | – of which subscriptions (3.3% of SAM) | 1.54 bn | $129k | |
   | – of which one Ministry of Justice contract | 1.35 bn | $112k | |

6. **Business model:**
   - **LTV/CAC:** small business 6.6, clinic 4.0, lender 9.4, payment service 9.5, bank 21.3.
   - **Payback:** 3–10 months.
   - **Break-even:** 117.8M UZS of monthly revenue, reached about October 2029.
   - **Cash need:** about **1.56 bn UZS (~$130k)**.
   - **The cost of lower prices:** compared with v7, break-even comes about 10 months later and the team needs about $17k more.

7. **Free in every plan:** a re-check when the law changes, and one "I fixed it" re-check a month. Fixed documents and a lawyer's review only through a partner law firm (R-08).

## Data

### 1. The customer's problems we solve (the sales story)

Probo is a **legal compliance check** of a website or app: does the service, as it actually works, meet what the law requires? Each problem is written the way a business owner says it, followed by what Probo gives. It covers several laws at once: ZRU-547 (personal data), ZRU-792 (e-commerce), Law 221-I (consumer rights) and the Law on the state language. Law facts: `legal-norms.md` (R-01), `legal-ecommerce.md`, `PASSPORT.md` §2.

| # | What the customer says | Why it happens | What Probo gives |
|---|---|---|---|
| 1 | **"We don't know if our site or app meets the law."** | Every business that takes applications, orders, bookings or registrations online is a personal-data operator under ZRU-547. The law sets many requirements at once: a privacy policy with set content (arts. 22–23), consent before collecting data, notices on forms, extra rules for health, children's and biometric data, rules on storage and transfer. Online stores also need seller details, a public offer, return terms and an Uzbek version. Nobody checks all of this together | One report on all requirements: what is missing, the exact article, how to fix it |
| 2 | **"The law changes and we can't keep up."** | The rules keep changing: in 2026 ZRU-1125 amended art. 27¹ of ZRU-547 and CMR No. 415 approved a list of countries; from 12.12.2026 ZRU-1173 makes return terms a required part of an e-commerce offer (`legal-ecommerce.md`) | A free re-check of the last report whenever a relevant law changes |
| 3 | **"Our documents look fine, but does the site actually work that way?"** | Lawyers check documents. The site is built and changed by marketers and developers, so the policy and the real site drift apart | Probo compares what the policy promises with what the service actually does |
| 4 | **"A legal check is expensive and out of date in a week."** | It needs a lawyer plus a developer: a consultation costs 300,000 UZS an hour ([pactum.uz/ceny](https://pactum.uz/ceny)), a privacy policy from 5,000,000 UZS ([pactum.uz/services](https://pactum.uz/services)). Then the site changes again | 3 audits a month from 99,000 UZS |
| 5 | **"We need to show that we comply."** | When a partner, an investor or an inspector asks, the company has nothing to show | A signed report (PDF and share link) with the date, what was checked and the result |

**How the same problems sound per client type (for sales conversations):**

- **Online shop:** "Do we have everything the law requires: public offer, seller details, return terms, an Uzbek version, consent on the order form?" → Tezkor or To'liq.
- **Clinic:** "Our appointment form asks about health. Do we have the consent and notice the law requires for this special data?" → To'liq.
- **Private school or training center:** "Parents register their children on our site. Is our consent text right?" → To'liq.
- **Lender, insurer, e-commerce platform:** "Our forms ask for passport and PINFL, and clients have a personal account. Does all of it meet the law, including the account area?" → Faol.
- **Bank or payment service:** "We have 25 sites and a mobile app, and need monthly proof that each one complies." → Ekspert + credits.

**Positioning rule:** Probo is legal tech, not a cybersecurity product. In sales and in the pitch, talk about legal requirements, compliance and evidence, not about leaks, attacks or vulnerabilities (`cyber-differentiation.md`, D-008).

### 2. What each plan includes

Check numbers are from `checks-by-difficulty.md` §1. Every report includes:
- the law text under each finding;
- the data-flow map;
- the law-change status;
- the evidence seal;
- a PDF and a share link.

| Plan | Adds | What the client gives | Pages per audit |
|---|---|---|---|
| **Tezkor** (checks 1–11) | HTTPS, security headers, policy present, trackers before consent, session recording, transfers outside the CMR 415 list, sensitive form fields, consent on forms, selfie or camera access, Uzbek version of a store, DNS and mail map | nothing | 30 |
| **To'liq** (12–19) | where form data goes, cloud databases in code, personal data in URLs, policy against arts. 22–23, services named in the policy, seller identity, offer and returns, policy against behaviour | nothing | 50 |
| **Faol** (20–25) | "Reject" stops trackers, canary forms (3), logged-in area (1 test account), API personal-data map (up to 50 endpoints), KYC flow (quarterly), data-subject request test (quarterly) | written permission, domain ownership proof, test account | 50 + banner runs + logged-in pages |
| **Ekspert** (26–30) | mobile app (each audit + a deep run quarterly), record of processing (1 process), storage regions (yearly), automated-decision review (yearly), launch check of a new app (at connection) | documents, app build, read-only access | as Faol |

**Plan rules:**
- **One site per plan.** Other sites are audited with credits; a plan can buy credits of its own level or lower.
- **Audits:** 3 a month, about every 10 days. Unused audits carry over once (D-026 rule).
- **Credits:** valid 12 months (**assumption**).
- **Support:** Tezkor has written help only; the other plans include human support.

### 3. Our cost per plan (UZS per month, v4 rate card)

The inputs:
- platform share 28,085 (law tracking, rule upkeep, alerts, billing, free law-change re-check);
- human support: 15 minutes a month + 5 minutes per site = 18,752 (not in Tezkor);
- 7.18 per page visit;
- 469 run triage per audit;
- 1,676 per AI document reading;
- 962 per canary form per run;
- 469 per automatic test login;
- 453 per API endpoint per month;
- KYC run 65,894; data-subject request test 61,015;
- app static check 14,352, deep run 132,745;
- 16,942 per process per month;
- 66,971 per data store;
- decision review 133,224;
- launch check 737,285.

| | Tezkor | To'liq | Faol | Ekspert |
|---|---|---|---|---|
| Platform share | 28,085 | 28,085 | 28,085 | 28,085 |
| Human support | — | 18,752 | 18,752 | 18,752 |
| Audits | 2,738 (3 + 1 free re-check) | 2,484 | 13,626 | 56,682 (incl. app check) |
| AI reading of policy + offer | — | 3,352 | 3,352 | 3,352 |
| API map (50 endpoints) | — | — | 22,650 | 22,650 |
| KYC + data-subject request test, quarterly | — | — | 42,303 | 42,303 |
| App deep run, quarterly | — | — | — | 44,248 |
| Record of processing, 1 process | — | — | — | 16,942 |
| Storage regions + decision review, yearly | — | — | — | 16,683 |
| **Cost per month** | **30,823** | **52,673** | **128,768** | **249,697** |
| One-off connection (12-month contract) | — | — | 621,093 | 2,286,395 |

### 4. Prices and margins

| Plan | Price | Price ÷ cost | Margin | After 2% fees | First year with connection cost |
|---|---|---|---|---|---|
| Tezkor | 99,000 | 3.2× | 68.9% | 66.9% | 66.9% |
| To'liq | 299,000 | 5.7× | 82.4% | 80.4% | 80.4% |
| Faol | 590,000 | 4.6× | 78.2% | 76.2% | 67.4% |
| Ekspert | 890,000 | 3.6× | 71.9% | 69.9% | 48.5% |

**How this compares with the floor and the market:**
- Tezkor and Ekspert are now below the team's "price ≥ 4× cost" floor (D-026). This is a deliberate choice for the Uzbek market.
- Typical software companies earn about 75–80% gross margin ([Aleph / Benchmarkit](https://www.getaleph.com/answers/saas-gross-margin-2026); [SaaS Rise](https://saasrise.com/blog/saas-benchmark-report-2026), read via search summaries). Our blended margin is 71%.

**Extra credits.** One credit = one more audit of one site. The cost shown is for an audit of another site, in the worst case.

| Credit | Price | Our cost | Margin |
|---|---|---|---|
| Tezkor | 35,000 | 5,372 | 84.7% |
| To'liq | 79,000 | 13,656 | 82.7% |
| Faol | 99,000 | 13,449 | 86.4% |
| Ekspert | 149,000 | 27,801 | 81.3% |

**Price by number of audits (To'liq):**
- 3 audits: 299,000;
- 4 audits: 378,000 (×1.26);
- 5 audits: 457,000 (×1.53);
- 30 audits: 2,432,000 (×8.1, against ×10 if linear).

**Market check:**
- **Tezkor** is half the price of Pactum's legal subscription (199,000 / 30 days).
- **To'liq** is about one lawyer-hour (300,000).
- **Ekspert** is below one Quantum IT SYS "GDPR / ISO assessment from 2M UZS" (`csec.md`).

### 5. Typical clients

| Client | What they take | Bill / month | Our cost | Gross profit after fees |
|---|---|---|---|---|
| Small online business | Tezkor | 99,000 | 30,823 | 66,197 (66.9%) |
| Clinic / private school | To'liq | 299,000 | 52,673 | 240,347 (80.4%) |
| Lender, e-commerce platform or insurer, 3 sites | Faol + 2 To'liq credits | 748,000 | 156,080 | 576,960 (77.1%) |
| Payment service, 3 sites | Ekspert + 2 To'liq credits | 1,048,000 | 277,009 | 750,031 (71.6%) |
| Bank, 25 sites | Ekspert + 24 To'liq credits | 2,786,000 | 577,441 | 2,152,839 (77.3%) |
| Ministry of Justice, per organization | 1 To'liq credit a quarter | 26,333 | 4,552 | 21,254 (80.7%) |

### 6. Unit economics (internal, not for the pitch)

We have no paying clients yet, so CAC and LTV below are assumptions for the team's own planning. The pitch shows only margins, break-even and TAM / SAM / SOM.


**Definitions:**
- **CAC (client acquisition cost):** what we spend on marketing and sales to win one paying client.
- **LTV (lifetime value):** the gross profit a client brings over the whole time they stay.
  - Formula: gross profit per month ÷ monthly churn, minus the one-off connection cost.
  - For example, 5% churn means the average client stays 20 months.
- **Rule of thumb:** LTV/CAC above 3 is healthy.

**CAC assumptions:**
- 0.2M for self-serve Tezkor (online ads + free sample report; lower than v4's 0.5M because there is no salesperson);
- 2M for a clinic;
- 3M for a lender;
- 5M for a payment service;
- 10M for a bank.

**Churn per month:** 5% / 3% / 2% / 1.5% / 1%.

| Client | Gross profit / month | Stays (months) | LTV | CAC | LTV/CAC | Payback |
|---|---|---|---|---|---|---|
| Small online business | 66,197 | 20 | 1.3M | 0.2M | **6.6** | 3.0 months |
| Clinic / school | 240,347 | 33 | 8.0M | 2M | **4.0** | 8.3 months |
| Lender / platform / insurer | 576,960 | 50 | 28.2M | 3M | **9.4** | 6.3 months |
| Payment service | 750,031 | 67 | 47.7M | 5M | **9.5** | 9.7 months |
| Bank | 2,152,839 | 100 | 213.0M | 10M | **21.3** | 5.7 months |

Payback = (CAC + connection cost) ÷ gross profit per month.

### 7. Break-even and three years (base case)

**Break-even.** Fixed costs are 83.666M UZS a month (`business-model.md` §9). At the blended margin of 71.0%, break-even is **117.8M UZS of monthly revenue**.

**Three-year assumptions:**
- the client counts at year end shown in the table;
- revenue on the average number of clients;
- acquisition = new clients (including replacements for churn) × CAC, which replaces the marketing line, so fixed costs here are 71.694M a month;
- one Ministry of Justice contract (4,258 organizations) in 2029.

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Clients at year end: small / clinic / lender / payment / bank | 150 / 10 / 3 / 0 / 0 | 450 / 30 / 10 / 2 / 2 | 800 / 60 / 20 / 5 / 4 |
| Revenue | 121M ($10k) | 533M ($44k) | 2,528M ($211k) |
| – of which Ministry of Justice | 0 | 0 | 1,346M |
| Gross profit | 82M (68%) | 361M (68%) | 1,903M (75%) |
| Acquisition | 73M | 208M | 340M |
| Fixed costs | 860M | 860M | 860M |
| **Operating result** | **−851M** | **−708M** | **+703M** |
| Cumulative | −851M | −1,559M ($130k) | −856M |
| Monthly revenue at year end | 20.1M | 68.7M | 128.5M |

How to read it:
- Monthly revenue passes break-even (117.8M) about October 2029.
- The team needs about **1.56 bn UZS** before the plans pay for themselves.
- Without the Ministry of Justice contract, 2029 still loses money. At these prices we need more clients than in v7, or the contract.

### 8. Market from auditable services

**Named services** (count × monthly bill of §5 × 12):

| Who | Count | Source | Bill / month | TAM, UZS / year | SAM share | SAM |
|---|---|---|---|---|---|---|
| Private clinics (5,929), private schools (551), private universities (97) | 6,577 | `market.md` §2 | 299,000 | 23.60 bn | 50% have a site or app that collects data (**assumption**) | 11.80 bn |
| Microfinance and other non-bank lenders | 237 | `market.md` §2 (Central Bank) | 748,000 | 2.13 bn | 100% | 2.13 bn |
| E-commerce platforms | 115 | `market.md` §2 (NAPP) | 748,000 | 1.03 bn | 100% | 1.03 bn |
| Insurance companies | 35 | [UzDaily, H1 2026](https://www.uzdaily.uz/en/infographics/uzbekistans-insurance-market-h1-2026-results/) | 748,000 | 0.31 bn | 100% | 0.31 bn |
| Payment organizations | 51 | [KPMG, 09.2026](https://kpmg.com/uz/en/insights/2026/09/overview-of-payment-organizations.html) (not checked against the Central Bank register) | 1,048,000 | 0.64 bn | 100% | 0.64 bn |
| Banks | 35 | `market.md` §2 (Central Bank) | 2,786,000 | 1.17 bn | 100% | 1.17 bn |
| **Total** | **7,050** | | | **28.88 bn ($2.4M)** | | **17.08 bn ($1.4M)** |

**Small online businesses (assumption).** Shops, delivery, travel, real estate and training centers: 489,100 small and micro companies (`market.md` §2) × 5% that take orders or applications online (**assumption, no source**) = 24,455 × 99,000 × 12 = **29.1 bn UZS ($2.4M)**.

**SAM total:** 17.08 bn (named services) + 29.05 bn (small online businesses, all assumed to collect data online) = **46.13 bn UZS ($3.9M)**. TAM total: 28.88 + 29.05 = **57.93 bn UZS ($4.8M)**.

**Ministry of Justice (counted separately).** 21,292 organizations × 26,333 UZS × 12 = **6.7 bn UZS** a year; 2.7 bn if 40% have a site.

**Not counted yet (no sourced count):** telecom operators, delivery and taxi apps, online shops on their own sites, travel agencies, real-estate developers.

**SOM, year 3 (2029, year-end run rate):**

| Who | Clients | UZS / year |
|---|---|---|
| Small online businesses (Tezkor) | 800 (3.3% of 24,455) | 950M |
| Clinics and schools (To'liq) | 60 (1.8% of 3,288) | 215M |
| Lenders, platforms, insurers (Faol + 2 credits) | 20 (5% of 387) | 180M |
| Payment services (Ekspert + 2 credits) | 5 of 51 | 63M |
| Banks (Ekspert + 24 credits) | 4 of 35 | 134M |
| **Subscriptions** | 889 | **1,542M ($129k)** |
| One Ministry of Justice contract | 4,258 organizations | 1,346M ($112k) |
| **Total** | | **2,888M ($241k)** |

### 9. Pitch line (uz, ru — drafts, a native speaker checks)

- **uz:** To'rtta tarif, har birida oyiga 3 ta audit: Tezkor — 99 000 so'm, To'liq — 299 000 so'm, Faol — 590 000 so'm, Ekspert — 890 000 so'm. Qo'shimcha audit 35 000 so'mdan.
- **ru:** Четыре тарифа, в каждом 3 аудита в месяц: Экспресс — 99 000 сум, Полный — 299 000 сум, Активный — 590 000 сум, Эксперт — 890 000 сум. Дополнительный аудит — от 35 000 сум.

## Questions for the team

1. **Role 1 (decision):** do plans with 3 audits and extra credits replace D-026's tokens per category? Tezkor and Ekspert are below D-026's 4× cost floor by choice; the decision log should say so.
2. **Alii / R-06:** test 99,000 / 299,000 / 590,000 / 890,000 in the interviews.
3. **Team:** is 5% of small companies taking orders online a fair assumption? It drives half of the market.
4. **Team:** should insurers be on Faol or Ekspert?

## Sources

- `research/checks-by-difficulty.md` (D-031); `PASSPORT.md` 0.16 (D-026, D-031, D-032)
- `research/business-model.md` §5, §8, §9 and `research/pricing.md` §4: rate card, CAC, churn, fixed costs
- `research/market.md` §2: counts of banks, lenders, e-commerce platforms, clinics, schools, universities and small companies
- Insurance companies: https://www.uzdaily.uz/en/infographics/uzbekistans-insurance-market-h1-2026-results/
- Payment organizations: https://kpmg.com/uz/en/insights/2026/09/overview-of-payment-organizations.html
- Pactum: https://pactum.uz/ceny , https://pactum.uz/services ; Quantum IT SYS via `research/csec.md`
- SaaS margins: https://www.getaleph.com/answers/saas-gross-margin-2026 , https://saasrise.com/blog/saas-benchmark-report-2026
- CBU rate 20.11.2026: https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/
- All computed numbers: one Python script (21.11.2026)
