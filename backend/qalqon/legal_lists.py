"""Country list for cross-border transfers (art. 27¹ part 3 ZRU-547 + CMR No. 415).

Uses rules/countries.yaml (Role 2, verified) if present, otherwise backend/data/countries_draft.yaml (NOT VERIFIED).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

import yaml

from .config import DATA_DIR, RULES_DIR

# Statuses, from "fine" to "unknown":
#   local               — Uzbekistan
#   adequate            — on the adequate-protection list
#   conditional_met     — conditional country and the condition looks met (e.g. US + DPF participant)
#   conditional_unknown — conditional country, condition not known to be met
#   not_listed          — explicitly not on the list
#   not_in_known_list   — not among the countries we know are listed (our list may be incomplete!)
#   unknown             — country could not be determined (CDN, no response)


@lru_cache(maxsize=1)
def countries() -> dict:
    team_file = RULES_DIR / "countries.yaml"
    path = team_file if team_file.exists() else DATA_DIR / "countries_draft.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data["_file"] = str(path.name)
    data["adequate"] = set(data.get("adequate") or [])
    data["conditional"] = dict(data.get("conditional") or {})
    data["not_listed_confirmed"] = set(data.get("not_listed_confirmed") or [])
    return data


def country_status(country: Optional[str], dpf: Optional[bool] = None) -> str:
    if not country or country in ("?", "LOCAL"):
        return "unknown"
    if country == "UZ":
        return "local"
    lists = countries()
    if country in lists["adequate"]:
        return "adequate"
    if country in lists["conditional"]:
        return "conditional_met" if dpf else "conditional_unknown"
    if country in lists["not_listed_confirmed"] or lists.get("complete"):
        return "not_listed"  # the CMR 415 annex is a closed list (rules/countries.yaml: complete: true, D-028)
    return "not_in_known_list"


def list_info() -> dict:
    lists = countries()
    return {"file": lists["_file"], "verified": bool(lists.get("verified")), "source": lists.get("source")}
