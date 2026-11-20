# Competitors — hands-on test of free scanners
- Author: Alii (GitHub Aliii2004) — research, R-04 competitors
- Date/time: 21.11.2026, 01:00–01:40 (Tashkent)
- Based on passport version: 0.10 (rechecked against 0.12 on 21.11: product renamed to Probo, D-022)
- Confidence: high for what each tool showed on this run; low for generalising (one site, one run per tool,
  free versions only).
- Test site: **theguardian.com** (international news site: consent banner, ad tech, forms, privacy policy). Not an
  Uzbek site on purpose — several of these tools publish results on public pages (D-003).

## Conclusions

1. **Same site, five working scanners, five different pictures.** Scores: SitePrivacyScore 100/100 (A), WhoGetsMyData
   73/100, Datascale 71/100, ImmuniWeb B+, Blacklight (no score) "scripts from PubMatic, OpenX and 8 other ad-tech
   companies". The main reason is **where the scanner stands**: from Frankfurt (WhoGetsMyData) the Guardian shows a
   Sourcepoint banner and sends no trackers before a choice; from California on a phone (Blacklight) it loads ad-tech
   scripts of 10 companies. → **A foreign tool sees a site the way a foreigner sees it. Probo must scan from an
   Uzbek IP (F-21) — this is a concrete, demonstrable reason why foreign scanners are not enough for Uzbekistan.**
2. **Static-HTML scanners are wrong in both directions.** Datascale (1.5 s, HTML only) raised a CRITICAL "no consent
   layer detected" — false, the site runs Sourcepoint. SitePrivacyScore's basic scan gave 100/100 with zero findings,
   while three other tools found Google Ad Manager and Comscore. → Confirms our D-016 (real browser) and D-019
   (precision over recall).
3. **Marketing ≠ what runs.** Datascale advertises an accept/reject "deep scan"; the result said "Consent simulation
   unavailable: no headless browser in the scan worker". Feroot's free scan timed out after 120 s. SitePrivacyScore
   advertises "200+ compliance signals" and found nothing.
4. **The only free tool that delivered depth is WhoGetsMyData**: banner test, recipients by company and jurisdiction,
   hosting and mail provider, policy check per service, signed evidence. Even it did not test "after Accept" on this
   site, and it maps nothing to law.
5. **Scores are unstable over time.** WhoGetsMyData scored the same site 60 on 13.11 and 73 on 20.11. → Our score
   must be explainable rule by rule and repeatable from saved facts (`facts.json` + `rescore`, D-015).
6. **Self-serve is rare at the top.** Of the 27, only 6 offer a free scan without an account or e-mail; Captain
   Compliance needs an account; Didomi, Cookiebot checker, iubenda and Privado need an e-mail; the rest are demo-only.

## Data

### What was run

| Tool | How | Ran? | Note |
|---|---|---|---|
| WhoGetsMyData | public API `POST /api/v1/scan` | yes (scan 232933, 20.11 20:01 UTC) | also read the earlier scan 190331 of 13.11 |
| ImmuniWeb Website Privacy Test | web form | yes (report JXawRUYn, 21.11 01:02 GMT+5) | per-section details load lazily, only the summary was read |
| Blacklight | web form | yes — **cached** result of 20.11 15:02 ET (default "use cached results") | defaults: iPhone, California |
| Datascale Tracking Check | web form | yes | 1.5 s scan |
| SitePrivacyScore | web form, "Basic Web Scan" | yes | full PDF report behind "Unlock" — not opened |
| Feroot pre-consent scan | web form | **failed** — "Scan timed out" (120 s) | |
| Captain Compliance | web form | **not run** — "Create account & scan" | no account created |
| Didomi, Cookiebot checker, iubenda, Privado free audit | — | not run | need an e-mail address |
| OneTrust, TrustArc, Securiti, Lokker, Privaini, Vakteye, c/side, Reflectiz, ObservePoint | — | not run | demo / sales only (or account) |

### Results side by side

| | WhoGetsMyData | ImmuniWeb | Blacklight | Datascale | SitePrivacyScore |
|---|---|---|---|---|---|
| Vantage point | browser in Frankfurt (EU), source from Switzerland | server IP in the US; tested `/international` | California, iPhone emulation; redirected to `/us` | not stated (static fetch) | not stated (static fetch) |
| Time | seconds via API (cached run of 20.11) | ~2–3 min | cached | 1.5 s | ~30 s |
| Score | **73/100** "Moderate" (60 on 13.11) | **B+** | none | **71/100** "Something here is broken" | **100/100, A**, "better than 100% of sites" |
| Consent banner | Sourcepoint found; no trackers before choice, none after Reject; after Accept **not tested** | not reported in summary | not tested | **CRITICAL: "No consent layer detected"** (false) | 0 findings |
| Trackers / ad tech | Google Ad Manager (−10), Comscore in a noscript fallback (−4), Braze; 11 cookies; 962 requests to other domains | 1 tracking pixel (scorecardresearch = Comscore); 0 third-party cookies; 0 external XHR | scripts of PubMatic, OpenX and 8 other ad-tech companies; 0 third-party cookies; no canvas, session recording, key logging, Meta/TikTok/X pixel | "No analytics tag found" (CRITICAL; the site uses its own analytics) | none |
| Pre-consent cookies | 7 cookies before choice | 7 first-party cookies, 6 without HttpOnly | — | "to review": gu_client_ab_tests, gu_v2_mvt_id, GU_mvt_id … | — |
| Privacy policy check | read (2,516 words): Google Ad Manager **named**, Comscore only as a category ("advertising"), Sourcepoint **not named** | privacy and cookie policy found | not checked by design | — | — |
| Where form data goes | forms on 5 pages analysed; key-logging test ran on 0 fields | **"1 web form submitting data to 1 external domain"** | key logging: none | — | — |
| Countries | recipients by jurisdiction: Google, Comscore, Sourcepoint, Fastly — US; Guardian — UK | server location US | — | — | — |
| Hosting / mail | Fastly CDN (US), DNS NS1, **mail Google Workspace** | server IP, bot-protection mechanisms (6) | — | — | — |
| Evidence | **SHA-256 + hash chain + Ed25519-signed zip**, verify URL | PDF report (not downloaded) | results archive (not downloaded), screenshots | 7-day share link | PDF behind "Unlock" |
| Law mapping | none | none ("as is") | none | none | none |

### Vendor claims checked

| Claim | Result on this run |
|---|---|
| Datascale: deep scan "answers the cookie banner once with accept and once with reject" | **Not run**: "Consent simulation unavailable: no headless browser in the scan worker" |
| SitePrivacyScore: "200+ compliance signals", results in ~30 s | Ran in ~30 s; **0 findings, 100/100**; the site itself says a basic scan "can miss up to 40% of hidden trackers" |
| Feroot: free pre-consent scan, 60 s target | **Timed out** at 120 s |
| ImmuniWeb: checks web forms | Yes — reported a form sending data to an external domain (summary level) |
| WhoGetsMyData: three-moment banner test, signed evidence | Before-choice and after-Reject ran; after-Accept not tested; evidence signed and verifiable |
| Blacklight: 9 tests, location choice | Results shown for all tests; location/device defaults (California, iPhone) changed what the site served |

## Feature ideas (passport §10 format)

- F-26 · **Two vantage points side by side**: scan from an Uzbek IP and from an EU/US IP and show the difference
  ("what Uzbek visitors get vs what Europeans get") · a vivid demo of why foreign tools miss Uzbek reality · M ·
  from this test (WhoGetsMyData vs Blacklight) · proposal · Final
- F-27 · **Repeatability statement in the report**: scan hash + "same facts → same score" (re-run `rescore`) · answers
  "why did the score change?" · S · from WhoGetsMyData's 60 → 73 drift · proposal · Final

## Questions for the team

- **Q10.** Should we run the Probo scanner on the same site (theguardian.com) for a head-to-head table in the
  pitch? Needs the backend set up on this machine (Playwright + geo databases, ~400 MB).
- **Q11.** Several free tools need an e-mail (Didomi, Cookiebot, iubenda, Privado). Should a team member with a work
  e-mail run them, so the paid-tier leaders are also tested?

## Limitations of this test

- One site, one run per tool, free versions only; paid products (OneTrust, Didomi ACM, Privado, Lokker, Vakteye …)
  were not tested.
- Blacklight returned a cached result (20.11); WhoGetsMyData returned its scan of 20.11 20:01 UTC.
- ImmuniWeb's per-section details, SitePrivacyScore's full report and the downloadable PDFs/archives were not opened.
- The Guardian is a UK site; behaviour differs by visitor country, which is itself the main finding.

## Sources

- https://whogetsmydata.com/api/v1/websites/theguardian.com (scans 190331 and 232933) · https://whogetsmydata.com/scan/232933
- https://www.immuniweb.com/privacy/www.theguardian.com/JXawRUYn/
- https://themarkup.org/blacklight?url=theguardian.com&device=mobile&location=us-ca&force=false
- https://datascale.de/en/resources/tracking-check/ (result for www.theguardian.com/europe)
- https://www.siteprivacyscore.com/scan/result?scanId=report-1795205026324-www-theguardian-com
- https://www.feroot.com/pre-consent-assessment/ (timed out)
- https://captaincompliance.com/solutions/cookie-scanner/ (account required)
