#!/usr/bin/env python3
"""Check false-negative risk by identifying missing method coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."
EXPECTED_METHOD_FAMILIES = {
    "knowledge_graph",
    "network_medicine",
    "omics_signature",
    "target_biology",
    "literature_and_trials",
    "real_world_data",
}


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"evidence_matrix": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def check_gaps(matrix_payload: dict[str, Any], fixture_only: bool) -> dict[str, Any]:
    rows = matrix_payload.get("evidence_matrix") or matrix_payload.get("items") or []
    gap_rows = []
    for row in rows:
        families = {str(signal.get("method_family", "")) for signal in row.get("method_signals", [])}
        missing = sorted(EXPECTED_METHOD_FAMILIES - families)
        unavailable = [signal.get("method_family", "unknown") for signal in row.get("method_signals", []) if signal.get("direction") in {"unavailable", "unknown"}]
        gap_score = round(min(1.0, (len(missing) / len(EXPECTED_METHOD_FAMILIES)) + (0.05 * len(unavailable))), 4)
        gap_rows.append(
            {
                "candidate_pair": f"{row.get('drug', '')} -> {row.get('disease', '')}",
                "false_negative_gap_score": gap_score,
                "missing_method_families": missing,
                "unavailable_method_families": sorted(set(unavailable)),
                "recall_actions": [
                    "expand synonyms and disease terms",
                    "run orthogonal method families where data exist",
                    "check negative and terminated studies",
                    "review citation trails and related mechanisms",
                ],
                "human_review_required": True,
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "false_negative_gap_assessments": gap_rows,
        "summary": {"candidates": len(gap_rows), "expected_method_families": sorted(EXPECTED_METHOD_FAMILIES)},
        "limitations": ["Missing method coverage can indicate missed opportunities, but it does not prove a false negative."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check false-negative risk and method coverage gaps.")
    parser.add_argument("evidence_matrix_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.evidence_matrix_json)
        result = check_gaps(payload, fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"false_negative_gap_checker.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
