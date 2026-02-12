#!/usr/bin/env python3
"""
M4 最终权威版替换检查：
默认检查结构合法；可通过 --strict 要求全部替换完成。
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

from cyberYJ.utils.rule_review_final_authority import (
    evaluate_rule_review_final_authority,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：要求 ready_for_final_authority_closeout=true",
    )
    args = parser.parse_args()

    report = evaluate_rule_review_final_authority(
        str(ROOT / "data" / "review" / "rule_review_evidence.json")
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not report["passed"]:
        return 1
    if args.strict and not report["ready_for_final_authority_closeout"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
