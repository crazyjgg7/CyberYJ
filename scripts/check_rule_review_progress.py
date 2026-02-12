#!/usr/bin/env python3
"""
检查 M4-P3 规则核对矩阵进度
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.rule_review_progress import evaluate_rule_review_progress


def main() -> int:
    report = evaluate_rule_review_progress(
        str(ROOT / "data" / "review" / "rule_review_matrix.json")
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
