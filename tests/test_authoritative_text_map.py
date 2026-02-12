from cyberYJ.utils.authoritative_text_map import (
    match_mapping_item,
    match_luopan_item,
    validate_authoritative_text_map_file,
)


def test_authoritative_text_map_valid():
    errors = validate_authoritative_text_map_file(
        "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
    )
    assert errors == []


def test_match_luopan_item_v2_field_path():
    item = {
        "field_path": "data.fengshui.flying_stars_scoring.thresholds"
    }
    match = match_luopan_item(item)
    assert match is not None
    assert match["target"] == "luopan"
    assert match["section"] == "flying_stars_scoring"
    assert match["field"] == "thresholds"


def test_match_mapping_item_scenario_wildcard_field_path():
    item = {
        "field_path": "data.scenarios.career.hexagrams[*].overall_tendency"
    }
    match = match_mapping_item(item, hexagram_id=11, scenario_code="career")
    assert match is not None
    assert match["target"] == "scenario_analysis.overall_tendency"


def test_match_mapping_item_scenario_specific_wildcard_subscene():
    item = {
        "field_path": "data.scenarios.career.hexagrams[*].scenario_specific[*].advice"
    }
    match = match_mapping_item(item, hexagram_id=11, scenario_code="career")
    assert match is not None
    assert match["target"] == "scenario_specific.*.advice"
