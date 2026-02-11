from cyberYJ.utils.authoritative_text_map import validate_authoritative_text_map_file


def test_authoritative_text_map_valid():
    errors = validate_authoritative_text_map_file(
        "/Users/apple/dev/CyberYJ/data/mappings/authoritative_text_map.json"
    )
    assert errors == []
