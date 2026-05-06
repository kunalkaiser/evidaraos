#!/usr/bin/env python3
"""Semantic Scholar Graph API search for normalized literature records."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
from typing import Any

DEFAULT_TIMEOUT_SECONDS = 30
SEARCH_ENDPOINT = "https://api.semanticscholar.org/graph/v1/paper/search"
MAX_RESULTS_UPPER_BOUND = 100
USER_AGENT = "evidenceos-pharma-slr/0.1 (DeerFlow skill; public literature review)"


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
        def get(
            url: str,
            params: dict | None = None,
            timeout: int = DEFAULT_TIMEOUT_SECONDS,
            headers: dict | None = None,
        ) -> _UrllibResponse:
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


def _external_ids(paper: dict) -> dict:
    external = paper.get("externalIds") or {}
    return external if isinstance(external, dict) else {}


def _journal_name(paper: dict) -> str:
    journal = paper.get("journal") or {}
    if isinstance(journal, dict):
        return journal.get("name") or ""
    return ""


def _keywords(paper: dict) -> list[str]:
    values: list[str] = []
    for field in paper.get("fieldsOfStudy") or []:
        if field:
            values.append(str(field))
    for field in paper.get("s2FieldsOfStudy") or []:
        if isinstance(field, dict) and field.get("category"):
            values.append(str(field["category"]))
    return sorted(set(values), key=str.lower)


def _normalize(paper: dict) -> dict:
    external = _external_ids(paper)
    paper_id = paper.get("paperId") or external.get("CorpusId") or ""
    pub_date = paper.get("publicationDate") or ""
    year = paper.get("year")
    return {
        "id": str(paper_id),
        "source": "semantic_scholar",
        "title": paper.get("title") or "",
        "authors": [author.get("name", "") for author in paper.get("authors", []) if author.get("name")],
        "abstract": paper.get("abstract") or "",
        "journal": _journal_name(paper),
        "year": str(year or (pub_date[:4] if pub_date else "")),
        "publication_date": pub_date,
        "doi": external.get("DOI") or "",
        "pmid": external.get("PubMed") or "",
        "url": paper.get("url") or (f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else ""),
        "keywords": _keywords(paper),
        "citationCount": paper.get("citationCount"),
        "influentialCitationCount": paper.get("influentialCitationCount"),
    }


def search(query: str, max_results: int = 20, year: str | None = None) -> list[dict]:
    if max_results <= 0:
        return []
    max_results = min(max_results, MAX_RESULTS_UPPER_BOUND)
    params = {
        "query": query,
        "limit": max_results,
        "fields": ",".join(
            [
                "paperId",
                "title",
                "authors",
                "abstract",
                "year",
                "publicationDate",
                "journal",
                "externalIds",
                "url",
                "citationCount",
                "influentialCitationCount",
                "fieldsOfStudy",
                "s2FieldsOfStudy",
            ]
        ),
    }
    if year:
        params["year"] = year
    resp = requests.get(
        SEARCH_ENDPOINT,
        params=params,
        timeout=DEFAULT_TIMEOUT_SECONDS,
        headers={"User-Agent": USER_AGENT},
    )
    if resp.status_code == 429:
        raise RuntimeError(
            "Semantic Scholar returned HTTP 429 rate limit. Retry later, reduce max_results, "
            "or configure an API key in a future production integration."
        )
    resp.raise_for_status()
    payload = resp.json()
    if "error" in payload:
        raise RuntimeError(f"Semantic Scholar returned an error: {payload['error']}")
    return [_normalize(paper) for paper in payload.get("data", [])]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar Graph API and emit normalized JSON records.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python semantic_scholar_search.py "dupilumab safety atopic dermatitis" --max-results 5\n'
            '  python semantic_scholar_search.py "atopic dermatitis biologics" --year 2020-2025\n'
        ),
    )
    parser.add_argument("query", help="free-text search query")
    parser.add_argument("--max-results", type=int, default=20, help="records to return")
    parser.add_argument("--year", default=None, help="optional year or range, e.g. 2024 or 2020-2025")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        records = search(args.query, args.max_results, args.year)
    except Exception as exc:
        print(f"semantic_scholar_search.py: {exc}", file=sys.stderr)
        return 1
    json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
