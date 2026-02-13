"""
Consistency guard for scene-driven suggestion output.
"""

from typing import Any, Dict, List, Tuple


_ATTACK_HINTS = ("积极", "进取", "把握机遇", "扩张", "突破", "冲刺", "大展宏图", "冒进")
_GUARD_HINTS = ("低调", "谨慎", "收敛", "等待", "暂缓", "自保", "韬光养晦", "先守")
_GUARD_CONFLICT_DONT = ("过于保守", "错失良机", "不宜等待", "忌守")
_ATTACK_CONFLICT_DO = ("暂缓", "按兵不动", "完全观望", "停止行动")


def apply_consistency_guard(
    tool_result: Dict[str, Any],
    do_dont: Dict[str, List[str]],
) -> Dict[str, Any]:
    """
    Check and adjust obvious tone conflicts in do/dont suggestions.
    """
    tone = _resolve_tone(tool_result, do_dont)
    advice_text = str(tool_result.get("fortune_advice", ""))

    adjusted_do, do_adjustments = _filter_items(
        items=do_dont.get("do", []),
        tone=tone,
        item_type="do",
    )
    adjusted_dont, dont_adjustments = _filter_items(
        items=do_dont.get("dont", []),
        tone=tone,
        item_type="dont",
    )

    adjustments = do_adjustments + dont_adjustments
    conflict_count = len(adjustments)

    if tone == "guard" and _contains_any(advice_text, _ATTACK_HINTS):
        conflict_count += 1
        adjustments.append("analysis.advice 包含进攻型措辞")
    if tone == "attack" and _contains_any(advice_text, _GUARD_HINTS):
        conflict_count += 1
        adjustments.append("analysis.advice 包含守势措辞")

    return {
        "do_dont": {
            "do": adjusted_do,
            "dont": adjusted_dont,
        },
        "consistency": {
            "status": "adjusted" if conflict_count > 0 else "pass",
            "tone": tone,
            "conflict_count": conflict_count,
            "adjustments": adjustments,
        },
    }


def _resolve_tone(tool_result: Dict[str, Any], do_dont: Dict[str, List[str]]) -> str:
    trace = tool_result.get("trace", [])
    if isinstance(trace, list):
        for item in trace:
            if not isinstance(item, str):
                continue
            if item.startswith("建议基调: "):
                tone_label = item.split(":", 1)[1].strip()
                if tone_label == "守势":
                    return "guard"
                if tone_label == "攻势":
                    return "attack"
                if tone_label == "中性":
                    return "neutral"

    do_text = " ".join(do_dont.get("do", []))
    dont_text = " ".join(do_dont.get("dont", []))
    merged = f"{do_text} {dont_text}"
    if _contains_any(merged, _GUARD_HINTS):
        return "guard"
    if _contains_any(merged, _ATTACK_HINTS):
        return "attack"
    return "neutral"


def _filter_items(items: List[str], tone: str, item_type: str) -> Tuple[List[str], List[str]]:
    filtered: List[str] = []
    adjustments: List[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            continue
        if tone == "guard":
            if item_type == "do" and _contains_any(item, _ATTACK_HINTS):
                adjustments.append(f"{item_type}: 移除进攻项 -> {item}")
                continue
            if item_type == "dont" and _contains_any(item, _GUARD_CONFLICT_DONT):
                adjustments.append(f"{item_type}: 移除守势冲突项 -> {item}")
                continue
        if tone == "attack":
            if item_type == "do" and _contains_any(item, _ATTACK_CONFLICT_DO):
                adjustments.append(f"{item_type}: 移除守势项 -> {item}")
                continue
            if item_type == "dont" and _contains_any(item, _ATTACK_HINTS):
                adjustments.append(f"{item_type}: 移除进攻冲突项 -> {item}")
                continue

        if item not in filtered:
            filtered.append(item)

    return filtered, adjustments


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    return any(hint in text for hint in hints)
