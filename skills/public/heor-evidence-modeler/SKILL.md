---
name: heor-evidence-modeler
display_name: EvidaraOS HEOR Evidence Modeler
version: 1.0.0
author: Evidara OS
description: >
  EvidaraOS skill for HEOR evidence modeling. Builds structured,
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

This is an EvidaraOS workflow built on the credited DeerFlow open-source agent runtime/harness. Keep DeerFlow MIT attribution intact.

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
8. Build auditable evidence maps and living-evidence update checks for model inputs.
9. Create health economist review queue.
10. Produce model input table, assumption register, evidence readiness summary, and limitations.

## Required Commands

```bash
python skills/public/heor-evidence-modeler/scripts/model_scope.py --condition "atopic dermatitis" --intervention "dupilumab" --comparator "standard of care" --perspective "US payer"
python skills/public/heor-evidence-modeler/scripts/model_input_table.py skills/public/heor-evidence-modeler/evals/example_fixture/inputs.sample.json
python skills/public/heor-evidence-modeler/scripts/assumption_register.py skills/public/heor-evidence-modeler/evals/example_fixture/inputs.sample.json
python skills/public/heor-evidence-modeler/scripts/evidence_readiness.py skills/public/heor-evidence-modeler/evals/example_fixture/inputs.sample.json
```

Evidence-intelligence workflow:

```bash
python skills/public/heor-evidence-modeler/scripts/evidence_signal_extraction.py skills/public/heor-evidence-modeler/evals/example_fixture/inputs.sample.json --output heor_signals.json
python skills/public/heor-evidence-modeler/scripts/evidence_map_builder.py heor_signals.json --output heor_evidence_map.json
python skills/public/heor-evidence-modeler/scripts/evidence_path_explainer.py heor_evidence_map.json --output heor_paths.json --markdown-output heor_paths.md
python skills/public/heor-evidence-modeler/scripts/living_evidence_monitor.py --current heor_evidence_map.json --output heor_living_update.json
```

## Human Review

All model inputs require health economist validation. Label missing source data as `assumption_required`; do not invent values.

Run shared governance after model input extraction:

```bash
python skills/public/heor-evidence-modeler/scripts/human_review_queue.py model_inputs.json --module heor-evidence-modeler --reviewer-id reviewer_001
python skills/public/heor-evidence-modeler/scripts/audit_trail.py --review-id <project_id> --module heor-evidence-modeler --events review_queue.json
python skills/public/heor-evidence-modeler/scripts/validation_report.py --module heor-evidence-modeler --review-queue review_queue.json --audit-summary audit_summary.json
python skills/public/heor-evidence-modeler/scripts/project_manifest.py --project-id <project_id> --module heor-evidence-modeler --structured-outputs model_inputs.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not generate final ICER, QALY, or budget impact claims unless a validated model artifact is provided.
- Every input must have a source, uncertainty range, or assumption flag.
- Evidence maps organize model-input signals; they do not validate economic model correctness.
- Fixture data is smoke-test only and never validation evidence.
