#!/usr/bin/env python3
"""Generate a payer dossier outline from scope JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate payer dossier outline.")
    parser.add_argument("scope_json")
    args = parser.parse_args()
    payload = json.loads(Path(args.scope_json).read_text(encoding="utf-8"))
    scope = payload.get("dossier_scope", payload)
    sections = payload.get("sections") or ["executive_summary", "disease_burden", "clinical_evidence", "heor_evidence", "claim_traceability"]
    markdown = [f"# Payer Value Dossier: {scope.get('product', '')} in {scope.get('indication', '')}", ""]
    for section in sections:
        markdown.extend([f"## {section.replace('_', ' ').title()}", "Evidence and claims pending source-traceable drafting.", ""])
    print(json.dumps({"outline_markdown": "\n".join(markdown), "sections": sections}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

