#!/usr/bin/env python3
"""Create a structured regulatory briefing context."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone


def main() -> int:
    parser = argparse.ArgumentParser(description="Create regulatory context JSON.")
    parser.add_argument("--product", required=True)
    parser.add_argument("--indication", required=True)
    parser.add_argument("--agency", required=True, choices=["FDA", "EMA", "PMDA", "Health Canada", "multi-agency"])
    parser.add_argument("--stage", required=True)
    parser.add_argument("--submission-type", default="")
    args = parser.parse_args()
    result = {
        "regulatory_context": {
            "product": args.product,
            "indication": args.indication,
            "agency": args.agency,
            "stage": args.stage,
            "submission_type": args.submission_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "human_review_required": True,
        },
        "evidence_tasks": [
            "agency_precedents",
            "guidance_documents",
            "benefit_risk_table",
            "uncertainty_register",
            "source_appendix",
        ],
        "warnings": ["Do not predict approval outcomes.", "All output requires regulatory expert review."],
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

