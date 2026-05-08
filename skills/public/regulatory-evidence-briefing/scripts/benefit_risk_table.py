#!/usr/bin/env python3
"""Build a conservative benefit-risk table from evidence rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build benefit-risk evidence table.")
    parser.add_argument("evidence_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
    evidence = payload if isinstance(payload, list) else payload.get("evidence", [])
    rows = []
    for item in evidence:
        rows.append(
            {
                "dimension": item.get("dimension", "benefit" if item.get("type") == "efficacy" else "risk"),
                "finding": item.get("finding", ""),
                "population": item.get("population", ""),
                "source": item.get("source", ""),
                "certainty": item.get("certainty", "not_assessed"),
                "regulatory_note": item.get("regulatory_note", "Requires regulatory review."),
            }
        )
    print(json.dumps({"benefit_risk_rows": rows, "human_review_required": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

