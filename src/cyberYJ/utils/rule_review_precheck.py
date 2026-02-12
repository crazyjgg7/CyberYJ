"""
M4-P3 规则结构预核对（矩阵 vs 数据文件）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _extract_ids(rows: List[Dict[str, Any]]) -> Set[str]:
    ids: Set[str] = set()
    for row in rows:
        if isinstance(row, dict) and isinstance(row.get("id"), str):
            ids.add(row["id"])
    return ids


def evaluate_rule_review_precheck(data_root: str, matrix_path: str) -> Dict[str, Any]:
    root = Path(data_root)
    matrix = _load_json(Path(matrix_path))
    groups = matrix.get("groups", {})
    if not isinstance(groups, dict):
        raise ValueError("matrix.groups must be object")

    matrix_luopan = _extract_ids(groups.get("luopan_24_mountains", []))
    matrix_bazhai = _extract_ids(groups.get("bazhai_rules", []))
    matrix_flying = _extract_ids(groups.get("flying_star_rules", []))

    luopan_data = _load_json(root / "fengshui" / "luopan.json")
    bazhai_data = _load_json(root / "fengshui" / "ba_zhai.json")
    fs_periods = _load_json(root / "fengshui" / "flying_stars_periods.json")
    fs_house = _load_json(root / "fengshui" / "flying_stars_house.json")
    fs_scoring = _load_json(root / "fengshui" / "flying_stars_scoring.json")

    luopan_ids = {
        row.get("name")
        for row in luopan_data
        if isinstance(row, dict) and isinstance(row.get("name"), str)
    }
    bazhai_ids = {
        row.get("house_gua")
        for row in bazhai_data
        if isinstance(row, dict) and isinstance(row.get("house_gua"), str)
    }

    luopan_report = {
        "matrix_count": len(matrix_luopan),
        "data_count": len(luopan_ids),
        "missing_in_data": sorted(matrix_luopan - luopan_ids),
        "extra_in_data": sorted(luopan_ids - matrix_luopan),
    }
    bazhai_report = {
        "matrix_count": len(matrix_bazhai),
        "data_count": len(bazhai_ids),
        "missing_in_data": sorted(matrix_bazhai - bazhai_ids),
        "extra_in_data": sorted(bazhai_ids - matrix_bazhai),
    }

    flying_requirements: List[str] = []
    period_ids: Set[int] = set()
    invalid_period_rows = 0
    if isinstance(fs_periods, list):
        for row in fs_periods:
            if not isinstance(row, dict):
                invalid_period_rows += 1
                continue
            period = row.get("period")
            if isinstance(period, int):
                period_ids.add(period)
            else:
                invalid_period_rows += 1
    else:
        invalid_period_rows += 1

    if "periods_table" in matrix_flying and len(period_ids) == 0:
        flying_requirements.append("periods_table")

    valid_house_rows = 0
    invalid_house_rows = 0
    house_pairs: Set[tuple[int, str]] = set()
    if isinstance(fs_house, list):
        for row in fs_house:
            if not isinstance(row, dict):
                invalid_house_rows += 1
                continue
            period = row.get("period")
            mountain = row.get("sitting_mountain")
            palace_map = row.get("palace_map")
            if not (isinstance(period, int) and isinstance(mountain, str) and isinstance(palace_map, dict)):
                invalid_house_rows += 1
                continue
            valid_house_rows += 1
            house_pairs.add((period, mountain))
    else:
        invalid_house_rows += 1

    expected_house_pairs = len(period_ids) * len(luopan_ids)
    if "house_rules_24x9" in matrix_flying:
        if (
            valid_house_rows == 0 or
            invalid_house_rows > 0 or
            len(house_pairs) != expected_house_pairs
        ):
            flying_requirements.append("house_rules_24x9")

    stars_table = fs_scoring.get("stars") if isinstance(fs_scoring, dict) else None
    valid_star_entries = 0
    if isinstance(stars_table, dict):
        for star in range(1, 10):
            row = stars_table.get(str(star))
            if (
                isinstance(row, dict) and
                isinstance(row.get("score"), (int, float)) and
                isinstance(row.get("label"), str)
            ):
                valid_star_entries += 1
    if "scoring_thresholds" in matrix_flying and valid_star_entries != 9:
        flying_requirements.append("scoring_thresholds")

    flying_report = {
        "matrix_count": len(matrix_flying),
        "missing_requirements": sorted(flying_requirements),
        "period_count": len(period_ids),
        "invalid_period_rows": invalid_period_rows,
        "house_expected_pairs": expected_house_pairs,
        "house_pair_count": len(house_pairs),
        "valid_house_rows": valid_house_rows,
        "invalid_house_rows": invalid_house_rows,
        "scoring_star_count": valid_star_entries,
    }

    passed = (
        len(luopan_report["missing_in_data"]) == 0 and
        len(luopan_report["extra_in_data"]) == 0 and
        len(bazhai_report["missing_in_data"]) == 0 and
        len(bazhai_report["extra_in_data"]) == 0 and
        len(flying_report["missing_requirements"]) == 0
    )

    return {
        "luopan": luopan_report,
        "bazhai": bazhai_report,
        "flying_star": flying_report,
        "passed": passed,
    }
