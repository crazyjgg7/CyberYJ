"""
M4 convention 剩余缺口统计：
识别 authoritative_text_map 中仍仅依赖 convention 的字段，供后续替换批次使用。
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Set


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _module_from_field_path(field_path: str) -> str:
    if field_path.startswith("data.core."):
        return "core"
    if field_path.startswith("data.fengshui."):
        return "fengshui"
    if field_path.startswith("data.scenarios."):
        return "scenarios"
    if field_path.startswith("data.prompts."):
        return "prompts"
    if field_path.startswith("data.templates."):
        return "templates"
    return "other"


def _as_source_ref(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(x) for x in value if isinstance(x, str) and x.strip()]
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def _load_allowlist(allowlist_path: str | None) -> tuple[Set[str], List[str]]:
    if allowlist_path is None:
        return set(), []

    payload = _load_json(allowlist_path)
    if not isinstance(payload, dict):
        return set(), ["allowlist root must be object"]

    rows = payload.get("allowed_convention_only_field_paths")
    if not isinstance(rows, list):
        return set(), ["allowlist.allowed_convention_only_field_paths must be list"]

    invalid_rows: List[str] = []
    values: Set[str] = set()
    for i, row in enumerate(rows):
        if not isinstance(row, str) or not row.strip():
            invalid_rows.append(f"allowed_convention_only_field_paths[{i}] must be non-empty string")
            continue
        values.add(row)
    return values, sorted(set(invalid_rows))


def evaluate_authoritative_convention_gap(
    mapping_path: str,
    convention_only_threshold: int = 18,
    allowlist_path: str | None = None,
) -> Dict[str, Any]:
    mapping = _load_json(mapping_path)
    if not isinstance(mapping, dict):
        raise ValueError("mapping root must be object")

    items = mapping.get("items")
    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")

    total_summary_items = 0
    convention_only_items = 0
    mixed_convention_items = 0
    convention_only_field_paths: List[str] = []
    mixed_convention_field_paths: List[str] = []
    by_module: Dict[str, Dict[str, int]] = {}
    invalid_items: List[str] = []

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            invalid_items.append(f"items[{i}]: item must be object")
            continue
        if item.get("license") != "summary_only":
            continue

        field_path = item.get("field_path")
        if not isinstance(field_path, str) or not field_path.strip():
            invalid_items.append(f"items[{i}]: field_path required for summary_only")
            continue

        refs = _as_source_ref(item.get("source_ref"))
        if not refs:
            invalid_items.append(f"items[{i}]: source_ref required for summary_only")
            continue

        total_summary_items += 1
        module = _module_from_field_path(field_path)
        by_module.setdefault(
            module,
            {
                "summary_items": 0,
                "convention_only_items": 0,
                "mixed_convention_items": 0,
            },
        )
        by_module[module]["summary_items"] += 1

        has_convention = "convention" in refs
        if has_convention and len(refs) == 1:
            convention_only_items += 1
            convention_only_field_paths.append(field_path)
            by_module[module]["convention_only_items"] += 1
        elif has_convention and len(refs) > 1:
            mixed_convention_items += 1
            mixed_convention_field_paths.append(field_path)
            by_module[module]["mixed_convention_items"] += 1

    allowlist, invalid_allowlist = _load_allowlist(allowlist_path)
    allowed_convention_only_fields = sorted(
        set(convention_only_field_paths) & set(allowlist)
    )
    unexpected_convention_only_fields = sorted(
        set(convention_only_field_paths) - set(allowlist)
    )

    convention_only_ratio = (
        round(convention_only_items / total_summary_items, 4) if total_summary_items else 0.0
    )

    passed = (
        len(invalid_items) == 0
        and len(invalid_allowlist) == 0
        and mixed_convention_items == 0
        and convention_only_items <= convention_only_threshold
        and len(unexpected_convention_only_fields) == 0
    )

    return {
        "total_summary_items": total_summary_items,
        "convention_only_items": convention_only_items,
        "mixed_convention_items": mixed_convention_items,
        "convention_only_ratio": convention_only_ratio,
        "convention_only_threshold": convention_only_threshold,
        "by_module": by_module,
        "convention_only_field_paths": sorted(set(convention_only_field_paths)),
        "allowed_convention_only_fields": allowed_convention_only_fields,
        "unexpected_convention_only_fields": unexpected_convention_only_fields,
        "mixed_convention_field_paths": sorted(set(mixed_convention_field_paths)),
        "invalid_items": sorted(set(invalid_items)),
        "allowlist_path": allowlist_path,
        "invalid_allowlist": invalid_allowlist,
        "passed": passed,
    }
