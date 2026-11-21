# Cybersecurity Center (csec.uz) and the security-audit market (R-09)
- Author: Alii (research), prepared with Claude Code
- Date/time: 21.11.2026, 08:40
- Based on passport version: 0.14
- Method:
  - I read the Center's own site in a browser on 21.11.2026: the main page, the services list, and the service pages
    "Website check" (`/ru/services/16`), "Xavfsizlink.uz" (`/17`) and "Information security audit" (`/12`). I also
    read UZCERT's "About" page.
  - Legal basis: PP-4452 and ZRU-764, from the local lex.uz corpus and live lex.uz (ZRU-764 art. 18 and art. 24 are
    quoted in `research/legal-our-risks.md`).
  - Private market: a published price list of one Tashkent security firm (Quantum IT SYS), plus the Uzbek firms
    already found in R-04 (`research/competitors.md`).
  - **Not done:** the phone call for the Center's price (+998 71 203-00-83). The service regulation PDF on the page
    was not downloaded.
- Confidence: **high** for what the Center says it does (its own pages). **Low** for the Center's prices (not
  published). **Medium** for the private market (one published price list).

## Conclusions

1. **The Center and Probo look at different things.**
   - *What the Center checks.* Its "website check" (`/ru/services/16`) is a **security examination**: SQL
     injection, XSS, CSRF, LFI/RFI, RCE, web shells, outdated CMS and plugins, authentication and sessions, server
     configuration, SSL/TLS, security headers, and leaked config files, backups, keys and **personal data left open**.
     It is automated scanning plus **manual testing**, and source-code review if needed.
   - *What Probo checks.* Whether the site **collects and passes on personal data lawfully** under ZRU-547: trackers
     before consent, foreign recipients and countries, policy versus behaviour, forms and consent.
   - *Where they overlap.* Only HTTPS and security headers (our SEC-01/02). Our SEC checks are a small subset of
     theirs.
2. **The Center's check is mandatory only for the state.**
   - *Who must pass it.* State bodies' information resources and systems, and systems in critical information
     infrastructure (ZRU-764 art. 18). For a private business it is a **paid service on request** ("Оформить заказ").
   - *Who the Center is.* A state institution under the State Security Service (PP-4452 of 14.09.2019, csec.uz main
     page). UZCERT is its incident-response service at the same address.
3. **Scale (9 months of 2026, csec.uz main page):**
   - 225 web-resource examinations;
   - 432 examinations of technical specifications;
   - 415 incidents found and fixed in the .uz domain;
   - 2,504 phishing sites blocked;
   - "1.684 bn+" threats detected and prevented.
   225 examinations in 9 months is about 25 a month. That is tiny next to 182,338 .uz domains (R-05), so most sites,
   and almost all private ones, are never examined.
4. **Prices: the Center publishes none; the private market does.**
   - *Quantum IT SYS (Tashkent)* lists "from" prices: pentest **from 15 M UZS**, web-application security analysis
     **from 8 M**, cybersecurity audit **from 4 M**, "GDPR and ISO 27001 compliance assessment" **from 2 M**.
   - *Nobody sells a ZRU-547 compliance check.* That firm's privacy offer is GDPR, not Uzbek law. Turan Security
     sells pentest and SOC with no privacy service (R-04). Law firms (Pactum, Juris, Bond Stone) check documents, not
     the site (R-04). Pactum's 60-minute consultation costs 300,000 UZS.
5. **Our difference in one sentence:** the Center and the security firms answer "can this site be hacked?"; lawyers
   answer "are the documents right?"; **Probo answers "what does the site actually do with visitors' personal data,
   and is that legal?"** — automatically, in 1–2 minutes, from an Uzbek IP, with the article of the law and the
   evidence.

## Data

### 1. Cybersecurity Center — services (csec.uz/ru/services, 21.11.2026)

| Service (as named on the site) | What it is | Relevant to Probo |
|---|---|---|
| «Проверка веб-сайтов, расположенных в национальном сегменте сети Интернет, на основе требований кибербезопасности» | security examination of .uz websites (details in §2) | the closest service; it does security, not data-processing law |
| «Подключение веб-приложений к системе защиты Firesight» | protection system for web applications | no |
| «Проведение экспертизы информационных систем на соответствие требованиям технического задания» | examination of systems against specifications | no |
| «Аудит информационной безопасности объектов информатизации» | information-security audit (the page has no description) | no |
| «Проведение экспертизы мобильного приложения на соответствие требованиям информационной безопасности» | mobile app security examination | near our roadmap (mobile apps), security only |
| «Помощь в разработке политик информационной безопасности» | help writing information-security policies | not personal-data policies |
| «Сертификация системы управления информационной безопасностью» | certification of an information-security management system | ISO 27001-type; no ZRU-547 |
| «Xavfsizlink.uz» | free public link, file and QR checker: blacklists, warns when a link asks for **camera, microphone or geolocation**, malware in downloads, AI-edited images | a citizen-facing tool; no legal check |
| Threat intelligence, CERT/CSIRT help, incident investigation, ICT certification, training, data recovery, examination of technical specifications | — | no |

### 2. What the "website check" covers and returns (csec.uz/ru/services/16)

| | Cybersecurity Center | Probo |
|---|---|---|
| Question | Can the site be hacked; is it already compromised? | Does the site process visitors' personal data lawfully (ZRU-547, CMR 415)? |
| Method | Automated scanning, then **manual** checks of login, registration, password recovery, upload, search, forms and admin panel; source-code review if needed | **Passive only**: opens public pages as an ordinary visitor and records network flows; forms and logins only on client sites with consent (D-009) |
| Typical findings | SQLi, XSS, CSRF, LFI/RFI, RCE, web shells, outdated CMS and plugins, session flaws, server misconfiguration, SSL/TLS, **security headers**, exposed configs, backups, keys, **personal data left open** | trackers before consent, data sent to foreign recipients and their countries (adequate or not), policy versus actual behaviour, PII in URLs, cloud databases in page code, consent and notice on forms, **HTTPS on PD forms**, headers |
| Report | List of checked resources, methods, vulnerabilities with severity (critical / high / medium / low), location, consequences, technical evidence, fixes, "conclusion on the overall level of cybersecurity" | findings with level 🔴🟡⚪, a **verbatim article of the law** and a lex.uz link, evidence (requests, hashes, signature), "how to fix" in uz/ru |
| Who must use it | state bodies and critical infrastructure (ZRU-764 art. 18); others on request | anyone with a website; no legal duty to use it |
| Time and price | not published; order via the site, tel. +998 71 203-00-83 | 1–2 minutes; public pricing in `business-model-v2.md` |
| Legal basis | ZRU-764; PP-4452 | ZRU-547; R-08: no license needed |

### 3. The security and privacy audit market in Uzbekistan

| Who | Type | What they sell | Price (published) | ZRU-547 website check? | Source |
|---|---|---|---|---|---|
| Cybersecurity Center (csec.uz) + UZCERT | state institution under the State Security Service | §1 | not published | no | csec.uz ; uzcert.uz/en/about/ |
| Quantum IT SYS | private IT and security firm, Tashkent | pentest; source-code, web-app and mobile-app security analysis; audit; IDS, DLP; GDPR and ISO 27001 assessment; incident response | from 2 M to from 15 M UZS per service (pentest from 15 M; web app from 8 M; audit from 4 M; GDPR/ISO 27001 from 2 M) | no (GDPR, not Uzbek law) | https://q-systems.uz/ru/cybersecurity |
| Turan Security | security firm, Tashkent | pentest, AppSec, red team, SOC, forensics, training | not stated | no | R-04, https://turansec.uz/ |
| Pactum, Juris, Bond Stone, VLO and others | law firms | documents, registration, audit of processes, localization advice | Pactum consultation 300,000 UZS / 60 min; VLO gap assessment "from the low thousands of USD" | no (documents, not the site) | R-04 |
| CERT-CBU (Central Bank) | sector CERT | cybersecurity for the banking sector | — | no | https://cbu.uz/ru/cert/about/ |

## Fact check (passport §11.4)

| ID | Claim | Status | Correct wording | Source |
|---|---|---|---|---|
| V-14 | Cybersecurity Center (PP-4452, under the SSS); mandatory examination of government resources; 225 web-resource examinations in 9 months of 2026; prices not published | **CONFIRMED** (from the Center's own pages) | Add: a state institution; examinations are mandatory for state bodies and critical infrastructure (ZRU-764 art. 18); private sites on request. The Q1 2026 figure "252 vulnerabilities, 169 on government resources" was **not re-checked** (secondary source) | https://csec.uz/ru/ ; https://csec.uz/ru/services/16 ; https://lex.uz/ru/docs/5960609 |
| §13 | "The Center looks for vulnerabilities, mostly on government sites" | **CONFIRMED** | Its website check is a security examination. Personal data appears only as "data left open", not lawful processing | csec.uz/ru/services/16 |

## Feature ideas (passport §10 format)

- F-52 · **"Security examination recommended" hand-off.** When SEC-01/02 or PD-DB-01 fire, the report suggests the
  Center's website examination (or a licensed firm) for the security side. It names no price and makes no promise ·
  shows we complement the Center (D-008), the answer to "Doesn't the Center already do this?" · S · R-09 · Final

## Questions for the team

- **Q-R9-1 (Alii, before 13:00).** Call +998 71 203-00-83: the price and time of the website examination for a
  private company, and whether they would accept Probo's report as input. One call closes the price gap.
- **Q-R9-2 (team, pitch).** Use "≈25 examinations a month vs 182,338 .uz domains" in the pitch? It shows the gap
  without criticising the Center.
- **Q-R9-3 (business).** A partnership idea: the Center does security, Probo does data law. A joint B2G package for
  state bodies (ZRU-764 art. 18 plus ZRU-547)? Ask the mentors.

## Sources

- Cybersecurity Center: https://csec.uz/ru/ (statistics, address: Tashkent, Mirabad district, Taras Shevchenko st. 20) ·
  services https://csec.uz/ru/services · website check https://csec.uz/ru/services/16 · Xavfsizlink.uz
  https://csec.uz/ru/services/17 · audit https://csec.uz/ru/services/12 · Telegram https://t.me/s/cyber_csec_uz
- UZCERT: https://uzcert.uz/en/about/
- PP-4452 of 14.09.2019: https://lex.uz/ru/docs/4665551
- ZRU-764 «On cybersecurity», art. 18: https://lex.uz/ru/docs/5960609
- Quantum IT SYS price list: https://q-systems.uz/ru/cybersecurity
- CERT-CBU: https://cbu.uz/ru/cert/about/
- Related: `research/competitors.md` (R-04, Uzbek firms), `research/market.md` (R-05, .uz domains),
  `research/legal-our-risks.md` (R-08, ZRU-764 art. 24)
