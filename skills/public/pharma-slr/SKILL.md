---
name: pharma-slr
display_name: EvidenceOS Precision-Controlled Pharmaceutical SLR
version: 1.2.0
author: EvidenceOS
description: >
  DeerFlow-powered EvidenceOS biomedical systematic literature review skill with
  precision-controlled retrieval. Supports PICO/PECO protocol framing, concept
  expansion, recall/precision mode selection, PubMed/Semantic Scholar/Crossref
  retrieval, deduplication, relevance scoring, screening prioritization, recall
  guardrails, evidence extraction, PRISMA precision summaries, and final reports.
compatibility: ">=2.0.0"
tags:
  - pharma
  - systematic-review
  - biomedical
  - evidence-synthesis
  - precision-search
  - medical-affairs
  - HEOR
  - pharmacovigilance
  - prisma
---

# EvidenceOS Precision-Controlled Pharmaceutical SLR

## Runtime and Attribution

This skill is an EvidenceOS workflow built on the credited DeerFlow open-source agent runtime/harness. Keep DeerFlow's MIT license, copyright notices, author names, and upstream attribution intact. Do not edit DeerFlow `LICENSE` while working on this skill.

## Product Purpose

This is not a basic PubMed summarizer. It is a precision-controlled biomedical systematic literature review workflow. SLR teams often maximize recall, but low precision creates a large downstream screening burden. This skill helps the reviewer choose a retrieval mode, show the tradeoff explicitly, prioritize records transparently, and keep recall guardrails in place before pruning.

## Precision Modes

Choose one mode at protocol time:

- `high_recall`: broadest concept matching; use when missing studies is the dominant risk.
- `balanced`: default mode; requires core disease/intervention/outcome alignment while keeping design filters flexible.
- `high_precision`: tighter outcome/design matching; use when screening capacity is constrained or sentinel recall has already been confirmed.

Do not silently use high precision. If high precision is selected, run recall guardrails before excluding borderline records.

## When To Use

Use `pharma-slr` for biomedical or pharmaceutical SLR work involving drugs, biologics, devices, diseases, biomarkers, exposures, safety signals, comparative effectiveness, medical affairs, HEOR, regulatory evidence, or pharmacovigilance literature.

Do not use it for single-paper review, general non-biomedical research, or unstructured search with no synthesis requirement.

## Workflow

### 1. PICO/PECO Protocol

Use `prompts/protocol_builder.md` and `schemas/pico.schema.json`.

Capture population/problem, intervention or exposure, comparator, outcomes, study designs, inclusion criteria, exclusion criteria, and assumptions. Use PECO for exposure/risk/association questions and PICO for intervention or comparative effectiveness questions.

### 2. Concept-Based Search Expansion

Run:

```bash
python skills/public/pharma-slr/scripts/concept_expand.py "<question>" --precision-mode balanced
```

The output structures:

- disease
- intervention/exposure
- comparator
- outcomes
- population
- study design
- synonyms
- MeSH-like terms where available
- drug brand/generic variants

Use these concepts as the source of truth for query building and relevance scoring.

### 3. Search Strategy Optimization

Run:

```bash
python skills/public/pharma-slr/scripts/search_strategy_optimizer.py "<question>" --precision-mode balanced
```

The optimizer returns:

- broad recall query
- balanced query
- precision-focused query
- PubMed Boolean query
- Semantic Scholar query
- Crossref query

Each strategy includes query string, intended mode, expected recall/precision tradeoff, included concepts, excluded concepts, and rationale.

### 4. Multi-Source Retrieval

Run source-specific retrieval scripts:

```bash
python skills/public/pharma-slr/scripts/pubmed_search.py "<pubmed_boolean_query>" --max-results <N>
python skills/public/pharma-slr/scripts/semantic_scholar_search.py "<semantic_scholar_query>" --max-results <N>
python skills/public/pharma-slr/scripts/crossref_search.py "<crossref_query>" --max-results <N>
```

Required smoke-test examples:

```bash
python skills/public/pharma-slr/scripts/pubmed_search.py "dupilumab atopic dermatitis safety" --max-results 5
python skills/public/pharma-slr/scripts/semantic_scholar_search.py "dupilumab safety atopic dermatitis" --max-results 5
python skills/public/pharma-slr/scripts/crossref_search.py "dupilumab atopic dermatitis safety" --max-results 5
```

Log source, query, filters, date, returned count, and source limitations.

### 5. Deduplicate

Run:

```bash
python skills/public/pharma-slr/scripts/deduplicate_records.py pubmed.json semantic_scholar.json crossref.json
```

Deduplication order is DOI, PMID, then normalized title. Preserve `sources` provenance for every merged record.

### 6. Precision Scoring

Run:

```bash
python skills/public/pharma-slr/scripts/precision_score.py deduplicated.json --concepts-json concepts.json --precision-mode balanced
```

Scoring fields:

- disease_match
- intervention_match
- outcome_match
- population_match
- study_design_match
- abstract_signal
- exclusion_signal
- final_relevance_score
- confidence
- transparent_reasons

Scores are prioritization aids, not final inclusion decisions.

### 7. Screening Prioritization

Run:

```bash
python skills/public/pharma-slr/scripts/screening_prioritizer.py scored_records.json
```

Groups:

- `very_likely_include`
- `possible_include`
- `uncertain_human_review`
- `likely_exclude`
- `background_only`

Human reviewers should validate `possible_include`, `uncertain_human_review`, exclusions with low confidence, and any record affected by a recall guardrail warning.

### 8. Recall Guardrail

Run before pruning, especially in `high_precision` mode:

```bash
python skills/public/pharma-slr/scripts/recall_guardrail.py deduplicated.json \
  --sentinel-json sentinel_papers.json \
  --mesh-candidates-json broad_concept_candidates.json \
  --citation-candidates-json citation_candidates.json
```

The guardrail checks whether known/sentinel papers are retrieved, whether broader concept/MeSH-style candidates were missed, whether citation-chasing candidates require review, and whether review articles may cite missing primary studies.

### 9. Human Validation

Use `prompts/title_abstract_screening.md`, `prompts/full_text_screening.md`, and `schemas/screening.schema.json`.

Record inclusion/exclusion reasons. Never let AI prioritization alone become final exclusion for records with weak confidence, missing abstracts, sentinel relevance, or citation-chain importance.

Build a review queue:

```bash
python skills/public/pharma-slr/scripts/human_review_queue.py prioritized_records.json --reviewer-id reviewer_001
```

### 10. Evidence Extraction

Use `prompts/evidence_extraction.md` and `schemas/extraction.schema.json`.

Extract disease, intervention/exposure, comparator, population, sample size, country, data source, study design, incidence, prevalence, mortality, safety outcomes, efficacy outcomes, follow-up, limitations, citation, and confidence.

Generate the evidence table:

```bash
python skills/public/pharma-slr/scripts/evidence_table.py included_extractions.json
```

### 11. PRISMA Precision Summary

Run:

```bash
python skills/public/pharma-slr/scripts/prisma_flow.py \
  --identified <N> \
  --deduplicated <N> \
  --screened <N> \
  --excluded <N> \
  --full-text-assessed <N> \
  --final-included <N> \
  --very-likely-include <N> \
  --possible-include <N> \
  --uncertain-human-review <N> \
  --likely-exclude <N> \
  --background-only <N> \
  --ai-prioritized-records <N> \
  --human-review-required-records <N>
```

Include both conventional PRISMA counts and precision-tier counts.

### 12. Final Report

Use `templates/biomedical-review.md`, `templates/systematic_review_report.md`, and `templates/precision_review_summary.md`.

The report must include:

- PICO/PECO protocol
- precision mode selection and rationale
- concept expansion
- search modes tested and tradeoffs
- retrieval and deduplication summary
- relevance scoring and screening prioritization
- human validation requirements
- recall guardrail findings
- evidence extraction table
- PRISMA precision summary
- final evidence synthesis and limitations

Save the report as `/mnt/user-data/outputs/evidenceos-pharma-slr-<topic-slug>-<YYYYMMDD>.md` and present it to the user.

## Validation, Governance, and Human Oversight

The skill also supports an auditable evidence-intelligence layer for source traceability and living evidence updates:

```bash
python skills/public/pharma-slr/scripts/evidence_signal_extraction.py records.json --output evidence_signals.json
python skills/public/pharma-slr/scripts/evidence_map_builder.py evidence_signals.json --output evidence_map.json
python skills/public/pharma-slr/scripts/evidence_path_explainer.py evidence_map.json --output evidence_paths.json --markdown-output evidence_paths.md
python skills/public/pharma-slr/scripts/living_evidence_monitor.py --previous previous_evidence_map.json --current evidence_map.json --output living_evidence_update.json
```

Evidence maps organize review signals only. They do not establish evidence quality, causal effect, clinical benefit, payer value, or regulatory acceptability without human review.

This skill supports validation-ready AI-assisted screening and extraction. It does not claim autonomous regulatory-grade review. Human reviewers remain responsible for final inclusion, exclusion, extraction acceptance, and adjudication.

Supported validation/governance steps:

- AI-assisted screening with structured human review
- Human agree, override, or second-review-needed decisions
- Performance evaluation against labeled records
- Exclusion rationale checking
- Audit-ready decision tracking
- Regulator/HTA-friendly evidence traceability
- Dual-reviewer adjudication support
- Project-level validation reporting

### Human Review Queue

Use `scripts/human_review_queue.py`, `schemas/reviewer_decision.schema.json`, and `templates/reviewer_queue.md`.

Required fields include AI decision, human decision/action, exclusion reason, confidence, notes, reviewer ID, and timestamp.

### Dual-Reviewer Workflow and Adjudication

Use `scripts/adjudication_workflow.py`, `schemas/adjudication.schema.json`, and `templates/adjudication_summary.md`.

Run:

```bash
python skills/public/pharma-slr/scripts/adjudication_workflow.py \
  --reviewer-one reviewer1.json \
  --reviewer-two reviewer2.json \
  --adjudicator-decisions adjudicator_decisions.json \
  --adjudicator-id adjudicator_001 \
  --adjudicator-signature "reviewed-by-adjudicator-001" \
  --lock-policy require_adjudicator_signature \
  --locked-output locked_labels.json \
  --output adjudicated.json
```

Lock policies:

- `agreement_or_adjudicated`: lock agreed dual-review labels and adjudicated conflict labels.
- `adjudicated_only`: lock only labels with an adjudicator decision.
- `require_adjudicator_signature`: lock only labels carrying adjudicator ID and signature metadata; use this for stricter regulated/HTA audit packs.

Supported conflict types:

- `include_vs_exclude`
- `different_exclusion_reason`
- `confidence_disagreement`
- `extraction_field_disagreement`
- `needs_full_text_review`

Adjudication output includes inter-reviewer raw agreement, Cohen's kappa, conflict counts, a worklist, schema validation status, and locked final labels according to the selected lock policy. Final decisions must be completed by a human adjudicator or approved dual-review process before regulator-facing inclusion/exclusion counts are treated as final.

### Screening Performance Evaluation

Run:

```bash
python skills/public/pharma-slr/scripts/evaluate_screening_performance.py --ai ai_decisions.json --gold human_labels.json
```

Outputs sensitivity, specificity, accuracy, precision, recall, F1, Cohen's kappa, confusion matrix, and markdown summary. Report metrics only against a labeled benchmark or project-specific human gold-standard set.

### Extraction Performance Evaluation

Run:

```bash
python skills/public/pharma-slr/scripts/evaluate_extraction_performance.py --ai ai_extraction.json --gold human_gold.json
```

Outputs field-level accuracy, F1 where appropriate, missing fields, mismatched fields, and confidence summary.

### Exclusion Rationale Evaluation

Run:

```bash
python skills/public/pharma-slr/scripts/evaluate_exclusion_rationales.py --ai ai_decisions.json --gold human_labels.json
```

Outputs rationale accuracy, common disagreement types, and examples requiring review.

### Audit Trail

Run:

```bash
python skills/public/pharma-slr/scripts/audit_trail.py --review-id demo --events screening_events.json
```

Tracks review ID, event ID, event type, record ID, timestamp, tool name, tool version, script path, prompt name/version, input/output hashes, model name when available, query string when available, AI decision, human decision, final decision, rationale, and provenance. Missing version/model/prompt metadata must be represented as `unknown`, not as a workflow failure.

### Project-Level Validation Report

Use `scripts/validation_report.py` and `templates/validation_report.md`.

Run:

```bash
python skills/public/pharma-slr/scripts/validation_report.py \
  --screening-metrics screening_metrics.json \
  --extraction-metrics extraction_metrics.json \
  --rationale-metrics rationale_metrics.json \
  --audit-summary audit_summary.json \
  --output validation_report.md
```

The report aggregates screening metrics, extraction metrics, exclusion rationale metrics, inter-reviewer/adjudication summary when supplied, audit trail completeness, and limitations. If any input comes from `evals/example_*` or contains `fixture_only=true`, the report must clearly state: "These results are from sample fixture data and are not validation evidence."

### Schema Validation

Use `scripts/schema_validate.py` for dependency-free validation against local pharma-slr schemas:

```bash
python skills/public/pharma-slr/scripts/schema_validate.py \
  --schema skills/public/pharma-slr/schemas/adjudication.schema.json \
  --json adjudicated.json \
  --items-key adjudication_records
```

This validator supports the schema subset used by this skill. Use `--items-key` when a script output wraps an array of records, such as `adjudication_records` or `locked_labels`. It is not a full JSON Schema Draft 2020-12 implementation, but it catches required fields, type mismatches, enum violations, array item errors, minimum values, and disallowed additional properties where specified.

### Project Manifest

Use `scripts/project_manifest.py`, `schemas/project_manifest.schema.json`, and `templates/project_manifest.md` to tie together the protocol, search logs, deduplicated records, human labels, adjudication, locked labels, audit trail, validation report, and final report.

```bash
python skills/public/pharma-slr/scripts/project_manifest.py \
  --review-id <review_id> \
  --protocol protocol.json \
  --search-log search_log.json \
  --deduplicated-records deduplicated.json \
  --screening-labels locked_labels.json \
  --adjudication adjudicated.json \
  --audit-trail audit_summary.json \
  --validation-report validation_report.md \
  --final-report final_report.md \
  --output project_manifest.json
```

### Sample Validation Fixtures

The folder `evals/example_dupilumab_ad/` contains tiny sample fixtures for smoke testing only. Do not use the sample fixture metrics as evidence of real-world model performance.

No real performance claims are allowed without human-labeled benchmark data that is appropriate for the target indication, source mix, study designs, and precision mode.

## Quality Rules

- Preserve DeerFlow attribution and MIT license compliance.
- Do not modify unrelated skills.
- Do not modify `skills/public/systematic-literature-review/` for this workflow.
- Do not fabricate source metadata, relevance scores, or screening counts.
- Treat Semantic Scholar rate limits as a retriable source limitation.
- Keep causal language conservative and study-design appropriate.
- High precision requires recall guardrails before pruning.
- Human-reviewed labels are required before reporting validation performance.
- Audit outputs should accompany regulator-facing or HTA-facing evidence packages.
