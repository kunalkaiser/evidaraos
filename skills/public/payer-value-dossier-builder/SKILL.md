---
name: payer-value-dossier-builder
display_name: EvidaraOS Payer Value Dossier Builder
version: 1.0.0
author: Evidara OS
description: >
  EvidaraOS skill for building payer value dossier evidence packages.
  Structures disease burden, unmet need, clinical evidence, comparator
  landscape, HEOR assumptions, HTA precedents, and claim traceability.
compatibility: ">=2.0.0"
tags:
  - payer
  - market-access
  - value-dossier
  - HTA
  - HEOR
  - claim-traceability
---

# EvidaraOS Payer Value Dossier Builder

## Runtime and Attribution

This is an EvidaraOS workflow built on the credited DeerFlow open-source agent runtime/harness.

## Purpose

Create evidence-traceable payer dossier drafts. Do not predict payer decisions, reimbursement outcomes, or pricing acceptance.

## Workflow

Before executing, read `references/methodology.md` for AMCP Format anchors and payer dossier evidence blocks.

1. Define dossier scope.
2. Build disease burden and unmet need summary.
3. Extract clinical evidence.
4. Build comparator landscape.
5. Capture HTA/payer precedents.
6. Build claim traceability matrix.
7. Check dossier section completeness and unsupported claims.
8. Build auditable evidence maps and living-evidence update checks for dossier claims.
9. Generate dossier sections.
10. Route claims for human review.

## Required Commands

```bash
python skills/public/payer-value-dossier-builder/scripts/dossier_scope.py --product "dupilumab" --indication "atopic dermatitis" --market "US"
python skills/public/payer-value-dossier-builder/scripts/claim_traceability.py skills/public/payer-value-dossier-builder/evals/example_fixture/claims.sample.json
python skills/public/payer-value-dossier-builder/scripts/dossier_outline.py skills/public/payer-value-dossier-builder/evals/example_fixture/scope.sample.json
python skills/public/payer-value-dossier-builder/scripts/dossier_gap_check.py --scope skills/public/payer-value-dossier-builder/evals/example_fixture/scope.sample.json --claims skills/public/payer-value-dossier-builder/evals/example_fixture/claims.sample.json
```

Evidence-intelligence workflow:

```bash
python skills/public/payer-value-dossier-builder/scripts/evidence_signal_extraction.py skills/public/payer-value-dossier-builder/evals/example_fixture/claims.sample.json --output payer_signals.json
python skills/public/payer-value-dossier-builder/scripts/evidence_map_builder.py payer_signals.json --output payer_evidence_map.json
python skills/public/payer-value-dossier-builder/scripts/evidence_path_explainer.py payer_evidence_map.json --output payer_paths.json --markdown-output payer_paths.md
python skills/public/payer-value-dossier-builder/scripts/living_evidence_monitor.py --current payer_evidence_map.json --output payer_living_update.json
```

## Human Review

Every claim must trace to a source or be labeled as unsupported. All payer strategy language requires human market-access review.

Run shared governance after claim traceability:

```bash
python skills/public/payer-value-dossier-builder/scripts/human_review_queue.py claim_traceability.json --module payer-value-dossier-builder --reviewer-id reviewer_001
python skills/public/payer-value-dossier-builder/scripts/audit_trail.py --review-id <project_id> --module payer-value-dossier-builder --events review_queue.json
python skills/public/payer-value-dossier-builder/scripts/validation_report.py --module payer-value-dossier-builder --review-queue review_queue.json --audit-summary audit_summary.json
python skills/public/payer-value-dossier-builder/scripts/project_manifest.py --project-id <project_id> --module payer-value-dossier-builder --structured-outputs claim_traceability.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not predict payer decisions, access outcomes, or formulary placement.
- Do not leave unsupported claims in final output.
- Economic claims must be sourced, modeled, or labeled as assumptions.
- Evidence maps organize claim-support signals; they do not validate payer acceptance.
