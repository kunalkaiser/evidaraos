#!/usr/bin/env python3
"""Generate transparent drug-disease repurposing candidates from graph paths."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


DRUG_TYPES = {"drug"}
DISEASE_TYPES = {"disease"}
PREDICATE_WEIGHT = {
    "treats": 1.0,
    "inhibits": 0.75,
    "activates": 0.55,
    "associated_with": 0.45,
    "biomarker_of": 0.35,
    "adverse_event_of": -0.3,
    "co_mentioned": 0.15,
}

FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_graph(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def predict_links(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in graph.get("nodes", [])}
    adjacency: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph.get("edges", []):
        adjacency[edge["source"]].append(edge)
        adjacency[edge["target"]].append({**edge, "source": edge["target"], "target": edge["source"], "predicate": edge["predicate"]})
    candidates = []
    drugs = [node for node in nodes.values() if node.get("type") in DRUG_TYPES]
    diseases = [node for node in nodes.values() if node.get("type") in DISEASE_TYPES]
    for drug in drugs:
        for disease in diseases:
            if drug["id"] == disease["id"]:
                continue
            direct_edges = [edge for edge in adjacency[drug["id"]] if edge["target"] == disease["id"]]
            two_hop_paths = []
            for first in adjacency[drug["id"]]:
                mid = first["target"]
                for second in adjacency[mid]:
                    if second["target"] == disease["id"]:
                        two_hop_paths.append([first, second])
            support = 0.0
            evidence_paths = []
            for edge in direct_edges:
                support += PREDICATE_WEIGHT.get(edge["predicate"], 0.1)
                evidence_paths.append([edge["source"], edge["predicate"], edge["target"]])
            for path in two_hop_paths:
                support += sum(PREDICATE_WEIGHT.get(edge["predicate"], 0.1) for edge in path) / 2
                evidence_paths.append([path[0]["source"], path[0]["predicate"], path[0]["target"], path[1]["predicate"], path[1]["target"]])
            if evidence_paths:
                score = round(max(0.0, min(1.0, support / max(1, len(evidence_paths)))), 4)
                candidates.append(
                    {
                        "drug": drug["id"],
                        "disease": disease["id"],
                        "candidate_pair": f"{drug['id']} -> {disease['id']}",
                        "link_prediction_score": score,
                        "evidence_paths": evidence_paths,
                        "missing_evidence": [
                            "prospective clinical validation",
                            "population-specific safety review",
                            "dose and comparator context",
                        ],
                        "label": "Mechanistic hypothesis - requires clinical validation",
                        "human_review_required": True,
                    }
                )
    candidates.sort(key=lambda row: row["link_prediction_score"], reverse=True)
    fixture_only = bool(graph.get("fixture_only"))
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "candidate_links": candidates,
        "summary": {"candidates": len(candidates)},
        "method": "transparent_graph_path_scoring",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Predict drug-disease repurposing links from graph paths.")
    parser.add_argument("graph_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = predict_links(_load_graph(args.graph_json))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"repurposing_link_prediction.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
