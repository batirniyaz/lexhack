# Rules (Role 2, R-03)

- Based on passport version: 0.13 · 21.11.2026
- A file here overrides `backend/rules_draft/<same ID>.yaml` (no code change). Detectors and `params` are the drafts'
  ones, unchanged. Backend tests: 51 passed, 1 skipped with these files (21.11.2026).
- `verified: true` = Role 2 checked the article choice and every quote against live lex.uz on 21.11.2026
  (ZRU-547 edition of 12.09.2026; MoJ model procedure No. 20-mh of 15.11.2023). `quote_uz` is lex.uz's Latin-script
  version of the official Uzbek text (https://lex.uz/docs/-4396419), `quote_ru` the lex.uz Russian translation.
  Interpretations are marked in each file's header comment.
- Reasoning: `research/legal-norms.md` (R-01), sanctions: `research/legal-liability.md` (R-02), localization:
  `research/legal-27-1-2026.md` (R-10).

| ID | Level | Changed vs draft | Main basis | Why this level |
|---|---|---|---|---|
| PD-LEAK-01 | 🔴 violation | — | arts. 28, 31 part 3, 23 part 2 | e-mail / phone seen in third-party requests; no ground fits analytics or ads |
| PD-MIS-01 | 🔴 violation | — | arts. 22, 12 part 2 | explicit promise contradicted (D-021) |
| PD-CNS-01 | 🟡 risk | **🔴 → 🟡** | arts. 18, 21, 23; model procedure item 9 | consent is one of seven grounds; a request before a contract or an accepted offer / terms is lawful; what we see is "no visible consent or notice" |
| PD-POL-01 | 🟡 risk | — | arts. 23, 22; model procedure item 30.12 | no norm requires a public policy; it is how the notice is usually given |
| PD-POL-02 | 🟡 risk | — | arts. 22, 23 | core = purposes and rights (art. 23) |
| PD-PII-01 | 🟡 risk | — | arts. 10, 19 | necessity depends on the service |
| PD-TRK-01 | 🟡 risk | — | arts. 4, 18 | V-08 (IP / cookie as PD) is an interpretation |
| PD-LOC-01 | 🟡 risk | — | arts. 27¹ part 3, 15; CMR 415 | bases abroad not visible; 🔴 only for 3 mandatory categories |
| PD-LOC-02 | 🟡 risk | — | arts. 15, 27¹, 4 | V-08 + bases not visible |
| PD-REC-01 | 🟡 risk | — | arts. 31 part 3, 10 | masking not always visible |
| PD-DB-01 | 🟡 risk | — | art. 27¹ parts 2–3 | data category in the cloud DB not visible |
| PD-BIO-01 | 🟡 risk | — | arts. 27¹ part 2, 26; model procedure item 1 | camera / photo seen, destination not |
| SEC-01 | 🟡 risk | — | art. 27; model procedure item 30.8 | no norm names HTTPS |
| SEC-02 | ⚪ recommendation | — | art. 27 (general) | good practice only |

Not created (no detector in the code yet): **PD-HOST-01** (site hosted abroad) and **PD-MAIL-01** (MX abroad) from
passport §5 — both would be 🟡 at most under art. 27¹ part 3 for ordinary data. E-commerce pilot rules `EC-01…03`
stay in `backend/rules_draft/` (`verified: false`) until Role 2 checks their norms (README-v2 task 5).
