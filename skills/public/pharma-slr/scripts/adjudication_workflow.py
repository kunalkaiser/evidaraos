#!/usr/bin/env python3
"""Build a dual-reviewer adjudication worklist for pharma-slr."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONFLICT_TYPES = {
    "include_vs_exclude",
    "different_exclusion_reason",
    "confidence_disagreement",
    "extraction_field_disagreement",
    "needs_full_text_review",
}

LABELS = ["include", "exclude", "uncertain"]
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "adjudication.schema.json"


def _load(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("review_queue", "decisions", "records", "items"):
        if isinstance(payload.get(key), list):
            return payload[key]
    raise ValueError(f"{path} must be a JSON array or contain review_queue/decisions/records/items")


def _write(path: str | None, payload: dict) -> None:
    if not path:
        return
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_optional(path: str | None) -> list[dict]:
    return _load(path) if path else []


def _record_id(item: dict) -> str:
    return str(item.get("record_id") or item.get("id") or "")


def _decision(item: dict) -> str:
    return str(item.get("human_decision") or item.get("decision") or item.get("label") or "").lower()


def _reason(item: dict) -> str:
    return str(item.get("exclusion_reason") or item.get("reason") or "").strip()


def _confidence(item: dict) -> float | None:
    value = item.get("confidence") or item.get("ai_confidence")
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extraction_fingerprint(item: dict) -> str:
    extraction = item.get("extraction") or {
        key: item.get(key)
        for key in ("population", "intervention_exposure", "comparator", "outcomes", "study_design")
        if key in item
    }
    return json.dumps(extraction, sort_keys=True, default=str)


def _conflict_type(one: dict, two: dict) -> str:
    d1, d2 = _decision(one), _decision(two)
    if {d1, d2} == {"include", "exclude"}:
        return "include_vs_exclude"
    if "uncertain" in {d1, d2}:
        return "needs_full_text_review"
    if d1 == d2 == "exclude" and _reason(one).lower() != _reason(two).lower():
        return "different_exclusion_reason"
    c1, c2 = _confidence(one), _confidence(two)
    if c1 is not None and c2 is not None and abs(c1 - c2) >= 0.25:
        return "confidence_disagreement"
    if _extraction_fingerprint(one) != _extraction_fingerprint(two):
        return "extraction_field_disagreement"
    return ""


def _safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def _cohens_kappa(pairs: list[tuple[str, str]]) -> float:
    if not pairs:
        return 0.0
    observed = sum(1 for one, two in pairs if one == two) / len(pairs)
    expected = 0.0
    for label in LABELS:
        p_one = sum(1 for one, _ in pairs if one == label) / len(pairs)
        p_two = sum(1 for _, two in pairs if two == label) / len(pairs)
        expected += p_one * p_two
    return _safe_div(observed - expected, 1 - expected)


def _inter_reviewer_metrics(one_by_id: dict[str, dict], two_by_id: dict[str, dict], ids: list[str]) -> dict:
    pairs = [(_decision(one_by_id.get(record_id, {})), _decision(two_by_id.get(record_id, {}))) for record_id in ids]
    pairs = [(one, two) for one, two in pairs if one and two]
    confusion = {one: {two: 0 for two in LABELS} for one in LABELS}
    for one, two in pairs:
        if one not in LABELS:
            one = "uncertain"
        if two not in LABELS:
            two = "uncertain"
        confusion[one][two] += 1
    agreements = sum(1 for one, two in pairs if one == two)
    return {
        "pairs_compared": len(pairs),
        "raw_agreement": round(_safe_div(agreements, len(pairs)), 4),
        "cohens_kappa": round(_cohens_kappa(pairs), 4),
        "confusion_matrix_reviewer1_by_reviewer2": confusion,
    }


def _validate_schema_instance(instance: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    for field in schema.get("required", []):
        if field not in instance:
            errors.append(f"missing required field: {field}")
    properties = schema.get("properties", {})
    for field, rules in properties.items():
        if field not in instance:
            continue
        value = instance[field]
        enum = rules.get("enum")
        if enum is not None and value not in enum:
            errors.append(f"{field}={value!r} not in enum {enum}")
        expected_type = rules.get("type")
        if expected_type == "string" and not isinstance(value, str):
            errors.append(f"{field} must be string")
    return errors


def _validate_adjudication_records(rows: list[dict]) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    record_errors = []
    for row in rows:
        errors = _validate_schema_instance(row, schema)
        if errors:
            record_errors.append({"record_id": row.get("record_id", ""), "errors": errors})
    return {"schema": str(SCHEMA_PATH), "valid": not record_errors, "errors": record_errors}


def _adjudicator_by_id(adjudicator_decisions: list[dict]) -> dict[str, dict]:
    return {_record_id(item): item for item in adjudicator_decisions if _record_id(item)}


def _apply_adjudicator_decisions(
    rows: list[dict],
    adjudicator_decisions: list[dict],
    adjudicator_id: str = "",
    adjudicator_signature: str = "",
) -> tuple[list[dict], list[dict]]:
    decisions_by_id = _adjudicator_by_id(adjudicator_decisions)
    locked_labels = []
    for row in rows:
        adjudicator = decisions_by_id.get(row["record_id"])
        if adjudicator:
            decision = _decision(adjudicator) or str(adjudicator.get("adjudicator_decision") or "").lower()
            row["adjudicator_decision"] = decision
            row["final_decision"] = decision
            row["final_exclusion_reason"] = _reason(adjudicator)
            row["adjudicator_notes"] = str(adjudicator.get("adjudicator_notes") or adjudicator.get("notes") or "")
            row["adjudicator_id"] = str(adjudicator.get("adjudicator_id") or adjudicator_id)
            row["adjudicator_signature"] = str(adjudicator.get("adjudicator_signature") or adjudicator_signature)
            row["adjudicated_at"] = datetime.now(timezone.utc).isoformat()
        else:
            row.setdefault("adjudicator_id", "")
            row.setdefault("adjudicator_signature", "")
            row.setdefault("adjudicated_at", "")
        if row.get("final_decision"):
            locked_labels.append(
                {
                    "record_id": row["record_id"],
                    "decision": row["final_decision"],
                    "exclusion_reason": row.get("final_exclusion_reason", ""),
                    "locked": True,
                    "locked_at": row.get("adjudicated_at") or row["timestamp"],
                    "source": "dual_reviewer_adjudication",
                    "adjudicator_id": row.get("adjudicator_id", ""),
                    "adjudicator_signature": row.get("adjudicator_signature", ""),
                }
            )
    return rows, locked_labels


def adjudicate(
    reviewer_one: list[dict],
    reviewer_two: list[dict],
    adjudicator_decisions: list[dict] | None = None,
    adjudicator_id: str = "",
    adjudicator_signature: str = "",
) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    one_by_id = {_record_id(item): item for item in reviewer_one if _record_id(item)}
    two_by_id = {_record_id(item): item for item in reviewer_two if _record_id(item)}
    all_ids = sorted(set(one_by_id) | set(two_by_id))
    rows = []
    for record_id in all_ids:
        one = one_by_id.get(record_id, {})
        two = two_by_id.get(record_id, {})
        d1 = _decision(one)
        d2 = _decision(two)
        agreement = "agreement" if d1 and d1 == d2 and not _conflict_type(one, two) else "conflict"
        conflict = "" if agreement == "agreement" else _conflict_type(one, two) or "needs_full_text_review"
        final_decision = d1 if agreement == "agreement" else ""
        final_reason = _reason(one) if agreement == "agreement" and final_decision == "exclude" else ""
        rows.append(
            {
                "record_id": record_id,
                "reviewer_1_decision": d1,
                "reviewer_2_decision": d2,
                "agreement_status": agreement,
                "conflict_type": conflict,
                "adjudicator_decision": "",
                "final_decision": final_decision,
                "final_exclusion_reason": final_reason,
                "adjudicator_notes": "",
                "adjudicator_id": "",
                "adjudicator_signature": "",
                "adjudicated_at": "",
                "timestamp": now,
            }
        )
    rows, locked_labels = _apply_adjudicator_decisions(rows, adjudicator_decisions or [], adjudicator_id, adjudicator_signature)
    inter_reviewer = _inter_reviewer_metrics(one_by_id, two_by_id, all_ids)
    summary = {
        "records_compared": len(rows),
        "agreements": sum(1 for row in rows if row["agreement_status"] == "agreement"),
        "conflicts": sum(1 for row in rows if row["agreement_status"] == "conflict"),
        "locked_final_labels": len(locked_labels),
        "pending_adjudication": sum(1 for row in rows if not row.get("final_decision")),
        "inter_reviewer_agreement": inter_reviewer,
        "conflict_type_counts": {
            conflict_type: sum(1 for row in rows if row["conflict_type"] == conflict_type)
            for conflict_type in sorted(CONFLICT_TYPES)
        },
    }
    markdown = "\n".join(
        [
            "| Record | Reviewer 1 | Reviewer 2 | Agreement | Conflict type | Final decision | Notes |",
            "|---|---|---|---|---|---|---|",
            *[
                f"| {row['record_id']} | {row['reviewer_1_decision']} | {row['reviewer_2_decision']} | {row['agreement_status']} | {row['conflict_type']} | {row['final_decision']} | {row['adjudicator_notes']} |"
                for row in rows
            ],
        ]
    )
    return {
        "summary": summary,
        "adjudication_records": rows,
        "locked_labels": locked_labels,
        "schema_validation": _validate_adjudication_records(rows),
        "markdown_summary": markdown,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a dual-reviewer adjudication worklist.")
    parser.add_argument("--reviewer-one", required=True, help="reviewer 1 decisions JSON")
    parser.add_argument("--reviewer-two", required=True, help="reviewer 2 decisions JSON")
    parser.add_argument("--adjudicator-decisions", help="optional adjudicator decisions JSON")
    parser.add_argument("--adjudicator-id", default="", help="adjudicator identifier to attach to locked labels")
    parser.add_argument("--adjudicator-signature", default="", help="adjudicator signature/attestation string")
    parser.add_argument("--output", help="optional output JSON file")
    parser.add_argument("--locked-output", help="optional locked final labels JSON output")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = adjudicate(
            _load(args.reviewer_one),
            _load(args.reviewer_two),
            _load_optional(args.adjudicator_decisions),
            args.adjudicator_id,
            args.adjudicator_signature,
        )
        _write(args.output, result)
        if args.locked_output:
            _write(args.locked_output, {"locked_labels": result["locked_labels"]})
    except Exception as exc:
        print(f"adjudication_workflow.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
