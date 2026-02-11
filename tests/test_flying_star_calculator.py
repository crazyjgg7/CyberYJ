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


def test_combine_flying_stars_thresholds_from_config():
    house_map = {
        "中宫": {"mountain_star": 9, "facing_star": 9},
    }
    annual_map = {"中宫": 2}
    scoring = {
        "stars": {
            "2": {"score": -2},
            "9": {"score": 2}
        },
        "thresholds": {
            "auspicious": 5,
            "inauspicious": -5
        }
    }

    combined, auspicious, inauspicious = combine_flying_stars(house_map, annual_map, scoring)
    assert combined["中宫"]["level"] == "neutral"
    assert auspicious == []
    assert inauspicious == []

    combined2, auspicious2, _ = combine_flying_stars(
        house_map,
        annual_map,
        scoring,
        auspicious_threshold=1,
        inauspicious_threshold=-1
    )
    assert combined2["中宫"]["level"] == "auspicious"
    assert "中宫" in auspicious2


def test_combine_flying_stars_missing_annual_star_neutral():
    house_map = {
        "中宫": {"mountain_star": 9, "facing_star": 9},
    }
    annual_map = {}
    scoring = {
        "stars": {
            "9": {"score": 2}
        },
        "fallback": {
            "missing_annual_star": "neutral"
        }
    }

    combined, auspicious, inauspicious = combine_flying_stars(house_map, annual_map, scoring)
    assert "中宫" in combined
    assert combined["中宫"]["annual_star"] is None
    assert combined["中宫"]["level"] == "neutral"
    assert combined["中宫"]["score"] is None
    assert auspicious == []
    assert inauspicious == []
