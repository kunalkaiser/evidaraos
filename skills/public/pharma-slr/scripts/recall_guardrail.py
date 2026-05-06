#!/usr/bin/env python3
"""Check recall guardrails before pruning retrieved records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _norm(value: str) -> str:
    return " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in value or "").split())


def _read_json(path: str | None, default):
    if not path:
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _records(payload) -> list[dict]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise ValueError("Records input must be a JSON array or object with records array")


def _sentinel_present(record: dict, sentinel: dict) -> bool:
    doi = _norm(record.get("doi", ""))
    pmid = _norm(record.get("pmid", ""))
    title = _norm(record.get("title", ""))
    return bool(
        (sentinel.get("doi") and _norm(sentinel["doi"]) == doi)
        or (sentinel.get("pmid") and _norm(str(sentinel["pmid"])) == pmid)
        or (sentinel.get("title") and _norm(sentinel["title"]) in title)
    )


def check_guardrails(records: list[dict], sentinels: list[dict], mesh_candidates: list[dict], citation_candidates: list[dict]) -> dict:
    missing_sentinels = [sentinel for sentinel in sentinels if not any(_sentinel_present(record, sentinel) for record in records)]
    retrieved_ids = {_norm(record.get("doi") or record.get("pmid") or record.get("title", "")) for record in records}
    missed_mesh = [
        candidate for candidate in mesh_candidates
        if _norm(candidate.get("doi") or candidate.get("pmid") or candidate.get("title", "")) not in retrieved_ids
    ]
    citation_flags = [
        candidate for candidate in citation_candidates
        if _norm(candidate.get("doi") or candidate.get("pmid") or candidate.get("title", "")) not in retrieved_ids
    ]
    review_articles = [
        record for record in records
        if "review" in _norm(record.get("title", "")) or "systematic review" in _norm(record.get("abstract", ""))
    ]
    warnings = []
    if missing_sentinels:
        warnings.append("One or more known/sentinel papers were not retrieved.")
    if missed_mesh:
        warnings.append("Concept/MeSH-style candidate records may be missing from the retrieved set.")
    if citation_flags:
        warnings.append("Citation-chasing candidates require review before pruning.")
    if review_articles:
        warnings.append("Review articles are present; check whether they cite primary studies absent from the retrieved set.")
    return {
        "summary": {
            "records_checked": len(records),
            "sentinels_checked": len(sentinels),
            "missing_sentinels": len(missing_sentinels),
            "mesh_or_concept_candidates_flagged": len(missed_mesh),
            "citation_chasing_candidates_flagged": len(citation_flags),
            "review_articles_for_backward_chasing": len(review_articles),
            "guardrail_passed": not (missing_sentinels or missed_mesh or citation_flags),
        },
        "missing_sentinel_papers": missing_sentinels,
        "mesh_or_concept_missed_records": missed_mesh,
        "citation_chasing_candidates": citation_flags,
        "review_articles_to_check_for_primary_studies": review_articles,
        "warnings": warnings,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run recall guardrails before high-precision pruning.")
    parser.add_argument("records", help="retrieved/deduplicated records JSON")
    parser.add_argument("--sentinel-json", help="known key papers JSON array")
    parser.add_argument("--mesh-candidates-json", help="candidate records from broader concept/MeSH query")
    parser.add_argument("--citation-candidates-json", help="candidate records from citation chasing")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = check_guardrails(
            _records(_read_json(args.records, [])),
            _read_json(args.sentinel_json, []),
            _read_json(args.mesh_candidates_json, []),
            _read_json(args.citation_candidates_json, []),
        )
    except Exception as exc:
        print(f"recall_guardrail.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
