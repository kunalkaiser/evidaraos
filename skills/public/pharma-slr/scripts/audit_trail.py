#!/usr/bin/env python3
"""Generate an audit-ready review decision trail with metadata hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "audit_trail.py/0.2"
UNKNOWN = "unknown"


def _load(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("events", "review_queue", "records", "items", "audit_events", "locked_labels"):
        if isinstance(payload.get(key), list):
            return payload[key]
    raise ValueError("Events input must be JSON array or object with events/review_queue/records/items/audit_events")


def _hash(value: Any) -> str:
    if value in (None, ""):
        return UNKNOWN
    encoded = json.dumps(value, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _value(event: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        value = event.get(key)
        if value not in (None, ""):
            return str(value)
    return default


def _event_id(review_id: str, event: dict, index: int) -> str:
    existing = event.get("event_id")
    if existing:
        return str(existing)
    record_id = _value(event, "record_id", "id", default=f"row-{index}")
    digest = hashlib.sha1(f"{review_id}:{record_id}:{index}".encode("utf-8")).hexdigest()[:12]
    return f"evt-{digest}"


def build_audit(review_id: str, events: list[dict]) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for index, event in enumerate(events, start=1):
        ai_decision = _value(event, "ai_decision", "decision", "label")
        human_decision = _value(event, "human_decision")
        final_decision = _value(event, "final_decision", default=human_decision or ai_decision)
        row = {
            "review_id": review_id,
            "event_id": _event_id(review_id, event, index),
            "event_type": _value(event, "event_type", default="screening_decision"),
            "record_id": _value(event, "record_id", "id"),
            "timestamp": _value(event, "timestamp", default=now),
            "tool_name": _value(event, "tool_name", default="pharma-slr"),
            "tool_version": _value(event, "tool_version", "tool_script_version", default=UNKNOWN),
            "script_path": _value(event, "script_path", default=__file__),
            "prompt_name": _value(event, "prompt_name", default=UNKNOWN),
            "prompt_version": _value(event, "prompt_version", default=UNKNOWN),
            "input_hash": _value(event, "input_hash", default=_hash(event.get("input") or event.get("record") or event.get("title"))),
            "output_hash": _value(event, "output_hash", default=_hash(event)),
            "model_name": _value(event, "model_name", default=UNKNOWN),
            "query_string": _value(event, "query_string", "query_used", "query"),
            "source": _value(event, "source"),
            "ai_decision": ai_decision,
            "human_decision": human_decision,
            "final_decision": final_decision,
            "rationale": _value(event, "rationale", "ai_rationale", "reason"),
            "provenance": event.get("provenance") or {
                "source": _value(event, "source"),
                "doi": _value(event, "doi"),
                "pmid": _value(event, "pmid"),
                "url": _value(event, "url"),
            },
        }
        rows.append(row)
    markdown = "\n".join(
        [
            "| Event | Record | Type | Tool | Model | Query | AI decision | Human decision | Final decision | Timestamp |",
            "|---|---|---|---|---|---|---|---|---|---|",
            *[
                f"| {row['event_id']} | {row['record_id']} | {row['event_type']} | {row['tool_name']} {row['tool_version']} | {row['model_name']} | {row['query_string']} | {row['ai_decision']} | {row['human_decision']} | {row['final_decision']} | {row['timestamp']} |"
                for row in rows
            ],
        ]
    )
    completeness_fields = [
        "review_id",
        "event_id",
        "event_type",
        "record_id",
        "timestamp",
        "tool_name",
        "tool_version",
        "script_path",
        "prompt_name",
        "prompt_version",
        "input_hash",
        "output_hash",
        "model_name",
        "ai_decision",
        "final_decision",
    ]
    present = sum(1 for row in rows for field in completeness_fields if row.get(field) not in (None, ""))
    total = len(rows) * len(completeness_fields)
    return {
        "summary": {
            "review_id": review_id,
            "events": len(rows),
            "generated_at": now,
            "tool_script_version": SCRIPT_VERSION,
            "required_field_completeness": round(present / total, 4) if total else 0.0,
        },
        "audit_events": rows,
        "markdown_summary": markdown,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create an audit trail from review decision events.")
    parser.add_argument("--review-id", required=True)
    parser.add_argument("--events", required=True, help="screening/extraction/audit events JSON")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_audit(args.review_id, _load(args.events))
    except Exception as exc:
        print(f"audit_trail.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
