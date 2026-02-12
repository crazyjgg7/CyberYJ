"""
M4 字段清单导出与映射缺口分析
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any, Dict, Iterable, List, Set, Tuple


CORE_DATASETS = {"hexagrams", "solar_terms", "trigrams", "hexagram_keywords"}
DYNAMIC_KEY_PARENTS = {"hexagrams", "scenario_specific", "stars", "palace_map"}
LIST_ROOT_PREFIXES = (
    "data.core.hexagrams",
    "data.core.solar_terms",
    "data.core.trigrams",
    "data.fengshui.ba_zhai",
    "data.fengshui.flying_stars_periods",
    "data.fengshui.flying_stars_house",
    "data.fengshui.luopan",
)

_ID_FILTER = re.compile(r"\[\?\(@\.id==[^\]]+\)\]")
_QUOTED_INDEX = re.compile(r"\['[^']+'\]")
_SCENARIO_SUBSCENE = re.compile(r"(\.scenario_specific)\.[^.]+(\.)")
_DIGIT_SEGMENT = re.compile(r"\.(\d+)(?=\.|$)")
_SIMPLE_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _value_type(value: Any) -> str:
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if value is None:
        return "null"
    return "string"


def _join_path(base: str, key: str) -> str:
    if key == "[*]":
        return f"{base}[*]"
    return f"{base}.{key}"


def _is_dynamic_key(parent_key: str, key: str) -> bool:
    if key.isdigit():
        return True
    if parent_key in DYNAMIC_KEY_PARENTS:
        return True
    return _SIMPLE_KEY.match(key) is None


def _walk(
    value: Any,
    path: str,
    parent_key: str,
    fields: Dict[str, str],
    use_parent_dynamic: bool = True,
) -> None:
    if isinstance(value, dict):
        for key in sorted(value.keys(), key=str):
            if not isinstance(key, str):
                continue
            child = value[key]
            if use_parent_dynamic:
                dynamic = _is_dynamic_key(parent_key, key)
            else:
                dynamic = key.isdigit() or _SIMPLE_KEY.match(key) is None
            segment = "[*]" if dynamic else key
            child_path = _join_path(path, segment)
            fields[child_path] = _value_type(child)
            _walk(child, child_path, key, fields, True)
        return

    if isinstance(value, list):
        if not value:
            return
        list_item_path = f"{path}[*]"
        sample = next((item for item in value if item is not None), value[0])
        fields[list_item_path] = _value_type(sample)
        for item in value:
            if item is None:
                continue
            _walk(item, list_item_path, parent_key, fields, False)


def _iter_domain_json_files(data_root: Path) -> Iterable[Tuple[str, str, Path]]:
    for module in ("core", "scenarios", "fengshui"):
        module_dir = data_root / module
        if not module_dir.exists():
            continue
        for path in sorted(module_dir.glob("*.json")):
            dataset = path.stem
            if module == "core" and dataset not in CORE_DATASETS:
                continue
            yield module, dataset, path


def _module_from_field_path(field_path: str) -> str:
    parts = field_path.split(".")
    if len(parts) >= 2 and parts[0] == "data":
        return parts[1]
    return "unknown"


def build_m4_field_inventory(data_root: str) -> Dict[str, Any]:
    root = Path(data_root)
    if not root.exists():
        raise ValueError(f"data_root not found: {data_root}")

    fields: Dict[str, str] = {}
    scanned_files: List[str] = []
    project_base = root.parent

    for module, dataset, path in _iter_domain_json_files(root):
        try:
            scanned_files.append(str(path.relative_to(project_base)))
        except ValueError:
            scanned_files.append(str(path))
        data = _load_json(path)
        base_path = f"data.{module}.{dataset}"
        fields[base_path] = _value_type(data)
        _walk(data, base_path, dataset, fields)

    field_items = [
        {
            "field_path": field_path,
            "module": _module_from_field_path(field_path),
            "value_type": value_type,
        }
        for field_path, value_type in sorted(fields.items())
    ]

    module_stats: Dict[str, Dict[str, int]] = {}
    for item in field_items:
        module = item["module"]
        module_stats.setdefault(module, {"total_fields": 0})
        module_stats[module]["total_fields"] += 1

    try:
        data_root_display = str(root.relative_to(project_base))
    except ValueError:
        data_root_display = str(root)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "data_root": data_root_display,
        "scanned_files": scanned_files,
        "total_fields": len(field_items),
        "modules": module_stats,
        "fields": field_items,
    }


def normalize_mapping_field_path(field_path: str) -> str:
    normalized = field_path
    if normalized.startswith("hexagrams"):
        normalized = f"data.core.{normalized}"

    normalized = _ID_FILTER.sub("[*]", normalized)
    normalized = _QUOTED_INDEX.sub("[*]", normalized)
    normalized = _SCENARIO_SUBSCENE.sub(r"\1[*]\2", normalized)
    normalized = _DIGIT_SEGMENT.sub(".[*]", normalized)

    for prefix in LIST_ROOT_PREFIXES:
        if normalized == prefix:
            normalized = f"{prefix}[*]"
            break
        if normalized.startswith(f"{prefix}.") and not normalized.startswith(f"{prefix}[*]."):
            normalized = normalized.replace(f"{prefix}.", f"{prefix}[*].", 1)
            break

    return normalized


def _is_covered(field_path: str, mapping_paths: Set[str]) -> bool:
    for mapped in mapping_paths:
        if field_path == mapped:
            return True
        if field_path.startswith(f"{mapped}."):
            return True
        if field_path.startswith(f"{mapped}[*]"):
            return True
    return False


def evaluate_m4_mapping_gap(
    inventory: Dict[str, Any],
    mapping_path: str,
) -> Dict[str, Any]:
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    items = mapping.get("items", [])
    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")

    mapping_paths: Set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        field_path = item.get("field_path")
        if not isinstance(field_path, str):
            continue
        mapping_paths.add(normalize_mapping_field_path(field_path))

    field_items = inventory.get("fields", [])
    if not isinstance(field_items, list):
        raise ValueError("inventory.fields must be list")

    mapped_fields: List[str] = []
    unmapped_fields: List[str] = []
    module_buckets: Dict[str, Dict[str, Any]] = {}

    for item in field_items:
        if not isinstance(item, dict):
            continue
        field_path = item.get("field_path")
        module = item.get("module", "unknown")
        if not isinstance(field_path, str):
            continue

        module_stats = module_buckets.setdefault(
            module,
            {"total_fields": 0, "mapped_fields": 0, "unmapped_fields": []},
        )
        module_stats["total_fields"] += 1

        if _is_covered(field_path, mapping_paths):
            mapped_fields.append(field_path)
            module_stats["mapped_fields"] += 1
        else:
            unmapped_fields.append(field_path)
            module_stats["unmapped_fields"].append(field_path)

    total = len(mapped_fields) + len(unmapped_fields)
    ratio = (len(mapped_fields) / total) if total else 0.0

    for module, stats in module_buckets.items():
        total_fields = stats["total_fields"]
        mapped = stats["mapped_fields"]
        stats["coverage_ratio"] = round((mapped / total_fields) if total_fields else 0.0, 4)
        stats["unmapped_fields"] = sorted(set(stats["unmapped_fields"]))
        module_buckets[module] = stats

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_fields": total,
        "mapped_fields": len(mapped_fields),
        "unmapped_fields_count": len(unmapped_fields),
        "coverage_ratio": round(ratio, 4),
        "mapping_item_count": len(mapping_paths),
        "mapped_fields_list": sorted(set(mapped_fields)),
        "unmapped_fields": sorted(set(unmapped_fields)),
        "modules": module_buckets,
    }
