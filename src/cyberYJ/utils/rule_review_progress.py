"""
M4-P3 规则逐条核对进度统计
"""

from __future__ import annotations

import json
from typing import Any, Dict, List


def evaluate_rule_review_progress(matrix_path: str) -> Dict[str, Any]:
    with open(matrix_path, "r", encoding="utf-8") as f:
        matrix = json.load(f)

    if not isinstance(matrix, dict):
        raise ValueError("matrix root must be object")

    groups = matrix.get("groups")
    status_enum = matrix.get("status_enum", ["pending", "verified", "blocked"])
    if not isinstance(groups, dict):
        raise ValueError("matrix.groups must be object")
    if not isinstance(status_enum, list):
        raise ValueError("matrix.status_enum must be list")

    allowed_status = {s for s in status_enum if isinstance(s, str)}
    if not allowed_status:
        raise ValueError("status_enum must contain at least one status")

    total_items = 0
    verified_items = 0
    blocked_items = 0
    invalid_items: List[str] = []
    group_counts: Dict[str, Dict[str, int]] = {}

    for group_name, entries in groups.items():
        if not isinstance(entries, list):
            invalid_items.append(f"{group_name}: entries must be list")
            continue

        g_total = 0
        g_verified = 0
        g_blocked = 0

        for idx, row in enumerate(entries):
            g_total += 1
            total_items += 1
            if not isinstance(row, dict):
                invalid_items.append(f"{group_name}[{idx}]: row must be object")
                continue

            status = row.get("status")
            if status not in allowed_status:
                invalid_items.append(f"{group_name}[{idx}]: invalid status={status}")
                continue

            if status == "verified":
                verified_items += 1
                g_verified += 1
            if status == "blocked":
                blocked_items += 1
                g_blocked += 1

        group_counts[group_name] = {
            "total": g_total,
            "verified": g_verified,
            "blocked": g_blocked,
        }

    pending_items = total_items - verified_items - blocked_items
    ratio = (verified_items / total_items) if total_items else 0.0

    return {
        "total_items": total_items,
        "verified_items": verified_items,
        "blocked_items": blocked_items,
        "pending_items": pending_items,
        "completion_ratio": round(ratio, 4),
        "group_counts": group_counts,
        "invalid_items": sorted(set(invalid_items)),
        "passed": len(invalid_items) == 0,
    }
