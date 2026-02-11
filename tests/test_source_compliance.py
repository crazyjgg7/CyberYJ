from cyberYJ.utils.source_compliance import evaluate_source_compliance


SOURCES_PATH = "/Users/apple/dev/CyberYJ/data/core/sources.json"
POLICY_PATH = "/Users/apple/dev/CyberYJ/data/core/source_compliance_policy.json"


def test_source_compliance_report_shape():
    report = evaluate_source_compliance(SOURCES_PATH, POLICY_PATH)
    assert "required_source_ids" in report
    assert "present_required_ids" in report
    assert "missing_required_ids" in report
    assert "invalid_fields" in report
    assert "passed" in report


def test_source_compliance_passed():
    report = evaluate_source_compliance(SOURCES_PATH, POLICY_PATH)
    assert report["passed"] is True
    assert report["missing_required_ids"] == []
    assert report["invalid_fields"] == []
