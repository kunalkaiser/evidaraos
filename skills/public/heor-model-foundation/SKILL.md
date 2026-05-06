---
name: heor-model-foundation
display_name: HEOR Model Foundation
version: 1.0.0
author: Evidara OS
description: >
  Builds the evidence foundation for health economics and outcomes research
  models. Extracts utility weights, event rates, resource utilization,
  and cost inputs from published literature. Produces structured model
  input tables ready for health economist review. All outputs are
  modeled estimates requiring validation by a qualified health economist.
compatibility: ">=2.0.0"
tags:
  - HEOR
  - health-economics
  - cost-effectiveness
  - QALY
  - utility
  - budget-impact
  - outcomes-research
  - payer
---

# HEOR Model Foundation

## When to use this skill

Use this skill when the user asks for:
- Health economics model inputs (utilities, costs, event rates)
- QALY calculations or estimates
- Cost-effectiveness model structure
- Budget impact model foundation
- Published utility weights for a condition
- Resource utilization data from clinical trials
- Cost inputs for pharmacoeconomic model
- Model validation inputs
- "What are the published utilities for [condition]?"
- "Help me build the evidence foundation for my cost-effectiveness model"

Do NOT use for:
- Full model programming (Excel, R, Python modeling — use code skill)
- Finalizing a model without health economist review
- Producing cost-effectiveness results for submission without validation

---

## Core Principles

1. All outputs are modeled estimates — never presented as definitive economic results
2. Every input traces to a published source with PMID
3. Utility weights are extracted from specific instruments (EQ-5D, SF-6D) and populations
4. Cost inputs use publicly available sources (CMS, published literature, DRG)
5. Uncertainty ranges reported for every input
6. Model structure recommendations are indicative — health economist review required
7. Results are ranges, never point estimates presented without sensitivity analysis

---

## Step 1 — Define Model Scope

Confirm before proceeding:

```
Condition/Indication:   [specific disease, severity, line of therapy]
Intervention:           [drug, dose, comparator]
Comparator:             [SoC, placebo, active comparator]
Model perspective:      [payer / societal / healthcare system]
Time horizon:           [lifetime / X years — specify]
Target market:          [US / UK / Canada / EU / global]
Model type:             [cost-effectiveness / budget impact / cost-utility / cost-minimization]
Target submission:      [NICE / CADTH / payer dossier / publication]
Key data available:     [trial data, observational, claims — user specifies]
```

---

## Step 2 — Utility Weight Extraction

Search published literature for health state utility values.

### Search Strategy
PubMed search:
```
("[condition]"[tiab] OR "[condition MeSH]") AND 
("utility"[tiab] OR "EQ-5D"[tiab] OR "SF-6D"[tiab] OR "QALY"[tiab] OR 
"health state"[tiab] OR "quality of life"[tiab])
```

Also search:
- NICE Evidence Reviews for condition (published utility values)
- EuroQol Group database (https://euroqol.org/publications/)
- Health Utility Index (HUI) publications

### Data Extraction for Each Utility Source:

```markdown
| Health State | Utility Value | Instrument | Population | N | Source |
|-------------|--------------|------------|------------|---|--------|
| On treatment, responder | 0.XXX (95% CI: X.XX-X.XX) | EQ-5D-3L | [population] | [N] | PMID:XXXXX |
| On treatment, non-responder | 0.XXX | EQ-5D-3L | [population] | [N] | PMID:XXXXX |
| SoC / comparator | 0.XXX | EQ-5D-3L | [population] | [N] | PMID:XXXXX |
| Disease progression | 0.XXX | EQ-5D-3L | [population] | [N] | PMID:XXXXX |
| Adverse event: [event] | 0.XXX (decrement) | [instrument] | [population] | [N] | PMID:XXXXX |
| Death | 0.000 | — | — | — | Assumption |
```

### Utility Recommendation:

```markdown
## Recommended Utility Inputs

Base case:
- On-treatment utility: X.XXX (source: PMID, preferred because: largest N, EQ-5D-3L, UK tariff)
- Comparator utility: X.XXX (source: PMID)
- QALY gain per year: X.XXX - X.XXX (treatment utility - comparator utility)

Sensitivity analysis range:
- Low: X.XXX (source: PMID — most conservative published value)
- High: X.XXX (source: PMID — most optimistic published value)

Uncertainty note: Utility values vary by instrument (EQ-5D-3L vs 5L vs SF-6D),
country tariff applied (UK vs US vs Canada), and population (trial vs real-world).
Specify instrument and tariff in model documentation.
```

---

## Step 3 — Clinical Event Rates

Extract event rates from clinical trials and published literature.

### For Each Key Clinical Event:

Search pivotal trial publications (by NCT ID or PMID) for:
- Annual event rates in treatment arm
- Annual event rates in comparator arm
- Relative risk reduction with 95% CI
- Absolute risk reduction
- Number needed to treat (NNT)

Search published natural history studies for:
- Background event rates without treatment
- Disease progression rates
- Mortality rates by disease stage

### Output Table:

```markdown
## Clinical Event Rate Inputs

| Event | Rate (Treatment) | Rate (Comparator) | RRR | ARR | NNT | Source |
|-------|-----------------|------------------|-----|-----|-----|--------|
| Primary endpoint | X.X%/yr | Y.Y%/yr | XX% (CI: XX-XX%) | X.X% | XX | NCT:XXXXX, PMID:XXXXX |
| Hospitalization | X.X%/yr | Y.Y%/yr | XX% | X.X% | XX | PMID:XXXXX |
| Disease progression | X.X%/yr | Y.Y%/yr | XX% | X.X% | XX | PMID:XXXXX |
| Death (all cause) | X.X%/yr | Y.Y%/yr | XX% | X.X% | XX | PMID:XXXXX |
| SAE: [event] | X.X% | Y.Y% | — | — | — | PMID:XXXXX |

Evidence classification: Causal (RCT primary/secondary) or Associative (post-hoc/observational)
```

---

## Step 4 — Cost Inputs

Extract published cost data from appropriate sources.

### Drug Costs
- WAC (Wholesale Acquisition Cost): search drugs@fda, manufacturer website
- ASP (Average Sales Price) for Medicare: CMS ASP files
- Net price estimate: published payer analyses, ICER assessments
- Comparator drug costs: same sources

### Healthcare Resource Utilization (HCRU)
Search trial publications and published HCRU studies:
- Hospitalizations: frequency, length of stay, cost per episode
- Outpatient visits: frequency, cost per visit
- Procedure costs: DRG codes, CMS rate
- Monitoring costs: lab tests, imaging frequency

### Cost Sources by Market:

**US:**
- Drug: WAC from FDA/manufacturer
- Hospital: CMS DRG rates (https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment)
- Physician: CMS Physician Fee Schedule
- Lab: CMS Clinical Lab Fee Schedule

**UK:**
- Drug: BNF price
- Hospital: NHS Reference Costs
- NICE costing templates where available

**Canada:**
- Drug: Ontario Drug Benefit formulary or published provincial costs
- Hospital: CIHI Cost per Weighted Case

### Output Table:

```markdown
## Cost Inputs

| Cost Item | Unit Cost | Frequency | Annual Cost | Source | Year |
|-----------|----------|-----------|-------------|--------|------|
| [Drug] | $X,XXX/unit | X doses/yr | $XX,XXX | WAC, [date] | 20XX |
| Comparator | $X,XXX/unit | X doses/yr | $XX,XXX | WAC, [date] | 20XX |
| Hospitalization | $XX,XXX/episode | X/yr | $XX,XXX | CMS DRG XXX | 20XX |
| Outpatient visit | $XXX/visit | X/yr | $X,XXX | CMS PFS | 20XX |
| Lab monitoring | $XX/test | X/yr | $XXX | CMS CLFS | 20XX |

Inflation adjustment: All costs in [year] USD/GBP/CAD. Adjust to model year using CPI.
```

---

## Step 5 — Model Structure Recommendation

Based on disease and evidence base, recommend model structure:

```markdown
## Recommended Model Structure

### Model Type: [Partitioned Survival / Markov State Transition / Decision Tree]

Rationale: [why this structure is appropriate for this indication and evidence base]

### Health States:
1. [State 1: e.g., Progression-Free on Treatment]
2. [State 2: e.g., Progressed]
3. [State 3: e.g., Death]

### Transition Probabilities:
- State 1 → State 2: derived from [PFS data, parametric extrapolation]
- State 2 → State 3: derived from [OS data, parametric extrapolation]
- Extrapolation method: [exponential / Weibull / log-normal — recommend fitting to trial KM data]

### Key Assumptions to Document:
1. [Assumption 1: e.g., treatment effect wanes after X years]
2. [Assumption 2: e.g., utility values constant within health state]
3. [Assumption 3: e.g., costs constant over time]

### Sensitivity Analyses Required:
- One-way: vary each input ±20%
- Probabilistic (PSA): beta distributions for utilities, gamma for costs, log-normal for RR
- Scenario: alternative time horizon, alternative comparator, subgroup populations

Classification: Model structure recommendation is indicative.
Final model design requires review by a qualified health economist familiar
with target HTA body requirements.
```

---

## Step 6 — QALY Calculation Summary

Produce an estimated QALY calculation for transparency:

```markdown
## QALY Calculation Summary (Illustrative)

Inputs used:
- On-treatment utility: X.XXX (PMID:XXXXX)
- Comparator utility: X.XXX (PMID:XXXXX)
- Time horizon: X years
- Discount rate: X% (NICE standard: 3.5%; US: 3%)

Calculation:
- QALY on treatment: X.XXX utility × X years × discount factor = X.XXX QALYs
- QALY on comparator: X.XXX utility × X years × discount factor = X.XXX QALYs
- Incremental QALYs: X.XXX - X.XXX = X.XXX QALYs

Incremental cost: $XXX,XXX - $XXX,XXX = $XXX,XXX

ICER estimate: $XXX,XXX ÷ X.XXX = $XXX,XXX per QALY
(modeled estimate based on published inputs — range: $XXX,XXX – $XXX,XXX)

Sensitivity: ICER range varies from $XXX,XXX to $XXX,XXX
across utility and cost assumptions.

WTP threshold comparison:
- NICE: £20,000–£30,000/QALY → [above/within/below threshold]
- ICER (US): $100,000–$150,000/QALY → [above/within/below threshold]
- CADTH: No fixed threshold (contextual factors considered)

Classification: MODELED ESTIMATE. This calculation uses published
utility and cost inputs and is not a validated health economic model.
It should be used only as a starting point for model development.
```

---

## Final Output

Save to: `/mnt/user-data/outputs/heor_[drug]_[indication]_[YYYY-MM-DD].md`

Structure:
1. Model Scope and Assumptions
2. Utility Weight Inputs (with sources)
3. Clinical Event Rate Inputs (with sources)
4. Cost Inputs (with sources)
5. Model Structure Recommendation
6. Illustrative QALY Calculation
7. Uncertainty and Sensitivity Analysis Plan
8. Health Economist Review Checklist
9. Audit Trail (all searches, databases, dates)

---

## Health Economist Review Checklist

Include at end of every output:

```markdown
## Required Health Economist Review

Before this foundation is used in any model, a qualified health economist must verify:

- [ ] Utility values appropriate for target HTA body (EQ-5D tariff matches country)
- [ ] Health states reflect natural history of condition correctly
- [ ] Event rates from appropriate population (trial vs real-world as needed)
- [ ] Cost inputs current and from appropriate source for target market
- [ ] Model structure appropriate for indication and data available
- [ ] Time horizon justified and documented
- [ ] Discount rates appropriate for target submission
- [ ] All assumptions documented with rationale
- [ ] PSA distributions appropriate for each input
- [ ] Scenario analyses cover key uncertainties identified by target HTA body

This output was generated by Evidara OS HEOR Model Foundation skill.
It is a research synthesis tool for evidence identification and
model scoping — not a validated health economic model.
Submission to any HTA body requires full model development,
validation, and review by a qualified health economist.
```

---

## Governance Notice

Health economics outputs from this skill are modeled estimates based
on published inputs. They are intended to support model scoping and
evidence identification — not to replace full health economic modeling.
ICER estimates and QALY calculations are illustrative and carry
substantial uncertainty. They must not be used in payer submissions,
regulatory documents, or public communications without validation
by a qualified health economist and review by medical affairs and
regulatory affairs professionals. All cost and utility inputs
should be verified for currency and applicability to the target
market and submission before use.
