"""URL helpers: hosts, registrable domains, and the SSRF guard for scan targets."""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urldefrag, urlparse

import tldextract

# Bundled public-suffix snapshot only — no network call at import time.
_extract = tldextract.TLDExtract(suffix_list_urls=())


class TargetNotAllowed(ValueError):
    """The URL must not be scanned (bad scheme, private network, unresolvable host)."""


def normalize_url(url: str) -> str:
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
    return urldefrag(url)[0]


def host_of(url: str) -> str:
    return (urlparse(url).hostname or "").lower()


def registrable_domain(host: str) -> str:
    """'www.shop.example.co.uk' -> 'example.co.uk'; IP addresses are returned as is."""
    if not host:
        return ""
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    ext = _extract(host)
    domain = getattr(ext, "top_domain_under_public_suffix", None) or ext.registered_domain
    return domain or host


def same_site(host: str, site_domain: str) -> bool:
    return registrable_domain(host) == site_domain


def _is_public(ip: str) -> bool:
    addr = ipaddress.ip_address(ip)
    return not (
        addr.is_private or addr.is_loopback or addr.is_link_local
        or addr.is_reserved or addr.is_multicast or addr.is_unspecified
    )


def check_target(url: str, allow_private: bool = False) -> None:
    """SSRF guard: only public http(s) targets, unless allow_private (local demo site)."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise TargetNotAllowed(f"scheme not allowed: {parsed.scheme!r}")
    host = parsed.hostname
    if not host:
        raise TargetNotAllowed("no host in URL")
    if allow_private:
        return
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as exc:
        raise TargetNotAllowed(f"cannot resolve {host}: {exc}") from exc
    for info in infos:
        ip = info[4][0]
        if not _is_public(ip):
            raise TargetNotAllowed(f"{host} resolves to non-public address {ip}")
