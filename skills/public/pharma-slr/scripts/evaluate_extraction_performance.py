#!/usr/bin/env python3
"""Evaluate AI evidence extraction against human gold-standard extraction."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DEFAULT_FIELDS = [
    "disease",
    "intervention_exposure",
    "comparator",
    "population",
    "sample_size",
    "country",
    "data_source",
    "study_design",
    "incidence",
    "prevalence",
    "mortality",
    "safety_outcomes",
    "efficacy_outcomes",
    "follow_up",
    "limitations",
    "citation",
]


def _load(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("extractions", "records", "items"):
        if isinstance(payload.get(key), list):
            return payload[key]
    raise ValueError(f"{path} must be a JSON array or contain extractions/records/items")


def _record_id(item: dict) -> str:
    return str(item.get("record_id") or item.get("id") or "")


def _norm(value: Any) -> str:
    if isinstance(value, list):
        return " | ".join(sorted(str(item).strip().lower() for item in value if item))
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True).lower()
    return " ".join(str(value or "").strip().lower().split())


def evaluate(ai_items: list[dict], gold_items: list[dict], fields: list[str]) -> dict:
    ai_by_id = {_record_id(item): item for item in ai_items if _record_id(item)}
    gold_by_id = {_record_id(item): item for item in gold_items if _record_id(item)}
    field_stats = {field: {"correct": 0, "incorrect": 0, "missing": 0, "total": 0} for field in fields}
    mismatched_fields = []
    missing_fields = []
    confidences = []

    for record_id, gold in gold_by_id.items():
        ai = ai_by_id.get(record_id, {})
        confidence = ai.get("confidence") or (ai.get("precision_score") or {}).get("confidence")
        if isinstance(confidence, (int, float)):
            confidences.append(float(confidence))
        for field in fields:
            gold_value = gold.get(field)
            ai_value = ai.get(field)
            if gold_value in (None, "", [], {}):
                continue
            field_stats[field]["total"] += 1
            if ai_value in (None, "", [], {}):
                field_stats[field]["missing"] += 1
                missing_fields.append({"record_id": record_id, "field": field, "gold": gold_value})
            elif _norm(ai_value) == _norm(gold_value):
                field_stats[field]["correct"] += 1
            else:
                field_stats[field]["incorrect"] += 1
                mismatched_fields.append({"record_id": record_id, "field": field, "ai": ai_value, "gold": gold_value})

    total_correct = sum(stats["correct"] for stats in field_stats.values())
    total = sum(stats["total"] for stats in field_stats.values())
    total_missing = sum(stats["missing"] for stats in field_stats.values())
    total_incorrect = sum(stats["incorrect"] for stats in field_stats.values())
    precision = total_correct / (total_correct + total_incorrect) if (total_correct + total_incorrect) else 0.0
    recall = total_correct / total if total else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    field_accuracy = {
        field: round(stats["correct"] / stats["total"], 4) if stats["total"] else None
        for field, stats in field_stats.items()
    }
    confidence_summary = {
        "count": len(confidences),
        "mean": round(sum(confidences) / len(confidences), 4) if confidences else None,
        "min": min(confidences) if confidences else None,
        "max": max(confidences) if confidences else None,
    }
    return {
        "summary": {
            "records_evaluated": len(gold_by_id),
            "field_level_accuracy": field_accuracy,
            "overall_field_accuracy": round(total_correct / total, 4) if total else 0.0,
            "f1": round(f1, 4),
            "missing_field_count": total_missing,
            "mismatched_field_count": total_incorrect,
            "confidence_summary": confidence_summary,
        },
        "missing_fields": missing_fields,
        "mismatched_fields": mismatched_fields,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate AI extraction against human gold extraction.")
    parser.add_argument("--ai", required=True, help="AI extraction JSON")
    parser.add_argument("--gold", required=True, help="human gold extraction JSON")
    parser.add_argument("--fields", nargs="*", default=DEFAULT_FIELDS, help="fields to evaluate")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = evaluate(_load(args.ai), _load(args.gold), args.fields)
    except Exception as exc:
        print(f"evaluate_extraction_performance.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
