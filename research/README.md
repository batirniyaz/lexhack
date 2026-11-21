# Research

- Based on passport version: 0.4

This folder holds the team's research. Code lives in `backend/`, `frontend/` and `demo-site/` (Role 1, batirniyaz). Rule files go to `rules/`, the pitch to `pitch/`. Per the git rules in `CLAUDE.md`, Role 2 writes `research/legal-*` and `rules/`, Role 3 writes the rest of `research/` and `pitch/`.

## Rules for every research file (from `PASSPORT.md` §0 and `CLAUDE.md`)

- Every fact needs a source URL. If no source is found, write **NOT VERIFIED**. Never invent numbers, article numbers, prices or company names.
- Laws come only from lex.uz: a verbatim quote, a link to the document and the edition date.
- Start each file with the header below and name the passport version it is based on.
- If something contradicts the passport, don't fix it silently: list it under "Questions for the team".

## Research tasks (passport §9.2)

| ID | Topic | Role | Output file | Status |
|---|---|---|---|---|
| R-01 | Personal data law (ZRU-547): articles on consent, purposes, cross-border transfer, localization (art. 27-1), registry, protection, subject rights; are IP and cookie IDs personal data (V-08) | 2 | `research/legal-norms.md` | to do |
| R-02 | Liability: Administrative and Criminal Code articles, fines in BCA (base calculation amount), BCA value for 2026, 2021 social-media restrictions and other practice | 2 | `research/legal-liability.md` | to do |
| R-03 | Rule catalog: one YAML per check in passport §5, schema §11.2 | 2 | `rules/*.yaml` | to do |
| R-04 | Competitors: global, regulator tools, Uzbekistan / Kazakhstan / Russia / CIS | 3 | `research/competitors.md` | to do |
| R-05 | Uzbek market: .uz domains, e-commerce, banks and microfinance, IT Park residents, TAM/SAM/SOM | 3 | `research/market.md` | to do |
| R-06 | Interview script (uz/ru), answer table, willingness to pay | 3 | `research/interviews.md` | to do |
| R-07 | Pitch: 3 min + 2 min demo + 2 min Q&A, uz/ru, 10 likely jury questions | 3 | `pitch/pitch-v1.md` | to do |
| R-08 | Our own legal risks: legality of scanning, storing results, publishing stats; report disclaimer; our policy and terms; does vulnerability checking need a license (V-15) | 2 | `research/legal-our-risks.md` | to do |
| R-09 | Cybersecurity Center (csec.uz) and the audit market: what they check, for whom, prices; private audit firms | 3 | `research/csec.md` | to do |
| R-10 | New art. 27-1 (ZRU-1125) and the 49-country list (CMR No. 415); how the recipient's country is determined (V-16) | 2 | `research/legal-27-1-2026.md` + `rules/countries.yaml` | to do |

## Already in this folder

| File | What it is |
|---|---|
| `architecture-proposal.md` | An alternative architecture written before passport v0.4. The team's architecture is `ARCHITECTURE.md` in the repo root (Role 1). Read it only as a list of suggestions; conflicts with v0.4 are listed at its top |
| `scope-extension-proposal.md` | Proposal: a structured product check for software builders on top of legal search. Conflicts with v0.4 are listed at its top |

## Header template (English version of passport §11.1)

```markdown
# <Title>
- Author: <name>, Role <N>
- Date/time: <DD.MM HH:MM>
- Based on passport version: <0.x>
- Confidence: high / medium / low

## Conclusions (3–5 points, most important first)
## Data (tables; every row has a source)
## Feature ideas (passport §10 format)
## Questions for the team / contradictions with the passport
## Sources (list of URLs)
```
