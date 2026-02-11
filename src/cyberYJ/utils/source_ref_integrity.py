"""
data 目录 source_ref 一致性校验（M4-P2）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _collect_source_refs(node: Any, path: str, out: List[Tuple[str, Any]]) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            next_path = f"{path}.{key}" if path else key
            if key == "source_ref":
                out.append((next_path, value))
            _collect_source_refs(value, next_path, out)
        return

    if isinstance(node, list):
        for idx, item in enumerate(node):
            next_path = f"{path}[{idx}]"
            _collect_source_refs(item, next_path, out)


def evaluate_source_ref_integrity(data_root: str, sources_path: str) -> Dict[str, Any]:
    data_dir = Path(data_root)
    sources_file = Path(sources_path)

    sources = _load_json(sources_file)
    if not isinstance(sources, list):
        raise ValueError("sources.json root must be list")

    known_source_ids: Set[str] = {
        row.get("source_id")
        for row in sources
        if isinstance(row, dict) and isinstance(row.get("source_id"), str)
    }

    unknown_source_refs: List[str] = []
    invalid_source_ref_entries: List[str] = []
    source_ref_count = 0
    scanned_files = 0

    for file_path in sorted(data_dir.rglob("*.json")):
        if file_path.resolve() == sources_file.resolve():
            continue
        if "__pycache__" in file_path.parts:
            continue

        scanned_files += 1
        payload = _load_json(file_path)
        refs: List[Tuple[str, Any]] = []
        _collect_source_refs(payload, "", refs)

        for json_path, value in refs:
            source_ref_count += 1
            if isinstance(value, str):
                values = [value]
            elif isinstance(value, list) and all(isinstance(x, str) for x in value):
                values = value
                if not values:
                    invalid_source_ref_entries.append(f"{file_path}:{json_path}: empty list")
                    continue
            else:
                invalid_source_ref_entries.append(
                    f"{file_path}:{json_path}: invalid type={type(value).__name__}"
                )
                continue

            for sid in values:
                if sid not in known_source_ids:
                    unknown_source_refs.append(f"{file_path}:{json_path}: {sid}")

    # 去重，保证报告稳定
    unknown_source_refs = sorted(set(unknown_source_refs))
    invalid_source_ref_entries = sorted(set(invalid_source_ref_entries))

    return {
        "scanned_files": scanned_files,
        "source_ref_count": source_ref_count,
        "unknown_source_refs": unknown_source_refs,
        "invalid_source_ref_entries": invalid_source_ref_entries,
        "passed": len(unknown_source_refs) == 0 and len(invalid_source_ref_entries) == 0,
    }
