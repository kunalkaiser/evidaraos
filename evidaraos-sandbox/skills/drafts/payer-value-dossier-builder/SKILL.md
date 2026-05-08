---
name: payer-value-dossier-builder
display_name: EvidaraOS Payer Value Dossier Builder
version: 0.1.0-draft
author: Evidara OS
description: >
  Draft EvidaraOS skill for building payer value dossier evidence packages.
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

This is an EvidaraOS workflow draft intended to run on the credited DeerFlow open-source agent runtime/harness after promotion.

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
8. Generate dossier sections.
9. Route claims for human review.

## Required Commands

```bash
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/dossier_scope.py --product "dupilumab" --indication "atopic dermatitis" --market "US"
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/claim_traceability.py evals/example_fixture/claims.sample.json
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/dossier_outline.py evals/example_fixture/scope.sample.json
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/dossier_gap_check.py --scope evals/example_fixture/scope.sample.json --claims evals/example_fixture/claims.sample.json
```

## Human Review

Every claim must trace to a source or be labeled as unsupported. All payer strategy language requires human market-access review.

Run shared governance after claim traceability:

```bash
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/human_review_queue.py claim_traceability.json --module payer-value-dossier-builder --reviewer-id reviewer_001
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/audit_trail.py --review-id <project_id> --module payer-value-dossier-builder --events review_queue.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/validation_report.py --module payer-value-dossier-builder --review-queue review_queue.json --audit-summary audit_summary.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/project_manifest.py --project-id <project_id> --module payer-value-dossier-builder --structured-outputs claim_traceability.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not predict payer decisions, access outcomes, or formulary placement.
- Do not leave unsupported claims in final output.
- Economic claims must be sourced, modeled, or labeled as assumptions.
