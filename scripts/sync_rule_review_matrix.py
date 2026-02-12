#!/usr/bin/env python3
"""
M4-P3 根据证据台账同步规则状态（confirmed -> verified）
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.rule_review_status_sync import sync_rule_review_matrix_from_evidence


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Sync rule_review_matrix from rule_review_evidence")
    p.add_argument(
        "--matrix",
        default=str(ROOT / "data" / "review" / "rule_review_matrix.json"),
        help="Path to rule_review_matrix.json",
    )
    p.add_argument(
        "--evidence",
        default=str(ROOT / "data" / "review" / "rule_review_evidence.json"),
        help="Path to rule_review_evidence.json",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Output matrix path (only used when --apply)",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes to matrix file. Without this flag, dry-run only.",
    )
    return p


def main() -> int:
    args = build_parser().parse_args()
    report = sync_rule_review_matrix_from_evidence(
        matrix_path=args.matrix,
        evidence_path=args.evidence,
        dry_run=not args.apply,
        output_matrix_path=args.output,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
