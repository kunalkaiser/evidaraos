#!/usr/bin/env python3
"""Create an EvidaraOS project manifest tying artifacts together."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _hash_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _artifact(kind: str, path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    p = Path(path)
    return {
        "type": kind,
        "path": str(p),
        "exists": p.exists(),
        "sha256": _hash_file(path) if p.exists() else "",
    }


def build_manifest(args: argparse.Namespace) -> dict[str, Any]:
    artifacts = [
        _artifact("scope", args.scope),
        _artifact("source_records", args.source_records),
        _artifact("structured_outputs", args.structured_outputs),
        _artifact("review_queue", args.review_queue),
        _artifact("audit_trail", args.audit_trail),
        _artifact("validation_report", args.validation_report),
        _artifact("final_report", args.final_report),
    ]
    artifacts = [item for item in artifacts if item]
    fixture_only = any("evals/example" in item["path"].replace("\\", "/") for item in artifacts)
    return {
        "project_id": args.project_id,
        "module": args.module,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "runtime": "DeerFlow",
        "tool_name": "evidaraos_governance",
        "tool_version": "project_manifest.py/0.1",
        "fixture_only": fixture_only,
        "fixture_warning": "These results are from sample fixture data and are not validation evidence." if fixture_only else "",
        "artifacts": artifacts,
        "governance": {
            "human_review_required": True,
            "audit_trail_present": any(item["type"] == "audit_trail" and item["exists"] for item in artifacts),
            "validation_report_present": any(item["type"] == "validation_report" and item["exists"] for item in artifacts),
            "final_report_present": any(item["type"] == "final_report" and item["exists"] for item in artifacts),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create EvidaraOS project manifest.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--module", required=True)
    parser.add_argument("--scope")
    parser.add_argument("--source-records")
    parser.add_argument("--structured-outputs")
    parser.add_argument("--review-queue")
    parser.add_argument("--audit-trail")
    parser.add_argument("--validation-report")
    parser.add_argument("--final-report")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = build_manifest(args)
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"project_manifest.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

