#!/usr/bin/env python3
"""Prioritize scored records into precision-aware screening buckets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _score(record: dict) -> float:
    return float((record.get("precision_score") or {}).get("final_relevance_score", 0.0))


def _confidence(record: dict) -> float:
    return float((record.get("precision_score") or {}).get("confidence", 0.0))


def _background(record: dict) -> bool:
    score = record.get("precision_score") or {}
    title = str(record.get("title", "")).lower()
    return bool(score.get("background_signal")) or any(term in title for term in ["review", "guideline", "consensus", "overview"])


def prioritize(records: list[dict]) -> dict:
    groups = {
        "very_likely_include": [],
        "possible_include": [],
        "uncertain_human_review": [],
        "likely_exclude": [],
        "background_only": [],
    }
    for record in records:
        score = _score(record)
        confidence = _confidence(record)
        exclusion = float((record.get("precision_score") or {}).get("exclusion_signal", 0.0))
        if _background(record) and score >= 0.35:
            bucket = "background_only"
        elif exclusion and score < 0.55:
            bucket = "likely_exclude"
        elif score >= 0.72 and confidence >= 0.60:
            bucket = "very_likely_include"
        elif score >= 0.48:
            bucket = "possible_include"
        elif score >= 0.25 or confidence < 0.55:
            bucket = "uncertain_human_review"
        else:
            bucket = "likely_exclude"
        groups[bucket].append(record)
    summary = {key: len(value) for key, value in groups.items()}
    summary["ai_prioritized_records"] = summary["very_likely_include"] + summary["possible_include"] + summary["background_only"]
    summary["human_review_required_records"] = summary["possible_include"] + summary["uncertain_human_review"]
    return {"summary": summary, "groups": groups}


def _read_records(path: str | None) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8")) if path else json.load(sys.stdin)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise ValueError("Input must be a JSON array or object with records array")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Group scored records into screening priority buckets.")
    parser.add_argument("records", nargs="?", help="scored records JSON file; reads stdin when omitted")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = prioritize(_read_records(args.records))
    except Exception as exc:
        print(f"screening_prioritizer.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
