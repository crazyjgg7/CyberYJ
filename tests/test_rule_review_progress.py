from cyberYJ.utils.rule_review_progress import evaluate_rule_review_progress


MATRIX_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_matrix.json"


def test_rule_review_progress_shape():
    report = evaluate_rule_review_progress(MATRIX_PATH)
    assert "total_items" in report
    assert "verified_items" in report
    assert "pending_items" in report
    assert "completion_ratio" in report
    assert "group_counts" in report
    assert "invalid_items" in report
    assert "passed" in report


def test_rule_review_progress_baseline_counts():
    report = evaluate_rule_review_progress(MATRIX_PATH)
    assert report["group_counts"]["luopan_24_mountains"]["total"] == 24
    assert report["group_counts"]["bazhai_rules"]["total"] == 8
    assert report["group_counts"]["flying_star_rules"]["total"] == 3
    assert report["total_items"] == 35
    assert report["invalid_items"] == []
