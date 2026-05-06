#!/usr/bin/env python3
"""Generate an EvidenceOS pharma-slr project manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_VERSION = "project_manifest.py/0.1"


def _hash_file(path: str | None) -> str:
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists():
        return ""
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def _load_optional(path: str | None) -> Any:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _artifact(path: str | None, artifact_type: str) -> dict:
    return {
        "type": artifact_type,
        "path": path or "",
        "sha256": _hash_file(path),
    }


def build_manifest(args: argparse.Namespace) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    artifacts = [
        _artifact(args.protocol, "protocol"),
        _artifact(args.search_log, "search_log"),
        _artifact(args.deduplicated_records, "deduplicated_records"),
        _artifact(args.screening_labels, "screening_labels"),
        _artifact(args.extractions, "extractions"),
        _artifact(args.adjudication, "adjudication"),
        _artifact(args.locked_labels, "locked_labels"),
        _artifact(args.audit_trail, "audit_trail"),
        _artifact(args.validation_report, "validation_report"),
        _artifact(args.final_report, "final_report"),
    ]
    artifacts = [artifact for artifact in artifacts if artifact["path"]]
    fixture_only = any("evals/example_" in artifact["path"].replace("\\", "/") for artifact in artifacts)
    return {
        "review_id": args.review_id,
        "generated_at": now,
        "tool_name": "pharma-slr",
        "tool_version": SCRIPT_VERSION,
        "runtime": "DeerFlow",
        "fixture_only": fixture_only,
        "fixture_warning": "These results are from sample fixture data and are not validation evidence." if fixture_only else "",
        "protocol_summary": _load_optional(args.protocol),
        "artifacts": artifacts,
        "governance": {
            "human_review_required": True,
            "dual_reviewer_adjudication": bool(args.adjudication),
            "audit_trail_present": bool(args.audit_trail),
            "validation_report_present": bool(args.validation_report),
            "final_report_present": bool(args.final_report),
        },
    }


def _write(path: str | None, payload: dict) -> None:
    if path:
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a pharma-slr project manifest tying review artifacts together.")
    parser.add_argument("--review-id", required=True)
    parser.add_argument("--protocol")
    parser.add_argument("--search-log")
    parser.add_argument("--deduplicated-records")
    parser.add_argument("--screening-labels")
    parser.add_argument("--extractions")
    parser.add_argument("--adjudication")
    parser.add_argument("--locked-labels")
    parser.add_argument("--audit-trail")
    parser.add_argument("--validation-report")
    parser.add_argument("--final-report")
    parser.add_argument("--output")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_manifest(args)
        _write(args.output, result)
    except Exception as exc:
        print(f"project_manifest.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
