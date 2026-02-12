#!/usr/bin/env python3
"""
M4 二次复核门禁检查（页码/段落级证据准备度）
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.rule_review_secondary_gate import evaluate_rule_review_secondary_gate


def main() -> int:
    report = evaluate_rule_review_secondary_gate(
        str(ROOT / "data" / "review" / "rule_review_evidence.json")
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
