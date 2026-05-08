#!/usr/bin/env python3
"""Build a transparent drug-repurposing knowledge graph from extracted relations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_payload(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"relations": payload, "fixture_only": False}
    return payload


def build_graph(relations: list[dict[str, Any]], fixture_only: bool = False) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edge_map: dict[tuple[str, str, str], dict[str, Any]] = {}
    for rel in relations:
        subj = str(rel.get("subject", ""))
        obj = str(rel.get("object", ""))
        pred = str(rel.get("predicate", "co_mentioned"))
        if not subj or not obj:
            continue
        nodes.setdefault(subj, {"id": subj, "label": subj, "type": rel.get("subject_type", "unknown"), "sources": []})
        nodes.setdefault(obj, {"id": obj, "label": obj, "type": rel.get("object_type", "unknown"), "sources": []})
        source = rel.get("source") or rel.get("record_id", "")
        if source:
            nodes[subj]["sources"].append(source)
            nodes[obj]["sources"].append(source)
        key = (subj, pred, obj)
        edge = edge_map.setdefault(
            key,
            {
                "source": subj,
                "target": obj,
                "predicate": pred,
                "evidence_records": [],
                "confidence": rel.get("confidence", "not_assessed"),
                "human_review_required": True,
            },
        )
        edge["evidence_records"].append(rel.get("record_id", ""))
    for node in nodes.values():
        node["sources"] = sorted(set(node["sources"]))
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "nodes": sorted(nodes.values(), key=lambda n: (n["type"], n["label"])),
        "edges": list(edge_map.values()),
        "summary": {
            "nodes": len(nodes),
            "edges": len(edge_map),
            "human_review_required": True,
        },
        "limitations": [
            "Graph edges represent extracted text evidence or co-mention signals, not validated biological causality.",
            "Drug-disease hypotheses require scientific and clinical review.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build drug-repurposing knowledge graph.")
    parser.add_argument("relations_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload = _load_payload(args.relations_json)
        fixture_only = bool(payload.get("fixture_only")) or "evals/example" in args.relations_json.replace("\\", "/")
        result = build_graph(payload.get("relations", []), fixture_only)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"knowledge_graph_builder.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
