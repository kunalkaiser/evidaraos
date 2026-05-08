# EvidaraOS Backend Module Bridge Plan

## Objective

Expose EvidenceOS product modules without rewriting DeerFlow core runtime.

## Initial Principle

Keep DeerFlow as the runtime. Add a thin EvidenceOS module layer that maps professional product modules to skills, prompts, scripts, and artifacts.

## Minimal Backend Needs

### Module Registry

Endpoint concept:

`GET /api/evidara/modules`

Returns:

- product module ID
- display name
- description
- mapped skill name
- status
- available scripts
- artifact types

### Project Creation

Endpoint concept:

`POST /api/evidara/projects`

Creates an EvidenceOS project shell with:

- project ID
- module
- title
- question/scope
- status
- linked DeerFlow thread ID if execution starts

### Workflow Start

Endpoint concept:

`POST /api/evidara/projects/{project_id}/start`

Starts a DeerFlow run with:

- selected module
- protocol inputs
- precision mode
- selected skill context

### Artifact Manifest

Endpoint concept:

`GET /api/evidara/projects/{project_id}/artifacts`

Returns:

- uploaded files
- generated outputs
- validation reports
- audit summaries
- project manifest

### Validation/Audit Summary

Endpoint concept:

`GET /api/evidara/projects/{project_id}/governance`

Returns:

- human review state
- adjudication state
- locked labels
- audit completeness
- validation report status

## No Core Runtime Rewrite Yet

Do not change:

- LangGraph run lifecycle
- DeerFlow skill parser
- sandbox execution core
- authentication core

Use existing:

- `/api/agents`
- `/api/skills`
- `/api/threads`
- `/api/runs`
- artifact APIs

## First Implementation Option

Start with static module registry in frontend or gateway. Then connect project creation and workflow start later.

