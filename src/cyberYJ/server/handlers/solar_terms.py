"""
solar_terms_lookup MCP 工具处理器
"""

from typing import Any, Dict, Optional, List

from cyberYJ.core.solar_calculator import SolarCalculator
from cyberYJ.utils.data_loader import get_data_loader
from cyberYJ.server.validation import get_timezone, parse_timestamp, optional_type
from cyberYJ.utils.authoritative_text_map import match_solar_terms_item


class SolarTermsHandler:
    """节气查询处理器"""

    def __init__(self, calculator: Optional[SolarCalculator] = None):
        self._calculator = calculator or SolarCalculator()
        self._data_loader = get_data_loader()

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        optional_type(arguments.get("timestamp"), str, "timestamp")
        timezone = get_timezone(arguments.get("timezone"))
        dt = parse_timestamp(arguments.get("timestamp"), timezone)

        term_info = self._calculator.get_current_solar_term(dt, timezone)

        trace = [
            f"输入时间: {dt.isoformat()}",
            f"当前太阳黄经: {term_info['solar_longitude']}°",
            f"匹配节气: {term_info['name']}（黄经 {term_info['longitude']}°）",
            f"距下一节气约: {term_info['days_to_next']} 天 → {term_info['next_term']}"
        ]

        sources = []
        cma = self._data_loader.get_source_by_id('cma_24_terms')
        if cma:
            sources.append(f"节气数据: {cma['title']}")

        mapped_sources = self._apply_authoritative_mappings(term_info, trace)
        for sid in mapped_sources:
            if sid == "cma_24_terms":
                continue
            src = self._data_loader.get_source_by_id(sid)
            if src:
                sources.append(f"权威映射: {src.get('title', sid)}")

        return {
            "solar_term": term_info["name"],
            "solar_longitude": term_info["solar_longitude"],
            "longitude": term_info["longitude"],
            "days_to_next": term_info["days_to_next"],
            "next_term": term_info["next_term"],
            "trace": trace,
            "sources": sources
        }

    def _apply_authoritative_mappings(
        self,
        term_info: Dict[str, Any],
        trace: List[str]
    ) -> List[str]:
        mapping = self._data_loader.get_authoritative_text_map()
        items = mapping.get("items", [])
        if not items:
            return []

        applied_sources: List[str] = []

        for item in items:
            match = match_solar_terms_item(item, term_info["name"])
            if not match:
                continue

            text_kind = item.get("text_kind")
            content = item.get("content")
            source_ref = item.get("source_ref", [])

            if text_kind == "citation_only":
                trace.append(f"权威映射: {match['field_path']} (citation_only)")
            elif content:
                field = match.get("field") or ""
                # 尝试字段级替换
                if field in ("name", "solar_term"):
                    term_info["name"] = content
                    trace.append(f"权威替换: 当前节气 → {content}")
                elif field in ("longitude", "solar_longitude_deg"):
                    try:
                        term_info["longitude"] = float(content)
                        trace.append(f"权威替换: 节气黄经 → {term_info['longitude']}°")
                    except Exception:
                        trace.append(f"权威摘要: {content}")
                elif field == "solar_longitude":
                    try:
                        term_info["solar_longitude"] = float(content)
                        trace.append(f"权威替换: 当前黄经 → {term_info['solar_longitude']}°")
                    except Exception:
                        trace.append(f"权威摘要: {content}")
                elif field == "next_term":
                    term_info["next_term"] = content
                    trace.append(f"权威替换: 下一节气 → {content}")
                else:
                    trace.append(f"权威摘要: {content}")

            for sid in source_ref:
                if sid not in applied_sources:
                    applied_sources.append(sid)

            if "convention" in source_ref:
                trace.append("注记: 权威映射仍含 convention 归纳规则")

        return applied_sources
