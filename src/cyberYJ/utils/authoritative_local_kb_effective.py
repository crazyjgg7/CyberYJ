"""
M4 本地权威知识库（展开版）：
将映射规则按字段清单展开为“有效字段级”知识库条目。
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from cyberYJ.utils.m4_mapping_gap import build_m4_field_inventory, normalize_mapping_field_path


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _load_sources_index(sources_path: str) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    payload = _load_json(sources_path)
    if not isinstance(payload, list):
        raise ValueError("sources root must be list")

    index: Dict[str, Dict[str, Any]] = {}
    invalid_rows: List[str] = []
    for i, row in enumerate(payload):
        if not isinstance(row, dict):
            invalid_rows.append(f"sources[{i}]: row must be object")
            continue
        source_id = row.get("source_id")
        if not _non_empty_str(source_id):
            invalid_rows.append(f"sources[{i}]: source_id must be non-empty string")
            continue
        index[str(source_id)] = row
    return index, sorted(set(invalid_rows))


def _as_source_ref(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(x) for x in value if _non_empty_str(x)]
    if _non_empty_str(value):
        return [str(value)]
    return []


def _load_allowlist(allowlist_path: Optional[str]) -> Tuple[Set[str], List[str]]:
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


def _is_under_allowlist(field_path: str, allowlist_paths: Set[str]) -> bool:
    for allowed in allowlist_paths:
        if field_path == allowed:
            return True
        if field_path.startswith(f"{allowed}."):
            return True
        if field_path.startswith(f"{allowed}[*]"):
            return True
    return False


def _is_covered(field_path: str, mapping_path: str) -> bool:
    if field_path == mapping_path:
        return True
    if mapping_path.endswith("[*]") and field_path == mapping_path[:-3]:
        return True
    if field_path.startswith(f"{mapping_path}."):
        return True
    if field_path.startswith(f"{mapping_path}[*]"):
        return True
    return False


def _mapping_specificity(normalized_path: str) -> Tuple[int, int]:
    wildcard_count = normalized_path.count("[*]")
    return (len(normalized_path), -wildcard_count)


def _pick_best_mapping(field_path: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    covered = [row for row in candidates if _is_covered(field_path, row["normalized_field_path"])]
    if not covered:
        return None
    covered.sort(key=lambda row: _mapping_specificity(row["normalized_field_path"]), reverse=True)
    return covered[0]


def _entry_id(field_path: str, mapping_field_path: str) -> str:
    raw = f"{field_path}|{mapping_field_path}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def build_effective_authoritative_local_kb(
    data_root: str,
    mapping_path: str,
    sources_path: str,
    allowlist_path: Optional[str] = None,
) -> Dict[str, Any]:
    inventory = build_m4_field_inventory(data_root)
    field_items = inventory.get("fields", [])
    if not isinstance(field_items, list):
        raise ValueError("inventory.fields must be list")

    mapping = _load_json(mapping_path)
    if not isinstance(mapping, dict):
        raise ValueError("mapping root must be object")
    items = mapping.get("items")
    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")

    sources_index, invalid_sources = _load_sources_index(sources_path)
    allowlist_paths, invalid_allowlist = _load_allowlist(allowlist_path)

    mapping_rows: List[Dict[str, Any]] = []
    invalid_mapping_items: List[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            invalid_mapping_items.append(f"items[{i}]: item must be object")
            continue
        field_path = item.get("field_path")
        if not _non_empty_str(field_path):
            invalid_mapping_items.append(f"items[{i}]: field_path must be non-empty string")
            continue
        mapping_rows.append(
            {
                "raw": item,
                "field_path": str(field_path),
                "normalized_field_path": normalize_mapping_field_path(str(field_path)),
            }
        )

    effective_entries: List[Dict[str, Any]] = []
    unresolved_fields: List[str] = []
    unknown_source_refs: List[str] = []
    allowed_convention_fields: List[str] = []
    unexpected_convention_fields: List[str] = []
    source_stats: Dict[str, int] = {}
    module_stats: Dict[str, Dict[str, int]] = {}

    for row in field_items:
        if not isinstance(row, dict):
            continue
        field_path = row.get("field_path")
        module = row.get("module", "unknown")
        value_type = row.get("value_type", "unknown")
        if not _non_empty_str(field_path):
            continue

        module_name = str(module)
        module_stats.setdefault(
            module_name,
            {"total_fields": 0, "resolved_fields": 0, "unresolved_fields": 0},
        )
        module_stats[module_name]["total_fields"] += 1

        best = _pick_best_mapping(str(field_path), mapping_rows)
        if best is None:
            unresolved_fields.append(str(field_path))
            module_stats[module_name]["unresolved_fields"] += 1
            continue

        item = best["raw"]
        refs = _as_source_ref(item.get("source_ref"))
        for source_id in refs:
            source_stats[source_id] = source_stats.get(source_id, 0) + 1
            if source_id not in sources_index:
                unknown_source_refs.append(source_id)

        effective_entry = {
            "entry_id": _entry_id(str(field_path), best["field_path"]),
            "field_path": str(field_path),
            "module": module_name,
            "value_type": value_type,
            "mapping_field_path": best["field_path"],
            "normalized_mapping_field_path": best["normalized_field_path"],
            "text_kind": item.get("text_kind"),
            "license": item.get("license"),
            "content": item.get("content"),
            "locator": item.get("locator"),
            "source_ref": refs,
            "primary_source": refs[0] if refs else None,
        }
        effective_entries.append(effective_entry)
        module_stats[module_name]["resolved_fields"] += 1

        if "convention" in refs:
            if len(refs) == 1 and _is_under_allowlist(str(field_path), allowlist_paths):
                allowed_convention_fields.append(str(field_path))
            else:
                unexpected_convention_fields.append(str(field_path))

    total_fields = len([x for x in field_items if isinstance(x, dict) and _non_empty_str(x.get("field_path"))])
    unresolved_fields_count = len(unresolved_fields)
    resolved_fields_count = len(effective_entries)

    return {
        "version": "1.0.0",
        "generated_at": str(date.today()),
        "total_fields": total_fields,
        "resolved_fields_count": resolved_fields_count,
        "unresolved_fields_count": unresolved_fields_count,
        "source_stats": dict(sorted(source_stats.items())),
        "module_stats": module_stats,
        "effective_entries": effective_entries,
        "unresolved_fields": sorted(set(unresolved_fields)),
        "unknown_source_refs": sorted(set(unknown_source_refs)),
        "invalid_sources": invalid_sources,
        "invalid_mapping_items": sorted(set(invalid_mapping_items)),
        "passed": (
            len(invalid_sources) == 0
            and len(invalid_mapping_items) == 0
            and unresolved_fields_count == 0
            and len(unknown_source_refs) == 0
            and len(invalid_allowlist) == 0
            and len(unexpected_convention_fields) == 0
        ),
        "allowlist_path": allowlist_path,
        "invalid_allowlist": invalid_allowlist,
        "allowed_convention_fields_count": len(allowed_convention_fields),
        "unexpected_convention_fields_count": len(unexpected_convention_fields),
        "allowed_convention_fields": sorted(set(allowed_convention_fields)),
        "unexpected_convention_fields": sorted(set(unexpected_convention_fields)),
    }


def write_effective_authoritative_local_kb(
    data_root: str,
    mapping_path: str,
    sources_path: str,
    output_dir: str,
    allowlist_path: Optional[str] = None,
) -> Dict[str, Any]:
    report = build_effective_authoritative_local_kb(
        data_root=data_root,
        mapping_path=mapping_path,
        sources_path=sources_path,
        allowlist_path=allowlist_path,
    )

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "effective_index.json"
    entries_path = out_dir / "effective_entries.jsonl"

    index_payload = {
        "version": report["version"],
        "generated_at": report["generated_at"],
        "total_fields": report["total_fields"],
        "resolved_fields_count": report["resolved_fields_count"],
        "unresolved_fields_count": report["unresolved_fields_count"],
        "source_stats": report["source_stats"],
        "module_stats": report["module_stats"],
        "unresolved_fields": report["unresolved_fields"],
        "unknown_source_refs": report["unknown_source_refs"],
        "invalid_sources": report["invalid_sources"],
        "invalid_mapping_items": report["invalid_mapping_items"],
        "allowlist_path": report["allowlist_path"],
        "invalid_allowlist": report["invalid_allowlist"],
        "allowed_convention_fields_count": report["allowed_convention_fields_count"],
        "unexpected_convention_fields_count": report["unexpected_convention_fields_count"],
        "allowed_convention_fields": report["allowed_convention_fields"],
        "unexpected_convention_fields": report["unexpected_convention_fields"],
    }
    index_path.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [json.dumps(row, ensure_ascii=False) for row in report["effective_entries"]]
    entries_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    return {
        "index_path": str(index_path),
        "entries_path": str(entries_path),
        "total_fields": report["total_fields"],
        "resolved_fields_count": report["resolved_fields_count"],
        "unresolved_fields_count": report["unresolved_fields_count"],
        "unknown_source_refs": report["unknown_source_refs"],
        "allowed_convention_fields_count": report["allowed_convention_fields_count"],
        "unexpected_convention_fields_count": report["unexpected_convention_fields_count"],
        "passed": report["passed"],
    }


def evaluate_effective_authoritative_local_kb(
    index_path: str,
    entries_path: str,
    sources_path: str,
    allowlist_path: Optional[str] = None,
) -> Dict[str, Any]:
    index = _load_json(index_path)
    if not isinstance(index, dict):
        raise ValueError("index root must be object")

    sources_index, invalid_sources = _load_sources_index(sources_path)
    allowlist_paths, invalid_allowlist = _load_allowlist(allowlist_path)
    entries: List[Dict[str, Any]] = []
    invalid_entries: List[str] = []
    unknown_source_refs: List[str] = []
    source_stats: Dict[str, int] = {}
    allowed_convention_fields: List[str] = []
    unexpected_convention_fields: List[str] = []

    with open(entries_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            raw = line.strip()
            if raw == "":
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                invalid_entries.append(f"entries[{i}]: invalid json")
                continue
            if not isinstance(row, dict):
                invalid_entries.append(f"entries[{i}]: row must be object")
                continue
            for field in ("entry_id", "field_path", "mapping_field_path", "source_ref"):
                if field not in row:
                    invalid_entries.append(f"entries[{i}]: missing {field}")

            refs = _as_source_ref(row.get("source_ref"))
            field_path = row.get("field_path")
            for source_id in refs:
                source_stats[source_id] = source_stats.get(source_id, 0) + 1
                if source_id not in sources_index:
                    unknown_source_refs.append(source_id)
            if isinstance(field_path, str) and "convention" in refs:
                if len(refs) == 1 and _is_under_allowlist(field_path, allowlist_paths):
                    allowed_convention_fields.append(field_path)
                else:
                    unexpected_convention_fields.append(field_path)
            entries.append(row)

    total_entries = len(entries)
    expected_total = index.get("resolved_fields_count")
    count_mismatch = not isinstance(expected_total, int) or expected_total != total_entries

    index_unknown = index.get("unknown_source_refs", [])
    if not isinstance(index_unknown, list):
        invalid_entries.append("index.unknown_source_refs must be list")
        index_unknown = []

    mismatch_unknown = sorted(set(unknown_source_refs) ^ set(x for x in index_unknown if isinstance(x, str)))

    expected_allowed = index.get("allowed_convention_fields_count")
    expected_unexpected = index.get("unexpected_convention_fields_count")
    convention_count_mismatch = []
    if not isinstance(expected_allowed, int):
        convention_count_mismatch.append("index.allowed_convention_fields_count must be int")
    elif expected_allowed != len(set(allowed_convention_fields)):
        convention_count_mismatch.append(
            f"allowed_convention_fields_count mismatch: index={expected_allowed}, entries={len(set(allowed_convention_fields))}"
        )
    if not isinstance(expected_unexpected, int):
        convention_count_mismatch.append("index.unexpected_convention_fields_count must be int")
    elif expected_unexpected != len(set(unexpected_convention_fields)):
        convention_count_mismatch.append(
            f"unexpected_convention_fields_count mismatch: index={expected_unexpected}, entries={len(set(unexpected_convention_fields))}"
        )

    passed = (
        len(invalid_sources) == 0
        and len(invalid_entries) == 0
        and len(unknown_source_refs) == 0
        and not count_mismatch
        and len(mismatch_unknown) == 0
        and len(invalid_allowlist) == 0
        and len(convention_count_mismatch) == 0
        and len(unexpected_convention_fields) == 0
    )

    return {
        "total_entries": total_entries,
        "expected_total_entries": expected_total,
        "count_mismatch": count_mismatch,
        "source_stats": dict(sorted(source_stats.items())),
        "invalid_sources": invalid_sources,
        "invalid_entries": sorted(set(invalid_entries)),
        "unknown_source_refs": sorted(set(unknown_source_refs)),
        "unknown_source_ref_mismatch": mismatch_unknown,
        "allowlist_path": allowlist_path,
        "invalid_allowlist": invalid_allowlist,
        "allowed_convention_fields_count": len(set(allowed_convention_fields)),
        "unexpected_convention_fields_count": len(set(unexpected_convention_fields)),
        "unexpected_convention_fields": sorted(set(unexpected_convention_fields)),
        "convention_count_mismatch": convention_count_mismatch,
        "unresolved_fields_count": index.get("unresolved_fields_count"),
        "passed": passed,
    }
