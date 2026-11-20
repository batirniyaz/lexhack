# Competitors — global
- Author: Alii (GitHub Aliii2004) — research, R-04 competitors (global part)
- Date/time: 20.11 23:50 (Step 1A) · 21.11 ~00:30 (Step 1B part 1, 10 companies) · 21.11 00:40 (Step 1B part 2, remaining 17)
- Based on passport version: 0.10 (rechecked against 0.12 on 21.11: product renamed to Probo, D-022)
- Confidence: medium. Facts come from each company's own site (read 21.11.2026) or named press/databases. Feature
  claims are the vendors' own marketing unless marked otherwise; nobody here was tested hands-on.
- Status: Step 1A approved ("APPROVED 1B", 21.11). On 21.11 the scope of 1B was widened from 10 to **all** shortlisted
  entries: part 1 (10) + part 2 (17) = 27 tools, plus 3 academic papers. Waiting for approval.
- **Deep function-by-function analysis of all 27 (docs, help centers, methodology): `research/competitors-global-features.md`.**
  CIS / Uzbekistan / Kazakhstan / Russia are a separate later step.

---

# STEP 1B — deep dive (all 27)

## Overall conclusions (all 27 tools + 3 papers)

1. **0 of 27 mention Uzbekistan, Russia, Kazakhstan or the CIS.** Laws named across all of them: GDPR, UK GDPR,
   ePrivacy, US federal and state laws (CCPA/CPRA, CIPA, VPPA, HIPAA, COPPA, BIPA, 20 state laws), LGPD (Brazil),
   PIPEDA and Law 25 (Canada), PIPL (China), DPDP (India), PDPL (Saudi Arabia), POPIA (South Africa), FADP
   (Switzerland), LFPDPPP (Mexico), Australian Privacy Act. The Uzbek niche is empty.
2. **"Policy vs behavior" is common:** 7 say yes (Vakteye, Privaini, WhoGetsMyData, Reflectiz, Datascale, Ours Privacy,
   SitePrivacyScore); about 10 more do it partly. Academic prior art since 2018 (Libert: 1 million websites, fewer
   than 15% of third-party flows disclosed).
3. **Data-destination country is less common:** clear "yes" only for c/side, Feroot, WhoGetsMyData and
   SitePrivacyScore (IP → location); partly for Privado, TrustArc, Didomi (non-adequate-country recommendation),
   Lokker (Geo category), ObservePoint (approved geolocations), iubenda (enterprise vendor map), OneTrust (vendor
   location). None checks a country list other than the EU's / their own. (Corrected after the deep read on 21.11.)
4. **The most complete "evidence for lawyers" products:** Captain Compliance Patrol (statute mapping + SHA-256 + HAR +
   screenshots), Vakteye (recording + network log + integrity-checked zip), WhoGetsMyData (Ed25519-signed records),
   Blacklight (open source, HAR + screenshots), noyb (HTML, data flows, screenshots for complaints).
5. **The market consolidates and pays exits:** Veeam bought Securiti for ~$1.725B (Oct 2025), Main Capital bought
   TrustArc (Oct 2025), team.blue owns iubenda + Complianz + CookieFirst + consentmanager, Didomi bought Sourcepoint
   (2025). Good for the B5 "growth potential" story.
6. **A national-law-first SaaS already exists elsewhere: ComplyZero (India, DPDP only, data stored in India, from
   ₹9,000 a month).** It is the closest *business* analog to what Probo can be in Uzbekistan — but it is a
   governance suite (consent, requests, registers), not a site scanner.

---

## Part 1 — 10 companies

Chosen from the 1A shortlist: the 8 proposed (Privado, Vakteye, Cookiebot, Didomi, c/side, Lokker, Privaini,
WhoGetsMyData) + OneTrust (market leader, named in passport §13) + Feroot (technically closest on "where data goes").

## Conclusions (Step 1B)

1. **None of the 10 mentions Uzbekistan, Russia, Kazakhstan or the CIS** on the pages read. They cover GDPR, US state
   laws (CCPA/CPRA, CIPA, VPPA, HIPAA), LGPD, PIPEDA, Quebec Law 25, PIPL, POPIA. Uzbek law (ZRU-547, art. 27-1,
   the CMR No. 415 list of 49 countries) + uz/ru + a catalog of local services is still an empty niche.
2. **Most of our other "differences" already exist somewhere.** Policy vs behavior: Vakteye, Privaini, WhoGetsMyData
   (yes), 5 others partially. Country map of data flows: c/side, Feroot, WhoGetsMyData. Where form data goes: c/side,
   WhoGetsMyData. Signed / hashed evidence: WhoGetsMyData (SHA-256 + Ed25519), Vakteye (zip with integrity check).
   Score: WhoGetsMyData 0–100, Lokker 0–1000, OneTrust "Compliance Score". We must not claim "first in the world".
3. **The closest product to our MVP is free and Swiss: WhoGetsMyData** (157,514 sites scanned; before/after consent,
   form destinations, policy promise check, companies on a world map, signed evidence, score 0–100). It says itself it
   is "not a legal assessment". The closest *paid* products are Vakteye (Sweden, EU law only) and Privaini (USA,
   statute-mapped, sold through insurers).
4. **Prices show two worlds:** CMPs are cheap and self-serve (Cookiebot €0–90 per domain/month, c/side $0–99/month);
   audit/monitoring tools are enterprise (Privado from $600 per website/month, min. 4 sites; OneTrust, Didomi,
   Feroot, Lokker, Privaini, Vakteye: "contact sales"). Nothing exists at an Uzbek SMB price with Uzbek law —
   supports our subscription tiers (passport §7) as a gap, not as a proven price (prices still need R-06 interviews).
5. **Money is in this market:** OneTrust >$1B raised ($4.5B valuation, 2023); Usercentrics >€100M ARR (Oct 2025);
   Didomi €72M growth round (2025) and bought Sourcepoint; Feroot $14M Series A (Nov 2025); c/side $7.7M (2024).
   Buyers of audit tools are compliance teams, **law firms** (Lokker: Orrick, Troutman) and **insurers** (Privaini:
   Beazley, Chubb, Marsh) — two channels worth adding to our B5 story.

## Data

### Table §11.3 (prices checked on the companies' own pages on 21.11.2026)

| Name | Country | What they do | Model and prices | Clients (vendor-stated) | Investment | What to borrow | How we differ | Link |
|---|---|---|---|---|---|---|---|---|
| **Privado.ai** (Web Auditor) | USA (Privado Inc., Dover, DE; team in US, Europe, India) | Scans websites/apps simulating accept/reject/no-action and login journeys; data-flow maps to third parties; flags cross-border flows; 30–50 preset checks; also code scanning, DPIA/RoPA AI agent | Web Auditor **from $600 per website/month**, billed annually, min. 4 websites; App Auditor from $800/app/month; Wren agent from $4,200/month; platform custom | HP Inc, HERE Technologies, Headspace, Zego, JobCloud; "10,000+ risks identified" | $3.5M seed (Jan 2022) + $14M Series A (Aug 2022, Insight Partners, Sequoia Capital India) = $17.5M | Journey scans after login; auto-tickets (Jira/Linear) for developers | US/EU/China/Canada laws only; enterprise price; no Uzbek list, no uz/ru | https://www.privado.ai/pricing |
| **Vakteye** | Sweden (Stockholm; Swedish law) | Monitors sites for privacy, security, accessibility; tests that "Reject" really works; extracts privacy-policy claims and compares them with observed behavior; flags transfers outside the EU and US recipients without DPF; human review of low-confidence findings | No list prices. Essentials (monthly scan, 1 apex domain), Professional (weekly + expert verification), Enterprise (up to 5 domains) — "Book demo" / "Get quote" | None named (one CEO testimonial, KeyMan) | Not stated | **Human review queue** for low-confidence findings (fits D-019); evidence zip with integrity check; public "Privacy Monitored" badge with record number | EU-only legal mapping; no document generation; Swedish/English only | https://www.vakteye.com/en/pricing |
| **Usercentrics Cookiebot** | Denmark (Usercentrics A/S, Copenhagen); Usercentrics founded in Munich | CMP: monthly cookie scan, auto-blocking, consent banner in 47+ languages, cookie declaration, privacy-policy generator, Google Consent Mode, IAB TCF | Free €0 (≤50 subpages, 1 domain); Premium Lite €7/mo; Small €15/mo/domain (≤350 subpages); Medium €30; Large €50; XLarge €90 (>7,000 subpages); daily scans +€99/mo; Advanced: contact sales | "600,000+ customers", "2.4M websites and apps", "8.8B monthly consents" | Usercentrics: €27.2M total (Series B €17M, 2020); ARR >€100M, profitable (Oct 2025) | Per-domain pricing by page count; free tier as lead magnet (= our Free plan) | GDPR/CCPA/LGPD/POPIA, not Uzbek law; consent tool, not an audit with legal findings | https://www.cookiebot.com/en/pricing/ |
| **Didomi** (CMP + Advanced Compliance Monitoring) | France (Didomi SAS, Paris) | CMP + scans simulating accept-all / refuse-all / no action; trackers before consent or after refusal; checks if the privacy notice declares each vendor; weekly alerts; time-stamped audit trail | No public prices: Essential / Advanced / Premium "Contact us"; free compliance scan with a free account | Europcar, Chantelle, Volvo, Yahoo, Michelin, Lacoste; "2,000+" / "2,800+" / "3,500 in 45 countries" (pages disagree) | €5M A (2020), $40M B (2021), €72M growth (2025, Marlin Equity); bought Agnostik (2022), Addingwell, Sourcepoint (2025) | Three consent scenarios as separate scans (our F-18); **free scan behind a work-email signup** = lead generation | No country/transfer view, no form destinations; no Uzbek law | https://didomi.io/advanced-compliance-monitoring |
| **OneTrust** (Cookie Consent + Compliance Assistant) | USA (Atlanta) | CMP: scans cookies/tags/pixels (simulated users, behind logins), 45M pre-categorized cookies, 250+ languages; Compliance Assistant: daily scans, Compliance Score, regulations mapped by geolocation; scans run from regional locations | No public prices; CMP priced by average daily visitors; "Contact sales" | "14,000+ customers", "750,000+ websites"; logos: Samsung, Walgreens, Atlassian, Adobe, Pfizer, Maersk | >$1B raised (company); last round $150M at $4.5B valuation (Jul 2023); CEO cited ARR $400M (2023) | **Scan from the visitor's region** (EU scans from Amsterdam) → we should scan from an Uzbek IP; regulatory content from DataGuidance "300+ jurisdictions" | Huge and expensive; no Uzbek law named; no country map in CMP | https://www.onetrust.com/products/cookie-compliance |
| **c/side** (Privacy Watch) | USA (Client-Side Development, Inc.; founded 2024; founder ex-Cloudflare) | Watches third-party scripts in real browser sessions: what data they read (incl. form fields) and where they send it; **map of cross-border data flows**; blocks scripts before consent; PCI DSS script inventory | Free $0 (2,000 pageviews/mo); Business **$99/mo** (100k payment page views; $499 for 500k); Enterprise custom; yearly −16% | Jomashop, Kikoff, eviivo, Wazuh; "thousands of domains" | $1.7M pre-seed (May 2024) + $6M seed (Sep 2024, Uncork Capital) = $7.7M | Alerts on "sudden changes in data destinations"; AI-written per-script justifications | Security product with privacy add-on; runs as a script **on the client's own site** (we scan from outside, any site); GDPR/CCPA/HIPAA only | https://cside.com/pricing |
| **Feroot Security** | Canada (Toronto) | AI agents for website compliance: trackers, scripts, cookies, data assets; **"Unauthorized Countries" + world map of data transfers**; consent enforcement; PCI script monitoring; free browser extension and free scanners (cookie consent, RoPA) | No public prices; tiers Assess (≤10 domains) / Govern (≤20) / Enterprise (≤5,000) — "Schedule a demo" | Instacart, Reddit, Gusto, Xerox, Forbes, Newegg; "200K+ websites covered" | $11M seed + $14M Series A (Nov 2025, True Ventures) ≈ $25M (sources: $25–27.5M) | "Unauthorized countries" counter on the dashboard = our PD-LOC-02 in one number; free extension as lead magnet | Claims "70+ laws" but none from the CIS; installs on the client's site; enterprise sales | https://www.feroot.com/pricing/ |
| **LOKKER** (Privacy Edge) | USA (San Francisco; Apomaya, Inc. dba Lokker) | Simulated sessions capture requests, cookies, payloads; **risk score 0–1000** in 7 categories (incl. Form Data, Session Replay, Geo); reason codes mapped to HIPAA/VPPA/CCPA/GDPR with remediation; consent validator; PDF/Excel evidence exports | No public prices; "Request a demo"; fees set per order | Law firms Orrick, Troutman Pepper Locke, Stinson; insurers Chubb, CFC; City of Hope | NOT VERIFIED: $5.9M (CB Insights) to $15.6M (other aggregators); investors Ulu Ventures, Richmond Global Ventures, DH Capital | **Reason codes** (each finding = code + law + severity + fix) — same as our rule IDs; partner API for law firms | US litigation focus (CIPA, VPPA); no country map; no Uzbek law | https://www.lokker.com |
| **Privaini** | USA (San Mateo, CA) | Outside-in risk assessment from a company name or domain: findings mapped to statutes in "90 countries"; policy vs observed practice; **fine/settlement exposure range per finding**; corporate footprint (subsidiaries, microsites) | No public prices; 3-week sale: demo → 5 of your entities assessed before contract → contract | Insurers/brokers Arch, Beazley, Chubb, Marsh, Sompo, WTW; customers Grammarly, Paychex, Herbalife, Dayforce; "4 of 10 top cyber insurers" | NOT VERIFIED: ~$2.0M pre-seed (Nov 2023, VCBacked / FundedIQ) | **Money exposure per finding** (fine range in BCA, once V-05 is closed); assess the prospect's sites for free before the contract | Sells risk to insurers, not fixes to site owners; "90 countries" list not public (Q6) | https://www.privaini.com/how-it-works |
| **WhoGetsMyData** | Switzerland (operator "WhoGetsMyData", Swiss law) | Free: homepage + 3 pages; Chromium opens the site 3 times (before choice / after Reject / after Accept); 3,319 services catalog; **where form data would be sent**; key-logging test with made-up text (forms never submitted); policy promise check; companies by country on a **world map**; signed evidence (SHA-256, Ed25519); score 0–100; history of changes | Free, no account; voluntary donations | No customers; "157,514 sites scanned"; avg. 14.6 external organisations per homepage | Donations only | Per-service policy check labels ("Named / Company named / Only the kind of service / Not found"); signed evidence chain; change history | **Not a legal assessment** — no law mapping, no rules, no fixes; Swiss/EU focus; no uz/ru | https://whogetsmydata.com/methodology |

### Feature matrix — our six claimed differences

`yes` = stated on the company's pages · `partial` = something close, see note · `no` = not stated on pages read.
"Uzbek" column: whether Uzbekistan/CIS law is named anywhere on the pages read.

| Company | 1. Uzbek law, uz/ru, local services | 2. Policy vs behavior | 3. Where form data goes | 4. Country map / cross-border | 5. Evidence pack | 6. Fixed documents |
|---|---|---|---|---|---|---|
| Privado | no | partial ("audit … for compliance with your privacy policies") | no | partial ("Flag cross-border data flows") | partial (records PD sent to third parties) | partial (DPIA/RoPA, not policies) |
| Vakteye | no (EU only) | **yes** ("compares what your privacy policy promises against what the site does") | partial (forms checked; destination not stated) | partial (transfers outside EU flagged, DPF check; no map) | **yes** (browser recording, network log, timeline, zip with integrity check) | no |
| Cookiebot | no | no | no | NOT VERIFIED (a support article seen only in search results says "country (adequate / not adequate)"; Cookiebot's own pages read on 21.11 do not say it; support site HTTP 403) | partial (consent records 12 months) | partial (privacy-policy generator, cookie declaration; Uzbek not checked) |
| Didomi | no | partial (is each vendor declared in the notice) | no | partial (recommendation "trackers from non-GDPR-adequate countries"; Vendor Trust Index uses the CNIL country-risk dataset; no map) | partial (time-stamped audit trail, JSON export) | partial (cookie-policy generator; 45+ notice languages) |
| OneTrust | no | partial ("policy gaps", method not described) | partial (forms detected, fields classed personal / non-personal; destination not stated) | partial (Services tab shows vendor location; no transfer check) | partial ("audit-ready history") | partial (cookie list into policies; notices in many languages) |
| c/side | no | partial (best practice in blog; "processors within intended scope") | **yes** (form/email field read → endpoint) | **yes** (map of cross-border flows; "when the data leaves the EEA") | partial (exportable evidence package, script hashes) | no |
| Feroot | no | partial (consent choices respected; not policy text) | partial (alerts when trackers access input fields) | **yes** ("Unauthorized Countries", world map) | partial (compliance reports, historical proof) | partial (RoPA generator) |
| Lokker | no | partial (customer guides) | **yes** (injects synthetic PII into forms and records which third parties receive it) | partial ("Geo": countries where requests resolve, restricted geographies; no map) | partial (PDF/Excel exports, payload explorer) | partial (example disclosure language) |
| Privaini | no ("90 countries", list not public) | **yes** ("maps declaration vs. observed practice") | no | no | partial (reproducible, timestamped) | no |
| WhoGetsMyData | no | **yes** (promise check: "Contradicted by the scan") | **yes** ("where form data would be sent") | **yes** (company country on a world map — operator's seat, not server location) | partial (SHA-256 + Ed25519 signed records; no screenshots/HAR) | no |
| **Probo (today, from README)** | **yes** (ZRU-547, 27-1, CMR 415 draft list, entities.yaml with Uzbek services) | yes (PD-MIS-01, quotes verified by code) | yes (PD-LOC-01) | yes (server country + owner company) | partial (HAR + facts.json; F-06 planned) | no (F-04 planned) |

Reading the matrix: on differences 2–5 we are **one of several**; only difference 1 is unique among the ten, and
difference 6 (fixed documents in Uzbek/Russian) is unique only if we actually build F-04 and nobody's generator
supports Uzbek (not checked).

### Feature lists per company (what each product does)

**Privado.ai** (https://www.privado.ai/pricing, https://privado.ai/cookie-consent, https://www.privado.ai/)
- Web Auditor: scans simulating consent accept / reject / no action
- Custom journey scans (login, actions); cookie, pixel and script discovery
- Cookie agent that checks categorization by researching the internet in real time
- Consent banner checks; geo-targeted banners
- Data-flow maps to third parties, by consent state; cross-border flags; sensitive-data leak detection
- Real-time risk alerts + auto-generated Jira/Linear tickets; automatic monthly scans
- App Auditor (iOS/Android SDKs, consent, data flows); code privacy scanning
- Wren AI agent: privacy intake, triage, assessments, RoPA; contract scanning
- Privacy management platform: PIA, DPIA, RoPA; integrations with OneTrust, TrustArc
- Free audits of other vendors' CMPs (Ketch, Transcend, TrustArc, OneTrust) and GPC

**Vakteye** (https://www.vakteye.com/en/pricing)
- Cookie/tracker detection against 400,000+ tracker domains; cookie security flags
- Tests that "Reject" really works; zombie cookies; dark patterns, pre-checked boxes, dead buttons
- Fingerprinting (canvas, WebGL, audio) and session-replay detection
- Privacy policy checked against GDPR art. 13 sections; policy-vs-practice contradictions
- Third-country transfer mapping; US recipients without DPF certification flagged
- Security headers, TLS, passive CVE / vulnerable library scan, exposed services, subdomain takeover, secrets in JS
- WCAG 2.1 AA accessibility checks
- Enterprise: forms, data residency, CNAME tracking
- Scheduled monitoring (monthly / weekly / daily) with notifications; human review queue
- Evidence: browser recording, network log, cookie timeline, downloadable zip with integrity check
- Public "Privacy Monitored" badge with record number; DPIA-ready and board reports

**Usercentrics Cookiebot** (https://www.cookiebot.com/en/pricing/, https://www.cookiebot.com/en/cookie-scanner/)
- Monthly automated cookie/tracker scan (daily for +€99/mo); crawls subpages, simulates users, watches third-party traffic
- Automatic categorization; cookie declaration (type, duration, provider, purpose)
- Manual and automatic blocking; consent banner (dialog, bar, compact), custom HTML/CSS/JS
- 47+ banner languages, auto-translation; geotargeting by region/country
- Google Consent Mode, Microsoft UET, Amazon Consent Signal, GPC, IAB TCF 2.4
- Privacy-policy generator; consent records up to 12 months; consent analytics; CSV export
- Configuration health checker; cross-domain consent sharing; SSO, API/SDK, A/B tests (Advanced)

**Didomi** (https://www.didomi.io/, https://didomi.io/advanced-compliance-monitoring, https://www.didomi.io/offers)
- Multi-regulation CMP (web, mobile apps, CTV); preference management
- Tracker, script and vendor scanning; daily / weekly / monthly scans
- Accept-all / refuse-all / no-action scenarios; trackers before consent or after refusal
- Is each vendor declared in the privacy notice; CMP vendor matching
- Weekly alerts; time-stamped audit trail; JSON export; consent proofs
- Cross-domain consent sync, notice A/B tests, consent analytics
- Privacy requests (access, deletion, opt-out — early access); server-side tagging (Addingwell)
- Cookie-policy generator; 45+ notice languages

**OneTrust** (https://www.onetrust.com/products/cookie-compliance, Compliance Assistant blog)
- Detects cookies, tags, trackers, pixels, beacons; simulated users, scans behind logins, hidden pages
- 45M pre-categorized cookies; scheduled scans; cookie list auto-filled into policies
- Banner templates, geolocation rules, 250+ languages, A/B tests; auto-blocking
- Consent transaction database; cross-device sync; mobile and CTV consent
- Compliance Assistant: daily scans, 12 months of results, Compliance Score
- Validates Google Consent Mode, GPC, IAB TCF/GPP; maps regulations by geolocation and domain
- Flags unauthorized tracking, dark patterns, broken consent signals, with remediation guidance
- Scans run from the regulated region (UK from London, EU from Amsterdam)

**c/side** (https://cside.com/, https://cside.com/pricing, Help Net Security 21.01.2026)
- Monitors third-party scripts in real browser sessions; script inventory and change monitoring (PCI DSS)
- Privacy Watch: what data scripts access and where they send it; scripts firing before consent
- Form/cookie data sent to unexpected endpoints; cross-border flow map; alerts on new destinations
- Script blocking before consent; CSP-based blocking
- Alerts to Slack/Teams/email/webhook; audit-ready reports; full payload logs; exportable evidence package
- AI-written per-script justifications; dependency graph / vendor load chain
- Separate Fingerprint product: device ID, bot/AI-agent detection, VPN/proxy detection

**Feroot Security** (https://www.feroot.com/, https://www.feroot.com/pricing/)
- Discovers trackers, scripts, cookies, data assets; free pre-consent scan
- DXComply: consent audits, cookie tracking, policy enforcement, evidence
- Data-transfer monitoring: "Unauthorized Countries", world map by country and hostname
- PaymentGuard (PCI 6.4.3/11.6.1); DXSecure: blocks skimming, formjacking, exfiltration
- Alerts when trackers access geolocation, login, password or card fields; PII/PHI exfiltration detection
- Consent choice analysis, geographic consent rules; automated compliance reports, AI attestation
- Free browser extension (inventory + data-access log export); free RoPA generator, cookie and checkout scanners
- SIEM integrations, API, SSO

**LOKKER** (https://www.lokker.com, https://lokker.com/llms-full.txt)
- Privacy Edge: simulated sessions capture requests, cookies, local storage, payloads, initiator chains
- Risk score 0–1000 + letter grade over 7 categories (Cookies, Form Data, Session Replay, Trackers, Consent, Geo, Perimeter)
- Reason codes mapped to HIPAA, VPPA, CCPA, CPRA, GDPR, with severity and step-by-step remediation
- Exports: risk & remediation PDF, GPC PDF, payload explorer and digital objects (Excel)
- 3D request graph; waterfall of initiator chains; scan data kept indefinitely; daily/weekly digests
- Guardian: one script on the client site that blocks untrusted requests and inspects payloads for PII
- Consent validator (no action / accept / reject / GPC); browser extension; partner API; training academy

**Privaini** (https://www.privaini.com/platform-overview, https://www.privaini.com/how-it-works)
- Outside-in assessment from a company name or domain; no install, no credentials
- Findings mapped to statutes; reproducible, timestamped; claimed coverage 90 countries and 20 US states
- Exposure modelling: litigation, regulatory, remediation, reputational — money range per finding
- Consent-flow failures (pre-checked boxes, dark patterns, firing before rejection)
- Policy analysis: privacy policy and terms vs observed practice
- Corporate intelligence: subsidiaries, microsites, digital footprint
- 8 finding categories: wrongful collection, consent, AI governance, video/tracking (VPPA/CIPA), biometrics (BIPA), children (COPPA), sharing/sale, retention
- Phased remediation plan; sample report on request

**WhoGetsMyData** (https://whogetsmydata.com/, https://whogetsmydata.com/methodology)
- Homepage + up to 3 linked pages (contact, shop, booking); real Chromium
- Three visits: before any choice, after Reject, after Accept
- Catalog of 3,319 services from 3,747 organisations
- Policy check per service (Named / Company named / Only the kind / Not found) + promise check vs scan
- Forms: where data would be sent, which fields; key-logging test with made-up text (never submits)
- Fingerprinting, Meta Pixel, session recording, remarketing, cookie syncing, hashed contact details
- Companies by country on a world map; hosting, CDN, DNS, mail providers
- Privacy headers; score 0–100 with per-rule breakdown; history of changes between scans
- Signed evidence record per scan (SHA-256, hash chain, Ed25519); robots.txt opt-out; browser extension

## Honest conclusion: where we really differ, and where we don't

**Not different (others already do it):** policy vs behavior, country map, form-data destination, before/after
consent tests, a 0–100 score, hashed evidence. In the pitch these are "what a modern scanner must do", not our moat.

**Different (none of the ten states it, as of 21.11.2026):**
- the law: ZRU-547 with the 2026 art. 27-1, the CMR No. 415 list of 49 countries, Uzbek liability articles — encoded as
  lawyer-editable YAML rules, updated when lex.uz changes (F-16);
- the language: report and fixed documents in Uzbek (Latin) and Russian;
- the local catalog: Uzbek trackers, CRMs, payment and delivery services, Telegram bots (`entities.yaml`);
- policy quotes verified by code (others don't describe how they avoid model errors);
- price level for Uzbek SMBs (to be proven by R-06 interviews).

**Risks:** a big player can add a jurisdiction (OneTrust buys legal content for "300+ jurisdictions"; Privaini claims
"90 countries" without a public list). Our defence is speed and depth on one country plus local data, not technology.

**One sentence for the jury question "What if OneTrust or Cookiebot come?" (passport §13):**
"They check cookies against GDPR and the EU list; none of the ten global tools we studied mentions Uzbekistan — we
check ZRU-547, article 27-1 and the list of 49 countries, in Uzbek and Russian, with a catalog of local services, at a
price local businesses can pay (Privado starts at $600 per site per month)."

## Feature ideas (passport §10 format)

- F-17 · Policy coverage per service with 4 labels (named / company named / only the kind / not found) · clear,
  low-risk wording for PD-POL-02 · S · borrowed from WhoGetsMyData, Ours Privacy · proposal · Final
- F-18 · Before / after consent scenarios (no action / reject / accept) as three visits · stronger evidence for PD-TRK-01 ·
  M · borrowed from Didomi, WhoGetsMyData, Vakteye · proposal · Roadmap
- F-19 · Signed evidence pack (SHA-256 of HAR + screenshots + policy text, timestamp, signature) · makes F-06
  court-grade · S · borrowed from WhoGetsMyData, Vakteye · proposal · Final
- F-20 · Fine exposure per finding (range in BCA from the cited article) · speaks the business owner's language (money) ·
  S once V-05/V-11 are closed · borrowed from Privaini · proposal · Final
- F-21 · Scan from an Uzbek IP address · the site behaves as for a real Uzbek visitor (geo-targeted banners, trackers) ·
  S · borrowed from OneTrust (scans from the regulated region) · proposal · Final
- F-22 · Human review queue for low-confidence findings ("awaiting lawyer check") · matches D-019 and the lawyer's role ·
  S · borrowed from Vakteye · proposal · Roadmap

## Questions for the team / contradictions with the passport

- **Q1 (resolved 21.11).** Alii does research (R-04 competitors); the code is written by Role 1.
- **Q2 (F-01 / §8 / §13 wording — now confirmed).** §8 says CMPs have "No 'policy vs behavior' check" — true for
  Cookiebot, but Vakteye, Privaini and WhoGetsMyData do it. F-01 "the main difference from all competitors" should
  become "the first such check under Uzbek law, with quotes verified by code".
- **Q3 (§13 answer).** Replace "They don't have Uzbek law, the language or a database of local services" with the
  sentence above (it adds evidence and a price).
- **Q4 (file name).** `research/competitors-global.md` for global; CIS part → `research/competitors.md`. OK?
- **Q5 (D-009 vs a competitor).** WhoGetsMyData types made-up text into form fields on **any** site (without
  submitting) to catch key-logging scripts. D-009 allows canaries only on clients' sites. Keep D-009 as is (safer for
  S4), or allow this passive variant? Team decision — not changed here.
- **Q6 (Privaini "90 countries").** Ask Privaini for a sample report / country list to check whether Uzbekistan is
  covered (they offer "See a sample report").
- **Q7 (unverified numbers).** Lokker and Privaini funding figures come only from aggregator databases that disagree;
  Cookiebot's country labels come from a support article our fetcher could not open (HTTP 403). Don't use these three
  in the pitch until checked.

## Sources (Step 1B)

- Privado: https://www.privado.ai/pricing · https://www.privado.ai/solutions/web-privacy · https://privado.ai/cookie-consent · https://www.privado.ai/customers · https://www.privado.ai/about · https://www.privado.ai/terms-of-service · https://yourstory.com/2022/08/privado-raises-14mn-insight-partners-sequoia-capital · https://www.privado.ai/post/privado-series-a-launch
- Vakteye: https://www.vakteye.com/en/pricing · https://www.vakteye.com/en/insights/privacy-policy-contradictions-guide · https://www.vakteye.com/en/about · https://www.vakteye.com/en/terms-of-service
- Cookiebot / Usercentrics: https://www.cookiebot.com/en/pricing/ · https://www.cookiebot.com/en/cookie-scanner/ · https://www.cookiebot.com/en/legal-notice/ · https://usercentrics.com/about-us/ · https://support.cookiebot.com/hc/en-us/articles/5007079527580-Understanding-the-scan-report (HTTP 403 to our fetcher)
- Didomi: https://www.didomi.io/ · https://didomi.io/advanced-compliance-monitoring · https://www.didomi.io/free-compliance-scan · https://www.didomi.io/offers · https://www.didomi.io/about · https://www.didomi.io/legal-notice
- OneTrust: https://www.onetrust.com/products/cookie-compliance · https://www.onetrust.com/blog/introducing-compliance-assistant-continuous-website-risk-monitoring-within-your-cmp/ · https://www.onetrust.com/pricing/ · https://www.onetrust.com/company/ · https://www.securityweek.com/onetrust-raises-150-million-at-4-5-billion-valuation/ · https://www.bloomberg.com/news/articles/2023-07-24/onetrust-raises-150-million-from-vcs-al-gore-s-firm
- c/side: https://cside.com/ · https://cside.com/pricing · https://cside.com/use-cases/compliance/gdpr · https://cside.com/blog/how-to-monitor-cross-border-data-transfer-on-your-website · https://cside.com/privacy-policy · https://www.helpnetsecurity.com/2026/01/21/cside-privacy-watch/ · https://cside.com/blog/cside-raises-a-6m-seed-round
- Feroot: https://www.feroot.com/ · https://www.feroot.com/pricing/ · https://feroot.com/feroot-pagescanner/ · https://www.feroot.com/gdpr-website-compliance-solution/ · https://www.feroot.com/about/ · https://www.feroot.com/news/feroot-security-raises-14m-series-a-to-scale-ai-powered-compliance-platform-protecting-websites-and-applications
- Lokker: https://www.lokker.com · https://lokker.com/llms-full.txt · https://lokker.com/about · https://lokker.com/terms-of-use · https://lokker.com/privacy-policy · https://www.cbinsights.com/company/lokker/financials
- Privaini: https://www.privaini.com/ · https://www.privaini.com/platform-overview · https://www.privaini.com/how-it-works · https://www.privaini.com/about-us · https://www.vcbacked.co/company/privaini
- WhoGetsMyData: https://whogetsmydata.com/ · https://whogetsmydata.com/methodology · https://whogetsmydata.com/about · https://whogetsmydata.com/terms · https://whogetsmydata.com/privacy · https://whogetsmydata.com/supporters

---

## Part 2 — the remaining 17 (read 21.11.2026 on their own sites)

### Table §11.3

| Name | Country | What they do | Model and prices | Clients (vendor-stated) | Investment / owner | What to borrow | How we differ | Link |
|---|---|---|---|---|---|---|---|---|
| **iubenda** | Italy (iubenda S.r.l., Milan) | CMP + cookie scanner; self-updating privacy & cookie policy and T&C generators (27 languages); free compliance site scanner; enterprise Compliance Monitor | Free plan; Essentials €4.99/site/mo (yearly; 25K pageviews, 1 language); Advanced €19.99 (50K, all languages); Ultimate €79.99 (150K, hourly scans); enterprise on request | "150K+ customers", "400K+ sites and apps"; Criteo, Siemens, UNICEF, Honda, Sony Music | Part of team.blue since 2022; parent of consentmanager, CookieFirst, Complianz | **Self-updating policy generator** (= our F-04 done right); CMS plugins | Uzbek/Russian not in UI list (27 document languages not listed); no flows/countries; no Uzbek law | https://www.iubenda.com/en/pricing |
| **TrustArc** | USA (TrustArc Inc, Walnut Creek, CA; founded 1997 as TRUSTe) | Cookie consent + Website Monitoring Manager: deep scans behind logins, tracker risk index (PSI), resource-chain analysis; data-flow map with cross-border transfers; 800+ templates | No public prices (pricing page 404); demo | "1500+ companies"; Abbott, ADP, GE, Hilton, Nike, Starbucks | Bought by Main Capital Partners (Oct 2025) from Bregal Sagemount ($70M in 2019) | Tracker risk index; resource chains | Enterprise; no CIS law; countries only in data-mapping module | https://trustarc.com/products/consent-consumer-rights/website-monitoring-manager/ |
| **Securiti** (Privacy Center / Consent Agent) | USA (Securiti, LLC, San Jose) | Scans site, auto-generates cookie banner and cookie policy, auto-blocking; Consent Agent checks pre-consent tracking, GPC, TCF, dark patterns; notices in 8 languages | Privacy Center Business **$599/mo** or $6,110/yr (5 domains); Enterprise custom | Not named | Acquired by Veeam for ~$1.725B (announced Oct 2025, Dec 2025 per Securiti) | Agent that checks consent config vs real user experience | No ru/uz among 8 languages; no country map; enterprise | https://securiti.ai/privacy-center/pricing/ |
| **Reflectiz** | Israel (HQ and R&D in Tel Aviv; hubs Boston, Sydney) | Agentless scans (URL only) simulating user journeys; trackers before consent / after rejection / ignoring GPC; **audits tracker classification against the published privacy policy**; mapped data flows | Quote only: Privacy Hub Standard (≤10 sites) / Professional (≤50 sites); add-ons | DAZN, Cox, lastminute.com, Payoneer, Castore | "$22M Series B" (own site; investors not named) | Peer-benchmarked "Privacy Rating" | GDPR/CCPA/HIPAA/PIPEDA only; no country view | https://www.reflectiz.com/plans/ |
| **ObservePoint** | USA (ObservePoint, Inc., Pleasant Grove, Utah) | Synthetic-traffic crawl of every page, tag and cookie; Reject-All and GPC tests; visits from different geographies; initiator chains; scheduled journey tests (checkout, login, forms) | Priced by pages scanned (calculator; figures not shown); free privacy scan | Microsoft, Mercedes-Benz, Pepsi, Disney, US Bank, Adobe | ~$32–38M per aggregators (Mercato, Pelion) — NOT VERIFIED | "Hand your lawyers proof of what ran, where, and when" — journey tests on forms | Marketing-analytics roots; no country view; GDPR/CPRA only | https://www.observepoint.com/solutions/web-privacy/ |
| **Captain Compliance** (Patrol) | USA (Captain Compliance Corp., Fort Lauderdale, FL; founded 2023) | Patrol: on-demand URL audit — cookies, trackers, banner, reject button, pre-consent cookies, GPC/TCF/GPP; **statute-mapped findings**; **PDF with SHA-256, HAR, screenshots, timestamps**; remediate & re-scan | Free (1 domain); Professional $499 (period not stated); Enterprise quote; Patrol price not stated | Advantage Rent A Car, JD Power, TaylorMade | Not stated; "Compliance Shield" covers up to $2M legal costs (contractual) | **Evidence format** (hash + HAR + screenshots) = target for our F-06/F-19 | GDPR/CCPA/ePrivacy (+LGPD company-wide); no countries, no forms | https://captaincompliance.com/platform/patrol/ |
| **webXray** | NOT VERIFIED (webXray LLC; founder Tim Libert, ex-Google) | Litigation search of violations across 1.2M sites in regulated sectors; forensic website preservation; consent-bypass analysis; expert testimony; scans from residential IPs in EU / California / US | Demo only | "Top US class action law firms and Fortune 100 compliance teams" (no names) | Not stated | **Forensic preservation** before a case; scans from the regulated region | US litigation tool; no fixes, no other laws | https://webxray.ai/litigation |
| **Darrow** | USA / Israel (Darrow Inc., New York / Tel Aviv; 2020) | "Legal exposure management": AI finds violations in public data for plaintiff firms and insurers; case valuation, intake | Demo only | Law firms Baron & Budd, Milberg, Kahn Swick & Foti; "80+ organizations", "$22B+ legal exposure surfaced" | ~$60M (Sacra); investors Georgian, F2, NFX, Entrée, Y Combinator | Money estimate per case; selling to law firms | Not a site scanner; precedent only | https://www.darrow.ai/platform |
| **noyb / WeComply** | Austria (non-profit association, Vienna) | 2021: software recognised unlawful cookie banners, sent 560 draft GDPR complaints in 33 countries; WeComply portal for site owners (guide + report compliance, 60-day grace period); 895 cases total | Free for companies; funded by 5,554 supporting members (€60–500+/yr) and donations | Targets, not clients (Booking, Cisco, WarnerMedia…) ; claims "€2B fines imposed" | Donations / members | "Draft complaint + fix guide + grace period" = a soft-enforcement model a regulator could use with us (B2G) | EU law only; NGO; no product to buy | https://wecomply.noyb.eu/en/app/faq |
| **SitePrivacyScore** | NOT VERIFIED (Delaware law in terms) | Free early access: trackers, cookies, consent validator, headers, PII leak checker, **policy analyzer**, **data-transfer scanner tracing destination IPs to location**, PDF summary, privacy-policy template | Free during early access | "10,000+ scans" | Not stated | IP → map location per vendor (same as ours) | Early-stage; no Uzbek law; no evidence pack | https://www.siteprivacyscore.com/tools/data-transfer-risk-scanner |
| **Datascale** | Germany (Datascale One GmbH, Gräfelfing) | Consultancy: free Tracking Check (39 checks), accept vs reject diff, privacy-policy match; paid audit sprints | Audit Sprint from €1,490 net (3 days); Plus from €2,900 net | "70+ setups across DACH" | Not stated | Fixed-price audit package (one-off "way in" = our Fix pack) | Service, not software; "legal assessment belongs to your counsel" | https://datascale.de/en/ |
| **Ours Privacy** | USA (Ours Wellness Inc., Houston, TX) | HIPAA marketing CDP + CMP; Web Scanner **reads the policy and flags contradictions**, weekly scans, 90-day history | Custom pricing by tracked users; demo | "200+ healthcare organizations"; WebMD Ignite, Maven Clinic, Midi Health | $15M Series A (Aug 2026, Lightbank, Health Velocity Capital) | Vertical focus (healthcare) → we could start with one sector (fintech/MFO) | US health only | https://oursprivacy.com/product/web-scanner |
| **EDPS Website Evidence Collector** | EU (European Data Protection Supervisor) | Open-source (EUPL-1.2) tool that automates collecting evidence of storage and transfer of personal data on websites; Puppeteer-based | Free | EU regulators (implied) | Public | Open, regulator-accepted evidence format | Evidence only, no law mapping, EU only | https://code.europa.eu/EDPS/website-evidence-collector |
| **EDPB Website Auditing Tool** | EU (EDPB Support Pool of Experts) | Open-source (EUPL-1.2) audit tool for DPAs and controllers: tracker evaluation, full-page screenshot, final audit report, knowledge databases with trust levels; imports EDPS WEC results; EN/FR/DE/IT/ES | Free | Data protection authorities; controllers | Public | **Regulator workflow** (prepare → run → evaluate → report) = what a B2G pilot with Uzbekistan's authorized body would need | EU only; manual auditor tool | https://www.edpb.europa.eu/documents/support-pool-of-experts/edpb-website-auditing-tool_en |
| **Blacklight** | USA (The Markup, non-profit newsroom) | Free real-time inspector, 9 tests (third-party cookies, ad trackers, **key logging**, session recording, canvas fingerprinting, Meta, Google remarketing, X, TikTok); location choice (Ohio, California, Europe); collector code open source (GPL-3.0) | Free | Journalists, public; 2020 survey of 100,000 sites | Donations | Plain-language results for citizens (S5 social impact) | No law, no policy check ("does not check… privacy policies") | https://themarkup.org/blacklight |
| **ImmuniWeb Website Privacy Test** | Switzerland (ImmuniWeb SA) | Free test: privacy policy check, third-party content, tracking cookies, XHR, pixels, web forms; PDF report; **publishes scanner IP ranges**; API | Free 10 tests/month (20 with account); Premium €25/mo (50 tests) … €499/mo (2,500 tests) | SMBs, municipalities, universities; "1,356,323 tests performed" | Not stated | Publish our scanner IPs so sites can allowlist (answer to "don't sites block bots?") | GDPR only; no countries; no fixes | https://www.immuniweb.com/privacy/limits/ |
| **ComplyZero** | India (Lanos Technologies Pvt. Ltd., Mumbai) | DPDP-only governance suite: request portal, consent hub (QR, kiosks, paper), website consent + cookie scans, PII discovery, registers, breach desk, readiness score, **sealed evidence (SHA-256 + Ed25519)**; data stored in India | Foundation ₹99,000/yr + GST (₹9,000/mo); Standard ₹2,09,000/yr; Compliance Pro ₹4,18,000/yr; Enterprise from ₹11 lakh/yr | Not named; study of 6,000+ Indian sites (Feb 2026): 95.9% without proper consent, 2 of 1,154 government sites with a banner | Not stated | **National-law-only positioning + a national study as PR** (= our F-03 "Uz-net Privacy 2026") | Governance suite, not a behavior scanner; India only | https://complyzero.com/pricing |

**Academic prior art** (not companies):
- **Libert 2018** (WWW '18): third-party flows on 1 million websites vs 200,000+ privacy policies — fewer than 15% of
  third-party flows disclosed. https://arxiv.org/abs/1805.01187
- **PoliCheck** (Andow et al., USENIX Security 2020; IBM, NC State, UC Berkeley): entity-sensitive policy vs data-flow
  check on 13,796 Android apps — up to 42.4% disclose incorrectly or omit. https://www.usenix.org/conference/usenixsecurity20/presentation/andow
- **PoliGraph** (Cui et al., USENIX Security 2023; UC Irvine): policy as a knowledge graph; 40% more collection
  statements found, 97% precision; compared with network traffic. https://www.usenix.org/conference/usenixsecurity23/presentation/cui

### Feature matrix — part 2

| Company | 1. Uzbek law | 2. Policy vs behavior | 3. Form data destination | 4. Country / cross-border | 5. Evidence pack | 6. Documents |
|---|---|---|---|---|---|---|
| iubenda | no | no | no | partial (enterprise Compliance Monitor: visual map of vendors by country) | partial (consent logs) | **yes** (policies, T&C; 27 languages, uz/ru not confirmed) |
| TrustArc | no | partial (notices vs trackers) | partial (tracker chains) | partial (data-flow map with cross-border transfers) | partial | partial (reports, templates) |
| Securiti | no | partial (consent config vs real experience) | no | no | partial | **yes** (cookie policy, notices; 8 languages, no ru/uz) |
| Reflectiz | no | **yes** (classification vs published policy) | no | no | partial (logs, reports) | no |
| ObservePoint | no | partial (cookie policy in sync) | partial (data to third parties; form journeys) | partial (approved-geolocation lists; "Domains & Geo" report; selectable scan location) | partial ("proof of what ran, where, when") | no |
| Captain Compliance Patrol | no | partial (company-level claim) | no | no | **yes** (SHA-256, HAR, screenshots, timestamps) | partial (hosted notices, company-level) |
| webXray | no | partial (founder's research) | no | no | partial (forensic preservation, export) | no |
| Darrow | no | no | no | no | no | no |
| noyb / WeComply | no | partial (banner behavior verified) | no | no | partial (HTML, data flows, screenshots) | **yes** for its own complaints (EN/DE + 5 languages) |
| SitePrivacyScore | no | **yes** | no | **yes** (destination IP → location) | partial (PDF) | partial (policy template) |
| Datascale | no | **yes** (tools missing from policy) | no | no | partial (audit evidence) | no |
| Ours Privacy | no | **yes** ("flags where your site contradicts what you published") | partial | no | partial (consent log, PDF) | no |
| EDPS WEC | no | no | no | not stated (README not readable) | partial (evidence collection) | no |
| EDPB WAT | no | no | no | no | partial (screenshot, audit report) | no |
| Blacklight | no | no ("does not check… privacy policies") | partial (key-logging test) | no | partial (HAR, screenshots, JSON; open source) | no |
| ImmuniWeb | no | partial (policy check; comparison not described) | partial (web forms check listed) | no | partial (PDF) | no |
| ComplyZero | no (India DPDP only) | partial | no | partial (own data in India; no destination check) | **yes** (SHA-256 + Ed25519) | partial (notices "ready for you to approve") |

### Feature lists — part 2

**iubenda** (https://www.iubenda.com/en/, /en/pricing): consent banner with prior blocking · cookie/pixel/tracker
scanner (monthly; hourly on Ultimate) · Google Consent Mode v2, IAB TCF · consent logs · self-updating privacy and
cookie policy generator · T&C generator · consent database for forms · free compliance site scanner · enterprise
Compliance Monitor with severity-ranked vendor issues · geo-targeting · mobile SDK · AI accessibility widget ·
plugins for WordPress, Shopify, PrestaShop, Magento, Joomla · MCP connector for AI assistants.

**TrustArc** (website-monitoring-manager, cookie-consent-manager): unlimited tracker scans incl. behind logins ·
auto-categorization · auto-blocking / zero-cookie load · consent logs and dashboards · geo-IP banners · Privacy
Sensitivity Index per tracker · resource-chain analysis · change alerts · AI assistant "Arc" · mobile SDK consent ·
data mapping with transfer-risk view · trust center, rights requests, PIAs · 800+ templates (Nymity).

**Securiti** (privacy-center/pricing, consent agent brief): website scan → auto banner and cookie policy · auto
categorization and blocking · geo-adaptive banner, language detection · Google-certified CMP, IAB TCF · consent
dashboards · privacy notice builder (8 languages) · Consent Agent: pre-consent tracking, GPC, Consent Mode, TC string,
dark patterns · mobile consent · RoPA and DSR on the wider platform.

**Reflectiz** (/gdpr/, /plans/): agentless scan from a URL · simulated user journeys · trackers before consent / after
rejection / ignoring GPC · tracking after consent withdrawal · tracker and cookie map with classification · tracker
classification vs published privacy policy · iframe and third-party element scanning · continuous monitoring of
network requests · consent and HIPAA dashboards · inventory, data flows, AI remediation assistant · Slack, REST API,
OneTrust integration · peer-benchmarked privacy rating · weekly and executive reports.

**ObservePoint** (/, /solutions/web-privacy/): cloud scanner with synthetic traffic · full-site crawl of pages, tags,
cookies · Reject-All and GPC tests · visits from different geographies · initiator chains · unapproved-vendor flags
with risk level · cookie & tag database · scheduled journey tests (checkout, login, forms) · analytics, WCAG, consent,
email-link and landing-page validation · browser debugger extension, MCP server.

**Captain Compliance — Patrol** (/platform/patrol/): on-demand URL audit · cookies, trackers, banners, dark patterns ·
reject button, opt-out link, pre-checked categories, pre-consent cookies · GPC pass · TCF v2 / GPP validation · Consent
Mode detection · statute-mapped findings (GDPR, CCPA, ePrivacy articles) · PDF with SHA-256, HAR, screenshots,
timestamps · scheduled audits, new-tag alerts · vendor script review · remediate & re-verify. Company also sells CMP,
DSR portal, assessments, data mapping, hosted notices, trust center.

**webXray** (/litigation, /defense, /enterprise): violation search across 1.2M regulated-sector sites · forensic
website preservation (every page, transfer, line of code) · consent-bypass analysis · expert testimony · defense:
client scans, privacy-tool validation, complaint fact-checks, evidence export · enterprise: sitemap scans, polite
crawling, residential scan locations (EU, California, US) · privacy search engine · forensic export of payloads and
traffic · quarterly top-million scan.

**Darrow** (/platform): ingests filings, incident reports, litigation patterns · 50+ legal exposure categories · case
inventory with settlement estimates · portfolio dashboard, conflict checks, intake, document collection · AI assistant
on merits and precedent · insurance underwriting product.

**noyb / WeComply** (noyb.eu/node/281, wecomply FAQ): software that recognises unlawful cookie banners · automatic
draft GDPR complaints · legal team review of each case · step-by-step CMP fix guides · grace period before filing ·
portal for site owners to review case and report compliance · evidence: HTML, data flows, configs, cookie data,
screenshots, repeated scans · formal complaints to DPAs · mass scanning system.

**SitePrivacyScore** (/tools): tracker detector · cookie scanner · consent banner validator · security headers ·
privacy policy analyzer (behavior vs policy) · data transfer risk scanner (destination IP → location) · CCPA/CPRA
checker · session replay detection · PII leak checker · third-party request analyzer · privacy policy template ·
PDF executive summary · Chrome extension.

**Datascale** (/en/, /en/resources/tracking-check/): free Tracking Check (39 checks, 6 modules) · accept vs reject
request diff · privacy-policy match · consent-loss calculator · EU AI Act quick check · GDPR stack calculator · audit
sprints with evidence, priorities, estimates · server-side GTM setups.

**Ours Privacy** (/product/web-scanner, /product/consent-management-platform): agentic web scanner, weekly scans ·
reads the policy and flags contradictions · per-hostname policy coverage · CSP parsing, WCAG 2.2 checks · 90-day
history · blocking before consent · regional consent rules, consent log · HIPAA CDP with 50+ integrations · BAA,
SOC 2 Type II · PDF exports.

**EDPS Website Evidence Collector** (code.europa.eu/EDPS/website-evidence-collector): automated collection of evidence
of personal-data storage and transfer on websites · headless browser (Puppeteer) · data categories chosen by the EDPS ·
results importable into the EDPB tool · open source, EUPL-1.2. (README could not be read; details NOT VERIFIED.)

**EDPB Website Auditing Tool** (edpb.europa.eu): audit preparation, completion and evaluation · tracker evaluation ·
final audit report · import/export of analyses · knowledge databases with source and trust level · full-page
screenshots · imports EDPS WEC results · for legal and technical auditors · EN/FR/DE/IT/ES · open source, EUPL-1.2.

**Blacklight** (themarkup.org/blacklight): real-time scan of homepage + a deeper page · 9 tests (third-party cookies,
ad trackers, key logging, session recording, canvas fingerprinting, Meta pixel, Google remarketing, X pixel, TikTok
pixel) · location and device options · comparison with top 100,000 sites · owner names and categories per domain ·
outputs: cookies JSON, HAR, screenshots, inspection log · batch tool (Blacklight Query).

**ImmuniWeb Website Privacy Test** (immuniweb.com/privacy): privacy policy check · third-party content test ·
tracking cookies · XHR requests · tracking pixels · web forms check · data-scraping protection · PDF report ·
published scanner IP ranges · API · monitoring.

**ComplyZero** (complyzero.com): DPDP request portal with deadline clock · consent hub (QR, kiosk, staff, paper, app,
site) · website consent banner + cookie scans · PII discovery (Aadhaar, PAN, UPI and 30+ types) · data, processing,
vendor and retention registers · breach desk · hosted trust centre · readiness score and report · sealed evidence
vault (SHA-256, Ed25519) with free verifier · deep scan of folders · data stored in India.

### New feature ideas from part 2 (passport §10 format)

- F-23 · Publish our scanner's IP ranges and user agent · sites can allowlist us; honest answer to "don't sites block
  bots?" (§13) · S · borrowed from ImmuniWeb, OneTrust · proposal · Final
- F-24 · Evidence export compatible with the EDPS Website Evidence Collector / EDPB tool format · speaks the
  regulators' language for a B2G pilot · M · borrowed from EDPB WAT · proposal · Roadmap
- F-25 · "Draft notice + fix guide + grace period" mode for B2G (regulator sends the site owner our report and gives
  time to fix) · soft enforcement, social impact (S5) · M · borrowed from noyb WeComply · proposal · Roadmap

### Questions added by part 2

- **Q8 (D-009, stronger now).** Blacklight (open source, public) and WhoGetsMyData both type made-up text into form
  fields on any site, without submitting, to detect key-logging. Team decision on whether a passive variant fits D-009.
- **Q9 (positioning).** Closest business analog is ComplyZero (India): one national law, local data storage, national
  study as PR. Worth citing in the B-pitch as "this model works in other countries" — team decision.

### Sources (part 2)

- iubenda: https://www.iubenda.com/en/ · https://www.iubenda.com/en/pricing · https://www.iubenda.com/en/scan · https://www.iubenda.com/en/about-iubenda/
- TrustArc: https://trustarc.com/products/consent-consumer-rights/website-monitoring-manager/ · https://trustarc.com/products/consent-consumer-rights/cookie-consent-manager/ · https://trustarc.com/company/why-trustarc/ · https://trustarc.com/solutions/international-data-transfers/ · https://www.fenwick.com/insights/experience/fenwick-represents-trustarc-in-acquisition-by-main-capital-partners · https://www.sagemount.com/news/trustarc-receives-70m-investment-to-accelerate-privacy-technology-innovation/
- Securiti: https://securiti.ai/privacy-center/pricing/ · https://securiti.ai/solution-briefs/consent-agent-consent-compliance-detection-and-remediation-agent/ · https://securiti.ai/about/ · https://www.securityweek.com/veeam-to-acquire-data-security-firm-securiti-ai-for-1-7-billion/ · https://techcrunch.com/2025/10/21/veeam-acquires-data-security-company-securiti-ai-for-1-7b/
- Reflectiz: https://www.reflectiz.com/ · https://www.reflectiz.com/gdpr/ · https://www.reflectiz.com/plans/ · https://www.reflectiz.com/about/
- ObservePoint: https://www.observepoint.com/ · https://www.observepoint.com/solutions/web-privacy/ · https://www.observepoint.com/pricing/ · https://www.observepoint.com/service-agreement/ · https://www.cbinsights.com/company/observepoint/financials
- Captain Compliance: https://captaincompliance.com/platform/patrol/ · https://captaincompliance.com/pricing/ · https://captaincompliance.com/about-us/ · https://captaincompliance.com/ai-information/
- webXray: https://webxray.ai/ · https://webxray.ai/litigation · https://webxray.ai/defense · https://webxray.ai/enterprise
- Darrow: https://www.darrow.ai/ · https://www.darrow.ai/platform · https://www.darrow.ai/company/about · https://www.darrow.ai/company/newsroom · https://sacra.com/c/darrow
- noyb: https://noyb.eu/en · https://noyb.eu/node/281 · https://noyb.eu/en/project/cookie-banners · https://noyb.eu/en/support-us · https://noyb.eu/en/about-us · https://wecomply.noyb.eu/en/app/faq
- SitePrivacyScore: https://www.siteprivacyscore.com/ · https://www.siteprivacyscore.com/tools · https://www.siteprivacyscore.com/tools/privacy-policy-analyzer · https://www.siteprivacyscore.com/tools/data-transfer-risk-scanner · https://www.siteprivacyscore.com/terms
- Datascale: https://datascale.de/en/ · https://datascale.de/en/resources/tracking-check/ · https://datascale.de/en/resources/checks/privacy-policy-match/ · https://datascale.de/en/imprint/
- Ours Privacy: https://oursprivacy.com/product/web-scanner · https://oursprivacy.com/pricing · https://oursprivacy.com/about · https://oursprivacy.com/terms · https://fiercehealthcare.com/health-tech/hipaa-compliant-marketing-platform-ours-privacy-lands-15m
- EDPS / EDPB: https://code.europa.eu/EDPS/website-evidence-collector · https://www.edpb.europa.eu/documents/support-pool-of-experts/edpb-website-auditing-tool_en · https://code.europa.eu/edpb/website-auditing-tool
- Blacklight: https://themarkup.org/blacklight · https://themarkup.org/blacklight/2020/09/22/how-we-built-a-real-time-privacy-inspector · https://github.com/the-markup/blacklight-collector
- ImmuniWeb: https://www.immuniweb.com/privacy/ · https://www.immuniweb.com/privacy/about/ · https://www.immuniweb.com/privacy/limits/
- ComplyZero: https://complyzero.com/ · https://complyzero.com/pricing · https://complyzero.com/about · https://complyzero.com/security · https://www.complyzero.com/research/state-of-cookie-compliance-india-2026
- Academic: https://arxiv.org/abs/1805.01187 · https://www.usenix.org/conference/usenixsecurity20/presentation/andow · https://www.usenix.org/conference/usenixsecurity23/presentation/cui

---

# STEP 1A — shortlist (approved 21.11)

## Conclusions (Step 1A)

1. **"Policy vs behavior" (F-01 / PD-MIS-01) is NOT unique globally.** At least six live products claim it for websites
   (Vakteye, WhoGetsMyData, SitePrivacyScore, Datascale, Privaini, Ours Privacy); Didomi checks whether the notice
   declares each tracker. Academic prior art: Libert 2018 (websites), PoliCheck 2020 (apps). See Q2.
2. **Country / cross-border checks also exist** (c/side, Feroot, Privado, WhoGetsMyData; Cookiebot labels per support
   article). Nobody found checks against Uzbekistan's list (CMR No. 415) or art. 27-1.
3. **What still looks distinctive:** Uzbek law + uz/ru + local-services catalog; quotes verified by code; lawyer-editable
   YAML rules; the honest pitch is "the first such scanner for Uzbek law", not "the first in the world".
4. **The category is validated:** paid B2B, sold to compliance teams, insurers and litigators; regulators use the same
   approach (EDPS WEC, EDPB Website Auditing Tool).
5. **Local-law-first players exist elsewhere** (India: ComplyZero, 6,000-site study) — precedent for our F-03.

## Shortlist (24)

Closeness: **direct** = scans a live site and maps findings to a personal-data law; **partial** = one of the two, or
2+ of our six differences; **adjacent** = neighboring area / precedent. Countries updated with Step 1B findings.

| # | Name | Cat. | Country | What it does (1–2 lines) | Closeness | Why included | Conf. | Link |
|---|---|---|---|---|---|---|---|---|
| 1 | Privado.ai — Web Auditor | C | USA | Simulated journeys incl. login, data-flow maps, cross-border flags, preset regulatory checks | direct | Closest commercial analog | M | https://www.privado.ai/solutions/web-privacy |
| 2 | Usercentrics Cookiebot | A | Denmark / Germany | CMP + cookie scanner; destination country labels (support article) | direct | Market leader | H | https://www.cookiebot.com/en/cookie-scanner/ |
| 3 | OneTrust (Cookie Compliance) | A | USA | Cookie/tag scanning, policy auto-fill, daily Compliance Assistant | partial | Largest vendor; in passport §13 | H | https://www.onetrust.com/products/cookie-compliance |
| 4 | Didomi — ACM + free scan | A | France | Accept/refuse/no-action scans; trackers before consent; declared in notice? | direct | Pre-consent tracking + partial policy check | H | https://www.didomi.io/free-compliance-scan |
| 5 | iubenda — compliance scanner | A | NOT VERIFIED | URL check of policy, cookie policy, banner, terms vs laws | partial | Document-side check; policy generator | M | https://www.iubenda.com/pt-br/scan |
| 6 | TrustArc — Website Monitoring Manager | A/C | NOT VERIFIED | Tracker monitoring incl. which script loaded which tracker | partial | Enterprise benchmark | M | https://trustarc.com/products/consent-consumer-rights/website-monitoring-manager/ |
| 7 | Securiti — Cookie Consent / Consent Agent | C | NOT VERIFIED | Scan, classify, banner and policy; 80+ jurisdictions | partial | Multi-jurisdiction encoding | M | https://securiti.ai/privaci/cookie-consent-management/ |
| 8 | Feroot | D | Canada | Script/PII monitoring, unauthorized countries map, 70+ laws | direct | "Which script sees which data" | M | https://feroot.com/feroot-pagescanner/ |
| 9 | c/side — Privacy Watch | D | USA | What scripts access and where they send it; cross-border map | direct | "Where does data go, which country" | M | https://cside.com/blog/how-to-monitor-cross-border-data-transfer-on-your-website |
| 10 | Reflectiz | D | NOT VERIFIED | Agentless monitoring of third-party web components | partial | Same outside-in model | L | https://www.reflectiz.com/gdpr/ |
| 11 | ObservePoint | D | NOT VERIFIED | Web governance audits: tags, cookies, policy links | partial | Report benchmark | M | https://www.observepoint.com/solutions/web-privacy/ |
| 12 | Lokker — Privacy Edge | D/E | USA | Trackers, harvested PD, law alerts, risk score | direct | Close business pattern | M | https://www.lokker.com |
| 13 | Captain Compliance — Patrol | D/E | NOT VERIFIED | URL scan, statute mapping, hash-verified evidence | direct | Evidence pack analog | L | https://captaincompliance.com/education/privacy-risk-scanning-tools-comparison/ |
| 14 | webXray | E | NOT VERIFIED (webXray LLC) | Forensic tracking scans for litigators | direct | "Scan → legal case" | M | https://webxray.ai/ |
| 15 | Privaini | E/F | USA | Outside-in scans mapped to statutes; policy vs practice; insurers | direct | Outside-in, insurance channel | M | https://www.privaini.com/ |
| 16 | Darrow | E | NOT VERIFIED | AI finds legal violations for plaintiff firms; ~$60M raised | adjacent | Precedent (passport §8) | H | https://techcrunch.com/2023/09/19/darrow-legal-tech |
| 17 | noyb (WeComply) | E | Austria (NOT VERIFIED on site) | 2021: automated draft complaints to 560 sites | adjacent | Precedent (passport §8) | H | https://noyb.eu/node/281 |
| 18 | Vakteye | F | Sweden | Policy claims vs observed behavior; evidence logs | direct | Directly does PD-MIS-01 | M | https://www.vakteye.com/en/insights/privacy-policy-contradictions-guide |
| 19 | WhoGetsMyData | F | Switzerland | Free: before/after consent, policy check, world map, signed evidence | partial | Closest free analog | M | https://whogetsmydata.com/ |
| 20 | SitePrivacyScore | F | NOT VERIFIED | Early access: policy vs behavior, transfer risk | partial | Crowding space | L | https://www.siteprivacyscore.com/ |
| 21 | Datascale — policy match | F | Germany | Tools on site but absent from policy; paid audits | partial | Price benchmark | M | https://datascale.de/en/resources/checks/privacy-policy-match/ |
| 22 | Ours Privacy — Web Scanner | F | NOT VERIFIED | Policy coverage per hostname (HIPAA) | partial | Vertical version | M | https://oursprivacy.com/blog/agentic-web-scanner-reads-your-privacy-policy |
| 23 | Academic: PoliCheck, PoliGraph, Libert "policyxray" | F | USA | Policy vs data-flow consistency | adjacent | Prior art | H | https://usenix.org/conference/usenixsecurity20/presentation/andow |
| 24 | EDPS Website Evidence Collector + EDPB Website Auditing Tool | B | EU | Open-source regulator tools | partial | B2G argument | H | https://edps.europa.eu/edps-inspection-software_en |

Free public baselines: Blacklight (The Markup / CalMatters, 18M+ scans) https://themarkup.org/blacklight ·
ImmuniWeb Website Privacy Test https://www.immuniweb.com/privacy/about/ · ComplyZero (India, DPDP; confidence L)
https://www.tribuneindia.com/news/business/96-of-indian-websites-collect-user-data-without-consent-reveals-largest-dpdp-compliance-study/

### Considered and excluded (and why)

| Name | Category | Why excluded |
|---|---|---|
| CookieYes, Cookie-Script, Termly, Osano, Ketch, Transcend, Complianz, CookieHub, CookieScan, Sourcepoint | A | Same CMP pattern as #2–#5 (Sourcepoint now part of Didomi). Price benchmarks only |
| Clarip | C | No distinct angle beyond #1/#11 |
| Zendata | C | "Policy-aware" claim too vague; G2 profile inactive >1 year |
| Jscrambler, Source Defense | D | Script security / PCI focus |
| Trackingplan | D | Analytics QA, not legal compliance |
| CyRisk, Guidewire Cyence | E | Cyber-insurance analytics |
| PrivacyScore, Webbkoll, WhoTracks.me, DuckDuckGo Tracker Radar, OpenWPM, CNIL tools | B | Research tools / data sources, not competitors |
| Pixeldefence, ToS;DR, PrivacySpy | F | Read policy text only |
| Coalition privacy controls | E | Insurer feature, policy presence only |
| Privacy Tools (Brazil), DPDP/LGPD plugins | G | Consent plugins only |
| Saudi PDPL / China PIPL / Turkey KVKK scanners | G | None found in one search each |

## Sources (Step 1A)

- https://www.privado.ai/solutions/web-privacy · https://cybersectools.com/tools/privado-web-auditor
- https://www.cookiebot.com/en/cookie-scanner/ · https://cookiebot.com/en/lgpd
- https://www.onetrust.com/products/cookie-compliance
- https://www.didomi.io/free-compliance-scan · https://www.didomi.io/blog/didomi-acquires-agnostik
- https://www.iubenda.com/pt-br/scan · https://trustarc.com/products/consent-consumer-rights/website-monitoring-manager/ · https://securiti.ai/privaci/cookie-consent-management/
- https://feroot.com/feroot-pagescanner/ · https://cside.com/blog/how-to-monitor-cross-border-data-transfer-on-your-website · https://www.reflectiz.com/gdpr/ · https://www.observepoint.com/solutions/web-privacy/
- https://www.lokker.com · https://www.helpnetsecurity.com/2024/02/14/lokker-web-privacy-solution/
- https://captaincompliance.com/education/privacy-risk-scanning-tools-comparison/
- https://webxray.ai/ · https://gizmodo.com/meet-webxray-a-search-engine-that-tells-you-how-youre-being-tracked-online-2000478699 · https://arxiv.org/pdf/1805.01187.pdf
- https://www.privaini.com/ · https://shiftingprivacyleft.buzzsprout.com/2059470/13304143
- https://techcrunch.com/2023/09/19/darrow-legal-tech · https://sacra.com/c/darrow
- https://noyb.eu/node/281 · https://edri.org/our-work/noyb-aims-to-end-cookie-banner-terror-and-issues-more-than-500-gdpr-complaint/
- https://www.vakteye.com/en/insights/privacy-policy-contradictions-guide · https://whogetsmydata.com/ · https://www.siteprivacyscore.com/
- https://datascale.de/en/resources/checks/privacy-policy-match/ · https://oursprivacy.com/blog/agentic-web-scanner-reads-your-privacy-policy
- https://usenix.org/conference/usenixsecurity20/presentation/andow · https://www.usenix.org/conference/usenixsecurity23/presentation/cui
- https://edps.europa.eu/edps-inspection-software_en · https://interoperable-europe.ec.europa.eu/collection/free-and-open-source-software/solution/website-evidence-collector · https://www.edpb.europa.eu/documents/support-pool-of-experts/edpb-website-auditing-tool_en
- https://themarkup.org/blacklight · https://calmatters.org/economy/technology/2026/02/blacklight-update-tiktok-x-twitter/ · https://www.immuniweb.com/privacy/about/
- https://www.tribuneindia.com/news/business/96-of-indian-websites-collect-user-data-without-consent-reveals-largest-dpdp-compliance-study/
