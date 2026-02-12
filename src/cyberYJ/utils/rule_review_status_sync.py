"""
M4-P3 将 evidence.confirmed 自动同步到 matrix.verified
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


RuleKey = Tuple[str, str]


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _key_label(group: str, rule_id: str) -> str:
    return f"{group}::{rule_id}"


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
            index[(group_name, rule_id)] = row

    return index, sorted(set(invalid_rows))


def _build_evidence_confirmed_index(evidence: Dict[str, Any]) -> Dict[RuleKey, Dict[str, Any]]:
    records = evidence.get("records")
    if not isinstance(records, list):
        raise ValueError("evidence.records must be list")

    out: Dict[RuleKey, Dict[str, Any]] = {}
    for row in records:
        if not isinstance(row, dict):
            continue
        if row.get("evidence_status") != "confirmed":
            continue
        group = row.get("group")
        rule_id = row.get("id")
        if not (_non_empty_str(group) and _non_empty_str(rule_id)):
            continue
        out[(group, rule_id)] = row
    return out


def _validate_confirmed_record(matrix_row: Dict[str, Any], evidence_row: Dict[str, Any]) -> Optional[str]:
    required_fields = ("source_id", "locator", "summary", "reviewed_by", "reviewed_at")
    for field in required_fields:
        if not _non_empty_str(evidence_row.get(field)):
            return f"{field} is required"

    source_id = evidence_row.get("source_id")
    if source_id != matrix_row.get("source_target"):
        return "source_id must match matrix.source_target"

    reviewed_at = evidence_row.get("reviewed_at")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", reviewed_at):
        return "reviewed_at must match YYYY-MM-DD"

    return None


def _append_auto_verified_note(existing_notes: str, source_id: str, reviewed_at: str) -> str:
    stamp = datetime.utcnow().strftime("%Y-%m-%d")
    marker = (
        f"AUTO-VERIFIED({stamp}): confirmed evidence "
        f"source_id={source_id}, reviewed_at={reviewed_at}"
    )
    if _non_empty_str(existing_notes):
        if marker in existing_notes:
            return existing_notes
        return f"{existing_notes} | {marker}"
    return marker


def sync_rule_review_matrix_from_evidence(
    matrix_path: str,
    evidence_path: str,
    dry_run: bool = True,
    output_matrix_path: Optional[str] = None,
) -> Dict[str, Any]:
    matrix = _load_json(matrix_path)
    evidence = _load_json(evidence_path)

    if not isinstance(matrix, dict):
        raise ValueError("matrix root must be object")
    if not isinstance(evidence, dict):
        raise ValueError("evidence root must be object")

    matrix_index, invalid_matrix_rows = _build_matrix_index(matrix)
    confirmed_index = _build_evidence_confirmed_index(evidence)

    confirmed_without_rule: List[str] = []
    skipped_not_blocked: List[str] = []
    invalid_confirmed_records: List[str] = []
    would_update: List[str] = []
    updated: List[str] = []

    for (group, rule_id), evidence_row in sorted(confirmed_index.items()):
        label = _key_label(group, rule_id)
        matrix_row = matrix_index.get((group, rule_id))
        if matrix_row is None:
            confirmed_without_rule.append(label)
            continue

        err = _validate_confirmed_record(matrix_row, evidence_row)
        if err:
            invalid_confirmed_records.append(f"{label}: {err}")
            continue

        status = matrix_row.get("status")
        if status != "blocked":
            skipped_not_blocked.append(label)
            continue

        would_update.append(label)
        if dry_run:
            continue

        matrix_row["status"] = "verified"
        matrix_row["notes"] = _append_auto_verified_note(
            existing_notes=matrix_row.get("notes", ""),
            source_id=str(evidence_row.get("source_id")),
            reviewed_at=str(evidence_row.get("reviewed_at")),
        )
        updated.append(label)

    if not dry_run:
        output_path = Path(output_matrix_path) if output_matrix_path else Path(matrix_path)
        output_path.write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return {
        "dry_run": dry_run,
        "applied": not dry_run,
        "matrix_path": output_matrix_path if (output_matrix_path and not dry_run) else matrix_path,
        "confirmed_records": len(confirmed_index),
        "would_update_count": len(would_update),
        "updated_count": len(updated),
        "would_update": would_update,
        "updated": updated,
        "confirmed_without_rule": sorted(set(confirmed_without_rule)),
        "skipped_not_blocked": sorted(set(skipped_not_blocked)),
        "invalid_matrix_rows": invalid_matrix_rows,
        "invalid_confirmed_records": sorted(set(invalid_confirmed_records)),
        "passed": (
            len(invalid_matrix_rows) == 0
            and len(invalid_confirmed_records) == 0
            and len(confirmed_without_rule) == 0
        ),
    }
