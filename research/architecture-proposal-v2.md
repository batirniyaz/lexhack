# Architecture proposal v2: what was adopted

- Author: batirniyaz, Role 1 (with Claude Code)
- Date/time: 21.11 04:15
- Based on passport version: 0.13
- Confidence: high
- v1: `architecture-proposal.md` (20.11). The team's architecture is the root `ARCHITECTURE.md`.

## Data

| Proposal (v1) | Decision | Where it is |
|---|---|---|
| Scan in a separate process (Playwright vs uvicorn on Windows) | **Adopted** (D-015) | `jobs.py` runs `python -m qalqon.scan --events` |
| Collect once, evaluate many (`rescore`) | **Adopted** (D-015); now also the base of the law-change re-check | `rescore.py` |
| Score counts triggered rules, undetermined findings don't lower it (P-D4) | **Adopted** (D-015) | `rules_engine.py` |
| SSRF guard | **Adopted** (D-015) | `urls.check_target` |
| LLM extracts, code compares, unverified quotes dropped (P-D3) | **Adopted** (D-010, D-021) | `llm/policy.py` |
| Demo site in bad and fixed versions + golden test | **Replaced** by real reference sites, anonymized in public (D-017) | `backend/data/reference_sites.yaml` |
| Polling instead of SSE | **Not adopted** — SSE with replay (D-012) | `api.py` |
| SQLite as queue and store | **Not adopted for the MVP** — files per scan; SQLite comes with accounts and tokens (F-36, F-37) | `scans/` |
| Tailwind | **Not adopted** — Astryx design system (D-023) | `frontend/` |
| Canary probe with cancelled send (P-D5) | **Roadmap, category III** (D-009) | — |
| P-F1 Portfolio mode for legal service centers | **Roadmap** (B2G pilot); the batch scan is the base | `batch.py` |
| P-F2 Integration API + webhooks | **Partly:** the REST API exists (`/docs`); webhooks roadmap | `api.py` |
| Answers for the technical mentor (§18) | **Useful for rehearsal** | — |

## Sources

- `research/architecture-proposal.md` (v1), `ARCHITECTURE.md`, `PASSPORT.md` §15
