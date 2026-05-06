#!/usr/bin/env python3
"""Create a human-in-the-loop screening review queue."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "reviewer_decision.schema.json"


def _load(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload.get("records"), list):
        return payload["records"]
    if isinstance(payload.get("groups"), dict):
        records = []
        for group, items in payload["groups"].items():
            for item in items:
                copy = dict(item)
                copy.setdefault("priority_group", group)
                records.append(copy)
        return records
    raise ValueError("Input must be a JSON array, records object, or prioritizer groups object")


def _ai_decision(record: dict) -> str:
    if record.get("decision"):
        return record["decision"]
    group = record.get("priority_group", "")
    if group in ("very_likely_include", "possible_include"):
        return "include"
    if group in ("likely_exclude", "background_only"):
        return "exclude"
    return "uncertain"


def build_queue(records: list[dict], reviewer_id: str = "", now: str | None = None) -> dict:
    timestamp = now or datetime.now(timezone.utc).isoformat()
    queue = []
    for record in records:
        score = record.get("precision_score") or {}
        reasons = score.get("transparent_reasons") or []
        queue.append(
            {
                "record_id": str(record.get("record_id") or record.get("id") or ""),
                "title": record.get("title", ""),
                "source": record.get("source", ""),
                "ai_decision": _ai_decision(record),
                "ai_rationale": "; ".join(reasons) if isinstance(reasons, list) else str(reasons),
                "ai_confidence": score.get("confidence") or record.get("confidence"),
                "priority_group": record.get("priority_group", ""),
                "human_decision": "",
                "human_action": "pending",
                "exclusion_reason": "",
                "confidence": "",
                "notes": "",
                "reviewer_id": reviewer_id,
                "timestamp": timestamp,
            }
        )
    markdown_lines = [
        "| Record | Source | AI decision | Priority | AI confidence | Human action | Exclusion reason | Notes |",
        "|---|---|---|---|---:|---|---|---|",
    ]
    for item in queue:
        markdown_lines.append(
            f"| {item['record_id']} | {item['source']} | {item['ai_decision']} | {item['priority_group']} | "
            f"{item['ai_confidence'] or ''} | pending |  |  |"
        )
    return {
        "summary": {"queue_items": len(queue), "reviewer_id": reviewer_id, "timestamp": timestamp},
        "review_queue": queue,
        "schema_validation": _validate_queue(queue),
        "markdown_queue": "\n".join(markdown_lines),
    }


def _validate_instance(instance: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    for field in schema.get("required", []):
        if field not in instance:
            errors.append(f"missing required field: {field}")
    for field, rules in schema.get("properties", {}).items():
        if field not in instance:
            continue
        enum = rules.get("enum")
        if enum is not None and instance[field] not in enum:
            errors.append(f"{field}={instance[field]!r} not in enum {enum}")
    return errors


def _validate_queue(queue: list[dict]) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = []
    for item in queue:
        item_errors = _validate_instance(item, schema)
        if item_errors:
            errors.append({"record_id": item.get("record_id", ""), "errors": item_errors})
    return {"schema": str(SCHEMA_PATH), "valid": not errors, "errors": errors}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a human review queue from AI decisions or prioritized records.")
    parser.add_argument("input", help="AI decisions/prioritizer output JSON")
    parser.add_argument("--reviewer-id", default="", help="reviewer identifier to prefill")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_queue(_load(args.input), args.reviewer_id)
    except Exception as exc:
        print(f"human_review_queue.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
