#!/usr/bin/env python3
"""Create a structured payer value dossier scope."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone


def main() -> int:
    parser = argparse.ArgumentParser(description="Create payer dossier scope JSON.")
    parser.add_argument("--product", required=True)
    parser.add_argument("--indication", required=True)
    parser.add_argument("--market", required=True)
    parser.add_argument("--comparator", default="")
    parser.add_argument("--submission-context", default="payer committee")
    args = parser.parse_args()
    result = {
        "dossier_scope": {
            "product": args.product,
            "indication": args.indication,
            "market": args.market,
            "comparator": args.comparator,
            "submission_context": args.submission_context,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "human_review_required": True,
        },
        "sections": [
            "executive_summary",
            "disease_burden",
            "unmet_need",
            "clinical_evidence",
            "safety_evidence",
            "comparator_landscape",
            "heor_evidence",
            "hta_precedents",
            "claim_traceability",
        ],
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

