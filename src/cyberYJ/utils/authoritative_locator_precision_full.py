"""
M4 全量 summary 项 locator 精度检查。
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List


BOOK_SOURCES = {
    "cinii_dili_bianzheng_shu",
    "cinii_bazhai_mingjing",
    "qingnang_aoyu",
    "sanmin_bazhai_mingjing",
    "sanmin_dili_bianzheng_shu",
    "bookschina_bazhai_mingjing",
    "books_com_tw_dili_bianzheng_shu",
    "openlibrary_dili_bianzheng_shu",
}
ENTRY_SOURCES = {"ctext_yijing", "ctext_shuogua", "cma_24_terms"}

BOOK_LOCATOR_RE = re.compile(r"(第\s*\d+\s*页|p\.?\s*\d+|§\s*\d+|第\s*\d+\s*段)")
ENTRY_LOCATOR_RE = re.compile(r"(第\s*\d+\s*卦|说卦|节气|黄经|关键词|条目|章节|第\s*\d+\s*段)")


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, dict):
        raise ValueError("mapping root must be object")
    return payload


def _source_ref(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(x) for x in value if isinstance(x, str) and x.strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def _reason_for_locator(locator: str, refs: List[str]) -> str | None:
    if not locator.strip():
        return "locator_missing"

    ref_set = set(refs)
    if ref_set & BOOK_SOURCES:
        if BOOK_LOCATOR_RE.search(locator) is None:
            return "book_locator_not_precise"
        return None
    if ref_set & ENTRY_SOURCES:
        if ENTRY_LOCATOR_RE.search(locator) is None:
            return "entry_locator_not_precise"
        return None
    return None


def evaluate_authoritative_locator_precision_full(mapping_path: str) -> Dict[str, Any]:
    mapping = _load_json(mapping_path)
    items = mapping.get("items")
    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")

    total_summary_items = 0
    failed_items: List[str] = []
    failed_reasons: Dict[str, str] = {}
    invalid_items: List[str] = []

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            invalid_items.append(f"items[{i}]: item must be object")
            continue
        if item.get("license") != "summary_only":
            continue
        total_summary_items += 1

        field_path = item.get("field_path")
        if not isinstance(field_path, str) or not field_path.strip():
            invalid_items.append(f"items[{i}]: field_path required for summary_only")
            continue

        refs = _source_ref(item.get("source_ref"))
        if not refs:
            failed_items.append(field_path)
            failed_reasons[field_path] = "source_ref_missing"
            continue

        locator = item.get("locator")
        if not isinstance(locator, str):
            failed_items.append(field_path)
            failed_reasons[field_path] = "locator_missing"
            continue

        reason = _reason_for_locator(locator, refs)
        if reason is not None:
            failed_items.append(field_path)
            failed_reasons[field_path] = reason

    failed_items = sorted(set(failed_items))
    passed_summary_items = total_summary_items - len(failed_items)
    passed = len(failed_items) == 0 and len(invalid_items) == 0

    return {
        "total_summary_items": total_summary_items,
        "passed_summary_items": passed_summary_items,
        "failed_items_count": len(failed_items),
        "failed_field_paths": failed_items,
        "failed_reasons": failed_reasons,
        "invalid_items": sorted(set(invalid_items)),
        "passed": passed,
    }
