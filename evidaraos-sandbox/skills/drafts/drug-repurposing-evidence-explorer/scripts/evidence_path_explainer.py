#!/usr/bin/env python3
"""Explain transparent evidence paths behind repurposing candidate links."""

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
        return {"candidate_links": payload, "fixture_only": False}
    return payload


def _candidates(payload: dict[str, Any], path: str) -> list[dict[str, Any]]:
    for key in ("candidate_links", "candidates", "items"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value
    raise ValueError(f"{path} must be a JSON array or contain candidate_links/candidates/items")


def _path_to_text(path: list[Any]) -> str:
    return " ".join(str(part) for part in path)


def _strength(score: float) -> str:
    if score >= 0.75:
        return "higher-priority hypothesis"
    if score >= 0.45:
        return "moderate-priority hypothesis"
    return "low-priority exploratory hypothesis"


def explain_paths(candidates: list[dict[str, Any]], fixture_only: bool = False) -> dict[str, Any]:
    summaries = []
    for index, candidate in enumerate(candidates):
        score = float(candidate.get("link_prediction_score") or candidate.get("score") or 0)
        paths = candidate.get("evidence_paths", [])
        path_text = [_path_to_text(path) if isinstance(path, list) else str(path) for path in paths]
        missing = candidate.get("missing_evidence") or [
            "clinical efficacy evidence",
            "population-specific safety evidence",
            "dose, comparator, and endpoint context",
        ]
        summaries.append(
            {
                "candidate_id": candidate.get("candidate_id") or f"candidate-{index + 1}",
                "candidate_pair": candidate.get("candidate_pair") or f"{candidate.get('drug', '')} -> {candidate.get('disease', '')}",
                "priority_label": _strength(score),
                "score": round(score, 4),
                "evidence_path_count": len(path_text),
                "evidence_paths": path_text,
                "plain_language_rationale": (
                    "This candidate is prioritized because the extracted graph contains one or more "
                    "drug, target, pathway, disease, or safety connections. The path is a hypothesis "
                    "signal only and requires scientific review."
                ),
                "missing_evidence": missing,
                "human_review_required": True,
            }
        )
    markdown = ["# Evidence Path Explanations", ""]
    for row in summaries:
        markdown.extend(
            [
                f"## {row['candidate_pair']}",
                "",
                f"- Priority: {row['priority_label']}",
                f"- Score: {row['score']}",
                f"- Evidence paths: {row['evidence_path_count']}",
                f"- Human review required: {row['human_review_required']}",
                "- Missing evidence: " + "; ".join(row["missing_evidence"]),
                "",
            ]
        )
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "evidence_path_summaries": summaries,
        "summary": {"candidates_explained": len(summaries), "human_review_required": True},
        "markdown": "\n".join(markdown),
        "limitations": [
            "Evidence paths explain why a hypothesis was surfaced; they do not prove treatment effect.",
            "All paths require source-level review by a qualified scientific reviewer.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Explain evidence paths for repurposing candidate links.")
    parser.add_argument("candidate_links_json")
    parser.add_argument("--output")
    parser.add_argument("--markdown-output")
    args = parser.parse_args()
    try:
        payload = _load_payload(args.candidate_links_json)
        fixture_only = bool(payload.get("fixture_only")) or "evals/example" in args.candidate_links_json.replace("\\", "/")
        result = explain_paths(_candidates(payload, args.candidate_links_json), fixture_only)
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
