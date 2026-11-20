# Global competitor features v2: decisions on "What Probo should take"

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:00
- Based on passport version: 0.13 (decision D-025)
- Confidence: high for the decisions
- v1: `competitors-global-features.md`. Feature-ID decisions (F-17…F-25) are in `competitors-global-v2.md`.

## Decisions on "What Probo should take from the deep read" (v1 F·Take 1–10)

| # | Take | Decision | Reason |
|---|---|---|---|
| 1 | Consent phases in fresh browsers, zombie cookies | **Roadmap (category III, F-18)** | Clicking banners on non-clients' sites is out of our passive scope for now |
| 2 | Confidence grades + human review | **Partly:** every finding already says how sure we are by level and evidence; a review queue is roadmap | D-019 |
| 3 | Court-grade evidence (SHA-256, hash chain, Ed25519, /verify) | **Accepted, building 21.11 (F-19)** | — |
| 4 | Show both countries: company jurisdiction and server location | **Accepted** (data already has `country` and `company_country`; the report shows both) | Matches V-16 reading in `legal-27-1-2026.md` |
| 5 | Typing into forms without submitting | **Not for non-clients** (D-009); category III with consent | — |
| 6 | Uzbek ID detectors with validation (PINFL, passport, phone, card) | **Accepted, building 21.11** | Local data = our moat; fewer false positives |
| 7 | Publish our scoring rules | **Accepted:** rules are YAML in the repo; the README lists the penalties | already public in the repo |
| 8 | Scanner transparency (IPs, UA, opt-out, legal basis) | **Not now** for IPs and UA (team decision until 22.11); the legal basis is R-08 (Role 2) | — |
| 9 | Money exposure | **Conditional** (F-20, after V-05) | — |
| 10 | Measure dark patterns, don't guess | **Roadmap** (needs banner interaction) | — |

## Sources

- `research/competitors-global-features.md` (v1)
