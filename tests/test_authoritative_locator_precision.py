from cyberYJ.utils.authoritative_locator_precision import evaluate_authoritative_locator_precision


MAPPING_PATH = "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
TARGETS_PATH = "/Users/apple/dev/CyberYJ/data/mappings/source_evidence_targets.json"


def test_authoritative_locator_precision_shape():
    report = evaluate_authoritative_locator_precision(MAPPING_PATH, TARGETS_PATH)
    assert "total_targets" in report
    assert "passed_targets" in report
    assert "failed_target_ids" in report
    assert "missing_mapping_target_ids" in report
    assert "missing_precision_locator_target_ids" in report
    assert "passed" in report


def test_authoritative_locator_precision_passed():
    report = evaluate_authoritative_locator_precision(MAPPING_PATH, TARGETS_PATH)
    assert report["passed"] is True
    assert report["failed_target_ids"] == []
    assert report["missing_mapping_target_ids"] == []
    assert report["missing_precision_locator_target_ids"] == []
