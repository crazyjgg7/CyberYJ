"""
M4 最终权威版替换进度评估：
用于识别 rule_review_evidence 中仍属于“过渡证据”的记录，并输出替换清单。
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List


PAGE_LOCATOR_RE = re.compile(r"(第?\d+\s*页|p\.\s*\d+|§\s*\d+|第?\d+\s*段)")
TRANSITION_MARKERS = ("过渡证据", "书目记录")
TRANSITION_NOTE_MARKERS = (
    "待后续权威文本页码替换后复核",
    "等待后续权威文本页码替换后复核",
)


def _non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _label(group: str, rule_id: str) -> str:
    return f"{group}::{rule_id}"


def _is_transition_edition(edition: str) -> bool:
    return any(marker in edition for marker in TRANSITION_MARKERS)


def _has_transition_note(notes: str) -> bool:
    return any(marker in notes for marker in TRANSITION_NOTE_MARKERS)


def evaluate_rule_review_final_authority(evidence_path: str) -> Dict[str, Any]:
    with open(evidence_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    if not isinstance(payload, dict):
        raise ValueError("evidence root must be object")

    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("evidence.records must be list")

    invalid_rows: List[str] = []
    transition_pending_records: List[str] = []
    missing_final_locator_records: List[str] = []
    pending_replacements: List[Dict[str, Any]] = []
    group_counts: Dict[str, Dict[str, int]] = {}

    total_confirmed_records = 0
    final_authority_ready_records = 0

    for idx, row in enumerate(records):
        if not isinstance(row, dict):
            invalid_rows.append(f"records[{idx}]: row must be object")
            continue

        group = row.get("group")
        rule_id = row.get("id")
        if not (_non_empty_str(group) and _non_empty_str(rule_id)):
            invalid_rows.append(f"records[{idx}]: group/id must be non-empty string")
            continue

        group_name = str(group)
        group_counts.setdefault(
            group_name,
            {
                "total": 0,
                "confirmed": 0,
                "transition_pending": 0,
                "final_ready": 0,
            },
        )
        group_counts[group_name]["total"] += 1

        if row.get("evidence_status") != "confirmed":
            continue

        total_confirmed_records += 1
        group_counts[group_name]["confirmed"] += 1

        edition = str(row.get("edition", "")).strip()
        notes = str(row.get("notes", "")).strip()
        locator = str(row.get("locator", "")).strip()

        label = _label(group_name, str(rule_id))
        reasons: List[str] = []

        if _is_transition_edition(edition) or _has_transition_note(notes):
            transition_pending_records.append(label)
            group_counts[group_name]["transition_pending"] += 1
            reasons.append("transition_source_not_replaced")

        if PAGE_LOCATOR_RE.search(locator) is None:
            missing_final_locator_records.append(label)
            reasons.append("final_page_locator_missing")

        if reasons:
            pending_replacements.append(
                {
                    "group": group_name,
                    "id": str(rule_id),
                    "label": label,
                    "source_id": row.get("source_id"),
                    "edition": edition,
                    "locator": locator,
                    "reasons": reasons,
                }
            )
        else:
            final_authority_ready_records += 1
            group_counts[group_name]["final_ready"] += 1

    ready_for_final_authority_closeout = (
        total_confirmed_records > 0
        and final_authority_ready_records == total_confirmed_records
        and len(transition_pending_records) == 0
        and len(missing_final_locator_records) == 0
    )

    return {
        "total_records": len(records),
        "total_confirmed_records": total_confirmed_records,
        "transitional_records_count": len(transition_pending_records),
        "transition_pending_records": sorted(set(transition_pending_records)),
        "missing_final_locator_records": sorted(set(missing_final_locator_records)),
        "final_authority_ready_records": final_authority_ready_records,
        "ready_for_final_authority_closeout": ready_for_final_authority_closeout,
        "group_counts": group_counts,
        "pending_replacements": pending_replacements,
        "invalid_rows": sorted(set(invalid_rows)),
        # passed 表示输入结构合法，不代表已完成最终权威替换。
        "passed": len(invalid_rows) == 0,
    }
