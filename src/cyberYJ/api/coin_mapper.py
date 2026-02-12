"""
Convert six-line coin toss values to trigram inputs for FengshuiHandler.
"""

from typing import Dict, List, Tuple


# bits order: from lower line to upper line (初爻 -> 上爻), 阳=1 阴=0
TRIGRAM_FROM_BITS: Dict[Tuple[int, int, int], str] = {
    (1, 1, 1): "乾",
    (0, 1, 1): "兌",
    (1, 0, 1): "離",
    (0, 0, 1): "震",
    (1, 1, 0): "巽",
    (0, 1, 0): "坎",
    (1, 0, 0): "艮",
    (0, 0, 0): "坤",
}


def map_coins_to_divination_input(coins: List[int]) -> Dict[str, object]:
    """
    Map coin toss results to divination input parameters.

    coins value: 6/7/8/9, order from 初爻 to 上爻.
    """
    if len(coins) != 6:
        raise ValueError("coins数组必须包含6个元素 (6/7/8/9)")
    if any(v not in (6, 7, 8, 9) for v in coins):
        raise ValueError("coins数组必须包含6个元素 (6/7/8/9)")

    line_bits = [1 if value in (7, 9) else 0 for value in coins]
    lower_bits = tuple(line_bits[:3])
    upper_bits = tuple(line_bits[3:])

    changing_lines = [idx + 1 for idx, value in enumerate(coins) if value in (6, 9)]

    return {
        "line_bits": line_bits,
        "hexagram_code": "".join(str(bit) for bit in line_bits),
        "lower_trigram": TRIGRAM_FROM_BITS[lower_bits],
        "upper_trigram": TRIGRAM_FROM_BITS[upper_bits],
        "changing_lines": changing_lines,
        "primary_changing_line": changing_lines[0] if changing_lines else None,
    }

