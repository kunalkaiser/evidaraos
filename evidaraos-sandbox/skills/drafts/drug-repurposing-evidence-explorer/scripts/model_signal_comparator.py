#!/usr/bin/env python3
"""Compare candidate support across repurposing method families."""

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
        payload = {"evidence_matrix": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def compare(matrix_payload: dict[str, Any], fixture_only: bool) -> dict[str, Any]:
    rows = matrix_payload.get("evidence_matrix") or matrix_payload.get("items") or []
    comparisons = []
    for row in rows:
        signals = row.get("method_signals", [])
        supportive = [s for s in signals if s.get("direction") == "supportive"]
        conflicting = [s for s in signals if s.get("direction") == "conflicting"]
        unavailable = [s for s in signals if s.get("direction") in {"unavailable", "unknown"}]
        method_count = len(signals)
        support_ratio = round(len(supportive) / max(1, method_count), 4)
        conflict_ratio = round(len(conflicting) / max(1, method_count), 4)
        if len(supportive) >= 3 and not conflicting:
            consensus = "multi_method_support"
        elif supportive and conflicting:
            consensus = "mixed_signal"
        elif supportive:
            consensus = "single_or_limited_method_support"
        else:
            consensus = "insufficient_method_support"
        comparisons.append(
            {
                "drug": row.get("drug", ""),
                "disease": row.get("disease", ""),
                "candidate_pair": f"{row.get('drug', '')} -> {row.get('disease', '')}",
                "consensus_status": consensus,
                "support_ratio": support_ratio,
                "conflict_ratio": conflict_ratio,
                "supportive_methods": [s.get("method_id", "unknown") for s in supportive],
                "conflicting_methods": [s.get("method_id", "unknown") for s in conflicting],
                "unavailable_methods": [s.get("method_id", "unknown") for s in unavailable],
                "human_review_required": True,
                "interpretation": "Prioritize for expert review; do not treat method agreement as clinical proof.",
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "candidate_signal_comparisons": comparisons,
        "summary": {
            "candidates": len(comparisons),
            "multi_method_support": sum(1 for item in comparisons if item["consensus_status"] == "multi_method_support"),
            "mixed_signal": sum(1 for item in comparisons if item["consensus_status"] == "mixed_signal"),
        },
        "limitations": ["Model-signal comparison is a governance artifact, not a therapeutic recommendation."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare repurposing method signals.")
    parser.add_argument("evidence_matrix_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.evidence_matrix_json)
        result = compare(payload, fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"model_signal_comparator.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
