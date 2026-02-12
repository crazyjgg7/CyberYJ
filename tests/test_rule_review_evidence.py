import json

from cyberYJ.utils.rule_review_evidence import evaluate_rule_review_evidence


MATRIX_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_matrix.json"
EVIDENCE_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_evidence.json"


def test_rule_review_evidence_shape():
    report = evaluate_rule_review_evidence(MATRIX_PATH, EVIDENCE_PATH)
    assert "total_rules" in report
    assert "total_records" in report
    assert "missing_records" in report
    assert "extra_records" in report
    assert "duplicate_records" in report
    assert "source_target_mismatches" in report
    assert "invalid_verified_records" in report
    assert "invalid_blocked_records" in report
    assert "invalid_pending_records" in report
    assert "passed" in report


def test_rule_review_evidence_passed():
    report = evaluate_rule_review_evidence(MATRIX_PATH, EVIDENCE_PATH)
    assert report["missing_records"] == []
    assert report["extra_records"] == []
    assert report["duplicate_records"] == []
    assert report["source_target_mismatches"] == []
    assert report["invalid_verified_records"] == []
    assert report["invalid_blocked_records"] == []
    assert report["invalid_pending_records"] == []
    assert report["passed"] is True


def test_rule_review_evidence_detects_missing_record(tmp_path):
    matrix = json.loads(open(MATRIX_PATH, "r", encoding="utf-8").read())
    evidence = json.loads(open(EVIDENCE_PATH, "r", encoding="utf-8").read())
    evidence["records"] = evidence["records"][:-1]

    tmp_matrix = tmp_path / "matrix.json"
    tmp_evidence = tmp_path / "evidence.json"
    tmp_matrix.write_text(json.dumps(matrix, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_evidence.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")

    report = evaluate_rule_review_evidence(str(tmp_matrix), str(tmp_evidence))
    assert report["passed"] is False
    assert len(report["missing_records"]) == 1
