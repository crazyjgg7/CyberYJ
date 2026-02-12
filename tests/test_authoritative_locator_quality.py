from cyberYJ.utils.authoritative_locator_quality import evaluate_authoritative_locator_quality


MAPPING_PATH = "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
TARGETS_PATH = "/Users/apple/dev/CyberYJ/data/mappings/source_evidence_targets.json"


def test_authoritative_locator_quality_shape():
    report = evaluate_authoritative_locator_quality(MAPPING_PATH, TARGETS_PATH)
    assert "total_targets" in report
    assert "passed_targets" in report
    assert "missing_mapping_target_ids" in report
    assert "missing_locator_target_ids" in report
    assert "passed" in report


def test_authoritative_locator_quality_passed():
    report = evaluate_authoritative_locator_quality(MAPPING_PATH, TARGETS_PATH)
    assert report["passed"] is True
    assert report["missing_mapping_target_ids"] == []
    assert report["missing_locator_target_ids"] == []
