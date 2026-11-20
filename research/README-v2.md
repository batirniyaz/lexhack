# Research v2: status after Role 1's review (21.11)

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:20
- Based on passport version: 0.13 (decisions D-025 … D-028)
- **Read this first.** Every research file now has a `-v2.md` partner with the decisions on its proposals:
  accepted, roadmap, or rejected, and why. v1 files are not changed.

## Conclusions

1. **Probo stays narrow:** a passive scanner for Uzbek personal-data law (+ one e-commerce pilot). New ideas go to
   the roadmap unless they work on any public URL, add no false findings, and fit before the final.
2. **Positioning:** "the first scanner for Uzbek law", not "the first in the world" — policy-vs-behaviour exists in
   global tools (`competitors-global-v2.md`). Our moat is Uzbek law in lawyer-editable YAML, verified quotes, UZ/RU,
   local catalog, scans from an Uzbek IP.
3. **Business model v2:** four audit categories, monthly tokens per category with a volume discount, one free
   partial audit after registration (`business-model-v2.md`).
4. **The weakest part now is legal, not features.** Legal is one third of the score. Before the checkpoint
   (21.11 14:00) the team's most valuable work is in the table below.

## Index

| v1 | v2 (decisions) | Main decision |
|---|---|---|
| `business-model.md` | `business-model-v2.md` | New public pricing: categories × tokens × volume discount; free partial audit |
| `service-catalog.md` | `service-catalog-v2.md` | M1–M16 grouped into 4 categories; sector packs not now |
| `role1-implementation-brief.md` | `role1-implementation-brief-v2.md` | W1, W2, W4, W9 accepted; W3, W5 rejected |
| `competitors-global.md` | `competitors-global-v2.md` | F-17, F-19 accepted; F-20 conditional; positioning changed |
| `competitors-global-features.md` | `competitors-global-features-v2.md` | Uzbek ID detectors, both countries, evidence accepted |
| `competitors.md` | `competitors-v2.md` | Pitch facts accepted; no e-mails to site owners |
| `competitors-handson.md` | `competitors-handson-v2.md` | Repeatability + vantage point go into the report |
| `market.md` | `market-v2.md` | Counts accepted; recompute TAM/SAM/SOM with v2 prices |
| `scope-extension-proposal.md` | `scope-extension-proposal-v2.md` | Only the e-commerce pilot goes beyond personal data |
| `architecture-proposal.md` | `architecture-proposal-v2.md` | What was adopted on 20.11 |
| `legal-27-1-2026.md` | `legal-27-1-2026-v2.md` | `rules/countries.yaml` in use; closed list read by code |

## What Role 1 builds on 21.11 (code freeze for the checkpoint ~11:30)

1. Law citations from lex.uz via lex-rag in every finding.
2. Evidence block: scope (pages, time, vantage point), SHA-256 hashes, Ed25519 signature, verify page.
3. AI services in the catalog; Uzbek ID detectors (PINFL, passport, phone, card); per-service policy coverage.
4. E-commerce transparency pilot (3 checks, `EC-*` rules).
5. "Law changed → status changed": saved scans re-checked under the old and the new art. 27¹.
6. Fine ranges: the mechanism; numbers only after Role 2 verifies them.

## What we ask from the team before 14:00 (in this order)

| # | Task | Who | Why |
|---|---|---|---|
| 1 | Verbatim quotes (uz + ru, edition date) for the 14 rules in `backend/rules_draft/`, or confirm the ones Role 1 pulls from lex-rag (they will appear in reports marked "not verified by a lawyer") | Role 2 | Legal criterion; every finding cites the law |
| 2 | R-08: is a passive scan of a public site legal; our disclaimer; our own policy for accounts | Role 2 | The jury will ask "is your scanning legal?" |
| 3 | V-05: fines for ZRU-547 violations (Administrative Code art. 46-2, Criminal Code art. 141-2), BCA value for 2026 | Role 2 | Fine ranges stay hidden until this is done |
| 4 | The old (pre-ZRU-1125) wording of art. 27¹, verbatim, with source | Role 2 / research | Law-change demo |
| 5 | Norms for the e-commerce pilot (ZRU-792, consumer protection, state language): which article requires seller details, offer, return terms, Uzbek version | Role 2 | Pilot rules |
| 6 | Pitch v1 with the competitor facts and the v2 prices; 3 interview calls if possible | Role 3 | Business criterion |
| 7 | Recompute TAM/SAM/SOM with v2 prices | Role 3 | Business criterion |

## Sources

- All files in `research/`; `PASSPORT.md` v0.13
