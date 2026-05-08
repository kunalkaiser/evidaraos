# EvidaraOS Module Roadmap

## Existing Modules To Productize

### Precision Literature Review

Reference skill: `skills/public/pharma-slr/`

Capabilities:

- PICO/PECO framing
- Precision mode selection
- Concept expansion
- Multi-source retrieval
- Deduplication
- Relevance scoring
- Human review queue
- Dual-reviewer adjudication
- Validation reporting
- Audit trail
- PRISMA-style reporting
- Evidence table generation

### HEOR Evidence Modeler

Reference skill: `skills/public/heor-model-foundation/`

Next upgrades:

- Structured model input schemas
- Utility/event-rate/cost extraction scripts
- Source provenance tables
- Health economist review queue
- Assumption register
- Sensitivity-analysis-ready exports

### Payer Value Dossier Builder

Reference skill: `skills/public/payer-value-dossier/`

Next upgrades:

- Dossier section schemas
- Evidence claim traceability
- Comparator landscape extraction
- HTA precedent tracking
- Review/approval workflow

### Regulatory Evidence Briefing

Reference skill: `skills/public/regulatory-briefing/`

Next upgrades:

- FDA/EMA/PMDA evidence source modules
- Benefit-risk framework schema
- Precedent table extraction
- Human regulatory signoff queue
- Submission-language caution checks

### Drug Repurposing Evidence Explorer

Reference skill: `skills/public/drug-repurposing/`

Next upgrades:

- Compound/disease mode schemas
- Mechanistic hypothesis scoring
- Safety transfer assessment
- Clinical evidence tiering
- Candidate validation checklist

## New Agents / Skills To Add

1. HTA Precedent Intelligence Agent
2. Clinical Trial Evidence Extractor
3. Real-World Evidence Cohort Feasibility Agent
4. Label / SmPC Comparison Agent
5. Safety Signal Evidence Agent
6. Guideline Landscape Agent
7. Comparator Landscape Agent
8. Evidence Gap Assessment Agent
9. Publication Planning Evidence Agent
10. Medical Affairs Response Pack Agent

## Quality Bar

Every new module should follow the pharma-slr pattern:

- Clear operating modes
- Structured schemas
- Deterministic scripts where possible
- Human-in-the-loop review
- Audit events
- Fixture-only warnings for sample evals
- No unsupported performance claims
- Traceable citations and provenance

