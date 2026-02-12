#!/usr/bin/env python3
"""
按批次生成最终权威替换执行清单（A/B/C1/C2/C3）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.utils.rule_review_final_authority import (
    evaluate_rule_review_final_authority,
)


def _pick(items: List[Dict[str, Any]], group: str) -> List[Dict[str, Any]]:
    return [item for item in items if item.get("group") == group]


def _pick_luopan_by_ids(items: List[Dict[str, Any]], ids: List[str]) -> List[Dict[str, Any]]:
    idset = set(ids)
    return [
        item
        for item in items
        if item.get("group") == "luopan_24_mountains" and item.get("id") in idset
    ]


def main() -> int:
    report = evaluate_rule_review_final_authority(
        str(ROOT / "data" / "review" / "rule_review_evidence.json")
    )
    pending = report["pending_replacements"]

    c1_ids = ["壬", "子", "癸", "丑", "艮", "寅", "甲", "卯"]
    c2_ids = ["乙", "辰", "巽", "巳", "丙", "午", "丁", "未"]
    c3_ids = ["坤", "申", "庚", "酉", "辛", "戌", "乾", "亥"]

    batches = [
        {"batch": "A", "scope": "flying_star_rules", "items": _pick(pending, "flying_star_rules")},
        {"batch": "B", "scope": "bazhai_rules", "items": _pick(pending, "bazhai_rules")},
        {"batch": "C1", "scope": "luopan_24_mountains", "items": _pick_luopan_by_ids(pending, c1_ids)},
        {"batch": "C2", "scope": "luopan_24_mountains", "items": _pick_luopan_by_ids(pending, c2_ids)},
        {"batch": "C3", "scope": "luopan_24_mountains", "items": _pick_luopan_by_ids(pending, c3_ids)},
    ]

    payload = {
        "version": "1.0.0",
        "generated_at": "2026-02-12",
        "source_report": "data/review/rule_review_final_replacement_report.json",
        "total_pending_items": len(pending),
        "batches": [
            {
                "batch": item["batch"],
                "scope": item["scope"],
                "item_count": len(item["items"]),
                "status": "done" if len(item["items"]) == 0 else "pending",
                "items": item["items"],
            }
            for item in batches
        ],
    }

    output_path = ROOT / "data" / "review" / "rule_review_final_replacement_batches.json"
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = {
        "output": str(output_path),
        "total_pending_items": payload["total_pending_items"],
        "batch_counts": {entry["batch"]: entry["item_count"] for entry in payload["batches"]},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
