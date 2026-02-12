"""
高频字段 locator 精度校验（M4）
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List


BOOK_PAGE_LOCATOR_RE = re.compile(r"(第\d+页|p\.?\s*\d+|§\s*\d+|第\d+段)")
ENTRY_LOCATOR_RE = re.compile(r"(第\d+卦|条目|节气|卦名|关键词|黄经)")

BOOK_SOURCES = {
    "cinii_dili_bianzheng_shu",
    "cinii_bazhai_mingjing",
    "qingnang_aoyu",
}
ENTRY_SOURCES = {
    "ctext_yijing",
    "ctext_shuogua",
    "cma_24_terms",
}


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


def _get_source_ref_set(item: Dict[str, Any]) -> set[str]:
    source_ref = item.get("source_ref")
    if isinstance(source_ref, str):
        return {source_ref}
    if isinstance(source_ref, list):
        return {x for x in source_ref if isinstance(x, str)}
    return set()


def _locator_is_precise(locator: str, required_source_ids: List[str]) -> bool:
    required_set = {x for x in required_source_ids if isinstance(x, str)}
    if required_set & BOOK_SOURCES:
        return BOOK_PAGE_LOCATOR_RE.search(locator) is not None
    if required_set & ENTRY_SOURCES:
        return ENTRY_LOCATOR_RE.search(locator) is not None
    # 其他来源当前不收紧精度规则
    return bool(locator.strip())


def evaluate_authoritative_locator_precision(mapping_path: str, targets_path: str) -> Dict[str, Any]:
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
    missing_precision_locator_target_ids: List[str] = []

    for target in target_items:
        if not isinstance(target, dict):
            continue
        target_id = target.get("id")
        match_rule = target.get("match", {})
        required_source_ids = target.get("required_source_ids", [])

        if not isinstance(target_id, str):
            continue
        if not isinstance(match_rule, dict) or not isinstance(required_source_ids, list) or not required_source_ids:
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
            if not required_set.issubset(refs):
                continue
            locator = item.get("locator")
            if not isinstance(locator, str) or not locator.strip():
                continue
            if _locator_is_precise(locator, required_source_ids):
                target_passed = True
                break

        if not target_passed:
            missing_precision_locator_target_ids.append(target_id)

    total_targets = len([t for t in target_items if isinstance(t, dict) and isinstance(t.get("id"), str)])
    all_failed = sorted(set(failed_target_ids + missing_mapping_target_ids + missing_precision_locator_target_ids))
    passed_targets = total_targets - len(all_failed)

    return {
        "total_targets": total_targets,
        "passed_targets": passed_targets,
        "failed_target_ids": sorted(set(failed_target_ids)),
        "missing_mapping_target_ids": sorted(set(missing_mapping_target_ids)),
        "missing_precision_locator_target_ids": sorted(set(missing_precision_locator_target_ids)),
        "passed": len(all_failed) == 0,
    }
