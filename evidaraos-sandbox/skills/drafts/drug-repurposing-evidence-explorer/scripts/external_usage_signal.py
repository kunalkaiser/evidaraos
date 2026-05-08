#!/usr/bin/env python3
"""Attach optional external usage signals to repurposing candidates."""

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


def _items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("zero_shot_candidates", "scored_candidates", "candidate_links", "items", "signals"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _pair(row: dict[str, Any]) -> str:
    return str(row.get("candidate_pair") or f"{row.get('drug', '')} -> {row.get('disease', '')}").lower()


def attach_usage(candidates: list[dict[str, Any]], signals: list[dict[str, Any]], fixture_only: bool) -> dict[str, Any]:
    signal_by_pair = {_pair(row): row for row in signals}
    rows = []
    for candidate in candidates:
        signal = signal_by_pair.get(_pair(candidate), {})
        usage_score = signal.get("usage_signal_score")
        rows.append(
            {
                **candidate,
                "external_usage_signal": {
                    "available": usage_score is not None,
                    "usage_signal_score": usage_score,
                    "source": signal.get("source", ""),
                    "interpretation": signal.get("interpretation", "not provided"),
                    "limitations": signal.get("limitations", ["External usage signals are optional and can be confounded."]),
                },
                "real_world_validation_status": "not_available" if usage_score is None else "signal_attached_requires_review",
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "candidates_with_usage_signal": rows,
        "summary": {
            "candidates": len(rows),
            "signals_attached": sum(1 for row in rows if row["external_usage_signal"]["available"]),
        },
        "limitations": [
            "External usage signals are not causal evidence and can reflect confounding, channeling bias, or disease severity.",
            "Do not claim real-world validation unless the data source, cohort design, and analysis are reviewed.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Attach optional external usage signals to candidates.")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--usage-signals")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        candidates_payload, cand_fixture = _load(args.candidates)
        signals_payload, sig_fixture = _load(args.usage_signals)
        result = attach_usage(_items(candidates_payload), _items(signals_payload), cand_fixture or sig_fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"external_usage_signal.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
