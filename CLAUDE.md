# CLAUDE.md

Project **Qalqon**: a scanner that checks websites against Uzbekistan's personal data law. LexHackathon 2026, track 1. A team of 3.

## Before any work
1. Read `PASSPORT.md` in full. It is the single source of truth for the team and all AI assistants.
2. Don't challenge the decisions in passport §15 ("Decision log"). Propose improvements as "Features" (§10).
3. Find out your person's role (§3) and work on that role's tasks (§9).

## Rules
- Facts only with a source. Laws only from lex.uz, with a verbatim quote. Mark anything unverified as `NOT VERIFIED`.
- Result formats strictly per §11: research file header, rule YAML schema, competitor table, fact-check table.
- Where results go:
  - research → `research/`;
  - rules → `rules/<ID>.yaml`;
  - pitch → `pitch/`;
  - code → `backend/`, `frontend/`, `demo-site/`.
- Don't invent new detectors (the `detector` field in YAML) without agreeing with Role 1. The detector list is in §5.
- If you change `PASSPORT.md`, bump the version in its header and add a line to the "Changelog". Only Role 1 edits the passport; others send proposals.
- Document language: English. Interface and pitch texts additionally in Uzbek (Latin script) and Russian.

## Code
- Architecture, the `facts.json` contract, the API and the step-by-step build plan are in `ARCHITECTURE.md`. Read it before any code change.
- Main principle: code collects facts, rules (YAML) decide, the LLM only reads texts and explains.
- Backend: Python 3.11+, FastAPI, Playwright. LLM: Claude API (`claude-sonnet-5-5` for analysis, `claude-haiku-5-5` for mass tasks), answers in structured JSON with quotes.
- Findings are called "signs of violation"; levels: violation 🔴 / risk 🟡 / recommendation ⚪.
- In the demo and in public statistics we don't name specific real websites. For the demo we use `demo-site/`.

## Environment
- Python runs only inside the project virtualenv `backend/.venv`:
  - create: `python -m venv backend/.venv`
  - install: `backend/.venv/Scripts/python -m pip install -r backend/requirements.txt`
  - browser: `backend/.venv/Scripts/python -m playwright install chromium`
- Secrets live in `.env` at the repo root (template: `.env.example`). Never commit `.env`.
- Run the API from `backend/`: `.venv/Scripts/python -m uvicorn qalqon.api:app --port 8000`.

## Git (repository github.com/batirniyaz/lexhack, branch main)
- Before starting work and before every push: `git pull --rebase`.
- Everyone writes **only to their own folders**: Role 1 — code and `PASSPORT.md`; Role 2 — `research/legal-*`, `rules/`; Role 3 — the rest of `research/`, `pitch/`. That way there are no conflicts.
- Only Role 1 changes `PASSPORT.md`. Write proposals for it in your research files ("Questions for the team" section) or as "Features".
- Commit messages: short, in English, saying what was added. Never commit secrets (`.env`, API keys).

## Deadline
Checkpoint with selection for the final: **21.11, 14:00**. A working prototype is needed by then.
