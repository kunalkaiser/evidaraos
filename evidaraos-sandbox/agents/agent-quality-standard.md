# EvidaraOS Agent Quality Standard

Use `skills/public/pharma-slr/` as the current reference standard.

Every serious EvidaraOS agent should include:

## 1. Protocol Layer

- structured question framing
- scope confirmation
- inclusion/exclusion boundaries
- output requirements
- user-provided assumptions

## 2. Retrieval / Source Layer

- source-specific retrieval scripts where possible
- normalized records
- provenance fields
- no unsupported source claims

## 3. Evidence Structuring Layer

- JSON schemas
- extraction tables
- deterministic helpers
- confidence fields
- missing-data handling

## 4. Human Review Layer

- review queue
- agree/override/needs-second-review
- exclusion or rejection rationale
- reviewer ID
- timestamp

## 5. Governance Layer

- audit trail
- project manifest
- locked labels/final decisions
- validation report
- fixture-only warnings

## 6. Product Output Layer

- markdown report template
- evidence table
- limitations
- citation traceability
- no real performance claims without validated benchmark data

## Required Folder Pattern

Draft new skills in sandbox first:

```text
evidaraos-sandbox/skills/drafts/<skill-name>/
  SKILL.md
  scripts/
  schemas/
  prompts/
  templates/
  references/
  evals/
```

Promote to `skills/public/` only after review.

