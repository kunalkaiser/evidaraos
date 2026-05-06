# Human Review Queue

Use this queue to validate AI-assisted screening before final inclusion/exclusion.

| Record | Source | AI decision | AI confidence | Human action | Human decision | Exclusion reason | Reviewer | Timestamp | Notes |
|---|---|---|---:|---|---|---|---|---|---|
| <record_id> | <source> | <include/exclude/uncertain> | <confidence> | <agree/override/second-review-needed> | <decision> | <reason> | <reviewer_id> | <timestamp> | <notes> |

Reviewer actions:

- `agree`: human accepts AI decision.
- `override`: human changes AI decision.
- `second-review-needed`: adjudication or second reviewer required.
- `pending`: not yet reviewed.

Final exclusion requires a human-readable reason.
