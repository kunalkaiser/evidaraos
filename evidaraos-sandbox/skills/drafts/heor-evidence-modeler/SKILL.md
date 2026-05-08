---
name: heor-evidence-modeler
display_name: EvidaraOS HEOR Evidence Modeler
version: 0.1.0-draft
author: Evidara OS
description: >
  Draft EvidaraOS skill for HEOR evidence modeling. Builds structured,
  source-traceable model input candidates for utilities, event rates, costs,
  resource utilization, assumptions, uncertainty ranges, and evidence gaps.
  All outputs require qualified health economist review before use.
compatibility: ">=2.0.0"
tags:
  - HEOR
  - health-economics
  - model-inputs
  - QALY
  - utility
  - pharmacoeconomics
  - evidence-governance
---

# EvidaraOS HEOR Evidence Modeler

## Runtime and Attribution

This is an EvidaraOS workflow draft intended to run on the credited DeerFlow open-source agent runtime/harness after promotion. Keep DeerFlow MIT attribution intact.

## Purpose

Turn biomedical literature and public evidence into structured HEOR model input candidates for human health economist review. This skill does not produce final cost-effectiveness results.

## Workflow

Before executing, read `references/methodology.md` for CHEERS, ISPOR-SMDM, and budget impact practice anchors.

1. Define model scope and decision problem.
2. Generate HEOR evidence needs by model type.
3. Extract utility, event-rate, cost, resource-use, discontinuation, mortality, and adverse-event inputs.
4. Build model input tables with source provenance and uncertainty fields.
5. Build an assumption register for missing or weak inputs.
6. Score evidence readiness.
7. Flag model structure, uncertainty, and validation gaps.
8. Create health economist review queue.
9. Produce model input table, assumption register, evidence readiness summary, and limitations.

## Required Commands

```bash
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/model_scope.py --condition "atopic dermatitis" --intervention "dupilumab" --comparator "standard of care" --perspective "US payer"
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/model_input_table.py evals/example_fixture/inputs.sample.json
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/assumption_register.py evals/example_fixture/inputs.sample.json
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/evidence_readiness.py evals/example_fixture/inputs.sample.json
```

## Human Review

All model inputs require health economist validation. Label missing source data as `assumption_required`; do not invent values.

Run shared governance after model input extraction:

```bash
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/human_review_queue.py model_inputs.json --module heor-evidence-modeler --reviewer-id reviewer_001
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/audit_trail.py --review-id <project_id> --module heor-evidence-modeler --events review_queue.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/validation_report.py --module heor-evidence-modeler --review-queue review_queue.json --audit-summary audit_summary.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/project_manifest.py --project-id <project_id> --module heor-evidence-modeler --structured-outputs model_inputs.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not generate final ICER, QALY, or budget impact claims unless a validated model artifact is provided.
- Every input must have a source, uncertainty range, or assumption flag.
- Fixture data is smoke-test only and never validation evidence.
