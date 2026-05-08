#!/usr/bin/env python3
"""Create EvidaraOS audit events with version/hash metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOL_VERSION = "evidaraos-governance-draft/0.1"


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _load_events(path: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("review_queue", "events", "items", "records"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value
    raise ValueError(f"{path} must be a JSON array or contain review_queue/events/items/records")


def _event_id(review_id: str, item: dict[str, Any], index: int) -> str:
    basis = f"{review_id}:{item.get('item_id') or item.get('record_id') or item.get('claim_id') or index}:{index}"
    return "evt-" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:12]


def build_audit(review_id: str, module: str, events: list[dict[str, Any]]) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for index, event in enumerate(events):
        rows.append(
            {
                "review_id": review_id,
                "event_id": _event_id(review_id, event, index),
                "event_type": event.get("event_type") or "human_review_item",
                "module": module,
                "record_id": str(event.get("item_id") or event.get("record_id") or event.get("claim_id") or event.get("parameter") or ""),
                "timestamp": event.get("timestamp") or now,
                "tool_name": "evidaraos_governance",
                "tool_version": TOOL_VERSION,
                "script_path": str(Path(__file__).resolve()),
                "prompt_name": event.get("prompt_name", "unknown"),
                "prompt_version": event.get("prompt_version", "unknown"),
                "input_hash": event.get("input_hash") or _sha(event.get("source_item", event)),
                "output_hash": event.get("output_hash") or _sha(event),
                "model_name": event.get("model_name", "unknown"),
                "query_string": event.get("query_string", ""),
                "ai_decision": event.get("ai_decision", ""),
                "human_decision": event.get("human_decision", ""),
                "final_decision": event.get("final_decision") or event.get("human_decision") or "",
                "rationale": event.get("rationale", ""),
                "provenance": event.get("provenance", {}),
            }
        )
    required = ["review_id", "event_id", "event_type", "record_id", "timestamp", "tool_name", "tool_version", "script_path", "input_hash", "output_hash"]
    missing = sorted({field for row in rows for field in required if row.get(field) in ("", None)})
    return {
        "summary": {
            "review_id": review_id,
            "module": module,
            "events": len(rows),
            "generated_at": now,
            "required_field_completeness": 1.0 if not missing else round(1 - (len(missing) / len(required)), 4),
            "missing_required_fields": missing,
        },
        "audit_events": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create EvidaraOS audit trail.")
    parser.add_argument("--review-id", required=True)
    parser.add_argument("--module", required=True)
    parser.add_argument("--events", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = build_audit(args.review_id, args.module, _load_events(args.events))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"audit_trail.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

