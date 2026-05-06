---
name: drug-repurposing
display_name: Drug Repurposing Intelligence
version: 1.0.0
author: Evidara OS
description: >
  Identifies evidence-supported repurposing candidates for approved compounds
  or finds approved compounds with mechanistic rationale for a given indication.
  Scores candidates across mechanistic plausibility, clinical evidence,
  safety transfer, and unmet need. All candidates labeled as mechanistic
  hypotheses requiring clinical validation.
compatibility: ">=2.0.0"
tags:
  - pharma
  - drug-repurposing
  - indication-expansion
  - R&D
  - pipeline
  - business-development
  - mechanistic
---

# Drug Repurposing Intelligence

## When to use this skill

Use this skill when the user asks for:
- Repurposing opportunities for an approved compound
- Approved drugs that could work for a new indication
- Indication expansion analysis
- 505(b)(2) pathway candidates
- Mechanistic rationale for off-label use
- Pipeline opportunity assessment from existing assets
- "What else could this drug treat?"
- "What approved drugs could work for this disease?"
- Repurposing gap analysis — high unmet need + existing mechanistic rationale

Do NOT use for:
- New molecular entity design
- De novo drug discovery
- Clinical trial design for repurposing (use pharma-slr for evidence)

---

## Core Principles

1. All repurposing candidates are labeled "Mechanistic Hypothesis — requires clinical validation" regardless of evidence strength
2. Mechanistic plausibility is never sufficient alone — clinical evidence required for any claim
3. Safety transfer is assessed conservatively — new population may have different risk profile
4. Association between target and disease is never upgraded to proven therapeutic benefit
5. Every source traces to ChEMBL, OpenTargets, DrugCentral, PMID, or NCT ID

---

## Two Operating Modes

### Mode A — Compound to Indications
Input: an approved compound name
Output: ranked list of candidate indications with evidence scores

### Mode B — Indication to Compounds
Input: an indication or disease name
Output: ranked list of approved compounds with mechanistic rationale

Detect mode from user input. If unclear, ask: "Are you starting with a compound or an indication?"

---

## Mode A: Compound → Indications

### Step A1 — Characterize the Compound

Search ChEMBL for:
- Mechanism of action (MOA)
- Primary molecular targets
- Target class (kinase, GPCR, ion channel, etc.)
- Approved indications
- Clinical stage pipeline indications

Search DrugCentral for:
- Additional MOA annotations
- Known off-label use patterns
- Drug-drug interaction profile

Output:
```markdown
## Compound Profile: [Drug Name]
- INN: [name]
- Brand: [name]
- MOA: [mechanism]
- Primary targets: [target 1 (gene symbol)], [target 2]
- Target class: [class]
- Approved indications: [list]
- ChEMBL ID: [ID]
- Source: ChEMBL, DrugCentral
```

### Step A2 — Identify Disease Associations for Each Target

For each primary target, search OpenTargets for:
- Diseases genetically associated with this target
- Overall association score (0-1)
- Evidence types: genetic association, somatic mutation, known drug, literature

Search DisGeNET for:
- Gene-disease associations
- Evidence score
- Source databases

Filter: association score ≥ 0.3 AND not already an approved indication.

### Step A3 — Search Clinical Evidence

For each candidate indication, search ClinicalTrials.gov:
- Any trials of this compound in this indication (any phase)
- Status: recruiting, completed, terminated
- Results posted?

Search PubMed:
- Case reports of off-label use
- Mechanistic studies in disease model
- Observational data

### Step A4 — Score and Rank Candidates

Score each candidate indication on 4 dimensions (0-100 each):

```
Mechanistic Plausibility (0-100):
- Target directly implicated in disease pathway: 80-100
- Target modulates upstream regulator: 50-79
- Target associated but mechanism unclear: 20-49
- Weak or indirect association: 0-19
Source: OpenTargets association score × 100

Clinical Evidence (0-100):
- Phase 3 RCT completed: 90-100
- Phase 2 completed with positive signal: 60-89
- Phase 1 or pilot study: 30-59
- Case reports only: 10-29
- No clinical evidence: 0-9
Source: ClinicalTrials.gov, PubMed

Safety Transfer (0-100):
- Known safety profile appropriate for new population: 80-100
- Minor monitoring adjustments needed: 60-79
- Significant safety concern in target population: 20-59
- Contraindicated or high-risk in target population: 0-19
Source: FDA label, published safety data

Unmet Need (0-100):
- High unmet need (>50% patients without adequate response): 80-100
- Moderate unmet need (25-50%): 50-79
- Low unmet need (<25%): 0-49
Source: Published epidemiology, treatment guidelines
```

Total Score = (Mechanistic × 0.35) + (Clinical × 0.30) + (Safety × 0.20) + (Unmet Need × 0.15)

### Step A5 — Output Ranked Candidates

```markdown
## Repurposing Candidates: [Compound Name]

| Rank | Indication | Total Score | Mechanistic | Clinical | Safety | Unmet Need | Evidence Classification |
|------|-----------|-------------|-------------|---------|--------|------------|------------------------|
| 1 | [Indication] | 74.2 | 85 | 60 | 78 | 82 | Mechanistic Hypothesis |
| 2 | [Indication] | 68.1 | 72 | 45 | 80 | 71 | Mechanistic Hypothesis |
| 3 | [Indication] | 61.5 | 65 | 30 | 75 | 68 | Mechanistic Hypothesis |

### Top Candidate Detail: [Indication 1]
Mechanistic rationale: [2-3 sentences explaining target-disease link, source: OpenTargets/PMID]
Clinical evidence: [what trials or case reports exist, NCT/PMID]
Safety transfer: [key considerations for this population]
Regulatory pathway: [505(b)(2) / full NDA / other — note this is indicative only]
Next step: [Phase 2 trial in [population] to establish proof of concept]

Classification: MECHANISTIC HYPOTHESIS — requires clinical validation before any therapeutic claim.
```

---

## Mode B: Indication → Compounds

### Step B1 — Characterize the Indication

Search OpenTargets for:
- Top genetic targets associated with indication
- Association scores
- Evidence types (GWAS, rare variant, somatic)

Search DisGeNET for:
- Additional gene-disease associations

Output top 10 targets by association score.

### Step B2 — Find Approved Compounds Hitting Those Targets

For each top target, search ChEMBL for:
- Approved drugs with activity at this target
- Selectivity (does it hit other targets that could cause safety issues?)
- Clinical stage compounds

Search DrugCentral for:
- Approved drugs with this MOA

### Step B3 — Filter for Feasibility

Exclude:
- Drugs already approved for this indication
- Drugs with known contraindication in target population
- Drugs with narrow therapeutic index unless strong mechanistic rationale

Include:
- Drugs approved in related indications with overlapping pathophysiology
- Drugs with completed Phase 1 safety in similar population
- Generic/off-patent drugs (lower development cost)

### Step B4 — Score and Rank (same 4-dimension scoring as Mode A)

### Step B5 — Gap Analysis

After ranking, identify:

```markdown
## Repurposing Gap Analysis: [Indication]

Highest opportunity: [Compound] — Score [X], [why this is the top candidate]

Underexplored targets:
- [Target 1]: High association score (X.XX) but no approved compounds in this indication
- [Target 2]: Druggable target with approved compounds in adjacent indications

Compounds with mechanistic rationale but no trials registered:
- [Compound A]: [MOA] → [why relevant] — no ClinicalTrials.gov registration found
- [Compound B]: [MOA] → [why relevant] — no ClinicalTrials.gov registration found

These represent highest-value repurposing opportunities:
high unmet need + existing approved compound + mechanistic rationale + no active development.
```

---

## Regulatory Pathway Note

For each candidate, indicate the most likely regulatory pathway.
Always label as indicative — never as legal or regulatory advice:

```
505(b)(2) — if same compound, new indication, existing safety data usable
Full NDA/BLA — if significant new clinical data required
Supplemental NDA — if already approved, indication expansion
Orphan Drug — if indication qualifies (<200K US patients)
Biosimilar — not applicable for repurposing
```

---

## Final Output

Save to: `/mnt/user-data/outputs/repurposing_[compound_or_indication]_[YYYY-MM-DD].md`

Structure:
1. Query Summary (mode, compound/indication, scope)
2. Compound/Indication Profile
3. Target-Disease Association Map
4. Clinical Evidence Summary
5. Ranked Candidates with Scores
6. Top 3 Candidate Deep Dives
7. Gap Analysis
8. Regulatory Pathway Notes
9. Audit Trail (all databases queried, search dates, result counts)

---

## Mandatory Classifications

Every candidate in every output must carry:

```
Classification: MECHANISTIC HYPOTHESIS
This candidate is based on target-disease association and/or preclinical/
early clinical evidence. It does not constitute proof of therapeutic benefit
in the proposed indication. Clinical validation in appropriately powered
trials is required before any therapeutic claim can be made.
Source provenance: [list all databases queried with dates]
```

---

## Governance Notice

Drug repurposing analyses produced by this skill are research intelligence
tools for hypothesis generation only. They do not constitute medical advice,
regulatory guidance, or investment recommendations. Mechanistic plausibility
scores are associative heuristics — they do not predict clinical trial outcomes.
Safety transfer assessments are based on published label data and do not
account for individual patient factors. All outputs require review by qualified
clinical pharmacologists, regulatory affairs professionals, and medical affairs
teams before use in any development, regulatory, or commercial decision.
