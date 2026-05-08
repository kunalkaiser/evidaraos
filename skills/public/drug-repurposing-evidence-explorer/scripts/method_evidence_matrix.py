#!/usr/bin/env python3
"""Build a candidate-by-method evidence matrix."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str) -> tuple[dict[str, Any], bool]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        payload = {"items": payload}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must be a JSON object or array")
    return payload, bool(payload.get("fixture_only")) or "evals/example" in path.replace("\\", "/")


def _candidate_key(row: dict[str, Any]) -> str:
    drug = row.get("drug") or row.get("candidate") or row.get("compound") or ""
    disease = row.get("disease") or row.get("indication") or row.get("condition") or ""
    return f"{str(drug).strip().lower()}::{str(disease).strip().lower()}"


def _candidate_label(row: dict[str, Any]) -> dict[str, str]:
    return {
        "drug": str(row.get("drug") or row.get("candidate") or row.get("compound") or ""),
        "disease": str(row.get("disease") or row.get("indication") or row.get("condition") or ""),
    }


def _score(row: dict[str, Any]) -> float:
    for key in (
        "zero_shot_hypothesis_score",
        "net_hypothesis_score",
        "link_prediction_score",
        "score",
        "usage_signal_score",
        "mechanistic_plausibility",
        "clinical_evidence",
    ):
        value = row.get(key)
        if isinstance(value, (int, float)):
            return round(float(value), 4)
    return 0.0


def build_matrix(signals_payload: dict[str, Any], fixture_only: bool) -> dict[str, Any]:
    signals = signals_payload.get("method_signals") or signals_payload.get("signals") or signals_payload.get("items") or []
    if not isinstance(signals, list):
        raise ValueError("signals input must contain a method_signals array")

    grouped: dict[str, dict[str, Any]] = {}
    for signal in signals:
        if not isinstance(signal, dict):
            continue
        key = _candidate_key(signal)
        if key == "::":
            continue
        grouped.setdefault(key, {**_candidate_label(signal), "method_signals": []})
        grouped[key]["method_signals"].append(
            {
                "method_id": signal.get("method_id", "unknown"),
                "method_family": signal.get("method_family", "unknown"),
                "direction": signal.get("direction", "unknown"),
                "score": _score(signal),
                "evidence_grade": signal.get("evidence_grade", "ungraded"),
                "human_review_required": bool(signal.get("human_review_required", True)),
                "rationale": signal.get("rationale", ""),
                "limitations": signal.get("limitations", []),
            }
        )

    rows = []
    for item in grouped.values():
        supportive = [s for s in item["method_signals"] if s["direction"] == "supportive"]
        conflicting = [s for s in item["method_signals"] if s["direction"] == "conflicting"]
        unavailable = [s for s in item["method_signals"] if s["direction"] in {"unavailable", "unknown"}]
        average_support = round(sum(s["score"] for s in supportive) / max(1, len(supportive)), 4)
        item["summary"] = {
            "supportive_methods": len(supportive),
            "conflicting_methods": len(conflicting),
            "unavailable_methods": len(unavailable),
            "average_supportive_score": average_support,
            "human_review_required": True,
        }
        rows.append(item)
    rows.sort(key=lambda row: (row["summary"]["supportive_methods"], row["summary"]["average_supportive_score"]), reverse=True)
    return {
        "fixture_only": fixture_only,
        "fixture_warning": FIXTURE_WARNING if fixture_only else "",
        "evidence_matrix": rows,
        "summary": {"candidates": len(rows), "method_signal_count": len(signals)},
        "limitations": [
            "Method agreement is a prioritization signal, not proof of efficacy.",
            "Conflicting and unavailable method signals should remain visible in review outputs.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build candidate-by-method evidence matrix.")
    parser.add_argument("method_signals_json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        payload, fixture = _load(args.method_signals_json)
        result = build_matrix(payload, fixture)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"method_evidence_matrix.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
