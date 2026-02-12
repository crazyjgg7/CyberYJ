#!/usr/bin/env python3
"""
导出全量 summary locator 精度报告。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_locator_precision_full import (
    evaluate_authoritative_locator_precision_full,
)


def main() -> int:
    report = evaluate_authoritative_locator_precision_full(
        str(ROOT / "data" / "mappings" / "authoritative_text_map.json")
    )

    out = ROOT / "data" / "review" / "m4_locator_precision_full_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "output": str(out),
        "total_summary_items": report["total_summary_items"],
        "passed_summary_items": report["passed_summary_items"],
        "failed_items_count": report["failed_items_count"],
        "passed": report["passed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
