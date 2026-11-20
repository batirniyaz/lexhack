"""HTTP API. Run from backend/: .venv/Scripts/python -m uvicorn qalqon.api:app --reload"""

from fastapi import FastAPI

from . import __version__
from .config import settings

app = FastAPI(title="Qalqon", version=__version__)


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "ok",
        "version": __version__,
        "llm_configured": bool(settings.anthropic_api_key),
        "lexrag_configured": bool(settings.lexrag_url),
    }
