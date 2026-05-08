#!/usr/bin/env python3
"""Find mechanistically similar diseases from transparent evidence features."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."
FEATURE_FIELDS = ("genes", "proteins", "pathways", "phenotypes", "exposures", "symptoms", "related_diseases")


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object")
    fixture = bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")
    return payload, fixture


def _items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("diseases", "items", "records"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    raise ValueError("input must contain diseases/items/records")


def _features(row: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for field in FEATURE_FIELDS:
        raw = row.get(field, [])
        if isinstance(raw, str):
            raw = [raw]
        if isinstance(raw, list):
            values.update(str(item).strip().lower() for item in raw if str(item).strip())
    return values


def _name(row: dict[str, Any]) -> str:
    return str(row.get("disease") or row.get("name") or row.get("id") or "")


def disease_similarity(payload: dict[str, Any], query: str | None, top_k: int, fixture_only: bool) -> dict[str, Any]:
    diseases = _items(payload)
    if query:
        query_row = next((row for row in diseases if _name(row).lower() == query.lower()), None)
        if not query_row:
            query_row = {"disease": query, **{field: payload.get(field, []) for field in FEATURE_FIELDS}}
    else:
        query_row = diseases[0]
    query_features = _features(query_row)
    scored = []
    for row in diseases:
        name = _name(row)
        if name.lower() == _name(query_row).lower():
            continue
        features = _features(row)
        shared = sorted(query_features & features)
        union = query_features | features
        score = round(len(shared) / len(union), 4) if union else 0.0
        scored.append(
            {
                "disease": name,
                "similarity_score": score,
                "shared_features": shared,
                "shared_feature_count": len(shared),
                "rationale": "Similarity is based on shared transparent features, not a learned embedding.",
            }
        )
    scored.sort(key=lambda row: (row["similarity_score"], row["shared_feature_count"]), reverse=True)
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "query_disease": _name(query_row),
        "query_features": sorted(query_features),
        "similar_diseases": scored[:top_k],
        "method": "transparent_feature_jaccard_similarity",
        "limitations": [
            "This is a deterministic similarity proxy, not a graph foundation model.",
            "Similar disease signals can suggest hypotheses but do not establish therapeutic transferability.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Find mechanistically similar diseases from feature JSON.")
    parser.add_argument("disease_features_json")
    parser.add_argument("--query-disease")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.disease_features_json)
        result = disease_similarity(payload, args.query_disease, args.top_k, fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"disease_similarity.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
