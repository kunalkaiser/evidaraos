#!/usr/bin/env python3
"""Compare repurposing evidence snapshots for living-review updates."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str | None) -> tuple[list[dict[str, Any]], bool]:
    if not path:
        return [], False
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    fixture = "evals/example" in path.replace("\\", "/")
    if isinstance(payload, dict):
        fixture = fixture or bool(payload.get("fixture_only"))
        for key in ("candidate_links", "candidates", "items", "records"):
            if isinstance(payload.get(key), list):
                return payload[key], fixture
    if isinstance(payload, list):
        return payload, fixture
    raise ValueError(f"{path} must be a JSON array or contain candidate_links/candidates/items/records")


def _key(row: dict[str, Any]) -> str:
    if row.get("candidate_pair"):
        return str(row["candidate_pair"]).lower()
    drug = str(row.get("drug") or row.get("compound") or "").lower()
    disease = str(row.get("disease") or row.get("indication") or "").lower()
    if drug or disease:
        return f"{drug}->{disease}"
    return str(row.get("id") or row.get("record_id") or row)


def _score(row: dict[str, Any]) -> float:
    for field in ("link_prediction_score", "repurposing_score", "score", "final_score"):
        value = row.get(field)
        if isinstance(value, (int, float)):
            return float(value)
    return 0.0


def compare_snapshots(previous: list[dict[str, Any]], current: list[dict[str, Any]], fixture_only: bool) -> dict[str, Any]:
    prev = {_key(row): row for row in previous}
    cur = {_key(row): row for row in current}
    new_keys = sorted(set(cur) - set(prev))
    removed_keys = sorted(set(prev) - set(cur))
    changed = []
    for key in sorted(set(cur) & set(prev)):
        delta = round(_score(cur[key]) - _score(prev[key]), 4)
        if abs(delta) >= 0.05:
            changed.append(
                {
                    "candidate_pair": cur[key].get("candidate_pair") or key,
                    "previous_score": _score(prev[key]),
                    "current_score": _score(cur[key]),
                    "delta": delta,
                    "review_priority": "high" if abs(delta) >= 0.2 else "standard",
                }
            )
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "new_candidates": [cur[key] for key in new_keys],
        "removed_candidates": [prev[key] for key in removed_keys],
        "score_changes": changed,
        "summary": {
            "previous_candidates": len(prev),
            "current_candidates": len(cur),
            "new_candidates": len(new_keys),
            "removed_candidates": len(removed_keys),
            "score_changes": len(changed),
            "human_review_required": len(new_keys) + len(removed_keys) + len(changed),
        },
        "limitations": [
            "Living evidence monitoring flags changes; it does not validate therapeutic utility.",
            "New or changed candidates require human review and source verification.",
        ],
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare previous and current repurposing evidence snapshots.")
    parser.add_argument("--previous")
    parser.add_argument("--current", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        previous, previous_fixture = _load(args.previous)
        current, current_fixture = _load(args.current)
        result = compare_snapshots(previous, current, previous_fixture or current_fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"living_evidence_monitor.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
