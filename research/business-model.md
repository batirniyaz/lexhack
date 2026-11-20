# Business model, services, prices and unit economics of Probo

- Author: [name], research team; prepared with Claude Code
- Date/time: 21.11 00:10 (v2: modular services, cost-based price formula, credential trust model); v3 21.11 00:55 (sector packs and services M13–M16 from `service-catalog.md`)
- Passport version: 0.10 (the task brief named 0.5; the repo was at 0.10 when this file was written)
- Confidence: **high** for competitor prices, LLM prices, wages and what the code does today (read 20.11.2026); **low** for staff minutes per unit, CAC and churn (assumptions to measure in a pilot)

> Product name: **Probo** (working name Qalqon in the passport, D-014). Builds on passport §4 (three access levels), §5 (check catalog), §7 (business model) and decisions D-007 (subscription is the main revenue), D-008 (no vulnerability scanning) and D-009 (passive mode for non-clients).
> USD at the CBU official rate for 20.11.2026: **1 USD = 11,971.64 UZS** ([cbu.uz](https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/)). Market sizes are in `research/market.md`.

## Conclusions

1. **The old 199,000 UZS "Start" price did not include everything.** It covered only the passive website check of one domain, with weekly rescans and alerts. APIs, logged-in areas, canary tests, business-process review, mobile apps and inside scans are separate modules (section 3). Open ports, exposed server files and other vulnerability checks are **not offered** (D-008); we refer those clients to the Cybersecurity Center or licensed firms.
2. **Price = 4 × our cost, for every module and every client.** Monthly price = 4 × (account base + Σ quantity × unit cost × frequency). The quantities (domains, pages, forms, API endpoints, test accounts, apps, processes, data stores) come from a free discovery scan or the client's declaration. A bank therefore pays for its size, a small shop pays for its size, and both give a **75% gross margin** (73% after payment fees). One number, the **Probo Scale Unit (PSU) = 1,000 UZS of our cost**, turns any scope into a price: **price = 4,000 UZS × PSU**.
3. **What the formula gives:** small site **187,000 UZS/month (~$15.6)**; clinic or private school **253,000 (~$21)** + 2.2M one-off; microfinance or e-commerce platform **1.53M (~$128)** + 9.1M one-off; bank or telecom **7.7M (~$643)** + 25.9M one-off (9.7M with apps and inside scans later). The small-site price sits inside the global range ($10–25 per site); the bank price is about $7.7k a year, below the ~$10k-a-year floor reported for OneTrust (`NOT VERIFIED`).
4. **Clients only give us access they choose, step by step,** and never real customer data. The ladder: nothing → proof of domain ownership → a test account → our scanner running inside their network → read-only schema access. Probo itself keeps secrets in a separate vault, masks tokens and personal data before storage, sends only public documents and masked facts to the LLM, deletes evidence on a schedule and shows the client every request it made (section 4).
5. **Unit economics stay healthy at a uniform 75% margin:** LTV/CAC 5.5× for small sites, 3.9× for clinics, 12–29× for regulated and large clients; one-off onboarding fees cover most of the acquisition cost of larger clients. Break-even is **about 115M UZS MRR (~$9.6k)** for three founders; base year-3 SOM is 235M UZS MRR.
6. **v3: services follow the law and the client's sector** (`service-catalog.md`). The client picks a sector (bank, microfinance, clinic, e-commerce, education, telecom…), we verify it and the system's size, the sector's legal pack pre-ticks the services its ZRU-547 articles require, and the client ticks extras. Four services were added: launch check for new apps (M13), KYC/biometrics (M14), scoring decisions (M15), data-subject requests (M16).

## Data

### 1. Global comparables (official pricing pages, read 20.11.2026)

| Product | Plans and prices | Billed per | Key limits | Source |
|---|---|---|---|---|
| Cookiebot (Usercentrics) | Free; Premium Lite €7/mo; Small €15; Medium €30; Large €50; XLarge €90 per domain per month; daily automated scans +€99/mo | domain | by subpages: ≤50 / ≤350 / ≤3,500 / ≤7,000 / >7,000 | [cookiebot.com/en/pricing](https://www.cookiebot.com/en/pricing/) |
| Usercentrics Web CMP | Free; Essential €7; Plus €15; Pro €30; Business €50 per month | account | 1 / 1 / 3 / 10 domains; 1,500–50,000 sessions | [usercentrics.com/pricing](https://usercentrics.com/pricing/) |
| Termly | Free; Starter $14/mo monthly ($10 annual); Pro+ $20 monthly ($15 annual); Agency custom | website | Pro+: unlimited policies, weekly scans | [termly.io/pricing](https://termly.io/pricing/) |
| iubenda | Essentials $6.99 monthly ($5.99 yearly); Advanced $27.99 ($24.99); Ultimate $119.99 ($99.99) | site | 25k / 50k / 150k pageviews | [iubenda.com/en/pricing](https://www.iubenda.com/en/pricing) |
| CookieYes | Free; Basic $10; Pro $25; Ultimate $55 per month; annual = 10 months | domain | 600 / 4,000 / 8,000 pages per scan | [cookieyes.com/pricing](https://www.cookieyes.com/pricing/) |
| Osano | Free; Plus $199/mo; Basic Privacy custom | account | Plus: 3 domains, 30,000 monthly visitors | [osano.com/plans/cookie-consent](https://www.osano.com/plans/cookie-consent) |
| OneTrust | no public price ("Get Pricing"), metered by average daily visitors | account | — | [onetrust.com/pricing](https://www.onetrust.com/pricing/); third-party blogs cite a ~$10k/year floor: `NOT VERIFIED` |

Note: the global tools also price by scale (pages, pageviews, sessions, domains). None of them covers Uzbek law or the Uzbek and Russian languages (passport §8; R-04 to confirm).

### 2. Local comparables

| Who | Offer | Price | Source | Checked |
|---|---|---|---|---|
| Pactum (legal marketplace) | "Политика конфиденциальности" (privacy policy), category "Защита персональных данных" | **from 5,000,000 UZS** (~$418) | [pactum.uz/services](https://pactum.uz/services) | opened 20.11 |
| Pactum | 60-minute consultation | 300,000 UZS (~$25) | [pactum.uz/ceny](https://pactum.uz/ceny) | opened |
| Pactum | "Юридический автопилот" (legal autopilot) subscription | 199,000 UZS per 30 days (~$16.6) | [pactum.uz/ceny](https://pactum.uz/ceny) | opened |
| Pactum | a dedicated "PD operator document kit" or State Register registration service | not listed | [pactum.uz](https://pactum.uz) | `NOT VERIFIED` that it exists |
| Cybersecurity Center (csec.uz) | web-resource security examination (225 in 9 months of 2026) | no public price list; services page empty | [csec.uz](https://csec.uz), [csec.uz/uz/services](https://csec.uz/uz/services) | price `NOT VERIFIED` (R-09: call) |
| Other private PD audit offers in Uzbekistan | none found | — | — | `NOT VERIFIED` |

### 3. Service catalog: what we can technically check, and what access it needs

Access levels follow passport §4: **L1** passive, as an ordinary visitor (any site, D-009); **L2** active with the client's written consent (forms, test account); **L3** inside, with read-only access the client grants.

| ID | Module | What it checks | Access | Status in code (21.11) | Constraint | Price driver |
|---|---|---|---|---|---|---|
| M1 | **Website privacy scan** | Cookies before and after consent; trackers and pixels; session recording (Webvisor, Clarity…); every third-party host with owner company and server country (data-flow map); site hosting country; forms, personal-data fields and consent; where forms send data; personal data in URLs; cloud databases and storage visible in page code; HTTPS and security headers | L1 | **Built**: 11 detectors in `backend/qalqon/detectors/` (`trackers_before_consent`, `session_replay`, `url_pii`, `foreign_requests`, `form_submit_destination`, `baas_detect`, `form_consent`, `form_pd_fields`, `biometric_capture`, `https`, `security_headers`) | none for public pages | domains; page visits (pages × frequency) |
| M2 | **Documents: policy analysis and "says vs does"** | 10 policy elements; promises in the policy vs what the network shows | L1 | **Built** (step 5; D-020, D-021) | quotes checked by code | documents (re-analyzed only when the text changes) |
| M3 | **DNS and mail map** | MX (whose mail), SPF (which mailing services and CRMs), certificate-log subdomains (crt.sh) | L1 | Not built; F-13 (Final) | passive, no requests to the client's servers | domains |
| M4 | **Canary form test** | Fill forms with fake identities and look for them in all outgoing traffic (plain, URL-encoded, base64, SHA-256): who really receives the personal data | L2 | Not built; F-11 (Final) | D-009: clients only, written consent | forms × frequency |
| M5 | **Logged-in area** | Registration, login and personal-account pages with a test account; the same checks as M1 behind the login | L2 | Not built (passport §4 stage 2; recording mode F-14 for SMS/OneID) | D-009 | test accounts (roles) × frequency; manual login when 2FA/SMS/OneID |
| M6 | **API personal-data map** | Which first-party API endpoints send or receive personal data, to which hosts and countries, and which fields go beyond the stated purpose (data minimization). From traffic recorded during M1/M5 and, optionally, the client's API spec. Normal use only | L1 / L2 | **Partly**: the crawler already records request type and POST data (`scanner/crawler.py`); grouping and classification of endpoints not built | D-008: no fuzzing, no auth bypass, no injection | API endpoints (method + path pattern) |
| M7 | **Processing register ("business flow")** | From a questionnaire and the client's documents: data categories, purposes, recipients, storage country, retention, consent, State Register registration → a record of processing and its gaps against ZRU-547, checked against the scan facts | L3-lite (client provides information) | Not built; needs Role 2 rules | a lawyer confirms the result | business processes |
| M8 | **Mobile app check** | Static: permissions and embedded SDKs/trackers in the app package. Dynamic: app traffic in an emulator with a proxy and a test account | static L1, dynamic L2 | **Roadmap** (F-09) | legality of downloading and analyzing public app packages: Role 2 (R-08) | apps |
| M9 | **Inside scan** | Read-only access to cloud metadata or the database schema: where data is stored (region), which columns hold personal data. Never row values | L3 | **Roadmap** (F-15) | contract; agent runs on the client's side | data stores |
| M10 | **Monitoring and alerts** | Scheduled re-runs of the chosen modules; Telegram alerts for new findings and law changes (re-evaluation without a new crawl) | — | **Partly**: rescore exists (D-015); scheduler and Telegram not built (F-05, F-16) | — | frequency: monthly ×1, weekly ×4.33, daily ×30 |
| M11 | **Fix documents** | Policy, consent texts, cookie-banner settings in UZ/RU | — | Not built (F-04, Final) | Role 2: is generating documents a licensed legal service? | documents |
| M12 | **Evidence pack and lawyer review** | HAR, screenshots, timestamps; a partner lawyer's memo | — | **Partly**: HAR and facts.json exist; lawyer review via a partner | the lawyer signs, not Probo | partner's hours, billed by the partner |
| — | **Not offered: vulnerability checks** | Open ports, exposed files and backups (.git, .env), outdated software, auth bypass, pentest | — | — | **D-008**; license question V-15 | referral to the Cybersecurity Center or licensed firms |

**v3:** four more services are designed in `research/service-catalog.md`: **M13 Launch check** for new apps with no personal data yet, **M14 KYC/biometric flow**, **M15 automated-decision (scoring) check**, **M16 data-subject request test**. That file also maps every service to its ZRU-547 article, defines the **sector packs** (bank, microfinance, insurance, telecom, clinic, education, e-commerce, delivery, HR, state bodies, IT/new product), says what audit-only access each service needs and how our agent enters, and how we verify sector and size so clients can't under-declare.

How the items in the question map to modules: **cookies** → M1; **APIs** → M6; **business flow / technical statement** → M7; **server** → M1 sees hosting country, provider, headers and HTTPS, M9 sees storage region from inside; **leaks of personal data** to third parties → M1 (`url_pii`) and M4; **leaks of server files, open ports** → not offered (D-008).

### 4. Trust: how a client can give us access without risk, and how Probo itself avoids leaks

**Principle: ask for the least, keep it for the shortest time, show everything we did.**

**4.1 Access ladder (the client chooses; each rung unlocks more modules)**

| Rung | What the client gives | What it unlocks | For whom |
|---|---|---|---|
| 0 | Nothing | M1, M2, M3 (passive) | anyone, free scan |
| 1 | **Proof of domain ownership** (DNS TXT record or a file on the site) + a signed authorization letter: domains, modules, dates | M4 canary tests, scheduled active scans | SMB clients |
| 2 | **A test account, never a real one**: a dedicated user with fake data, the lowest role that shows the flow, time-limited and revocable. With SMS/2FA/OneID the client logs in in our isolated browser (recording mode, F-14) and we keep only the session for the scan window | M5, M6 behind login | clinics, schools, MFOs, e-commerce |
| 3 | **Our scanner runs inside the client's network** (a container they control); credentials never leave; only masked facts (or only the report) come out | M5, M6 for banks and telecom | banks, telecom, marketplaces |
| 4 | **Read-only schema / cloud-metadata access** for an agent that reads structure and regions, never row values | M9 | large clients, roadmap |

**4.2 Technical safeguards inside Probo**

| Risk | Safeguard | Status |
|---|---|---|
| Stolen client credentials | Separate encrypted secrets vault (not the app database), per-client keys, only the scanner process can read them, never written to logs, HAR, screenshots or LLM prompts; auto-expire after the scan window; two-person rule for staff access | to build |
| Personal data in our evidence | Canary identities only (fake data); tokens, cookies, auth headers and personal-data values masked before storage (the code already masks identifiers, `detectors/trackers.py` `_mask`); store facts rather than raw pages where possible | partly built |
| Data sent to the LLM | Only public documents (policy, offer) and masked facts go to the model; never credentials or customer records | built for documents (`llm/policy.py`) |
| Cross-client leaks | A fresh browser context per scan; no shared cookies or storage between clients | built (one context per scan) |
| Keeping data too long | Raw evidence deleted after a fixed period (proposal: 90 days, client can delete earlier; "delete account and all scans" is already in `PRODUCT.md`) | to decide |
| "What did you do on my site?" | The client sees every request we made with their access (the HAR is the evidence); our scanner uses fixed, published egress IPs and a recognizable user agent so they can allowlist and audit us | partly built (HAR) |
| Telecom data | Personal data of telecom-service users must stay in Uzbekistan (art. 27-1 as amended by ZRU-1125, passport §2, V-02). If a telecom client's logged-in scan captures subscriber data, it must be stored on servers in Uzbekistan | to decide: local hosting provider `NOT VERIFIED` |

**4.3 Contract and proof**

- Authorization letter with scope (D-009), NDA, and a data-processing agreement: we act only on the client's instructions (Role 2: our status under ZRU-547).
- Probo's own compliance: privacy policy and terms (R-08), registration of our own database in the State Register (art. 20, V-13), breach notification within the CMR No. 415 deadlines (V-12), and a published Probo scan of our own site.
- An independent security assessment of Probo itself by the Cybersecurity Center or a licensed firm (we don't pentest ourselves, D-008). It is likely needed before any integration with Ministry of Justice systems (`NOT VERIFIED`, ask at the pilot). ISO/IEC 27001 on the roadmap.
- A public "what we never do" list: no pentests, no real customer data, no reuse of credentials, no scanning of logged-in areas without a signed letter.

### 5. Price formula

**Monthly price = k × [ A + Σ over chosen modules (q × c × f) ]**
**One-off price = k × Σ (q × c)**

| Symbol | Meaning | Value |
|---|---|---|
| k | uniform multiplier for every module and client | **4** → 75% gross margin before ~2% payment fees (73% after) |
| A | account base: 15 min support, a share of law tracking and rule maintenance, alerts and billing | cost 39,755 UZS/month (see rate card) |
| q | quantity of a scale unit: domains, page visits, documents, forms, test accounts, API endpoints, apps, processes, data stores, hours | measured by a free discovery scan (sitemap pages, forms, observed API endpoints, subdomains) or declared by the client and checked at onboarding |
| c | our loaded cost per unit: compute + LLM + staff minutes × loaded hourly cost | rate card below |
| f | frequency per month | monthly 1, weekly 4.33, daily 30 |
| **PSU** | **Probo Scale Unit = 1,000 UZS of our cost**; any scope sums to one number | **price = 4,000 UZS × PSU** |

**Cost basis:** support staff 7.27M UZS/month and ICT staff 17.0M UZS/month (national averages, Jan–Sep 2026, [zamin.uz](https://zamin.uz/en/economy/225656-average-monthly-salary-in-uzbekistan-reached-7-27-million-soums.html)), × 1.3 for employer social tax of 12% ([PwC](https://taxsummaries.pwc.com/Republic-of-Uzbekistan/Individual/Other-taxes), search summary), equipment and idle time (**assumption**) → **56,256 UZS/hour support**, **131,548 UZS/hour analyst or in-house lawyer**. Browser compute $0.0006 per page visit (assumption, section 7). LLM at Claude Opus 5.5 prices (D-020). Law tracking: 0.5 FTE analyst spread over 500 accounts (assumption).

**Rate card** (price = cost × 4; USD at 11,971.64)

| Unit | Our cost, UZS | PSU | **Price, UZS** | ≈ USD |
|---|---|---|---|---|
| **Recurring, per month** | | | | |
| A · Account base | 39,755 | 39.8 | **159,022** | 13.28 |
| B · Each domain | 4,688 | 4.7 | 18,752 | 1.57 |
| C · 100 page visits (pages × runs) | 718 | 0.72 | 2,873 | 0.24 |
| D · Document analysis (each document, when it changes) | 1,676 | 1.7 | 6,704 | 0.56 |
| E · Canary test, per form per run | 962 | 0.96 | 3,846 | 0.32 |
| F · Test account per run, automatic login | 469 | 0.47 | 1,875 | 0.16 |
| F · Test account per run, manual login (SMS/2FA/OneID) | 9,376 | 9.4 | 37,504 | 3.13 |
| G · API endpoint under watch | 453 | 0.45 | 1,811 | 0.15 |
| H · Mobile app, static check (roadmap) | 14,352 | 14.4 | 57,408 | 4.80 |
| H · Mobile app, dynamic run (roadmap) | 132,745 | 132.7 | 530,979 | 44.35 |
| I · Business process upkeep | 16,942 | 16.9 | 67,769 | 5.66 |
| J · Data store, inside scan (roadmap) | 66,971 | 67.0 | 267,884 | 22.38 |
| K · Analyst / account-management hour | 131,548 | 131.5 | 526,190 | 43.95 |
| **One-off** | | | | |
| O1 · Active-mode onboarding (ownership proof, letter, vault) | 263,095 | 263.1 | 1,052,381 | 87.91 |
| O2 · Test account setup, per account | 131,548 | 131.5 | 526,190 | 43.95 |
| O3 · First mapping, per API endpoint | 4,529 | 4.5 | 18,114 | 1.51 |
| O4 · Generated document (UZ + RU, analyst-reviewed) | 36,478 | 36.5 | 145,914 | 12.19 |
| O5 · First deep check per mobile app (roadmap) | 395,840 | 395.8 | 1,583,360 | 132.26 |
| O6 · First mapping per business process | 400,629 | 400.6 | 1,602,515 | 133.86 |
| O7 · Support for a one-off report (30 min) | 28,128 | 28.1 | 112,512 | 9.40 |
| **Added in v3** (services M13–M16, see `service-catalog.md`) | | | | |
| M13 · Launch check, per screen or form reviewed (5 min analyst) | 11,202 | 11.2 | 44,807 | 3.74 |
| M13 · Launch check, per 10 database tables (structure only, 10 min) | 22,523 | 22.5 | 90,093 | 7.53 |
| M13 · Launch report, article by article (3 h) | 400,630 | 400.6 | 1,602,519 | 133.86 |
| M14 · KYC / biometric flow, per run (30 min, synthetic image) | 65,894 | 65.9 | 263,575 | 22.02 |
| M15 · Automated-decision flow review, per flow (1 h) | 133,224 | 133.2 | 532,896 | 44.51 |
| M16 · Data-subject request test, per request | 61,015 | 61.0 | 244,060 | 20.39 |
| V · Sector and size verification, regulated sectors only (one-off, 15 min) | 32,887 | 32.9 | 131,548 | 10.99 |

**One exception:** a partner lawyer's review (M12) is billed by the partner at their own rate (e.g. Pactum's 300,000 UZS/hour). Multiplying it by 4 would make it 1.2M UZS/hour and unsellable. Our in-house lawyer's time is already inside the rate card at the analyst rate.

### 6. Worked examples (presets the calculator starts from; the client can switch modules on and off)

| Client type | Scope (quantities) | Modules | **Monthly price** | **One-off** |
|---|---|---|---|---|
| **Small site** (landing, small shop) | 1 domain, 20 pages weekly, 1 policy | M1, M2, M10 | **186,966 UZS ($15.62)** | — |
| **Clinic / private school** | 1 domain, 50 pages weekly, 2 documents, 3 forms canary-tested monthly, 1 patient/student test account weekly (automatic login), 20 API endpoints | + M4, M5, M6 | **253,289 UZS ($21.16)** | 2,232,685 UZS ($186.50): onboarding, 1 test account, 20 endpoints, 2 generated documents |
| **MFO / e-commerce platform** | 3 domains, 300 pages weekly, 4 documents, 8 forms weekly, 2 test accounts weekly (1 with SMS), 120 endpoints, 3 business processes, 1 analyst hour | + M7 | **1,530,030 UZS ($127.80)**; 1,587,438 with 1 app later | 9,086,025 UZS ($759): onboarding, 2 accounts, 120 endpoints, 3 processes; 10.67M with 1 app later |
| **Bank / telecom** | 25 domains, 2,500 pages weekly + 400 pages daily, 10 documents, 15 forms weekly, 3 test accounts with 2FA weekly, 400 endpoints, 10 processes, 8 analyst hours | all available | **7,699,442 UZS ($643)**; **9,679,867 ($809)** with 2 apps and 3 data stores later | 25,901,828 UZS ($2,164); 29.07M with 2 app deep checks later |
| **Fix pack** (one-off, any small site) | 1 scan of 50 pages + rescan after fixes, policy analysis, 3 generated documents, 30 min support | M1, M2, M11 | — | **559,830 UZS ($46.76)** |
| **B2G, per organization** | 1 domain, 20 pages monthly, 1 document; the account base is per legal service center, not per organization | M1, M2 | **26,031 UZS ($2.17)** | — |

**With sector packs (v3, `service-catalog.md` §7):** the sector pre-ticks the services its law requires, so the presets become: clinic **334,642 UZS/month** (adds a quarterly data-subject request test); microfinance **2,052,590** (adds a KYC run and a quarterly scoring review); bank **8,663,209** (adds 2 KYC runs, 2 scoring flows and a request test); a new app's launch check **4,108,020 one-off**.

What changes compared with the first version of this file: prices are no longer fixed plans. Small sites now pay a little less (187,000 instead of 199,000 UZS), large clients pay for what they use (a bank 7.7M instead of 3.9M UZS), and the margin is the same 75% everywhere. The Fix pack drops from 1.49M to 0.56M UZS because generating documents costs us little. Cost-based pricing gives up some value-based upside there (a lawyer charges from 5M UZS for a policy alone), so R-06 should still test both prices.

### 7. Cost inputs

| Item | Value | Source / status |
|---|---|---|
| Claude Opus 5.5 (current default, D-020) | $4 input / $20 output per 1M tokens; cache hits $0.20; Batch API −50% | [Claude pricing](https://platform.claude.com/docs/en/about-claude/pricing), read 20.11.2026 |
| Claude Sonnet 5.5 / Haiku 5.5 | $2 / $10 and $0.10 / $0.50 per 1M tokens | same |
| Tokens per policy analysis | typical 20k in / 3k out → **$0.14** on Opus ($0.07 Sonnet); worst case 55k / 6k → $0.34 (the code caps input at 150,000 characters and 2 documents) | `backend/qalqon/llm/policy.py`; ~3 characters per token for RU/UZ is an **assumption** |
| Tokens per API endpoint classification | 1.5k in / 0.3k out → $0.012 on Opus | **assumption** |
| Document generation | 15k in / 12k out → $0.30 on Opus | **assumption** |
| "Policy vs behavior" | no extra LLM call: the model extracts, code compares | `policy.py`, D-021 |
| Browser compute | **$0.0006 per page visit** (the crawler observes 8 s on the first page and 3.5 s on others, `scanner/crawler.py`; ~10× headroom over a cloud VM) | VM prices `NOT VERIFIED`: Hetzner changed cloud prices twice in 2026 ([price adjustment](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/)) |
| Staff minutes per unit | support: 15 min per account per month, 5 min per domain, 1 min per form run, 10 min per manual login; analyst: 2 h onboarding, 1 h per test-account setup, 2 min per endpoint, 3 h per process mapping, 3 h per app deep check | **assumptions**; P-F23 measures them |
| Payment processing (Payme, Click, cards) | 2% | **assumption**, `NOT VERIFIED` |
| Employer social tax | 12% of payroll; IT Park residents exempt until 01.01.2028 | [PwC](https://taxsummaries.pwc.com/Republic-of-Uzbekistan/Individual/Other-taxes), [IT Park](https://outsource.gov.uz/en/media/tax-incentives-for-startups-and-foreign-investors-in-uzbekistans-it-sector) (search summaries, pages not opened) |

### 8. Unit economics by client type (gross margin 73% after payment fees for all)

| Client type | Monthly price | One-off | Gross profit / month | CAC (assumption) | Churn / month (assumption) | **LTV** | **LTV/CAC** | **Payback** |
|---|---|---|---|---|---|---|---|---|
| Small site | 186,966 UZS ($15.6) | — | 136,485 UZS | 500,000 UZS ($42) | 5% | 2.73M UZS ($228) | **5.5** | **3.7 mo** |
| Clinic / school | 253,289 ($21.2) | 2.23M ($186) | 184,901 | 2M ($167) | 3% | 7.79M ($651) | **3.9** | **2.0 mo** (one-off covers most of the CAC) |
| MFO / e-commerce | 1.53M ($128) | 9.09M ($759) | 1.12M | 5M ($418) | 2% | 62.5M ($5,219) | **12.5** | **0** (one-off covers the CAC) |
| Bank / telecom | 7.70M ($643) | 25.9M ($2,164) | 5.62M | 20M ($1,671) | 1% | 581M ($48,529) | **29.0** | **0.2 mo** |

**With sector packs (v3):** clinic 334,642 UZS/month → LTV 9.87M UZS ($824), LTV/CAC **4.9**, payback 1.1 months; microfinance 2,052,590 → LTV 81.6M ($6,820), LTV/CAC **16.3**; bank 8,663,209 → LTV 651M ($54,413), LTV/CAC **32.6**, payback 0.2 months.

LTV = monthly gross profit / churn + one-off gross profit. Payback = (CAC − one-off gross profit) / monthly gross profit. Churn follows secondary SMB SaaS benchmarks of 3–7% a month ([smbs.com](https://www.smbs.com/statistics/saas-churn-rate), [visionary-marketing.co.uk](https://visionary-marketing.co.uk/blog/saas-churn-benchmarks-2026)).

**Sensitivity, small site:** worst case (CAC 1M UZS, churn 7%) → LTV/CAC **1.9**, payback 7.3 months; best case (CAC 300k, churn 3%) → LTV/CAC 15.2, payback 2.2 months. **Small sites are the weakest segment**; acquire them through cheap channels (free scan, law firms, IT Park), not paid sales.

Switching the policy analysis from Opus to Sonnet halves the LLM line; with the uniform multiplier this lowers prices, not margins. **The biggest cost is staff time**, so the minutes per unit must be measured (P-F23).

### 9. Fixed costs and break-even

| Item (per month) | UZS | USD | Basis |
|---|---|---|---|
| 3 founders at the ICT average wage × 1.3 | 66,300,000 | 5,538 | 3 × 17.0M × 1.3 |
| Fixed infrastructure | 2,394,000 | 200 | assumption |
| Marketing | 11,972,000 | 1,000 | assumption |
| Accounting, legal, other | 3,000,000 | 251 | assumption |
| **Total fixed costs** | **83,666,000** | **6,989** | |
| **Break-even MRR** at 73% gross margin | **114,611,000** | **9,574** | fixed / 0.73 |

Example mix at break-even: 350 small sites + 50 clinics/schools + 12 MFO/e-commerce + 3 banks = **119.6M UZS MRR** (132.8M with sector packs). The base year-3 SOM in `market.md` (v3, sector packs) is **235.2M UZS MRR** (2.1× break-even).

### 10. Channels

| Channel | How it works | Target (market.md) | Cost to acquire | Why it can work |
|---|---|---|---|---|
| **Direct SMB** | free scan (L1) → Fix pack → monitoring; Telegram ads; anonymized "Uz-net Privacy 2026" report (F-03) | ~39,900 small sites in base SAM | CAC 300k–1M UZS (assumption) | the free scan shows a concrete problem in one minute |
| **Regulated mid and large** | founder-led sales; discovery scan → transparent quote from the formula; the access ladder (section 4) answers the trust question | 35 banks, 237 non-bank credit organizations, 115 e-commerce platforms, 6,577 private clinics and schools | 2–20M UZS (assumption), mostly covered by the one-off fee | dozens of domains and APIs; a lawyer who needs evidence |
| **Law firms** | firms resell Probo modules under their brand at a 20% partner discount (assumption) and add their own review | ~4,000 advocates (2019, stale) | low | firms already sell PD documents (Pactum, from 5M UZS) but can't check code |
| **IT Park** | free scans for residents; studios that build sites and apps for clients add Probo checks before release (F-08) | 4,200+ residents | near zero | IT Park co-organizes the hackathon; IT Park residents are exempt from social tax until 2028 |
| **B2G pilot: Ministry of Justice** | legal service center lawyers receive Probo reports for the organizations they serve | 21,292 organizations, 2,012 legal service staff | pilot = hackathon prize | the lawyers exist; the tool to check websites doesn't |
| **Cybersecurity Center** | referral partner for everything D-008 excludes (ports, vulnerabilities) | public sector, banks | — | complementary, not competing |

### 11. Mapping to the business mentor's criteria (passport §12)

| Criterion | What we show | Key numbers |
|---|---|---|
| **B1 Relevance of the problem** | The law changed twice in 2026; lawyers check documents, data leaks through code; our scan data | 182,338 .uz domains; batch of 8 real sites: trackers before consent on 7/8, Webvisor on 5/8 (passport 0.10; pitch numbers only from `GET /api/stats`) |
| **B2 Business model** | Free scan → one-off fix → monthly monitoring (D-007), priced by a transparent formula per module; law firms; B2G | price = 4,000 UZS × PSU; small site 187k, bank 7.7M UZS/month |
| **B3 Competitive advantage** | Global tools don't know Uzbek law; local lawyers don't check code; csec.uz checks vulnerabilities, not data handling | "says vs does" (F-01), API personal-data map, access ladder with no real credentials |
| **B4 Financial sustainability** | Uniform 75% gross margin by design; one-off onboarding pays for acquisition of large clients | LTV/CAC 3.9–29× (small sites 5.5×, worst 1.9×); break-even 115M UZS MRR |
| **B5 Growth potential** | New modules on the same formula (APIs, apps, inside scans); partner channels; other jurisdictions (F-10); B2G | SAM $9.6M a year; SOM year 3 $378k (v3, sector packs); B2G 21,292 organizations |

## Features for the product (§10 format)

IDs continue from `research/market.md` (P-F20…P-F22). Role 1 assigns real F-IDs.

| ID | Feature | What it gives | Complexity | Who proposed | Status |
|---|---|---|---|---|---|
| P-F23 | **Usage metering:** store per scan the pages, requests, forms, endpoints, LLM tokens, staff minutes and cost; roll up per account | Replaces the assumed minutes and costs in the rate card with measured ones; plan limits later | S | Research (Role 3) | Proposal (Final) |
| P-F24 | **"Your policy changed" alert** when the cached policy hash changes | Uses the D-020 cache; a reason to keep the subscription | S | Research | Proposal (Roadmap) |
| P-F25 | **Model routing:** Haiku 5.5 for page/document/endpoint classification; Opus or Sonnet only for policy extraction | Cheaper mass scans and endpoint maps; lower prices at the same margin | M | Research | Proposal (Roadmap) |
| P-F26 | **Law-firm workspace:** multi-client dashboard and white-label PDF | Enables the law-firm channel | M | Research | Proposal (Roadmap) |
| P-F27 | **B2G dashboard** for legal service centers | The Ministry of Justice pilot | M | Research | Proposal (Roadmap) |
| P-F28 | **Price calculator and checkout in UZS:** the discovery scan fills in the quantities, the client toggles modules, the page shows PSU and price (Payme / Click) | Turns the formula into a self-serve quote | M | Research | Proposal (Roadmap) |
| P-F29 | **API endpoint grouping and personal-data classification** from the requests the crawler already records (method + path pattern, PD fields, destination country) | Module M6, without any active testing (D-008) | M | Research | Proposal (Roadmap) |
| P-F30 | **Domain ownership proof** (DNS TXT or file) before any active module | The first rung of the access ladder; stops scans of sites the requester doesn't own | S | Research | Proposal (Final) |
| P-F31 | **Secrets vault and evidence masking:** credentials outside the app database, auto-expiry, masking of tokens, cookies and PD values in HAR before storage | The trust model in section 4 | M | Research | Proposal (before any L2 client) |
| P-F32 | **Client-side runner:** the scanner as a container the client runs inside its network; only masked facts leave | Banks and telecom without sharing credentials | L | Research | Proposal (Roadmap) |

## Questions for the team / contradictions with the passport

1. **Open ports, server files and other vulnerability checks** were asked for. D-008 excludes them (and V-15 asks whether they need a license). This file keeps them out and refers clients to the Cybersecurity Center. If the team wants them, it needs a new decision-log entry.
2. **The uniform multiplier k = 4** is a team decision (it sets the margin for everything). Is 75% the right target, or should automated modules carry a higher multiplier and staff-heavy modules a lower one?
3. **Staff minutes per unit are guesses** and drive most of the large-client price. P-F23 should measure them during the pilot.
4. **Fix pack generates a policy and consent text.** Is that a licensed legal service, and what disclaimer do we need? Role 2, R-08.
5. **Probo's own status under ZRU-547** when it holds test accounts and evidence for clients (operator, third party?), and whether telecom clients' evidence must be stored in Uzbekistan. Role 2.
6. **B2G buyer:** the Ministry of Justice (legal service centers) or the State Personalization Center (V-03)? Would integration require a csec.uz examination of Probo first?
7. **CAC, churn and willingness to pay are assumptions.** Add to the R-06 interviews: would they choose modules or a bundle; 560k vs 1.49M UZS for the Fix pack; would they give a test account, and on what conditions?
8. **Probo's own IT Park residency** (social-tax exemption until 2028) would lower the cost basis: `NOT VERIFIED` whether we qualify.
9. **Fines (V-05) are still unverified.** Until R-02 is done, the pitch leads with the 2026 law changes and the evidence, not fine amounts.

## Sources

- https://cbu.uz/en/arkhiv-kursov-valyut/json/USD/2026-11-20/ — CBU official rate, 20.11.2026
- https://www.cookiebot.com/en/pricing/
- https://usercentrics.com/pricing/
- https://termly.io/pricing/
- https://www.iubenda.com/en/pricing
- https://www.cookieyes.com/pricing/
- https://www.osano.com/plans/cookie-consent
- https://www.onetrust.com/pricing/
- https://pactum.uz/services ; https://pactum.uz/ceny
- https://csec.uz ; https://csec.uz/uz/services
- https://platform.claude.com/docs/en/about-claude/pricing
- https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/
- https://zamin.uz/en/economy/225656-average-monthly-salary-in-uzbekistan-reached-7-27-million-soums.html
- https://taxsummaries.pwc.com/Republic-of-Uzbekistan/Individual/Other-taxes (search summary)
- https://outsource.gov.uz/en/media/tax-incentives-for-startups-and-foreign-investors-in-uzbekistans-it-sector (search summary)
- https://www.smbs.com/statistics/saas-churn-rate (secondary benchmark)
- https://visionary-marketing.co.uk/blog/saas-churn-benchmarks-2026 (secondary benchmark)
- `files/taqdimot.pdf` — LexHackathon 2026 Ministry of Justice infographic (in the repo)
- `research/market.md` — counts, TAM/SAM/SOM
- `backend/qalqon/detectors/`, `backend/qalqon/scanner/crawler.py`, `backend/qalqon/llm/policy.py`, `backend/qalqon/llm/client.py`, `PRODUCT.md` — what the code does today
