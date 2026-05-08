# Module Spec: Regulatory Evidence Briefing

## Product Name

Regulatory Evidence Briefing

## Source Skill

`skills/public/regulatory-briefing/`

## User

- regulatory affairs team
- clinical strategy team
- medical writing team
- evidence generation team

## Job To Be Done

Create a conservative, traceable regulatory evidence briefing for a product, indication, or benefit-risk question.

## Inputs

- drug / compound
- indication
- target agency
- development stage
- submission type
- key trial IDs
- known regulatory interactions, if user provides them

## Core Workflow

1. Define regulatory context
2. Retrieve agency precedents
3. Retrieve guidance and public review documents
4. Structure benefit-risk evidence
5. Identify residual uncertainty
6. Draft conservative regulatory briefing language
7. Route for regulatory review
8. Create audit trail and source appendix

## Needed Scripts

- `agency_precedent_search.py`
- `guidance_search.py`
- `benefit_risk_table.py`
- `regulatory_uncertainty_register.py`
- `submission_language_checker.py`

## Needed Schemas

- `regulatory_context.schema.json`
- `agency_precedent.schema.json`
- `benefit_risk.schema.json`
- `uncertainty.schema.json`
- `briefing_claim.schema.json`

## Governance

- never predict approval
- cite public FDA/EMA/PMDA documents, PMID, or NCT IDs
- label drafts as requiring regulatory expert review
- conservative language only

## Product Output

- regulatory evidence briefing
- benefit-risk table
- precedent appendix
- uncertainty register
- review queue

