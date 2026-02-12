"""
M4 二次复核门禁：
检查 confirmed 证据是否具备“页码/段落级”二次复核字段。
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PAGE_LOCATOR_RE = re.compile(r"(第?\d+\s*页|p\.\s*\d+|§\s*\d+|第?\d+\s*段)")


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _record_label(record: Dict[str, Any]) -> str:
    return f"{record.get('group', '')}::{record.get('id', '')}"


def evaluate_rule_review_secondary_gate(evidence_path: str) -> Dict[str, Any]:
    with open(evidence_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if not isinstance(payload, dict):
        raise ValueError("evidence root must be object")

    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("evidence.records must be list")

    invalid_rows: List[str] = []
    confirmed_count = 0
    secondary_ready_count = 0
    missing_secondary_fields: Dict[str, List[str]] = {}

    for idx, row in enumerate(records):
        if not isinstance(row, dict):
            invalid_rows.append(f"records[{idx}]: row must be object")
            continue

        group = row.get("group")
        rule_id = row.get("id")
        if not (_non_empty_str(group) and _non_empty_str(rule_id)):
            invalid_rows.append(f"records[{idx}]: group/id must be non-empty string")
            continue

        if row.get("evidence_status") != "confirmed":
            continue

        confirmed_count += 1
        label = _record_label(row)
        missing: List[str] = []

        locator = row.get("locator")
        if not _non_empty_str(locator) or PAGE_LOCATOR_RE.search(str(locator)) is None:
            missing.append("page_or_paragraph_locator")

        second_reviewer = row.get("second_reviewer")
        if not _non_empty_str(second_reviewer):
            missing.append("second_reviewer")

        second_reviewed_at = row.get("second_reviewed_at")
        if not (_non_empty_str(second_reviewed_at) and DATE_RE.match(str(second_reviewed_at))):
            missing.append("second_reviewed_at")

        if missing:
            missing_secondary_fields[label] = missing
        else:
            secondary_ready_count += 1

    ready_for_full_secondary_review = (
        confirmed_count > 0 and secondary_ready_count == confirmed_count
    )

    return {
        "total_records": len(records),
        "total_confirmed_records": confirmed_count,
        "secondary_ready_records": secondary_ready_count,
        "missing_secondary_fields": missing_secondary_fields,
        "ready_for_full_secondary_review": ready_for_full_secondary_review,
        "invalid_rows": sorted(set(invalid_rows)),
        # passed 表示校验器运行成功且输入结构有效，不代表已经满足二次复核条件
        "passed": len(invalid_rows) == 0,
    }
