from cyberYJ.utils.source_ref_integrity import evaluate_source_ref_integrity


DATA_ROOT = "/Users/apple/dev/CyberYJ/data"
SOURCES_PATH = "/Users/apple/dev/CyberYJ/data/core/sources.json"


def test_source_ref_integrity_report_shape():
    report = evaluate_source_ref_integrity(DATA_ROOT, SOURCES_PATH)
    assert "scanned_files" in report
    assert "source_ref_count" in report
    assert "unknown_source_refs" in report
    assert "invalid_source_ref_entries" in report
    assert "passed" in report


def test_source_ref_integrity_passed():
    report = evaluate_source_ref_integrity(DATA_ROOT, SOURCES_PATH)
    assert report["source_ref_count"] > 0
    assert report["unknown_source_refs"] == []
    assert report["invalid_source_ref_entries"] == []
    assert report["passed"] is True
