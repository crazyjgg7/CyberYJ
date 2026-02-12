import json
from pathlib import Path

from cyberYJ.utils.rule_review_status_sync import sync_rule_review_matrix_from_evidence


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sample_matrix() -> dict:
    return {
        "version": "1.0.0",
        "status_enum": ["pending", "verified", "blocked"],
        "groups": {
            "luopan_24_mountains": [
                {
                    "id": "壬",
                    "status": "blocked",
                    "source_target": "qingnang_aoyu",
                    "notes": "waiting evidence",
                }
            ]
        },
    }


def _sample_evidence_confirmed() -> dict:
    return {
        "version": "1.0.0",
        "evidence_status_enum": ["pending", "missing_text", "unavailable", "conflict", "confirmed"],
        "records": [
            {
                "group": "luopan_24_mountains",
                "id": "壬",
                "source_target": "qingnang_aoyu",
                "evidence_status": "confirmed",
                "source_id": "qingnang_aoyu",
                "edition": "四库全书本",
                "section": "卷1",
                "locator": "第1页",
                "summary": "二十四山向定义",
                "reviewed_by": "codex",
                "reviewed_at": "2026-02-12",
                "notes": "ready",
            }
        ],
    }


def test_status_sync_dry_run_does_not_write(tmp_path):
    matrix_path = tmp_path / "matrix.json"
    evidence_path = tmp_path / "evidence.json"
    _write_json(matrix_path, _sample_matrix())
    _write_json(evidence_path, _sample_evidence_confirmed())

    report = sync_rule_review_matrix_from_evidence(
        matrix_path=str(matrix_path),
        evidence_path=str(evidence_path),
        dry_run=True,
    )
    matrix_after = json.loads(matrix_path.read_text(encoding="utf-8"))

    assert report["would_update_count"] == 1
    assert report["updated_count"] == 0
    assert report["applied"] is False
    assert matrix_after["groups"]["luopan_24_mountains"][0]["status"] == "blocked"


def test_status_sync_apply_updates_blocked_to_verified(tmp_path):
    matrix_path = tmp_path / "matrix.json"
    evidence_path = tmp_path / "evidence.json"
    _write_json(matrix_path, _sample_matrix())
    _write_json(evidence_path, _sample_evidence_confirmed())

    report = sync_rule_review_matrix_from_evidence(
        matrix_path=str(matrix_path),
        evidence_path=str(evidence_path),
        dry_run=False,
    )
    matrix_after = json.loads(matrix_path.read_text(encoding="utf-8"))
    row = matrix_after["groups"]["luopan_24_mountains"][0]

    assert report["would_update_count"] == 1
    assert report["updated_count"] == 1
    assert report["applied"] is True
    assert row["status"] == "verified"
    assert "AUTO-VERIFIED" in row["notes"]


def test_status_sync_skips_invalid_confirmed_record(tmp_path):
    matrix_path = tmp_path / "matrix.json"
    evidence_path = tmp_path / "evidence.json"
    matrix = _sample_matrix()
    evidence = _sample_evidence_confirmed()
    evidence["records"][0]["locator"] = ""
    _write_json(matrix_path, matrix)
    _write_json(evidence_path, evidence)

    report = sync_rule_review_matrix_from_evidence(
        matrix_path=str(matrix_path),
        evidence_path=str(evidence_path),
        dry_run=False,
    )
    matrix_after = json.loads(matrix_path.read_text(encoding="utf-8"))

    assert report["updated_count"] == 0
    assert report["invalid_confirmed_records"] != []
    assert matrix_after["groups"]["luopan_24_mountains"][0]["status"] == "blocked"
