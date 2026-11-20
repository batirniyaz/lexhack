# Competitors — Uzbekistan, Russia, Kazakhstan and other CIS (R-04, regional part)
- Author: Alii (GitHub Aliii2004) — research, R-04 competitors (regional part)
- Date/time: 21.11.2026, 01:35 · updated 02:05 (Uzbek/Kazakh-language searches, more CIS countries, Russian
  scanners re-tested on a Russian site)
- Based on passport version: 0.12
- Confidence: medium-high. Every service was opened on its own site on 21.11.2026; three Russian scanners were run
  hands-on. Fine amounts, regulator statistics and usage counters are the vendors' own claims unless marked.
- Global part: `research/competitors-global.md` (27 tools), `competitors-global-features.md`, `competitors-handson.md`.

## Conclusions

1. **Uzbekistan: no automated website checker for Uzbek personal-data law exists.** The market is law firms and
   advisers that sell documents, database registration and localization advice "on request" (Pactum, Juris, Bond
   Stone, VLO, Lexcell) and security firms that do pentests (Turan Security). None checks a website technically
   (trackers, cookies, where form data goes). The only software that encodes ZRU-547 is **SECURITM**, a Russian GRC
   system with a ZRU-547 requirements catalog — questionnaire-based, not a scanner. Searches were run in Uzbek,
   Russian and English (law firms incl. Azizov & Partners, Black Swan, Kosta Legal, Kinstellar, GRATA; IT Park;
   hosting and data centres such as UzCloud/UZTELECOM that sell "localization" infrastructure). → The Probo niche in
   Uzbekistan is empty as far as public sources show (confidence: medium-high — Telegram channels and offline
   offers were not searched).
2. **Russia is the closest precedent — and it is a crowded market.** At least 14 services check websites for
   152-FZ, launched 2024–2026 after three triggers: data localization and the ban on foreign trackers for primary
   collection, automated Roskomnadzor monitoring (vendors cite "159,000 sites checked since 2025", attributed to
   Kommersant — NOT VERIFIED), and turnover fines. Models: free lead magnets of web agencies (1PS, YuSMP, CAPS),
   cheap per-audit reports (help152: 1,490–4,990 RUB; 152norm: 300/990 RUB), document kits (help152: 57 documents for
   2,500 RUB), AI analysis (fzscan, toolfox with DeepSeek, Metascan Deep) and an enterprise "web perimeter" product
   (Metascan, API, batch). help152 claims **435,807 sites checked**. → Lesson for the pitch: once a law has
   localization rules, automated enforcement and real fines, a scanner market appears within 1–2 years. Uzbekistan
   got its new art. 27-1 and the list of 49 countries in 2026.
3. **Russian tools do not work for Uzbek sites.** Hands-on on one foreign site: toolfox scored 87/100 but said "too
   little could be checked", found no cross-border trackers that other tools found, and raised Russia-only
   requirements (INN/OGRN in the footer, prices in rubles, age labels under 436-FZ); Metascan could not check the
   site at all; fzscan found 6 cross-border requests among 2,245 external requests and gave a "critical" AI verdict,
   but every article it cites is Russian (152-FZ, KoAP 13.11). Re-tested fairly on a Russian site (habr.com):
   toolfox works as designed there (79/100, trackers before consent, no cookie banner, ad-marking gap, fine range
   455,000–1,310,000 RUB, benchmark vs 63 media sites) — but still contradicts itself (finds the owner's INN on the
   page and also reports "no INN on the site"). → They are real products for Russia, and they would cite the wrong
   law, wrong register (RKN) and wrong fines for an Uzbek business.
4. **Kazakhstan, Belarus, Kyrgyzstan: no scanners found; manual audits only.** Kazakhstan's OSN (IT studio) sells a
   basic personal-data audit for **300,000 ₸**, full compliance **2,400,000 ₸**, enterprise **6,200,000 ₸**; Acsour
   sells document sets and process audits (prices on request). Kazakhstan's regulator ran **77 personal-data
   inspections in 2025 and 44 in 2026** (to 20.08), tripled administrative fines (up to 2,000 MCI for PD breaches)
   and calls for "constant monitoring" of the internet — demand without a tool. Belarus has an active regulator
   (2023: 13 planned, 7 unplanned, 18 desk inspections) but no commercial checker was found. Kyrgyzstan replaced its
   law with the Digital Code (2025/2026). Georgia (Revera: audits, policies, consulting on cookie traffic),
   Azerbaijan (Deloitte legal) and Armenia (regulator PDPA) — consulting only, no scanner. → Real expansion room
   for F-10 (other jurisdictions), Kazakhstan first.
5. **Uzbek law firms are channel partners, not rivals.** They sell exactly what our scan cannot do (registration,
   internal documents, legal opinions) and cannot do what we do (see the site's real behaviour). This supports the
   "For law firms" plan in passport §7. Three of them (Juris, Bond Stone, Pactum) already describe the March 2026
   ZRU-1125 changes; two (VLO, Lexcell) still describe the old blanket localization — Uzbek businesses get
   contradictory advice, which is itself a problem we can show.

## Data

### A. Uzbekistan

| Name | Type, city | What they do (personal data) | Model and prices | Clients | Checks websites technically? | Law version on the page | Link |
|---|---|---|---|---|---|---|---|
| **Pactum** (ООО «PACTUM-AI CA») | law firm + legal platform, Tashkent | data-processing audit (systems, flows, contractors), **localization map per category with the art. 27-1 basis**, operator document kit (policy, order on responsible person, internal procedure, consent forms per purpose), **registration in the State Register**, processor contract terms, "inspection readiness" pack | PD work on request; 60-min lawyer consultation **300,000 UZS** (prepaid); registration: no state fee, 5 working days | none named (page: no reviews or cases yet) | no ("not only the site" — systems, not site scanning) | reflects ZRU-1125 and CMR No. 415 (49 states; KZ, UAE, TR, CN not listed; US only DPF; 24 h / 72 h notice) | https://pactum.uz/solutions/personalnye-dannye-uzbekistan |
| **Juris** (Juris Advisory) | legal & regulatory advisory, Tashkent; small senior team | guide for IT teams with checklist, consent / registration / leak runbook; "data protection & localization" for fintech | "Book a call"; no prices | "20+ companies structured", "30+ fintech products" (firm-wide) | no | reflects ZRU-1125 (article 16.10.2026, checked against Lex 14.10.2026); **notes that Administrative Code art. 46-2 and Criminal Code art. 141-2 still use the old, broader localization wording** | https://juris.uz/insights/uzbekistan-personal-data-law |
| **Bond Stone** | international law firm (HQ Almaty; offices incl. Tashkent; since 2007) | post-reform compliance review, localization for the 3 categories, cross-border structuring (adequacy, standard terms, BCR), PP-153 financial-sector compliance, registration advice, DPO role, policies and notices, DPAs with SaaS vendors, compliance audits, data mapping, breach plan | on request | anonymised (foreign bank's subsidiary, telecom operator, manufacturer) | no | reflects ZRU-1125; names the CMR 415 authorized body as "Department of Migration and Personalisation under the MoI" — differs from art. 8 (Q15) | https://bondstonelaw.com/practice-areas/data-protection-in-uzbekistan/ |
| **VLO Law Firm** | international boutique (Lisbon, 2011) | gap assessment, registration, responsible person, cross-border, breach response | gap assessment "from the low thousands of USD"; Uzbek data-centre hosting "low thousands USD per year" (indicative) | not named | no | **outdated**: calls localization a hard rule for all data (article dated 16.04.2026) | https://vlolawfirm.com/tpost/uzbekistan-data-protection |
| **Lexcell** | law firm, Tashkent | explainer only (data privacy and content takedown, 05.01.2025) | not stated | not stated | no | **pre-reform** wording | https://www.lexcell.uz/new14-eng |
| **Turan Security** | cybersecurity company, Tashkent | pentest, AppSec, incident response, red team, SOC, forensics, training — **no privacy service** | not stated | logos incl. banks, payment, telecom, IT Park (from logo filenames, not verified) | security checks only (out of our scope, D-008) | n/a | https://turansec.uz/ |
| **SECURITM** | Russian SGRC software (cloud or on-prem) | requirements catalog incl. **ZRU-547** (articles, assessment by questionnaire), plus Kazakhstan and Belarus documents; risk, assets, tasks, surveys | cloud "Community" free (1 team, 100 objects); paid cloud and on-prem tiers (prices on vendor site, not read) | not stated | no (questionnaire / catalog) | catalog text matches narrowed art. 27-1 | https://service.securitm.ru/docs/zru-547-pdn |

| **Azizov & Partners** | firm of advocates, Tashkent and Astana | memo on database registration (pd.gov.uz, 15-day decision, 10-day change notices) | not stated | not stated | no | **pre-reform** (memo 04.10.2024) | https://azizovpartners.uz/en/memos/registration-of-databases-containing-personal-information/ |
| **Black Swan Consulting** | multi-practice law firm, Tashkent (since 2019) | "confidentiality and personal data protection": corporate PD documents, database registration, NDAs | not stated | not stated | no | article 2023 (a 31.03.2026 item on amendments listed, not read) | https://blackswan.law/personal-data-processing-in-uzbekistan/ |
| Kosta Legal, Kinstellar, GRATA (Tashkent offices) | international / regional law firms | data protection named in TMT practice or staff profiles (directories) | not stated | not stated | no evidence | not checked (Kinstellar site refused connection) | https://www.legal500.com/firms/16096-grata-international/20760-tashkent-uzbekistan |
| **UzCloud (UZTELECOM)** and other data centres | infrastructure, Tashkent / Kokand / Bukhara (sponsored articles, 2026) | cloud and private cloud "in line with" the personal-data law; Tier III Design (Kokand); geo-redundant DCs | not stated | — | n/a — adjacent: they sell **where** to store data, we show **where data actually goes** | describes localization as a general requirement | https://www.spot.uz/ru/2026/04/15/uzcloud/ |

Not found in Uzbekistan: any automated site scanner, any CMP or cookie-banner product, any published price list
for personal-data compliance packages (Settle Law Firm page returned 404). Registration in the State Register
itself is free (15-day review per older sources; 5 working days per Pactum). Note: "Enterprise Uzbekistan", a new
special regime for tech companies (08.2026), reportedly sets its own personal-data rules — page blocked (HTTP 403),
NOT VERIFIED; worth a Role 2 look.

### B. Russia — 152-FZ website checkers (the regional precedent)

| Name | Operator | What it checks | How it scans | Model and prices (RUB) | Usage claims | Link |
|---|---|---|---|---|---|---|
| **help152 (ПОМОЩЬ152)** | АНО «Цифровые платформы» (INN 6168990775) | "100+" checks (about page: "200+ rules"): policy, consent in forms, cookie banner and counters, **where data is physically stored**, requisites, advertising law, consumer law, shop rules; 38 sector checks; 57-document kit; hosting list | robot loads pages, analyses content, headers, JavaScript, external connections ("static and dynamic analysis"); 30–60 s | Express free (score + counts); Basic 1,490; Standard 2,990; Complex 4,990 **per audit**; document kit 2,500; agencies >10 sites/month: individual | **435,807 sites checked**; "28% without a policy"; GA/GTM on 100% of last 3,000 checks; **writes to site owners when violations are found** | https://help152.ru/ |
| **Metascan 152-ФЗ** | ООО «Метаскан», St Petersburg (RU software registry No. 19437) | SSL/TLS, **hosting location by ASN**, cookies before consent, foreign analytics (cross-border), foreign OAuth buttons (406-FZ), forms without separate consent, policy sections (7 of 7), **operator lookup in the RKN register by INN and match with the policy**, anti-bot status | Regular (homepage, 1 credit) / Deep with **AI analysis** (5 credits; 1–100 pages) | 1 site free; enterprise by volume after demo; **API, batch, CSV, team roles** | none for itself; cites RKN "159,000 checks" | https://152.metascan.ru/ |
| **fzscan (ФЗ-скан)** | ИП Никитин Н. В. | cookie banner, forms (each with CSS selector), **cross-border scripts per domain + server country by IP**, policy sections, TLS, **168-FZ anglicisms with LLM** | AI analysis ("machine-learning models"), sitemap + selected pages | brief report free; full report paid (prices not shown) | not stated | https://fzscan.ru/ |
| **toolfox** | ИП Авдеев Р. С., Kazan (one person) | **134 detectors** (52 for 152-FZ): banner before counters, policy 11 sections, forms, cross-border (GA, Meta Pixel, Cloudflare), headers, rights, special categories, RKN register, plus 168-FZ, ad marking, 436-FZ age labels, consumer law, biometrics | **headless Chromium 130 via Playwright**, network log, cookies before/after load; **policy semantics classified by DeepSeek LLM** | free, no registration; PDF/HTML/JSON; 3 free document templates | "opened 1,127 times" | https://toolfox.ru/tools/proverka-sajta-fz-152 |
| **imyrist** | ИП Чвилев Г. Ю., St Petersburg | "25+" deterministic rules incl. foreign counters, tracking before consent, **cookies after refusal**, hosting region, separate marketing consent | not stated; "smart analysis" to prioritise | free 2/day (20 with account) → paid document package | not stated | https://imyrist.ru/monitoring |
| **152norm** | self-employed (placeholders on legal pages) | documents, SSL, cookies, "banned services" (GA, Meta, TikTok), forms, servers in Russia | extracts HTML | free (10 pages), 300 (100 pages), 990 (3,000 pages) | not stated | https://152norm.ru/ |
| **CAPS 152** | CAPS web studio domain, St Petersburg | 15 points incl. **RKN register lookup by INN**, foreign services, offer | opens public pages | free (agency lead magnet) | not stated | https://152.capsagency.ru/ |
| **YuSMP 152-FZ check** | ООО «ЮСМП ГРУПП Технологии», Novosibirsk | 14 points: HTTPS and Russian CA, **hosting country**, banner with reject, counters disclosed in policy, policy content, forms, marketing consent | "from outside, as Roskomnadzor does" | free; PDF after leaving contacts → "under-the-key" development | not stated | https://yusmpgroup.ru/products/152-fz-check |
| **PR-CY audit-152** | ООО «Анализ Сайта», Nizhny Novgorod | banner, form consents, policy and offer, policy content incl. storage in Russia, external calls | public pages | inside SEO SaaS: free / 990 / 2,490 / 9,990 per month | not stated | https://pr-cy.ru/app/audit-152/ |
| **1PS 152-FZ check** | web agency (ИП), Irkutsk | policy, form checkbox, HTTPS, cookie banner | 1–3 min | free lead magnet | not stated | https://1ps.ru/instrumentyi-i-kalkulyatoryi/proverka-sajta-na-sootvetstvie-152-fz/ |
| **Klerk site check** | Klerk.ru (accounting media) | scripts that may transfer personal data (list of problems) | not stated | free | not stated | https://www.klerk.ru/tool/check-site/ |
| **ScanBase 152-FZ** (WordPress plugin) | ScanBase service | score 0–100, violations with article and fine, manual items, admin-bar indicator | thin client of a cloud API | free 5 checks/day; one-off and subscription (prices not stated) | "fewer than 10" installs | https://wordpress.org/plugins/scanbase-152fz/ |
| **Chimitdorzhi audit** | ИП, Chita | manual 30+-item checklist incl. cross-border, analytics, localization, HTTPS | manual "from the visitor's side" | audit from 5,000; audit + fix from 30,000; turnkey from 80,000 (1 year support) | "100+ sites audited" | https://audit.chimitdorzhi.tech/ |
| **quickaudit.ru** | — | — | — | — | could not be opened (connection refused) | https://quickaudit.ru/ |

Founder story (T—Ж, 03.02.2026): a developer built a 152-FZ checker "in a couple of weeks at night" after a client
got a Roskomnadzor order; **1,517 checks in the first two weeks**; counters without consent on ~90% of sites;
**several law firms asked for an API**; LLM used only as an assistant ("close to right in about 1 of 10"
checks). https://t-j.ru/dev-story-servis-kotoryi-proveriaet-riski-po-152-fz/

Enterprise personal-data platforms (Kontur.Aegis, Security Vision): pages blocked (HTTP 403 / 401) — NOT VERIFIED.

### C. Kazakhstan, Belarus, Kyrgyzstan

| Name | Country | What | Prices | Website technical checks? | Link |
|---|---|---|---|---|---|
| **OSN.KZ** (ТОО «OpenSky Corporation», IT studio, Astana / Pavlodar) | KZ | personal-data compliance packages: audit of site and forms, policy, cookie banner → full compliance (documents, implementation, training, CMP, 3 months support) → enterprise (all systems, GDPR + KZ law, DPO as a service 12 months, pentest) | basic **300,000 ₸**; full **2,400,000 ₸**; enterprise **6,200,000 ₸**; security monthly 200,000–1,500,000 ₸ | partly (site and forms reviewed manually; no tracker / data-location scan) | https://osn.kz/blog/zashchita-personalnyh-dannyh-kz-2026 |
| **Acsour** | KZ | process and system audit, full document set in RU and KZ (policy, regulations, transfer and consent registers, orders), consultations, also 152-FZ work | on request | no | https://acsour.kz/personal-data-protection/ |
| **Nomad Guard** (eGov Mobile, Ministry of Digital Development) | KZ | for citizens: were my data leaked, is a link dangerous | free | no (not for site owners) | https://www.zakon.kz/sovety/6481355-kak-proverit-utechku-personalnykh-dannykh-cherez-spetsialnyy-servis.html |
| **PwC Kazakhstan** | KZ | data privacy services | — | page HTTP 403 — NOT VERIFIED | https://www.pwc.com/kz/ru/services/data-privacy.html |
| **NCPDP** (National Personal Data Protection Center) | BY | regulator: inspections (2023: 13 planned, 7 unplanned, 18 desk), small-business checklist (2025), training (20,000+ people) | free | no automated checker found | https://pravo.by/novosti/obshchestvenno-politicheskie-i-v-oblasti-prava/2024/february/76829/ |
| **Art Legal** (via Myfin) | BY | advice article: policy must be online, consent, breach notice to NCPDP within 3 working days, fines 20–50 base units | — | no | https://myfin.by/stati/view/kejsy-i-sovety-po-rabote-s-personalnymi-dannymi |
| **Kyrgyzstan** (ICNL, Invest Compass) | KG | Digital Code replaced the 2008 law (from 05.02.2026); fines added 23.11.2025; responsible person for >10 employees | — | no checker found | https://invest.gov.kg/en/invest-compass/assets/personal-data |
| **Kazakhstan regulator** (Ministry of AI and Digital Development, press 20.08.2026) | KZ | 77 PD inspections in 2025, 44 in 2026; typical violations: no consent, no lists of responsible persons, excessive data, missing MFA/logging/crypto; fines tripled (up to 2,000 MCI); Digital Code and Cybersecurity Law in force 12.07.2026; PD amendments 24.08.2026; calls for "constant monitoring" of the internet | — | method not stated, no scanner named | https://www.gov.kz/memleket/entities/maidd/press/news/details/1277592 |
| **Revera** (Georgia office) | GE | PD audits, policies, internal documents, **consulting on website traffic monitoring with cookies**, transfers, children's products (GDPR/COPPA), training | not stated | consulting only | https://georgia.revera.legal/en/uslugi/zashhita-personalnyx-dannyx/ |
| Deloitte Azerbaijan; Armenia PDPA | AZ / AM | legal advice on the Law "On Personal Data" (AZ); regulator with templates and inspections (AM) | — | no | https://www.deloitte.com/az/en/services/legal/perspectives/data-privacy-gdpr.html · https://www.dlapiperdataprotection.com/?c=AM&t=law |

Unsourced numbers on vendor pages (do not use in the pitch): OSN's "2,400+ inspections, 1.2 bn ₸ fines in 2025";
help152's "87% of sites per Roskomnadzor"; workspace.ru's claims about an "AI scanner" at Roskomnadzor.

### D. Hands-on: Russian scanners on the same test site (theguardian.com, 21.11.2026)

| Tool | Result | What it shows about the tool |
|---|---|---|
| toolfox | 87/100, "too little could be checked"; 14 violations, 65 items "not checked automatically"; fine range 140,500–490,000 RUB; "foreign PD services not found in the network log" | Real browser, but cross-border detection limited to a known list (missed Google Ad Manager and Comscore that WhoGetsMyData and ImmuniWeb found); raises Russia-only rules (INN, rubles, age labels) on a foreign site |
| fzscan | ~3 min; "critical" AI verdict; 17 problems; **2,245 external requests analysed, 6 cross-border**; full report paywalled | Counts cross-border traffic; verdict and articles are Russian law only |
| Metascan | "Could not check the site" | Free single-site check failed on a large foreign site |

Re-test on a Russian site (habr.com), so the tools are judged on their own ground:

| Tool | Result | What it shows |
|---|---|---|
| toolfox | 79/100 "some things to fix"; 17 violations; 53 items not checked automatically; fine range for an organisation 455,000–1,310,000 RUB; benchmark "average of 63 media sites: 76"; top issues: trackers before consent, no cookie banner, ad creative without erid marking, a tracking cookie before consent | Works as designed on Russian sites and is useful (industry benchmark, fine per entity type, free document templates); contradiction inside one report: "INN 7705756279 found on the page" and "no INN/OGRN on the site" |
| fzscan | ~3 min; "critical" AI verdict; 7 problems; **8,902 external requests analysed, 3 cross-border**; points to cookie notice, policy completeness ("Russian" specifics, security measures, rights, cross-border terms) and processes vs declared bases; details paywalled | Free version gives a verdict and counts only; the value (per-finding details) is behind the paywall — the same freemium funnel as help152 |

### Functions worth noting (what the strongest regional tools do)

- **Register lookup**: find the owner's INN on the site and check it in the regulator's public register, then
  compare with the INN in the policy (Metascan, CAPS). Uzbek equivalent depends on V-04 (is pd.gov.uz searchable?).
- **Hosting country by ASN + cross-border scripts per domain** (Metascan, fzscan, YuSMP) — same idea as Probo's
  enrichment.
- **"Cookies after refusal"** and **"tracking before consent"** as separate checks (imyrist).
- **Fine estimate per finding, separately for sole proprietor and company** (toolfox, Metascan).
- **Document kit generated from the scan** — policy, consent, notice to the regulator (help152 57 docs for
  2,500 RUB; toolfox and imyrist free templates).
- **Web perimeter**: one table for all domains and subdomains of a group, API, CSV (Metascan) — for banks and
  telecoms.
- **State-language check** (Russia: 168-FZ anglicisms via dictionaries + LLM — fzscan, toolfox).

## Feature ideas (passport §10 format)

- F-28 · State Register lookup: find STIR/INN on the site and check the operator in the State Register of personal
  data bases, compare with the policy · a fact, not a guess, for PD-POL / registration findings · S · borrowed from
  Metascan, CAPS · proposal · Final (only if V-04 shows a public search)
- F-29 · Document kit priced per kit (policy, consent, notice) generated from scan facts · the paid "Fix pack" of §7
  has a market price reference (2,500 RUB in Russia) · M · borrowed from help152 · proposal · Final
- F-30 · Web-perimeter scan for groups: all domains and subdomains in one table, API, CSV · sells to banks, telecom,
  marketplaces (§7 "large companies") · M · borrowed from Metascan · proposal · Roadmap
- F-31 · Fine estimate per finding for sole proprietor vs company (in BCA) · same as F-20, confirmed by two regional
  tools · S · proposal · Final

## Questions for the team / contradictions with the passport

- **Q12 (ethics, D-003/D-009).** help152 e-mails site owners when its automatic scan finds violations — a growth
  channel. Do we ever contact owners of sites we scanned without a request? Recommendation: no, at least not before
  R-08 is done.
- **Q13 (Role 2).** Russian tools also check the state-language law (168-FZ). Does Uzbekistan's Law "On the State
  Language" require site content or consumer information in Uzbek? Possible extra check — needs a lex.uz source.
- **Q14 (Role 2, R-02).** Juris says Administrative Code art. 46-2 and Criminal Code art. 141-2 still use the old,
  broader localization wording after ZRU-1125. If true, liability and the new art. 27-1 disagree — important for
  PD-LOC levels.
- **Q15 (Role 2, V-03).** Bond Stone names the CMR No. 415 authorized body as the "Department of Migration and
  Personalisation under the Ministry of Internal Affairs"; ZRU-547 art. 8 names the State Personalization Center.
  Which is current?
- **Q16 (business).** SECURITM (Russian GRC) already sells a ZRU-547 requirements catalog to security teams.
  Partner (they assess processes, we scan sites) or competitor for enterprise clients?
- **Q17 (pitch).** Passport §8 row "CIS / Central Asia — UNKNOWN — the main question of R-04" can now be answered:
  "Russia: 14+ 152-FZ scanners since 2024; Uzbekistan, Kazakhstan, Belarus, Kyrgyzstan: none".

## Coverage and limits of this step

- Searched in Uzbek, Russian, English and Kazakh; opened every listed service on its own site on 21.11.2026.
- Hands-on: toolfox and fzscan on two sites (theguardian.com, habr.com), Metascan on one (failed). help152 was
  deliberately not run: it says it e-mails owners of scanned sites.
- Not covered: Telegram channels and offline offers in Uzbekistan; Tajikistan and Turkmenistan; Russian CMP vendors;
  Kontur.Aegis, Security Vision, PwC Kazakhstan, Kinstellar, "Enterprise Uzbekistan" pages (blocked or refused).
- Details of services come from the vendors' own pages; prices change — dates are 21.11.2026.

## Sources

- Uzbekistan (added): https://azizovpartners.uz/en/memos/registration-of-databases-containing-personal-information/ · https://blackswan.law/personal-data-processing-in-uzbekistan/ · https://www.spot.uz/ru/2026/03/12/uzcloud/ · https://www.spot.uz/ru/2026/04/15/uzcloud/ · https://anhor.uz/news/v-uzbekistane-88/ · https://www.lexology.com/library/detail.aspx?g=c705796b-e78b-4a69-a3bc-f4267b841089
- Kazakhstan / Georgia / Azerbaijan / Armenia (added): https://www.gov.kz/memleket/entities/maidd/press/news/details/1277592 · https://georgia.revera.legal/en/uslugi/zashhita-personalnyx-dannyx/ · https://www.deloitte.com/az/en/services/legal/perspectives/data-privacy-gdpr.html · https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2025/armenia
- Hands-on (added): https://fzscan.ru/report/01a1fab3-0948-7237-88f0-7af10882a523 (habr.com) · toolfox result for habr.com
- Uzbekistan: https://pactum.uz/solutions/personalnye-dannye-uzbekistan · https://pactum.uz/ceny · https://juris.uz/insights/uzbekistan-personal-data-law · https://bondstonelaw.com/practice-areas/data-protection-in-uzbekistan/ · https://bondstonelaw.com/data-protection-compliance-in-uzbekistan/ · https://vlolawfirm.com/tpost/uzbekistan-data-protection · https://www.lexcell.uz/new14-eng · https://turansec.uz/ · https://service.securitm.ru/docs/zru-547-pdn · https://www.anti-malware.ru/reviews/SECURITM · https://www.dentons.com/en/insights/articles/2026/march/31/uzbekistan-dismantles-strict-data-localization-regime
- Russia: https://help152.ru/ · https://help152.ru/about · https://help152.ru/pricing · https://152.metascan.ru/ · https://fzscan.ru/ · https://fzscan.ru/report/example · https://toolfox.ru/tools/proverka-sajta-fz-152 · https://toolfox.ru/methodology · https://imyrist.ru/monitoring · https://152norm.ru/ · https://152.capsagency.ru/ · https://yusmpgroup.ru/products/152-fz-check · https://pr-cy.ru/app/audit-152/ · https://pr-cy.ru/prices/ · https://1ps.ru/instrumentyi-i-kalkulyatoryi/proverka-sajta-na-sootvetstvie-152-fz/ · https://www.klerk.ru/tool/check-site/ · https://wordpress.org/plugins/scanbase-152fz/ · https://audit.chimitdorzhi.tech/ · https://t-j.ru/dev-story-servis-kotoryi-proveriaet-riski-po-152-fz/ · https://workspace.ru/blog/sayt-kompanii-pod-avtomaticheskim-kontrolem-rkn-polnyy-razbor-trebovaniy-2026-goda/
- Kazakhstan / Belarus / Kyrgyzstan: https://osn.kz/blog/zashchita-personalnyh-dannyh-kz-2026 · https://osn.kz/services/security · https://acsour.kz/personal-data-protection/ · https://www.zakon.kz/sovety/6481355-kak-proverit-utechku-personalnykh-dannykh-cherez-spetsialnyy-servis.html · https://pravo.by/novosti/obshchestvenno-politicheskie-i-v-oblasti-prava/2024/february/76829/ · https://pravo.by/novosti/obshchestvenno-politicheskie-i-v-oblasti-prava/2025/september/90172/ · https://myfin.by/stati/view/kejsy-i-sovety-po-rabote-s-personalnymi-dannymi · https://www.icnl.org/post/news/kyrgyzstans-digital-code-understanding-and-complying-with-personal-data-provisions · https://invest.gov.kg/en/invest-compass/assets/personal-data
- Hands-on results: https://fzscan.ru/report/01a1faa7-e425-710f-9fa9-1970a291fb78 · toolfox result page (theguardian.com) · Metascan (failed)
