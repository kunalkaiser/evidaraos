#!/usr/bin/env python3
"""Build an auditable evidence map from extracted evidence signals."""

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
        return {"records": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload


def build_map(payload: dict[str, Any], fixture_only: bool = False) -> dict[str, Any]:
    records = payload.get("records", [])
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    for row in records:
        record_id = str(row.get("record_id") or row.get("id") or "")
        if not record_id:
            continue
        nodes[record_id] = {"id": record_id, "label": record_id, "type": "record", "source": row.get("source", "")}
        for signal, detail in row.get("signals", {}).items():
            if not detail.get("present"):
                continue
            nodes.setdefault(signal, {"id": signal, "label": signal.replace("_", " "), "type": "evidence_signal"})
            edges.append(
                {
                    "source": record_id,
                    "target": signal,
                    "predicate": "contains_signal",
                    "matched_patterns": detail.get("matched_patterns", []),
                    "human_review_required": True,
                }
            )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "nodes": sorted(nodes.values(), key=lambda node: (node["type"], node["id"])),
        "edges": edges,
        "summary": {
            "records": sum(1 for node in nodes.values() if node["type"] == "record"),
            "signals": sum(1 for node in nodes.values() if node["type"] == "evidence_signal"),
            "edges": len(edges),
            "human_review_required": True,
        },
        "limitations": [
            "Evidence maps organize signals for review; they do not establish evidence quality by themselves.",
            "Source verification and domain expert review remain required.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build an auditable evidence map from signal extraction output.")
    parser.add_argument("signals_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload = _load_payload(args.signals_json)
        fixture_only = bool(payload.get("fixture_only")) or "evals/example" in args.signals_json.replace("\\", "/")
        result = build_map(payload, fixture_only)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"evidence_map_builder.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
