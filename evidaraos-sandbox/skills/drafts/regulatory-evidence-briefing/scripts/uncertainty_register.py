#!/usr/bin/env python3
"""Create a regulatory uncertainty register from evidence rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


UNCERTAIN_MARKERS = {"not_assessed", "low", "unclear", "limited", ""}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create regulatory uncertainty register.")
    parser.add_argument("evidence_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
    evidence = payload if isinstance(payload, list) else payload.get("evidence", [])
    uncertainties = []
    for item in evidence:
        certainty = str(item.get("certainty", "")).lower()
        if certainty in UNCERTAIN_MARKERS or not item.get("source"):
            uncertainties.append(
                {
                    "finding": item.get("finding", ""),
                    "dimension": item.get("dimension", ""),
                    "reason": "limited_certainty_or_missing_source",
                    "proposed_follow_up": "regulatory reviewer to confirm evidence strength and source applicability",
                }
            )
    print(json.dumps({"uncertainties": uncertainties, "count": len(uncertainties)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

