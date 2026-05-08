# Zero-Shot Repurposing Summary

## Query Disease

<disease and feature set>

## Similar Disease Support

| Similar Disease | Score | Shared Features | Review Notes |
|---|---:|---|---|
| <disease> | <score> | <features> | requires expert review |

## Candidate Ranking

| Candidate Pair | Zero-Shot Score | Indication Signal | Contraindication Signal | Review Status |
|---|---:|---:|---:|---|
| <drug -> disease> | <score> | <score> | <score> | hypothesis only |

## Multi-Hop Explanation Paths

| Candidate Pair | Top Path | Path Score | Review Focus |
|---|---|---:|---|
| <candidate> | <path> | <score> | mechanism or safety |

## Human Explanation Review

<mechanistic plausibility, clinical usefulness, safety concern, missing evidence, and overclaim risk>

## Guardrails

- This is not TxGNN and does not reproduce TxGNN benchmark performance.
- Similar disease support and graph paths are hypothesis-generation signals only.
- External usage signals, if provided, are not causal evidence.
- Expert scientific and safety review is required before any development decision.
