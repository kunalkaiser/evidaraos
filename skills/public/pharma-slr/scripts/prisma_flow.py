#!/usr/bin/env python3
"""Create a structured PRISMA-style flow summary."""

from __future__ import annotations

import argparse
import json
import sys


def build_prisma_summary(
    identified: int,
    deduplicated: int,
    screened: int,
    excluded: int,
    full_text_assessed: int,
    final_included: int,
    very_likely_include: int = 0,
    possible_include: int = 0,
    uncertain_human_review: int = 0,
    likely_exclude: int = 0,
    background_only: int = 0,
    ai_prioritized_records: int = 0,
    human_review_required_records: int = 0,
) -> dict:
    counts = {
        "identified": identified,
        "deduplicated": deduplicated,
        "screened": screened,
        "excluded": excluded,
        "full_text_assessed": full_text_assessed,
        "final_included": final_included,
        "precision_tiers": {
            "very_likely_include": very_likely_include,
            "possible_include": possible_include,
            "uncertain_human_review": uncertain_human_review,
            "likely_exclude": likely_exclude,
            "background_only": background_only,
        },
        "ai_prioritized_records": ai_prioritized_records,
        "human_review_required_records": human_review_required_records,
    }
    duplicates_removed = max(identified - deduplicated, 0)
    not_retrieved_or_not_assessed = max(screened - excluded - full_text_assessed, 0)
    full_text_excluded = max(full_text_assessed - final_included, 0)
    markdown_table = "\n".join(
        [
            "| PRISMA stage | Count |",
            "|---|---:|",
            f"| Records identified | {identified} |",
            f"| Records after deduplication | {deduplicated} |",
            f"| Duplicates removed | {duplicates_removed} |",
            f"| Records screened | {screened} |",
            f"| Records excluded at title/abstract screening | {excluded} |",
            f"| Records not retrieved or not assessed | {not_retrieved_or_not_assessed} |",
            f"| Full-text records assessed | {full_text_assessed} |",
            f"| Full-text records excluded or not eligible | {full_text_excluded} |",
            f"| Studies included in synthesis | {final_included} |",
            f"| AI-prioritized records | {ai_prioritized_records} |",
            f"| Human-review-required records | {human_review_required_records} |",
            f"| Precision tier: very likely include | {very_likely_include} |",
            f"| Precision tier: possible include | {possible_include} |",
            f"| Precision tier: uncertain human review | {uncertain_human_review} |",
            f"| Precision tier: likely exclude | {likely_exclude} |",
            f"| Precision tier: background only | {background_only} |",
        ]
    )
    return {
        "summary": {
            "counts": counts,
            "derived": {
                "duplicates_removed": duplicates_removed,
                "not_retrieved_or_not_assessed": not_retrieved_or_not_assessed,
                "full_text_excluded": full_text_excluded,
            },
        },
        "markdown_table": markdown_table,
    }


def _nonnegative(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("count must be non-negative")
    return parsed


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit a structured PRISMA-style JSON summary and markdown table.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  python prisma_flow.py --identified 60 --deduplicated 45 --screened 45 --excluded 30 --full-text-assessed 15 --final-included 10\n",
    )
    parser.add_argument("--identified", required=True, type=_nonnegative)
    parser.add_argument("--deduplicated", required=True, type=_nonnegative)
    parser.add_argument("--screened", required=True, type=_nonnegative)
    parser.add_argument("--excluded", required=True, type=_nonnegative)
    parser.add_argument("--full-text-assessed", required=True, type=_nonnegative, dest="full_text_assessed")
    parser.add_argument("--final-included", required=True, type=_nonnegative, dest="final_included")
    parser.add_argument("--very-likely-include", type=_nonnegative, default=0, dest="very_likely_include")
    parser.add_argument("--possible-include", type=_nonnegative, default=0, dest="possible_include")
    parser.add_argument("--uncertain-human-review", type=_nonnegative, default=0, dest="uncertain_human_review")
    parser.add_argument("--likely-exclude", type=_nonnegative, default=0, dest="likely_exclude")
    parser.add_argument("--background-only", type=_nonnegative, default=0, dest="background_only")
    parser.add_argument("--ai-prioritized-records", type=_nonnegative, default=0, dest="ai_prioritized_records")
    parser.add_argument("--human-review-required-records", type=_nonnegative, default=0, dest="human_review_required_records")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        result = build_prisma_summary(
            args.identified,
            args.deduplicated,
            args.screened,
            args.excluded,
            args.full_text_assessed,
            args.final_included,
            args.very_likely_include,
            args.possible_include,
            args.uncertain_human_review,
            args.likely_exclude,
            args.background_only,
            args.ai_prioritized_records,
            args.human_review_required_records,
        )
    except Exception as exc:
        print(f"prisma_flow.py: {exc}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
