import json
from pathlib import Path

from cyberYJ.utils.rule_review_final_authority import (
    evaluate_rule_review_final_authority,
)


EVIDENCE_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_evidence.json"
BATCHES_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_final_replacement_batches.json"


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sample_payload(record: dict) -> dict:
    return {
        "version": "1.0.0",
        "evidence_status_enum": ["pending", "missing_text", "unavailable", "conflict", "confirmed"],
        "records": [record],
    }


def test_rule_review_final_authority_shape():
    report = evaluate_rule_review_final_authority(EVIDENCE_PATH)
    assert "total_records" in report
    assert "total_confirmed_records" in report
    assert "transitional_records_count" in report
    assert "transition_pending_records" in report
    assert "missing_final_locator_records" in report
    assert "final_authority_ready_records" in report
    assert "ready_for_final_authority_closeout" in report
    assert "pending_replacements" in report
    assert "passed" in report


def test_rule_review_final_authority_baseline_not_closeout():
    report = evaluate_rule_review_final_authority(EVIDENCE_PATH)
    assert report["total_records"] == 35
    assert report["total_confirmed_records"] == 35
    assert report["transitional_records_count"] == 0
    assert report["final_authority_ready_records"] == 35
    assert "flying_star_rules::periods_table" not in report["transition_pending_records"]
    assert "flying_star_rules::house_rules_24x9" not in report["transition_pending_records"]
    assert "flying_star_rules::scoring_thresholds" not in report["transition_pending_records"]
    assert "bazhai_rules::乾宅" not in report["transition_pending_records"]
    assert "bazhai_rules::兑宅" not in report["transition_pending_records"]
    assert "bazhai_rules::离宅" not in report["transition_pending_records"]
    assert "bazhai_rules::震宅" not in report["transition_pending_records"]
    assert "bazhai_rules::巽宅" not in report["transition_pending_records"]
    assert "bazhai_rules::坎宅" not in report["transition_pending_records"]
    assert "bazhai_rules::艮宅" not in report["transition_pending_records"]
    assert "bazhai_rules::坤宅" not in report["transition_pending_records"]
    assert "luopan_24_mountains::壬" not in report["transition_pending_records"]
    assert "luopan_24_mountains::子" not in report["transition_pending_records"]
    assert "luopan_24_mountains::癸" not in report["transition_pending_records"]
    assert "luopan_24_mountains::丑" not in report["transition_pending_records"]
    assert "luopan_24_mountains::艮" not in report["transition_pending_records"]
    assert "luopan_24_mountains::寅" not in report["transition_pending_records"]
    assert "luopan_24_mountains::甲" not in report["transition_pending_records"]
    assert "luopan_24_mountains::卯" not in report["transition_pending_records"]
    assert "luopan_24_mountains::乙" not in report["transition_pending_records"]
    assert "luopan_24_mountains::辰" not in report["transition_pending_records"]
    assert "luopan_24_mountains::巽" not in report["transition_pending_records"]
    assert "luopan_24_mountains::巳" not in report["transition_pending_records"]
    assert "luopan_24_mountains::丙" not in report["transition_pending_records"]
    assert "luopan_24_mountains::午" not in report["transition_pending_records"]
    assert "luopan_24_mountains::丁" not in report["transition_pending_records"]
    assert "luopan_24_mountains::未" not in report["transition_pending_records"]
    assert "luopan_24_mountains::坤" not in report["transition_pending_records"]
    assert "luopan_24_mountains::申" not in report["transition_pending_records"]
    assert "luopan_24_mountains::庚" not in report["transition_pending_records"]
    assert "luopan_24_mountains::酉" not in report["transition_pending_records"]
    assert "luopan_24_mountains::辛" not in report["transition_pending_records"]
    assert "luopan_24_mountains::戌" not in report["transition_pending_records"]
    assert "luopan_24_mountains::乾" not in report["transition_pending_records"]
    assert "luopan_24_mountains::亥" not in report["transition_pending_records"]
    assert report["ready_for_final_authority_closeout"] is True
    assert report["passed"] is True


def test_rule_review_final_authority_ready_on_final_record(tmp_path):
    evidence_path = tmp_path / "evidence.json"
    _write_json(
        evidence_path,
        _sample_payload(
            {
                "group": "flying_star_rules",
                "id": "periods_table",
                "source_target": "cinii_dili_bianzheng_shu",
                "evidence_status": "confirmed",
                "source_id": "cinii_dili_bianzheng_shu",
                "edition": "地理辨正疏（权威版）",
                "section": "卷一",
                "locator": "第12页",
                "summary": "摘要",
                "reviewed_by": "codex",
                "reviewed_at": "2026-02-12",
                "notes": "已替换为最终权威版本页码定位。",
                "second_reviewer": "apple",
                "second_reviewed_at": "2026-02-12",
            }
        ),
    )

    report = evaluate_rule_review_final_authority(str(evidence_path))
    assert report["total_records"] == 1
    assert report["total_confirmed_records"] == 1
    assert report["transitional_records_count"] == 0
    assert report["missing_final_locator_records"] == []
    assert report["pending_replacements"] == []
    assert report["final_authority_ready_records"] == 1
    assert report["ready_for_final_authority_closeout"] is True
    assert report["passed"] is True


def test_rule_review_final_authority_marks_missing_locator(tmp_path):
    evidence_path = tmp_path / "evidence.json"
    _write_json(
        evidence_path,
        _sample_payload(
            {
                "group": "bazhai_rules",
                "id": "乾宅",
                "source_target": "cinii_bazhai_mingjing",
                "evidence_status": "confirmed",
                "source_id": "cinii_bazhai_mingjing",
                "edition": "八宅明镜（权威版）",
                "section": "上卷",
                "locator": "",
                "summary": "摘要",
                "reviewed_by": "codex",
                "reviewed_at": "2026-02-12",
                "notes": "已替换为最终权威版本。",
            }
        ),
    )

    report = evaluate_rule_review_final_authority(str(evidence_path))
    assert report["total_confirmed_records"] == 1
    assert report["transitional_records_count"] == 0
    assert report["missing_final_locator_records"] == ["bazhai_rules::乾宅"]
    assert report["final_authority_ready_records"] == 0
    assert report["ready_for_final_authority_closeout"] is False
    assert len(report["pending_replacements"]) == 1


def test_rule_review_final_replacement_batches_consistent_with_report():
    report = evaluate_rule_review_final_authority(EVIDENCE_PATH)
    batches = json.loads(Path(BATCHES_PATH).read_text(encoding="utf-8"))

    assert batches["total_pending_items"] == len(report["pending_replacements"])

    batch_rows = batches["batches"]
    assert isinstance(batch_rows, list) and batch_rows
    assert sum(int(row["item_count"]) for row in batch_rows) == batches["total_pending_items"]

    counts = {row["batch"]: int(row["item_count"]) for row in batch_rows}
    pending_by_group = {}
    for item in report["pending_replacements"]:
        group = item["group"]
        pending_by_group[group] = pending_by_group.get(group, 0) + 1

    assert counts.get("A", 0) == pending_by_group.get("flying_star_rules", 0)
    assert counts.get("B", 0) == pending_by_group.get("bazhai_rules", 0)
    assert counts.get("C1", 0) + counts.get("C2", 0) + counts.get("C3", 0) == pending_by_group.get(
        "luopan_24_mountains",
        0,
    )
