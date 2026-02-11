from typing import Any, Dict, Optional, Tuple, List


def _score_star(scoring: Dict[str, Dict[str, int]], star: Optional[int], default_score: int = 0) -> int:
    if star is None:
        return default_score
    entry = scoring.get(str(star))
    if not entry:
        return default_score
    return int(entry.get("score", 0))


def combine_flying_stars(
    house_map: Dict[str, Dict[str, int]],
    annual_map: Dict[str, int],
    scoring: Dict[str, Any],
    auspicious_threshold: Optional[int] = None,
    inauspicious_threshold: Optional[int] = None
) -> Tuple[Dict[str, Dict[str, int]], List[str], List[str]]:
    score_table = scoring.get("stars", scoring)
    thresholds = scoring.get("thresholds", {})
    fallback = scoring.get("fallback", {})

    if auspicious_threshold is None:
        auspicious_threshold = int(thresholds.get("auspicious", 2))
    if inauspicious_threshold is None:
        inauspicious_threshold = int(thresholds.get("inauspicious", -2))

    missing_annual_star_strategy = fallback.get("missing_annual_star", "skip")
    unknown_star_score = int(fallback.get("unknown_star_score", 0))

    combined: Dict[str, Dict[str, int]] = {}
    auspicious: List[str] = []
    inauspicious: List[str] = []

    for palace, house_stars in house_map.items():
        annual_star = annual_map.get(palace)
        if annual_star is None:
            if missing_annual_star_strategy == "skip":
                continue
            if missing_annual_star_strategy == "neutral":
                combined[palace] = {
                    "mountain_star": house_stars.get("mountain_star"),
                    "facing_star": house_stars.get("facing_star"),
                    "annual_star": None,
                    "score": None,
                    "level": "neutral",
                    "reason": "missing_annual_star"
                }
                continue

        mountain_star = house_stars.get("mountain_star")
        facing_star = house_stars.get("facing_star")

        score = (
            _score_star(score_table, mountain_star, unknown_star_score) +
            _score_star(score_table, facing_star, unknown_star_score) +
            _score_star(score_table, annual_star, unknown_star_score)
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
