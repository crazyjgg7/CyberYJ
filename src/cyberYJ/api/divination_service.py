"""
Service adapter for Wechat mini-program divination HTTP API.
"""

from typing import Any, Dict, List, Optional

from cyberYJ.api.coin_mapper import TRIGRAM_FROM_BITS, map_coins_to_divination_input
from cyberYJ.api.consistency_guard import apply_consistency_guard
from cyberYJ.api.scene_output import build_scene_enhancements
from cyberYJ.server.handlers.fengshui import FengshuiHandler
from cyberYJ.utils.data_loader import DataLoader, get_data_loader


class DivinationService:
    """Adapter from coins-based payload to current fengshui handler output."""

    SCENE_TO_QUESTION_TYPE = {
        "fortune": "命运",
        "career": "事业",
        "love": "感情",
        "wealth": "财运",
        "health": "健康",
        "study": "学业",
        "family": "家庭",
        "travel": "出行",
        "lawsuit": "诉讼",
    }

    def __init__(
        self,
        handler: Optional[FengshuiHandler] = None,
        data_loader: Optional[DataLoader] = None,
    ) -> None:
        self._handler = handler or FengshuiHandler()
        self._data_loader = data_loader or get_data_loader()

    def interpret(
        self,
        coins: List[int],
        question: Optional[str] = None,
        scene_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        mapped = map_coins_to_divination_input(coins)
        question_type = self.SCENE_TO_QUESTION_TYPE.get(scene_type) if scene_type else None
        tool_result = self._handler.execute(
            {
                "upper_trigram": mapped["upper_trigram"],
                "lower_trigram": mapped["lower_trigram"],
                "changing_line": mapped["primary_changing_line"],
                "question_type": question_type,
                "question_text": question,
            }
        )
        resolved_scene_type = (
            tool_result.get("scenario", {}).get("code")
            or scene_type
            or "fortune"
        )
        do_dont = self._normalize_do_dont(tool_result)
        guard_result = apply_consistency_guard(tool_result, do_dont)
        do_dont = guard_result["do_dont"]
        consistency = guard_result["consistency"]
        scene_enhancements = build_scene_enhancements(
            tool_result=tool_result,
            scene_type=resolved_scene_type,
            do_dont=do_dont,
        )

        response = {
            "scene_type": resolved_scene_type,
            "hexagram": self._build_hexagram(mapped, tool_result),
            "changing_hexagram": self._build_changing_hexagram(mapped, tool_result),
            "analysis": self._build_analysis(coins, mapped, tool_result),
            "do_dont": do_dont,
            "keywords": scene_enhancements["keywords"],
            "advice_tags": scene_enhancements["advice_tags"],
            "score": scene_enhancements["score"],
            "consistency": consistency,
            "trace": self._build_trace(coins, mapped, tool_result),
            "sources": self._normalize_sources(tool_result),
        }
        return response

    def _build_hexagram(self, mapped: Dict[str, Any], tool_result: Dict[str, Any]) -> Dict[str, Any]:
        main_hexagram = tool_result.get("main_hexagram", {})
        hexagram_id = main_hexagram.get("id", 0)
        return {
            "code": mapped["hexagram_code"],
            "name": main_hexagram.get("name", ""),
            "symbol": main_hexagram.get("symbol", self._symbol_from_id(hexagram_id)),
            "judgment": main_hexagram.get("judgment", ""),
            "image": main_hexagram.get("image", ""),
            "upper_trigram": main_hexagram.get("upper_trigram", mapped["upper_trigram"]),
            "lower_trigram": main_hexagram.get("lower_trigram", mapped["lower_trigram"]),
        }

    def _build_changing_hexagram(
        self,
        mapped: Dict[str, Any],
        tool_result: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        changing_lines = mapped["changing_lines"]
        if not changing_lines:
            return None

        changed_bits = list(mapped["line_bits"])
        for line in changing_lines:
            idx = line - 1
            changed_bits[idx] = 1 - changed_bits[idx]

        lower_bits = tuple(changed_bits[:3])
        upper_bits = tuple(changed_bits[3:])
        lower_trigram = TRIGRAM_FROM_BITS[lower_bits]
        upper_trigram = TRIGRAM_FROM_BITS[upper_bits]
        changed_hexagram = self._data_loader.get_hexagram_by_trigrams(upper_trigram, lower_trigram)

        if changed_hexagram:
            hexagram_id = changed_hexagram.get("id", 0)
            return {
                "code": "".join(str(v) for v in changed_bits),
                "name": changed_hexagram.get("name", ""),
                "symbol": self._symbol_from_id(hexagram_id),
                "judgment": changed_hexagram.get("judgment_summary", ""),
                "image": changed_hexagram.get("image_summary", ""),
                "upper_trigram": changed_hexagram.get("upper_trigram", upper_trigram),
                "lower_trigram": changed_hexagram.get("lower_trigram", lower_trigram),
            }

        # fallback to tool result (single changing line path)
        fallback = tool_result.get("changing_hexagram")
        if not fallback:
            return None

        hexagram_id = fallback.get("id", 0)
        return {
            "code": "".join(str(v) for v in changed_bits),
            "name": fallback.get("name", ""),
            "symbol": self._symbol_from_id(hexagram_id),
            "judgment": fallback.get("judgment", ""),
            "image": "",
        }

    def _build_analysis(
        self,
        coins: List[int],
        mapped: Dict[str, Any],
        tool_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        scenario_analysis = tool_result.get("scenario_analysis", {})
        overall = scenario_analysis.get("overall_tendency") or tool_result.get("fortune_advice", "")

        return {
            "overall": overall,
            "active_lines": self._build_active_lines(coins, mapped["changing_lines"]),
            "five_elements": tool_result.get("five_elements", ""),
            "solar_term": tool_result.get("solar_term_influence", ""),
            "advice": tool_result.get("fortune_advice", ""),
        }

    def _build_active_lines(self, coins: List[int], changing_lines: List[int]) -> List[str]:
        result: List[str] = []
        for line in changing_lines:
            coin_value = coins[line - 1]
            line_type = "老阴" if coin_value == 6 else "老阳"
            result.append(f"第{line}爻动（{line_type}）")
        return result

    def _normalize_do_dont(self, tool_result: Dict[str, Any]) -> Dict[str, List[str]]:
        do_dont = tool_result.get("do_dont") or {}
        do_items = do_dont.get("do") if isinstance(do_dont.get("do"), list) else []
        dont_items = do_dont.get("dont") if isinstance(do_dont.get("dont"), list) else []
        return {"do": do_items, "dont": dont_items}

    def _build_trace(
        self,
        coins: List[int],
        mapped: Dict[str, Any],
        tool_result: Dict[str, Any],
    ) -> List[str]:
        trace = [
            "Step 0: mapped coins to yin/yang bits and trigrams",
            (
                "Step 1: lower={lower}, upper={upper}, changing_lines={lines}, code={code}"
            ).format(
                lower=mapped["lower_trigram"],
                upper=mapped["upper_trigram"],
                lines=mapped["changing_lines"],
                code=mapped["hexagram_code"],
            ),
            "Step 2: called fengshui_divination handler",
            "Step 3: transformed result to mini-program API schema",
        ]
        tool_trace = tool_result.get("trace")
        if isinstance(tool_trace, list):
            trace.extend(tool_trace)
        return trace

    def _normalize_sources(self, tool_result: Dict[str, Any]) -> List[str]:
        sources = tool_result.get("sources")
        if isinstance(sources, list):
            return [str(item) for item in sources]
        return []

    @staticmethod
    def _symbol_from_id(hexagram_id: int) -> str:
        if isinstance(hexagram_id, int) and 1 <= hexagram_id <= 64:
            return chr(0x4DC0 + hexagram_id - 1)
        return ""
