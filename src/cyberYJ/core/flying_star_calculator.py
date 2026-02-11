from typing import Dict, Tuple, List


def _score_star(scoring: Dict[str, Dict[str, int]], star: int) -> int:
    entry = scoring.get(str(star))
    if not entry:
        return 0
    return int(entry.get("score", 0))


def combine_flying_stars(
    house_map: Dict[str, Dict[str, int]],
    annual_map: Dict[str, int],
    scoring: Dict[str, Dict[str, int]],
    auspicious_threshold: int = 2,
    inauspicious_threshold: int = -2
) -> Tuple[Dict[str, Dict[str, int]], List[str], List[str]]:
    if "stars" in scoring:
        scoring = scoring["stars"]
    combined: Dict[str, Dict[str, int]] = {}
    auspicious: List[str] = []
    inauspicious: List[str] = []

    for palace, house_stars in house_map.items():
        annual_star = annual_map.get(palace)
        if annual_star is None:
            continue

        mountain_star = house_stars.get("mountain_star")
        facing_star = house_stars.get("facing_star")

        score = (
            _score_star(scoring, mountain_star) +
            _score_star(scoring, facing_star) +
            _score_star(scoring, annual_star)
        )

        level = "neutral"
        if score >= auspicious_threshold:
            level = "auspicious"
            auspicious.append(palace)
        elif score <= inauspicious_threshold:
            level = "inauspicious"
            inauspicious.append(palace)

        combined[palace] = {
            "mountain_star": mountain_star,
            "facing_star": facing_star,
            "annual_star": annual_star,
            "score": score,
            "level": level
        }

    return combined, auspicious, inauspicious
