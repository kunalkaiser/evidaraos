#!/usr/bin/env python3
"""Check payer dossier section and claim gaps."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_SECTIONS = [
    "executive_summary",
    "disease_burden",
    "unmet_need",
    "clinical_evidence",
    "safety_evidence",
    "comparator_landscape",
    "heor_evidence",
    "claim_traceability",
]


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check payer dossier gaps.")
    parser.add_argument("--scope", required=True)
    parser.add_argument("--claims")
    args = parser.parse_args()
    scope = _load(args.scope)
    sections = scope.get("sections", [])
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in sections]
    unsupported_claims = []
    if args.claims:
        claims_payload = _load(args.claims)
        for claim in claims_payload.get("claims", claims_payload if isinstance(claims_payload, list) else []):
            if not claim.get("sources"):
                unsupported_claims.append(claim.get("claim_id", claim.get("claim", "")))
    result = {
        "gap_summary": {
            "missing_required_sections": missing_sections,
            "unsupported_claim_count": len(unsupported_claims),
            "ready_for_human_review": not missing_sections and not unsupported_claims,
        },
        "unsupported_claims": unsupported_claims,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

