#!/usr/bin/env python3
"""
导出 convention 缺口报告到 data/review。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.authoritative_convention_gap import (
    evaluate_authoritative_convention_gap,
)


def main() -> int:
    report = evaluate_authoritative_convention_gap(
        mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
        convention_only_threshold=18,
        allowlist_path=str(ROOT / "data" / "core" / "convention_allowlist.json"),
    )

    out = ROOT / "data" / "review" / "m4_convention_gap_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "output": str(out),
        "total_summary_items": report["total_summary_items"],
        "convention_only_items": report["convention_only_items"],
        "mixed_convention_items": report["mixed_convention_items"],
        "passed": report["passed"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
