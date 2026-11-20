"""Forms: consent, excessive data, biometrics."""

from __future__ import annotations

import re

from ..scanner.analysis import SENSITIVE_CATEGORIES
from . import detector

# Buttons of forms that submit an application / order (as opposed to "log in", "get code", "search").
_LEAD_BUTTON = re.compile(
    r"yubor|ariza|buyurtma|qoldir|ro.yxatdan|отправ|заявк|оставить|заказ|оформ|зарегистр|записат|send|submit|apply|order|sign ?up|register",
    re.I,
)


def _is_login(form: dict) -> bool:
    has_password = any(f.get("pd") == "password" for f in form["fields"])
    return has_password and len(form.get("pd_categories", [])) <= 1


def _is_identifier_only(form: dict) -> bool:
    """One phone/email field: usually login by SMS code or a newsletter — consent is taken elsewhere or is a separate question."""
    pd_fields = [f for f in form["fields"] if f.get("pd") in ("phone", "email")]
    return form.get("pd_categories") in (["phone"], ["email"]) and len(pd_fields) == 1


@detector("form_consent")
def form_consent(facts: dict, params: dict):
    evidence, seen = [], set()
    for form in facts.get("forms", []):
        if not form.get("collects_pd") or _is_login(form) or form.get("has_consent"):
            continue
        buttons = " ".join(form.get("buttons") or [])
        if _is_identifier_only(form) and not _LEAD_BUTTON.search(buttons):
            continue
        key = (form["pages"][0], tuple(form["pd_categories"]))
        if key in seen:
            continue  # the same form rendered several times on one page
        seen.add(key)
        evidence.append({
            "summary": f"Form on {form['pages'][0]} collects {', '.join(form['pd_categories'])} without a consent checkbox or consent text",
            "data": {"pages": form["pages"][:5], "pd": form["pd_categories"], "buttons": form.get("buttons"),
                     "fields": [f["label"] or f["name"] or f["placeholder"] for f in form["fields"] if f.get("pd")][:10]},
        })
    return evidence


@detector("form_pd_fields")
def form_pd_fields(facts: dict, params: dict):
    sensitive = set(params.get("categories") or SENSITIVE_CATEGORIES)
    evidence = []
    for form in facts.get("forms", []):
        found = [c for c in form.get("pd_categories", []) if c in sensitive]
        if found:
            evidence.append({
                "summary": f"Form on {form['pages'][0]} asks for {', '.join(found)} — check that this is necessary for the stated purpose",
                "data": {"pages": form["pages"][:5], "sensitive": found, "all_pd": form["pd_categories"]},
            })
    return evidence


@detector("biometric_capture")
def biometric_capture(facts: dict, params: dict):
    evidence = []
    for upload in facts.get("uploads", []):
        if upload.get("pd") == "photo" or upload.get("capture") is not None:
            evidence.append({"summary": f"Photo/selfie upload on {upload['page']} ({upload['label'] or 'file field'}) — possible biometric data",
                             "data": upload})
    for permission in facts.get("permissions", []):
        if permission.get("api") == "camera_or_microphone" and permission.get("video"):
            evidence.append({"summary": f"Camera access requested on {permission['page']}", "data": permission})
    return evidence
