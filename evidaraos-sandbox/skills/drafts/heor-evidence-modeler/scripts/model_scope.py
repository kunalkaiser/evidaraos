#!/usr/bin/env python3
"""Create a structured HEOR model scope."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone


def build_scope(args: argparse.Namespace) -> dict:
    return {
        "model_scope": {
            "condition": args.condition,
            "intervention": args.intervention,
            "comparator": args.comparator,
            "perspective": args.perspective,
            "market": args.market,
            "time_horizon": args.time_horizon,
            "model_type": args.model_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "human_review_required": True,
        },
        "evidence_needs": [
            "health_state_utilities",
            "event_rates",
            "resource_utilization",
            "cost_inputs",
            "treatment_discontinuation",
            "adverse_event_disutilities",
            "uncertainty_ranges",
        ],
        "warnings": [
            "Model inputs are candidates for health economist review, not final economic results.",
            "Missing values must be labeled as assumptions rather than invented.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a HEOR model scope JSON.")
    parser.add_argument("--condition", required=True)
    parser.add_argument("--intervention", required=True)
    parser.add_argument("--comparator", default="")
    parser.add_argument("--perspective", required=True)
    parser.add_argument("--market", default="US")
    parser.add_argument("--time-horizon", default="not specified")
    parser.add_argument("--model-type", default="cost-effectiveness")
    args = parser.parse_args()
    print(json.dumps(build_scope(args), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

