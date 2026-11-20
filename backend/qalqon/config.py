"""Settings from environment variables; .env is read from the repo root."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
DATA_DIR = BACKEND_DIR / "data"
RULES_DIR = REPO_ROOT / "rules"
SCANS_DIR = REPO_ROOT / "scans"  # raw scan outputs (HAR, facts.json) — git-ignored

load_dotenv(REPO_ROOT / ".env")


def _bool(name: str, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")
    lexrag_url: str = os.environ.get("LEXRAG_URL", "")
    lexrag_api_key: str = os.environ.get("LEXRAG_API_KEY", "")
    max_pages: int = int(os.environ.get("QALQON_MAX_PAGES", "20"))
    headless: bool = _bool("QALQON_HEADLESS", True)


settings = Settings()
