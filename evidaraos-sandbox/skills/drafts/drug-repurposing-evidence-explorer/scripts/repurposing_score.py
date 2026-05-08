#!/usr/bin/env python3
"""Score repurposing candidates transparently."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


FIELDS = ["mechanistic_plausibility", "clinical_evidence", "safety_transfer", "unmet_need"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Score repurposing candidates.")
    parser.add_argument("candidates_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.candidates_json).read_text(encoding="utf-8"))
    candidates = payload if isinstance(payload, list) else payload.get("candidates", [])
    scored = []
    for item in candidates:
        parts = {field: float(item.get(field, 0)) for field in FIELDS}
        score = round(sum(parts.values()) / len(FIELDS), 4)
        scored.append(
            {
                "candidate": item.get("candidate", ""),
                "indication": item.get("indication", ""),
                "scores": parts,
                "final_score": score,
                "label": "Mechanistic hypothesis - requires clinical validation",
                "transparent_reasons": item.get("reasons", []),
            }
        )
    scored.sort(key=lambda row: row["final_score"], reverse=True)
    print(json.dumps({"ranked_candidates": scored}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

