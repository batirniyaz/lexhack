# Probo service catalog: sectors, legal checks, audit access and verification

- Author: [name], research team; prepared with Claude Code
- Date/time: 21.11 00:40
- Passport version: 0.10
- Confidence: **high** for the ZRU-547 article titles and texts quoted below (read on lex.uz on 21.11.2026, unofficial Russian translation; the official text is Uzbek) and for the world-practice sources; **medium** for the design; **low** for sector-law article numbers (`NOT VERIFIED`, Role 2)

> Product name: **Probo** (working name Qalqon, D-014). This file turns the team's ideas into one design: the client picks a **sector**, Probo **verifies** the sector and the size of the system, the sector's **legal pack** pre-ticks the required checks, the client ticks optional services, the **price is calculated** by the formula in `business-model.md` §5, the client gives **audit-only access**, and receives a **report whose scope can be verified**.
> Respects D-004 ("signs of violation"), D-008 (no vulnerability testing), D-009 (active checks only with written consent), D-010 (rules decide, not the LLM).

## Conclusions

1. **Every service checks a specific article of ZRU-547.** The law is built around consent (art. 21), information about processing (art. 22), automated decisions (art. 24), special data such as health and criminal records (art. 25), biometrics and genetics (art. 26), protection measures (art. 27), mandatory storage in Uzbekistan for biometrics, genetics and telecom users (art. 27¹), registration of exactly those databases (art. 20), cross-border transfer (art. 15) and subject rights (art. 30). Sectors differ in **which of these apply**, so the sector decides the legal pack.
2. **The flow is: pick a sector → we verify sector and size → legal pack pre-ticks services → client ticks extras → price → audit-only access → agent runs → scoped report.** A client can pick several sectors (a bank with an online shop); the stricter pack applies.
3. **New apps with no personal data yet get a "Launch check".** We check the design before data arrives: screens and consent texts, API spec, database schema (structure only), SDKs in a test build, and the draft policy, all against the same articles. The world does the same under GDPR art. 25 and 35 (privacy by design, DPIA) and with code scanners such as Privado and Bearer.
4. **Clients can't usefully lie about sector or size.** We check the declared sector against the license register, the main activity code and our own page classifier, and measure size with a discovery scan. Every report states its exact scope. Declaring a smaller system only gives a narrower report, and anything found outside the scope is listed and offered as an extension. No company can fully prevent misdeclaration; the world practice is to make it pointless, and we copy that.
5. **Access is given only for the audit and proves itself both ways.** The client creates audit-only keys, routes, test accounts and roles: read-only, time-limited, bound to our IPs. Our agent signs every request (RFC 9421, as Cloudflare's Web Bot Auth does) so the client can tell our traffic from an attacker's. The report carries a hash and a verification page. The "verified" badge is live and is revoked automatically. The cautionary example is TRUSTe, which paid the FTC $200,000 after skipping more than 1,000 annual recertifications.

## Data

### 1. Legal basis: ZRU-547 articles each service checks

Source: [lex.uz/ru/docs/4396428](https://lex.uz/ru/docs/4396428), read 21.11.2026 (unofficial Russian translation; Role 2 adds the official Uzbek text).

| Article | Title (verbatim, RU) | What it means for the checks |
|---|---|---|
| 15 | «Трансграничная передача персональных данных» | where data leaves the country (M1, M6) |
| 20 | «Порядок регистрации баз персональных данных» | after ZRU-1125 only databases under art. 27¹ part 2 are registered: «Базы персональных данных, подлежащие обязательному хранению на территории Республики Узбекистан в соответствии с частью второй статьи 27¹ настоящего Закона, подлежат регистрации…» (M7, M13) |
| 21 | «Порядок дачи и отзыва согласия на обработку персональных данных» | consent on forms, in apps, before trackers (M1, M4, M5) |
| 22 | «Порядок предоставления информации, касающейся обработки персональных данных» | the policy and what it must say (M2) |
| 24 | «Автоматизированная обработка персональных данных» | the subject may object to a decision made only by automated processing; the operator must explain it and answer an objection «в течение десяти дней» (M15: scoring in banks and MFOs) |
| 25 | «Обработка специальных персональных данных» | special data includes data «касающиеся физического или душевного (психического) здоровья, сведения о частной жизни и судимости»; processing is prohibited except listed cases, e.g. written consent (clinics, insurers, HR) |
| 26 | «Обработка биометрических и генетических данных» | biometric data used to identify a person «могут обрабатываться только при наличии согласия данного субъекта» (M14: selfie/KYC) |
| 27 | «Гарантии защиты персональных данных» | legal, organizational and technical protection measures (M1: HTTPS, headers; trust model) |
| 27¹ | «Особые условия хранения и обработки персональных данных» | must be stored in Uzbekistan: «биометрические данные…; генетические данные…; данные физических лиц — пользователей услуг операторов телекоммуникаций» (M1, M6, M14, M9) |
| 28 | «Конфиденциальность персональных данных» | leaks to third parties (M1 `url_pii`, M4) |
| 30 / 31 | «Права и обязанности субъекта» / «…собственника и (или) оператора» | requests for access and deletion (M16) |
| 33 | «Ответственность за нарушение законодательства о персональных данных» | sanctions (Role 2, R-02) |

### 2. Sectors (fields) and their legal packs

The client chooses one or more sectors. ✔ = pre-ticked (required by the pack), ○ = recommended. Service IDs are in section 3.

| Sector | Typical personal data | Legal pack (ZRU-547 + sector law) | Required ✔ / recommended ○ | How we verify the sector |
|---|---|---|---|---|
| **Bank** | financial data, bank secrecy, KYC selfie, card forms | art. 15, 21, 22, 24, 26, 27, 27¹, 28; Law "On bank secrecy" ([lex.uz/acts/41882](https://lex.uz/acts/41882)); Law "On banks and banking activity" ([lex.uz/acts/12011](https://lex.uz/acts/12011)); possibly critical information infrastructure under ZRU-764 ([lex.uz/docs/5960609](https://lex.uz/ru/docs/5960609)). Articles `NOT VERIFIED` | ✔ M1 M2 M4 M5 M6 M14 M15 M16 · ○ M3 M7 M8 M9 | CBU license (35 banks), license register |
| **Microfinance, pawnshop, payment, fintech** | financial data, scoring, KYC | art. 15, 21, 22, 24, 26, 27¹, 28; CBU licensing (`NOT VERIFIED` act) | ✔ M1 M2 M4 M5 M6 M14 M15 · ○ M8 M16 | CBU register of non-bank credit organizations (237) |
| **Insurance** | health data in policies, financial | art. 21, 25, 27, 28; insurance law `NOT VERIFIED` | ✔ M1 M2 M4 M5 · ○ M6 M16 | license register |
| **Telecom / internet provider** | subscriber data (must stay in Uzbekistan) | art. 20, 27¹ part 2, 21, 28; law on telecommunications `NOT VERIFIED`; whether site visitors count as "users" is V-18 | ✔ M1 M2 M5 M6 M9 · ○ M4 M8 M16 | telecom license |
| **Clinic, hospital, pharmacy, laboratory** | health data (special data), appointments | art. 21, 25 (written consent), 27, 28; Law "On protection of health of citizens" ([lex.uz/acts/41329](https://lex.uz/acts/41329)), medical-secrecy article `NOT VERIFIED` | ✔ M1 M2 M4 M5 M16 · ○ M6 M8 | medical license |
| **Education** (school, university, kindergarten, online school, training center) | children's data, grades, parents' contacts | art. 21, 22, 27, 28; consent for minors and the education law `NOT VERIFIED` | ✔ M1 M2 M4 · ○ M5 M8 | education license |
| **E-commerce / marketplace** | buyers' names, phones, addresses, payments, marketing | art. 15, 21, 22, 28; Law "On electronic commerce" ZRU-792 ([lex.uz/docs/6213428](https://lex.uz/ru/docs/6213428)) and consumer protection law, articles `NOT VERIFIED` | ✔ M1 M2 M4 · ○ M5 M6 M8 M16 | main activity code, our page classifier (catalog, cart, checkout) |
| **Delivery, taxi, logistics** | location, phone, address | art. 15, 21, 27¹ (if telecom data), 28 | ✔ M1 M2 M4 · ○ M5 M6 M8 | main activity code, app store listing |
| **HR, recruiting, job boards** | CVs, which may include health and criminal records (special data) | art. 21, 25, 28 | ✔ M1 M2 M4 M5 · ○ M16 | main activity code |
| **State bodies and state organizations** (B2G) | citizens' requests, records | ZRU-547 + ZRU-764 (mandatory examination of state information resources, passport V-14) | ✔ M1 M2 · ○ M4 M16 | via the Ministry of Justice legal service centers |
| **IT company / app studio / new product** | users' data of the product they build | art. 20, 21, 22, 24–27¹ depending on the product | ✔ M13 (before launch) · ○ M1 M2 M6 M8 | IT Park residency, main activity code |

### 3. Services: what each one checks, what the client gives, how our agent enters

Access levels (passport §4): **L1** passive like a visitor; **L2** active with written consent; **L3** inside, read-only. IDs M1–M12 match `business-model.md` §3; M13–M16 are new.

| ID | Service | ZRU-547 | What the client gives (audit-only) | How our agent enters and checks | What we never do |
|---|---|---|---|---|---|
| M1 | Website privacy scan | 15, 21, 27, 27¹, 28 | nothing (L1). For staging: our IPs on the allowlist | opens pages in a real browser, records requests, cookies, forms, hosts and their countries (built: 11 detectors) | log in, submit forms on non-clients' sites (D-009) |
| M2 | Policy and "says vs does" | 22 | nothing; for unpublished documents, a file in the audit data room | the LLM extracts policy elements with verified quotes; code compares with M1 facts (built) | let the LLM decide a violation (D-010) |
| M3 | DNS and mail map | 15 | nothing | reads public DNS (MX, SPF) and certificate logs (crt.sh) | send requests to the client's servers |
| M4 | Canary form test | 21, 28 | domain ownership proof + signed letter listing the forms | fills listed forms with fake identities and searches all outgoing traffic for them (plain, URL-encoded, base64, SHA-256) | use real people's data |
| M5 | Logged-in area | 21, 22, 28 | **dedicated test accounts** named `probo-audit-*`, lowest role, fake data, expiring at the window end; for SMS/OneID the client logs in themselves in our isolated browser (F-14) | logs in, walks the account pages, runs M1 detectors behind the login | use a real customer's account; change settings or data |
| M6 | API personal-data map | 15, 21, 27¹, 28 | the **list of in-scope routes** or an OpenAPI file; an **audit API key** with read-only scopes, rate limit, expiry, bound to our IPs; staging for write calls | groups requests by method and path, finds personal-data fields and the hosts/countries they go to, flags fields beyond the stated purpose | fuzzing, auth bypass, injection, calling out-of-scope routes (D-008) |
| M7 | Processing register (business flow) | 20, 21, 22, 25, 27¹ | questionnaire answers + data-flow documents in the audit data room | LLM drafts the record of processing from the documents; an analyst and the lawyer check it against the articles and the scan facts | invent facts the client didn't give |
| M8 | Mobile app check | 21, 26, 27¹, 28 | store link or **test build** (APK / TestFlight); test account for dynamic runs | static: permissions and embedded SDKs; dynamic: app traffic through our proxy in an emulator | reverse-engineer beyond what is needed to list SDKs and permissions (Role 2) |
| M9 | Inside scan | 20, 27¹ | a **read-only cloud role** restricted to metadata (pattern used by Drata and Vanta: a dedicated role with a per-tenant external ID), or the client runs our agent | lists data stores, their regions, and column names that hold personal data | read row values |
| M10 | Monitoring and alerts | all | — | re-runs the chosen modules on a schedule; re-evaluates on law changes without a new crawl | — |
| M11 | Fix documents | 21, 22 | — | drafts policy, consent texts and banner settings in UZ/RU; analyst reviews | sign them as a lawyer |
| M12 | Evidence pack and lawyer review | all | — | HAR, screenshots, timestamps; partner lawyer memo | — |
| **M13** | **Launch check (new app, no personal data yet)** | 20, 21, 22, 24, 25, 26, 27, 27¹ | staging URL with synthetic data, screens or Figma export, OpenAPI file, **database schema without rows**, test build, list of SDKs and vendors, draft policy; optionally read-only access to one repository, or the client runs an open-source code scanner (Privado / Bearer) and uploads the result | runs M1/M4 on staging, reads spec and schema to list personal-data fields, statically checks the build, and produces an **article-by-article launch checklist**: consent screens, policy, storage country, whether registration (art. 20) is needed, special or biometric data, automated decisions | touch production; keep the code |
| **M14** | **KYC / biometric flow** | 26, 27¹, 20 | a test environment where the selfie or face step can be run with a **synthetic test image** | records where the photo or video is uploaded (country), whether consent is asked first, and whether the database must be registered (built: `biometric_capture` detector finds camera or selfie requests) | use a real person's face |
| **M15** | **Automated-decision check** (scoring) | 24 | a test account that can go through an application flow; the notice texts | checks that the flow tells the person a decision is automated, offers an objection, and that the 10-day answer process exists | influence the real scoring |
| **M16** | **Data-subject request test** | 22, 30, 31 | consent to send a request from a test identity | sends an access or deletion request as the test user and measures the reply time and content | send requests on behalf of real people or to non-clients |
| — | **Not offered** | — | — | open ports, exposed server files, vulnerability scans, pentests: D-008, referral to the Cybersecurity Center or licensed firms | — |

### 4. Verifying sector and size: "they can't lie to us"

| What could be misdeclared | How we check it | What happens on a mismatch |
|---|---|---|
| **Who the client is** | taxpayer number (STIR) of the legal entity; the order and the authorization letter signed with an electronic signature; **domain ownership proof** (a DNS TXT record, the same method [Google Search Console](https://support.google.com/webmasters/answer/9008080) uses) for every domain in scope | no active service starts without it |
| **Sector** | (1) licenses in the public license register kept by the Ministry of Digital Technologies ([gov.uz](https://gov.uz/en/digital/pages/litsenzialar-reestri)); (2) CBU lists for banks and non-bank lenders; (3) main activity code in the state registry (lookup by STIR `NOT VERIFIED`); (4) our page classifier on the discovery scan (card forms, appointment forms, catalogs, loan calculators) | the stricter sector pack applies; the client can appeal with documents |
| **Size** (domains, pages, forms, API endpoints, apps) | discovery scan: sitemap pages, forms, API endpoints seen in traffic, subdomains from certificate logs, apps under the company's developer name in the stores | the quote is recalculated **before** work starts; no silent price changes |
| **Size** (test accounts, processes, data stores) | declared, confirmed at onboarding | anything found later is listed in the report as "outside the audited scope" and offered as an extension at the formula price |
| **Everything** | every report and badge states its **scope**: domains, endpoints, apps, dates, access level, rules version | declaring less only produces a narrower report; misdeclaration voids the badge (contract clause) |

### 5. Audit-only access, and how we prove we are who we say

**What the client gives, and how it is limited**

| Access item | How it is restricted | How it ends |
|---|---|---|
| Domain ownership token (DNS TXT `probo-verify=…`) | one per domain | the client removes it |
| IP allowlist | only our published fixed IPs, only for staging or the WAF bypass the client chooses | removed at the window end |
| Test accounts `probo-audit-*` | lowest role that shows the flow; fake data; no payments with real money | expire at the window end |
| Audit API key | read-only scopes where possible, rate-limited, bound to our IPs, expiry date; write calls only on staging | expires automatically |
| In-scope route list / OpenAPI file | our agent calls only these routes | part of the signed letter |
| Read-only cloud role | metadata only, per-tenant external ID | the client deletes the role |
| Documents | an audit data room per engagement: watermarked, access-logged | deleted at the end; we send a deletion certificate |

**What Probo gives the client (so they can trust us)**

| Item | What it proves |
|---|---|
| Engagement letter with scope, window, IPs, accounts and keys, signed electronically by both sides; NDA and data-processing agreement | what we are allowed to do, and nothing more |
| **Signed agent traffic**: every request carries an HTTP Message Signature ([RFC 9421](https://www.rfc-editor.org/rfc/rfc9421)) with our published key and the engagement ID; the same approach as Cloudflare's [Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/) for verified bots | the client's logs and WAF can tell Probo from an attacker using our name |
| Published IPs, key directory and a `security.txt` contact ([RFC 9116](https://www.rfc-editor.org/rfc/rfc9116)) | who to call if our agent misbehaves |
| Full request log (HAR) of everything done with their access | "you can see every click we made" |
| Report hash + QR to a verification page: scope, date, rules version, reviewer | the report wasn't edited after we issued it |
| **Live badge**: "No signs of violation found in scope X on date Y", valid only while monitoring runs and no 🔴 is open, revoked automatically | avoids the TRUSTe failure; follows D-004 wording |
| Our own checks: a security assessment of Probo by the Cybersecurity Center or a licensed firm, ISO/IEC 27001 roadmap, the Ministry of Justice pilot as a reference | that Probo itself is safe to give access to |

### 6. World practice: what matches your ideas, what is different

| Your idea | What others do | Verdict |
|---|---|---|
| **Pick a sector → different checks** | Sector-specific rules are standard: GDPR art. 9 treats health and biometric data separately ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)); ZRU-547 does the same in art. 25–26 | **Matches.** Addition: allow several sectors; the stricter pack applies |
| **Price by scale (API routes, services)** | Pentest firms quote by hosts, endpoints and **user roles**; one vendor calls endpoint count the main driver, another says role and tenant testing matters more ([Schellman](https://www.schellman.com/blog/cybersecurity/the-cost-of-a-penetration-test), [SecurityWall](https://securitywall.co/blog/penetration-testing-cost-guide-2026)); Cookiebot prices by subpage count ([pricing](https://www.cookiebot.com/en/pricing/)) | **Matches.** Our formula already weights test accounts and manual logins more than endpoints. Lesson: tier jumps after a scan annoy clients, so we **quote before work and never change the price without consent** |
| **"They can't lie"** | Nobody fully prevents misdeclaration. Certifications are tied to a stated scope and can be withdrawn: GDPR art. 42 certifications last at most 3 years and are withdrawn when requirements stop being met ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)) | **Adjusted:** we can't stop a lie, but we make it pointless: verified sector, measured size, scoped report |
| **Keys, routes, permissions only for the audit** | Compliance-automation tools connect through a dedicated read-only role with a per-tenant external ID (Drata: built on AWS's SecurityAudit policy, [docs](https://help.drata.com/en/articles/13455825-understanding-aws-permissions-and-how-drata-integrates-with-aws-concept-guide); Vanta: a `vanta-auditor` role, [docs](https://help.vanta.com/en/articles/11345630-connecting-vanta-aws-account)); pentest scoping asks for test accounts, a role matrix, exclusions and testing windows ([SecurityWall](https://securitywall.co/blog/penetration-testing-cost-guide-2026)) | **Matches.** Addition: for banks prefer **the client runs our agent**, so no credentials leave their network |
| **Check new apps before they have personal data** | GDPR art. 25 (privacy by design and by default) and art. 35 (DPIA before risky processing) ([EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj)); Privado and Bearer scan source code to map personal-data flows and generate processing records ([Privado](https://github.com/privado-inc/privado), [Bearer](https://docs.bearer.com/explanations/reports/)) | **Matches** (M13). Addition: let the client run the open-source scanner and send only the result |
| **"Our service is verified" badge** | TRUSTe told sites it recertified seal holders yearly but skipped more than 1,000 reviews (2006–2013); the FTC settlement in 2014 cost $200,000 ([FTC](https://www.ftc.gov/news-events/news/press-releases/2015/03/ftc-approves-final-order-truste-privacy-case), [Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/truste-reaches-settlement-ftc-alleged-ftc-act-violations)) | **Adjusted:** our badge is a live status tied to monitoring, with scope and date, revoked automatically; wording "no signs of violation found", never "compliant" (D-004) |
| (not in your list) **Identify the scanner** | Verified bots sign requests (RFC 9421, Cloudflare Web Bot Auth) | **Added** (section 5) |
| (not in your list) **Rules of engagement** | Testing windows, exclusions of fragile systems, emergency contact (pentest practice, [SecurityWall](https://securitywall.co/blog/penetration-testing-cost-guide-2026)) | **Added** to the engagement letter |
| (not in your list) **Independence** | Auditors usually don't certify work they fixed themselves (general audit principle; `NOT VERIFIED` whether Uzbek law requires it for us) | **Risk:** we sell the Fix pack *and* the badge. Mitigation: the badge is issued only by the rules after a fresh scan, and a partner lawyer can sign for regulated sectors |

### 7. Sector → ticks → price (worked examples; prices from `business-model.md` §5, price = 4 × our cost)

| Client | Sector pack (ticked) | Monthly | One-off |
|---|---|---|---|
| **New app before launch** (staging, 15 screens, 30 API endpoints, 20 tables, 1 test build) | M13 + onboarding | — | **4,108,020 UZS (~$343)** |
| **Clinic** | ✔ M1 M2 M4 M5 M16 (quarterly) + ○ M6 (20 endpoints) | **334,642 UZS (~$28)** | 2,364,233 UZS (~$197), incl. sector verification |
| **Microfinance** | ✔ M1 M2 M4 M5 M6 M14 (1 run) M15 (quarterly) + M7 (3 processes) | **2,052,590 UZS (~$171)** | 9,217,573 UZS (~$770) |
| **Bank** | ✔ full pack: M1 M2 M4 M5 M6 M14 (2 runs) M15 (2 flows, quarterly) M16 + M7 (10 processes), 8 analyst hours | **8,663,209 UZS (~$724)** | 26,033,376 UZS (~$2,175) |

New unit prices (added to the rate card in `business-model.md` §5): launch check per screen 44,807 UZS; per 10 schema tables 90,093; launch report 1,602,519; KYC/biometric run 263,575; automated-decision review 532,896; data-subject request test 244,060; sector verification for regulated sectors 131,548 (one-off).

## Features for the product (§10 format)

IDs continue from `business-model.md` (P-F23…P-F32). Role 1 assigns real F-IDs.

| ID | Feature | What it gives | Complexity | Who proposed | Status |
|---|---|---|---|---|---|
| P-F33 | **Sector picker and legal packs:** a `sectors.yaml` that lists which rule IDs and services each sector requires; rules get an optional `sectors:` field | Law-first service selection; the rules engine only reports what applies | S | Team idea, written up by research | Proposal (Final) |
| P-F34 | **Sector and size verification:** license register check, CBU lists, page classifier, discovery-scan counts → quote | Clients can't under-declare; quote is automatic | M | Team idea | Proposal (Roadmap) |
| P-F35 | **Scoped, signed report:** scope block, hash and QR verification page | Proof the report is ours and unchanged | S | Research | Proposal (Final) |
| P-F36 | **Signed agent traffic** (RFC 9421) + published IPs and key directory + `security.txt` | Clients can identify and allowlist Probo | M | Research | Proposal (Roadmap) |
| P-F37 | **Engagement letter generator** (scope, window, accounts, keys, routes) with e-signature and automatic revocation reminders | Audit-only access in one document | S | Team idea | Proposal (Roadmap) |
| P-F38 | **Launch check (M13)** for new apps: staging scan + spec/schema reading + build check + article checklist | A product for builders and IT Park studios | M | Team idea | Proposal (Roadmap) |
| P-F39 | **Live badge** with automatic revocation | Viral growth without the TRUSTe risk | S | Research | Proposal (Roadmap; replaces the static idea in F-07) |
| P-F40 | **Data-subject request test (M16)** | Checks art. 22, 30, 31 in practice | S | Research | Proposal (Roadmap) |

## Questions for the team / contradictions with the passport

1. **Sector-law articles** (bank secrecy, medical secrecy, e-commerce, education, telecom, insurance, payment systems) need Role 2 with verbatim quotes. This file only links the laws.
2. **Can we call it a "certificate"?** Probo is not an accredited certification body. Proposal: "verification report" and a "status badge". Role 2.
3. **Independence:** selling fixes and issuing the badge (section 6, last row). Team decision.
4. **Synthetic biometric test images (M14)** and analysis of public app packages (M8): legal? Role 2, R-08.
5. **Banks as critical information infrastructure (ZRU-764):** do their contractors need a Cybersecurity Center approval? `NOT VERIFIED`.
6. **Registry lookup by STIR** (main activity code): is there a public or paid API? `NOT VERIFIED`. The license register is public (gov.uz).
7. **D-008 boundary for M6:** only normal calls on in-scope routes; who approves the route list (client signs it in the letter).
8. **PASSPORT.md §5 / §10** would need new rows if the team accepts M13–M16 and P-F33…P-F40. Only Role 1 edits the passport.

## Sources

- https://lex.uz/ru/docs/4396428 — ZRU-547 (article titles and quotes read 21.11.2026)
- https://lex.uz/acts/41882 — Law "On bank secrecy"
- https://lex.uz/acts/12011 — Law "On banks and banking activity"
- https://lex.uz/ru/docs/5960609 — ZRU-764 "On cybersecurity"
- https://lex.uz/acts/41329 — Law "On protection of health of citizens"
- https://lex.uz/ru/docs/6213428 — ZRU-792 "On electronic commerce"
- https://gov.uz/en/digital/pages/litsenzialar-reestri — public license register (search summary)
- https://eur-lex.europa.eu/eli/reg/2016/679/oj — GDPR art. 9, 25, 35, 42
- https://www.rfc-editor.org/rfc/rfc9421 — HTTP Message Signatures
- https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/ — Web Bot Auth
- https://www.rfc-editor.org/rfc/rfc9116 — security.txt
- https://help.drata.com/en/articles/13455825-understanding-aws-permissions-and-how-drata-integrates-with-aws-concept-guide
- https://help.vanta.com/en/articles/11345630-connecting-vanta-aws-account
- https://www.schellman.com/blog/cybersecurity/the-cost-of-a-penetration-test
- https://securitywall.co/blog/penetration-testing-cost-guide-2026
- https://www.cookiebot.com/en/pricing/
- https://github.com/privado-inc/privado ; https://docs.bearer.com/explanations/reports/
- https://www.ftc.gov/news-events/news/press-releases/2015/03/ftc-approves-final-order-truste-privacy-case ; https://www.hunton.com/privacy-and-cybersecurity-law-blog/truste-reaches-settlement-ftc-alleged-ftc-act-violations
- `research/business-model.md` — price formula and rate card
- `backend/qalqon/detectors/` — what is built today
