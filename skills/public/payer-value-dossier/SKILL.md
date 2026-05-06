---
name: payer-value-dossier
display_name: Pharmaceutical Payer Value Dossier
version: 1.0.0
author: Evidara OS
description: >
  Generates a complete payer value dossier for pharmaceutical market access.
  Synthesizes clinical evidence, HTA precedents, comparator landscape,
  and health economics modeling into an 8-section value brief.
  Designed for medical affairs, market access, and HEOR teams preparing
  for payer committee submissions.
compatibility: ">=2.0.0"
tags:
  - pharma
  - payer
  - market-access
  - HTA
  - HEOR
  - value-dossier
  - medical-affairs
  - reimbursement
---

# Pharmaceutical Payer Value Dossier

## When to use this skill

Use this skill when the user asks for:
- Payer value dossier or value brief for a drug or indication
- HTA submission preparation (NICE, CADTH, G-BA, AIFA, TLV)
- Market access evidence package
- Reimbursement landscape analysis
- Payer committee preparation
- ICER range estimation or budget impact modeling
- Comparator landscape or standard of care analysis
- "What will payers ask about this drug?"
- Any task mentioning value dossier, formulary, reimbursement, HTA, ICER, QALY

Do NOT use for:
- Clinical trial design (use pharma-slr)
- Regulatory submission drafting (use regulatory-briefing)
- Raw literature search without payer framing

---

## Core Methodology

This skill produces an 8-section value dossier structured for payer committee review.
It enforces evidence integrity rules throughout:

1. All health economics outputs are modeled estimates with stated assumptions — never presented as actuarial fact
2. ICER is always a range, never a point estimate
3. Comparator landscape cites only approved treatments — pipeline is noted separately
4. HTA precedents are descriptive — never used to predict regulatory outcomes
5. Every efficacy claim traces to a PMID or NCT ID
6. Unmet need is quantified from epidemiological data, not asserted
7. Association is never upgraded to causation

---

## Step 1 — Define the Value Dossier Scope

Before building, confirm:

```
Drug/Compound:        [INN name, brand name if approved]
Indication:           [specific indication, line of therapy]
Target market(s):     [US / EU5 / Canada / Australia / global]
Comparator(s):        [current standard of care, active comparators]
Submission target:    [NICE / CADTH / G-BA / formulary / all]
Evidence available:   [Phase 2 / Phase 3 / approved / post-market]
Price point:          [known / estimated / not specified]
```

State all assumptions explicitly before proceeding.

---

## Step 2 — Disease Burden and Unmet Need

Quantify from published epidemiological sources:

### Epidemiology
Search CDC Wonder, IHME GBD, NCI SEER, published registry studies for:
- Incidence (new cases per year, per 100K)
- Prevalence (total cases, per 100K)
- Population breakdown by age, sex, geography
- Disease progression rates and natural history

### Current Standard of Care Gaps
- What treatments exist? What do they achieve?
- What proportion of patients achieve adequate response?
- What are the unmet needs in non-responders, specific subgroups?
- What is the treatment burden (frequency, route, monitoring)?

### Patient Impact
- Quality of life burden (published EQ-5D, SF-36, PRO data)
- Economic burden to patients and caregivers
- Work productivity loss where published

Output format:
```markdown
## Disease Burden Summary
- Incidence: [X per 100K, source: PMID/registry]
- Prevalence: [X per 100K, source: PMID/registry]
- Unmet need: [% patients without adequate response on SoC, source]
- QoL burden: [EQ-5D utility score on SoC, source]
- Key evidence gap: [what SoC fails to address]
```

---

## Step 3 — Clinical Evidence Summary

Run targeted evidence synthesis (abbreviated SLR if full not already available):

### Efficacy Evidence
- Primary endpoint: result, CI, p-value, source PMID/NCT
- Key secondary endpoints: results with source
- Subgroup findings: pre-specified subgroups only
- Durability: follow-up duration, maintenance of effect

### Safety Evidence
- SAE rate vs comparator
- Discontinuation rate and reasons
- Key adverse events of interest
- Long-term safety data if available
- FAERS signal status

### Evidence Quality (abbreviated GRADE)
- Study design, N, follow-up
- Risk of bias assessment
- Overall GRADE rating per primary outcome

Evidence classification on every claim:
- Causal: RCT primary endpoint, adequate power, ITT analysis
- Associative: observational, indirect comparison
- Descriptive: reported result, no inference

---

## Step 4 — Comparator Landscape

### Approved Treatments in Indication
Search FDA Orange Book, EMA EPAR, published treatment guidelines:

| Treatment | Mechanism | Line | Key Efficacy | Key Safety | Approval Year |
|-----------|-----------|------|-------------|------------|---------------|
| [Drug 1]  | [MOA]     | 1L   | [result]    | [SAE rate] | [year]        |
| [Drug 2]  | [MOA]     | 2L   | [result]    | [SAE rate] | [year]        |

### Head-to-Head Evidence
- Direct RCT comparisons: state results with PMID
- Indirect comparisons (NMA/MTC): label as indirect, state methodology
- No head-to-head: state explicitly as evidence gap

### Mechanism Differentiation
- How does the drug's MOA differ from existing treatments?
- Does differentiation translate to clinical benefit in specific subgroups?
- Label all MOA claims as Causal Hypothesis unless confirmed in RCT

### Pipeline (not comparators — noted separately)
- Late-stage pipeline compounds (Phase 3) in same indication
- Expected approval timeline if publicly disclosed
- Source: ClinicalTrials.gov only

---

## Step 5 — HTA Precedents

Search public HTA databases for reimbursement decisions in same indication or drug class:

### NICE (UK)
Search: https://www.nice.org.uk/guidance (Technology Appraisals)
Extract: decision (recommended/not recommended/restricted), ICER accepted, access conditions, date

### CADTH (Canada)
Search: https://www.cadth.ca/reimbursement-review-reports
Extract: recommendation, conditions, ICER threshold applied

### G-BA (Germany)
Search: https://www.g-ba.de/beschluesse/
Extract: additional benefit rating (major/considerable/minor/none), comparator used

### EMA EPAR
Search: https://www.ema.europa.eu/en/medicines/
Extract: approved indication, label restrictions, REMS equivalent

### Output Format:
```markdown
## HTA Precedent Summary

| Agency | Drug/Class | Decision | ICER Accepted | Access Conditions | Year |
|--------|-----------|---------|---------------|-------------------|------|
| NICE   | [drug]    | Recommended with CED | £X-Y/QALY | PAS required | 20XX |
| CADTH  | [drug]    | Reimburse with conditions | N/A | Criteria of use | 20XX |
| G-BA   | [drug]    | Considerable benefit | N/A | IQWiG assessment | 20XX |

### Predicted Payer Questions
Based on HTA precedent patterns, prepare for:
1. [Question 1 — most likely based on precedents]
2. [Question 2]
3. [Question 3]
4. [Question 4]
5. [Question 5]
```

Predicted payer questions must be grounded in actual HTA decision rationale —
not generic. Reference the specific precedent that drives each question.

---

## Step 6 — Health Economics Model

All outputs in this section are modeled estimates.
Every number must be labeled: "modeled estimate based on [source and assumption]"
Never present as actuarial certainty.

### Cost-Effectiveness (ICER)

ICER range estimation methodology:
1. Base case utility: published EQ-5D on treatment vs SoC (source: PMID)
2. QALY gain: (utility on treatment - utility on SoC) × time horizon
3. Incremental cost: drug cost + admin + monitoring - offset costs
4. ICER = incremental cost ÷ QALY gain
5. Sensitivity range: vary utility ±20%, time horizon, discount rate

Output:
```markdown
## ICER Estimate
Base case ICER: $X,000 – $Y,000 per QALY gained
(modeled estimate; range reflects utility weight and time horizon uncertainty)

Assumptions:
- Utility on treatment: X.XX (source: PMID, EQ-5D)
- Utility on SoC: X.XX (source: PMID, EQ-5D)
- Time horizon: X years
- Discount rate: 3% costs, 3% outcomes (NICE base case)
- Drug cost: WAC price or estimated list price

NICE threshold: £20,000–£30,000/QALY
ICER vs threshold: [above / within / below / uncertain]
```

### Budget Impact (5-Year)

```markdown
## Budget Impact Estimate
Target population: [N patients eligible in market]
Market uptake assumption: Y1: X%, Y2: X%, Y3: X%, Y4: X%, Y5: X%
Annual drug cost per patient: $X (WAC or estimated)
Offset: $X reduction in hospitalization/SoC costs (source: PMID)

5-year cumulative budget impact: $X million – $Y million
(modeled estimate; range reflects uptake and offset assumptions)
Per-member-per-month (PMPM): $X.XX – $Y.YY
```

### Cost Offsets
Quantify avoided costs from:
- Reduced hospitalizations (published event rates × DRG cost)
- Reduced SoC drug costs
- Reduced monitoring/procedure costs
- Productivity gains (where published and relevant)

All offset calculations cite source for event rates and unit costs.

---

## Step 7 — Evidence Gaps and Residual Risk

Structure explicitly — this section builds payer trust:

```markdown
## Evidence Gaps
1. [Gap 1]: No head-to-head RCT vs [comparator] — indirect comparison only
2. [Gap 2]: Limited follow-up data beyond [X months]
3. [Gap 3]: Underrepresented populations: [elderly / pediatric / renal impairment]
4. [Gap 4]: No published real-world evidence
5. [Gap 5]: Health economics model based on trial data, not real-world outcomes

## Residual Risks
1. [Risk 1]: Long-term safety profile not established beyond [X months]
2. [Risk 2]: ICER sensitive to utility weight assumption — high uncertainty
3. [Risk 3]: Subgroup benefit not pre-specified — exploratory only
4. [Risk 4]: Budget impact assumes [X]% uptake — actual uptake uncertain
```

---

## Step 8 — Executive Summary (1 Page)

Write last, after all sections complete. Decision-ready for non-specialist payer reviewer:

```markdown
## Executive Summary

[Drug] is a [mechanism] approved/in development for [indication].
It demonstrates [primary outcome result] vs [comparator] in [trial name]
(GRADE: [rating], source: PMID/NCT).

Disease burden: [X] patients affected in [market], with [Y]% achieving
inadequate response on current standard of care.

Payer value proposition:
- Clinical: [one sentence on key efficacy differentiation]
- Safety: [one sentence on safety profile vs comparator]
- Economic: ICER estimated at $X,000–$Y,000/QALY (modeled estimate)
- Access: [precedent-based access pathway recommendation]

Key uncertainties requiring human review:
- [Top 2-3 evidence gaps most likely to drive payer questions]

This brief was generated by Evidara OS and requires review by a
qualified health economist and medical affairs professional before
submission or external use.
```

---

## Final Output

Save to: `/mnt/user-data/outputs/vd_[drug]_[indication]_[YYYY-MM-DD].md`

Also generate PDF if requested using the pdf skill.

Structure:
1. Executive Summary
2. Disease Burden and Unmet Need
3. Clinical Evidence Summary
4. Comparator Landscape
5. HTA Precedents and Predicted Payer Questions
6. Health Economics (ICER range, budget impact, cost offsets)
7. Evidence Gaps and Residual Risk
8. Audit Trail (all sources, search dates, databases queried)

---

## Governance Notice

All outputs from this skill are intended for research and
decision-support purposes only. Health economics estimates are
modeled ranges based on published inputs — they are not actuarial
projections and should not be submitted to payers without review
and validation by a qualified health economist. HTA precedents are
descriptive and do not predict future reimbursement decisions.
Every efficacy and safety claim traces to a published PMID or NCT ID.
Human review by a qualified medical affairs or market access
professional is required before any external use.
