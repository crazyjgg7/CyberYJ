"""
权威映射覆盖率统计
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} root must be object")
    return data


def _match_field_path(field_path: str, match_rule: Dict[str, Any]) -> bool:
    prefix = match_rule.get("prefix")
    if isinstance(prefix, str) and prefix:
        return field_path.startswith(prefix)

    pattern = match_rule.get("regex")
    if isinstance(pattern, str) and pattern:
        return re.search(pattern, field_path) is not None

    return False


def evaluate_authoritative_coverage(mapping_path: str, targets_path: str) -> Dict[str, Any]:
    mapping = _load_json(mapping_path)
    targets = _load_json(targets_path)

    items = mapping.get("items", [])
    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")

    target_items = targets.get("targets", [])
    if not isinstance(target_items, list):
        raise ValueError("targets.targets must be list")

    threshold = targets.get("threshold", 0.8)
    if not isinstance(threshold, (float, int)):
        raise ValueError("targets.threshold must be number")
    threshold = float(threshold)

    field_paths = [
        item.get("field_path")
        for item in items
        if isinstance(item, dict) and isinstance(item.get("field_path"), str)
    ]

    covered_target_ids: List[str] = []
    uncovered_target_ids: List[str] = []

    for target in target_items:
        if not isinstance(target, dict):
            continue
        target_id = target.get("id")
        match_rule = target.get("match", {})
        if not isinstance(target_id, str) or not isinstance(match_rule, dict):
            continue

        covered = any(_match_field_path(path, match_rule) for path in field_paths)
        if covered:
            covered_target_ids.append(target_id)
        else:
            uncovered_target_ids.append(target_id)

    total = len(covered_target_ids) + len(uncovered_target_ids)
    ratio = (len(covered_target_ids) / total) if total else 0.0

    return {
        "total_targets": total,
        "covered_targets": len(covered_target_ids),
        "coverage_ratio": round(ratio, 4),
        "threshold": threshold,
        "passed": ratio >= threshold,
        "covered_target_ids": covered_target_ids,
        "uncovered_target_ids": uncovered_target_ids,
    }
