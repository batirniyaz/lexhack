# Scope extension v2: decisions

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:10
- Based on passport version: 0.13 (decisions D-025, D-027)
- Confidence: high for the decisions
- v1: `scope-extension-proposal.md` (20.11)

## Conclusions

1. **The core stays the website scanner for the personal-data law** (D-002). We do not build "check every action
   against all Uzbek law", and we do not build a free-form legal chat.
2. **One narrow step beyond personal data is accepted: the e-commerce transparency pilot (D-027).** Three checks for
   online stores (seller identity, offer and return terms, an Uzbek version). It follows v1's own advice: a fixed list
   of regulated activities Role 2 can verify, not a chat.

## Data

| ID | Proposal | Decision | Reason |
|---|---|---|---|
| P-F3 | Legal engine on the lex.uz corpus | **Covered by lex-rag (D-013); now wired into reports** (21.11) | — |
| P-F4 | Product check for builders (questionnaire → norms) | **Roadmap, category IV (launch check M13)** | Needs Role 2's list of regulated activities; questionnaire answers can't be verified by code |
| P-F5 | Combined report: law vs claims vs behaviour | **Done in the narrow form:** "policy says vs site does" + verbatim law citations | — |
| P-F6 | Passive security checks (secrets in JS, PII in API responses, cookie flags, CORS) | **No** | D-008; PII in URLs is PD-LEAK-01 (now with Uzbek ID detectors) |
| P-F7 | Active security checks | **No** (withdrawn in v1) | D-008 |
| P-D6 | Widen D-002 | **Replaced by D-027** (one pilot, three checks) | — |

## Sources

- `research/scope-extension-proposal.md` (v1)
