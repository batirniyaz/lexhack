"""Thin wrapper around the Anthropic SDK: structured JSON output, refusal fallback, prompt caching, disk cache."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import anthropic

from ..config import SCANS_DIR

MODEL = os.environ.get("QALQON_LLM_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("QALQON_LLM_EFFORT", "medium")   # extraction task: medium is enough; raise if quality drops
CACHE_DIR = SCANS_DIR / ".llm_cache"                      # git-ignored with scans/
TIMEOUT_S = 180


class LLMError(Exception):
    """The model could not produce a usable answer (API error, refusal, truncated or invalid JSON)."""


@dataclass
class LLMResult:
    data: dict
    model: str
    cached: bool
    usage: dict


@lru_cache(maxsize=1)
def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic(timeout=TIMEOUT_S, max_retries=2)


def _cache_key(*parts: str) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part.encode("utf-8"))
        digest.update(b"\x00")
    return digest.hexdigest()[:32]


def structured_call(system: str, user: str, schema: dict, prompt_version: str) -> LLMResult:
    """One request with a JSON-schema answer. Results are cached on disk by (model, prompt version, input)."""
    key = _cache_key(MODEL, EFFORT, prompt_version, system, user, json.dumps(schema, sort_keys=True))
    cache_file = CACHE_DIR / f"{key}.json"
    if cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        return LLMResult(data=cached["data"], model=cached["model"], cached=True, usage=cached.get("usage", {}))

    try:
        response = _client().beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",                    # on a policy decline the API retries on a fallback model
            cache_control={"type": "ephemeral"},    # automatic prompt caching of the stable prefix
            output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": schema}},
            system=[{"type": "text", "text": system}],
            messages=[{"role": "user", "content": user}],
        )
    except anthropic.BadRequestError as exc:
        raise LLMError(f"bad request: {exc.message}") from exc
    except (anthropic.AuthenticationError, anthropic.PermissionDeniedError) as exc:
        raise LLMError("LLM credentials rejected — check ANTHROPIC_API_KEY in .env") from exc
    except anthropic.RateLimitError as exc:
        raise LLMError("rate limited by the LLM API — try again later") from exc
    except anthropic.APIStatusError as exc:
        raise LLMError(f"LLM API error {exc.status_code}: {exc.message}") from exc
    except anthropic.APIConnectionError as exc:
        raise LLMError("cannot reach the LLM API (network)") from exc

    if response.stop_reason == "refusal":
        raise LLMError("the model declined to answer")
    if response.stop_reason == "max_tokens":
        raise LLMError("answer was cut off (max_tokens)")
    text = next((block.text for block in response.content if block.type == "text"), None)
    if not text:
        raise LLMError("no text block in the answer")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError("answer is not valid JSON") from exc

    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cache_read_input_tokens": getattr(response.usage, "cache_read_input_tokens", None),
        "cache_creation_input_tokens": getattr(response.usage, "cache_creation_input_tokens", None),
    }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps({"data": data, "model": response.model, "usage": usage}, ensure_ascii=False),
                          encoding="utf-8")
    return LLMResult(data=data, model=response.model, cached=False, usage=usage)


def configured() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))


def model_name() -> Optional[str]:
    return MODEL
