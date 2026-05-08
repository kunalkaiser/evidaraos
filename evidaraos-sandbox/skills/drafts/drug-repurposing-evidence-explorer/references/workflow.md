# Drug Repurposing Evidence Explorer Workflow

Candidates are mechanistic hypotheses. Score transparently and require scientific review.

Never upgrade target-disease association to therapeutic benefit.

## Literature-to-Graph Expansion

For projects that require broader discovery, add a transparent NLP and graph pass:

1. Extract drugs, diseases, genes/proteins, pathways, adverse events, phenotypes, and biomarkers from literature records.
2. Extract relation candidates using auditable patterns and co-mention evidence.
3. Build a graph of entities and evidence-backed edges.
4. Score direct and two-hop drug-disease candidate paths.
5. Explain evidence paths in plain language.
6. Compare current and previous candidate snapshots for living evidence updates.
7. Route graph-derived hypotheses through human review, validation reporting, and audit trail.

Graph-derived candidates are hypothesis-generation outputs only. They should never be represented as established efficacy, safety, or clinical utility without human-reviewed source evidence.

## Zero-Shot Explanation Review

When the disease has limited treatment options or sparse evidence:

1. Build disease feature sets from genes, pathways, phenotypes, symptoms, exposures, and related diseases.
2. Identify mechanistically similar diseases with transparent shared-feature rationale.
3. Separate candidate support into indication and contraindication signal scores.
4. Combine graph-path support and similar-disease support into a zero-shot hypothesis ranking.
5. Rank multi-hop paths for explanation review.
6. Route explanations to scientific reviewers for plausibility, usefulness, safety concern, missing evidence, and overclaim risk.
7. Attach external usage signals only if reviewed data is provided; never treat usage enrichment as causal validation.

This workflow is inspired by published graph-based repurposing methods but is not a foundation model and must not be marketed as validated zero-shot performance.

## Method-Governed Evidence Comparison

When many papers or model families are relevant:

1. Register each method family with inputs, outputs, validation design, and failure modes.
2. Build a candidate-by-method evidence matrix.
3. Compare supportive, conflicting, unavailable, and unknown signals.
4. Assess false-positive risk from conflicting signals, limited support, and unavailable coverage.
5. Assess false-negative risk from missing method families, sparse disease data, and recall gaps.
6. Generate a validation plan before any claim is made.
7. Keep fixture-only warnings in every smoke-test output.

This layer turns research literature into governed EvidenceOS method signals. It does not imply that EvidenceOS has reproduced any paper's model, benchmark, or clinical performance.
