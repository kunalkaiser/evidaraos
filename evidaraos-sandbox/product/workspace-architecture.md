# EvidaraOS Workspace Architecture

## Goal

Create a serious product workspace shell over the DeerFlow runtime. The workspace should feel like an evidence operations console, not a generic chat app.

## Core Navigation

Primary workspace sections:

- Projects
- Precision SLR
- Screening Queue
- Evidence Extraction
- PRISMA
- Validation Reports
- Payer Dossiers
- Regulatory Briefs
- Audit Trail

## Status Labels

When backend integration is incomplete, modules must be labeled honestly:

- `configured workflow`
- `connected skill`
- `pending live execution`

Do not display fake live results.

## Project Object

Each EvidaraOS project should eventually contain:

```json
{
  "project_id": "string",
  "title": "string",
  "module": "precision_slr",
  "status": "draft | running | human_review | validated | archived",
  "created_at": "iso8601",
  "updated_at": "iso8601",
  "protocol": {},
  "artifacts": [],
  "audit_summary": {},
  "validation_summary": {},
  "runtime": "DeerFlow",
  "module_version": "string"
}
```

## Product Module Registry

The workspace should introduce a product module registry that maps product modules to DeerFlow skills.

Example:

```json
{
  "precision_literature_review": {
    "display_name": "Precision Literature Review",
    "skill": "pharma-slr",
    "status": "connected skill",
    "entry_route": "/workspace/modules/precision-slr"
  }
}
```

## Proposed Workspace Routes

These should be planned in the sandbox before implementation:

- `/workspace/projects`
- `/workspace/projects/[project_id]`
- `/workspace/modules`
- `/workspace/modules/precision-slr`
- `/workspace/modules/heor`
- `/workspace/modules/payer-value-dossier`
- `/workspace/modules/regulatory-briefing`
- `/workspace/modules/drug-repurposing`
- `/workspace/review/screening`
- `/workspace/review/extraction`
- `/workspace/review/prisma`
- `/workspace/validation`
- `/workspace/audit-trail`

## Reuse Existing DeerFlow Runtime

Keep:

- thread chat
- artifacts
- uploads
- skills settings
- LangGraph streaming
- auth
- project persistence where available

Adapt:

- navigation labels
- empty states
- module entry pages
- skill surfacing
- artifact summaries

Avoid:

- deleting generic DeerFlow routes before replacement is stable
- hiding runtime attribution from legal/about surfaces
- faking module execution before backend bridge exists

