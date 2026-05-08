#!/usr/bin/env python3
"""Rank zero-shot repurposing candidates using graph paths and disease similarity."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str | None) -> tuple[dict[str, Any], bool]:
    if not path:
        return {}, False
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"items": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _items(payload: dict[str, Any], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def rank_zero_shot(candidate_payload: dict[str, Any], similarity_payload: dict[str, Any], fixture_only: bool) -> dict[str, Any]:
    candidates = _items(candidate_payload, ("scored_candidates", "candidate_links", "candidates", "items"))
    similar = _items(similarity_payload, ("similar_diseases", "items"))
    similarity_boost = sum(float(row.get("similarity_score", 0)) for row in similar[:3]) / max(1, min(3, len(similar)))
    rows = []
    for candidate in candidates:
        base = float(candidate.get("net_hypothesis_score") or candidate.get("link_prediction_score") or candidate.get("score") or 0)
        safety_penalty = float(candidate.get("contraindication_signal_score") or 0)
        zero_shot_score = round(max(0.0, min(1.0, (0.75 * base) + (0.25 * similarity_boost) - (0.2 * safety_penalty))), 4)
        rows.append(
            {
                **candidate,
                "zero_shot_hypothesis_score": zero_shot_score,
                "similar_disease_support_score": round(similarity_boost, 4),
                "zero_shot_rationale": [
                    "Candidate has graph-path support.",
                    "Similar disease support is included as a transparent boost.",
                    "Contraindication signal is subtracted when present.",
                ],
                "label": "Zero-shot hypothesis only - requires expert review and validation",
            }
        )
    rows.sort(key=lambda row: row["zero_shot_hypothesis_score"], reverse=True)
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "zero_shot_candidates": rows,
        "summary": {"candidates": len(rows), "similar_disease_support_score": round(similarity_boost, 4)},
        "method": "transparent_graph_path_similarity_ranker",
        "limitations": [
            "This is not TxGNN and does not reproduce TxGNN benchmark performance.",
            "Zero-shot scores are prioritization aids, not therapeutic probabilities.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank zero-shot repurposing candidates.")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--disease-similarity")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        candidates, cand_fixture = _load(args.candidates)
        similarity, sim_fixture = _load(args.disease_similarity)
        result = rank_zero_shot(candidates, similarity, cand_fixture or sim_fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"zero_shot_candidate_ranker.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
