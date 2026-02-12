from cyberYJ.api.coin_mapper import map_coins_to_divination_input


def test_map_coins_to_trigrams_and_changing_lines():
    mapped = map_coins_to_divination_input([8, 8, 8, 9, 8, 8])
    assert mapped["line_bits"] == [0, 0, 0, 1, 0, 0]
    assert mapped["hexagram_code"] == "000100"
    assert mapped["lower_trigram"] == "坤"
    assert mapped["upper_trigram"] == "艮"
    assert mapped["changing_lines"] == [4]
    assert mapped["primary_changing_line"] == 4


def test_map_coins_without_changing_line():
    mapped = map_coins_to_divination_input([7, 7, 8, 8, 7, 8])
    assert mapped["changing_lines"] == []
    assert mapped["primary_changing_line"] is None
