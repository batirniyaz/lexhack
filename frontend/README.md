# Probo — web app

React 19 + Vite + TypeScript + Astryx (theme-neutral). How to run: see the root `README.md` ("Web app").
What the screens do: `../PRODUCT.md`. How it looks and why: `DESIGN.md`. API contract: `../ARCHITECTURE.md`.

- `src/api.ts` — typed API client + SSE subscription
- `src/i18n.tsx` — Uzbek (Latin) and Russian texts, presentation mode, country names
- `src/components/` — `FlowMap` (world map), `LiveScan` (live feed), `Report` (report screen and its parts), `Header`
- `src/pages/` — `Home`, `ScanPage` (live → report), `History`
