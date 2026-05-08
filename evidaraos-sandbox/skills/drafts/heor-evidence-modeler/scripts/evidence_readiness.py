#!/usr/bin/env python3
"""Score HEOR model inputs for evidence readiness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_BY_CATEGORY = {
    "utility": ["parameter", "value", "population", "source", "range_low", "range_high"],
    "event_rate": ["parameter", "value", "population", "source"],
    "cost": ["parameter", "value", "population", "source"],
    "resource_use": ["parameter", "value", "population", "source"],
}


def _items(path: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, list) else payload.get("inputs", [])


def score_item(item: dict[str, Any]) -> dict[str, Any]:
    category = str(item.get("category") or "unspecified")
    required = REQUIRED_BY_CATEGORY.get(category, ["parameter", "value", "source"])
    missing = [field for field in required if item.get(field) in ("", None, [])]
    score = max(0.0, 1.0 - (len(missing) / len(required)))
    if item.get("confidence") == "high":
        score = min(1.0, score + 0.05)
    if not item.get("source"):
        score = min(score, 0.4)
    return {
        "parameter": item.get("parameter", ""),
        "category": category,
        "readiness_score": round(score, 4),
        "missing_fields": missing,
        "ready_for_modeler_review": score >= 0.75,
        "requires_assumption": bool(missing),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score HEOR input evidence readiness.")
    parser.add_argument("input_json")
    args = parser.parse_args()
    rows = [score_item(item) for item in _items(args.input_json)]
    summary = {
        "total": len(rows),
        "ready_for_modeler_review": sum(1 for row in rows if row["ready_for_modeler_review"]),
        "requires_assumption": sum(1 for row in rows if row["requires_assumption"]),
    }
    print(json.dumps({"summary": summary, "readiness": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

