#!/usr/bin/env python3
"""Evaluate AI screening decisions against human gold-standard labels."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

POSITIVE = {"include"}
NEGATIVE = {"exclude", "uncertain", "background_only"}


def _load_records(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("decisions", "records", "labels", "items"):
        if isinstance(payload.get(key), list):
            return payload[key]
    raise ValueError(f"{path} must be a JSON array or contain decisions/records/labels/items")


def _record_id(item: dict) -> str:
    return str(item.get("record_id") or item.get("id") or "")


def _decision(item: dict) -> str:
    return str(item.get("decision") or item.get("label") or item.get("final_decision") or "").lower()


def _binary(label: str) -> str:
    return "include" if label in POSITIVE else "not_include"


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _kappa(confusion: dict[str, dict[str, int]]) -> float:
    labels = sorted(confusion)
    total = sum(confusion[a][b] for a in labels for b in labels)
    if total == 0:
        return 0.0
    observed = sum(confusion[label][label] for label in labels) / total
    expected = 0.0
    for label in labels:
        row = sum(confusion[label][b] for b in labels)
        col = sum(confusion[a][label] for a in labels)
        expected += (row / total) * (col / total)
    return _safe_div(observed - expected, 1 - expected)


def evaluate(ai_items: list[dict], gold_items: list[dict]) -> dict:
    ai_by_id = {_record_id(item): _decision(item) for item in ai_items if _record_id(item)}
    gold_by_id = {_record_id(item): _decision(item) for item in gold_items if _record_id(item)}
    labels = ["include", "exclude", "uncertain"]
    confusion = {gold: {ai: 0 for ai in labels} for gold in labels}
    binary = {"tp": 0, "tn": 0, "fp": 0, "fn": 0}
    missing_ai = []

    for record_id, gold in gold_by_id.items():
        ai = ai_by_id.get(record_id)
        if ai is None:
            missing_ai.append(record_id)
            ai = "uncertain"
        if gold not in labels:
            gold = "uncertain"
        if ai not in labels:
            ai = "uncertain"
        confusion[gold][ai] += 1
        gold_bin = _binary(gold)
        ai_bin = _binary(ai)
        if gold_bin == "include" and ai_bin == "include":
            binary["tp"] += 1
        elif gold_bin == "not_include" and ai_bin == "not_include":
            binary["tn"] += 1
        elif gold_bin == "not_include" and ai_bin == "include":
            binary["fp"] += 1
        elif gold_bin == "include" and ai_bin == "not_include":
            binary["fn"] += 1

    tp, tn, fp, fn = binary["tp"], binary["tn"], binary["fp"], binary["fn"]
    sensitivity = _safe_div(tp, tp + fn)
    specificity = _safe_div(tn, tn + fp)
    precision = _safe_div(tp, tp + fp)
    recall = sensitivity
    accuracy = _safe_div(tp + tn, tp + tn + fp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)
    kappa = _kappa(confusion)
    markdown = "\n".join(
        [
            "| Metric | Value |",
            "|---|---:|",
            f"| Sensitivity | {sensitivity:.3f} |",
            f"| Specificity | {specificity:.3f} |",
            f"| Accuracy | {accuracy:.3f} |",
            f"| Precision | {precision:.3f} |",
            f"| Recall | {recall:.3f} |",
            f"| F1 | {f1:.3f} |",
            f"| Cohen's kappa | {kappa:.3f} |",
        ]
    )
    return {
        "summary": {
            "records_evaluated": len(gold_by_id),
            "missing_ai_decisions": missing_ai,
            "sensitivity": round(sensitivity, 4),
            "specificity": round(specificity, 4),
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "cohens_kappa": round(kappa, 4),
        },
        "confusion_matrix": confusion,
        "binary_confusion": binary,
        "markdown_summary": markdown,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate AI screening against human gold labels.")
    parser.add_argument("--ai", required=True, help="AI screening decisions JSON")
    parser.add_argument("--gold", required=True, help="human gold-standard labels JSON")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = evaluate(_load_records(args.ai), _load_records(args.gold))
    except Exception as exc:
        print(f"evaluate_screening_performance.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
