#!/usr/bin/env python3
"""Assess false-positive risk for repurposing hypotheses."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"candidate_signal_comparisons": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def assess(comparison_payload: dict[str, Any], fixture_only: bool) -> dict[str, Any]:
    comparisons = comparison_payload.get("candidate_signal_comparisons") or comparison_payload.get("items") or []
    rows = []
    for item in comparisons:
        conflict = float(item.get("conflict_ratio", 0))
        support = float(item.get("support_ratio", 0))
        unavailable_count = len(item.get("unavailable_methods", []))
        risk_score = round(max(0.0, min(1.0, (0.45 * conflict) + (0.25 * (1 - support)) + (0.08 * unavailable_count))), 4)
        if risk_score >= 0.65:
            tier = "high"
        elif risk_score >= 0.35:
            tier = "moderate"
        else:
            tier = "lower_but_not_absent"
        drivers = [
            "conflicting method signals" if conflict else "",
            "limited cross-method support" if support < 0.5 else "",
            "unavailable method families" if unavailable_count else "",
            "clinical efficacy not established by computational signal",
        ]
        rows.append(
            {
                "candidate_pair": item.get("candidate_pair", ""),
                "false_positive_risk_score": risk_score,
                "risk_tier": tier,
                "drivers": [driver for driver in drivers if driver],
                "required_controls": [
                    "safety transfer assessment",
                    "expert mechanism review",
                    "primary evidence verification",
                    "do not present as therapy recommendation",
                ],
                "human_review_required": True,
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "false_positive_risk_assessments": rows,
        "summary": {"candidates": len(rows), "high_risk": sum(1 for row in rows if row["risk_tier"] == "high")},
        "limitations": ["Risk tiers are transparent governance heuristics, not calibrated error probabilities."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess false-positive risk for repurposing candidates.")
    parser.add_argument("comparison_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.comparison_json)
        result = assess(payload, fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"false_positive_risk_assessor.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
