#!/usr/bin/env python3
"""Flag overconfident regulatory language."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

RISKY_TERMS = ["will be approved", "guarantees", "proves safety", "proves efficacy", "no risk", "certain approval"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check regulatory language for overclaims.")
    parser.add_argument("claims_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.claims_json).read_text(encoding="utf-8"))
    claims = payload if isinstance(payload, list) else payload.get("claims", [])
    findings = []
    for claim in claims:
        text = str(claim.get("claim", ""))
        lower = text.lower()
        hits = [term for term in RISKY_TERMS if term in lower]
        findings.append(
            {
                "claim_id": claim.get("claim_id", ""),
                "claim": text,
                "overclaim_terms": hits,
                "status": "revise" if hits else "acceptable_for_human_review",
            }
        )
    print(json.dumps({"language_findings": findings}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

