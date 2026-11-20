# Market v2: decisions and what to recompute

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:10
- Based on passport version: 0.13 (decisions D-025, D-026)
- Confidence: high for the decisions; the counts are v1's (sourced)
- v1: `market.md`

## Conclusions

1. **Counts are accepted for the pitch:** 182,338 active .uz domains (V-10 closed), 41–90k live sites (DNS proxy),
   660,392 organizations, 35 banks, 237 non-bank lenders, 115 e-commerce platforms, 21,292 organizations served by
   Ministry of Justice legal service centers (the organizer's own infographic — strong for the B2G story).
2. **TAM / SAM / SOM must be recomputed** with the v2 prices (`business-model-v2.md`): v1 used the formula prices.
   Also present TAM carefully: the base case multiplies **all** .uz domains by a full price, which a mentor can call
   inflated. Lead with SAM and the beachhead list (6,964 named regulated organizations).

## Data

| ID | Proposal | Decision | Reason |
|---|---|---|---|
| P-F20 | SAM calibrator from the batch scan | **Partly:** `/api/stats` already gives shares for the 8 reference sites; n = 8 is too small to replace the 50% assumption — say so if used | small sample |
| P-F21 | Sector tag per scanned domain | **Not now** | Tied to sector packs (rejected for now) |
| P-F22 | Private teaser report to site owners | **No** | Same as Q12 in `competitors-v2.md`: no unsolicited contact before R-08 |

## Task for Role 3

Recompute TAM / SAM / SOM with the v2 model. Suggested inputs: small sites buy 1 × II per month (250,000 UZS);
clinics and schools 1 × II + quarterly III later; mid-regulated 3 × II + 1 × III; banks by contract. Keep every share
an explicit assumption.

## Sources

- `research/market.md` (v1), `research/business-model-v2.md`
