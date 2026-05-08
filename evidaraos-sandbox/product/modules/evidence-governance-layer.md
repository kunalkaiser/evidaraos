# Module Spec: Evidence Governance & Validation Layer

## Product Name

Evidence Governance & Validation Layer

## Reference

Use the governance layer in `skills/public/pharma-slr/`.

## User

- evidence quality lead
- regulatory operations
- HTA submission team
- compliance reviewer
- medical governance team

## Job To Be Done

Provide traceability, human oversight, validation readiness, and audit-ready metadata across all EvidaraOS evidence workflows.

## Core Capabilities

- human review queue
- dual-reviewer adjudication
- adjudicator signature policy
- locked final decisions
- audit events
- project manifest
- validation report
- fixture-only warnings
- source provenance summary

## Cross-Module Requirements

Every module should eventually emit:

- `review_id` or `project_id`
- `artifact_id`
- `source`
- `query_string`, if applicable
- `input_hash`
- `output_hash`
- `tool_name`
- `tool_version`
- `prompt_name`
- `prompt_version`
- `model_name`, if available
- `human_decision`, if applicable
- `final_decision`, if applicable
- `rationale`
- `timestamp`

## Product Output

- governance dashboard
- validation report
- audit summary
- project manifest
- source provenance appendix

