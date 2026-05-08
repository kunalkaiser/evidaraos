# Module Spec: Payer Value Dossier Builder

## Product Name

Payer Value Dossier Builder

## Source Skill

`skills/public/payer-value-dossier/`

## User

- market access lead
- payer strategy team
- medical affairs
- HEOR team

## Job To Be Done

Produce a structured, evidence-traceable payer value dossier draft from clinical evidence, disease burden, comparator, and HEOR inputs.

## Inputs

- product / compound
- indication
- target markets
- comparators
- evidence package
- submission context
- price assumptions, if available

## Core Workflow

1. Define dossier scope
2. Summarize disease burden and unmet need
3. Extract clinical efficacy and safety evidence
4. Build comparator landscape
5. Summarize HTA/payer precedents
6. Attach HEOR evidence model inputs
7. Draft value narrative
8. Create claim traceability matrix
9. Route claims for human review

## Needed Scripts

- `dossier_scope.py`
- `disease_burden_search.py`
- `comparator_landscape.py`
- `hta_precedent_search.py`
- `claim_traceability.py`
- `dossier_section_builder.py`

## Needed Schemas

- `dossier_scope.schema.json`
- `claim.schema.json`
- `comparator.schema.json`
- `hta_precedent.schema.json`
- `value_message.schema.json`

## Governance

- every efficacy/safety claim traces to PMID, NCT ID, or accepted source
- economic claims labeled as assumptions or modeled estimates
- payer implications are framed as evidence-informed considerations, not predictions
- human market access review required

## Product Output

- payer value dossier markdown
- claim traceability matrix
- comparator table
- HTA precedent appendix
- review queue

