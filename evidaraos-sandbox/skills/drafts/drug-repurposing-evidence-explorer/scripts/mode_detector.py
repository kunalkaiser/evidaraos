#!/usr/bin/env python3
"""Detect drug repurposing workflow mode from a user question."""

from __future__ import annotations

import argparse
import json


def detect(question: str) -> str:
    q = question.lower()
    if any(term in q for term in ["what drugs", "which drugs", "approved compounds", "for this disease"]):
        return "indication_to_compounds"
    return "compound_to_indications"


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect repurposing workflow mode.")
    parser.add_argument("question")
    args = parser.parse_args()
    mode = detect(args.question)
    print(json.dumps({"question": args.question, "mode": mode, "human_confirmation_recommended": True}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

