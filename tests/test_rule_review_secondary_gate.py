import json
from pathlib import Path

from cyberYJ.utils.rule_review_secondary_gate import evaluate_rule_review_secondary_gate


EVIDENCE_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_evidence.json"


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sample_evidence_one_record() -> dict:
    return {
        "version": "1.0.0",
        "evidence_status_enum": ["pending", "missing_text", "unavailable", "conflict", "confirmed"],
        "records": [
            {
                "group": "flying_star_rules",
                "id": "periods_table",
                "source_target": "cinii_dili_bianzheng_shu",
                "evidence_status": "confirmed",
                "source_id": "cinii_dili_bianzheng_shu",
                "edition": "book",
                "section": "chap1",
                "locator": "第12页",
                "summary": "摘要",
                "reviewed_by": "codex",
                "reviewed_at": "2026-02-12",
                "notes": "ok",
                "second_reviewer": "apple",
                "second_reviewed_at": "2026-02-12",
            }
        ],
    }


def test_rule_review_secondary_gate_shape():
    report = evaluate_rule_review_secondary_gate(EVIDENCE_PATH)
    assert "total_records" in report
    assert "total_confirmed_records" in report
    assert "secondary_ready_records" in report
    assert "missing_secondary_fields" in report
    assert "ready_for_full_secondary_review" in report
    assert "passed" in report


def test_rule_review_secondary_gate_baseline_not_ready():
    report = evaluate_rule_review_secondary_gate(EVIDENCE_PATH)
    assert report["total_confirmed_records"] == 35
    assert report["secondary_ready_records"] < report["total_confirmed_records"]
    assert report["ready_for_full_secondary_review"] is False
    assert report["passed"] is True


def test_rule_review_secondary_gate_ready_on_complete_record(tmp_path):
    evidence_path = tmp_path / "evidence.json"
    _write_json(evidence_path, _sample_evidence_one_record())

    report = evaluate_rule_review_secondary_gate(str(evidence_path))
    assert report["total_records"] == 1
    assert report["total_confirmed_records"] == 1
    assert report["secondary_ready_records"] == 1
    assert report["missing_secondary_fields"] == {}
    assert report["ready_for_full_secondary_review"] is True
    assert report["passed"] is True
