#!/usr/bin/env python3
"""Generate a generic EvidaraOS validation/governance report."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load(path: str | None) -> tuple[dict[str, Any], bool]:
    if not path:
        return {}, False
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    path_fixture = "evals/example" in path.replace("\\", "/")
    flag = bool(payload.get("fixture_only")) if isinstance(payload, dict) else False
    return payload, path_fixture or flag


def _audit_summary(audit: dict[str, Any]) -> dict[str, Any]:
    return audit.get("summary", {}) if isinstance(audit, dict) else {}


def _queue_summary(queue: dict[str, Any]) -> dict[str, Any]:
    return queue.get("summary", {}) if isinstance(queue, dict) else {}


def build_report(module: str, queue: dict[str, Any], audit: dict[str, Any], fixture_only: bool, limitations: list[str]) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    queue_summary = _queue_summary(queue)
    audit_summary = _audit_summary(audit)
    lines = [
        f"# EvidaraOS Validation Report: {module}",
        "",
        f"Generated at: {now}",
        "",
    ]
    if fixture_only:
        lines.extend([f"**Fixture-only warning**: {FIXTURE_WARNING}", ""])
    lines.extend(
        [
            "## Human Review Queue",
            "",
            f"- Items: {queue_summary.get('items', 'not provided')}",
            f"- Second review needed: {queue_summary.get('second_review_needed', 'not provided')}",
            "",
            "## Audit Trail",
            "",
            f"- Events: {audit_summary.get('events', 'not provided')}",
            f"- Required field completeness: {audit_summary.get('required_field_completeness', 'not provided')}",
            f"- Missing required fields: {', '.join(audit_summary.get('missing_required_fields', [])) or 'none'}",
            "",
            "## Limitations",
            "",
        ]
    )
    if limitations:
        lines.extend(f"- {item}" for item in limitations)
    else:
        lines.extend(
            [
                "- Validation metrics require human-labeled benchmark data.",
                "- Audit completeness checks field presence, not scientific correctness.",
                "- Draft skills require domain expert review before production use.",
            ]
        )
    return {
        "summary": {
            "module": module,
            "generated_at": now,
            "fixture_only": fixture_only,
            "fixture_warning": FIXTURE_WARNING if fixture_only else "",
            "queue_summary": queue_summary,
            "audit_summary": audit_summary,
        },
        "markdown_report": "\n".join(lines),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate EvidaraOS validation report.")
    parser.add_argument("--module", required=True)
    parser.add_argument("--review-queue")
    parser.add_argument("--audit-summary")
    parser.add_argument("--limitation", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        queue, queue_fixture = _load(args.review_queue)
        audit, audit_fixture = _load(args.audit_summary)
        result = build_report(args.module, queue, audit, queue_fixture or audit_fixture, args.limitation)
        if args.output:
            Path(args.output).write_text(result["markdown_report"] + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"validation_report.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

