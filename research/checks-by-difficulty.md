# What Probo finds, from the easiest to the hardest — three groups for pricing

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 10:40
- Based on passport version: 0.14 (decision D-031)
- Confidence: **high** for what each check does and its status (read from the code, run on 8 real sites on 21.11);
  **low** for the cost figures (assumptions from `business-model.md` §5 and §7)
- For Role 3: set prices per group from this file. `business-model-v2.md` §1 maps the groups to its categories.

## Conclusions

1. **30 checks in total: 19 work today, 11 are roadmap.** Sorted by how hard they are for us to do, they fall into
   three groups:
   - **Easy (11):** what any visitor's browser receives, checked automatically in seconds, no AI.
   - **Medium (8):** deeper automatic analysis — page code, validated identifiers, documents read by AI with every quote
     checked by code, comparison with what the site does.
   - **Hard (11):** needs the client's written permission or access, or days of expert work. Not built yet.
2. **One scan collects the facts for every Easy and Medium check at once.** So a Medium audit always includes all Easy
   checks; the extra cost of Medium is mainly one AI reading of the documents.
3. **Hard has two very different halves:** checks that are automatic but allowed only with the client's permission
   (Hard-A), and checks that are mostly people's work (Hard-B). They probably need two price points.
4. **Difficulty is not the same as importance.** Two of the most serious signs (🔴) are Medium checks: personal data in
   URLs and "the policy contradicts what the site does". The column "Max level" shows importance.

## How the checks were ranked

In this order of weight: (1) what the client must give us; (2) the method — browser facts only / page code and
validation / AI reading plus comparison / people; (3) our cost and time per check; (4) the risk of a false finding and
how much work it takes to keep that risk low (D-019).

## Data

### 1. All checks, easiest first

Max level: 🔴 violation, 🟡 risk, ⚪ recommendation (levels from `rules/` by Role 2). Status on 21.11.2026.

| # | Group | Rule / ID | What we find (plain words) | How we find it | What the client gives | Max level | Status |
|---|---|---|---|---|---|---|---|
| 1 | Easy | SEC-01 | The site or its personal-data forms work without HTTPS | address and form targets | nothing | 🟡 | built |
| 2 | Easy | SEC-02 | Basic security headers are missing | response headers | nothing | ⚪ | built |
| 3 | Easy | PD-POL-01 | No privacy / personal-data policy on the site | links and document titles on the scanned pages | nothing | 🟡 | built |
| 4 | Easy | PD-TRK-01 | Trackers (analytics, ads) load on the first visit, before any consent | network requests before any click | nothing | 🟡 | built |
| 5 | Easy | PD-REC-01 | Session recording (Yandex Webvisor, Clarity, Hotjar) records what visitors type | scripts and requests | nothing | 🟡 | built |
| 6 | Easy | PD-LOC-02 | Trackers and AI services send visitor data to countries outside the CMR No. 415 list | server and company country of every host, checked against the 49-country list | nothing | 🟡 | built |
| 7 | Easy | PD-PII-01 | Forms ask for sensitive data: passport, PINFL, card number, photo | form fields | nothing | 🟡 | built |
| 8 | Easy | PD-CNS-01 | A form collects personal data with no visible consent or notice | form fields, checkbox and text near the button | nothing | 🟡 | built |
| 9 | Easy | PD-BIO-01 | The site asks for a selfie or camera access (biometrics must stay in Uzbekistan) | file inputs, camera permission requests | nothing | 🟡 | built |
| 10 | Easy | EC-03 | An online store has no Uzbek-language version (pilot) | page language, language links, Uzbek text | nothing | 🟡 | built |
| 11 | Easy | M3 / F-13 | Whose mail service and which SaaS the company uses (MX, SPF, certificate logs) | public DNS | nothing | info | roadmap |
| 12 | Medium | PD-LOC-01 | Where form data really goes: another domain, a Telegram bot, a CRM — and in which country | form targets + messenger / CRM calls found in the site's own code | nothing | 🟡 | built |
| 13 | Medium | PD-DB-01 | The site's code connects to a foreign cloud database or storage (Firebase, Supabase, S3) | reading the site's scripts (keys are never stored) | nothing | 🟡 | built |
| 14 | Medium | PD-LEAK-01 | Personal data leaks to third parties in URLs: e-mail, phone, PINFL, passport, Uzcard/Humo card | every request to other companies; formats validated (dates in PINFL, Luhn for cards) | nothing | 🔴 | built |
| 15 | Medium | PD-POL-02 | The policy misses what the law requires (arts. 22–23: operator, purposes, data, retention, recipients, transfers abroad, rights, contact) | AI reads the policy; every quote is checked against the text by code | nothing | 🟡 | built |
| 16 | Medium | F-17 (inside PD-POL-02) | For each service the site uses: does the policy name it — product / company only / only the kind / not named | policy text vs the services seen in traffic | nothing | 🟡 | built |
| 17 | Medium | EC-01 | An online store's offer does not name the seller, contacts or address (pilot) | offer and contact page text; evaluated only if the offer was read | nothing | 🟡 | built |
| 18 | Medium | EC-02 | No public offer / terms of sale, or nothing about returning goods (pilot) | documents found and read | nothing | 🟡 / ⚪ | built |
| 19 | Medium | PD-MIS-01 | The policy promises one thing and the site does another (e.g. "we don't share data" + 5 trackers) | AI extracts promises with verbatim quotes; code compares them with network facts; promises with exceptions are downgraded | nothing | 🔴 | built |
| 20 | Hard-A | F-18 | Does "Reject" in the cookie banner really stop the trackers? | three visits: no click / Reject / Accept | written permission (clicks on the site) | 🟡 | roadmap |
| 21 | Hard-A | M4 / F-11 | Who really receives what people type into forms | fake test data sent through the forms, searched for in all outgoing traffic | written permission, domain ownership proof | 🔴 | roadmap |
| 22 | Hard-A | M5 / F-14 | The same checks inside the personal account | a test account (or the client logs in in our browser) | test account | 🔴 | roadmap |
| 23 | Hard-A | M6 | Which API endpoints carry personal data, and to which countries | grouping the requests seen while using the site | route list or API spec, test account | 🟡 | roadmap |
| 24 | Hard-A | M14 | The KYC / selfie flow: where the photo goes, is consent asked first | a synthetic test image in a test environment | test environment | 🔴 | roadmap |
| 25 | Hard-A | M16 | Does the company answer a data-subject request (access, deletion) in time | a request from a test identity, reply time measured | consent to send the request | 🟡 | roadmap |
| 26 | Hard-B | M8 / F-09 | A mobile app: permissions, built-in SDKs, where its traffic goes | app package analysis + traffic in an emulator | store link or test build | 🔴 | roadmap |
| 27 | Hard-B | M9 / F-15 | Where data is actually stored: cloud regions, columns with personal data | read-only metadata access (never row values) | read-only cloud or schema access | 🔴 | roadmap |
| 28 | Hard-B | M15 | Automated decisions (scoring): does the person learn about it and can object (art. 24) | review of the flow and notices | test account, notice texts | 🟡 | roadmap |
| 29 | Hard-B | M7 | Record of processing: data, purposes, recipients, countries, retention — and the gaps | analyst works from documents and a questionnaire, checked against the scan | documents, interviews | 🟡 | roadmap |
| 30 | Hard-B | M13 | Launch check of a new app before it has users: screens, API spec, database schema, SDKs | analyst review + scans of the staging site | staging, specs, schema, test build | 🟡 | roadmap |

### 2. The three groups

| | Easy | Medium | Hard |
|---|---|---|---|
| Checks | 1–11 (10 built + DNS map roadmap) | 12–19 (all built) | 20–30 (all roadmap): Hard-A 20–25, Hard-B 26–30 |
| What the client gives | nothing — any public site | nothing — any public site | Hard-A: written permission, test account; Hard-B: documents, builds, read-only access |
| Method | browser facts only | page code, validated IDs, AI reading with quotes checked by code, comparison | Hard-A: automatic, only with permission (D-009); Hard-B: analyst and lawyer work |
| Time | 1–2 min per site (one scan) | + about 1 min for the AI reading | Hard-A: hours incl. setup; Hard-B: days |
| Our main cost (assumption, `business-model.md` §5, §7) | browser ≈ 0.0006 $ per page | + one AI reading ≈ 0.15–0.34 $ per policy | Hard-A: setup ≈ 1 analyst hour (131,548 UZS) + runs; Hard-B: 3 h to days of analyst time |
| Risk of a false finding | low: facts are directly visible | medium: needs validation and quote checks; PD-MIS-01 is the most delicate (a lawyer should look) | low for facts, but every result needs a person to interpret |
| `business-model-v2.md` category | I Express | II Full (includes all Easy checks) | III Active (Hard-A), IV Expert (Hard-B) |

### 3. Included in every report, not priced separately

Verbatim law text under each finding (lex.uz via lex-rag or Role 2's quotes) · possible consequences (Administrative
Code art. 46², where R-02 supports it) · data-flow world map · "the law changed → the status changed" on saved scans ·
evidence seal (scope, Uzbek vantage point, SHA-256, Ed25519 signature, `/verify`) · PDF and share link.

### 4. Not checks — services only through a partner

Fixed documents (policy, consent texts; M11) and a lawyer's review (M12) are legal consulting under CMR No. 675. Per
R-08 (`research/legal-our-risks.md`, conclusion 3) we sell them only through a partner legal-consulting firm or an
advocate, unless Probo hires a legal consultant and notifies the justice body first.

## Questions for the team

1. **Role 3:** price per group: Easy and Medium per audit (Medium includes Easy); Hard-A per check or per flow plus a
   one-off setup; Hard-B per project. Do we keep one price for "Hard" or two (A and B)?
2. **Role 3:** importance vs difficulty: should a Medium audit cost more because it can find 🔴 signs, or only because
   it costs us more (the AI step)?
3. **Role 2 (R-08, conclusion 2):** SEC-01, SEC-02 and PD-DB-01 details may count as vulnerability information
   (ZRU-764 art. 24). Their details must be hidden in public views of sites the user does not own (F-47, Role 1).

## Sources

- Code: `backend/qalqon/detectors/`, `backend/rules_draft/`, `rules/` (Role 2, 21.11), run on the batch
  `batch-20261120-231932` (8 sites)
- `research/service-catalog.md` (M1–M16), `research/business-model.md` (cost inputs), `research/business-model-v2.md`
- `research/legal-our-risks.md` (R-08), `research/legal-norms.md` (R-01), `research/legal-liability.md` (R-02)
