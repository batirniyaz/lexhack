# Implementation brief v2: what Role 1 accepted, what not, and the build order

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 03:55
- Based on passport version: 0.13 (decision D-025)
- Confidence: high (decisions); build status is updated in `ARCHITECTURE.md` as each item lands
- v1: `role1-implementation-brief.md`

## Conclusions

1. **Accepted and building on 21.11 (in this order):** W2 law citations → W9-light evidence block (scope,
   hashes, Ed25519 signature, verify page) → W1 AI services (catalog only, no new rule) → Uzbek ID detectors →
   per-service policy coverage (F-17) → e-commerce pilot (D-027) → W4 law-change re-check (demo on saved scans) →
   fine mechanism (shown only after verification).
2. **Not accepted:** W3 AI legal review and W5 sector packs (reasons below). W6–W8 stay the design for when active
   mode and accounts exist.
3. **Code freeze for the checkpoint: 21.11 ~11:30.** What is not finished by then continues after the checkpoint
   without touching the demo path.

## Data

### 1. Work items

| Item | Decision | Reason | Notes |
|---|---|---|---|
| W1 AI providers (passive) | **Accepted, minimal** | Cheap and correct, but on our 8 reference sites **0** call an AI API or a chat widget from the browser (checked in the saved scans, 21.11). So: add entities with category `ai` to `entities.yaml`; they flow into the existing PD-LOC-02 and PD-POL-02. **No separate PD-AI-01 rule, not a pitch item.** Keys found in page code are never stored or reported (D-008) | answers brief question 2: we do not report exposed keys |
| W2 Law citations | **Done through Role 2's rules** | Verbatim quotes from live lex.uz in every rule; code shows them under each finding | — |
| W3 Project profile → legal search → AI legal review | **Rejected** | This is the free-form "AI lawyer" that D-002 ruled out: hard to verify, easy for mentors to break, and it moves the LLM towards deciding (D-010). Our narrow, verifiable extension beyond personal data is the e-commerce pilot (D-027) | brief question 1: the review never creates findings — moot |
| W4 Law-change re-check | **Accepted, narrow** | The best reason to pay monthly, and 2026 gives a real example (ZRU-1125 + CMR 415). Built as rule-set versions + `rescore` on saved facts, shown as "before / after" on the site page. **No RSS monitor and no LLM relevance step yet** | old wording of art. 27¹ needs Role 2 confirmation |
| W5 Sector packs | **Rejected for now** | In passive mode almost every ZRU-547 rule applies to every site; a sector picker would change nothing visible. Revisit with category III | see `service-catalog-v2.md` |
| W6 Evidence and credential firewall | **Partly done** | Public demo: HAR, facts and other users' scans are closed to visitors (D-003 fix, 21.11 02:03). Full redaction is needed before any active mode | — |
| W7 AI data-flow canaries | **Roadmap, category III** | D-009 | — |
| W8 Monitored sites and frequency | **Replaced** by tokens: monitoring = a schedule that spends tokens (`business-model-v2.md`) | — | — |
| W9 Scope, report hash, identifiable agent | **Scope + hashes + Ed25519 signature + verify page: accepted.** Identifiable agent: not now | Passive scans keep a normal browser user agent until 22.11 (team decision) | brief question 3 |

### 2. Answers to the brief's questions

1. D-010: no change — the LLM never creates scored findings.
2. D-008: exposed AI keys are not reported and not stored.
3. Unidentified passive crawler: team decision for the hackathon (until 22.11); R-08 (Role 2) still needs a written
   answer for the jury.
4. AI-provider countries stay `NOT VERIFIED` in `entities.yaml` until Role 2 checks them; DPF for the five big US
   companies is now confirmed (`legal-27-1-2026.md`, V-19).
5. lex.uz terms (V-17): open, Role 2.
6. Passport rows: added in v0.13.

## Sources

- `research/role1-implementation-brief.md` (v1); saved scans in `scans/` (AI-host check, 21.11)
