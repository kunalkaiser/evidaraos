#!/usr/bin/env python3
"""Rank multi-hop evidence paths for repurposing explanation review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."
PREDICATE_WEIGHT = {
    "treats": 1.0,
    "inhibits": 0.8,
    "activates": 0.65,
    "associated_with": 0.5,
    "biomarker_of": 0.45,
    "adverse_event_of": 0.35,
    "co_mentioned": 0.1,
}


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"candidate_links": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _candidates(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("candidate_links", "scored_candidates", "candidates", "items"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _predicates(path: list[Any]) -> list[str]:
    return [str(path[index]) for index in range(1, len(path), 2)]


def rank_paths(candidates: list[dict[str, Any]], fixture_only: bool = False) -> dict[str, Any]:
    ranked_candidates = []
    for candidate in candidates:
        ranked_paths = []
        for path in candidate.get("evidence_paths", []):
            if not isinstance(path, list):
                continue
            predicates = _predicates(path)
            hop_count = max(1, len(predicates))
            raw = sum(PREDICATE_WEIGHT.get(predicate, 0.1) for predicate in predicates)
            path_score = round(raw / hop_count, 4)
            ranked_paths.append(
                {
                    "path": path,
                    "path_text": " -> ".join(map(str, path)),
                    "path_score": path_score,
                    "hop_count": hop_count,
                    "predicates": predicates,
                    "review_focus": "safety" if "adverse_event_of" in predicates else "mechanism",
                }
            )
        ranked_paths.sort(key=lambda row: row["path_score"], reverse=True)
        ranked_candidates.append(
            {
                "candidate_pair": candidate.get("candidate_pair"),
                "ranked_paths": ranked_paths,
                "top_path": ranked_paths[0] if ranked_paths else {},
                "human_review_required": True,
            }
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "ranked_candidate_paths": ranked_candidates,
        "summary": {"candidates": len(ranked_candidates), "human_review_required": True},
        "method": "transparent_predicate_weighted_path_ranking",
        "limitations": [
            "Path ranking highlights explanation candidates; it does not prove model faithfulness or causality.",
            "Path importance requires human review and source-level verification.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank multi-hop evidence paths for explanation review.")
    parser.add_argument("candidate_links_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.candidate_links_json)
        result = rank_paths(_candidates(payload), fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"multi_hop_path_ranker.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
