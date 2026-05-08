#!/usr/bin/env python3
"""Build a target-disease evidence matrix for repurposing review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_TYPE_WEIGHTS = {
    "genetic_association": 1.0,
    "known_drug": 0.9,
    "clinical_evidence": 0.9,
    "animal_model": 0.5,
    "pathway": 0.4,
    "literature": 0.4,
    "expression": 0.3,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create target-disease evidence matrix.")
    parser.add_argument("evidence_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.evidence_json).read_text(encoding="utf-8"))
    evidence = payload if isinstance(payload, list) else payload.get("target_evidence", payload.get("evidence", []))
    rows = []
    for item in evidence:
        data_type = str(item.get("data_type", "literature"))
        raw_score = float(item.get("score", 0))
        weight = DATA_TYPE_WEIGHTS.get(data_type, 0.25)
        rows.append(
            {
                "target": item.get("target", ""),
                "disease": item.get("disease", ""),
                "data_type": data_type,
                "source": item.get("source", ""),
                "weighted_score": round(min(1.0, raw_score * weight), 4),
                "directionality": item.get("directionality", "unknown"),
                "review_note": "Association evidence only; does not establish therapeutic benefit.",
            }
        )
    rows.sort(key=lambda row: row["weighted_score"], reverse=True)
    print(json.dumps({"target_evidence_matrix": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

