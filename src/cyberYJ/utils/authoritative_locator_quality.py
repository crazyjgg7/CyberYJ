"""
高频字段 locator 质量门禁（M4）
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

    regex = match_rule.get("regex")
    if isinstance(regex, str) and regex:
        return re.search(regex, field_path) is not None

    return False


def _has_locator(item: Dict[str, Any]) -> bool:
    locator = item.get("locator")
    return isinstance(locator, str) and locator.strip() != ""


def evaluate_authoritative_locator_quality(mapping_path: str, targets_path: str) -> Dict[str, Any]:
    mapping = _load_json(mapping_path)
    targets = _load_json(targets_path)

    items = mapping.get("items", [])
    target_items = targets.get("targets", [])

    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")
    if not isinstance(target_items, list):
        raise ValueError("targets.targets must be list")

    missing_mapping_target_ids: List[str] = []
    missing_locator_target_ids: List[str] = []

    for target in target_items:
        if not isinstance(target, dict):
            continue

        target_id = target.get("id")
        match_rule = target.get("match", {})

        if not isinstance(target_id, str) or not isinstance(match_rule, dict):
            continue

        matched_items: List[Dict[str, Any]] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            field_path = item.get("field_path")
            if not isinstance(field_path, str):
                continue
            if _match_field_path(field_path, match_rule):
                matched_items.append(item)

        if not matched_items:
            missing_mapping_target_ids.append(target_id)
            continue

        if not any(_has_locator(item) for item in matched_items):
            missing_locator_target_ids.append(target_id)

    total_targets = len([t for t in target_items if isinstance(t, dict) and isinstance(t.get("id"), str)])
    failed_target_ids = sorted(set(missing_mapping_target_ids + missing_locator_target_ids))
    passed_targets = total_targets - len(failed_target_ids)

    return {
        "total_targets": total_targets,
        "passed_targets": passed_targets,
        "missing_mapping_target_ids": sorted(set(missing_mapping_target_ids)),
        "missing_locator_target_ids": sorted(set(missing_locator_target_ids)),
        "passed": len(failed_target_ids) == 0,
    }
