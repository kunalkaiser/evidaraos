---
name: regulatory-evidence-briefing
display_name: EvidaraOS Regulatory Evidence Briefing
version: 1.0.0
author: Evidara OS
description: >
  EvidaraOS skill for conservative regulatory evidence briefings.
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

This is an EvidaraOS workflow built on the credited DeerFlow open-source agent runtime/harness.

## Purpose

Create conservative, traceable regulatory evidence briefings. Never predict regulatory approval or replace regulatory affairs review.

## Workflow

Before executing, read `references/methodology.md` for FDA and EMA benefit-risk anchors.

1. Define regulatory context.
2. Retrieve/publicly summarize agency precedents.
3. Structure benefit-risk evidence.
4. Capture residual uncertainty.
5. Check submission-style language for overclaiming.
6. Build auditable evidence maps and living-evidence update checks for briefing sources.
7. Build human regulatory review queue.
8. Produce briefing and source appendix.

## Required Commands

```bash
python skills/public/regulatory-evidence-briefing/scripts/regulatory_context.py --product "dupilumab" --indication "atopic dermatitis" --agency FDA --stage "post-market"
python skills/public/regulatory-evidence-briefing/scripts/benefit_risk_table.py skills/public/regulatory-evidence-briefing/evals/example_fixture/evidence.sample.json
python skills/public/regulatory-evidence-briefing/scripts/language_guardrail.py skills/public/regulatory-evidence-briefing/evals/example_fixture/claims.sample.json
python skills/public/regulatory-evidence-briefing/scripts/uncertainty_register.py skills/public/regulatory-evidence-briefing/evals/example_fixture/evidence.sample.json
```

Evidence-intelligence workflow:

```bash
python skills/public/regulatory-evidence-briefing/scripts/evidence_signal_extraction.py skills/public/regulatory-evidence-briefing/evals/example_fixture/evidence.sample.json --output regulatory_signals.json
python skills/public/regulatory-evidence-briefing/scripts/evidence_map_builder.py regulatory_signals.json --output regulatory_evidence_map.json
python skills/public/regulatory-evidence-briefing/scripts/evidence_path_explainer.py regulatory_evidence_map.json --output regulatory_paths.json --markdown-output regulatory_paths.md
python skills/public/regulatory-evidence-briefing/scripts/living_evidence_monitor.py --current regulatory_evidence_map.json --output regulatory_living_update.json
```

## Human Review

All briefing outputs require regulatory expert review. Use conservative language and cite public sources.

Run shared governance after benefit-risk and uncertainty outputs:

```bash
python skills/public/regulatory-evidence-briefing/scripts/human_review_queue.py benefit_risk.json --module regulatory-evidence-briefing --reviewer-id reviewer_001
python skills/public/regulatory-evidence-briefing/scripts/audit_trail.py --review-id <project_id> --module regulatory-evidence-briefing --events review_queue.json
python skills/public/regulatory-evidence-briefing/scripts/validation_report.py --module regulatory-evidence-briefing --review-queue review_queue.json --audit-summary audit_summary.json
python skills/public/regulatory-evidence-briefing/scripts/project_manifest.py --project-id <project_id> --module regulatory-evidence-briefing --structured-outputs benefit_risk.json --review-queue review_queue.json --audit-trail audit_summary.json --validation-report validation_report.md
```

## Output Guardrails

- Do not predict approval.
- Do not say evidence proves safety or efficacy.
- Separate evidence, uncertainty, and interpretation.
- Evidence maps organize benefit-risk signals; they do not validate regulatory acceptability.
