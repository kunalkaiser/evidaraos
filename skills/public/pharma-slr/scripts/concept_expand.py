#!/usr/bin/env python3
"""Expand a biomedical review question into structured search concepts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any


DRUG_VARIANTS = {
    "dupilumab": ["Dupixent", "IL-4 receptor alpha antagonist", "IL-4R alpha", "anti-IL-4R"],
    "omalizumab": ["Xolair", "anti-IgE"],
    "tralokinumab": ["Adtralza", "Adbry", "anti-IL-13"],
    "lecanemab": ["Leqembi", "BAN2401"],
    "semaglutide": ["Ozempic", "Wegovy", "Rybelsus", "GLP-1 receptor agonist"],
}

DISEASE_SYNONYMS = {
    "atopic dermatitis": ["eczema", "dermatitis, atopic"],
    "asthma": ["bronchial asthma"],
    "alzheimer": ["Alzheimer disease", "Alzheimer's disease"],
    "psoriasis": ["psoriatic disease"],
    "rheumatoid arthritis": ["RA", "arthritis, rheumatoid"],
}

OUTCOME_SYNONYMS = {
    "safety": ["adverse events", "adverse effects", "toxicity", "tolerability"],
    "efficacy": ["effectiveness", "treatment outcome", "clinical response"],
    "mortality": ["death", "survival"],
    "incidence": ["risk", "rate", "occurrence"],
    "prevalence": ["burden", "frequency"],
}

STUDY_DESIGN_TERMS = {
    "randomized": ["randomized controlled trial", "RCT", "clinical trial"],
    "real-world": ["observational study", "registry", "cohort", "claims"],
    "cohort": ["cohort study", "observational"],
    "case": ["case report", "case series"],
    "meta-analysis": ["systematic review", "meta-analysis"],
}


def _find_terms(text: str, dictionary: dict[str, list[str]]) -> tuple[list[str], dict[str, list[str]]]:
    found: list[str] = []
    synonyms: dict[str, list[str]] = {}
    lowered = text.lower()
    for term, variants in dictionary.items():
        if term in lowered or any(variant.lower() in lowered for variant in variants):
            found.append(term)
            synonyms[term] = variants
    return found, synonyms


def _guess_population(question: str, disease_terms: list[str]) -> str:
    match = re.search(r"\b(?:in|among|with|for)\s+(.+?)(?:\?|$)", question, re.I)
    if match:
        return match.group(1).strip(" .?")
    return disease_terms[0] if disease_terms else ""


def _token_candidates(question: str) -> list[str]:
    stop = {
        "what", "which", "does", "do", "the", "and", "or", "for", "with", "among", "patients",
        "patient", "adults", "children", "safety", "efficacy", "effectiveness", "risk", "review",
    }
    return [word for word in re.findall(r"[A-Za-z][A-Za-z0-9-]+", question) if word.lower() not in stop]


def expand_concepts(question: str, precision_mode: str = "balanced") -> dict:
    disease, disease_synonyms = _find_terms(question, DISEASE_SYNONYMS)
    drugs, drug_synonyms = _find_terms(question, DRUG_VARIANTS)
    outcomes, outcome_synonyms = _find_terms(question, OUTCOME_SYNONYMS)
    designs, design_synonyms = _find_terms(question, STUDY_DESIGN_TERMS)

    candidates = _token_candidates(question)
    intervention = drugs[0] if drugs else (candidates[0] if candidates else "")
    disease_value = disease[0] if disease else ""
    if not outcomes:
        outcomes = ["safety"] if "adverse" in question.lower() else ["clinical outcomes"]

    concepts = {
        "question": question,
        "precision_mode": precision_mode,
        "disease": disease_value,
        "intervention_exposure": intervention,
        "comparator": "not specified",
        "outcomes": outcomes,
        "population": _guess_population(question, disease),
        "study_design": designs,
        "synonyms": {
            "disease": disease_synonyms,
            "intervention_exposure": drug_synonyms,
            "outcomes": outcome_synonyms,
            "study_design": design_synonyms,
        },
        "mesh_like_terms": {
            "disease": [variant for term in disease for variant in disease_synonyms.get(term, []) if "," in variant],
            "intervention_exposure": [intervention] if intervention else [],
            "outcomes": [variant for term in outcomes for variant in outcome_synonyms.get(term, [])],
        },
        "drug_brand_generic_variants": drug_synonyms,
    }
    return concepts


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a biomedical question into structured concepts for precision-controlled SLR search.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Example:\n  python concept_expand.py "dupilumab atopic dermatitis safety" --precision-mode balanced\n',
    )
    parser.add_argument("question")
    parser.add_argument("--precision-mode", choices=["high_recall", "balanced", "high_precision"], default="balanced")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = expand_concepts(args.question, args.precision_mode)
    except Exception as exc:
        print(f"concept_expand.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
