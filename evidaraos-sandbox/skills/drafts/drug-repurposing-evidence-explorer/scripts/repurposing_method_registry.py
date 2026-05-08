#!/usr/bin/env python3
"""Describe drug-repurposing method families and their validation risks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


METHODS: list[dict[str, Any]] = [
    {
        "method_id": "knowledge_graph_reasoning",
        "method_family": "knowledge_graph",
        "purpose": "Surface drug-disease hypotheses from biomedical entity relationships and multi-hop paths.",
        "required_inputs": ["drug entities", "disease entities", "target/pathway relationships", "curated or extracted graph edges"],
        "typical_outputs": ["candidate links", "multi-hop evidence paths", "path rationale"],
        "validation_type": ["known indication holdout", "known contraindication holdout", "expert path review"],
        "false_positive_risks": [
            "co-occurrence mistaken for mechanism",
            "outdated or biased graph edges",
            "path exists but is not therapeutically actionable",
        ],
        "false_negative_risks": [
            "missing edges for rare diseases",
            "new mechanisms absent from graph",
            "drug effects not represented as graph relationships",
        ],
        "evidence_strength": "hypothesis_generation",
        "implementation_readiness": "mvp_transparent_rules",
        "human_review_required": True,
    },
    {
        "method_id": "network_medicine_proximity",
        "method_family": "network_medicine",
        "purpose": "Estimate whether drug targets are close to disease modules in biological networks.",
        "required_inputs": ["disease genes", "drug targets", "protein interaction network"],
        "typical_outputs": ["network proximity score", "target-disease module overlap"],
        "validation_type": ["approved indication enrichment", "permutation testing", "expert mechanism review"],
        "false_positive_risks": [
            "generic hub proteins inflate signal",
            "network proximity does not imply clinical efficacy",
            "disease module definition is incomplete",
        ],
        "false_negative_risks": [
            "unknown targets or sparse disease genes",
            "non-protein mechanisms missed",
            "context-specific biology absent from generic networks",
        ],
        "evidence_strength": "mechanistic_prioritization",
        "implementation_readiness": "requires_curated_network_data",
        "human_review_required": True,
    },
    {
        "method_id": "transcriptomic_signature_reversal",
        "method_family": "omics_signature",
        "purpose": "Compare disease expression signatures with drug perturbation signatures.",
        "required_inputs": ["disease expression signature", "drug perturbation signature", "cell/tissue context"],
        "typical_outputs": ["signature reversal score", "context match notes"],
        "validation_type": ["cell-line/tissue concordance", "known mechanism recovery", "orthogonal biology review"],
        "false_positive_risks": [
            "cell line is not disease-relevant",
            "reversal score reflects stress response rather than therapeutic mechanism",
            "dose/time mismatch",
        ],
        "false_negative_risks": [
            "no matching tissue or perturbation data",
            "drug effect is post-transcriptional",
            "heterogeneous disease subtypes diluted in signature",
        ],
        "evidence_strength": "orthogonal_biologic_signal",
        "implementation_readiness": "requires_external_signature_database",
        "human_review_required": True,
    },
    {
        "method_id": "target_based_repurposing",
        "method_family": "target_biology",
        "purpose": "Prioritize drugs whose known targets are implicated in the new disease.",
        "required_inputs": ["drug-target annotations", "target-disease associations", "directionality where available"],
        "typical_outputs": ["target plausibility score", "mechanism alignment notes"],
        "validation_type": ["target validation evidence", "directionality review", "safety transfer review"],
        "false_positive_risks": [
            "target association has wrong directionality",
            "drug modulation differs from desired biology",
            "target evidence is genetic but drug action is not comparable",
        ],
        "false_negative_risks": [
            "polypharmacology not captured",
            "unknown or secondary targets missing",
            "disease biology involves pathway context rather than single target",
        ],
        "evidence_strength": "mechanistic_plausibility",
        "implementation_readiness": "mvp_with_curated_target_inputs",
        "human_review_required": True,
    },
    {
        "method_id": "clinical_literature_signal",
        "method_family": "literature_and_trials",
        "purpose": "Detect clinical, preclinical, and trial evidence relevant to a repurposing hypothesis.",
        "required_inputs": ["PubMed records", "clinical trial records", "study design tags", "outcomes"],
        "typical_outputs": ["clinical evidence signal", "study design distribution", "evidence gaps"],
        "validation_type": ["systematic review", "trial registry verification", "human screening"],
        "false_positive_risks": [
            "review articles or editorials counted as primary evidence",
            "underpowered or uncontrolled studies over-weighted",
            "wrong population or comparator",
        ],
        "false_negative_risks": [
            "missed synonyms and indexing terms",
            "negative studies harder to retrieve",
            "unpublished or terminated trials absent",
        ],
        "evidence_strength": "clinical_context",
        "implementation_readiness": "mvp_search_and_screening",
        "human_review_required": True,
    },
    {
        "method_id": "real_world_usage_signal",
        "method_family": "real_world_data",
        "purpose": "Use reviewed external usage or co-prescription signals as contextual, confounded evidence.",
        "required_inputs": ["source description", "cohort definition", "drug exposure", "diagnosis/outcome", "bias controls"],
        "typical_outputs": ["usage signal", "confounding notes", "validation status"],
        "validation_type": ["cohort design review", "negative controls", "sensitivity analysis"],
        "false_positive_risks": [
            "channeling bias",
            "disease severity confounding",
            "drug prescribed for comorbidity rather than target disease",
        ],
        "false_negative_risks": [
            "low adoption or access barriers",
            "coding gaps",
            "insufficient follow-up",
        ],
        "evidence_strength": "contextual_signal_only",
        "implementation_readiness": "requires_governed_real_world_dataset",
        "human_review_required": True,
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit the EvidenceOS drug-repurposing methods registry.")
    parser.add_argument("--method-family", help="Filter by method family.")
    parser.add_argument("--output")
    args = parser.parse_args()

    methods = METHODS
    if args.method_family:
        methods = [method for method in METHODS if method["method_family"] == args.method_family]

    result = {
        "registry_name": "EvidenceOS Drug Repurposing Methods Registry",
        "fixture_only": False,
        "methods": methods,
        "summary": {"method_count": len(methods), "human_review_required": True},
        "limitations": [
            "The registry describes method families and failure modes; it is not a benchmark.",
            "EvidenceOS should not claim performance without human-labeled validation data.",
        ],
    }
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
