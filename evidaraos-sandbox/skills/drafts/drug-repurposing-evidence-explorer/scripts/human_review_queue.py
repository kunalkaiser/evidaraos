#!/usr/bin/env python3
"""Create a generic EvidaraOS human review queue."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _load_items(path: str) -> tuple[list[dict[str, Any]], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    fixture_only = "evals/example" in path.replace("\\", "/") or bool(payload.get("fixture_only") if isinstance(payload, dict) else False)
    if isinstance(payload, list):
        return payload, fixture_only
    for key in ("records", "items", "claims", "inputs", "evidence", "candidates", "model_inputs", "ranked_candidates", "benefit_risk_rows"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value, fixture_only
    raise ValueError(f"{path} must be a JSON array or contain a supported item list")


def _item_id(item: dict[str, Any], index: int) -> str:
    return str(
        item.get("record_id")
        or item.get("claim_id")
        or item.get("parameter")
        or item.get("candidate")
        or item.get("id")
        or f"item-{index + 1}"
    )


def build_queue(items: list[dict[str, Any]], module: str, reviewer_id: str, fixture_only: bool = False) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    queue = []
    for index, item in enumerate(items):
        risk_flags = []
        if item.get("traceable") is False or item.get("review_status") in {"unsupported_requires_revision", "needs_health_economist_review"}:
            risk_flags.append("source_or_review_gap")
        if item.get("requires_assumption") is True:
            risk_flags.append("assumption_required")
        if item.get("status") in {"revise", "requires_safety_review"}:
            risk_flags.append("requires_revision")
        queue.append(
            {
                "module": module,
                "item_id": _item_id(item, index),
                "ai_decision": item.get("status") or item.get("review_status") or "needs_human_review",
                "human_decision": "",
                "second_review_needed": bool(risk_flags),
                "rationale": item.get("rationale") or item.get("review_note") or "",
                "risk_flags": risk_flags,
                "confidence": item.get("confidence") or item.get("readiness_score") or item.get("final_score") or "not_assessed",
                "reviewer_id": reviewer_id,
                "notes": "",
                "timestamp": now,
                "source_item": item,
            }
        )
    markdown = ["| Item | AI decision | Risk flags | Confidence | Human decision | Reviewer |", "|---|---|---|---|---|---|"]
    for row in queue:
        markdown.append(
            f"| {row['item_id']} | {row['ai_decision']} | {', '.join(row['risk_flags']) or 'none'} | {row['confidence']} | {row['human_decision']} | {row['reviewer_id']} |"
        )
    return {
        "summary": {
            "module": module,
            "items": len(queue),
            "second_review_needed": sum(1 for row in queue if row["second_review_needed"]),
            "generated_at": now,
            "fixture_only": fixture_only,
            "fixture_warning": "These results are from sample fixture data and are not validation evidence." if fixture_only else "",
        },
        "fixture_only": fixture_only,
        "review_queue": queue,
        "markdown_queue": "\n".join(markdown),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create EvidaraOS human review queue.")
    parser.add_argument("items_json")
    parser.add_argument("--module", required=True)
    parser.add_argument("--reviewer-id", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        items, fixture_only = _load_items(args.items_json)
        result = build_queue(items, args.module, args.reviewer_id, fixture_only)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"human_review_queue.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
