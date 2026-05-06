#!/usr/bin/env python3
"""Crossref Works API search for DOI-centered normalized records."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
from typing import Any

DEFAULT_TIMEOUT_SECONDS = 30
WORKS_ENDPOINT = "https://api.crossref.org/works"
MAX_RESULTS_UPPER_BOUND = 100
USER_AGENT = "evidenceos-pharma-slr/0.1 (mailto:contact@example.org)"

try:
    import requests  # type: ignore
except ImportError:
    import urllib.error
    import urllib.request

    class _UrllibResponse:
        def __init__(self, data: bytes, status: int) -> None:
            self.status_code = status
            self.text = data.decode("utf-8", errors="replace")

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"HTTP {self.status_code}: {self.text[:500]}")

        def json(self) -> Any:
            return json.loads(self.text)

    class _UrllibRequestsShim:
        @staticmethod
        def get(url: str, params: dict | None = None, timeout: int = DEFAULT_TIMEOUT_SECONDS, headers: dict | None = None) -> _UrllibResponse:
            if params:
                query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote_plus)
                url = f"{url}?{query}"
            req = urllib.request.Request(url, headers=headers or {})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return _UrllibResponse(resp.read(), resp.status)
            except urllib.error.HTTPError as exc:
                return _UrllibResponse(exc.read(), exc.code)

    requests = _UrllibRequestsShim()  # type: ignore


def _first(value: Any) -> str:
    if isinstance(value, list) and value:
        return str(value[0])
    if isinstance(value, str):
        return value
    return ""


def _date_parts(item: dict) -> str:
    for key in ["published-print", "published-online", "published", "created", "issued"]:
        parts = ((item.get(key) or {}).get("date-parts") or [[]])[0]
        if parts:
            year = str(parts[0])
            month = str(parts[1]).zfill(2) if len(parts) > 1 else ""
            day = str(parts[2]).zfill(2) if len(parts) > 2 else ""
            return "-".join(part for part in [year, month, day] if part)
    return ""


def _authors(item: dict) -> list[str]:
    names = []
    for author in item.get("author") or []:
        given = author.get("given") or ""
        family = author.get("family") or ""
        name = " ".join(part for part in [given, family] if part).strip()
        if name:
            names.append(name)
    return names


def _clean_abstract(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return " ".join(html.unescape(text).split())


def _normalize(item: dict) -> dict:
    doi = (item.get("DOI") or "").lower()
    pub_date = _date_parts(item)
    return {
        "id": doi,
        "source": "crossref",
        "title": _first(item.get("title")),
        "authors": _authors(item),
        "abstract": _clean_abstract(item.get("abstract") or ""),
        "journal": _first(item.get("container-title")),
        "year": pub_date[:4] if pub_date else "",
        "publication_date": pub_date,
        "doi": doi,
        "pmid": "",
        "url": item.get("URL") or (f"https://doi.org/{doi}" if doi else ""),
        "keywords": [str(subject) for subject in item.get("subject") or []],
    }


def search(query: str, max_results: int = 20) -> list[dict]:
    if max_results <= 0:
        return []
    max_results = min(max_results, MAX_RESULTS_UPPER_BOUND)
    resp = requests.get(
        WORKS_ENDPOINT,
        params={
            "query": query,
            "rows": max_results,
            "select": "DOI,title,author,abstract,container-title,published-print,published-online,published,created,issued,subject,URL",
        },
        timeout=DEFAULT_TIMEOUT_SECONDS,
        headers={"User-Agent": USER_AGENT},
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("status") == "failed":
        raise RuntimeError(f"Crossref returned an error: {payload}")
    return [_normalize(item) for item in payload.get("message", {}).get("items", [])]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search Crossref works and emit DOI-centered normalized JSON records.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example:\n  python crossref_search.py "dupilumab atopic dermatitis safety" --max-results 5\n',
    )
    parser.add_argument("query", help="free-text Crossref works query")
    parser.add_argument("--max-results", type=int, default=20, help="records to return")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        records = search(args.query, args.max_results)
    except Exception as exc:
        print(f"crossref_search.py: {exc}", file=sys.stderr)
        return 1
    json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
