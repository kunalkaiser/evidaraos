# Drug Repurposing Evidence Explorer Methodology Notes

Use these sources as methodological anchors when building or reviewing repurposing outputs.

## Translational Science Anchor

NCATS describes translational science as developing and improving processes that move observations into health solutions, including finding, designing, and testing molecules with therapeutic potential.

Source:

- NCATS overview: https://ncats.nih.gov/about/ncats-overview/strategic-plan/overview-of-ncats
- NCATS drug discovery/development impact: https://ncats.nih.gov/preclinical/repurpose

## Target-Disease Evidence Anchor

Open Targets aggregates target-disease evidence from multiple sources, standardizes evidence to reference target and disease identifiers, and provides scoring frameworks by source/data type.

Sources:

- Evidence docs: https://platform-docs.opentargets.org/evidence
- Association docs: https://platform-docs.opentargets.org/associations

## Compound / Target Anchor

ChEMBL is an open data bioactivity database with binding, functional, and ADMET information curated from the literature.

Source:

- https://pubmed.ncbi.nlm.nih.gov/21948594/

## Graph-Based Repurposing Anchor

Recent graph-based repurposing work highlights useful product patterns for EvidenceOS:

- zero-shot hypothesis generation for diseases with limited treatment options
- disease similarity and knowledge transfer across related mechanisms
- separate therapeutic indication and contraindication reasoning
- multi-hop explanation paths that human experts can inspect
- human evaluation of explanation usefulness and trust
- optional real-world usage signals that require careful confounding review

Methodological anchor:

- Huang, K. et al. A foundation model for clinician-centered drug repurposing. Nature Medicine 30, 3601-3613 (2024). https://doi.org/10.1038/s41591-024-03233-x

EvidenceOS uses these as design guidance only. Do not copy article language, figures, code, or benchmark claims into product outputs.

## Evidence Axes

Score candidates on:

- mechanism plausibility
- target-disease association
- directionality fit
- existing clinical evidence
- biomedical entity and relation evidence
- graph-path support
- safety transfer
- drug-drug interaction burden
- development feasibility
- unmet need
- regulatory path plausibility

## Method Registry Axes

When reviewing additional drug-repurposing papers, classify the method rather than copying the paper into the product. Capture:

- method family
- required data inputs
- generated signal type
- validation design
- false-positive risks
- false-negative risks
- evidence strength
- implementation readiness
- human review requirement

Common method families include knowledge graph reasoning, network medicine proximity, transcriptomic signature reversal, target-based repurposing, clinical literature or trial mining, and reviewed real-world usage signals. Agreement across families can prioritize review, but it does not prove efficacy. Disagreement or missing method coverage must remain visible in the report.

## Prohibited Behavior

- Do not present candidates as recommended treatment.
- Do not upgrade target association to proven therapeutic benefit.
- Do not ignore population-specific safety risk.
- Do not rank candidates without transparent rationale.
- Do not treat co-mentions or extracted relations as causal proof.
- Do not represent zero-shot hypotheses as validated therapeutic predictions.
- Do not claim foundation-model performance unless a validated model and benchmark are actually integrated.
- Do not present method agreement as proof.
- Do not suppress false-positive or false-negative risks.
