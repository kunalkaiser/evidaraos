#!/usr/bin/env python3
"""Extract biomedical entities from text records using transparent dictionaries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_LEXICON = {
    "drug": ["dupilumab", "methotrexate", "adalimumab", "tofacitinib", "baricitinib"],
    "disease": ["atopic dermatitis", "asthma", "eosinophilic esophagitis", "psoriasis", "rheumatoid arthritis"],
    "gene_protein": ["IL4R", "IL4", "IL13", "JAK1", "TNF"],
    "pathway": ["type 2 inflammation", "JAK-STAT signaling", "Th2 pathway", "TNF signaling"],
    "adverse_event": ["infection", "conjunctivitis", "malignancy", "hepatic injury"],
    "phenotype": ["itch", "eczema", "eosinophilia", "skin inflammation"],
    "biomarker": ["eosinophils", "IgE", "IL-13"],
}

FIXTURE_WARNING = "These results are from sample fixture data and are not validation evidence."


def _load_texts(path: str) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    for key in ("records", "items", "evidence", "articles"):
        value = payload.get(key) if isinstance(payload, dict) else None
        if isinstance(value, list):
            return value
    raise ValueError(f"{path} must be a JSON array or contain records/items/evidence/articles")


def _fixture_only(path: str) -> bool:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return "evals/example" in path.replace("\\", "/") or bool(isinstance(payload, dict) and payload.get("fixture_only"))


def _load_lexicon(path: str | None) -> dict[str, list[str]]:
    if not path:
        return DEFAULT_LEXICON
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    lexicon = {key: list(value) for key, value in payload.items() if isinstance(value, list)}
    return {**DEFAULT_LEXICON, **lexicon}


def _record_text(record: dict[str, Any]) -> str:
    return " ".join(str(record.get(field, "")) for field in ("title", "abstract", "text", "snippet", "claim", "finding"))


def extract_entities(records: list[dict[str, Any]], lexicon: dict[str, list[str]]) -> dict[str, Any]:
    output = []
    for index, record in enumerate(records):
        text = _record_text(record)
        lower = text.lower()
        entities = []
        for entity_type, terms in lexicon.items():
            for term in terms:
                if re.search(rf"\b{re.escape(term.lower())}\b", lower):
                    entities.append(
                        {
                            "text": term,
                            "type": entity_type,
                            "normal_id": term.upper().replace(" ", "_"),
                            "confidence": "dictionary_match",
                        }
                    )
        output.append(
            {
                "record_id": str(record.get("record_id") or record.get("id") or f"record-{index + 1}"),
                "source": record.get("source", ""),
                "entities": entities,
                "entity_count": len(entities),
            }
        )
    return {
        "fixture_only": False,
        "fixture_warning": "",
        "entity_extraction_method": "transparent_dictionary_match",
        "records": output,
        "limitations": [
            "Dictionary matching is a deterministic MVP and will miss synonyms not in the lexicon.",
            "Entity extraction requires human review before scientific use.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract biomedical entities from JSON text records.")
    parser.add_argument("records_json")
    parser.add_argument("--lexicon-json")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = extract_entities(_load_texts(args.records_json), _load_lexicon(args.lexicon_json))
        if _fixture_only(args.records_json):
            result["fixture_only"] = True
            result["fixture_warning"] = FIXTURE_WARNING
        if args.output:
            Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        print(f"entity_extraction.py: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
