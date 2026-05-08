#!/usr/bin/env python3
"""Generate a validation plan for drug-repurposing hypotheses."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str | None) -> tuple[dict[str, Any], bool]:
    if not path:
        return {}, False
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"items": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _pairs(*payloads: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for payload in payloads:
        for key in ("candidate_signal_comparisons", "false_positive_risk_assessments", "false_negative_gap_assessments", "items"):
            for item in payload.get(key, []) or []:
                pair = item.get("candidate_pair")
                if pair and pair not in found:
                    found.append(pair)
    return found


def plan(comparison: dict[str, Any], fp: dict[str, Any], fn: dict[str, Any], fixture_only: bool) -> dict[str, Any]:
    pair_plans = []
    fp_by_pair = {row.get("candidate_pair"): row for row in fp.get("false_positive_risk_assessments", [])}
    fn_by_pair = {row.get("candidate_pair"): row for row in fn.get("false_negative_gap_assessments", [])}
    comparison_by_pair = {row.get("candidate_pair"): row for row in comparison.get("candidate_signal_comparisons", [])}
    for pair in _pairs(comparison, fp, fn):
        pair_plans.append(
            {
                "candidate_pair": pair,
                "current_signal_status": comparison_by_pair.get(pair, {}).get("consensus_status", "unknown"),
                "false_positive_risk_tier": fp_by_pair.get(pair, {}).get("risk_tier", "not_assessed"),
                "false_negative_gap_score": fn_by_pair.get(pair, {}).get("false_negative_gap_score", None),
                "validation_steps": [
                    "Verify primary sources and study designs.",
                    "Review mechanism directionality and target context.",
                    "Assess contraindication, adverse-event, and population transfer risk.",
                    "Run missing-method-family checks and citation recall expansion.",
                    "Define a human-labeled benchmark before reporting performance.",
                    "Document final expert decision, rationale, and audit trail.",
                ],
                "minimum_evidence_before_claim": [
                    "human-reviewed mechanism rationale",
                    "human-reviewed clinical or preclinical evidence table",
                    "safety-transfer review",
                    "validation metrics from non-fixture benchmark data",
                ],
                "allowed_language": "hypothesis prioritized for review",
                "disallowed_language": "validated treatment, proven indication, or clinical recommendation",
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "repurposing_validation_plan": pair_plans,
        "summary": {"candidate_pairs": len(pair_plans), "real_performance_claims_allowed": False},
        "limitations": [
            "A validation plan is not validation evidence.",
            "Do not make real performance claims without independent human-labeled benchmark data.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate repurposing validation plan.")
    parser.add_argument("--comparison", required=True)
    parser.add_argument("--false-positive")
    parser.add_argument("--false-negative")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        comparison, comp_fixture = _load(args.comparison)
        fp, fp_fixture = _load(args.false_positive)
        fn, fn_fixture = _load(args.false_negative)
        result = plan(comparison, fp, fn, comp_fixture or fp_fixture or fn_fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"repurposing_validation_plan.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
