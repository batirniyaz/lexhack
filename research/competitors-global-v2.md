# Global competitors v2: decisions on the proposals, and how we position Probo

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:00
- Based on passport version: 0.13 (decision D-025)
- Confidence: high for the decisions; facts about vendors are the research team's (v1), not re-checked by Role 1
- v1: `competitors-global.md` (27 tools) and `competitors-global-features.md` (deep cards; its v2 is a short note)

## Conclusions

1. **Positioning changes.** v1 shows that "policy vs behaviour", a country map, form destinations, consent tests and
   a 0–100 score exist in several global tools (WhoGetsMyData, Vakteye, Privaini, Ours Privacy and others). So
   passport F-01 "the main difference from all competitors" is too strong. **We say: "the first scanner for Uzbek
   law"** — never "the first in the world" (v1 G·C1 2, G·1A 3).
2. **Our real moat:** ZRU-547, art. 27¹ and the CMR 415 list in lawyer-editable YAML; policy quotes checked by code;
   Uzbek and Russian; a local service catalog; **scans run from an Uzbek IP** (our server's egress: Uzbektelekom,
   AS8193, checked 21.11). The Guardian test in `competitors-handson.md` shows why the vantage point matters.
3. **Jury sentence (from v1 G·HC, use as is):** none of the global tools studied mentions Uzbekistan; the closest
   paid ones are enterprise products (Privado starts at $600 per site per month, from its pricing page).

## Data

### Decisions on the proposed features

| ID | Proposal | Decision | Reason |
|---|---|---|---|
| F-17 | Policy coverage per service in 4 levels (named / company named / only the kind / not found) | **Accepted, building 21.11** | Sharper, more honest PD-POL-02; passive |
| F-18 | Three consent visits (no click / Reject / Accept) | **Roadmap, category III** | Needs clicking banners; detection of many CMPs; we keep precision first (D-019) |
| F-19 | Signed evidence pack (SHA-256, Ed25519, verify page) | **Accepted, building 21.11** | Evidence for lawyers; cheap |
| F-20 | Fine exposure in BCA per finding | **Accepted with a condition:** the mechanism is built, numbers appear only when Role 2 verifies V-05 | A wrong fine is worse than none |
| F-21 | Scan from an Uzbek IP | **Already true** (server in Tashkent; checked 21.11) | Put it in the report scope and the pitch |
| F-22 | Human review queue | **Roadmap** | Needs a reviewer and clients |
| F-23 | Publish scanner IPs and user agent | **Not now** | Passive scans keep a normal browser user agent until 22.11 (team decision); revisit for active mode |
| F-24 | Evidence export compatible with EDPS WEC / EDPB WAT | **Roadmap** | Interesting for the B2G pilot |
| F-25 | "Draft notice + fix guide + grace period" B2G mode (noyb model) | **Roadmap, use in the pitch** | A soft-enforcement story for the Ministry of Justice pilot |

### Claims not to use in the pitch

Everything v1 marks NOT VERIFIED, all vendor customer counts, funding figures and scan counts, and the Cookiebot
"adequate country" labels. Use only prices from vendors' own pricing pages (read 21.11) and the cited papers.

## Sources

- `research/competitors-global.md`, `research/competitors-global-features.md`, `research/competitors-handson.md` (v1)
