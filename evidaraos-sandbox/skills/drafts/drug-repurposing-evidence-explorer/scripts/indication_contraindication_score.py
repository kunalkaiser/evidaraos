#!/usr/bin/env python3
"""Separate indication and contraindication signals for repurposing candidates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."
INDICATION_PREDICATES = {"treats", "inhibits", "activates", "associated_with", "biomarker_of"}
CONTRAINDICATION_PREDICATES = {"adverse_event_of", "toxicity", "contraindicated_with", "safety_risk"}


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"candidate_links": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("candidate_links", "candidates", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _path_predicates(path: Any) -> list[str]:
    if not isinstance(path, list):
        return []
    return [str(path[index]) for index in range(1, len(path), 2)]


def score_candidates(candidates: list[dict[str, Any]], fixture_only: bool = False) -> dict[str, Any]:
    rows = []
    for candidate in candidates:
        indication_support = 0.0
        contraindication_support = 0.0
        indication_reasons = []
        contraindication_reasons = []
        for path in candidate.get("evidence_paths", []):
            predicates = _path_predicates(path)
            if any(predicate in INDICATION_PREDICATES for predicate in predicates):
                indication_support += 1
                indication_reasons.append(" -> ".join(map(str, path)))
            if any(predicate in CONTRAINDICATION_PREDICATES for predicate in predicates):
                contraindication_support += 1
                contraindication_reasons.append(" -> ".join(map(str, path)))
        total_paths = max(1, len(candidate.get("evidence_paths", [])))
        indication_score = round(indication_support / total_paths, 4)
        contraindication_score = round(contraindication_support / total_paths, 4)
        net_score = round(max(0.0, indication_score - contraindication_score), 4)
        rows.append(
            {
                **candidate,
                "indication_signal_score": indication_score,
                "contraindication_signal_score": contraindication_score,
                "net_hypothesis_score": net_score,
                "indication_reasons": indication_reasons,
                "contraindication_reasons": contraindication_reasons,
                "safety_review_required": contraindication_score > 0,
                "label": "Hypothesis only - indication and contraindication signals require expert review",
            }
        )
    rows.sort(key=lambda row: (row["net_hypothesis_score"], row.get("link_prediction_score", 0)), reverse=True)
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "scored_candidates": rows,
        "summary": {
            "candidates": len(rows),
            "safety_review_required": sum(1 for row in rows if row["safety_review_required"]),
        },
        "method": "transparent_path_predicate_signal_separation",
        "limitations": [
            "Scores are transparent triage signals, not model-calibrated probabilities.",
            "Contraindication signals require expert safety review and source verification.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score indication and contraindication signals.")
    parser.add_argument("candidate_links_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.candidate_links_json)
        result = score_candidates(_candidates(payload), fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"indication_contraindication_score.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
