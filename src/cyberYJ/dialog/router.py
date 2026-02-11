"""
关键词路由：将用户输入映射为 MCP 工具调用参数
"""

import re
from typing import Any, Dict, Optional, Tuple

from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool


_FENGSHUI_PREFIX: Tuple[str, ...] = ("风水：", "风水:")
_LUOPAN_PREFIX: Tuple[str, ...] = ("罗盘：", "罗盘:")

_CHANGING_LINE_MAP = {
    "初": 1,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "上": 6,
}

_BUILDING_TYPE_MAP = {
    "住宅": "住宅",
    "公寓": "住宅",
    "办公室": "办公室",
    "商铺": "商铺",
    "工厂": "工厂",
}


def route_message(text: str) -> Dict[str, Any]:
    raw = text.strip()
    if raw.startswith(_FENGSHUI_PREFIX):
        content = _strip_prefix(raw, _FENGSHUI_PREFIX)
        return _route_fengshui(content)
    if raw.startswith(_LUOPAN_PREFIX):
        content = _strip_prefix(raw, _LUOPAN_PREFIX)
        return _route_luopan(content)

    return {
        "error": "未识别的关键词入口，请使用“风水：”或“罗盘：”开头",
        "raw": raw,
    }


def _strip_prefix(raw: str, prefixes: Tuple[str, ...]) -> str:
    for prefix in prefixes:
        if raw.startswith(prefix):
            return raw[len(prefix):].strip()
    return raw.strip()


def _route_fengshui(content: str) -> Dict[str, Any]:
    upper, lower = _extract_trigrams(content)
    if not upper or not lower:
        return {
            "error": "风水输入需包含“上X下Y”或“上卦X下卦Y”",
            "raw": content,
        }

    question_type = _detect_question_type(content)
    changing_line = _extract_changing_line(content)

    arguments: Dict[str, Any] = {
        "upper_trigram": upper,
        "lower_trigram": lower,
        "question_text": content,
    }
    if question_type:
        arguments["question_type"] = question_type
    if changing_line:
        arguments["changing_line"] = changing_line

    return {
        "tool": "fengshui_divination",
        "arguments": arguments,
    }


def _route_luopan(content: str) -> Dict[str, Any]:
    direction = _extract_direction(content)
    building_type = _extract_building_type(content)
    owner_birth = _extract_birth(content)

    if not direction:
        return {
            "error": "罗盘输入需包含坐向，例如“坐北朝南”或“坐亥向巳”",
            "raw": content,
        }
    if not building_type:
        return {
            "error": "罗盘输入需包含建筑类型（住宅/办公室/商铺/工厂）",
            "raw": content,
        }

    arguments: Dict[str, Any] = {
        "sitting_direction": direction,
        "building_type": building_type,
    }
    if owner_birth:
        arguments["owner_birth"] = owner_birth

    return {
        "tool": "luopan_orientation",
        "arguments": arguments,
    }


def _extract_trigrams(content: str) -> Tuple[Optional[str], Optional[str]]:
    # 支持：上坤下乾 / 上卦坤下卦乾 / 上坤 下乾
    m = re.search(r"上卦?([^\s，,]+)下卦?([^\s，,]+)", content)
    if m:
        return m.group(1), m.group(2)
    return None, None


def _detect_question_type(content: str) -> Optional[str]:
    mapping = FengshuiDivinationTool.QUESTION_TYPE_MAPPING
    for key in mapping.keys():
        if key in content:
            return key
    return None


def _extract_changing_line(content: str) -> Optional[int]:
    # 第1爻 / 1爻 / 初爻 / 二爻
    m = re.search(r"第([1-6])爻", content)
    if m:
        return int(m.group(1))
    m = re.search(r"([1-6])爻", content)
    if m:
        return int(m.group(1))
    m = re.search(r"(初|一|二|三|四|五|六|上)爻", content)
    if m:
        return _CHANGING_LINE_MAP.get(m.group(1))
    return None


def _extract_direction(content: str) -> Optional[str]:
    # 优先匹配“坐...向...”或“坐...朝...”
    m = re.search(r"(坐[^\s]+(?:朝|向)[^\s]+)", content)
    if m:
        return m.group(1)
    # 兜底：抓取“坐...”片段
    m = re.search(r"(坐[^\s]+)", content)
    if m:
        return m.group(1)
    return None


def _extract_building_type(content: str) -> Optional[str]:
    for key, value in _BUILDING_TYPE_MAP.items():
        if key in content:
            return value
    return None


def _extract_birth(content: str) -> Optional[str]:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", content)
    if m:
        return m.group(1)
    return None
