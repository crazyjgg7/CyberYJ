#!/usr/bin/env python3
"""
生成 M4 最终权威版替换清单报告。
"""

from __future__ import annotations

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
    report = evaluate_rule_review_final_authority(
        str(ROOT / "data" / "review" / "rule_review_evidence.json")
    )
    output_path = ROOT / "data" / "review" / "rule_review_final_replacement_report.json"
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    summary = {
        "output": str(output_path),
        "total_confirmed_records": report["total_confirmed_records"],
        "transitional_records_count": report["transitional_records_count"],
        "final_authority_ready_records": report["final_authority_ready_records"],
        "ready_for_final_authority_closeout": report["ready_for_final_authority_closeout"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
