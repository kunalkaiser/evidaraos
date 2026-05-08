#!/usr/bin/env python3
"""Evaluate payer dossier claim traceability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build claim traceability matrix.")
    parser.add_argument("claims_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.claims_json).read_text(encoding="utf-8"))
    claims = payload if isinstance(payload, list) else payload.get("claims", [])
    rows = []
    unsupported = 0
    for claim in claims:
        sources = claim.get("sources") or []
        traceable = bool(sources)
        unsupported += 0 if traceable else 1
        rows.append(
            {
                "claim_id": claim.get("claim_id", ""),
                "claim": claim.get("claim", ""),
                "section": claim.get("section", ""),
                "sources": sources,
                "traceable": traceable,
                "review_status": "ready_for_review" if traceable else "unsupported_requires_revision",
            }
        )
    print(json.dumps({"claims": rows, "summary": {"total": len(rows), "unsupported": unsupported}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

