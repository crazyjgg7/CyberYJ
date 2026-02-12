"""
M4-P3 规则证据门禁校验（matrix status -> evidence completeness）
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple


RuleKey = Tuple[str, str]


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _key_label(key: RuleKey) -> str:
    return f"{key[0]}::{key[1]}"


def _build_matrix_index(matrix: Dict[str, Any]) -> Tuple[Dict[RuleKey, Dict[str, Any]], List[str]]:
    groups = matrix.get("groups")
    if not isinstance(groups, dict):
        raise ValueError("matrix.groups must be object")

    index: Dict[RuleKey, Dict[str, Any]] = {}
    invalid_rows: List[str] = []

    for group_name, rows in groups.items():
        if not isinstance(rows, list):
            invalid_rows.append(f"{group_name}: rows must be list")
            continue
        for idx, row in enumerate(rows):
            if not isinstance(row, dict):
                invalid_rows.append(f"{group_name}[{idx}]: row must be object")
                continue
            rule_id = row.get("id")
            status = row.get("status")
            source_target = row.get("source_target")
            if not _non_empty_str(rule_id):
                invalid_rows.append(f"{group_name}[{idx}]: id must be non-empty string")
                continue
            if status not in {"pending", "verified", "blocked"}:
                invalid_rows.append(f"{group_name}[{idx}]: invalid status={status}")
                continue
            if not _non_empty_str(source_target):
                invalid_rows.append(f"{group_name}[{idx}]: source_target must be non-empty string")
                continue
            key = (group_name, rule_id)
            index[key] = row
    return index, sorted(set(invalid_rows))


def _build_evidence_index(
    evidence: Dict[str, Any]
) -> Tuple[Dict[RuleKey, Dict[str, Any]], List[str], List[str]]:
    records = evidence.get("records")
    if not isinstance(records, list):
        raise ValueError("evidence.records must be list")

    index: Dict[RuleKey, Dict[str, Any]] = {}
    duplicate_records: List[str] = []
    invalid_records: List[str] = []

    for idx, row in enumerate(records):
        if not isinstance(row, dict):
            invalid_records.append(f"records[{idx}]: row must be object")
            continue
        group = row.get("group")
        rule_id = row.get("id")
        if not _non_empty_str(group) or not _non_empty_str(rule_id):
            invalid_records.append(f"records[{idx}]: group/id must be non-empty string")
            continue
        key = (group, rule_id)
        if key in index:
            duplicate_records.append(_key_label(key))
            continue
        index[key] = row

    return index, sorted(set(duplicate_records)), sorted(set(invalid_records))


def _validate_verified(matrix_row: Dict[str, Any], evidence_row: Dict[str, Any]) -> Optional[str]:
    required_fields = ("source_id", "locator", "summary", "reviewed_by", "reviewed_at")
    if evidence_row.get("evidence_status") != "confirmed":
        return "evidence_status must be confirmed for verified rule"

    for field in required_fields:
        if not _non_empty_str(evidence_row.get(field)):
            return f"{field} is required for verified rule"

    if evidence_row.get("source_id") != matrix_row.get("source_target"):
        return "source_id must match matrix source_target for verified rule"

    reviewed_at = evidence_row.get("reviewed_at")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", reviewed_at):
        return "reviewed_at must be YYYY-MM-DD for verified rule"

    return None


def _validate_blocked(_matrix_row: Dict[str, Any], evidence_row: Dict[str, Any]) -> Optional[str]:
    if evidence_row.get("evidence_status") not in {"missing_text", "conflict", "unavailable"}:
        return "evidence_status must be missing_text/conflict/unavailable for blocked rule"
    if not _non_empty_str(evidence_row.get("notes")):
        return "notes is required for blocked rule"
    return None


def _validate_pending(_matrix_row: Dict[str, Any], evidence_row: Dict[str, Any]) -> Optional[str]:
    if evidence_row.get("evidence_status") not in {"pending", "missing_text"}:
        return "evidence_status must be pending/missing_text for pending rule"
    return None


def evaluate_rule_review_evidence(matrix_path: str, evidence_path: str) -> Dict[str, Any]:
    matrix = _load_json(matrix_path)
    evidence = _load_json(evidence_path)

    if not isinstance(matrix, dict):
        raise ValueError("matrix root must be object")
    if not isinstance(evidence, dict):
        raise ValueError("evidence root must be object")

    matrix_index, invalid_matrix_rows = _build_matrix_index(matrix)
    evidence_index, duplicate_records, invalid_record_rows = _build_evidence_index(evidence)

    missing_keys = sorted(set(matrix_index.keys()) - set(evidence_index.keys()))
    extra_keys = sorted(set(evidence_index.keys()) - set(matrix_index.keys()))

    source_target_mismatches: List[str] = []
    invalid_verified_records: List[str] = []
    invalid_blocked_records: List[str] = []
    invalid_pending_records: List[str] = []

    for key in sorted(set(matrix_index.keys()) & set(evidence_index.keys())):
        matrix_row = matrix_index[key]
        evidence_row = evidence_index[key]

        matrix_source = matrix_row.get("source_target")
        evidence_source = evidence_row.get("source_target")
        if matrix_source != evidence_source:
            source_target_mismatches.append(
                f"{_key_label(key)}: matrix={matrix_source}, evidence={evidence_source}"
            )

        status = matrix_row.get("status")
        if status == "verified":
            err = _validate_verified(matrix_row, evidence_row)
            if err:
                invalid_verified_records.append(f"{_key_label(key)}: {err}")
        elif status == "blocked":
            err = _validate_blocked(matrix_row, evidence_row)
            if err:
                invalid_blocked_records.append(f"{_key_label(key)}: {err}")
        elif status == "pending":
            err = _validate_pending(matrix_row, evidence_row)
            if err:
                invalid_pending_records.append(f"{_key_label(key)}: {err}")

    missing_records = [_key_label(x) for x in missing_keys]
    extra_records = [_key_label(x) for x in extra_keys]

    return {
        "total_rules": len(matrix_index),
        "total_records": len(evidence_index),
        "missing_records": missing_records,
        "extra_records": extra_records,
        "duplicate_records": duplicate_records,
        "invalid_matrix_rows": invalid_matrix_rows,
        "invalid_record_rows": invalid_record_rows,
        "source_target_mismatches": sorted(set(source_target_mismatches)),
        "invalid_verified_records": sorted(set(invalid_verified_records)),
        "invalid_blocked_records": sorted(set(invalid_blocked_records)),
        "invalid_pending_records": sorted(set(invalid_pending_records)),
        "passed": (
            len(missing_records) == 0
            and len(extra_records) == 0
            and len(duplicate_records) == 0
            and len(invalid_matrix_rows) == 0
            and len(invalid_record_rows) == 0
            and len(source_target_mismatches) == 0
            and len(invalid_verified_records) == 0
            and len(invalid_blocked_records) == 0
            and len(invalid_pending_records) == 0
        ),
    }
