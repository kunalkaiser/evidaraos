# Module Spec: HEOR Evidence Modeler

## Product Name

HEOR Evidence Modeler

## Source Skill

`skills/public/heor-model-foundation/`

## User

- HEOR modeler
- health economist
- market access analyst
- evidence generation lead

## Job To Be Done

Turn biomedical literature and public evidence sources into structured model input candidates for health economist review.

## Inputs

- condition / indication
- intervention
- comparator
- target geography
- model perspective
- time horizon
- model type
- evidence sources available

## Core Workflow

1. Define model scope
2. Frame evidence needs
3. Retrieve utility, event-rate, resource-use, and cost evidence
4. Normalize candidate inputs
5. Extract source provenance
6. Generate assumption register
7. Flag uncertainty and missing evidence
8. Produce review-ready model input tables

## Needed Scripts

- `utility_search.py`
- `event_rate_extraction.py`
- `cost_input_extraction.py`
- `resource_use_extraction.py`
- `assumption_register.py`
- `model_input_table.py`
- `heor_validation_queue.py`

## Needed Schemas

- `model_scope.schema.json`
- `utility_input.schema.json`
- `event_rate.schema.json`
- `cost_input.schema.json`
- `assumption.schema.json`
- `model_input_table.schema.json`

## Governance

- every model input must have source provenance or be labeled as assumption
- every estimate needs uncertainty bounds where available
- health economist review required before use
- no cost-effectiveness result claims without actual model execution and validation

## Product Output

- model input table
- assumption register
- evidence gap summary
- health economist review queue
- source provenance appendix

