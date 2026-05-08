#!/usr/bin/env python3
"""Extract transparent biomedical relations from text and entity records."""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any


RELATION_PATTERNS = {
    "inhibits": [r"inhibit(?:s|ed|ing)?", r"block(?:s|ed|ing)?", r"antagonis(?:t|m)"],
    "activates": [r"activat(?:es|ed|ing)?", r"stimulat(?:es|ed|ing)?"],
    "treats": [r"treat(?:s|ed|ment)?", r"improv(?:es|ed|ing)?", r"effective"],
    "associated_with": [r"associated with", r"linked to", r"correlat(?:es|ed|ion)"],
    "adverse_event_of": [r"adverse event", r"safety", r"risk of", r"toxicity"],
    "biomarker_of": [r"biomarker", r"predict(?:s|ed|ive)?"],
}

FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    return payload.get("records", [])


def _original_by_id(path: str | None) -> dict[str, dict[str, Any]]:
    if not path:
        return {}
    payload = _load_json(path)
    records = payload if isinstance(payload, list) else payload.get("records", payload.get("items", []))
    return {str(item.get("record_id") or item.get("id") or f"record-{index + 1}"): item for index, item in enumerate(records)}


def _text(record: dict[str, Any]) -> str:
    return " ".join(str(record.get(field, "")) for field in ("title", "abstract", "text", "snippet", "claim", "finding"))


def _relation_from_text(text: str) -> tuple[str, str]:
    lower = text.lower()
    for relation, patterns in RELATION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lower):
                return relation, pattern
    return "co_mentioned", "co_mentioned"


def _has(text: str, relation: str) -> str | None:
    lower = text.lower()
    for pattern in RELATION_PATTERNS.get(relation, []):
        if re.search(pattern, lower):
            return pattern
    return None


def _typed_relation(left: dict[str, Any], right: dict[str, Any], text: str) -> tuple[str, str] | None:
    types = {left.get("type"), right.get("type")}
    if "adverse_event" in types and "drug" not in types:
        return None
    if "drug" in types and "adverse_event" in types:
        return "adverse_event_of", _has(text, "adverse_event_of") or "drug_adverse_event_pair"
    if "drug" in types and "disease" in types:
        if pattern := _has(text, "treats"):
            return "treats", pattern
        return "associated_with", _has(text, "associated_with") or "drug_disease_pair"
    if "drug" in types and ("gene_protein" in types or "pathway" in types):
        if pattern := _has(text, "inhibits"):
            return "inhibits", pattern
        if pattern := _has(text, "activates"):
            return "activates", pattern
        return "associated_with", _has(text, "associated_with") or "drug_mechanism_pair"
    if "disease" in types and "biomarker" in types:
        return "biomarker_of", _has(text, "biomarker_of") or "disease_biomarker_pair"
    if "disease" in types and ("gene_protein" in types or "pathway" in types or "phenotype" in types):
        if pattern := _has(text, "biomarker_of"):
            return "biomarker_of", pattern
        return "associated_with", _has(text, "associated_with") or "disease_biology_pair"
    if "gene_protein" in types and "pathway" in types:
        return "associated_with", _has(text, "associated_with") or "gene_pathway_pair"
    return _relation_from_text(text)


def extract_relations(entity_payload: dict[str, Any], source_records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    relations = []
    for row in _records(entity_payload):
        entities = row.get("entities", [])
        record_id = str(row.get("record_id", ""))
        text = _text(source_records.get(record_id, {}))
        for left, right in itertools.combinations(entities, 2):
            if left["text"] == right["text"]:
                continue
            typed = _typed_relation(left, right, text)
            if typed is None:
                continue
            relation, evidence_pattern = typed
            relations.append(
                {
                    "record_id": record_id,
                    "source": row.get("source", ""),
                    "subject": left["text"],
                    "subject_type": left["type"],
                    "predicate": relation,
                    "object": right["text"],
                    "object_type": right["type"],
                    "evidence_pattern": evidence_pattern,
                    "confidence": "pattern_match" if relation != "co_mentioned" else "co_mention_only",
                    "human_review_required": True,
                }
            )
    return {
        "fixture_only": bool(entity_payload.get("fixture_only")),
        "fixture_warning": FIXTURE_WARNING if entity_payload.get("fixture_only") else "",
        "relation_extraction_method": "transparent_pattern_and_co_mention",
        "relations": relations,
        "relation_count": len(relations),
        "limitations": ["Co-mention relations are weak signals and must not be treated as causal or therapeutic evidence."],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract biomedical relations from entity extraction output.")
    parser.add_argument("entities_json")
    parser.add_argument("--records-json", help="original text records for relation pattern matching")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = extract_relations(_load_json(args.entities_json), _original_by_id(args.records_json))
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"relation_extraction.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
