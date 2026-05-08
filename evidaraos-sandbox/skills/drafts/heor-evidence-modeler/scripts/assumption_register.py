#!/usr/bin/env python3
"""Create an HEOR assumption register from missing or weak model inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an assumption register.")
    parser.add_argument("input_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    items = payload if isinstance(payload, list) else payload.get("inputs", [])
    assumptions = []
    for item in items:
        if not item.get("source") or item.get("value") in ("", None):
            assumptions.append(
                {
                    "parameter": item.get("parameter", ""),
                    "reason": "missing_source_or_value",
                    "proposed_handling": "health_economist_to_validate_or_replace",
                    "sensitivity_analysis_required": True,
                }
            )
    print(json.dumps({"assumptions": assumptions, "count": len(assumptions)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

