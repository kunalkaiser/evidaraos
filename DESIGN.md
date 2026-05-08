---
name: EvidaraOS Design System
version: 0.1.0
status: draft
owner: Evidara OS
format: design.md-compatible
tokens:
  color:
    canvas:
      deepest: "#070d17"
      base: "#08111f"
      raised: "#071523"
      panel: "#0b1828"
      inset: "#0e2234"
    text:
      primary: "#f8f1e3"
      secondary: "#c7d1d8"
      muted: "#aebbc5"
      faint: "#8395a3"
      inverse: "#08111f"
    accent:
      clinical: "#8ec7c1"
      clinicalSoft: "#dff7f2"
      evidenceGold: "#d7b46a"
      evidenceGoldHover: "#f0cc80"
    border:
      default: "rgba(255,255,255,0.10)"
      strong: "rgba(255,255,255,0.15)"
      clinical: "rgba(142,199,193,0.35)"
      gold: "rgba(215,180,106,0.35)"
  typography:
    family:
      sans: "system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    heading:
      weight: 600
      tracking: "0"
      lineHeightTight: "0.95"
      lineHeightCompact: "0.98"
    body:
      weight: 400
      lineHeight: "1.65"
    label:
      weight: 600
      tracking: "0.18em-0.26em"
      transform: uppercase
  spacing:
    base: 4
    pageXMobile: 20
    pageXDesktop: 32
    sectionY: 96
    maxWidth: 1280
  radius:
    default: 0
    maxCardRadius: 8
  components:
    primaryButton:
      background: "{tokens.color.accent.evidenceGold}"
      foreground: "{tokens.color.text.inverse}"
      hover: "{tokens.color.accent.evidenceGoldHover}"
    secondaryButton:
      border: "{tokens.color.border.strong}"
      foreground: "{tokens.color.text.primary}"
      hoverBorder: "rgba(142,199,193,0.60)"
    panel:
      background: "{tokens.color.canvas.raised}"
      border: "{tokens.color.border.default}"
    dataGrid:
      divider: "{tokens.color.border.default}"
      cellBackground: "{tokens.color.canvas.panel}"
---

# EvidaraOS Design System

EvidaraOS should look like a serious enterprise life-sciences intelligence company: precise, governed, clinical, and quietly premium. The interface should feel like evidence infrastructure used by HEOR, regulatory, evidence generation, medical affairs, and market-access teams.

This file is the visual source of truth for AI agents and developers working on EvidaraOS pages, workspace screens, decks, and marketing artifacts.

## Brand Atmosphere

EvidaraOS is not a playful AI app and not a generic SaaS dashboard. It should feel like a controlled evidence operations layer: boardroom-ready, scientifically literate, and calm under scrutiny.

Use language and visuals that imply:

- traceability
- governance
- precision
- scientific restraint
- human review
- validated workflow readiness
- life-sciences enterprise credibility

Avoid language and visuals that imply:

- AI magic
- instant answers
- unsupported clinical proof
- fake metrics
- consumer startup energy
- decorative futurism
- generic gradient SaaS

## Color System

The base palette is dark navy, ivory, slate, clinical teal, and restrained evidence gold.

Use dark navy as the dominant environment. Use ivory for primary text. Use slate for secondary text and interface labels. Use clinical teal for evidence-system structure, active states, graph lines, and protocol metadata. Use evidence gold only for primary CTAs, important provenance markers, and sparse emphasis.

Do not introduce large purple, blue-purple, beige, tan, orange, or neon palettes. Do not use gradient blobs, bokeh, or decorative orbs.

## Typography

Headlines should be confident and compact. Use large type only for true page heroes. Inside product panels, tables, cards, and workspace screens, use smaller headings with dense but readable spacing.

Rules:

- Heading letter spacing is `0`, never negative.
- Eyebrows and metadata labels use uppercase with wide tracking.
- Body copy should be short and concrete.
- Avoid marketing filler. Prefer architecture, workflow, artifact, source, validation, and governance language.
- Do not use emoji.

## Layout

Use full-width bands, strong grids, and evidence-system diagrams. The design should reveal how evidence moves through the platform.

Preferred structures:

- split hero with product console or architecture visual
- grid-based workflow maps
- module matrices
- provenance tables
- audit timelines
- evidence stack diagrams
- lifecycle rails
- dense workspace shells

Avoid:

- nested cards
- oversized rounded cards
- floating marketing cards
- generic three-card SaaS sections
- pure text sections without structure
- decorative illustrations that do not show product, data, evidence, workflow, or governance

## Components

Panels should be square or lightly rounded, with 1px borders and restrained contrast. Cards are allowed for repeated items and workspace modules, but should stay compact and no more than 8px radius.

Buttons:

- Primary buttons use evidence gold with dark navy text.
- Secondary buttons use transparent backgrounds with subtle borders.
- Icon buttons should use lucide icons when available.

Tables and matrices:

- Use grid dividers and clear columns.
- Keep row density high enough for professional review work.
- Always distinguish source evidence, AI interpretation, human decision, validation status, and limitations.

Workflow visuals:

- Show data movement with lines, rails, tiers, or matrices.
- Prefer structure over decoration.
- Every visual should answer "how is this done?" or "what is governed?"

## Page Patterns

Homepage:

- Hero: brand/product signal in first viewport.
- Visual: evidence operations console or system architecture.
- Must show the platform lifecycle: Question -> Protocol -> Retrieval -> Evidence Map -> Human Review -> Extraction -> Validation -> Report -> Audit.
- Include a proof mosaic or artifact wall that shows the breadth of evidence workflows without inventing customer claims.
- Use "work", "platform", "modules", "governance", and "resources" bands to create enterprise depth.

Solution pages:

- Translate skills into product modules.
- Show workflow, artifacts, guardrails, and status.
- Do not expose raw DeerFlow skills as public-facing product pages.
- Use a module-specific proof structure: problem, governed workflow, artifacts, validation controls, limitations, next action.

Workspace:

- Serious shell with projects, modules, artifact status, validation status, and audit status.
- If execution is not live, label status as configured workflow, connected skill, fixture ready, or pending live execution.
- Do not fake live data.

Governance:

- Lead with human review, validation reports, audit trails, project manifests, fixture-only warnings, and no unsupported claims.

## Inspiration Translation: Enterprise Health Intelligence

Use companies like IMO Health, Truveta, and Atropos Health as references for maturity, not as sources to copy. The reusable pattern is:

- a confident hero with a clear data/intelligence foundation message
- a navigation system that feels like a real company, not a demo
- product and solution modules separated clearly
- a visual wall of proof, artifacts, resources, or use cases
- a "work" section that explains the operating model
- an "impact" section only when supported by real evidence
- resource/research pages that build domain credibility
- a final CTA that feels enterprise, not hype-driven

For EvidaraOS, translate that pattern into:

- evidence workflow modules instead of generic products
- validation and audit artifacts instead of unsupported metrics
- fixture-labeled demos instead of fake customer proof
- research/methodology content instead of generic blog filler
- life-sciences evidence language instead of health-system coding language

Never copy another site's words, claims, images, layout, logos, or case studies.

## EvidenceOS-Specific Rules

- DeerFlow may be credited as the open-source runtime/harness, but public product pages should not look like DeerFlow.
- Do not remove DeerFlow attribution or upstream notices.
- Do not use fake benchmarks, fake validation, fake live data, or fake customer logos.
- Fixture data must always be labeled as smoke-test/demo-only and not validation evidence.
- AI output must remain separate from human decision and final decision.
- Research-paper inspiration must become governed method signals, not product proof.

## Accessibility

- Maintain WCAG AA contrast for text.
- Do not put small slate text on low-contrast panels.
- Avoid hover-only meaning.
- Buttons and links must have visible focus/hover affordances.
- Text must not overlap or resize layout unexpectedly.

## Prompt Contract

When building any EvidaraOS interface, first read this file. Preserve the tokens, tone, layout rules, and governance constraints. If a new visual direction is needed, update `DESIGN.md` before applying it broadly.
