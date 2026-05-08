#!/usr/bin/env python3
"""Extract transparent evidence signals from biomedical review records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."

SIGNAL_PATTERNS = {
    "population_signal": [r"adult", r"pediatric", r"patient", r"cohort", r"population", r"subgroup"],
    "intervention_signal": [r"drug", r"intervention", r"exposure", r"treatment", r"therapy", r"dose"],
    "comparator_signal": [r"placebo", r"comparator", r"control", r"standard of care", r"usual care"],
    "outcome_signal": [r"outcome", r"endpoint", r"efficacy", r"safety", r"mortality", r"response"],
    "study_design_signal": [r"randomi[sz]ed", r"trial", r"cohort", r"case-control", r"registry", r"meta-analysis"],
    "safety_signal": [r"adverse", r"toxicity", r"warning", r"serious adverse", r"risk"],
    "economic_signal": [r"cost", r"utility", r"qaly", r"budget impact", r"resource use"],
    "payer_signal": [r"coverage", r"formulary", r"payer", r"rebate", r"value dossier"],
    "regulatory_signal": [r"label", r"approval", r"regulatory", r"submission", r"benefit-risk"],
    "uncertainty_signal": [r"limitation", r"uncertain", r"bias", r"confounding", r"missing"],
    "validation_gap": [r"requires validation", r"further studies", r"not established", r"hypothesis"],
}


def _load_payload(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"records": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload


def _records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("records", "items", "evidence", "articles", "claims", "studies", "inputs"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _fixture_only(path: str, payload: dict[str, Any]) -> bool:
    return "evals/example" in path.replace("\\", "/") or bool(payload.get("fixture_only"))


def _text(row: dict[str, Any]) -> str:
    fields = (
        "title",
        "abstract",
        "full_text",
        "text",
        "summary",
        "claim",
        "finding",
        "rationale",
        "population",
        "intervention",
        "comparator",
        "outcomes",
        "parameter",
        "category",
        "value",
        "confidence",
    )
    return " ".join(str(row.get(field, "")) for field in fields)


def extract_signals(records: list[dict[str, Any]], fixture_only: bool = False) -> dict[str, Any]:
    rows = []
    for index, record in enumerate(records):
        text = _text(record)
        lower = text.lower()
        signals: dict[str, dict[str, Any]] = {}
        for signal, patterns in SIGNAL_PATTERNS.items():
            matched = [pattern for pattern in patterns if re.search(pattern, lower)]
            signals[signal] = {"present": bool(matched), "matched_patterns": matched}
        rows.append(
            {
                "record_id": str(record.get("record_id") or record.get("id") or record.get("pmid") or f"record-{index + 1}"),
                "source": record.get("source", ""),
                "signals": signals,
                "signal_count": sum(1 for value in signals.values() if value["present"]),
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
            "Signals require human review before scientific, payer, regulatory, or commercial use.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract transparent evidence signals from JSON records.")
    parser.add_argument("records_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload = _load_payload(args.records_json)
        result = extract_signals(_records(payload), _fixture_only(args.records_json, payload))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"evidence_signal_extraction.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
