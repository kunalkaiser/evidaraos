#!/usr/bin/env python3
"""Generate a model input table from candidate HEOR inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_items(path: str) -> list[dict]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get("inputs", [])


def build_table(items: list[dict]) -> dict:
    rows = []
    for item in items:
        source = item.get("source") or item.get("pmid") or item.get("doi") or ""
        rows.append(
            {
                "parameter": item.get("parameter", ""),
                "category": item.get("category", ""),
                "value": item.get("value", ""),
                "range_low": item.get("range_low", ""),
                "range_high": item.get("range_high", ""),
                "population": item.get("population", ""),
                "source": source,
                "confidence": item.get("confidence", "low" if not source else "medium"),
                "review_status": "needs_health_economist_review",
            }
        )
    markdown = ["| Parameter | Category | Value | Range | Population | Source | Confidence |", "|---|---|---:|---|---|---|---|"]
    for row in rows:
        rng = f"{row['range_low']} - {row['range_high']}".strip(" -")
        markdown.append(f"| {row['parameter']} | {row['category']} | {row['value']} | {rng} | {row['population']} | {row['source']} | {row['confidence']} |")
    return {"model_inputs": rows, "markdown_table": "\n".join(markdown)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a HEOR model input table.")
    parser.add_argument("input_json")
    args = parser.parse_args()
    print(json.dumps(build_table(load_items(args.input_json)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

