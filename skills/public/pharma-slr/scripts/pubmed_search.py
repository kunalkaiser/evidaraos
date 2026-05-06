#!/usr/bin/env python3
"""PubMed search CLI for the EvidenceOS pharma SLR DeerFlow skill.

Uses NCBI E-utilities public endpoints and emits normalized JSON records.
No API key is required.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Any

DEFAULT_TIMEOUT_SECONDS = 30
ESEARCH_ENDPOINT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH_ENDPOINT = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
MAX_RESULTS_UPPER_BOUND = 200
USER_AGENT = "evidenceos-pharma-slr/0.1 (DeerFlow skill; public biomedical review)"

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
                query = urllib.parse.urlencode(params, doseq=True, quote_via=urllib.parse.quote_plus)
                url = f"{url}?{query}"
            req = urllib.request.Request(url, headers=headers or {})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return _UrllibResponse(resp.read(), resp.status)
            except urllib.error.HTTPError as exc:
                return _UrllibResponse(exc.read(), exc.code)

    requests = _UrllibRequestsShim()  # type: ignore


def _text(node: ET.Element | None, default: str = "") -> str:
    return " ".join((node.text or default).split()) if node is not None else default


def _node_text(parent: ET.Element, path: str, default: str = "") -> str:
    return _text(parent.find(path), default)


def _article_title(article: ET.Element) -> str:
    node = article.find(".//ArticleTitle")
    return " ".join("".join(node.itertext()).split()) if node is not None else ""


def _abstract(article: ET.Element) -> str:
    parts = []
    for node in article.findall(".//Abstract/AbstractText"):
        label = node.get("Label")
        text = " ".join("".join(node.itertext()).split())
        if text:
            parts.append(f"{label}: {text}" if label else text)
    return " ".join(parts)


def _authors(article: ET.Element) -> list[str]:
    authors: list[str] = []
    for author in article.findall(".//AuthorList/Author"):
        collective = _node_text(author, "CollectiveName")
        if collective:
            authors.append(collective)
            continue
        first = _node_text(author, "ForeName")
        last = _node_text(author, "LastName")
        initials = _node_text(author, "Initials")
        if first and last:
            authors.append(f"{first} {last}")
        elif initials and last:
            authors.append(f"{initials} {last}")
        elif last:
            authors.append(last)
    return authors


def _publication_date(article: ET.Element) -> str:
    pub_date = article.find(".//Journal/JournalIssue/PubDate")
    if pub_date is None:
        pub_date = article.find(".//ArticleDate")
    if pub_date is None:
        return ""
    year = _node_text(pub_date, "Year") or _node_text(pub_date, "MedlineDate")[:4]
    month = _node_text(pub_date, "Month")
    day = _node_text(pub_date, "Day")
    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
    }
    if month:
        month = month_map.get(month[:3], month.zfill(2) if month.isdigit() else "")
    if day:
        day = day.zfill(2)
    return "-".join(part for part in [year, month, day] if part)


def _doi(article: ET.Element) -> str:
    for node in article.findall(".//ArticleIdList/ArticleId"):
        if node.get("IdType", "").lower() == "doi":
            return _text(node).lower()
    for node in article.findall(".//ELocationID"):
        if node.get("EIdType", "").lower() == "doi":
            return _text(node).lower()
    return ""


def _keywords(article: ET.Element) -> list[str]:
    values = []
    for node in article.findall(".//KeywordList/Keyword"):
        value = " ".join("".join(node.itertext()).split())
        if value:
            values.append(value)
    for node in article.findall(".//MeshHeading/DescriptorName"):
        value = _text(node)
        if value:
            values.append(value)
    return sorted(set(values), key=str.lower)


def _parse_article(article: ET.Element) -> dict:
    pmid = _node_text(article, ".//PMID")
    pub_date = _publication_date(article)
    return {
        "id": pmid,
        "source": "pubmed",
        "title": _article_title(article),
        "authors": _authors(article),
        "abstract": _abstract(article),
        "journal": _node_text(article, ".//Journal/Title") or _node_text(article, ".//Journal/ISOAbbreviation"),
        "year": pub_date[:4] if pub_date else "",
        "publication_date": pub_date,
        "doi": _doi(article),
        "pmid": pmid,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
        "keywords": _keywords(article),
    }


def _raise_for_ncbi_error(resp: Any, context: str) -> None:
    resp.raise_for_status()
    text = resp.text.strip()
    if "<ERROR>" in text or "<ErrorList>" in text:
        raise RuntimeError(f"NCBI {context} returned an error: {text[:1000]}")


def search(query: str, max_results: int = 20, start_date: str | None = None, end_date: str | None = None) -> list[dict]:
    if max_results <= 0:
        return []
    max_results = min(max_results, MAX_RESULTS_UPPER_BOUND)
    params: dict[str, Any] = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
        "usehistory": "n",
        "tool": "evidenceos-pharma-slr",
    }
    if start_date or end_date:
        params["datetype"] = "pdat"
        params["mindate"] = start_date or "1900/01/01"
        params["maxdate"] = end_date or "3000/12/31"
    resp = requests.get(ESEARCH_ENDPOINT, params=params, timeout=DEFAULT_TIMEOUT_SECONDS, headers={"User-Agent": USER_AGENT})
    _raise_for_ncbi_error(resp, "ESearch")
    payload = resp.json()
    if payload.get("error"):
        raise RuntimeError(f"NCBI ESearch returned an error: {payload['error']}")
    result = payload.get("esearchresult", {})
    if result.get("errorlist"):
        raise RuntimeError(f"NCBI ESearch returned an error: {result['errorlist']}")
    pmids = result.get("idlist", [])
    if not pmids:
        return []
    time.sleep(0.12)
    resp = requests.get(
        EFETCH_ENDPOINT,
        params={"db": "pubmed", "id": ",".join(pmids), "retmode": "xml", "rettype": "abstract", "tool": "evidenceos-pharma-slr"},
        timeout=DEFAULT_TIMEOUT_SECONDS,
        headers={"User-Agent": USER_AGENT},
    )
    _raise_for_ncbi_error(resp, "EFetch")
    root = ET.fromstring(resp.text)
    errors = [node.text for node in root.findall(".//ERROR") if node.text]
    if errors:
        raise RuntimeError(f"NCBI EFetch returned an error: {'; '.join(errors)}")
    by_pmid = {_node_text(article, ".//PMID"): _parse_article(article) for article in root.findall(".//PubmedArticle")}
    return [by_pmid[pmid] for pmid in pmids if pmid in by_pmid]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search PubMed through NCBI E-utilities and emit normalized JSON records.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python pubmed_search.py "dupilumab atopic dermatitis safety" --max-results 5\n'
            '  python pubmed_search.py "asthma biologics" --max-results 10 --start-date 2020-01-01\n'
        ),
    )
    parser.add_argument("query", help="PubMed search query")
    parser.add_argument("--max-results", type=int, default=20, help="records to return")
    parser.add_argument("--start-date", default=None, help="publication start date, YYYY-MM-DD")
    parser.add_argument("--end-date", default=None, help="publication end date, YYYY-MM-DD")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        records = search(args.query, args.max_results, args.start_date, args.end_date)
    except Exception as exc:
        print(f"pubmed_search.py: {exc}", file=sys.stderr)
        return 1
    json.dump(records, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
