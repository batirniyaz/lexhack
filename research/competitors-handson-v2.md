# Hands-on scanner test v2: decisions

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:05
- Based on passport version: 0.13 (decision D-025)
- Confidence: high for the decisions
- v1: `competitors-handson.md`

## Conclusions

1. **The strongest pitch evidence in the research:** the same site looks different to scanners in different places
   (Frankfurt vs California), static-HTML scanners are wrong both ways, and scores drift without explanation. Probo
   answers all three: it scans from Uzbekistan, uses a real browser (D-016), and every score is re-computable from
   saved facts (`rescore`) and now carries a hash and a signature.

## Data

| ID | Proposal | Decision | Reason |
|---|---|---|---|
| F-26 | Two vantage points side by side (Uzbek IP vs EU/US IP) | **Roadmap** | Needs a second egress point; good future demo |
| F-27 | Repeatability statement (scan hash, "same facts → same score") | **Accepted, building 21.11** as part of the evidence block | — |
| Q10 | Run Probo on the same test site for a head-to-head table | **Accepted, optional:** Role 1 runs it during the morning batch if time allows; in public material call it "a large UK news site" | D-003 spirit |
| Q11 | Run tools that need an e-mail | **Not needed** | Enough evidence already |

## Sources

- `research/competitors-handson.md` (v1)
