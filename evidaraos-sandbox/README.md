# EvidaraOS Sandbox

This folder is the controlled working area for the Evidara OS / EvidenceOS product build on top of the DeerFlow repository.

## Boundary Rule

All EvidaraOS planning, prototypes, generated assets, draft code, module specs, security notes, and experiments should live here first.

Do not modify DeerFlow core, public website routes, backend routes, or unrelated skills unless a change is explicitly promoted from this sandbox and approved for implementation.

## Product Direction

Evidara OS is a precision evidence operating system for life sciences teams. It helps evidence, HEOR, regulatory, and market access teams turn biomedical literature, clinical evidence, and real-world data into traceable, validation-ready evidence workflows.

DeerFlow remains the credited MIT-licensed open-source agent runtime/harness. EvidaraOS product surfaces should not look like DeerFlow or expose generic DeerFlow skills as product pages.

## Current Product Modules

- Precision Literature Review
- HEOR Evidence Modeler
- Payer Value Dossier Builder
- Regulatory Evidence Briefing
- Drug Repurposing Evidence Explorer
- Evidence Governance & Validation Layer

## Product Layer v1

The product spine now lives in:

- `product/platform-layer.md`
- `product/manifests/`
- `product/demo-projects/`
- `product/taxonomy/`
- `product/content/`
- `product/schemas/`

Use this layer as the source of truth for the next public website and workspace rebuild. It defines module positioning, routes, workflows, artifacts, governance controls, demo projects, fixture-only warnings, and language guardrails.

## Reference Implementation

The strongest current module reference is:

- `skills/public/pharma-slr/`

Use the pharma-slr skill as the quality bar for future EvidaraOS agents: precision mode, concept retrieval, search optimization, deduplication, screening prioritization, human review, adjudication, validation reporting, audit trail, schemas, templates, and fixture-only evaluation warnings.

## Folder Map

- `docs/` - architecture notes, inspection reports, implementation plans
- `product/` - product module specs, route maps, IA, positioning
- `design/` - design system drafts, visual direction, page wireframes
- `frontend/` - isolated frontend prototypes before touching `frontend/src`
- `backend/` - isolated API/module bridge prototypes before touching `backend`
- `skills/` - new skill drafts before promotion to `skills/public`
- `agents/` - agent/workflow specs
- `security/` - repo safety review, deployment risk notes, credential/telemetry notes
- `experiments/` - disposable prototypes and tests
- `fixtures/` - clearly labeled local-only sample fixtures
- `outputs/` - generated reports or artifacts from sandbox work

## Promotion Rule

Before moving anything out of this folder, document:

1. Why the change is needed
2. Exact target files outside the sandbox
3. Whether DeerFlow attribution or license notices are affected
4. How the change will be tested
5. Rollback plan
