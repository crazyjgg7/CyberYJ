from cyberYJ.utils.source_evidence_check import evaluate_source_evidence


MAPPING_PATH = "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
TARGETS_PATH = "/Users/apple/dev/CyberYJ/data/mappings/source_evidence_targets.json"


def test_source_evidence_report_shape():
    report = evaluate_source_evidence(MAPPING_PATH, TARGETS_PATH)
    assert "total_targets" in report
    assert "passed_targets" in report
    assert "failed_target_ids" in report
    assert "missing_mapping_target_ids" in report
    assert "passed" in report


def test_source_evidence_passed():
    report = evaluate_source_evidence(MAPPING_PATH, TARGETS_PATH)
    assert report["total_targets"] > 0
    assert report["failed_target_ids"] == []
    assert report["missing_mapping_target_ids"] == []
    assert report["passed"] is True
