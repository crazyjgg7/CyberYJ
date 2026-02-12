"""
高频输出字段与权威来源证据的一对一检查（M4-P2）
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Set


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


def _get_source_ref_set(item: Dict[str, Any]) -> Set[str]:
    source_ref = item.get("source_ref")
    if isinstance(source_ref, str):
        return {source_ref}
    if isinstance(source_ref, list):
        return {x for x in source_ref if isinstance(x, str)}
    return set()


def evaluate_source_evidence(mapping_path: str, targets_path: str) -> Dict[str, Any]:
    mapping = _load_json(mapping_path)
    targets = _load_json(targets_path)

    items = mapping.get("items", [])
    target_items = targets.get("targets", [])

    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")
    if not isinstance(target_items, list):
        raise ValueError("targets.targets must be list")

    failed_target_ids: List[str] = []
    missing_mapping_target_ids: List[str] = []

    for target in target_items:
        if not isinstance(target, dict):
            continue
        target_id = target.get("id")
        match_rule = target.get("match", {})
        required_source_ids = target.get("required_source_ids", [])

        if not isinstance(target_id, str):
            continue
        if not isinstance(match_rule, dict):
            failed_target_ids.append(target_id)
            continue
        if not isinstance(required_source_ids, list) or not required_source_ids:
            failed_target_ids.append(target_id)
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

        required_set = {sid for sid in required_source_ids if isinstance(sid, str)}
        target_passed = False
        for item in matched_items:
            refs = _get_source_ref_set(item)
            if required_set.issubset(refs):
                target_passed = True
                break

        if not target_passed:
            failed_target_ids.append(target_id)

    total_targets = len([t for t in target_items if isinstance(t, dict) and isinstance(t.get("id"), str)])
    passed_targets = total_targets - len(set(failed_target_ids + missing_mapping_target_ids))

    return {
        "total_targets": total_targets,
        "passed_targets": passed_targets,
        "failed_target_ids": sorted(set(failed_target_ids)),
        "missing_mapping_target_ids": sorted(set(missing_mapping_target_ids)),
        "passed": len(failed_target_ids) == 0 and len(missing_mapping_target_ids) == 0,
    }
