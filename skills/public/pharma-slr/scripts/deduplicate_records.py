#!/usr/bin/env python3
"""Deduplicate normalized literature records by DOI, PMID, then title."""

from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


def _norm_doi(value: str | None) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    value = re.sub(r"^doi:\s*", "", value)
    return value.rstrip(".")


def _norm_pmid(value: str | int | None) -> str:
    return str(value or "").strip()


def _norm_title(value: str | None) -> str:
    value = re.sub(r"[^a-z0-9]+", " ", (value or "").lower())
    return " ".join(value.split())


def _record_key(record: dict) -> tuple[str, str]:
    doi = _norm_doi(record.get("doi"))
    if doi:
        return ("doi", doi)
    pmid = _norm_pmid(record.get("pmid"))
    if pmid:
        return ("pmid", pmid)
    title = _norm_title(record.get("title"))
    if title:
        return ("title", title)
    return ("id", f"{record.get('source', '')}:{record.get('id', '')}")


def _provenance(record: dict) -> dict:
    return {
        "source": record.get("source", ""),
        "id": record.get("id", ""),
        "doi": _norm_doi(record.get("doi")),
        "pmid": _norm_pmid(record.get("pmid")),
        "url": record.get("url", ""),
    }


def _merge_record(base: dict, incoming: dict) -> dict:
    for key, value in incoming.items():
        if key == "sources":
            continue
        if key not in base or base.get(key) in ("", None, [], {}):
            base[key] = value
        elif key == "keywords":
            merged = list(base.get("keywords") or []) + list(value or [])
            base["keywords"] = sorted(set(str(item) for item in merged if item), key=str.lower)
        elif key in ("citationCount", "influentialCitationCount") and value is not None:
            base[key] = value
    provenance = _provenance(incoming)
    if provenance not in base.setdefault("sources", []):
        base["sources"].append(provenance)
    return base


def deduplicate(records: list[dict]) -> dict:
    seen: dict[tuple[str, str], dict] = {}
    duplicates = 0
    match_counts = {"doi": 0, "pmid": 0, "title": 0, "id": 0}
    for record in records:
        key = _record_key(record)
        match_counts[key[0]] = match_counts.get(key[0], 0) + 1
        if key in seen:
            duplicates += 1
            _merge_record(seen[key], record)
            continue
        copy = deepcopy(record)
        copy["doi"] = _norm_doi(copy.get("doi"))
        copy["pmid"] = _norm_pmid(copy.get("pmid"))
        copy["sources"] = [_provenance(record)]
        seen[key] = copy
    records_out = list(seen.values())
    return {
        "summary": {
            "input_records": len(records),
            "unique_records": len(records_out),
            "duplicates_removed": duplicates,
            "match_counts": match_counts,
        },
        "records": records_out,
    }


def _read_records(paths: list[str]) -> list[dict]:
    payloads: list[Any] = []
    if paths:
        for path in paths:
            payloads.append(json.loads(Path(path).read_text(encoding="utf-8")))
    else:
        payloads.append(json.load(sys.stdin))
    records: list[dict] = []
    for payload in payloads:
        if isinstance(payload, list):
            records.extend(payload)
        elif isinstance(payload, dict) and isinstance(payload.get("records"), list):
            records.extend(payload["records"])
        else:
            raise ValueError("Input must be a JSON list or an object with a records array")
    return records


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deduplicate records by DOI first, PMID second, normalized title third.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python deduplicate_records.py pubmed.json semantic.json crossref.json\n  python deduplicate_records.py < combined.json\n",
    )
    parser.add_argument("inputs", nargs="*", help="JSON files; reads stdin when omitted")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = deduplicate(_read_records(args.inputs))
    except Exception as exc:
        print(f"deduplicate_records.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
