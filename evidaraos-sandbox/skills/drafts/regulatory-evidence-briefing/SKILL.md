---
name: regulatory-evidence-briefing
display_name: EvidaraOS Regulatory Evidence Briefing
version: 0.1.0-draft
author: Evidara OS
description: >
  Draft EvidaraOS skill for conservative regulatory evidence briefings.
  Structures agency context, precedents, benefit-risk evidence, uncertainty,
  source provenance, and human regulatory review queues.
compatibility: ">=2.0.0"
tags:
  - regulatory
  - FDA
  - EMA
  - benefit-risk
  - evidence-briefing
  - governance
---

# EvidaraOS Regulatory Evidence Briefing

## Runtime and Attribution

This is an EvidaraOS workflow draft intended to run on the credited DeerFlow open-source agent runtime/harness after promotion.

## Purpose

Create conservative, traceable regulatory evidence briefings. Never predict regulatory approval or replace regulatory affairs review.

## Workflow

Before executing, read `references/methodology.md` for FDA and EMA benefit-risk anchors.

1. Define regulatory context.
2. Retrieve/publicly summarize agency precedents.
3. Structure benefit-risk evidence.
4. Capture residual uncertainty.
5. Check submission-style language for overclaiming.
6. Build human regulatory review queue.
7. Produce briefing and source appendix.

## Required Commands

```bash
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/regulatory_context.py --product "dupilumab" --indication "atopic dermatitis" --agency FDA --stage "post-market"
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/benefit_risk_table.py evals/example_fixture/evidence.sample.json
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/language_guardrail.py evals/example_fixture/claims.sample.json
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/uncertainty_register.py evals/example_fixture/evidence.sample.json
```

## Human Review

All briefing outputs require regulatory expert review. Use conservative language and cite public sources.

Run shared governance after benefit-risk and uncertainty outputs:

```bash
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/human_review_queue.py benefit_risk.json --module regulatory-evidence-briefing --reviewer-id reviewer_001
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/audit_trail.py --review-id <project_id> --module regulatory-evidence-briefing --events review_queue.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/validation_report.py --module regulatory-evidence-briefing --review-queue review_queue.json --audit-summary audit_summary.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/project_manifest.py --project-id <project_id> --module regulatory-evidence-briefing --structured-outputs benefit_risk.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not predict approval.
- Do not say evidence proves safety or efficacy.
- Separate evidence, uncertainty, and interpretation.
