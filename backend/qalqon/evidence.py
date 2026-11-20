"""Evidence seal for every report (F-19, F-27, F-21).

- `scope(facts)`: what was checked, when, from where, with which rules, model and prompt.
- `write_seal(scan_dir)`: SHA-256 of facts.json, scan.har and the report, signed with Ed25519 → seal.json.
- `verify(seal)`: checks the signature and whether this server issued a report with that hash.

The signing key is PROBO_SIGNING_KEY (base64 of a 32-byte seed) or scans/.signing_key, created on first use.
Same facts + same rules version → same report hash: anyone can re-run `rescore` and compare.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from . import __version__
from .config import BACKEND_DIR, DATA_DIR, RULES_DIR, SCANS_DIR

KEY_FILE = SCANS_DIR / ".signing_key"
ALGORITHM = "Ed25519"


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@lru_cache(maxsize=1)
def rules_version() -> str:
    """Short hash over every file that decides findings: rules (draft + team), countries list, law quotes."""
    files = sorted((BACKEND_DIR / "rules_draft").glob("*.yaml")) + sorted(RULES_DIR.glob("*.yaml"))
    files += [DATA_DIR / "law_quotes.json"]
    digest = hashlib.sha256()
    for path in files:
        if path.exists():
            digest.update(path.name.encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def scope(facts: dict) -> dict:
    policy = facts.get("policy") or {}
    stats = facts.get("stats") or {}
    return {
        "mode": "passive",
        "pages": [p.get("url") for p in facts.get("pages") or []][:50],
        "pages_count": stats.get("pages"),
        "requests": stats.get("requests"),
        "scanned_at": facts.get("scanned_at"),
        "vantage": os.environ.get("PROBO_VANTAGE") or None,   # e.g. "UZ, Uzbektelekom (AS8193)" on the server
        "scanner_version": __version__,
        "rules_version": rules_version(),
        "llm": {"model": policy.get("model"), "prompt_version": policy.get("prompt_version")} if policy.get("model") else None,
    }


@lru_cache(maxsize=1)
def _private_key() -> Ed25519PrivateKey:
    seed_b64 = os.environ.get("PROBO_SIGNING_KEY", "")
    if seed_b64:
        return Ed25519PrivateKey.from_private_bytes(base64.b64decode(seed_b64))
    if KEY_FILE.exists():
        return Ed25519PrivateKey.from_private_bytes(base64.b64decode(KEY_FILE.read_text().strip()))
    key = Ed25519PrivateKey.generate()
    seed = key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(base64.b64encode(seed).decode())
    try:
        KEY_FILE.chmod(0o600)
    except OSError:
        pass
    return key


def public_key_b64() -> str:
    raw = _private_key().public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return base64.b64encode(raw).decode()


def key_id() -> str:
    return sha256_bytes(base64.b64decode(public_key_b64()))[:16]


def report_hash(report: dict) -> str:
    return sha256_bytes(canonical(report))


def _relative_id(scan_dir: Path) -> str:
    try:
        return scan_dir.resolve().relative_to(SCANS_DIR.resolve()).as_posix()
    except ValueError:
        return scan_dir.name


def write_seal(scan_dir: Path) -> Optional[dict]:
    """Seal the report in scan_dir (call after report.json is written). Returns the seal."""
    report_path = scan_dir / "report.json"
    if not report_path.exists():
        return None
    report = json.loads(report_path.read_text(encoding="utf-8"))
    statement = {
        "issuer": "Probo",
        "scan_id": report.get("scan_id") or _relative_id(scan_dir),
        "site": report.get("site"),
        "scanned_at": report.get("scanned_at"),
        "status": report.get("status"),
        "score": report.get("score"),
        "levels": report.get("levels"),
        "scope": report.get("scope"),
        "sha256": {"report": report_hash(report), "facts": sha256_file(scan_dir / "facts.json"),
                   "har": sha256_file(scan_dir / "scan.har")},
        "sealed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "key_id": key_id(),
    }
    signature = base64.b64encode(_private_key().sign(canonical(statement))).decode()
    seal = {"statement": statement, "algorithm": ALGORITHM, "public_key": public_key_b64(), "signature": signature}
    (scan_dir / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=2), encoding="utf-8")
    return seal


def _known_report(report_sha: str) -> Optional[dict]:
    for path in SCANS_DIR.rglob("seal.json"):
        try:
            statement = json.loads(path.read_text(encoding="utf-8"))["statement"]
        except (OSError, ValueError, KeyError):
            continue
        if (statement.get("sha256") or {}).get("report") == report_sha:
            return statement
    return None


def verify(seal: dict) -> dict:
    """Is the signature valid, is it our key, and did this server issue a report with that hash?"""
    try:
        statement = seal["statement"]
        public = Ed25519PublicKey.from_public_bytes(base64.b64decode(seal["public_key"]))
        public.verify(base64.b64decode(seal["signature"]), canonical(statement))
        valid = True
    except (KeyError, ValueError, TypeError, InvalidSignature):
        return {"valid_signature": False, "our_key": False, "known_report": False}
    report_sha = (statement.get("sha256") or {}).get("report") or ""
    return {
        "valid_signature": valid,
        "our_key": seal.get("public_key") == public_key_b64(),
        "known_report": _known_report(report_sha) is not None,
        "statement": statement,
    }
