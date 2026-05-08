#!/usr/bin/env python3
"""Generate validation checklist for repurposing candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CHECKS = [
    "confirm_mechanism_in_target_population",
    "verify_primary_clinical_evidence",
    "review_safety_transfer",
    "check_drug_drug_interactions",
    "assess_regulatory_pathway",
    "confirm_unmet_need_and_comparator_landscape",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate repurposing validation checklist.")
    parser.add_argument("candidates_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.candidates_json).read_text(encoding="utf-8"))
    candidates = payload if isinstance(payload, list) else payload.get("candidates", [])
    rows = [{"candidate": item.get("candidate", ""), "indication": item.get("indication", ""), "checks": CHECKS, "status": "requires_scientific_review"} for item in candidates]
    print(json.dumps({"validation_checklists": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

