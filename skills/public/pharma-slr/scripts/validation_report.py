#!/usr/bin/env python3
"""Generate a project-level validation report for pharma-slr."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_optional(path: str | None) -> tuple[dict, bool]:
    if not path:
        return {}, False
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    fixture_path = "evals/example_" in path.replace("\\", "/")
    fixture_flag = bool(payload.get("fixture_only")) if isinstance(payload, dict) else False
    return payload, fixture_path or fixture_flag


def _summary(payload: dict) -> dict:
    return payload.get("summary", {}) if isinstance(payload, dict) else {}


def _metric(summary: dict, key: str) -> str:
    value = summary.get(key)
    if value is None:
        return "not provided"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def _audit_completeness(audit: dict) -> dict:
    events = audit.get("audit_events") or []
    required = ["review_id", "event_id", "event_type", "record_id", "timestamp", "tool_name", "tool_version", "script_path", "input_hash", "output_hash", "final_decision"]
    if not events:
        return {"events": 0, "required_field_completeness": 0.0, "missing_required_fields": required}
    total = len(events) * len(required)
    present = 0
    missing = set()
    for event in events:
        for field in required:
            if event.get(field) not in (None, ""):
                present += 1
            else:
                missing.add(field)
    return {
        "events": len(events),
        "required_field_completeness": round(present / total, 4) if total else 0.0,
        "missing_required_fields": sorted(missing),
    }


def build_report(inputs: dict[str, tuple[dict, bool]]) -> dict:
    screening, screening_fixture = inputs["screening"]
    extraction, extraction_fixture = inputs["extraction"]
    rationale, rationale_fixture = inputs["rationale"]
    audit, audit_fixture = inputs["audit"]
    adjudication, adjudication_fixture = inputs["adjudication"]
    fixture_only = any([screening_fixture, extraction_fixture, rationale_fixture, audit_fixture, adjudication_fixture])

    screening_summary = _summary(screening)
    extraction_summary = _summary(extraction)
    rationale_summary = _summary(rationale)
    audit_completeness = _audit_completeness(audit)
    adjudication_summary = _summary(adjudication)
    inter_reviewer = adjudication_summary.get("inter_reviewer_agreement", {}) if isinstance(adjudication_summary, dict) else {}
    generated_at = datetime.now(timezone.utc).isoformat()

    lines = [
        "# EvidenceOS pharma-slr Validation Report",
        "",
        f"Generated at: {generated_at}",
        "",
    ]
    if fixture_only:
        lines.extend([f"**Fixture-only warning**: {FIXTURE_WARNING}", ""])
    lines.extend(
        [
            "## Screening Performance",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Sensitivity | {_metric(screening_summary, 'sensitivity')} |",
            f"| Specificity | {_metric(screening_summary, 'specificity')} |",
            f"| Accuracy | {_metric(screening_summary, 'accuracy')} |",
            f"| Precision | {_metric(screening_summary, 'precision')} |",
            f"| Recall | {_metric(screening_summary, 'recall')} |",
            f"| F1 | {_metric(screening_summary, 'f1')} |",
            f"| Cohen's kappa | {_metric(screening_summary, 'cohens_kappa')} |",
            "",
            "## Extraction Performance",
            "",
            f"- Overall field accuracy: {_metric(extraction_summary, 'overall_field_accuracy')}",
            f"- F1: {_metric(extraction_summary, 'f1')}",
            f"- Missing field count: {_metric(extraction_summary, 'missing_field_count')}",
            f"- Mismatched field count: {_metric(extraction_summary, 'mismatched_field_count')}",
            "",
            "## Exclusion Rationale Performance",
            "",
            f"- Rationale accuracy: {_metric(rationale_summary, 'rationale_accuracy')}",
            f"- Disagreement count: {_metric(rationale_summary, 'disagreement_count')}",
            "",
            "## Inter-Reviewer Agreement / Adjudication",
            "",
            f"- Records compared: {_metric(adjudication_summary, 'records_compared')}",
            f"- Agreements: {_metric(adjudication_summary, 'agreements')}",
            f"- Conflicts: {_metric(adjudication_summary, 'conflicts')}",
            f"- Locked final labels: {_metric(adjudication_summary, 'locked_final_labels')}",
            f"- Pending adjudication: {_metric(adjudication_summary, 'pending_adjudication')}",
            f"- Inter-reviewer raw agreement: {_metric(inter_reviewer, 'raw_agreement')}",
            f"- Inter-reviewer Cohen's kappa: {_metric(inter_reviewer, 'cohens_kappa')}",
            "",
            "## Audit Trail Completeness",
            "",
            f"- Events: {audit_completeness['events']}",
            f"- Required field completeness: {audit_completeness['required_field_completeness']:.3f}",
            f"- Missing required fields: {', '.join(audit_completeness['missing_required_fields']) or 'none'}",
            "",
            "## Limitations",
            "",
            "- Validation metrics are meaningful only when evaluated against human-labeled benchmark or project gold-standard data.",
            "- Sample fixtures are smoke-test assets and are not scientific validation evidence.",
            "- Audit completeness checks field presence; they do not verify clinical correctness.",
        ]
    )
    return {
        "summary": {
            "generated_at": generated_at,
            "fixture_only": fixture_only,
            "fixture_warning": FIXTURE_WARNING if fixture_only else "",
            "audit_trail_completeness": audit_completeness,
        },
        "markdown_report": "\n".join(lines),
    }


def _write(path: str | None, markdown: str) -> None:
    if path:
        Path(path).write_text(markdown + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a project-level pharma-slr validation report.")
    parser.add_argument("--screening-metrics", help="screening performance JSON")
    parser.add_argument("--extraction-metrics", help="extraction performance JSON")
    parser.add_argument("--rationale-metrics", help="exclusion rationale metrics JSON")
    parser.add_argument("--adjudication-summary", help="adjudication workflow JSON")
    parser.add_argument("--audit-summary", help="audit trail JSON")
    parser.add_argument("--output", help="optional markdown output path")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_report(
            {
                "screening": _load_optional(args.screening_metrics),
                "extraction": _load_optional(args.extraction_metrics),
                "rationale": _load_optional(args.rationale_metrics),
                "adjudication": _load_optional(args.adjudication_summary),
                "audit": _load_optional(args.audit_summary),
            }
        )
        _write(args.output, result["markdown_report"])
    except Exception as exc:
        print(f"validation_report.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
