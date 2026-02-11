from cyberYJ.utils.authoritative_text_map import (
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
