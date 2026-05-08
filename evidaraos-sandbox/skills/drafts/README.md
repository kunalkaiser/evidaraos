# EvidaraOS Draft Skills

These are sandbox-only draft skills modeled after `skills/public/pharma-slr/`.

Do not promote them to `skills/public/` until reviewed.

## Drafts Created

### `heor-evidence-modeler`

Purpose:

- HEOR model scope
- model input table
- assumption register
- evidence readiness scoring
- health economist review requirement

Smoke commands:

```bash
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/model_scope.py --condition "atopic dermatitis" --intervention dupilumab --comparator "standard of care" --perspective "US payer"
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/model_input_table.py evidaraos-sandbox/skills/drafts/heor-evidence-modeler/evals/example_fixture/inputs.sample.json
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/assumption_register.py evidaraos-sandbox/skills/drafts/heor-evidence-modeler/evals/example_fixture/inputs.sample.json
python evidaraos-sandbox/skills/drafts/heor-evidence-modeler/scripts/evidence_readiness.py evidaraos-sandbox/skills/drafts/heor-evidence-modeler/evals/example_fixture/inputs.sample.json
```

### `payer-value-dossier-builder`

Purpose:

- payer dossier scope
- claim traceability
- dossier outline
- dossier gap checking
- human market-access review requirement

Smoke commands:

```bash
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/dossier_scope.py --product dupilumab --indication "atopic dermatitis" --market US
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/claim_traceability.py evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/evals/example_fixture/claims.sample.json
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/dossier_outline.py evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/evals/example_fixture/scope.sample.json
python evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/scripts/dossier_gap_check.py --scope evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/evals/example_fixture/scope.sample.json --claims evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/evals/example_fixture/claims.sample.json
```

### `regulatory-evidence-briefing`

Purpose:

- regulatory context
- benefit-risk table
- uncertainty register
- conservative language guardrail
- regulatory expert review requirement

Smoke commands:

```bash
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/regulatory_context.py --product dupilumab --indication "atopic dermatitis" --agency FDA --stage post-market
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/benefit_risk_table.py evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/evals/example_fixture/evidence.sample.json
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/language_guardrail.py evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/evals/example_fixture/claims.sample.json
python evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/scripts/uncertainty_register.py evidaraos-sandbox/skills/drafts/regulatory-evidence-briefing/evals/example_fixture/evidence.sample.json
```

### `drug-repurposing-evidence-explorer`

Purpose:

- mode detection
- transparent repurposing score
- target-disease evidence matrix
- safety transfer assessment
- validation checklist
- hypothesis-only labeling

Smoke commands:

```bash
python evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/scripts/mode_detector.py "Could dupilumab be repurposed for another inflammatory disease?"
python evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/scripts/repurposing_score.py evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/evals/example_fixture/candidates.sample.json
python evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/scripts/validation_checklist.py evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/evals/example_fixture/candidates.sample.json
python evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/scripts/target_evidence_matrix.py evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/evals/example_fixture/target_evidence.sample.json
python evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/scripts/safety_transfer_assessment.py evidaraos-sandbox/skills/drafts/drug-repurposing-evidence-explorer/evals/example_fixture/candidates.sample.json
```

## Fixture Warning

All `evals/example_fixture/` data is synthetic fixture-only smoke-test data. It is not validation evidence and must not be used for scientific, regulatory, payer, or marketing claims.

## Shared Governance Layer

Shared draft governance scripts live in `_shared_governance/`.

Capabilities:

- human review queue
- audit trail with hashes/version metadata
- validation report
- project manifest
- fixture-only warning propagation

Smoke commands:

```bash
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/human_review_queue.py evidaraos-sandbox/skills/drafts/payer-value-dossier-builder/evals/example_fixture/claims.sample.json --module payer-value-dossier-builder --reviewer-id reviewer_001 --output /tmp/evidaraos_review_queue.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/audit_trail.py --review-id demo-payer --module payer-value-dossier-builder --events /tmp/evidaraos_review_queue.json --output /tmp/evidaraos_audit_summary.json
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/validation_report.py --module payer-value-dossier-builder --review-queue /tmp/evidaraos_review_queue.json --audit-summary /tmp/evidaraos_audit_summary.json --output /tmp/evidaraos_validation_report.md
python evidaraos-sandbox/skills/drafts/_shared_governance/scripts/project_manifest.py --project-id demo-payer --module payer-value-dossier-builder --review-queue /tmp/evidaraos_review_queue.json --audit-trail /tmp/evidaraos_audit_summary.json --validation-report /tmp/evidaraos_validation_report.md --output /tmp/evidaraos_project_manifest.json
```

## Promotion TODO

Before promotion:

- add broader schemas
- add governance/audit scripts shared from pharma-slr pattern
- add project manifest support
- add human review queues
- add source-specific retrieval scripts where needed
- run full smoke tests after copying into `skills/public/`
