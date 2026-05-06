#!/usr/bin/env python3
"""Score normalized records for likely relevance to structured concepts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from concept_expand import expand_concepts


WEIGHTS = {
    "high_recall": {
        "disease_match": 0.20,
        "intervention_match": 0.25,
        "outcome_match": 0.15,
        "population_match": 0.10,
        "study_design_match": 0.10,
        "abstract_signal": 0.15,
        "exclusion_signal": -0.20,
    },
    "balanced": {
        "disease_match": 0.22,
        "intervention_match": 0.28,
        "outcome_match": 0.18,
        "population_match": 0.10,
        "study_design_match": 0.10,
        "abstract_signal": 0.12,
        "exclusion_signal": -0.25,
    },
    "high_precision": {
        "disease_match": 0.22,
        "intervention_match": 0.30,
        "outcome_match": 0.22,
        "population_match": 0.08,
        "study_design_match": 0.12,
        "abstract_signal": 0.06,
        "exclusion_signal": -0.35,
    },
}

EXCLUSION_TERMS = ["editorial", "comment", "letter", "protocol", "animal", "mouse", "mice", "in vitro"]
BACKGROUND_TERMS = ["review", "overview", "guideline", "consensus"]


def _terms(concepts: dict, key: str) -> list[str]:
    terms: list[str] = []
    value = concepts.get(key)
    if isinstance(value, str) and value:
        terms.append(value)
    elif isinstance(value, list):
        terms.extend(str(item) for item in value if item)
    syn = concepts.get("synonyms", {}).get(key)
    if isinstance(syn, dict):
        for variants in syn.values():
            terms.extend(str(item) for item in variants if item)
    elif isinstance(syn, list):
        terms.extend(str(item) for item in syn if item)
    return sorted(set(term.lower() for term in terms if term), key=str.lower)


def _contains_any(text: str, terms: list[str]) -> tuple[float, list[str]]:
    if not terms:
        return 0.0, []
    lowered = text.lower()
    hits = [term for term in terms if term and term in lowered]
    if not hits:
        return 0.0, []
    return 1.0, hits


def score_record(record: dict, concepts: dict, precision_mode: str = "balanced") -> dict:
    text = " ".join(str(record.get(key, "")) for key in ["title", "abstract", "journal", "keywords"]).lower()
    title = str(record.get("title", "")).lower()
    weights = WEIGHTS[precision_mode]

    disease_score, disease_hits = _contains_any(text, _terms(concepts, "disease"))
    intervention_score, intervention_hits = _contains_any(text, _terms(concepts, "intervention_exposure"))
    outcome_score, outcome_hits = _contains_any(text, _terms(concepts, "outcomes"))
    population_score, population_hits = _contains_any(text, _terms(concepts, "population"))
    design_score, design_hits = _contains_any(text, _terms(concepts, "study_design"))

    abstract_signal = 1.0 if record.get("abstract") and len(str(record.get("abstract"))) > 120 else 0.35 if record.get("abstract") else 0.0
    exclusion_hits = [term for term in EXCLUSION_TERMS if term in title or term in text[:500]]
    exclusion_signal = 1.0 if exclusion_hits else 0.0

    raw = (
        disease_score * weights["disease_match"]
        + intervention_score * weights["intervention_match"]
        + outcome_score * weights["outcome_match"]
        + population_score * weights["population_match"]
        + design_score * weights["study_design_match"]
        + abstract_signal * weights["abstract_signal"]
        + exclusion_signal * weights["exclusion_signal"]
    )
    final_score = max(0.0, min(1.0, raw))
    confidence = min(1.0, 0.35 + 0.15 * sum(1 for score in [disease_score, intervention_score, outcome_score, population_score, design_score] if score > 0) + (0.15 if record.get("abstract") else 0))

    reasons = []
    for label, hits in [
        ("disease", disease_hits),
        ("intervention/exposure", intervention_hits),
        ("outcome", outcome_hits),
        ("population", population_hits),
        ("study design", design_hits),
    ]:
        if hits:
            reasons.append(f"Matched {label}: {', '.join(hits[:5])}")
    if not record.get("abstract"):
        reasons.append("No abstract available; confidence reduced.")
    if exclusion_hits:
        reasons.append(f"Potential exclusion signal: {', '.join(exclusion_hits)}")

    scored = dict(record)
    scored["precision_score"] = {
        "precision_mode": precision_mode,
        "disease_match": disease_score,
        "intervention_match": intervention_score,
        "outcome_match": outcome_score,
        "population_match": population_score,
        "study_design_match": design_score,
        "abstract_signal": abstract_signal,
        "exclusion_signal": exclusion_signal,
        "final_relevance_score": round(final_score, 3),
        "confidence": round(confidence, 3),
        "transparent_reasons": reasons,
        "background_signal": any(term in title for term in BACKGROUND_TERMS),
    }
    return scored


def score_records(records: list[dict], concepts: dict, precision_mode: str = "balanced") -> dict:
    return {
        "summary": {"records_scored": len(records), "precision_mode": precision_mode},
        "records": [score_record(record, concepts, precision_mode) for record in records],
    }


def _read_records(path: str | None) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8")) if path else json.load(sys.stdin)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise ValueError("Records input must be a JSON array or object with records array")


def _read_concepts(path: str | None, question: str | None, mode: str) -> dict:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    if not question:
        raise ValueError("Provide --concepts-json or --question")
    return expand_concepts(question, mode)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score normalized records for likely SLR relevance.")
    parser.add_argument("records", nargs="?", help="records JSON file; reads stdin when omitted")
    parser.add_argument("--concepts-json", help="concept JSON file")
    parser.add_argument("--question", help="question to expand when concepts JSON is not supplied")
    parser.add_argument("--precision-mode", choices=["high_recall", "balanced", "high_precision"], default="balanced")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = score_records(_read_records(args.records), _read_concepts(args.concepts_json, args.question, args.precision_mode), args.precision_mode)
    except Exception as exc:
        print(f"precision_score.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
