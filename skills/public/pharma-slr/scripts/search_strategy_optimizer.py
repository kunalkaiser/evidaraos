#!/usr/bin/env python3
"""Generate recall/precision-aware search strategies from expanded concepts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from concept_expand import expand_concepts


def _concept_terms(concepts: dict, key: str) -> list[str]:
    value = concepts.get(key)
    terms: list[str] = []
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
    return sorted(set(terms), key=str.lower)


def _primary_terms(concepts: dict, key: str) -> list[str]:
    value = concepts.get(key)
    if isinstance(value, str) and value:
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return []


def _or_group(terms: list[str], pubmed: bool = False) -> str:
    if not terms:
        return ""
    if pubmed:
        return "(" + " OR ".join(f'"{term}"[tiab]' if " " in term else f"{term}[tiab]" for term in terms) + ")"
    return "(" + " OR ".join(f'"{term}"' if " " in term else term for term in terms) + ")"


def build_strategies(concepts: dict) -> dict:
    disease = _concept_terms(concepts, "disease")
    intervention = _concept_terms(concepts, "intervention_exposure")
    outcomes = _concept_terms(concepts, "outcomes")
    population = _concept_terms(concepts, "population")
    designs = _concept_terms(concepts, "study_design")

    broad_parts = [_or_group(intervention), _or_group(disease or population)]
    balanced_parts = [_or_group(intervention), _or_group(disease or population), _or_group(outcomes)]
    precision_parts = [_or_group(intervention), _or_group(disease or population), _or_group(outcomes), _or_group(designs)]

    pubmed_balanced = [_or_group(intervention, pubmed=True), _or_group(disease or population, pubmed=True), _or_group(outcomes, pubmed=True)]
    if designs:
        pubmed_precision = pubmed_balanced + [_or_group(designs, pubmed=True)]
    else:
        pubmed_precision = pubmed_balanced

    strategies = [
        {
            "name": "broad_recall_query",
            "intended_mode": "high_recall",
            "query_string": " AND ".join(part for part in broad_parts if part),
            "expected_recall_precision_tradeoff": "Maximizes sensitivity by requiring core intervention and disease/population only; higher screening burden expected.",
            "included_concepts": ["intervention_exposure", "disease_or_population"],
            "excluded_concepts": ["outcomes", "study_design"],
            "rationale": "Use early to avoid missing sentinel or unexpected outcome records.",
        },
        {
            "name": "balanced_query",
            "intended_mode": "balanced",
            "query_string": " AND ".join(part for part in balanced_parts if part),
            "expected_recall_precision_tradeoff": "Balances recall and precision by adding outcome concepts while keeping study design open.",
            "included_concepts": ["intervention_exposure", "disease_or_population", "outcomes"],
            "excluded_concepts": ["study_design"],
            "rationale": "Default EvidenceOS search mode for most SLR starts.",
        },
        {
            "name": "precision_focused_query",
            "intended_mode": "high_precision",
            "query_string": " AND ".join(part for part in precision_parts if part),
            "expected_recall_precision_tradeoff": "Reduces screening burden by requiring outcome and design concepts; may miss sparsely indexed studies.",
            "included_concepts": ["intervention_exposure", "disease_or_population", "outcomes", "study_design"],
            "excluded_concepts": [],
            "rationale": "Use when the team prioritizes screening efficiency or already has sentinel recall coverage.",
        },
        {
            "name": "pubmed_boolean_query",
            "intended_mode": concepts.get("precision_mode", "balanced"),
            "query_string": " AND ".join(part for part in (pubmed_precision if concepts.get("precision_mode") == "high_precision" else pubmed_balanced) if part),
            "expected_recall_precision_tradeoff": "PubMed title/abstract Boolean strategy with explicit concept blocks.",
            "included_concepts": ["intervention_exposure", "disease_or_population", "outcomes"],
            "excluded_concepts": [] if concepts.get("precision_mode") == "high_precision" else ["study_design"],
            "rationale": "Use for the PubMed retrieval script.",
        },
        {
            "name": "semantic_scholar_query",
            "intended_mode": concepts.get("precision_mode", "balanced"),
            "query_string": " ".join((_primary_terms(concepts, "intervention_exposure")[:1] + (_primary_terms(concepts, "disease") or _primary_terms(concepts, "population"))[:1] + _primary_terms(concepts, "outcomes")[:2])),
            "expected_recall_precision_tradeoff": "Short metadata query suited to broad scholarly search ranking.",
            "included_concepts": ["intervention_exposure", "disease_or_population", "outcomes"],
            "excluded_concepts": ["most synonyms"],
            "rationale": "Semantic Scholar performs best with concise natural-language queries.",
        },
        {
            "name": "crossref_query",
            "intended_mode": concepts.get("precision_mode", "balanced"),
            "query_string": " ".join((_primary_terms(concepts, "intervention_exposure")[:1] + (_primary_terms(concepts, "disease") or _primary_terms(concepts, "population"))[:1] + _primary_terms(concepts, "outcomes")[:2])),
            "expected_recall_precision_tradeoff": "DOI metadata query for publication matching and enrichment.",
            "included_concepts": ["intervention_exposure", "disease_or_population", "outcomes"],
            "excluded_concepts": ["study_design filters"],
            "rationale": "Crossref works best as DOI-centered metadata enrichment, not full biomedical screening.",
        },
    ]
    return {"concepts": concepts, "strategies": strategies}


def _load_concepts(path: str | None, question: str | None, mode: str) -> dict:
    if path:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    if not question:
        raise ValueError("Provide --concepts-json or a question")
    return expand_concepts(question, mode)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate precision-aware search strategies.")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--concepts-json", help="JSON file from concept_expand.py")
    parser.add_argument("--precision-mode", choices=["high_recall", "balanced", "high_precision"], default="balanced")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_strategies(_load_concepts(args.concepts_json, args.question, args.precision_mode))
    except Exception as exc:
        print(f"search_strategy_optimizer.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
