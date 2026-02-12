#!/usr/bin/env python3
"""
生成 M4 字段清单与映射缺口报告
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.m4_mapping_gap import (
    build_m4_field_inventory,
    evaluate_m4_mapping_gap,
)


def main() -> int:
    inventory = build_m4_field_inventory(str(ROOT / "data"))
    gap_report = evaluate_m4_mapping_gap(
        inventory=inventory,
        mapping_path=str(ROOT / "data" / "mappings" / "authoritative_text_map.json"),
    )

    review_dir = ROOT / "data" / "review"
    review_dir.mkdir(parents=True, exist_ok=True)

    inventory_path = review_dir / "m4_field_inventory.json"
    gap_path = review_dir / "m4_mapping_gap_report.json"

    inventory_path.write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    gap_path.write_text(
        json.dumps(gap_report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    output = {
        "inventory_output": str(inventory_path),
        "gap_output": str(gap_path),
        "total_fields": gap_report["total_fields"],
        "mapped_fields": gap_report["mapped_fields"],
        "unmapped_fields_count": gap_report["unmapped_fields_count"],
        "coverage_ratio": gap_report["coverage_ratio"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
