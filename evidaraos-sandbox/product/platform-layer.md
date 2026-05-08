# EvidaraOS Product Layer v1

This folder now defines the product spine that should come before the public website rebuild.

## What It Provides

- Product module manifests in `manifests/`
- Fixture-only demo project manifests in `demo-projects/`
- Shared artifact taxonomy in `taxonomy/artifact-taxonomy.json`
- Shared workflow lifecycle in `taxonomy/workflow-lifecycle.md`
- Website content primitives in `content/website-content.json`
- Workspace content primitives in `content/workspace-content.json`
- JSON schemas for module and demo manifests in `schemas/`

## Why This Matters

The EvidenceOS website should describe a real governed platform, not a generic SaaS wrapper. These manifests make the product modules concrete while keeping DeerFlow correctly credited as the runtime/harness.

## Product Wedge

EvidenceOS is strongest where competitors tend to blur AI claims: precision evidence workflows with governance built in.

The core differentiators are:

- precision-controlled retrieval and screening
- traceable evidence maps
- human review and adjudication
- validation reports with fixture-only warnings
- audit trails and project manifests
- module-specific outputs for SLR, HEOR, payer, regulatory, and repurposing workflows

## Frontend Use

The next website/workspace build should read from these product primitives or mirror them closely:

- Public solution pages should use `manifests/*.json`.
- Demo cards should use `demo-projects/*.json`.
- Navigation and copy should use `content/*.json`.
- Claims and badges should follow `taxonomy/artifact-taxonomy.json`.

## Guardrail

Do not claim live execution, benchmark performance, RWD network access, regulatory-grade evidence, or production validation until those capabilities exist and are supported by human-labeled validation data.
