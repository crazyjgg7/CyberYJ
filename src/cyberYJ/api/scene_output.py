"""
Scene-focused response enrichment helpers for mini-program API.
"""

from typing import Any, Dict, List


_SCENE_TAGS = {
    "fortune": "运势",
    "career": "职场",
    "love": "关系",
    "wealth": "财务",
    "health": "健康",
    "study": "学业",
    "family": "家庭",
    "travel": "出行",
    "lawsuit": "诉讼",
}

_RISK_HINTS = ("风险", "冲突", "破财", "争执", "冒进", "纠纷", "隐患")
_COMM_HINTS = ("沟通", "交流", "协作", "协调", "讨论")
_TIMING_HINTS = ("时机", "窗口", "节奏", "时点", "等待")


def build_scene_enhancements(
    tool_result: Dict[str, Any],
    scene_type: str,
    do_dont: Dict[str, List[str]],
) -> Dict[str, Any]:
    """Build keywords/advice_tags/score fields from tool output."""
    scenario_analysis = tool_result.get("scenario_analysis", {})
    scenario_specific = tool_result.get("scenario_specific", {})

    keywords = _extract_keywords(scenario_analysis, scenario_specific)
    advice_tags = _extract_advice_tags(
        scene_type=scene_type,
        do_dont=do_dont,
        trace=tool_result.get("trace", []),
    )
    score = _score_from_rating(scenario_analysis.get("rating"))

    return {
        "keywords": keywords,
        "advice_tags": advice_tags,
        "score": score,
    }


def _extract_keywords(
    scenario_analysis: Dict[str, Any],
    scenario_specific: Dict[str, Any],
) -> List[str]:
    result: List[str] = []

    for item in scenario_analysis.get("key_points", []):
        _append_unique(result, item)

    if isinstance(scenario_specific, dict):
        for detail in scenario_specific.values():
            if not isinstance(detail, dict):
                continue
            for advice in detail.get("advice", []):
                _append_unique(result, advice)
                if len(result) >= 8:
                    return result

    return result[:8]


def _extract_advice_tags(
    scene_type: str,
    do_dont: Dict[str, List[str]],
    trace: List[str],
) -> List[str]:
    tags: List[str] = []

    tone_label = _tone_label_from_trace(trace)
    if tone_label:
        _append_unique(tags, tone_label)
    _append_unique(tags, _SCENE_TAGS.get(scene_type, "场景"))

    do_text = " ".join(do_dont.get("do", []))
    dont_text = " ".join(do_dont.get("dont", []))
    merged = f"{do_text} {dont_text}"

    if _contains_any(merged, _RISK_HINTS):
        _append_unique(tags, "防风险")
    if _contains_any(do_text, _COMM_HINTS):
        _append_unique(tags, "沟通")
    if _contains_any(merged, _TIMING_HINTS):
        _append_unique(tags, "节奏把控")

    return tags[:5]


def _tone_label_from_trace(trace: List[str]) -> str:
    if not isinstance(trace, list):
        return ""
    for item in trace:
        if not isinstance(item, str):
            continue
        if item.startswith("建议基调: "):
            tone = item.split(":", 1)[1].strip()
            if tone == "守势":
                return "守势"
            if tone == "攻势":
                return "进取"
            if tone == "中性":
                return "稳健"
    return ""


def _score_from_rating(rating: Any) -> int:
    try:
        value = int(rating)
    except (TypeError, ValueError):
        value = 3
    value = max(1, min(5, value))
    return value * 20


def _append_unique(target: List[str], item: Any) -> None:
    if not isinstance(item, str):
        return
    normalized = item.strip()
    if not normalized:
        return
    if normalized not in target:
        target.append(normalized)


def _contains_any(text: str, hints: tuple[str, ...]) -> bool:
    return any(hint in text for hint in hints)
