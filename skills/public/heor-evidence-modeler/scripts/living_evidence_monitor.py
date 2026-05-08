#!/usr/bin/env python3
"""Compare evidence-map snapshots for living evidence review."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str | None) -> tuple[dict[str, Any], bool]:
    if not path:
        return {}, False
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _edge_key(edge: dict[str, Any]) -> str:
    return f"{edge.get('source')}|{edge.get('predicate')}|{edge.get('target')}"


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def compare(previous: dict[str, Any], current: dict[str, Any], fixture_only: bool = False) -> dict[str, Any]:
    prev_edges = {_edge_key(edge): edge for edge in previous.get("edges", [])}
    cur_edges = {_edge_key(edge): edge for edge in current.get("edges", [])}
    added = sorted(set(cur_edges) - set(prev_edges))
    removed = sorted(set(prev_edges) - set(cur_edges))
    changed = []
    for key in sorted(set(cur_edges) & set(prev_edges)):
        if _hash(cur_edges[key]) != _hash(prev_edges[key]):
            changed.append({"edge": key, "previous_hash": _hash(prev_edges[key]), "current_hash": _hash(cur_edges[key])})
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "new_evidence_paths": [cur_edges[key] for key in added],
        "removed_evidence_paths": [prev_edges[key] for key in removed],
        "changed_evidence_paths": changed,
        "summary": {
            "previous_paths": len(prev_edges),
            "current_paths": len(cur_edges),
            "new_paths": len(added),
            "removed_paths": len(removed),
            "changed_paths": len(changed),
            "human_review_required": len(added) + len(removed) + len(changed),
        },
        "limitations": ["Living monitoring flags map changes; it does not validate scientific meaning."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare previous and current evidence-map snapshots.")
    parser.add_argument("--previous")
    parser.add_argument("--current", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        previous, previous_fixture = _load(args.previous)
        current, current_fixture = _load(args.current)
        result = compare(previous, current, previous_fixture or current_fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"living_evidence_monitor.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
