#!/usr/bin/env python3
"""Assess safety-transfer concerns for repurposing candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RISK_TERMS = ["immunosuppressed", "pediatric", "pregnancy", "elderly", "renal", "hepatic", "oncology"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess safety transfer for repurposing candidates.")
    parser.add_argument("candidates_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.candidates_json).read_text(encoding="utf-8"))
    candidates = payload if isinstance(payload, list) else payload.get("candidates", [])
    rows = []
    for item in candidates:
        text = " ".join(str(item.get(field, "")) for field in ["indication", "population", "safety_notes"]).lower()
        flags = [term for term in RISK_TERMS if term in text]
        base = float(item.get("safety_transfer", 0))
        status = "requires_safety_review" if flags or base < 0.5 else "safety_transfer_plausible_pending_review"
        rows.append(
            {
                "candidate": item.get("candidate", ""),
                "indication": item.get("indication", ""),
                "safety_transfer_score": base,
                "population_risk_flags": flags,
                "status": status,
            }
        )
    print(json.dumps({"safety_transfer_assessments": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

