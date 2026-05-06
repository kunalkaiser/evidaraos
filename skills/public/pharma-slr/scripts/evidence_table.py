#!/usr/bin/env python3
"""Generate a markdown evidence table from extracted study records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

COLUMNS = [
    ("study", "Study"),
    ("disease", "Disease"),
    ("intervention_exposure", "Intervention/exposure"),
    ("comparator", "Comparator"),
    ("population", "Population"),
    ("sample_size", "Sample size"),
    ("country", "Country"),
    ("data_source", "Data source"),
    ("study_design", "Study design"),
    ("incidence", "Incidence"),
    ("prevalence", "Prevalence"),
    ("mortality", "Mortality"),
    ("safety_outcomes", "Safety outcomes"),
    ("efficacy_outcomes", "Efficacy outcomes"),
    ("follow_up", "Follow-up"),
    ("limitations", "Limitations"),
    ("citation", "Citation"),
    ("confidence", "Confidence"),
]


def _as_text(value: Any) -> str:
    if value is None or value == "":
        return "not reported"
    if isinstance(value, list):
        return "; ".join(str(item) for item in value if item) or "not reported"
    return " ".join(str(value).split())


def _escape_cell(value: Any) -> str:
    return _as_text(value).replace("|", "\\|").replace("\n", "<br>")


def _study_label(item: dict) -> str:
    if item.get("study"):
        return _as_text(item["study"])
    authors = item.get("authors") or []
    first_author = str(authors[0]).split(",")[0].strip() if authors else "Unknown"
    year = item.get("year") or item.get("publication_year") or ""
    title = item.get("title") or ""
    label = f"{first_author} et al. {year}".strip()
    return f"{label}: {title}" if title else label


def _normalise_item(item: dict) -> dict:
    citation_parts = []
    for key, label in [("pmid", "PMID"), ("doi", "DOI"), ("url", "URL")]:
        value = item.get(key) or (item.get("citation") or {}).get(key)
        if value:
            citation_parts.append(f"{label}: {value}")
    precision_score = item.get("precision_score") or {}
    return {
        "study": _study_label(item),
        "disease": item.get("disease") or item.get("condition"),
        "intervention_exposure": item.get("intervention_exposure")
        or item.get("intervention_or_exposure")
        or item.get("intervention")
        or item.get("exposure"),
        "comparator": item.get("comparator"),
        "population": item.get("population") or item.get("sample") or item.get("participants"),
        "sample_size": item.get("sample_size") or item.get("n") or item.get("enrollment"),
        "country": item.get("country") or item.get("geography"),
        "data_source": item.get("data_source") or item.get("journal") or item.get("source"),
        "study_design": item.get("study_design") or item.get("design"),
        "incidence": item.get("incidence"),
        "prevalence": item.get("prevalence"),
        "mortality": item.get("mortality"),
        "safety_outcomes": item.get("safety_outcomes") or item.get("safety_findings"),
        "efficacy_outcomes": item.get("efficacy_outcomes") or item.get("key_findings") or item.get("findings"),
        "follow_up": item.get("follow_up") or item.get("followup") or item.get("duration"),
        "limitations": item.get("limitations") or item.get("notes") or item.get("full_text_eligibility_notes"),
        "citation": "; ".join(citation_parts) if citation_parts else item.get("citation"),
        "confidence": item.get("confidence") or precision_score.get("confidence"),
    }


def build_evidence_table(items: list[dict]) -> dict:
    rows = [_normalise_item(item) for item in items]
    lines = [
        "| " + " | ".join(label for _, label in COLUMNS) + " |",
        "|" + "|".join("---" for _ in COLUMNS) + "|",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_escape_cell(row[key]) for key, _ in COLUMNS) + " |")
    return {"summary": {"input_items": len(items), "rows": len(rows)}, "markdown_table": "\n".join(lines)}


def _read_payload(path: str | None) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8")) if path else json.load(sys.stdin)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("extractions", "records", "items"):
            if isinstance(payload.get(key), list):
                return payload[key]
    raise ValueError("Input must be a JSON array or an object with an extractions, records, or items array")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a markdown evidence table from extracted study JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  python evidence_table.py included_extractions.json\n  python evidence_table.py < included_extractions.json\n",
    )
    parser.add_argument("input", nargs="?", help="JSON input file; reads stdin when omitted")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_evidence_table(_read_payload(args.input))
    except Exception as exc:
        print(f"evidence_table.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
