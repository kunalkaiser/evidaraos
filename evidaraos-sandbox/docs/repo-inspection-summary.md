# Repo Inspection Summary

Date: 2026-05-06

## Current Stack

- Frontend: Next.js App Router, React, TypeScript, Tailwind/shadcn-style components
- Backend: FastAPI gateway plus DeerFlow harness/runtime
- Agent runtime: DeerFlow / LangGraph
- Product workspace today: generic DeerFlow chat, agents, skills, artifacts, uploads, memory, settings

## Important Existing Routes

Public/frontend:

- `/`
- `/workspace`
- `/workspace/chats`
- `/workspace/chats/[thread_id]`
- `/workspace/agents`
- `/workspace/agents/new`
- `/login`
- `/setup`
- `/blog`
- `/[lang]/docs`

Backend/API:

- `/api/agents`
- `/api/skills`
- `/api/models`
- `/api/mcp`
- `/api/memory`
- `/api/threads`
- `/api/threads/{thread_id}/uploads`
- `/api/threads/{thread_id}/artifacts`
- `/api/runs`
- `/api/v1/auth`

## Product Reuse Candidates

- DeerFlow runtime, threads, artifacts, uploads, auth, LangGraph streaming
- Skill loader and skill settings
- Workspace shell components
- Existing EvidenceOS skills:
  - `skills/public/pharma-slr/`
  - `skills/public/heor-model-foundation/`
  - `skills/public/payer-value-dossier/`
  - `skills/public/regulatory-briefing/`
  - `skills/public/drug-repurposing/`
- Supporting skills:
  - `chart-visualization`
  - `data-analysis`
  - `academic-paper-review`
  - `consulting-analysis`
  - `ppt-generation`

## Safety Notes

- `frontend/public/demo/threads/.../diana_hu_research.md` is a bundled demo output, not a hidden installer.
- `.agent/skills/smoke-test/` contains local smoke-test/deploy scripts. Treat as operational tooling, not product code.
- Docker compose mounts host auth folders such as `~/.claude` and `~/.codex`. This should be documented and controlled before customer-facing packaging.
- Optional tracing exists through LangSmith/Langfuse configuration. Do not enable telemetry unless explicitly configured.

## First Product Build Direction

Build professional EvidaraOS product surfaces over DeerFlow:

- Public EvidenceOS website
- EvidenceOS workspace shell
- Product module registry
- Skill-to-module mapping layer
- Governance and validation-first UX

