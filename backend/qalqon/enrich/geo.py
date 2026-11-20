"""IP -> country / ASN / network owner, from offline DB-IP Lite databases (CC BY 4.0).

Attribution required in reports: "IP Geolocation by DB-IP" (https://db-ip.com).
Download/refresh (from backend/):  .venv/Scripts/python -m qalqon.enrich.geo --download
"""

from __future__ import annotations

import argparse
import gzip
import ipaddress
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Optional

import httpx
import maxminddb

from ..config import DATA_DIR

GEO_DIR = DATA_DIR / "geo"
ATTRIBUTION = "IP Geolocation by DB-IP (https://db-ip.com), CC BY 4.0"

# Anycast CDNs: the IP's country says nothing about where the data ends up.
CDN_ASNS = {
    13335: "Cloudflare", 209242: "Cloudflare",
    20940: "Akamai", 16625: "Akamai", 21342: "Akamai", 32787: "Akamai",
    54113: "Fastly",
}


def _latest(kind: str) -> Optional[Path]:
    files = sorted(GEO_DIR.glob(f"dbip-{kind}-lite-*.mmdb"))
    return files[-1] if files else None


class GeoDB:
    def __init__(self) -> None:
        country_path, asn_path = _latest("country"), _latest("asn")
        self.country = maxminddb.open_database(str(country_path)) if country_path else None
        self.asn = maxminddb.open_database(str(asn_path)) if asn_path else None
        self.files = [p.name for p in (country_path, asn_path) if p]

    @property
    def available(self) -> bool:
        return self.country is not None

    @lru_cache(maxsize=4096)
    def lookup(self, ip: str) -> dict:
        result = {"server_country": None, "asn": None, "org": None, "is_cdn": False}
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return result
        if not addr.is_global:
            result["server_country"] = "LOCAL"
            return result
        if self.country:
            rec = self.country.get(ip) or {}
            result["server_country"] = (rec.get("country") or {}).get("iso_code")
        if self.asn:
            rec = self.asn.get(ip) or {}
            result["asn"] = rec.get("autonomous_system_number")
            result["org"] = rec.get("autonomous_system_organization")
        if result["asn"] in CDN_ASNS:
            result["is_cdn"] = True
        return result


@lru_cache(maxsize=1)
def geodb() -> GeoDB:
    return GeoDB()


def download(month: Optional[str] = None) -> list[Path]:
    month = month or date.today().strftime("%Y-%m")
    GEO_DIR.mkdir(parents=True, exist_ok=True)
    saved = []
    for kind in ("country", "asn"):
        name = f"dbip-{kind}-lite-{month}.mmdb"
        url = f"https://download.db-ip.com/free/{name}.gz"
        response = httpx.get(url, timeout=180, follow_redirects=True)
        response.raise_for_status()
        target = GEO_DIR / name
        target.write_bytes(gzip.decompress(response.content))
        saved.append(target)
    return saved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="qalqon.enrich.geo")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--month", help="YYYY-MM, default: current month")
    args = parser.parse_args()
    if args.download:
        for path in download(args.month):
            print("saved", path)
