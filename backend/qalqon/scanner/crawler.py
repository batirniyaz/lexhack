"""Headless crawl of one site: requests + server IPs, cookies, forms, permissions, legal documents, backends in code.

Navigation never waits for `load` / `networkidle` (ARCHITECTURE.md §2.1, decision D-016):
one hanging third-party script would block those events forever. We commit the navigation,
then watch the network for a fixed window, then read the DOM.
"""

from __future__ import annotations

import asyncio
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import urldefrag, urlparse, urlsplit

from playwright.async_api import BrowserContext, Page, Request, Response, async_playwright

from ..config import settings
from ..urls import host_of, normalize_url, registrable_domain
from .analysis import analyze_form, document_kind, find_backends, has_webvisor
from .page_js import HOOKS_JS, LINKS_JS, PAGE_JS, TEXT_JS

Emit = Callable[[dict], None]

UA_TEMPLATE = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36"
)
# Pages most likely to collect personal data or hold legal documents are visited first.
PRIORITY_WORDS = (
    "contact", "aloqa", "kontakt", "register", "ro'yxat", "royxat", "signup", "checkout",
    "buyurtma", "order", "login", "kirish", "anketa", "ariza", "privacy", "maxfiylik",
    "policy", "siyosat", "oferta", "offer", "politika", "konfiden", "shartlar", "terms",
)
SKIP_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico", ".zip", ".rar",
    ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".mp4", ".mp3", ".avi",
)
POST_DATA_LIMIT = 4000
MAX_DEPTH = 2
BLOCK_STATUSES = {401, 403, 429, 498, 503}   # landing answers that mean "not served to us"
MAX_LINKS_PER_PAGE = 300
MIN_LINKS = 5            # fewer links than this after the observation window -> wait and read again (SPA)
SITEMAP_LIMIT = 20       # non-priority sitemap URLs to queue
MAX_SCRIPT_READS = 60    # script bodies scanned for backends per site
MAX_SCRIPT_BYTES = 3_000_000
# Public pages any visitor could open; probed only if the site does not answer 200 to every path.
COMMON_PATHS = (
    "/contact", "/contacts", "/aloqa", "/privacy", "/privacy-policy", "/policy",
    "/oferta", "/offer", "/public-offer", "/terms", "/agreement",
)
CHALLENGE_TITLES = (
    ("just a moment", "cloudflare-challenge"),
    ("attention required", "cloudflare-block"),
    ("checking your browser", "browser-check"),
    ("ddos-guard", "ddos-guard"),
    ("вы не робот", "captcha"),
    ("are you not a robot", "captcha"),
    ("siz robot emasmisiz", "captcha"),
    ("access denied", "access-denied"),
)
CHALLENGE_EXTRA_WAIT_MS = 8000
SECURITY_HEADERS = (
    "strict-transport-security", "content-security-policy", "x-content-type-options",
    "x-frame-options", "referrer-policy", "permissions-policy", "server",
)


def _noop(_: dict) -> None:
    pass


class _Recorder:
    """Collects request/response facts for the whole browser context."""

    def __init__(self, site_domains: set[str], emit: Emit):
        self.site_domains = site_domains
        self.emit = emit
        self.records: list[dict] = []
        self.backends: list[dict] = []
        self._by_request: dict[Request, dict] = {}
        self._tasks: set[asyncio.Task] = set()
        self._announced_hosts: set[str] = set()
        self._script_reads = 0
        self.current_page: Optional[str] = None
        self.phase = "landing"  # 'landing' = first page, nothing clicked; then 'crawl'
        self.t0 = time.monotonic()

    def is_third_party(self, host: str) -> bool:
        return registrable_domain(host) not in self.site_domains

    def on_request(self, request: Request) -> None:
        url = request.url
        if not url.startswith(("http://", "https://")):
            return  # data:, blob:, chrome-extension: …
        host = host_of(url)
        record = {
            "url": url[:2000],
            "host": host,
            "method": request.method,
            "type": request.resource_type,
            "page": self.current_page,
            "phase": self.phase,
            "t_ms": int((time.monotonic() - self.t0) * 1000),
            "third_party": self.is_third_party(host),
            "post_data": None,
            "status": None,
            "ip": None,
            "failed": None,
        }
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body = request.post_data
            except Exception:  # binary body
                body = None
            if body:
                record["post_data"] = body[:POST_DATA_LIMIT]
        self.records.append(record)
        self._by_request[request] = record

    def on_response(self, response: Response) -> None:
        task = asyncio.ensure_future(self._fill_response(response))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _fill_response(self, response: Response) -> None:
        record = self._by_request.get(response.request)
        if record is None:
            return
        record["status"] = response.status
        try:
            addr = await response.server_addr()
        except Exception:
            addr = None
        if addr:
            record["ip"] = addr.get("ipAddress")
        host = record["host"]
        if host not in self._announced_hosts:
            self._announced_hosts.add(host)
            self.emit({
                "type": "host",
                "host": host,
                "ip": record["ip"],
                "third_party": record["third_party"],
                "phase": record["phase"],
            })
        if record["type"] == "script" and record["phase"] != "challenge" and self._script_reads < MAX_SCRIPT_READS:
            self._script_reads += 1
            try:
                body = await response.body()
            except Exception:
                body = b""
            if body and len(body) <= MAX_SCRIPT_BYTES:
                for item in find_backends(body.decode("utf-8", errors="ignore"), record["url"]):
                    item["page"] = record["page"]
                    self.backends.append(item)

    def on_failed(self, request: Request) -> None:
        record = self._by_request.get(request)
        if record is not None:
            record["failed"] = request.failure or "failed"

    async def drain(self) -> None:
        if self._tasks:
            await asyncio.gather(*list(self._tasks), return_exceptions=True)


def _key(url: str) -> str:
    """Identity of a page for de-duplication: no fragment, lower-case host, no trailing slash."""
    parsed = urlparse(urldefrag(url)[0])
    path = parsed.path.rstrip("/") or "/"
    query = f"?{parsed.query}" if parsed.query else ""
    return f"{parsed.scheme}://{(parsed.hostname or '').lower()}{path}{query}"


def _challenge(final_url: str, title: Optional[str]) -> Optional[str]:
    """Bot-protection page instead of the real site? Findings on such a page would be false."""
    url = (final_url or "").lower()
    if "showcaptcha" in url or "captcha" in urlparse(url).path:
        return "captcha"
    text = (title or "").lower()
    for marker, kind in CHALLENGE_TITLES:
        if marker in text:
            return kind
    return None


def _priority(url: str, text: str) -> int:
    haystack = (url + " " + text).lower()
    return 0 if any(word in haystack for word in PRIORITY_WORDS) else 1


def _crawlable(url: str, site_domains: set[str]) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if registrable_domain(host_of(url)) not in site_domains:
        return False
    return not parsed.path.lower().endswith(SKIP_EXTENSIONS)


async def _discover(context: BrowserContext, start_url: str, site_domains: set[str]) -> list[tuple[int, str]]:
    """Extra pages for SPAs that render few <a href> links: sitemap.xml + common public paths."""
    parsed = urlparse(start_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    found: list[tuple[int, str]] = []

    async def fetch(url: str, timeout: int = 8000):
        try:
            return await context.request.get(url, timeout=timeout, max_redirects=3)
        except Exception:
            return None

    response = await fetch(origin + "/sitemap.xml")
    if response is not None and response.ok:
        text = await response.text()
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text)[:500]
        if "<sitemapindex" in text:
            nested = []
            for sub in locs[:2]:
                sub_response = await fetch(sub)
                if sub_response is not None and sub_response.ok:
                    nested += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", await sub_response.text())[:500]
            locs = nested
        plain = 0
        for loc in locs:
            if not _crawlable(loc, site_domains):
                continue
            priority = _priority(loc, "")
            if priority == 1:
                if plain >= SITEMAP_LIMIT:
                    continue
                plain += 1
            found.append((priority, urldefrag(loc)[0]))

    probe = await fetch(origin + "/qalqon-404-probe-7f3a", timeout=6000)
    if probe is not None and probe.status == 404:
        responses = await asyncio.gather(*(fetch(origin + path, timeout=6000) for path in COMMON_PATHS))
        for response in responses:
            if response is None or not response.ok:
                continue
            if "html" not in (response.headers.get("content-type") or ""):
                continue
            if _crawlable(response.url, site_domains):
                found.append((0, urldefrag(response.url)[0]))
    return found


_CONTACT_PATH = re.compile(r"contact|kontakt|aloqa|about|o-nas|biz-haqimizda|haqimizda|rekvizit|реквизит|контакт", re.I)


def _is_landing_or_contact(url: str) -> bool:
    path = urlsplit(url).path.strip("/")
    return path in ("", "uz", "ru", "oz", "en", "uz/", "ru/") or bool(_CONTACT_PATH.search(path))


async def _collect(page: Page, info: dict) -> None:
    """Read everything we need from the DOM of the current page into `info`."""
    info["final_url"] = page.url
    try:
        data = await page.evaluate(PAGE_JS)
    except Exception:
        data = None
    if data:
        info["title"] = data["title"]
        info["storage_keys"] = data["storage_keys"]
        info["permissions"] = data["permissions"]
        info["forms"] = [analyze_form(form) for form in data["forms"]]
        info["legal_links"] = data["legal_links"]
        info["inline_backends"] = [
            item for script in data["inline_scripts"] for item in find_backends(script, f"inline script on {page.url}")
        ]
        info["webvisor"] = any(has_webvisor(script) for script in data["inline_scripts"])
        info["lang"] = data.get("lang") or None
        info["alternates"] = data.get("alternates") or []
        info["lang_links"] = data.get("lang_links") or []
        # Visible text only where seller details usually are: the landing page and contact / about pages.
        if _is_landing_or_contact(page.url):
            info["text"] = data.get("text") or ""
    info["challenge"] = _challenge(info["final_url"], info["title"])
    kind = None if info["challenge"] else document_kind(info["final_url"], info["title"] or "")
    if kind:
        try:
            info["document"] = {"kind": kind, "text": await page.evaluate(TEXT_JS)}
        except Exception:
            pass


async def _visit(page: Page, url: str, observe_ms: int, nav_timeout_ms: int) -> dict:
    started = time.monotonic()
    response = None
    error: Optional[str] = None
    try:
        response = await page.goto(url, wait_until="commit", timeout=nav_timeout_ms)
    except Exception as exc:
        error = f"{type(exc).__name__}: {str(exc).splitlines()[0][:200]}"
    await page.wait_for_timeout(observe_ms)
    info = {
        "url": url,
        "final_url": page.url,
        "status": response.status if response else None,
        "title": None,
        "error": error,
        "headers": {k: v for k, v in (response.headers if response else {}).items() if k in SECURITY_HEADERS},
        "storage_keys": {"local": [], "session": []},
        "observed_ms": 0,
    }
    await _collect(page, info)
    info["observed_ms"] = int((time.monotonic() - started) * 1000)
    return info


async def _links(page: Page) -> list[tuple[str, str]]:
    try:
        raw = await page.evaluate(LINKS_JS)
    except Exception:
        return []
    return [(urldefrag(href)[0], text) for href, text in raw[:MAX_LINKS_PER_PAGE]]


def _cookie_facts(cookies: list[dict], landing_keys: set[tuple[str, str]], site_domains: set[str]) -> list[dict]:
    result = []
    for c in cookies:
        domain = c.get("domain", "").lstrip(".")
        result.append({
            "name": c.get("name"),
            "domain": c.get("domain"),
            "path": c.get("path"),
            "expires": c.get("expires"),
            "http_only": c.get("httpOnly"),
            "secure": c.get("secure"),
            "same_site": c.get("sameSite"),
            "third_party": registrable_domain(domain) not in site_domains,
            "set_on_landing": (c.get("name"), c.get("domain")) in landing_keys,
        })
    return result


def _form_signature(form: dict) -> tuple:
    return (form.get("action"), tuple((f["name"], f["label"][:40], f["type"]) for f in form["fields"]))


def _assemble_page_facts(pages: list[dict], script_backends: list[dict]) -> dict:
    """Move per-page DOM findings into site-level lists (forms de-duplicated across pages)."""
    forms: dict[tuple, dict] = {}
    permissions, uploads, webvisor_pages = [], [], []
    documents: dict[str, dict] = {}
    legal_links: dict[str, dict] = {}
    backends: dict[tuple, dict] = {}
    for item in script_backends:
        backends.setdefault((item["kind"], item.get("region")), item)

    for p in pages:
        page_url = p["final_url"]
        per_page = {k: p.pop(k, None) for k in ("forms", "permissions", "legal_links", "inline_backends", "webvisor", "document")}
        if p.get("challenge"):
            continue
        for form in per_page["forms"] or []:
            signature = _form_signature(form)
            if signature in forms:
                forms[signature]["pages"].append(page_url)
                continue
            form["pages"] = [page_url]
            forms[signature] = form
            for field in form["fields"]:
                if field["type"] == "file":
                    uploads.append({"page": page_url, "label": field["label"], "accept": field["accept"],
                                    "capture": field["capture"], "pd": field.get("pd"), "destination": None})
        for permission in per_page["permissions"] or []:
            permissions.append({**permission, "page": page_url})
        for item in per_page["inline_backends"] or []:
            backends.setdefault((item["kind"], item.get("region")), {**item, "page": page_url})
        if per_page["webvisor"]:
            webvisor_pages.append(page_url)
        if per_page["document"]:
            documents[_key(page_url)] = {
                "kind": per_page["document"]["kind"], "url": page_url, "title": p["title"],
                "visited": True, "text": per_page["document"]["text"],
            }
        for link in per_page["legal_links"] or []:
            legal_links.setdefault(_key(link["href"]), link)

    for key, link in legal_links.items():
        if key not in documents:
            documents[key] = {"kind": document_kind(link["href"], link["text"]), "url": link["href"],
                              "title": link["text"], "visited": False, "text": None}
    return {
        "forms": list(forms.values()),
        "permissions": permissions,
        "uploads": uploads,
        "backends": list(backends.values()),
        "documents": list(documents.values()),
        "session_replay": {"webvisor_pages": webvisor_pages},
    }


async def crawl(
    start_url: str,
    *,
    max_pages: Optional[int] = None,
    har_path: Optional[Path] = None,
    emit: Emit = _noop,
    observe_first_ms: int = 8000,
    observe_ms: int = 3500,
    nav_timeout_ms: int = 20000,
) -> dict:
    """Crawl one site in passive mode and return the raw facts (ARCHITECTURE.md §2.3)."""
    start_url = normalize_url(start_url)
    max_pages = max_pages or settings.max_pages
    site_domains = {registrable_domain(host_of(start_url))}
    scanned_at = datetime.now(timezone.utc).isoformat()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=settings.headless)
        major = browser.version.split(".")[0]
        context: BrowserContext = await browser.new_context(
            user_agent=UA_TEMPLATE.format(major=major),
            locale="uz-UZ",
            viewport={"width": 1366, "height": 768},
            ignore_https_errors=True,
            record_har_path=str(har_path) if har_path else None,
            record_har_content="omit",
        )
        await context.add_init_script(HOOKS_JS)
        recorder = _Recorder(site_domains, emit)
        context.on("request", recorder.on_request)
        context.on("response", recorder.on_response)
        context.on("requestfailed", recorder.on_failed)
        page = await context.new_page()

        queue: list[tuple[int, str, int]] = [(0, start_url, 0)]  # (priority, url, depth)
        seen = {_key(start_url)}
        pages: list[dict] = []
        landing_cookie_keys: set[tuple[str, str]] = set()
        blocked: Optional[str] = None

        def enqueue(url: str, priority: int, depth: int) -> None:
            key = _key(url)
            if key not in seen and _crawlable(url, site_domains):
                seen.add(key)
                queue.append((priority, url, depth))

        while queue and len(pages) < max_pages:
            queue.sort(key=lambda item: item[0])
            _, url, depth = queue.pop(0)
            recorder.current_page = url
            emit({"type": "page", "url": url, "n": len(pages) + 1, "max": max_pages})
            info = await _visit(page, url, observe_first_ms if not pages else observe_ms, nav_timeout_ms)
            info["depth"] = depth
            seen.add(_key(info["final_url"]))

            if len(pages) == 0:
                if info["challenge"]:
                    # Bot protection: give an automatic JS challenge time to pass, then decide.
                    kind = info["challenge"]
                    emit({"type": "challenge", "kind": kind, "url": info["final_url"]})
                    for record in recorder.records:
                        record["phase"] = "challenge"
                    await page.wait_for_timeout(CHALLENGE_EXTRA_WAIT_MS)
                    await _collect(page, info)
                    if info["challenge"]:
                        blocked = kind
                        pages.append(info)
                        emit({"type": "blocked", "kind": kind})
                        break
                    info["challenge_passed"] = kind
                    # Treat the real page as the landing from here on; earlier requests stay marked 'challenge'.
                    recorder.current_page = info["final_url"]
                    await page.wait_for_timeout(observe_ms)
                    await _collect(page, info)
                # Anti-bot or error answer without a challenge page: HTTP 403/429/498/503 and almost no text
                # (wildberries.uz answered 498 with 28 characters on 21.11). Findings on it would be false (D-018).
                status = info.get("status") or 0
                if status in BLOCK_STATUSES and len((info.get("text") or "").strip()) < 300:
                    blocked = f"http-{status}"
                    info["challenge"] = blocked
                    pages.append(info)
                    emit({"type": "blocked", "kind": blocked})
                    break
                # The landing page may redirect to another registrable domain (example.uz -> example.com).
                landing_domain = registrable_domain(host_of(info["final_url"]))
                if landing_domain and landing_domain not in site_domains:
                    site_domains.add(landing_domain)
                pages.append(info)
                await recorder.drain()
                landing_cookie_keys = {(c["name"], c["domain"]) for c in await context.cookies()}
                recorder.phase = "crawl"
                for priority, extra in await _discover(context, info["final_url"] or start_url, site_domains):
                    enqueue(extra, priority, 1)
            else:
                pages.append(info)
                if info["challenge"]:
                    continue  # no links from a challenge page

            for form in info.get("forms", []):
                if form["collects_pd"]:
                    emit({"type": "form", "page": info["final_url"], "pd": form["pd_categories"],
                          "consent": form["has_consent"]})
            if info.get("document"):
                emit({"type": "document", "kind": info["document"]["kind"], "url": info["final_url"]})

            if depth < MAX_DEPTH:
                links = await _links(page)
                if len(links) < MIN_LINKS:
                    await page.wait_for_timeout(3000)  # SPA: links may render late
                    links = await _links(page)
                for href, text in links:
                    enqueue(href, _priority(href, text), depth + 1)

        await recorder.drain()
        cookies = await context.cookies()
        await context.close()  # flushes the HAR file
        await browser.close()

    # Re-evaluate third-party flags now that all site domains are known.
    for record in recorder.records:
        record["third_party"] = registrable_domain(record["host"]) not in site_domains
        record["pending"] = record["status"] is None and record["failed"] is None

    page_facts = _assemble_page_facts(pages, recorder.backends)
    third_party_hosts = sorted({r["host"] for r in recorder.records if r["third_party"]})
    return {
        "schema": 1,
        "site": start_url,
        "site_domains": sorted(site_domains),
        "scanned_at": scanned_at,
        "mode": "passive",
        "consent_given": False,  # passive mode never clicks a consent banner
        "blocked": blocked,      # bot protection we could not pass -> no findings must be produced
        "pages": pages,
        "requests": recorder.records,
        "cookies": _cookie_facts(cookies, landing_cookie_keys, site_domains),
        **page_facts,
        "dns": {},
        "policy": {},
        "stats": {
            "pages": len(pages),
            "requests": len(recorder.records),
            "third_party_requests": sum(1 for r in recorder.records if r["third_party"]),
            "third_party_hosts": len(third_party_hosts),
            "cookies": len(cookies),
            "pending_requests": sum(1 for r in recorder.records if r["pending"]),
            "challenge_pages": sum(1 for p in pages if p.get("challenge")),
            "forms_with_pd": sum(1 for f in page_facts["forms"] if f["collects_pd"]),
            "documents_found": len(page_facts["documents"]),
        },
    }
