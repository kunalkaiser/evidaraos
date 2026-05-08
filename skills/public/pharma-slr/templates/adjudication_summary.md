# Dual-Reviewer Adjudication Summary

## Overview

| Metric | Count |
|---|---:|
| Records compared | <records_compared> |
| Agreements | <agreements> |
| Conflicts | <conflicts> |
| Locked final labels | <locked_final_labels> |
| Pending adjudication | <pending_adjudication> |
| Pending locked label | <pending_locked_label> |
| Lock policy | <lock_policy> |
| Inter-reviewer raw agreement | <raw_agreement> |
| Inter-reviewer Cohen's kappa | <cohens_kappa> |

## Conflict Types

| Conflict type | Count |
|---|---:|
| include_vs_exclude | <count> |
| different_exclusion_reason | <count> |
| confidence_disagreement | <count> |
| extraction_field_disagreement | <count> |
| needs_full_text_review | <count> |

## Adjudication Worklist

| Record | Reviewer 1 | Reviewer 2 | Agreement | Conflict type | Adjudicator | Adjudicator decision | Final decision | Final exclusion reason | Notes |
|---|---|---|---|---|---|---|---|---|---|
| <record_id> | <decision> | <decision> | <agreement/conflict> | <type> | <adjudicator_id> | <decision> | <decision> | <reason> | <notes> |

Final decisions must be made by an adjudicator or agreed dual-review process before regulator-facing inclusion/exclusion counts are treated as final.

Lock policy options:
- `agreement_or_adjudicated`: lock agreed dual-review labels and adjudicated conflict labels.
- `adjudicated_only`: lock only labels with an adjudicator decision.
- `require_adjudicator_signature`: lock only labels with adjudicator ID and signature metadata.

## Locked Labels

| Record | Final decision | Final exclusion reason | Adjudicator | Signature | Lock policy | Locked at |
|---|---|---|---|---|---|---|
| <record_id> | <decision> | <reason> | <adjudicator_id> | <signature> | <lock_policy> | <timestamp> |
