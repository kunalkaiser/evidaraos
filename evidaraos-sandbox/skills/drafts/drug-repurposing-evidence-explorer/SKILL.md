---
name: drug-repurposing-evidence-explorer
display_name: EvidaraOS Drug Repurposing Evidence Explorer
version: 1.0.0
author: Evidara OS
description: >
  EvidaraOS skill for drug repurposing evidence exploration. Supports
  compound-to-indication and indication-to-compound workflows with mechanistic
  plausibility, clinical evidence, safety transfer, knowledge-graph hypothesis
  generation, unmet need, and validation readiness scoring.
compatibility: ">=2.0.0"
tags:
  - drug-repurposing
  - translational-science
  - target-disease
  - safety-transfer
  - clinical-evidence
  - biomedical-nlp
  - knowledge-graph
---

# EvidaraOS Drug Repurposing Evidence Explorer

## Runtime and Attribution

This is an EvidaraOS workflow built on the credited DeerFlow open-source agent runtime/harness.

## Purpose

Identify and rank repurposing hypotheses from literature, target biology, safety-transfer evidence, and transparent graph paths. Every candidate remains a mechanistic hypothesis requiring clinical validation.

## Modes

- `compound_to_indications`
- `indication_to_compounds`
- `zero_shot_disease_to_candidates`

## Workflow

Before executing, read `references/methodology.md` for NCATS, Open Targets, and ChEMBL anchors.

1. Detect workflow mode.
2. Build compound or disease profile.
3. Map mechanisms and disease associations.
4. Search/structure clinical signal evidence.
5. Assess safety transfer.
6. Score candidates.
7. Generate validation checklist.

## Zero-Shot and Clinician-Centered Review Layer

This layer is inspired by current scientific work on graph-based, clinician-centered drug repurposing, but it is an original EvidenceOS workflow. It does not copy TxGNN code, wording, figures, or benchmark claims, and it must not be described as TxGNN.

Use it when the question concerns diseases with limited treatment options, sparse evidence, rare disease contexts, or hypotheses that require multi-hop explanation review.

1. Compare diseases by transparent shared features such as genes, pathways, phenotypes, symptoms, exposures, and related diseases.
2. Separate indication signals from contraindication or safety-risk signals.
3. Rank zero-shot hypotheses using graph-path support, similar-disease support, and safety penalties.
4. Rank multi-hop explanation paths for expert review.
5. Create an explanation review queue covering plausibility, usefulness, safety concern, missing evidence, and overclaim risk.
6. Optionally attach external usage signals only when the user provides reviewed data.
7. Preserve fixture-only warnings and avoid performance claims without benchmark data.

## NLP and Knowledge Graph Layer

Use this layer when the project needs literature-scale signal extraction rather than only manually curated candidate scoring.

1. Extract biomedical entities from title, abstract, full-text, or table-like records.
2. Extract relation candidates such as `inhibits`, `activates`, `treats`, `associated_with`, `adverse_event_of`, and `biomarker_of`.
3. Build a transparent drug-target-pathway-disease knowledge graph.
4. Generate drug-disease candidate links from direct and two-hop graph paths.
5. Explain why each candidate was surfaced.
6. Run living evidence monitoring when a new search snapshot is available.
7. Route all candidate links and evidence paths through human review and audit trail.

This MVP uses deterministic dictionaries and pattern matching. It is intentionally auditable, but it is not a trained biomedical NER or causal inference system.

## Method-Governed Repurposing Layer

Use this layer when the user asks whether EvidenceOS should incorporate a new paper, model family, or drug-repurposing method. Do not clone every paper into a separate workflow. Convert the paper into a method-family entry, evidence signal type, validation requirement, and failure-mode profile.

Supported method families:

- knowledge-graph reasoning
- network-medicine proximity
- transcriptomic or perturbational signature reversal
- target-based repurposing
- clinical literature and trial signal mining
- reviewed real-world usage signal

For each method, preserve:

1. Required inputs.
2. Output signal type.
3. Validation design.
4. False-positive risks.
5. False-negative risks.
6. Implementation readiness.
7. Human review requirements.

The goal is not to claim that EvidenceOS has proven a model. The goal is to compare independent evidence signals, expose gaps, and create a validation plan before any product, clinical, investment, or regulatory use.

## Required Commands

```bash
python skills/public/drug-repurposing-evidence-explorer/scripts/mode_detector.py "Could dupilumab be repurposed for another inflammatory disease?"
python skills/public/drug-repurposing-evidence-explorer/scripts/repurposing_score.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/candidates.sample.json
python skills/public/drug-repurposing-evidence-explorer/scripts/validation_checklist.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/candidates.sample.json
python skills/public/drug-repurposing-evidence-explorer/scripts/target_evidence_matrix.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/target_evidence.sample.json
python skills/public/drug-repurposing-evidence-explorer/scripts/safety_transfer_assessment.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/candidates.sample.json
```

Knowledge graph workflow:

```bash
python skills/public/drug-repurposing-evidence-explorer/scripts/entity_extraction.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/literature_records.sample.json --output entities.json
python skills/public/drug-repurposing-evidence-explorer/scripts/relation_extraction.py entities.json --records-json skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/literature_records.sample.json --output relations.json
python skills/public/drug-repurposing-evidence-explorer/scripts/knowledge_graph_builder.py relations.json --output graph.json
python skills/public/drug-repurposing-evidence-explorer/scripts/repurposing_link_prediction.py graph.json --output candidate_links.json
python skills/public/drug-repurposing-evidence-explorer/scripts/evidence_path_explainer.py candidate_links.json --output path_explanations.json --markdown-output path_explanations.md
python skills/public/drug-repurposing-evidence-explorer/scripts/full_text_signal_extraction.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/literature_records.sample.json --output full_text_signals.json
python skills/public/drug-repurposing-evidence-explorer/scripts/living_evidence_monitor.py --current candidate_links.json --output living_monitor.json
```

Zero-shot explanation workflow:

```bash
python skills/public/drug-repurposing-evidence-explorer/scripts/disease_similarity.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/disease_features.sample.json --query-disease asthma --output disease_similarity.json
python skills/public/drug-repurposing-evidence-explorer/scripts/indication_contraindication_score.py candidate_links.json --output indication_contraindication.json
python skills/public/drug-repurposing-evidence-explorer/scripts/zero_shot_candidate_ranker.py --candidates indication_contraindication.json --disease-similarity disease_similarity.json --output zero_shot_candidates.json
python skills/public/drug-repurposing-evidence-explorer/scripts/multi_hop_path_ranker.py zero_shot_candidates.json --output ranked_paths.json
python skills/public/drug-repurposing-evidence-explorer/scripts/explanation_review_queue.py ranked_paths.json --reviewer-id reviewer_001 --output explanation_review_queue.json
python skills/public/drug-repurposing-evidence-explorer/scripts/external_usage_signal.py --candidates zero_shot_candidates.json --usage-signals skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/external_usage_signals.sample.json --output usage_augmented_candidates.json
```

Method-governed comparison workflow:

```bash
python skills/public/drug-repurposing-evidence-explorer/scripts/repurposing_method_registry.py --output method_registry.json
python skills/public/drug-repurposing-evidence-explorer/scripts/method_evidence_matrix.py skills/public/drug-repurposing-evidence-explorer/evals/example_fixture/method_signals.sample.json --output method_matrix.json
python skills/public/drug-repurposing-evidence-explorer/scripts/model_signal_comparator.py method_matrix.json --output signal_comparison.json
python skills/public/drug-repurposing-evidence-explorer/scripts/false_positive_risk_assessor.py signal_comparison.json --output false_positive_risk.json
python skills/public/drug-repurposing-evidence-explorer/scripts/false_negative_gap_checker.py method_matrix.json --output false_negative_gaps.json
python skills/public/drug-repurposing-evidence-explorer/scripts/repurposing_validation_plan.py --comparison signal_comparison.json --false-positive false_positive_risk.json --false-negative false_negative_gaps.json --output validation_plan.json
```

## Human Review

Never present candidates as recommended therapy. Label each candidate as hypothesis-only and route for scientific review.

Run shared governance after scoring and safety transfer assessment:

```bash
python skills/public/drug-repurposing-evidence-explorer/scripts/human_review_queue.py ranked_candidates.json --module drug-repurposing-evidence-explorer --reviewer-id reviewer_001
python skills/public/drug-repurposing-evidence-explorer/scripts/audit_trail.py --review-id <project_id> --module drug-repurposing-evidence-explorer --events review_queue.json
python skills/public/drug-repurposing-evidence-explorer/scripts/validation_report.py --module drug-repurposing-evidence-explorer --review-queue review_queue.json --audit-summary audit_summary.json
python skills/public/drug-repurposing-evidence-explorer/scripts/project_manifest.py --project-id <project_id> --module drug-repurposing-evidence-explorer --structured-outputs ranked_candidates.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not upgrade target-disease association to therapeutic benefit.
- Do not treat co-mention, relation extraction, or graph path scoring as causal proof.
- Do not claim TxGNN-level or foundation-model performance unless an actual validated model integration and benchmark exist.
- Do not turn a single research article into a product claim. Convert it into a method-family signal with explicit validation requirements.
- Do not hide false-positive and false-negative risks.
- Do not use external usage signals as causal evidence.
- Do not ignore safety-transfer differences in new populations.
- Every ranked candidate must include transparent reasons and validation gaps.
- Every generated hypothesis must be labeled as hypothesis-only and routed to human review before product, clinical, regulatory, or investment use.
