#!/usr/bin/env python3
"""Explain evidence-map paths for reviewer-facing traceability."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_map(path: str) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be an evidence map JSON object")
    return payload


def explain_paths(evidence_map: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in evidence_map.get("nodes", [])}
    explanations = []
    for edge in evidence_map.get("edges", []):
        source = nodes.get(edge.get("source"), {})
        target = nodes.get(edge.get("target"), {})
        explanations.append(
            {
                "record_id": edge.get("source"),
                "signal": edge.get("target"),
                "path": f"{source.get('label', edge.get('source'))} -> {edge.get('predicate')} -> {target.get('label', edge.get('target'))}",
                "matched_patterns": edge.get("matched_patterns", []),
                "plain_language_rationale": "This record was flagged because its text matched one or more transparent evidence-signal patterns.",
                "human_review_required": True,
            }
        )
    markdown = ["# Evidence Path Summary", ""]
    for row in explanations:
        markdown.extend(
            [
                f"## {row['record_id']} -> {row['signal']}",
                "",
                f"- Path: {row['path']}",
                f"- Matched patterns: {', '.join(row['matched_patterns']) or 'none'}",
                "- Human review required: true",
                "",
            ]
        )
    fixture_only = bool(evidence_map.get("fixture_only"))
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "evidence_path_summaries": explanations,
        "summary": {"paths": len(explanations), "human_review_required": True},
        "markdown": "\n".join(markdown),
        "limitations": ["Evidence paths explain triage signals; they do not replace source-level review."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain evidence-map paths.")
    parser.add_argument("evidence_map_json")
    parser.add_argument("--output")
    parser.add_argument("--markdown-output")
    args = parser.parse_args()
    try:
        result = explain_paths(_load_map(args.evidence_map_json))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        if args.markdown_output:
            Path(args.markdown_output).write_text(result["markdown"] + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"evidence_path_explainer.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
