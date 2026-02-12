"""
M4 本地权威知识库生成与校验。

将 authoritative_text_map 中可合法落地的摘要条目（summary_only）
归档到 data/authoritative，形成可复核的本地知识库索引与条目清单。
"""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple


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


def _normalize_source_ref(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(x) for x in value if _non_empty_str(x)]
    if _non_empty_str(value):
        return [str(value)]
    return []


def _entry_id(field_path: str, content: str, idx: int) -> str:
    raw = f"{field_path}|{content}|{idx}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:16]


def build_authoritative_local_kb(mapping_path: str, sources_path: str) -> Dict[str, Any]:
    mapping = _load_json(mapping_path)
    if not isinstance(mapping, dict):
        raise ValueError("mapping root must be object")

    items = mapping.get("items")
    if not isinstance(items, list):
        raise ValueError("mapping.items must be list")

    sources_index, invalid_sources = _load_sources_index(sources_path)
    entries: List[Dict[str, Any]] = []
    invalid_items: List[str] = []
    unknown_source_refs: List[str] = []
    source_stats: Dict[str, int] = {}

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            invalid_items.append(f"items[{i}]: item must be object")
            continue

        if item.get("license") != "summary_only":
            continue

        field_path = item.get("field_path")
        content = item.get("content")
        if not (_non_empty_str(field_path) and _non_empty_str(content)):
            invalid_items.append(f"items[{i}]: field_path/content required for summary_only")
            continue

        source_ref = _normalize_source_ref(item.get("source_ref"))
        if not source_ref:
            invalid_items.append(f"items[{i}]: source_ref required for summary_only")
            continue

        locator = item.get("locator")
        if not _non_empty_str(locator):
            invalid_items.append(f"items[{i}]: locator required for summary_only")
            continue

        details: List[Dict[str, Any]] = []
        for source_id in source_ref:
            if source_id not in sources_index:
                unknown_source_refs.append(source_id)
            else:
                src = sources_index[source_id]
                details.append(
                    {
                        "source_id": source_id,
                        "title": src.get("title"),
                        "edition": src.get("edition"),
                        "url_or_archive": src.get("url_or_archive"),
                    }
                )
            source_stats[source_id] = source_stats.get(source_id, 0) + 1

        entry = {
            "entry_id": _entry_id(str(field_path), str(content), i),
            "field_path": str(field_path),
            "text_kind": item.get("text_kind"),
            "license": item.get("license"),
            "content": str(content),
            "locator": str(locator),
            "source_ref": source_ref,
            "primary_source": source_ref[0],
            "source_details": details,
        }
        entries.append(entry)

    return {
        "version": "1.0.0",
        "generated_at": str(date.today()),
        "total_entries": len(entries),
        "source_stats": dict(sorted(source_stats.items())),
        "entries": entries,
        "invalid_sources": invalid_sources,
        "invalid_items": sorted(set(invalid_items)),
        "unknown_source_refs": sorted(set(unknown_source_refs)),
        "passed": len(invalid_sources) == 0 and len(invalid_items) == 0,
    }


def write_authoritative_local_kb(mapping_path: str, sources_path: str, output_dir: str) -> Dict[str, Any]:
    report = build_authoritative_local_kb(mapping_path=mapping_path, sources_path=sources_path)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    index_path = out_dir / "index.json"
    entries_path = out_dir / "entries.jsonl"

    index_payload = {
        "version": report["version"],
        "generated_at": report["generated_at"],
        "total_entries": report["total_entries"],
        "source_stats": report["source_stats"],
        "unknown_source_refs": report["unknown_source_refs"],
        "invalid_sources": report["invalid_sources"],
        "invalid_items": report["invalid_items"],
    }
    index_path.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [json.dumps(row, ensure_ascii=False) for row in report["entries"]]
    entries_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    return {
        "index_path": str(index_path),
        "entries_path": str(entries_path),
        "total_entries": report["total_entries"],
        "source_stats": report["source_stats"],
        "unknown_source_refs": report["unknown_source_refs"],
        "passed": report["passed"],
    }


def evaluate_authoritative_local_kb(index_path: str, entries_path: str, sources_path: str) -> Dict[str, Any]:
    index = _load_json(index_path)
    if not isinstance(index, dict):
        raise ValueError("index root must be object")

    sources_index, invalid_sources = _load_sources_index(sources_path)

    entries: List[Dict[str, Any]] = []
    invalid_entries: List[str] = []
    unknown_source_refs: List[str] = []
    source_stats: Dict[str, int] = {}

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
            required = ("entry_id", "field_path", "content", "license", "source_ref", "locator")
            for field in required:
                if field not in row:
                    invalid_entries.append(f"entries[{i}]: missing {field}")
            if row.get("license") != "summary_only":
                invalid_entries.append(f"entries[{i}]: license must be summary_only")
            if not _non_empty_str(row.get("content")):
                invalid_entries.append(f"entries[{i}]: empty content")
            if not _non_empty_str(row.get("locator")):
                invalid_entries.append(f"entries[{i}]: empty locator")

            refs = _normalize_source_ref(row.get("source_ref"))
            if not refs:
                invalid_entries.append(f"entries[{i}]: source_ref required")
            for source_id in refs:
                source_stats[source_id] = source_stats.get(source_id, 0) + 1
                if source_id not in sources_index:
                    unknown_source_refs.append(source_id)

            entries.append(row)

    total_entries = len(entries)
    expected_total = index.get("total_entries")
    count_mismatch = not isinstance(expected_total, int) or expected_total != total_entries

    index_source_stats = index.get("source_stats")
    if not isinstance(index_source_stats, dict):
        source_count_mismatches = ["index.source_stats must be object"]
    else:
        source_count_mismatches = []
        keyset = sorted(set(index_source_stats.keys()) | set(source_stats.keys()))
        for key in keyset:
            left = int(index_source_stats.get(key, 0))
            right = int(source_stats.get(key, 0))
            if left != right:
                source_count_mismatches.append(f"{key}: index={left}, entries={right}")

    passed = (
        len(invalid_sources) == 0
        and len(invalid_entries) == 0
        and len(unknown_source_refs) == 0
        and not count_mismatch
        and len(source_count_mismatches) == 0
    )

    return {
        "total_entries": total_entries,
        "expected_total_entries": expected_total,
        "count_mismatch": count_mismatch,
        "source_stats": dict(sorted(source_stats.items())),
        "source_count_mismatches": sorted(set(source_count_mismatches)),
        "invalid_sources": invalid_sources,
        "invalid_entries": sorted(set(invalid_entries)),
        "unknown_source_refs": sorted(set(unknown_source_refs)),
        "passed": passed,
    }
