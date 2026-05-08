# Module Spec: Drug Repurposing Evidence Explorer

## Product Name

Drug Repurposing Evidence Explorer

## Source Skill

`skills/public/drug-repurposing/`

## User

- translational science team
- business development
- pipeline strategy
- R&D leadership

## Job To Be Done

Identify evidence-supported repurposing hypotheses and rank them by mechanistic plausibility, clinical evidence, safety transfer, and unmet need.

## Modes

### Compound To Indications

Start with an approved compound and identify plausible new indications.

### Indication To Compounds

Start with a disease and identify approved compounds with plausible evidence.

## Core Workflow

1. Detect operating mode
2. Characterize compound or disease
3. Retrieve target/mechanism evidence
4. Retrieve disease association evidence
5. Retrieve clinical evidence
6. Assess safety transfer
7. Score candidate hypotheses
8. Generate validation checklist
9. Produce ranked evidence explorer report

## Needed Scripts

- `compound_profile.py`
- `disease_target_map.py`
- `repurposing_candidate_search.py`
- `clinical_signal_search.py`
- `safety_transfer_assessment.py`
- `repurposing_score.py`

## Needed Schemas

- `compound_profile.schema.json`
- `candidate_indication.schema.json`
- `repurposing_score.schema.json`
- `safety_transfer.schema.json`

## Governance

- every candidate labeled as mechanistic hypothesis requiring clinical validation
- no therapeutic benefit claim from target association alone
- safety transfer assessed conservatively
- source provenance required

## Product Output

- ranked candidate table
- evidence scorecard
- safety transfer notes
- validation checklist
- evidence explorer report

