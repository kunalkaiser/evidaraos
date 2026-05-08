# EvidaraOS Implementation Plan

## Rule

Build and review in `evidaraos-sandbox/` first. Promote only approved changes into DeerFlow app files.

## Phase 1: Product Framing and Shell

Status: planned

Sandbox artifacts:

- `product/website-ia.md`
- `product/workspace-architecture.md`
- `design/design-system.md`

Future promotion targets:

- `frontend/src/app/page.tsx`
- `frontend/src/components/landing/*`
- new `frontend/src/app/platform/page.tsx`
- new `frontend/src/app/solutions/.../page.tsx`
- new `frontend/src/app/governance/page.tsx`
- new `frontend/src/app/demo/page.tsx`

Deliverable:

- EvidaraOS public website replacing generic DeerFlow landing page.
- DeerFlow attribution preserved in company/legal/notices surfaces.

## Phase 2: Product Module Registry

Status: planned

Sandbox artifacts:

- `backend/api/module-bridge-plan.md`
- `product/modules/*.md`

Future promotion targets:

- frontend-only first:
  - `frontend/src/core/evidara/modules.ts`
  - `frontend/src/components/evidara/module-card.tsx`
  - `frontend/src/app/workspace/modules/page.tsx`
- backend later:
  - `backend/app/gateway/routers/evidara.py`
  - `backend/app/gateway/app.py`

Deliverable:

- Product modules shown as EvidaraOS capabilities, not raw skills.
- Each module shows honest status: configured workflow, connected skill, pending live execution.

## Phase 3: Workspace Reframe

Status: planned

Future promotion targets:

- `frontend/src/components/workspace/workspace-sidebar.tsx`
- `frontend/src/components/workspace/workspace-nav-menu.tsx`
- `frontend/src/app/workspace/page.tsx`
- new workspace module routes

Deliverable:

- Evidence operations navigation:
  - Projects
  - Precision SLR
  - Screening Queue
  - Evidence Extraction
  - PRISMA
  - Validation Reports
  - Payer Dossiers
  - Regulatory Briefs
  - Audit Trail

## Phase 4: Backend Module Bridge

Status: planned

Future promotion targets:

- `backend/app/gateway/routers/evidara.py`
- `backend/app/gateway/app.py`
- maybe `backend/packages/harness/deerflow/skills/*` only if needed

Deliverable:

- `GET /api/evidara/modules`
- `POST /api/evidara/projects`
- `GET /api/evidara/projects/{project_id}`
- `GET /api/evidara/projects/{project_id}/artifacts`

Do not rewrite DeerFlow runtime.

## Phase 5: Skill Hardening

Status: planned

Reference:

- `skills/public/pharma-slr/`

Targets:

- `skills/public/heor-model-foundation/`
- `skills/public/payer-value-dossier/`
- `skills/public/regulatory-briefing/`
- `skills/public/drug-repurposing/`

Deliverable:

- Upgrade each skill toward pharma-slr quality standard:
  - scripts
  - schemas
  - prompts
  - templates
  - references
  - governance hooks
  - fixture-only evals

## Phase 6: Security / Packaging

Status: planned

Tasks:

- remove generic demo threads from production surface
- document credential mounts
- ensure telemetry off by default
- preserve DeerFlow MIT attribution
- update third-party notices as needed

## Suggested Next Work

1. Build static EvidaraOS module registry in sandbox.
2. Draft frontend page components in `evidaraos-sandbox/frontend/`.
3. Review visual direction.
4. Promote homepage only after approval.

