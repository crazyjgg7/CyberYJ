from cyberYJ.utils.authoritative_locator_precision_full import (
    evaluate_authoritative_locator_precision_full,
)


MAPPING_PATH = "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"


def test_authoritative_locator_precision_full_shape():
    report = evaluate_authoritative_locator_precision_full(MAPPING_PATH)
    assert "total_summary_items" in report
    assert "passed_summary_items" in report
    assert "failed_items_count" in report
    assert "failed_field_paths" in report
    assert "failed_reasons" in report
    assert "passed" in report


def test_authoritative_locator_precision_full_passed():
    report = evaluate_authoritative_locator_precision_full(MAPPING_PATH)
    assert report["total_summary_items"] >= 157
    assert report["failed_items_count"] == 0
    assert report["failed_field_paths"] == []
    assert report["passed"] is True
