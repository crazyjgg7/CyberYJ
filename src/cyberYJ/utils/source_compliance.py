"""
来源索引合规校验（M4-P2）
"""

from __future__ import annotations

import json
from typing import Any, Dict, List


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_source_compliance(sources_path: str, policy_path: str) -> Dict[str, Any]:
    sources = _load_json(sources_path)
    policy = _load_json(policy_path)

    if not isinstance(sources, list):
        raise ValueError("sources root must be list")
    if not isinstance(policy, dict):
        raise ValueError("policy root must be object")

    required_ids = policy.get("required_source_ids", [])
    required_fields = policy.get("required_fields", [])
    disallow_values = set(policy.get("disallow_values", []))
    require_http_url = bool(policy.get("require_http_url", False))

    if not isinstance(required_ids, list) or not isinstance(required_fields, list):
        raise ValueError("policy.required_source_ids/required_fields must be list")

    index: Dict[str, Dict[str, Any]] = {}
    for row in sources:
        if isinstance(row, dict) and isinstance(row.get("source_id"), str):
            index[row["source_id"]] = row

    present_required_ids: List[str] = []
    missing_required_ids: List[str] = []
    invalid_fields: List[str] = []

    for sid in required_ids:
        if sid not in index:
            missing_required_ids.append(sid)
            continue

        present_required_ids.append(sid)
        row = index[sid]

        for field in required_fields:
            value = row.get(field)
            if value is None:
                invalid_fields.append(f"{sid}.{field}: missing")
                continue
            if isinstance(value, str):
                val = value.strip()
                if val in disallow_values:
                    invalid_fields.append(f"{sid}.{field}: disallowed_value={val}")
                if field == "url_or_archive" and require_http_url:
                    if not (val.startswith("http://") or val.startswith("https://")):
                        invalid_fields.append(f"{sid}.{field}: invalid_url_scheme")
            else:
                invalid_fields.append(f"{sid}.{field}: non_string")

    return {
        "required_source_ids": required_ids,
        "present_required_ids": present_required_ids,
        "missing_required_ids": missing_required_ids,
        "invalid_fields": invalid_fields,
        "passed": len(missing_required_ids) == 0 and len(invalid_fields) == 0,
    }
