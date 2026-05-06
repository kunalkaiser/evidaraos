---
name: regulatory-briefing
display_name: Regulatory Benefit-Risk Intelligence
version: 1.0.0
author: Evidara OS
description: >
  Builds regulatory benefit-risk frameworks aligned with FDA, EMA, and PMDA
  expectations. Synthesizes clinical evidence into structured benefit-risk
  assessments, identifies regulatory precedents, and generates submission-ready
  language. All outputs require human regulatory review before use.
compatibility: ">=2.0.0"
tags:
  - pharma
  - regulatory
  - benefit-risk
  - FDA
  - EMA
  - PMDA
  - submission
  - medical-affairs
---

# Regulatory Benefit-Risk Intelligence

## When to use this skill

Use this skill when the user asks for:
- Benefit-risk framework or assessment for a drug
- Regulatory strategy analysis (FDA, EMA, PMDA, Health Canada)
- Submission-ready language for clinical findings
- Regulatory precedent analysis for an indication or drug class
- IND, NDA, BLA, or MAA preparation support
- Advisory committee (AdCom) preparation
- Label negotiation strategy
- Risk management program (REMS/RMP) landscape
- "What will FDA ask about this drug?"
- "How has EMA treated similar drugs?"

Do NOT use for:
- Predicting regulatory approval outcomes — this skill never predicts approvals
- Replacing regulatory affairs counsel — always flag for expert review
- Generating actual submission documents — outputs are drafts requiring review

---

## Core Principles

1. Never predict regulatory outcomes — present precedents only
2. Every regulatory claim traces to a public FDA/EMA document, PMID, or NCT ID
3. Benefit-risk is always framed in context of the specific indication and population
4. All submission language is conservative — never overclaims
5. Human regulatory review is required before any submission use — always stated
6. Residual uncertainty is always disclosed — never hidden

---

## Step 1 — Define Regulatory Context

Confirm before proceeding:

```
Drug/Compound:        [INN, brand if approved]
Indication:           [specific population, line of therapy, biomarker]
Target agency:        [FDA / EMA / PMDA / Health Canada / all]
Development stage:    [IND / Phase 2 / Phase 3 / NDA/BLA / Post-market]
Prior interactions:   [any prior agency meetings or feedback — user provides]
Submission type:      [NDA / BLA / MAA / sNDA / 505(b)(2) / other]
Key clinical data:    [pivotal trial names, NCT IDs]
```

---

## Step 2 — Regulatory Landscape

### FDA Precedents
Search FDA drugs@fda (https://www.accessdata.fda.gov/scripts/cder/daf/):
- All approved drugs in same indication
- Approval dates, review times, priority designations
- Complete Response Letters (CRLs) in indication if any
- Advisory committee votes and meeting minutes

Search FDA guidance documents:
- Indication-specific guidance (search: https://www.fda.gov/regulatory-information/search-fda-guidance-documents)
- Disease-specific draft or final guidances
- Key safety guidance relevant to drug class

### EMA Precedents
Search EMA EPAR database (https://www.ema.europa.eu/en/medicines/):
- EPARs for approved drugs in same class/indication
- CHMP assessment reports — extract key benefit-risk language
- Refused applications if any (what EMA found insufficient)
- EMA scientific guidelines for indication

### PMDA (Japan) — if requested
Search PMDA database for approval history in indication.

### Output:
```markdown
## Regulatory Precedent Summary

### FDA
Approved drugs in indication: [N drugs, list with approval years]
Priority designations used: [Breakthrough / Fast Track / Accelerated Approval / Priority Review]
Key precedents:
- [Drug 1]: Approved [year] on [primary endpoint], [N] patients in pivotal trial
- [Drug 2]: CRL issued [year] — reason: [inadequate safety data in [population]]
Relevant guidance: [guidance document title, date]

### EMA
Approved drugs in indication: [N drugs]
Key CHMP benefit-risk language from most recent approval:
"[quoted language from public EPAR — keep under 15 words, paraphrase rest]"
Refused applications: [any, reason]
```

---

## Step 3 — FDA Benefit-Risk Framework

Structure using FDA's 5-dimension benefit-risk framework
(from FDA PDUFA VI commitment — Benefit-Risk Assessment in Drug Regulatory Decision-Making):

```markdown
## FDA Benefit-Risk Framework: [Drug] for [Indication]

### Dimension 1: Analysis of Condition
- Severity: [life-threatening / serious / moderate / mild]
- Unmet medical need: [quantified — % patients without adequate response]
- Impact on daily functioning and quality of life
- Available therapies and their limitations
- Source: [published epidemiology, treatment guidelines — PMID]

### Dimension 2: Current Treatment Options
- Approved treatments: [list with key efficacy/safety data]
- Gaps in current therapy: [specific unmet needs]
- Why existing options are inadequate for [specific population]
- Source: [treatment guidelines, PMID]

### Dimension 3: Benefit Summary
Primary evidence of benefit:
- [Pivotal trial]: [primary endpoint result, CI, p-value] (NCT: [ID], PMID: [ID])
  Evidence classification: Causal (pre-specified RCT primary endpoint)
- Key secondary endpoints: [results with source]
- Subgroup consistency: [pre-specified subgroups, consistency noted]
- Durability: [follow-up data]

Benefit characterization:
- Magnitude: [clinically meaningful / modest / uncertain]
- Certainty: GRADE [High / Moderate / Low / Very Low]
- Generalizability: [applicable to broad population / restricted subgroup]

### Dimension 4: Risk Summary
Key risks identified:
| Risk | Incidence (drug) | Incidence (comparator) | Severity | Manageability |
|------|-----------------|----------------------|----------|---------------|
| [Risk 1] | X% | Y% | [Serious/Moderate] | [Manageable/Requires monitoring] |
| [Risk 2] | X% | Y% | [Serious/Moderate] | [Manageable/Requires monitoring] |

Source: [pivotal trial safety data, FAERS signal status — NCT/PMID]
Evidence classification: Causal (RCT) or Associative (observational/FAERS)

Long-term safety: [available / limited to X months / unknown]
Special populations: [pregnancy, pediatric, renal/hepatic impairment — data available?]

### Dimension 5: Benefit-Risk Summary and Assessment
Overall assessment:
"[Drug] demonstrates [benefit characterization] for [indication] with a risk profile
that is [manageable / requires risk minimization / uncertain]. The benefit-risk
balance is [favorable / uncertain / context-dependent] in [specific population]."

Uncertainties requiring human regulatory judgment:
1. [Uncertainty 1 — most significant]
2. [Uncertainty 2]
3. [Uncertainty 3]

This framework is a research synthesis and requires review by qualified
regulatory affairs professionals before submission use.
```

---

## Step 4 — EMA CHMP Framework (if requested)

Structure using EMA benefit-risk methodology (EMA/CHMP/15404/2014):

```markdown
## EMA Benefit-Risk Assessment: [Drug] for [Indication]

### Favorable Effects
Clinical context: [indication, population, severity]
Primary evidence: [pivotal trial result, source NCT/PMID]
Magnitude of effect: [absolute and relative, NNT where calculable]
Consistency: [across trials, subgroups, regions]
Clinical relevance: [is the endpoint a validated surrogate or clinical outcome?]

### Uncertainties / Limitations of Favorable Effects
- [Limitation 1: e.g., single pivotal trial, no active comparator]
- [Limitation 2: e.g., surrogate endpoint, clinical benefit not established]
- [Limitation 3: e.g., limited follow-up]

### Unfavorable Effects
Key risks: [list with incidence and severity]
Serious risks: [SAEs, deaths, discontinuations]
Uncertainty in risk: [long-term data gap, rare events not powered to detect]

### Uncertainties / Limitations of Unfavorable Effects
- [Gap 1: e.g., no comparative safety data vs active comparator]
- [Gap 2: e.g., limited data in elderly patients]

### Benefit-Risk Balance
"The benefit-risk balance of [drug] is [positive/negative/uncertain] for [indication]
given [primary benefit] offset by [primary risk], with the following risk minimization
measures recommended: [REMS/RMP elements if applicable]."

Classification: This assessment is a research synthesis.
EMA review and CHMP deliberation are required for actual regulatory determination.
```

---

## Step 5 — Submission Language Generator

Convert clinical findings to regulator-appropriate language.
Always conservative. Never overclaims. Flags where clinical data is insufficient.

### Input format:
```
Finding: [plain language description of clinical result]
Target agency: [FDA / EMA / PMDA]
Context: [efficacy / safety / benefit-risk / label]
```

### Output format:
```markdown
## Submission Language: [Finding]

### Plain Language Input:
"[User's original plain language finding]"

### FDA-Appropriate Language:
"[Conservative regulatory language — present tense, qualified, no superlatives]"
Caveat: [any qualification needed — e.g., "based on single trial data"]
Missing data flag: [if clinical data insufficient to support this language]

### EMA-Appropriate Language:
"[EMA style — often more detailed, explicit about uncertainty]"
Caveat: [qualifications]

### What NOT to say:
"[Example of overclaiming language to avoid]"
Reason: [why this would be rejected or queried]

Human review required: YES — regulatory language must be reviewed by
qualified regulatory affairs counsel before inclusion in any submission.
```

---

## Step 6 — Risk Management Landscape

Search for existing REMS (FDA) or RMP (EMA) in drug class:

```markdown
## Risk Management Landscape

### FDA REMS in Drug Class
- [Drug 1]: REMS type [ETASU / medication guide / communication plan], reason: [safety concern]
- [Drug 2]: REMS type, reason
Source: FDA REMS database (https://www.accessdata.fda.gov/scripts/cder/rems/)

### EMA RMP Elements in Drug Class
- Standard safety specification elements applicable
- Additional pharmacovigilance activities typical for class
- Risk minimization measures precedent

### Implications for [Drug]
Based on class precedent:
- Likely REMS/RMP elements: [list]
- Monitoring requirements: [list]
- Label warnings expected: [list]

Classification: Indicative only based on class precedent.
Actual REMS/RMP requirements determined by agency in review.
```

---

## Step 7 — Advisory Committee Preparation (if requested)

If AdCom preparation is in scope:

```markdown
## Advisory Committee Preparation: [Drug]

### Historical AdCom Votes in Indication
| Drug | Vote | Date | Key Concern Raised |
|------|------|------|-------------------|
| [Drug 1] | X-Y (yes-no) | [date] | [main concern] |

### Anticipated Questions Based on Precedent
1. [Question 1]: [why this will be asked, based on precedent]
   Suggested response framing: [how to frame the answer]

2. [Question 2]: [rationale]
   Suggested response framing: [framing]

3. [Question 3]: [rationale]
   Suggested response framing: [framing]

### Vulnerability Assessment
Strongest benefit argument: [what the data supports best]
Most vulnerable point: [where the data is weakest — be honest]
Risk mitigation narrative: [how to frame the risk-benefit for this vulnerability]

Classification: Preparation aid only. AdCom strategy requires
experienced regulatory affairs and medical affairs team review.
```

---

## Final Output

Save to: `/mnt/user-data/outputs/regulatory_[drug]_[indication]_[YYYY-MM-DD].md`

Structure:
1. Regulatory Context Summary
2. Regulatory Precedent (FDA + EMA)
3. FDA Benefit-Risk Framework (5 dimensions)
4. EMA CHMP Framework (if requested)
5. Submission Language (if specific findings provided)
6. Risk Management Landscape
7. AdCom Preparation (if requested)
8. Key Uncertainties and Human Review Requirements
9. Audit Trail

---

## Governance Notice

All outputs from this skill are research intelligence for regulatory
preparation purposes only. They do not constitute regulatory advice,
legal counsel, or a prediction of agency decisions. Submission language
drafts require review and approval by qualified regulatory affairs
professionals before inclusion in any IND, NDA, BLA, MAA, or agency
correspondence. Benefit-risk assessments reflect published evidence
and regulatory precedent — they do not reflect agency deliberations
or non-public information. Human regulatory review is mandatory
before any external use of outputs from this skill.
