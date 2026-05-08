#!/usr/bin/env python3
"""Extract transparent drug-repurposing signals from article-like text records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SIGNAL_PATTERNS = {
    "mechanism_signal": [r"mechanism", r"pathway", r"target", r"inhibit", r"activate", r"receptor"],
    "clinical_signal": [r"trial", r"cohort", r"case-control", r"randomi[sz]ed", r"endpoint", r"efficacy"],
    "safety_signal": [r"adverse", r"safety", r"toxicity", r"contraindication", r"warning"],
    "population_signal": [r"adult", r"pediatric", r"older", r"population", r"patients"],
    "dose_signal": [r"dose", r"mg", r"administration", r"regimen"],
    "comparator_signal": [r"placebo", r"standard of care", r"comparator", r"control"],
    "validation_gap": [r"preclinical", r"in vitro", r"mouse", r"hypothesis", r"further studies"],
}

FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_records(path: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("records", "items", "articles", "evidence"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value
    raise ValueError(f"{path} must be a JSON array or contain records/items/articles/evidence")


def _fixture_only(path: str) -> bool:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return "evals/example" in path.replace("\\", "/") or bool(isinstance(payload, dict) and payload.get("fixture_only"))


def _text(row: dict[str, Any]) -> str:
    fields = ("title", "abstract", "full_text", "text", "tables", "results", "methods")
    return " ".join(str(row.get(field, "")) for field in fields)


def extract_signals(records: list[dict[str, Any]], fixture_only: bool = False) -> dict[str, Any]:
    rows = []
    for index, record in enumerate(records):
        text = _text(record)
        lower = text.lower()
        signals: dict[str, dict[str, Any]] = {}
        for signal, patterns in SIGNAL_PATTERNS.items():
            matched = []
            for pattern in patterns:
                if re.search(pattern, lower):
                    matched.append(pattern)
            signals[signal] = {"present": bool(matched), "matched_patterns": matched}
        readiness = sum(1 for value in signals.values() if value["present"])
        rows.append(
            {
                "record_id": str(record.get("record_id") or record.get("id") or f"record-{index + 1}"),
                "source": record.get("source", ""),
                "signals": signals,
                "signal_count": readiness,
                "human_review_required": True,
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "signal_extraction_method": "transparent_pattern_match",
        "records": rows,
        "summary": {"records": len(rows), "human_review_required": True},
        "limitations": [
            "Pattern matching is a triage aid and may miss context, negation, or table-specific meaning.",
            "Full-text and table extraction require source verification before evidence use.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract full-text/table-like repurposing signals from JSON records.")
    parser.add_argument("records_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = extract_signals(_load_records(args.records_json), _fixture_only(args.records_json))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"full_text_signal_extraction.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
