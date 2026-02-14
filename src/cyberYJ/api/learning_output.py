"""
Learning-mode response transformer for mini-program compliance.
"""

from __future__ import annotations

from typing import Any, Dict, List


_TEXT_REPLACEMENTS = (
    ("趋吉避凶", "学习建议"),
    ("吉凶", "文本倾向"),
    ("运势", "主题倾向"),
    ("结果判断", "解读角度"),
    ("行动指令", "学习建议"),
    ("宜：", "可参考："),
    ("忌：", "注意点："),
    ("宜 ", "可参考 "),
    ("忌 ", "注意 "),
    ("会不会", "可从哪些角度理解"),
    ("能否", "如何理解"),
)

_TONE_TO_READING_STYLE = {
    "attack": "主动阅读",
    "guard": "审慎阅读",
    "neutral": "平衡阅读",
}


def to_learning_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform divination response into learning-oriented response schema.
    """
    data = _sanitize_obj(raw)
    analysis = data.get("analysis") if isinstance(data.get("analysis"), dict) else {}

    learning_points = _build_learning_points(data.get("do_dont"))
    topic_tags = _build_topic_tags(data.get("advice_tags"))
    reading_style = _build_reading_style(data.get("consistency"))

    data.pop("do_dont", None)
    data.pop("advice_tags", None)
    data.pop("score", None)
    data.pop("consistency", None)

    if isinstance(analysis, dict):
        advice = str(analysis.get("advice", "")).strip()
        if advice:
            analysis["advice"] = (
                f"{advice}\n（说明：本内容用于经典学习与文本解读，不对现实结果作判断。）"
            )
        else:
            analysis["advice"] = "建议结合原文注释进行学习记录，不作为现实决策依据。"
        data["analysis"] = analysis

    data["learning_points"] = learning_points
    data["topic_tags"] = topic_tags
    data["reading_style"] = reading_style
    return data


def _build_learning_points(do_dont: Any) -> Dict[str, List[str]]:
    if not isinstance(do_dont, dict):
        return {"can_refer": [], "attention": []}

    can_refer = do_dont.get("do") if isinstance(do_dont.get("do"), list) else []
    attention = do_dont.get("dont") if isinstance(do_dont.get("dont"), list) else []
    return {
        "can_refer": [str(item) for item in can_refer if str(item).strip()],
        "attention": [str(item) for item in attention if str(item).strip()],
    }


def _build_topic_tags(advice_tags: Any) -> List[str]:
    if not isinstance(advice_tags, list):
        return ["国学学习", "文本解读"]
    tags = [str(item).strip() for item in advice_tags if str(item).strip()]
    if "国学学习" not in tags:
        tags.append("国学学习")
    return tags[:6]


def _build_reading_style(consistency: Any) -> str:
    if not isinstance(consistency, dict):
        return "平衡阅读"
    tone = str(consistency.get("tone", "")).strip()
    return _TONE_TO_READING_STYLE.get(tone, "平衡阅读")


def _sanitize_obj(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _sanitize_obj(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize_obj(item) for item in value]
    if isinstance(value, str):
        text = value
        for old, new in _TEXT_REPLACEMENTS:
            text = text.replace(old, new)
        return text
    return value
