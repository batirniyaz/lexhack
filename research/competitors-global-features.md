# Competitors — global: deep feature analysis (27 tools)
- Author: Alii (GitHub Aliii2004) — research, R-04 competitors
- Date/time: 21.11.2026 ~02:00
- Based on passport version: 0.10 (rechecked against 0.12 on 21.11: product renamed to Probo, D-022)
- Companion to `research/competitors-global.md` (tables, prices, funding, matrix). This file answers "what exactly
  does each product do and how": every function found, how scanning works, what the report contains, workflow,
  laws, limitations.
- Sources: each vendor's own product pages, **documentation / help centers** (docs.privado.ai, help.observepoint.com,
  support.didomi.io, docs.onetrust.com, docs.cside.com, docs.oursprivacy.com, iubenda help, complyzero docs,
  WhoGetsMyData methodology, Blacklight methodology, GitHub READMEs), read 21.11.2026.
- Confidence: medium-high for *what vendors say*; **nothing here was tested hands-on**. "Vendor claim" = stated by the
  company only. Gaps per card are listed under "Limitations / gaps".

## Coverage and depth (honest)

| Depth | Tools | What was read |
|---|---|---|
| Deep (docs or methodology + product pages, 30–65 functions) | WhoGetsMyData, Vakteye, Lokker, Captain Compliance, Privado, c/side, Feroot, Reflectiz, Didomi, ObservePoint, Ours Privacy, OneTrust, Cookiebot, iubenda, SitePrivacyScore, Datascale, Blacklight, ImmuniWeb, ComplyZero | Help center / docs / methodology pages, pricing, sample reports where public |
| Medium (product pages only, no public docs) | Privaini, TrustArc, Securiti, webXray, Darrow, noyb/WeComply | Product and solution pages, FAQ |
| Shallow (sources blocked) | EDPS Website Evidence Collector, EDPB Website Auditing Tool | README/wiki did not render (JS-loaded); EDPS page HTTP 403 |

## What Probo should take from the deep read (mechanics, not slogans)

1. **Consent tested in separate phases, each in a fresh browser** — no choice / Reject / Accept / GPC (Lokker,
   Ours Privacy, Feroot, WhoGetsMyData), up to 6 phases incl. settings-panel toggles and IAB strings (Captain
   Compliance Radar), zombie-cookie respawn test (Vakteye). → F-18.
2. **Confidence grades + human review** — CERTAIN / FIRM / TENTATIVE / UNVERIFIED and an analyst queue for low-confidence
   findings (Vakteye). Fits D-019 and Role 2 exactly. → F-22.
3. **Evidence that survives a court** — per-scan record with SHA-256 of page source and policy text, hash chain,
   Ed25519 signature, public key and a /verify page (WhoGetsMyData, ComplyZero); PDF + HAR + screenshots + SHA-256
   (Captain Compliance); network log + session recording + integrity-checked zip (Vakteye). → F-19.
4. **Two different "countries"** — WhoGetsMyData keeps *jurisdiction = where the operating company is established*
   separate from *server country = IP registration*. This is exactly our open question V-16 (Telegram: UAE company vs
   server location). We should show both, like they do.
5. **Typing into forms without submitting** — Blacklight, WhoGetsMyData (made-up e-mail and phone, up to 5 fields,
   never submits, searches outgoing requests for plain / URL-encoded / Base64 / MD5 / SHA-1 / SHA-256 / SHA-512 forms)
   and Lokker ("injects synthetic PII into form fields") do it on any site. → team decision vs D-009 (Q8).
6. **National ID detectors with checksum validation** — ComplyZero's Ladon validates Aadhaar with the Verhoeff
   checksum, cards with Luhn, GSTIN, IBAN; Ours Privacy finds card numbers (Luhn) and 10 other categories in outgoing
   requests. → For us: PINFL, passport series, Uzbek phone formats, card numbers, with validation, in form fields
   (PD-PII-01) and in URLs/payloads (PD-LEAK-01).
7. **Published scoring rules** — WhoGetsMyData and ImmuniWeb publish every deduction (e.g. "trackers after Reject −12",
   "tracking pixel −20"). Answers the jury's "why −15?" (passport §5 score). → publish ours.
8. **Scanner transparency** — published IP ranges and user agent (ImmuniWeb, OneTrust, Vakteye, WhoGetsMyData), opt-out
   page and robots.txt respect (Vakteye, WhoGetsMyData), **the legal basis for scanning stated publicly** (Vakteye:
   GDPR Art. 6(1)(f) legitimate interest). → R-08 and F-23.
9. **Money exposure per finding** — Privaini models a fine/settlement range per finding and a total. → F-20 (in BCA once
   V-05/V-11 are closed).
10. **Dark patterns measured, not guessed** — Captain Compliance reports the measured size ratio of Accept vs Reject
    buttons (e.g. 108×38 px vs 54×24 px) and hidden / off-screen reject options.

---
## A. Closest to Probo (scan a live site + read the policy or map to law)

### 1. WhoGetsMyData (Switzerland) — free public scanner
**What / who:** free, no account; homepage + up to 3 linked pages → 0–100 score, recipients, policy check, signed evidence. For the public, researchers, site owners.
**Modules:** source scanner (v5.43.0, 18.11.2026) · real-browser test (Chromium/Playwright, Frankfurt) · policy check + "promises vs practice" · data & CO2 footprint · single-page check · service DB (3,319 services / 3,747 organisations) · signed evidence + /verify · rankings, statistics, open data, public API, browser extension, correction form.
**Functions:**
1. Homepage fetch, up to 5 redirects; headers, cookies, TLS; private networks blocked; retries www / HTTP/1.1.
2. robots.txt opt-out: a matching entry stops scans and deletes results.
3. Picks up to 3 linked pages by kind (contact, shop, booking, jobs, blog, about); never login/cart/checkout.
4. Extracts scripts, styles, images, iframes, forms, fonts, preconnects, inline code.
5. Script signature analysis (IDs, fingerprinting APIs) on a limited number of downloaded scripts.
6. Reads tag-manager containers (weight 0.6, may load conditionally).
7. Cookie capture: names, domains, lifetimes — values never stored.
8. Service identification (domains, signatures, cookie names, HTML markers); a cookie name alone never names a service.
9. Groups domains by operating organisation; unmatched = "unknown third party".
10. Hosting, CDN, DNS and e-mail provider from ASN, DNS, headers.
11. CNAME-cloaking detection (first-party subdomains aliasing trackers).
12. **Form analysis**: destination, method, encryption, field kinds; −5 per form sent over HTTP, −2 per form sent to an unidentified third party.
13. Fonts / iframes / embeds origin.
14. Privacy headers: Referrer-Policy, CSP, Permissions-Policy (Topics), HSTS, reporting endpoints, client hints.
15. GPC (gpc.json) and Google Consent Mode defaults.
16. Technology detection (319 CMS/shop systems).
17. AI-service marking (chatbots, voice agents, AI search), no score effect.
18. **Banner test**: homepage opened 3 times with an empty profile — no click / Reject + reload + scroll / Accept + reload + scroll.
19. Banner recognition: DuckDuckGo Autoconsent rules, else button text in 13 languages.
20. Verdicts: choice respected / tracking before choice / tracking after Reject / no reject option / tracking without banner / no tracking / not determined.
21. Ad trackers and third-party cookies at each of the three moments.
22. Cookie-syncing test (an ID of 8–120 chars reappearing at another company).
23. Canvas fingerprinting (at least 10 distinct chars or 2 colours on 16×16 px or more, read back).
24. Canvas-font fingerprinting (50+ fonts, 50+ measurements).
25. Audio fingerprinting.
26. Shown-only signals: WebGL, WebRTC local probe, battery, media devices.
27. API wrappers record which script called which browser function.
28. **Key-logging test**: types a made-up e-mail, a test phone number and text into up to 5 visible fields (never password, payment or code fields), never submits, watches 4 s for the entries in plain, URL-encoded, Base64, MD5, SHA-1 or SHA-256 form.
29. Address autocomplete and form validation shown separately, not counted as key logging.
30. Hashed contact details sent to Meta, Google, TikTok, Pinterest, Snapchat, X.
31. Session-recording detection.
32. Meta Pixel events and advanced-matching parameter names (never values).
33. Google remarketing detection.
34. Consent Mode "denied" pings still count as contacts (IP, browser and URL are still sent).
35. Bot protection: CAPTCHAs and bot managers shown, not scored; block pages get no score.
36. Privacy-policy locator (many languages, rel=privacy-policy, banner links, sitemap, parent-company domain).
37. Reads text PDFs and the cookie policy.
38. **Provider-naming check** per service: Named / Company named / Only the kind of service / Not found; also lists trackers the policy names but the scan did not see.
39. Policy content summary: date, laws, contact/DPO, legal bases, rights, complaint, cookies, transfers abroad and basis, retention, recipients; flags Privacy Shield / Safe Harbor / old directive.
40. **Promises vs practice**: first-person site-wide statements (no tracking, no cookies, no sharing, location, service, consent) compared with the scan; sentences with exceptions excluded; labels Contradicted / Worth a closer look / No contradiction.
41. AI mention check in the policy.
42. Data footprint of a first visit; CO2 estimate (Sustainable Web Design v4).
43. Score engine: 100 minus impact (10/7/4/2/1/0) × discovery multiplier; 34 category caps; fixed −50 when the domain belongs to an ad-tech company.
44. Banner score rules: trackers before choice −8, after Reject −12, fingerprinting −8, key logging −10; small bonuses for good headers.
45. Score bands: 90–100 Excellent, 75–89 Good, 50–74 Moderate, 25–49 Poor, 0–24 Critical.
46. Evidence levels (observed / detected / inferred / potential / unknown) and confidence.
47. **Jurisdiction = where the operating organisation is established; server country = IP registration** (kept separate).
48. Change detection vs previous scan; Atom feed of changes.
49. Single-page check (personal-looking URLs refused).
50. Sector classification (21 sectors, only on clear evidence).
51. Rankings (scans of 30 days or less; percentages only with 20+ sites); statistics (214,341 scans at reading time).
52. **Signed evidence record**: evidence.json (time, scanner version, IPs, headers, requests, cookie names, SHA-256 of page source and of policy text), hash-chained to the previous record, Ed25519-signed, public key published; checked in the browser at /verify or with OpenSSL.
53. Open data (CSV/JSON, CC BY 4.0); public JSON API with rate limits; extension-fed scan queue.
**How it scans:** own user agent; source read from Switzerland; browser test in Frankfurt (published IPs), empty profile, homepage only, Quad9 DNS. Stores no cookie values, no screenshots, nothing about who started a scan.
**Report:** summary, score with rule-by-rule breakdown, banner test (3 moments), tracking techniques, recipients by organisation and jurisdiction, forms, headers, hosting, policy, promises, history, evidence download.
**Laws:** none assessed ("not a legal assessment"); the policy check looks for mentions of GDPR, Swiss FADP, UK GDPR, CCPA.
**Limitations / gaps:** browser test on the homepage only; banners differ by country and device; server-side flows invisible; service database maintained by hand; small inconsistencies in the methodology (bonus "max 5" vs table sum 8).
**Pages read:** whogetsmydata.com/methodology (full), /methodology/changelog, /api, /statistics, /evidence, /verify.

### 2. Vakteye (Sweden) — compliance monitor (Essentials / Professional / Enterprise)
**What / who:** independent monitor of privacy, security and accessibility for EU organisations (DPOs, security leads, procurement). No list prices.
**Functions:**
1. DNS and CNAME-chain analysis for trackers cloaked behind first-party subdomains.
2. TLS: certificate, protocol, cipher, HSTS.
3. E-mail security: SPF, DKIM, DMARC, BIMI.
4. DNSSEC and CAA records.
5. Baseline cookie inventory before any choice; each cookie classified against 400,000+ tracker domains.
6. Banner detection and Reject click across 2,800+ CMPs; visual analysis for unusual banners; "no working reject path" is itself a finding.
7. Reject cookie diff.
8. **Zombie cookies**: clear all cookies, wait 3 s, re-check which respawn.
9. Network monitoring after Reject.
10. Accept flow in a separate clean browser; baseline vs Reject vs Accept → "consent theater" and "non-functional accept".
11. Undisclosed vendors (receive data after Accept but are not listed in the banner).
12. Google Consent Mode v2 pings sent after denial.
13. TCF v2.2 pre-ticked legitimate-interest toggles.
14. Per-vendor audit against the CMP's declared vendor list.
15. Consent tests on up to 10 pages.
16. Geo-aware scanning (mechanics not stated).
17. Fingerprinting (canvas, WebGL, AudioContext).
18. Session replay (Hotjar, FullStory, Clarity).
19. **Policy vs practice**: AI extracts policy claims, compares each with scan evidence, maps to GDPR Art. 5(1)(a), 13, 6(1)(a).
20. Policy completeness vs GDPR Art. 13 (legal basis, retention, recipients, rights, DPO contact).
21. **Form analysis for Art. 9 special-category data** (health, religion, ethnicity).
22. Data residency: US recipients without DPF certification or SCC/adequacy flagged.
23. Children's data collected without age verification.
24. Security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy, COOP/COEP).
25. Passive CVE and vulnerable-JS-library checks, exposed admin panels (no active probes).
26. Exposed services and subdomain takeover (no port scanning).
27. Hard-coded secrets in client JavaScript.
28. New subdomain discovery and risk ranking.
29. WCAG 2.1 AA checks with a fix suggestion per finding.
30. **Confidence grading**: CERTAIN (behavioural proof) / FIRM (several signals) / TENTATIVE (one pattern) / UNVERIFIED (not reproduced); severity shown separately.
31. **Human verification queue**: low-confidence findings shown as "awaiting verification", not as confirmed.
32. Reviewer-feedback learning (two or more confirmations before auto-adjusting).
33. **Forensic evidence package**: network recordings per phase, session replays, cookie snapshots, tamper-proof manifest with cryptographic check; downloadable.
34. Four report types: compliance report (15–40 pp), DPIA (20–35 pp), executive summary (3–5 pp), annual assessment (10–20 pp).
35. Monitoring (monthly / weekly / daily) with new-finding notifications.
36. Fix retest with history.
37. "Privacy Monitored" badge with a record number, valid 90 days, public verify page.
38. Scanner opt-out by verified e-mail link.
39. WAF allowlisting with RFC 9421 Ed25519-signed requests.
40. Staging scans via allowlisted EU egress IPs.
**How it scans:** browser from an EU data centre; published user agent and IPs; under 2 minutes typical; no logins, no form submissions, no port scans; the legal basis for scanning is stated publicly (GDPR Art. 6(1)(f)).
**Laws:** GDPR (Art. 5, 6, 7, 9, 13, 24, 30, 32, 35, 36, 44–49, 83), ePrivacy Art. 5(3), Swedish LEK, NIS2, Swedish cybersecurity act, European Accessibility Act, EDPB guidance, Schrems II / DPF. EU only.
**Limitations / gaps:** web only; no logins; no list prices; no blanket EU-only processing guarantee.
**Pages read:** vakteye.com/en/pricing, /en/faq, /audit, /en/about, /en/insights and 5 articles (scan internals, confidence system, report types, policy contradictions, how the scanner works).

### 3. Privaini (USA) — outside-in privacy risk intelligence
**What / who:** assessment from a company name and domain only; sold to insurers, brokers, law firms, M&A and risk advisors, enterprises.
**Functions:**
1. Outside-in assessment, no install, no credentials.
2. Corporate intelligence: locations, subsidiaries, microsites, digital footprint.
3. **Privacy policy and terms parsing; declared vs observed practice; undisclosed practices.**
4. Live tracker, pixel and consent-behaviour detection (100+ signals per assessment).
5. Statute mapping per finding ("90 countries + 20 US states"; list not public).
6. Jurisdiction-specific counts (example: "47 trackers → 12 violate LGPD").
7. Wrongful collection (CCPA/CPRA).
8. Consent flow failures (GDPR/ePrivacy): pre-checked, dark patterns, firing before rejection.
9. AI governance gaps (EU AI Act, state AI laws).
10. Video / wiretap exposure (VPPA, CIPA).
11. Biometrics (BIPA).
12. Children's data (COPPA).
13. Data sharing and sale (CCPA/CPRA).
14. Retention and deletion.
15. Litigation exposure signals (VPPA, BIPA, wiretapping).
16. **Exposure modelling**: litigation / regulatory / remediation / reputational range per finding, from settlements and fines.
17. Aggregate exposure (sample: "$18M – $58M" across 19 jurisdictions).
18. Risk score (e.g. HIGH).
19. Finding cards with ID, severity, statute, observation and a UTC timestamp to the second.
20. Phased remediation plan with exposure reduction per step.
21. Portfolio monitoring for insurers.
**Workflow:** demo → 5 of the buyer's own entities assessed before the contract → contract (about 3 weeks).
**Limitations / gaps:** scan mechanics (browser, pages, frequency, locations) not stated; sample report only on request; "validated in a UK ICO response" is a vendor claim. Read from product pages only (no public docs).
**Pages read:** privaini.com/how-it-works, /risk-intelligence, /platform-overview, /case-studies, /solutions, /what-we-find.

### 4. LOKKER (USA) — Privacy Edge, Guardian, Consent Validator, Privacy Extension, Partner API
**What / who:** simulated sessions, risk score and reason codes, plus in-browser enforcement; for privacy/legal teams, defence counsel, cyber insurers, agencies.
**Functions:**
1. Scheduled portfolio scans: headless browser replays user sessions and records requests, cookies, storage, payloads, initiator chains.
2. **Risk score 0–1000 (higher = worse)**, benchmarked against the S&P 500.
3. Letter grades A+ … E per category.
4. Cookies category (Secure flag, lifetime, first/third party, owner).
5. **Form Data category**: do form values reach third parties.
6. Session Replay category (several tools; use on unmasked form pages).
7. Trackers category.
8. Consent category (banner coverage per page, GPC read and honoured).
9. **Geo category**: countries where third-party requests resolve; restricted geographies (named: North Korea, Belarus, Russia, China).
10. Perimeter category: third-party domains registered within 30/60/90 days, SSL problems, HTTP, headers.
11. **Reason codes** with severity Critical/High/Medium/Low, mapped law (HIPAA, VPPA, CCPA, CPRA, GDPR) and step-by-step remediation (e.g. "Meta Pixel receiving PHI on a healthcare page", "No consent banner detected").
12. Context detection: healthcare pages evaluated against HIPAA; California traffic against CCPA/CPRA.
13. Critical alert banner when findings match patterns with documented litigation.
14. Cookie inventory (name, domain, max-age, Secure, SameSite, owner).
15. **Form data tracing: injects synthetic PII into form fields and records which third parties receive it.**
16. GPC testing (does traffic drop when GPC is on).
17. Domain intelligence enrichment.
18. Change monitoring, tag-container drift.
19. Constellation view (3D request graph) and Waterfall view (initiator tree).
20. Payload Explorer: query parameters, cookies, event data, POST keys per third party.
21. Every scan kept indefinitely; retrieval for a past date.
22. Daily or weekly digests (no push alerts).
23. Domain classification and Trusted/Blocked rules pushed to Guardian.
24. Consent Validator: no interaction / accept / reject / GPC; priorities P1 (should be blocked) / P2 / P3; detects the CMP (OneTrust, Cookiebot, Didomi, Usercentrics and others).
25. Guardian: one script intercepts scripts, pixels, fetch/XHR before they leave the browser; blocks by domain, bad actors, geographies, unknowns.
26. Guardian DLP detectors: card, US passport, SSN, first/last name, e-mail, phone, medical terms; decodes payloads; decision log.
27. Privacy Extension: GPC off/on side by side; exports workbook, HTML report, audit bundle.
28. Partner API: onboarding, scans, scores, reason codes, webhooks.
**Report:** Risk & Remediation PDF, GPC Compliance PDF, Payload Explorer and Digital Objects (Excel), Consent Validator PDF (~15 pp) and Excel, portfolio roll-ups.
**Laws:** CIPA, CCPA/CPRA, VPPA, HIPAA (+ HHS OCR tracking guidance), Washington MHMDA, New York HIPA, BIPA, GDPR, UK GDPR.
**Limitations / gaps:** "technical observations, not legal conclusions"; no pricing; docs.lokker.com did not resolve; scan origin not stated.
**Pages read:** lokker.com/llms-full.txt (full), /products/privacy-edge, /guardian, /consent-validator, /privacy-extension, /partner-api.

### 5. Captain Compliance (USA) — Radar engine, Patrol, Cookie Scanner, CMP suite
**What / who:** scan engine plus scheduled audits with statute-mapped, hash-verified reports, plus CMP, notices, DSAR; for privacy/legal teams and law firms.
**Functions:**
1. Browser consent-journey scan: cookies, pixels, SDKs, session replay, chat, third-party requests.
2. **Six isolated phases, each in a fresh browser context**: pre-consent · accept all · reject all · GPC · settings-panel toggles · IAB (TCF v2, GPP, Consent Mode).
3. Reject test (sample: "7 still firing", with vendor names).
4. GPC test.
5. Settings-panel test, category by category.
6. IAB / GPP / Consent Mode strings validated against behaviour.
7. Pre-consent itemisation of every script, pixel, cookie.
8. **Dark patterns measured**: rendered size, colour and contrast of Accept vs Reject (sample: 108×38 px vs 54×24 px).
9. Hidden reject (behind a click, off-screen, styled as plain text).
10. Pre-checked toggles.
11. Re-prompt after Reject.
12. Calls to data brokers before consent (LiveRamp, Acxiom, Meta) as possible CCPA "sale" evidence.
13. Geo-disparity: scans from several regions.
14. Grade letter + score out of 100.
15. **Per-state verdict PASS / FAIL / AT RISK with statute citation** (20+ US states).
16. Tracker classification with vendor, purpose, retention, risk.
17. ML classifier for unknown banners and trackers.
18. Patrol: daily / weekly / monthly audits; new trackers, vendor script drift.
19. Findings mapped to statutes, labelled Strong / Informational.
20. **Hash-verified records: PDF with SHA-256, screenshots (1440×900), HAR, capture time, region, duration.**
21. Free audit scope incl. VPPA video players, Meta/TikTok pixels, session replay, chat.
22. CMP with geo rules, IAB TCF, Consent Mode v2, signed consent receipts; hosted dynamic cookie policy and notices; DSAR portal; assessments; data mapping; Trust Center.
23. "Compliance Shield": contractual legal-cost cover on eligible plans (not insurance).
**Pricing:** Free (1 domain, 50 scans); Professional $499 (period not stated); Enterprise on quote.
**Laws:** GDPR, ePrivacy 5(3), CCPA/CPRA (§1798.100, §1798.135), LGPD, CIPA, VPPA, 20 US state laws named.
**Limitations / gaps:** "documents observed behaviour; does not establish legal compliance"; sample is a logged-out desktop scan; Patrol price unclear.
**Pages read:** captaincompliance.com/platform/patrol (incl. sample report), /platform/radar, /platform, /pricing, /ai-information, /solutions/cookie-scanner, /free-privacy-audit.

### 6. Privado.ai (USA) — Web Auditor, App Auditor, data maps, AI assessments, DSR, open-source CLI
**What / who:** privacy-automation SaaS for privacy, legal and engineering teams. Web Auditor from $600 per website/month (annual, min. 4 sites).
**Functions:**
1. Consent-action simulation per banner and location: accept / reject / no action.
2. **Location-specific rule evaluation** (user picks simulated locations, e.g. Netherlands, Germany, California, UK).
3. GPC testing.
4. Third-party cookie, pixel and script inventory (name, category, lifespan).
5. "Cookie agent" re-checks each cookie's category by researching it online.
6. **Data-flow map**: personal data elements (user ID, e-mail, card number, location) → recipients (Meta, Stripe, TikTok), per consent state; cross-border flags.
7. Sensitive-data leak detection regardless of consent (example: precise location to TikTok).
8. Banner and compliance-link visibility per location.
9. Dark-pattern flags.
10. 30–50 preset checks (pages disagree): CCPA, CIPA, VPPA, GDPR, IAB TCF, PIPEDA, GPC, PIPL.
11. Journeys before and after login.
12. Multi-page scans (default 100 pages per Test).
13. Staging scans before release.
14. "Tests" (since 2.11.2026): geography + policies + page types, each with its own schedule and results.
15. Page types by URL pattern, sitemap or page element.
16. **Compliance score** = share of applicable policies passing in every test.
17. Pages tab with failure reasons.
18. Real-time risk alerts.
19. Auto-generated Jira/Linear tickets.
20. Alerts on each new third party or data element.
21. App Auditor: iOS IPA, Android APK/AAB or store URL; journeys pre/post login.
22. SDK and permission inventory; which consent action triggers which SDK.
23. Pre-fills Apple Privacy Manifest and Google Data Safety.
24. Code scanning via source-code management.
25. SaaS scanning via API (CRM, HRIS, CDP, ESP …).
26. Data-element inventory with Low/Medium/High sensitivity (110+ types).
27. Third-party inventory with flows and purposes.
28. RoPA automation.
29. Assessment agent reads PRDs, Jira tickets, specs, contracts → prefilled PIA/DPIA/RoPA with citations.
30. Contract agent.
31. Wren agent: intake, triage, research, drafting, approval routing, risk tracking.
32. DSR intake, workflows, dashboard (processing integrations "coming soon").
33. Sync to OneTrust and TrustArc.
34. Open-source Privado CLI: local code scan → privado.json with source-to-sink data flows; YAML policy-as-code.
**Report:** compliance % per regulation, alert counts per law, issue objects with timestamps, cookie and data-flow tables, exports (format not stated). Screenshots/HAR/hashes: not stated.
**Limitations / gaps:** scan locations, IPs, bot handling not stated; check count inconsistent; 4-site minimum.
**Pages read:** privado.ai home, /pricing, /products (web-auditor, app-auditor, wren, dynamic-data-maps, agentic-assessments, dsr-automation), /solutions (web-privacy, consent-monitoring), help.privado.ai Tests article, docs.privado.ai (CLI).

## B. "Where does the data go" — browser and script monitoring

### 7. c/side (USA) — Script Security, PCI Shield, Privacy Watch, CSP Builder, Fingerprint
**What / who:** one JavaScript tag in the client's own site watches third-party scripts in every real visitor session; PCI DSS 6.4.3/11.6.1 evidence; device fingerprinting. Free → Business $99/mo → Enterprise.
**Functions:**
1. In-session script monitoring via a `client.js` tag (vendor: every session, no sampling).
2. cside fetches third-party scripts on its own servers for analysis.
3. Per-page script inventory: vendor, category, last seen, Approved/Pending.
4. AI-written business justification per script.
5. Vendor approval and per-vendor permissions.
6. Payload change detection vs the last approved version (hash match).
7. Roll a changed script back to a previous safe hash.
8. Payload history (7 / 30 / 90 days by plan).
9. Dependency graph: which script loaded which.
10. Threat rulesets: obfuscation, redirectors, keyloggers, crypto miners, fake checkout overlays, code reading payment fields.
11. Ad-injection detection.
12. Threat-list matching (URLs, domains, IPs, GTM containers).
13. Vulnerable-library matching (OSV, RetireJS).
14. Review of unapproved outbound hosts.
15. Security-header monitoring on checkout paths (12-hour windows).
16. PCI 6.4.3 / 11.6.1 dashboard and weekly PCI report (PDF, e-mail, webhook, S3).
17. Script blocking by domain, URL, IP; CSP-based blocking; CSP Builder (report-only first, then enforce).
18. **Privacy Watch: what data each script accesses and where it sends it; cookie access and injection.**
19. Scripts firing before consent or outside approved categories; GPC and opt-out checks.
20. **Cross-border tracking: shows when data leaves the EEA**; dashboard map of cross-border flows; claims geo-restriction or rerouting.
21. Claims to prevent extraction of cookies and form data to unexpected endpoints (mechanism not described).
22. Separate GDPR, CCPA/CPRA and HIPAA dashboards.
23. Notification rules (13 trigger types; immediate / hourly / daily / weekly); Jira, Linear, Zapier, Slack, webhooks, S3.
24. Optional external "Scan Method" crawler (Enterprise; "very limited coverage").
25. Fingerprint product: device ID, bot and AI-agent detection, VPN/proxy, JA4, IP enrichment, account-takeover signals; chargeback evidence (CB911).
**Report:** dashboards, weekly PCI PDF, payload logs, version history, timestamps. Screenshots/HAR: not stated.
**Laws:** PCI DSS 4.0.1, GDPR, CCPA/CPRA, other US state laws, HIPAA.
**Limitations / gaps:** must be installed on the client's site (cannot audit a site that is not a client); method for destination countries not stated; Privacy Watch screens are UI mock-ups; docs contradict pricing on Free blocking.
**Pages read:** cside.com home, /pricing, /use-cases/compliance/gdpr, /solutions/pci-shield, /solutions/privacy-watch, /changelog, docs.cside.com (quickstart, adding-your-domain, notification-endpoints), Help Net Security 21.01.2026.

### 8. Feroot Security (Canada) — DXComply, PaymentGuard, DXSecure, free scanners
**What / who:** browser-layer consent, PCI and script security; agentless discovery plus optional script tag. Plans Assess (≤10 domains) / Govern (≤20) / Enterprise (≤5,000); no public prices.
**Functions:**
1. Free pre-consent scan: URL + region (US, UK, EU) → scripts, cookies, vendors, data assets, framework status (GDPR, CCPA/CPRA, HIPAA, PIPEDA, LGPD).
2. **Four consent states**: Default, Accept All, Reject All, GPC; per vendor: allowed / did not load / loaded before consent / not honoured.
3. Consent-choice analysis vs observed vendor behaviour.
4. Geographic consent rules (opt-in, opt-out, do-not-sell by jurisdiction).
5. Script, cookie, tracker, vendor inventory with load chains.
6. **Data-flow mapping "independent of where a vendor is registered".**
7. Pre-consent activity, post-rejection tracking, mislabelled cookies.
8. Drift detection across repeated audits.
9. Risk score High/Medium/Low by materiality.
10. Same audit evaluated against several regulations without rescanning.
11. Automated compliance reports, AI attestation, "historical proof of compliance".
12. Dated evidence with session recordings and reasoning logs per finding.
13. Mobile-app audit without SDK.
14. AI agents test every page, screen and consent state.
15. Vendor inventory and third-party data-access monitoring.
16. Alerts to SIEM, SOAR, ticketing.
17. Free GDPR Art. 30 RoPA generator from a URL.
18. Free browser extension: trackers on the current page, sensitive fields touched (geolocation, login, password, card), export to Excel/JSON.
19. PaymentGuard: payment-page script inventory, authorisation record and justification, integrity checks, change detection (hourly–weekly), QSA evidence export, runtime policy.
20. DXSecure: blocks skimming, formjacking, malicious injection; exfiltration prevention; **request and data-transfer analysis flags transfers to unexpected regions**.
21. Dashboard: policy issues, trackers, scripts, transfers, **"Unauthorized Countries"**, world map of transfers by country and hostname.
**Laws:** GDPR, CCPA/CPRA, HIPAA, CIPA, LGPD, PIPEDA, Quebec Law 25, PDPA, POPIA, Australian Privacy Act, UK DPA, GLBA, COPPA; PCI DSS, DORA, NIST, OWASP ("70+").
**Limitations / gaps:** no public prices; free scans may be blocked or time out; method for destination countries not stated; some plan contradictions.
**Pages read:** feroot.com home, /pricing, /dxcomply, /pci-paymentguard, /dxsecure, /platform-overview, /checkout-scanner, /pre-consent-assessment, /generate-ropa-for-website, /gdpr-website-compliance-solution, PageScanner page.

### 9. Reflectiz (Israel) — Security Hub, Privacy Hub, Offensive Hub, PCI Module
**What / who:** agentless (remote) web-exposure platform: own browser crawls the site from outside; quote-only pricing; Privacy Hub ≤10 or ≤50 sites.
**Functions:**
1. Remote discovery crawl incl. authenticated, checkout and pre-production pages.
2. Behavioural execution analysis: scripts, iframes, tags, pixels, cookies, headers, JS execution, network requests.
3. Reputation cross-check of components.
4. WHO / WHAT / WHERE: which third parties, risky behaviour (keylogging, tracking, PII harvesting), where they send data.
5. Prioritised alerts with mitigation steps.
6. AI auto-approvals, AI chat and de-obfuscation.
7. REST API, SIEM/SOAR, Jira, Slack, OneTrust.
8. On-demand blocking via CSP meta header (requires a tag); one-click unblock.
9. Privacy Hub: inventory of applications, domains, trackers.
10. **Data-flow mapping: which inputs each tracker touches and where data goes, incl. fourth parties.**
11. Unauthorised form-field access (trackers and AI SDKs reading PII, PHI, payment fields).
12. **Consent states**: Accept All, Reject All, Functional, Performance, Targeting, GPC.
13. Consent violations: before consent, after Reject, ignored GPC, misclassified cookies.
14. Shadow IT and tag-manager bypass; vendor change detection.
15. Root cause via initiator chains.
16. Smart baselining and policies.
17. AI remediation assistant.
18. **Consent Dashboard: banner config vs live behaviour; trackers missing from the banner; cross-border transfers.**
19. HIPAA Dashboard.
20. Peer-benchmarked privacy rating.
21. **Cookie classification vs published privacy policy.**
22. Offensive Hub: agentic pentesting (out of our scope, D-008).
23. PCI 6.4.3/11.6.1 module; Exposure Rating A–F with improvement simulator.
**Laws:** GDPR, CCPA/CPRA, Texas TDPSA, VCDPA, CTDPA, CPA, BIPA, HIPAA, PIPEDA, GPC; PCI DSS, DORA.
**Limitations / gaps:** no prices; destination-country method not stated; rating weighting not disclosed.
**Pages read:** reflectiz.com home, /plans, /platform/how-it-works, /platform/blocking, /platform/exposure-rating, /privacy-hub, /use-cases/pci-compliance, /gdpr.

## C. Consent-monitoring and CMP vendors

### 10. Didomi (France) — Advanced Compliance Monitoring (ACM), Compliance Report, free scan
**What / who:** scans what runs before consent, after refusal and with no action, against the declared banner and notice; for privacy/legal/DPO and marketing teams.
**Functions:**
1. Basic Compliance Report: bot session capped at **20 pages**, accept-all scenario only.
2. **Didomi Rating 0–4 stars** (from a 0–100 score): trackers/vendors despite refusal, CMP present, privacy policy present, security protocols.
3. Tracker typing: cookie, pixel, local storage; party set by who dropped it.
4. Tracker table (10 fields incl. initiator, lifetime, value, scenario), CSV.
5. Vendor identification against Didomi's database; unknown vendors flagged; IAB / Google ATP / custom.
6. Vendor vs initiator views and chaining graph.
7. **Vendor Trust Index 0–1**: 60% IAB declaration, **30% CNIL country-risk dataset**, 10% category vigilance.
8. ~12 rule-based recommendations, incl. privacy policy not reachable from every page, no CMP, no opt-out, cookies over 13 months, **trackers from non-GDPR-adequate countries**, unknown vendors, choices not honoured, no cookie policy.
9. Tag heuristics (response type, size, query params, domain).
10. ACM multi-scenario scans: Accept / Refuse / No action per property.
11. Compliance issues list (trackers in Refuse and No-action).
12. Custom interaction sequences via API (e.g. reject on a second layer).
13. Logged-in scans.
14. Custom user agent for allowlisting.
15. Daily / weekly / monthly frequency.
16. Weekly e-mail alerts.
17. Analytics over time; time-stamped history.
18. CMP Vendor Sync into the Didomi notice.
19. Collection diagnostics: unreachable, anti-bot, no CMP, no refuse option, click failed.
20. Daily CSV export to S3/SFTP (raw trackers, vendors, status) incl. TCF string consistency flag.
21. Privacy and cookie policy presence checks.
22. Free scan (work e-mail): fired before consent, after refusal, declared in the notice or not.
**Laws:** GDPR, CCPA/CPRA, VCDPA, CTDPA, CPA, Quebec Law 25, US state laws, Chile, Australia, Canada, Nordics; TCF, GPP, GPC, DMA, Consent Mode v2.
**Limitations / gaps:** vendor: "a tool for guidance, not a compliance validator"; false positives/negatives; fails on captchas; export CSV only; no prices.
**Pages read:** didomi.io/advanced-compliance-monitoring, /free-compliance-scan, /offers, support.didomi.io (8 articles: features, report, multi-scenario, vendor trust index, alerts, data export, allowlisting), developers.didomi.io.

### 11. ObservePoint (USA) — Audits, Journeys, Standards, Cookie & Tag Database
**What / who:** cloud web-governance platform; synthetic audits and journeys; priced by pages scanned.
**Functions:**
1. Cloud synthetic audits (no code on site).
2. Crawl scope: default 100 pages, up to 10,000; sitemap, robots, include/exclude regex.
3. Concurrency 1–50 browsers.
4. **Selectable scan location** (default Oregon, US).
5. User agent, viewport, custom headers.
6. Tag blocking during audit; file substitution.
7. Pre-audit actions: login, language/country cookies, CMP Accept All / Reject All.
8. Opted-In / Opted-Out / GPC audits per property and geography (e.g. 10 domains × 3 countries × 3 scenarios = 90 audits).
9. GPC header toggle; block third-party cookies.
10. On-page actions: clicks, form submissions, downloads; "ClickAll+".
11. Journeys: login, forms, cart, checkout, step by step.
12. **Consent categories = approved lists of cookies, tags, request domains and geolocations**; anything else flagged.
13. OneTrust category import.
14. Cookies Privacy Compliance report (approved/unapproved, origin, pages).
15. Cookie initiators and "Origin Story".
16. Privacy Tags report; approve tag account IDs.
17. Tag initiators; rogue and piggybacking tags.
18. Tag & Variable rules (e.g. CMP present on every page).
19. Alerts by e-mail or Slack.
20. Consent Mode v2 validation (gcs/gcd values).
21. **PII regex detection** (e-mail, phone, SSN, licence, address, medical codes, card) in URLs, tag variables, requests.
22. Authenticated audits.
23. Cookie & Tag Database with vendor, purpose, risk.
24. CMP validation; mobile via proxy and HAR analyser.
25. REST API, MCP server; free 50-page sample audit.
**Report:** Cookies / Tags / **Domains & Geo Privacy Compliance**, page details, initiators; rule pass/fail; history.
**Laws:** GDPR, CCPA/CPRA, CIPA, ePrivacy; rules "for any regional privacy laws".
**Limitations / gaps:** journeys cannot use consent categories; PII regex false positives; no prices.
**Pages read:** observepoint.com (home, platform, web-privacy, consent-management, pricing, sample-audit, cookie-and-tag-database), help.observepoint.com (implementation guide, PII detection, piggybacking, Consent Mode v2, cookies report, consent categories, creating audits, GPC).

### 12. Ours Privacy (USA) — Web Scanner, CMP, HIPAA CDP
**What / who:** healthcare marketing data platform with a web scanner and CMP; "200+ healthcare organisations"; custom pricing.
**Functions:**
1. Crawl from homepage and sitemaps within the domain tree.
2. Third-party script and stylesheet inventory by vendor and risk.
3. Keyword scan inside third-party JS/CSS (ad IDs, trackers, storage, PHI terms).
4. Cookies and localStorage by controller and category.
5. CSP capture and gap analysis per host.
6. WCAG 2.1/2.2 audit with score.
7. **"Data observed"**: inspects query strings, bodies and paths of third-party requests (decodes one Base64 layer) for 11 categories — e-mail, phone, SSN, card (Luhn), date of birth, IP, medical record no., health plan ID, diagnosis, medication, condition; shows field, never the value.
8. **Four consent states** on the homepage: before choice, Reject all, Accept all, GPC.
9. Scheduling daily/weekly/monthly; change notices (e-mail, in-app, Slack).
10. Uncovered-vendor flag; suppression rules with reasons.
11. Verify a single page after a fix; URL coverage tab.
12. Authenticated scanning; WAF allowlisting guide.
13. **AI policy alignment (beta)**: reads the policy per host, lists disclosure gaps and destination mismatches with the quoted passage and a fix.
14. Results via assistant, MCP and REST API; PDF export.
15. CMP: banner modes, opt-in/opt-out per region, region overrides, script blocking (automatic/manual), Monitor vs Enforce, consent log with version, subject export.
16. CDP: data-sharing report per destination (raw/hashed/redacted), governance rules, PII hashing, PHI stripping, bot scoring.
**Laws:** HIPAA (+ HHS OCR), US state laws, GDPR, CCPA, Quebec Law 25, PIPEDA, WCAG.
**Limitations / gaps:** consent check on homepage only; pattern detection has misses; policy alignment is beta; does not fill forms.
**Pages read:** oursprivacy.com (home, product, web-scanner, CMP, pricing, integrations), docs.oursprivacy.com (11 pages on scanner, consent, compliance report).

### 13. SitePrivacyScore — 15 free tools + full audit (early access)
**What / who:** free single-URL tools and a free (early-access) browser audit with a PDF "fix report".
**Functions:**
1. Security headers checker. 2. Cookie scanner (initial response only). 3. Consent banner validator (first pass). 4. Tracker detector (static HTML; ad / analytics / session replay). 5. Session-replay detector. 6. Privacy policy generator (Markdown template). 7. **Privacy policy analyzer**: parses the policy, maps homepage connections, flags transfers to Meta/Google/TikTok not named in the policy and vague retention. 8. CCPA/CPRA checker. 9. **Data Transfer Risk Scanner**: "Critical" = user data to a non-adequate country, "High" = processor without SCCs, "Moderate" = vendor not named in the policy (method for countries not stated). 10. robots.txt generator. 11. CSP generator. 12. Referrer-policy checker. 13. Third-party requests analyzer. 14. PII leak checker (e-mails in URLs). 15. GDPR quick check. 16. Full browser audit with score 0–100 + letter grade, regulatory impact text, fix steps with code.
**Limitations / gaps:** free tools run no JavaScript; full-audit internals undocumented; monitoring, history, API "coming soon"; operator not identified.
**Pages read:** siteprivacyscore.com home, /tools and all 15 tool pages, /about, /learn, /sample-report.

### 14. Datascale (Germany) — free Tracking Check (39 checks) + Audit Sprint
**What / who:** consultancy's free check (GA4/GTM/Consent Mode) as a lead tool for paid audits (€1,490 / €2,900 net).
**Functions (6 modules, 39 checks):** C01 Consent Mode V2 (CMP detection for 11 platforms, consent activates measurement, V2 parameters, Basic vs Advanced mode, update signal, TCF/GPP) · C02 Cookies & scripts before/after consent (third-party cookies, Borlabs config decoding, CMP group mapping, accept/reject simulation, pre-consent cookies and scripts, privacy policy found, **policy match: tools never mentioned in the policy**, reject respected) · C03 Tracking core (Ads conversion tag, server-side APIs, dataLayer, duplicate IDs, server-side tracking, architecture, analytics tag for 12 tools, tag manager) · C04 Product & price data (currency, price consistency, JSON-LD, view_item) · C05 Script inventory & performance (Privacy Sandbox, sync scripts, third-party count thresholds 11/21, payload 100/200 KB) · C06 Security & bots (AI-crawler rules, headers, HTTPS, JSON-LD, llms.txt, meta tags, robots.txt). Shareable permalink kept 7 days in the EU.
**Limitations / gaps:** up to 3 pages; marketing-analytics focus; "early warning, not a certificate"; legal assessment left to counsel.
**Pages read:** datascale.de/en/resources/tracking-check, /en/resources/checks (all 39), /en/.

## D. Large CMP / privacy-platform vendors

### 15. OneTrust (USA) — Cookie Consent + Compliance Assistant
**What / who:** enterprise CMP and privacy suite; "14,000+ customers"; no public prices.
**Functions:**
1. Scanner = Google Chrome VM that clicks from page to page and records cookies, tags, forms, storage, initiators, services.
2. Scope by domain / subdomain / path; include, exclude, prioritise; sitemap input.
3. Smart Scope 1,000 pages; recommended 2,000–3,000; maximum 15,000; typical scan 6–24 hours.
4. Query-parameter filter; scans behind login; waits up to 60 s per page for delayed cookies.
5. **Selectable scanner location** (default northern Europe); published IPs and user agent.
6. Scheduled scans (months); status pipeline; scan health checks.
7. Cookie categorisation via Cookiepedia (Strictly necessary / Performance / Functionality / Targeting / Unknown).
8. Cookie attributes (host, expiry, Secure, HttpOnly, session) with page list.
9. Tags incl. web beacons, grouped by domain; initiator chains 2 levels up/down.
10. **Forms detection: fields classified Personal (name, e-mail, password) or Non-personal.**
11. Pages tab: flags pages with forms, privacy policy, cookie policy, login.
12. Local/session storage.
13. **Services tab: vendor, category, vendor location, privacy-policy URL.**
14. Added/removed since last scan; audit log; Excel export; archives as JSON (kept 3 years).
15. Compliance Assistant: daily scans, 12 months of results, **Compliance Score**, scans from the regulated region (UK from London, EU from Amsterdam), violation checks (banner, cookie logic, "policy gaps", pixels after opt-out, dark patterns, Consent Mode timing, GPC, TCF/GPP), remediation card per violation.
16. Banner templates per law incl. India DPDPA; geolocation rules; auto-blocking; A/B tests; consent dashboards and receipts; 250+ languages; APIs, SDKs, MCP server.
**Laws:** GDPR, UK GDPR, CCPA/CPRA, LGPD, Quebec Law 25, VPPA, CIPA, US state laws, India DPDPA; DataGuidance content "300+ jurisdictions".
**Limitations / gaps (vendor-stated):** **scanner performs no user actions** (no accept, no reject, no form submit); **does not support single-page applications**; scans can take days; no evidence pack described.
**Pages read:** onetrust.com/products/cookie-compliance, Compliance Assistant blog, docs.onetrust.com (scanning a website, viewing and exporting results, consent audit, banners), developer.onetrust.com.

### 16. Usercentrics Cookiebot (Denmark) — CMP + scanner
**What / who:** CMP for SMBs and agencies; per-domain pricing by page count (€0–90/month); Usercentrics Advanced for enterprises.
**Functions:**
1. Patented scan: simulated, fully rendered browser sessions ("7–8 simulated users on average"), scroll, click links/menus/buttons, play media; monitors all traffic to third parties.
2. Per tracker: properties, type, expiry, **exact location in source code**, provider, purpose.
3. Covers HTTP/JS cookies, local storage, IndexedDB, Flash/Silverlight storage, pixels.
4. Purpose classification by a research team (repository size stated inconsistently).
5. Monthly scans (daily +€99/mo); on-demand scans; monthly change e-mail.
6. Billing tier by highest page count seen.
7. Automatic blocking (Premium); cookie declaration generator.
8. Banner layouts, custom code, branding; explicit/implicit consent; geotargeting; 47+ languages.
9. Consent log per consent: anonymised ID, categories, URL, **IP-based country of the visitor**, timestamp (12 months); CSV export.
10. Consent analytics; configuration health checker; cross-domain consent.
11. Consent Mode v2, Microsoft UET/Clarity, Amazon, GPC, IAB TCF.
12. Privacy-policy generator (Premium).
13. Developer API (consent object, events, server-side reading).
14. Free cookie checker: report e-mailed in under 2 minutes.
**Correction for our earlier file:** the deep read found **no statement on Cookiebot's own pages** that the scan report shows each cookie's destination country as adequate / not adequate; the support articles that may say so returned HTTP 403. Treat as NOT VERIFIED.
**Laws:** GDPR, ePrivacy, CCPA/CPRA, VCDPA, LGPD, POPIA, UK GDPR, DMA, IAB TCF.
**Pages read:** cookiebot.com (home, cookie-scanner, pricing, cookie-consent-solution, cookie-checker, developer); support.cookiebot.com HTTP 403.

### 17. iubenda (Italy, team.blue) — Cookie Solution, scanner, Consent Database, generators, Compliance Monitor
**What / who:** compliance SaaS for small businesses and agencies; €4.99–79.99 per site/month.
**Functions:**
1. Free compliance scan: URL + your location + users' location + site type → checks privacy policy, cookie policy, banner, T&C against applicable laws; e-mailed report; leads into a setup wizard.
2. Cookie/pixel/tracker scanner (monthly; hourly on Ultimate); alerts on new services.
3. Prior blocking; banner configurator by territory and regulation, with warnings when settings break a law.
4. Banner styling, per-country copy, preview by device and language; remote configuration.
5. Geo-targeting; pageview metering (€0.05 per 1,000 extra).
6. Consent log; consent recovery; analytics; consent paywall.
7. Consent Mode v2; IAB TCF.
8. **Self-updating privacy and cookie policy generator** (2,400+ clauses; documents updated when laws change).
9. T&C generator (translation into 15 languages).
10. Consent Database (records from forms, API, webhooks to HubSpot/Mailchimp; €5 per 1,000 consents).
11. Records of processing (Art. 30), whistleblowing tool, data-subject-rights form.
12. **Compliance Monitor (enterprise): crawler, risk dashboard, visual map of vendors by country, issues by severity, alerts, CSV/XLS export, API.**
13. Plugins (WordPress, Shopify, Joomla, PrestaShop, Magento), MCP connector.
**Languages:** documents "up to 27 languages"; Uzbek and Russian **not confirmed**.
**Laws:** GDPR, UK GDPR, ePrivacy, US state laws, LGPD, Swiss FADP, EU Whistleblower Directive.
**Limitations / gaps:** scanner method, pages per scan and locations not stated.
**Pages read:** iubenda.com/en (cookie-solution, scan, pricing, consent-database, help: banner configuration, Compliance Monitor).

### 18. TrustArc (USA, Main Capital since 10.2025) — Website Monitoring Manager, Cookie Consent Manager, Data Mapping, Assessments
**What / who:** enterprise privacy suite; no public prices.
**Functions:**
1. Deep scans incl. subpages and pages behind login and HTML forms; unlimited, frequent scans.
2. First-party, third-party and "piggybacking" tracker discovery.
3. **Resource-chain (daisy-chain) analysis**: which first-party script loads which tracker.
4. Auto-categorisation (required / functional / advertising).
5. Tracker risk score: proprietary Privacy Sensitivity Index (scale not stated).
6. Pre-consent and post-rejection firing detection.
7. Service provider vs third party (CCPA).
8. Tracker performance impact (downstream requests, load time).
9. Change alerts; reporting dashboards; sync to Google Sheets, Salesforce.
10. AI assistant "Arc" for scans and recategorisation.
11. Geo-aware banner, auto-blocking, consent logs, GPC/TCF/GPP/Consent Mode, mobile SDK, WCAG 2.2.
12. Data inventory and **data-flow map with cross-border transfers**; risk scoring "based on 130+ laws"; Art. 30 reports.
13. Assessments (PIA, DPIA, TIA, vendor, AI) with AI-suggested answers; DPF / APEC CBPR support.
**Laws:** GDPR, ePrivacy, UK PECR, CCPA/CPRA and 7 other US states, PIPEDA, Quebec Law 25, COPPA, PIPL, India DPDPA, LGPD, Mexico LFPDPPP, EU AI Act ("100+ jurisdictions").
**Limitations / gaps:** product pages only — scanning method, report formats and languages not stated.
**Pages read:** trustarc.com (website-monitoring-manager, cookie-consent-manager, international-data-transfers, data-mapping-risk-manager, assessment-manager).

### 19. Securiti (USA, Veeam since 12.2025) — Privacy Center, Consent Management, Consent Agent
**What / who:** consent part of a large data-security platform; Privacy Center Business $599/month (5 domains), Enterprise custom.
**Functions:**
1. Scan of "all pages" → automatic categorisation with a cookie-intelligence DB → banner and cookie policy generated.
2. Auto-blocking (zero-code on Enterprise); GPC and vendor opt-outs.
3. Geo-adaptive banner by reverse IP; banner language from browser.
4. Preference centre; consent records; dashboards; consent lookup by ID.
5. Auto-updating privacy notices from scan results; notice builder (8 languages: EN, PT, IT, ES, DE, JA, FR, AR — **no Russian or Uzbek**).
6. Scheduled and CI/CD-triggered scans; private scans behind login (Enterprise).
7. Google-certified CMP, IAB TCF; mobile app consent.
8. **Consent Agent**: checks banner presence, pre-consent tracking, preference enforcement, Consent Mode, TC strings, GPC, dark patterns, accessibility, disclosure completeness; ranks issues by severity and confidence; deploys approved fixes.
9. Hosting region EU or US; DSR intake and data mapping (adjacent).
**Laws:** GDPR, CCPA/CPRA, LGPD, ePrivacy, PIPEDA, PIPL ("+ more").
**Limitations / gaps:** product pages only — scan method and report contents not stated.
**Pages read:** securiti.ai (cookie-consent-management, consent-management-platform, privacy-center/pricing, privacy-center/third-party-tracking-consent, Consent Agent brief).

## E. Legal outcome: litigation, complaints

### 20. webXray (USA) — Litigation, Defense, Enterprise, Adtech & CMP
**What / who:** web-tracking evidence platform for plaintiff and defence firms, enterprises, ad-tech vendors. Demo-only pricing.
**Functions:**
1. Violation search over ~1.2M sites in regulated sectors (filter by tags, e.g. ad cookies without consent).
2. Consent-bypass analysis.
3. **Forensic website preservation** (every page, transfer and line of code, indexed) before filing.
4. Expert assistance and testimony ("Daubert standard").
5. Enterprise full-site scans via sitemap/URL list, slow "polite" crawling.
6. Quarterly scan of the global top million homepages.
7. **Scans from residential locations in the EU, California and the US with real browsers.**
8. Privacy search engine; forensic export of payloads, stored values, full traffic.
9. GPC journey replays; CMP integration audits at scale; disclosure-to-behaviour mapping; risk prioritisation.
10. Defence: scan client properties, validate privacy tools, fact-check complaints, evidence export.
**Laws:** CCPA, GPC; others not named. **Limitations / gaps:** no docs or methodology public; outputs described as "data, not a dashboard"; no prices.
**Pages read:** webxray.ai home, /litigation, /defense, /enterprise, /adtech.

### 21. Darrow (USA / Israel) — legal exposure intelligence
**What / who:** AI finds litigation opportunities in public data for plaintiff firms, funders, insurers. Not a site scanner — a precedent for the business model.
**Functions:** AI case detection over 50+ exposure categories · dual legal review · damages and settlement modelling · defensibility review · case-fit matching · case pipeline with estimated value · conflict check and claim · portfolio dashboard · case memos and evidence · AI Q&A on merits and precedent · plaintiff intake · negotiation intelligence · valuation memo with scenarios · insurer risk profiles and claim benchmarks · privacy exposure detection (example: CIPA pen-register claim).
**Data:** regulatory filings, incident reports, litigation patterns, public data; "5M+ signals per month" (vendor claim).
**Pages read:** darrow.ai home, /platform, /law-firms, /insurance, /research, /faq, /domain-coverage, /predictive-underwriting.

### 22. noyb + WeComply (Austria, non-profit) — cookie-banner campaign
**What / who:** NGO mass-scanning popular EU sites, generating GDPR complaints, giving owners a free fix channel.
**Functions:**
1. Mass scanning (target "up to 10,000 most visited sites in Europe").
2. Detection of unlawful banners; violations grouped into lettered types; "more than fifteen common abuses".
3. Checks named: no reject on first layer (81% of the 2021 wave), deceptive colours (73%), hard withdrawal (90%), reject hidden in sub-menus.
4. Repeated scans before and after the visit; site selection by jurisdiction, traffic, CMP used, violations.
5. **Automatic draft-complaint generation**, reviewed by the legal team; a person re-checks the technical analysis.
6. Evidence: HTML, data flows, configuration files, cookie data, screenshots.
7. Draft complaint + CMP-specific fix guide (OneTrust, TrustArc, Cookiebot, Usercentrics, Didomi, Quantcast …) sent by e-mail.
8. **Grace period** (60 days per FAQ; "one month" in 2021 text).
9. WeComply portal: case login, download, "report error", "report full compliance"; noyb verifies.
10. If not fixed: formal complaint to the DPA (GDPR Art. 77/80); "all or nothing".
11. Random re-scans later; public case register with outcomes (Won, Partly Won, Withdrawn (Complied), Pending).
**Languages:** platform EN, DE, ES, FR, EL, IT, PL. **Laws:** GDPR, ePrivacy.
**Limitations / gaps:** detection method and full violation list not public; banners only.
**Pages read:** noyb.eu/node/281, /en/project/cookie-banners, wecomply.noyb.eu and its FAQ.

## F. Regulator tools, public baselines, national-law analog

### 23. EDPS Website Evidence Collector (EU) — open source (EUPL-1.2)
**What is known:** "automates the website evidence collection of storage and transfer of personal data"; repository on code.europa.eu (1,547 commits, 34 releases, created 06.2024); results importable into the EDPB tool; Blacklight's tests were partly inspired by it.
**Gaps:** README did not render (JavaScript-loaded), GitHub archive 404, EDPS page HTTP 403 → **functions, outputs and options NOT VERIFIED**. Needs a manual read in a browser.

### 24. EDPB Website Auditing Tool (EU) — open source (EUPL-1.2)
**What is known:** for legal and technical auditors at DPAs and for controllers; audit preparation → visit → tracker evaluation against knowledge databases (several, each with source and "trust level") → final audit report; full-page screenshots; import/export of analyses; imports EDPS WEC results; EN/FR/DE/IT/ES.
**Gaps:** wiki and docs folder did not render → method and report format NOT VERIFIED.

### 25. Blacklight (The Markup, USA) — free inspector, collector open source (GPL-3.0)
**Functions:**
1. Third-party cookies (Set-Cookie and document.cookie; owner via DuckDuckGo Tracker Radar).
2. Ad trackers (EasyList/EasyPrivacy + Tracker Radar "Ad Motivated Tracking").
3. **Key logging**: types values into every input, never submits, searches requests for plain, Base64, MD5, SHA-256, SHA-512 forms.
4. Session recording (Princeton list).
5. Canvas fingerprinting (OpenWPM thresholds: ≥16 px, ≥10 characters, toDataURL / getImageData).
6. Meta pixel (standard, custom events, advanced matching); Google remarketing; X pixel and TikTok pixel (added 06.02.2026).
7. Script attribution via instrumented browser APIs.
8. Homepage + one random deeper page; location (Ohio, California, Europe) and device options; 24-hour cache.
9. Benchmark label vs Tranco top 100,000.
10. Collector options: tests, crawl depth, HAR and screenshot capture, timeouts, headers, device emulation; batch CLI "Blacklight Query".
**Output:** cookies JSON, inspection log, inspection.json (start/end time), HTML and JPEG per page, requests.har.
**Limits:** "does not check… privacy policies"; no law mapping; results are "an initial automated inspection".
**Pages read:** themarkup.org/blacklight and the 2020 methodology article (updated 2026), GitHub blacklight-collector and blacklight-query.

### 26. ImmuniWeb Website Privacy Test (Switzerland) — free test + premium
**Functions and published scoring:** privacy policy present +10 · reachable over HTTP −50 · HTTP without redirect −40 · third-party cookies without a banner −25 · third-party cookie living >3 months −5 each · tracking pixel −20 each · tracker in Local Storage −20 · XHR to third party −2 per host · **form data sent to a third party −2 per host** · third-party iframe −2 · third-party resource −1 per type · grades A+ … F · PDF report · weekly monitoring of 3 sites free · API · **published scanner IP ranges**.
**Pricing:** free 10 tests/month (20 with account); Premium €25 (50 tests) … €499 (2,500 tests) per month.
**Limits:** method, pages and retention not stated; GDPR only named.
**Pages read:** immuniweb.com/privacy, /about, /limits, /api, /monitoring, /scoring.

### 27. ComplyZero (India) — DPDP governance suite
**What / who:** one national law (DPDP Act 2023), data stored in India, for Indian SMBs; ₹9,000/month and up.
**Functions:**
1. Free cookie scan (homepage, first visit, real browser): cookies, local/session storage, IndexedDB; flags "set before consent".
2. Heuristic cookie categorisation; paid scans up to 3,000 pages.
3. Banner that holds trackers until consent; purposes; notice builder; install check.
4. Consent records (write-once, versions, exportable for the Data Protection Board).
5. Consent Hub: QR, kiosk, staff tablet, paper, app — notices in several Indian languages.
6. Requests (rights) with deadlines; registers (data, processing, vendors, retention); breach desk; trust centre.
7. **Readiness score out of 80** (+20 after a paid audit), 6 weighted areas, PDF report.
8. **Sealed evidence: Ed25519-signed exports, SHA-256 per record, free verifier.**
9. **Ladon PII discovery in connected systems: 34 categories incl. Aadhaar (Verhoeff checksum), PAN, GSTIN, UPI, card (Luhn), passport, voter ID; digits read in nine Indian scripts.**
10. Isolated parsing, read-only DB connectors, AES-256-GCM, masked findings.
**Research:** "State of Cookie Compliance in India 2026" — 6,000+ sites, headless Chromium, first page load only: 4.1% show a banner; 2 of 1,154 government sites.
**Limits:** governance suite, not a behaviour scanner (no flow/country analysis); free scan homepage only; Readiness "not a legal certificate".
**Pages read:** complyzero.com (home, governance-suite, pricing, security, ladon, docs: readiness, cookies, seal check, website), research page.

## Sources
All page URLs are listed under "Pages read" in each card; all were read on 21.11.2026.
