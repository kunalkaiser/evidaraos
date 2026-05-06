#!/usr/bin/env python3
"""Evaluate AI exclusion rationales against human-reviewed reasons."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


REASON_KEYWORDS = {
    "wrong_population": ["wrong population", "population"],
    "wrong_intervention": ["wrong intervention", "wrong exposure", "intervention", "exposure"],
    "wrong_outcome": ["wrong outcome", "outcome"],
    "wrong_design": ["wrong design", "study design", "design"],
    "duplicate": ["duplicate"],
    "non_evidence": ["editorial", "comment", "letter", "protocol", "non-evidence"],
    "insufficient_information": ["insufficient", "missing abstract", "full text needed", "uncertain"],
}


def _load(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("decisions", "records", "labels", "items"):
        if isinstance(payload.get(key), list):
            return payload[key]
    raise ValueError(f"{path} must be a JSON array or contain decisions/records/labels/items")


def _record_id(item: dict) -> str:
    return str(item.get("record_id") or item.get("id") or "")


def _reason(item: dict) -> str:
    return str(item.get("exclusion_reason") or item.get("reason") or item.get("rationale") or "").lower()


def _decision(item: dict) -> str:
    return str(item.get("decision") or item.get("label") or item.get("final_decision") or "").lower()


def _category(reason: str) -> str:
    for category, keywords in REASON_KEYWORDS.items():
        if any(keyword in reason for keyword in keywords):
            return category
    return "other"


def evaluate(ai_items: list[dict], gold_items: list[dict]) -> dict:
    ai_by_id = {_record_id(item): item for item in ai_items if _record_id(item)}
    gold_by_id = {_record_id(item): item for item in gold_items if _record_id(item)}
    compared = 0
    matched = 0
    disagreements = []
    types = Counter()

    for record_id, gold in gold_by_id.items():
        if _decision(gold) != "exclude":
            continue
        ai = ai_by_id.get(record_id, {})
        gold_category = _category(_reason(gold))
        ai_category = _category(_reason(ai))
        compared += 1
        if gold_category == ai_category:
            matched += 1
        else:
            types[f"{ai_category}_vs_{gold_category}"] += 1
            disagreements.append(
                {
                    "record_id": record_id,
                    "ai_reason": _reason(ai),
                    "human_reason": _reason(gold),
                    "ai_category": ai_category,
                    "human_category": gold_category,
                }
            )
    accuracy = matched / compared if compared else 0.0
    return {
        "summary": {
            "excluded_records_compared": compared,
            "rationale_accuracy": round(accuracy, 4),
            "matched_rationales": matched,
            "disagreement_count": len(disagreements),
            "most_common_disagreement_types": types.most_common(),
        },
        "examples_requiring_review": disagreements[:25],
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare AI exclusion reasons against human-reviewed reasons.")
    parser.add_argument("--ai", required=True, help="AI screening decisions JSON")
    parser.add_argument("--gold", required=True, help="human-reviewed labels/reasons JSON")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = evaluate(_load(args.ai), _load(args.gold))
    except Exception as exc:
        print(f"evaluate_exclusion_rationales.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
