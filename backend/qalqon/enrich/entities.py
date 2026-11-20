"""Host -> owning company (entity), its country and the service category (data/entities.yaml)."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

import yaml

from ..config import DATA_DIR

ENTITIES_FILE = DATA_DIR / "entities.yaml"


@lru_cache(maxsize=1)
def _index() -> list[tuple[str, dict]]:
    data = yaml.safe_load(ENTITIES_FILE.read_text(encoding="utf-8")) or {}
    index = []
    for entity in data.get("entities", []):
        for domain in entity.get("domains", []):
            index.append((domain.lower(), entity))
    index.sort(key=lambda item: len(item[0]), reverse=True)  # most specific first
    return index


def _matches(host: str, domain: str) -> bool:
    return host == domain or host.endswith("." + domain)


def identify(host: str) -> Optional[dict]:
    """Return {entity, company_country, dpf, category} or None if the host is unknown."""
    host = host.lower()
    for domain, entity in _index():
        if _matches(host, domain):
            categories = entity.get("category_by_domain") or {}
            # most specific category key that matches the host
            category = entity.get("category", "other")
            best = -1
            for key, value in categories.items():
                if _matches(host, key) and len(key) > best:
                    category, best = value, len(key)
            return {
                "entity": entity["name"],
                "company_country": entity.get("country"),
                "dpf": entity.get("dpf"),
                "category": category,
            }
    return None
