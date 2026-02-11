from cyberYJ.utils.authoritative_coverage import evaluate_authoritative_coverage


MAPPING_PATH = "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
TARGETS_PATH = "/Users/apple/dev/CyberYJ/data/mappings/authoritative_coverage_targets.json"


def test_evaluate_authoritative_coverage_shape():
    report = evaluate_authoritative_coverage(MAPPING_PATH, TARGETS_PATH)
    assert "total_targets" in report
    assert "covered_targets" in report
    assert "coverage_ratio" in report
    assert "threshold" in report
    assert "passed" in report
    assert "uncovered_target_ids" in report


def test_authoritative_coverage_meets_m4_threshold():
    report = evaluate_authoritative_coverage(MAPPING_PATH, TARGETS_PATH)
    assert report["threshold"] == 0.8
    assert report["coverage_ratio"] >= report["threshold"]
    assert report["passed"] is True
