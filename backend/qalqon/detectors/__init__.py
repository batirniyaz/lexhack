"""Detectors: pure functions facts -> evidence. Rules (YAML) decide the level and the legal basis.

A detector returns:
  - a list of evidence dicts {"summary": str, "data": {...}} — empty list = nothing found;
  - None — cannot be evaluated on these facts (e.g. the policy was not analysed by the LLM yet).
"""

from __future__ import annotations

from typing import Callable, Optional

Evidence = dict
Detector = Callable[[dict, dict], Optional[list[Evidence]]]

DETECTORS: dict[str, Detector] = {}

TRACKING_CATEGORIES = {"analytics", "advertising", "session_replay", "social", "marketing", "ab_testing"}


def detector(name: str):
    def register(fn: Detector) -> Detector:
        DETECTORS[name] = fn
        return fn
    return register


# Import modules so their detectors register themselves.
from . import documents, forms, locality, security, trackers  # noqa: E402,F401
