from cyberYJ.utils.rule_review_precheck import evaluate_rule_review_precheck


DATA_ROOT = "/Users/apple/dev/CyberYJ/data"
MATRIX_PATH = "/Users/apple/dev/CyberYJ/data/review/rule_review_matrix.json"


def test_rule_review_precheck_shape():
    report = evaluate_rule_review_precheck(DATA_ROOT, MATRIX_PATH)
    assert "luopan" in report
    assert "bazhai" in report
    assert "flying_star" in report
    assert "passed" in report


def test_rule_review_precheck_passed():
    report = evaluate_rule_review_precheck(DATA_ROOT, MATRIX_PATH)
    assert report["luopan"]["missing_in_data"] == []
    assert report["luopan"]["extra_in_data"] == []
    assert report["bazhai"]["missing_in_data"] == []
    assert report["bazhai"]["extra_in_data"] == []
    assert report["flying_star"]["missing_requirements"] == []
    assert report["flying_star"]["period_count"] == 9
    assert report["flying_star"]["invalid_period_rows"] == 0
    assert report["flying_star"]["house_expected_pairs"] == 216
    assert report["flying_star"]["house_pair_count"] == 216
    assert report["flying_star"]["valid_house_rows"] == 216
    assert report["flying_star"]["invalid_house_rows"] == 0
    assert report["flying_star"]["scoring_star_count"] == 9
    assert report["passed"] is True
