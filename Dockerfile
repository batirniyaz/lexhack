# Probo: one image = FastAPI backend + headless Chromium (Playwright) + the built web app on one port.
# Build:  docker compose build      Run:  docker compose up -d      (see docker-compose.yml)

# --- 1. Build the web app -------------------------------------------------------------------------
FROM node:24-slim AS web
WORKDIR /web
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# --- 2. Backend + browser -------------------------------------------------------------------------
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    QALQON_HEADLESS=true
WORKDIR /app/backend

# Dependencies first (cached unless requirements change); Chromium with its system libraries.
# libatomic1: Playwright's bundled node driver needs it and python:3.11-slim does not ship it (verified 21.11).
COPY backend/requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends libatomic1 && rm -rf /var/lib/apt/lists/* \
 && pip install -r requirements.txt \
 && python -m playwright install --with-deps chromium

# Source code (secrets, scans, node_modules, venv are excluded by .dockerignore).
COPY . /app
COPY --from=web /web/dist /app/frontend/dist

# Offline IP -> country / ASN databases (DB-IP Lite, CC BY 4.0) for the current month.
RUN python -m qalqon.enrich.geo --download

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "qalqon.api:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
