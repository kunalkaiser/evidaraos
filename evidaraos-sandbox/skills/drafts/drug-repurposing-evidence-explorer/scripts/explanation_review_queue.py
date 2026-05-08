#!/usr/bin/env python3
"""Create a human review queue for repurposing explanations."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"items": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("ranked_candidate_paths", "evidence_path_summaries", "zero_shot_candidates", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def build_queue(items: list[dict[str, Any]], reviewer_id: str, fixture_only: bool) -> dict[str, Any]:
    queue = []
    now = datetime.now(timezone.utc).isoformat()
    for index, item in enumerate(items):
        candidate = item.get("candidate_pair") or item.get("drug") or f"candidate-{index + 1}"
        queue.append(
            {
                "review_item_id": f"explanation-{index + 1}",
                "candidate_pair": candidate,
                "ai_explanation": item.get("top_path") or item.get("evidence_paths") or item.get("ranked_paths", []),
                "review_dimensions": {
                    "mechanistic_plausibility": "pending",
                    "clinical_usefulness": "pending",
                    "safety_concern": "pending",
                    "missing_evidence": "pending",
                    "overclaim_risk": "pending",
                },
                "human_decision": "pending",
                "reviewer_id": reviewer_id,
                "timestamp": now,
                "notes": "",
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "review_queue": queue,
        "summary": {"items": len(queue), "human_review_required": True},
        "limitations": ["Explanation review evaluates usefulness and plausibility; it is not clinical validation."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an explanation review queue.")
    parser.add_argument("explanations_json")
    parser.add_argument("--reviewer-id", default="reviewer_001")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.explanations_json)
        result = build_queue(_items(payload), args.reviewer_id, fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"explanation_review_queue.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
