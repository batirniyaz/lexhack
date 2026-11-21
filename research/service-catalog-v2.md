# Service catalog v2: decisions on v1, services grouped into four audit categories

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 03:50
- Based on passport version: 0.13 (decisions D-025, D-026)
- Confidence: high for the decisions (team decision of 21.11); the legal mapping of v1 stays as v1 wrote it
- v1: `service-catalog.md` (stays as the reference for article mapping, access design and world practice)

## Conclusions

1. **All 16 services of v1 stay in the catalog**, now grouped into **four audit categories** (Express, Full,
   Active, Expert) that also define the price (`business-model-v2.md`). Two categories are built; two are roadmap.
2. **Accepted now:** nothing that needs client access. The hackathon product is categories I and II.
3. **Not now:** sector packs, sector and size verification, engagement letters, signed agent traffic, live badge.
   They are correct designs for active services, but there is no active service and no client yet. They stay in
   v1 as the roadmap design.

## Data

### 1. Every service → category → status

| Service | Category | Status 21.11 | Note |
|---|---|---|---|
| M1 Website privacy scan | I Express | built (14 rules) | + Uzbek ID detectors, AI services in the catalog (21.11) |
| M2 Policy, "says vs does" | II Full | built | + per-service coverage in 4 levels (F-17), 21.11 |
| M3 DNS and mail map | I Express | not built | F-13, after the final |
| E-commerce transparency (pilot, new) | II Full | building 21.11 | seller identity, offer and return terms, Uzbek version (D-027) |
| Law citations from lex.uz (new) | II Full | done 21.11 | quotes in Role 2's rules |
| Signed evidence pack + scope + verify page (new; F-06, F-19, F-27) | II Full | building 21.11 | SHA-256 + Ed25519 |
| Fine range per finding (F-20) | II Full | mechanism 21.11, shown only after Role 2 verifies V-05 | never show an unverified fine |
| M10 Monitoring and alerts | platform (spends tokens) | partly: rescore; scheduler and Telegram not built | F-05 |
| Law-change re-check (F-16) | platform, free | building 21.11 (demo on saved scans) | W4 of the brief |
| M4 Canary form test | III Active | roadmap | D-009: clients only, written consent |
| Consent banner Accept / Reject runs (F-18) | III Active | roadmap | clicks on the client's site |
| M5 Logged-in area | III Active | roadmap | test accounts, F-14 |
| M6 API personal-data map | III Active | roadmap (crawler already records requests) | D-008 limits |
| M14 KYC / biometric flow | III Active | roadmap | synthetic images only (Role 2) |
| M16 Data-subject request test | III Active | roadmap | test identity only |
| M7 Record of processing | IV Expert | roadmap | lawyer confirms |
| M8 Mobile app check | IV Expert | roadmap (F-09) | legality of app analysis: Role 2 |
| M9 Inside scan | IV Expert | roadmap (F-15) | metadata only |
| M11 Fix documents | IV Expert | roadmap (F-04) | is it a licensed legal service? R-08 |
| M12 Lawyer review | IV Expert | partner, billed by the partner | — |
| M13 Launch check for new apps | IV Expert | roadmap | good story for IT Park; mention in the pitch as roadmap |
| M15 Automated-decision review | IV Expert | roadmap | — |

### 2. Decisions on the v1 feature proposals

| ID (v1) | Proposal | Decision | Reason |
|---|---|---|---|
| P-F33 | Sector picker and legal packs | **Not now** (roadmap) | In passive mode a sector changes almost nothing: ZRU-547 rules apply to every site. Packs matter when III–IV exist |
| P-F34 | Sector and size verification | **Not now** | Needed for quotes on active work; no active work yet |
| P-F35 | Scoped, hashed report + verification page | **Accepted, building now** | Cheap; makes the report usable as evidence; answers "why did the score change?" |
| P-F36 | Signed agent traffic (RFC 9421), published IPs | **Not now** | For active mode only. Passive scans keep a normal browser user agent until 22.11 (team decision) |
| P-F37 | Engagement letter generator | **Not now** | Paperwork for active services |
| P-F38 | Launch check (M13) | **Roadmap, category IV** | Strong story for IT Park; shown as roadmap |
| P-F39 | Live badge with automatic revocation | **Not now** | Needs monitoring and clients; TRUSTe lesson noted |
| P-F40 | Data-subject request test (M16) | **Roadmap, category III** | — |

## Questions for the team

1. **Role 2:** the e-commerce pilot needs verbatim norms (ZRU-792 "On electronic commerce", consumer protection law,
   state-language law). Role 2 confirms the articles on lex.uz.
2. Open questions 1–8 of v1 stay open; they matter when category III starts.

## Sources

- `research/service-catalog.md` (v1), `research/business-model-v2.md`, `research/role1-implementation-brief.md`
