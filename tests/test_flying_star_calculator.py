from cyberYJ.core.flying_star_calculator import combine_flying_stars


def test_combine_flying_stars_basic():
    house_map = {
        "中宫": {"mountain_star": 9, "facing_star": 9},
        "坎": {"mountain_star": 8, "facing_star": 1}
    }
    annual_map = {"中宫": 2, "坎": 1}
    scoring = {
        "stars": {
            "1": {"score": 2},
            "2": {"score": -2},
            "8": {"score": 3},
            "9": {"score": 2}
        }
    }

    combined, auspicious, inauspicious = combine_flying_stars(house_map, annual_map, scoring)

    assert "中宫" in combined
    assert "坎" in combined
    assert combined["中宫"]["score"] == 2
    assert "坎" in auspicious
