"""
风水占卜工具 - 易经六十四卦解卦分析

实现 fengshui_divination MCP 工具，提供：
- 卦象解析
- 五行分析
- 节气影响
- 场景化分析（命运、事业、感情等）
- 趋吉避凶建议
"""

from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
import pytz

from cyberYJ.core.hexagram_analyzer import HexagramAnalyzer
from cyberYJ.core.solar_calculator import SolarCalculator
from cyberYJ.core.prompt_builder import PromptBuilder
from cyberYJ.utils.data_loader import get_data_loader
from cyberYJ.utils.authoritative_text_map import match_mapping_item


class FengshuiDivinationTool:
    """风水占卜工具 - 易经六十四卦解卦分析"""

    # 问题类型到场景代码的映射
    QUESTION_TYPE_MAPPING = {
        "命运": "fortune",
        "流年": "fortune",
        "运势": "fortune",
        "事业": "career",
        "工作": "career",
        "职业": "career",
        "求职": "career",
        "创业": "career",
        "感情": "love",
        "爱情": "love",
        "婚姻": "love",
        "恋爱": "love",
        "财运": "wealth",
        "财富": "wealth",
        "投资": "wealth",
        "健康": "health",
        "学业": "study",
        "考试": "study",
        "家庭": "family",
        "出行": "travel",
        "诉讼": "lawsuit"
    }

    # 建议基调关键词（用于一致性判定）
    GUARD_HINTS = [
        "低调", "收敛", "保守", "谨慎", "等待", "暂缓", "自保", "韬光养晦",
        "不宜", "避免冲突", "防止", "风险偏高", "不利", "凶"
    ]
    ATTACK_HINTS = [
        "积极", "进取", "把握机遇", "扩张", "突破", "推进", "冲刺", "放手一搏", "大展宏图"
    ]
    GUARD_CONFLICT_DONT = ["过于保守", "错失良机", "不宜等待", "忌守"]
    ATTACK_CONFLICT_DO = ["暂缓", "按兵不动", "完全观望", "停止行动"]

    # 强语义卦名的基调兜底（用于防止 key_points 缺失时跑偏）
    GUARD_HEXAGRAMS = {"明夷", "否", "遯", "剥", "困", "蹇", "坎"}
    ATTACK_HEXAGRAMS = {"乾", "泰", "晋", "大有", "升", "解"}

    TONE_TEMPLATES = {
        "guard": {
            "do": [
                "低调行事，先稳住局面",
                "以守代攻，控制节奏",
                "优先自保，减少无谓消耗",
            ],
            "dont": [
                "盲目冒进，强行突破",
                "高调出头，激化矛盾",
                "忽视风险，过度扩张",
            ],
        },
        "attack": {
            "do": [
                "顺势推进，主动把握窗口",
                "聚焦关键目标，果断执行",
                "整合资源，扩大成果",
            ],
            "dont": [
                "犹豫拖延，错失时机",
                "分散精力，贪多求快",
                "忽视边界，过度冒险",
            ],
        },
        "neutral": {
            "do": [
                "稳扎稳打，循序推进",
                "先验证再扩大投入",
                "保持沟通，动态调整",
            ],
            "dont": [
                "急于求成，一步到位",
                "情绪决策，忽略复盘",
                "长期僵化，不做调整",
            ],
        },
    }

    def __init__(self):
        """初始化工具"""
        self.hexagram_analyzer = HexagramAnalyzer()
        self.solar_calculator = SolarCalculator()
        self.prompt_builder = PromptBuilder()
        self.data_loader = get_data_loader()

    def execute(
        self,
        upper_trigram: str,
        lower_trigram: str,
        question_type: Optional[str] = None,
        question_text: Optional[str] = None,
        changing_line: Optional[int] = None,
        timestamp: Optional[str] = None,
        timezone: str = "Asia/Shanghai"
    ) -> Dict[str, Any]:
        """
        执行风水占卜分析

        Args:
            upper_trigram: 上卦（卦名/数字/方位）
            lower_trigram: 下卦（卦名/数字/方位）
            question_type: 问题类型（命运/事业/感情/财运/健康等），可选
            question_text: 用户问题原文（用于智能场景识别），可选
            changing_line: 变爻位置（1-6），可选
            timestamp: RFC3339 时间戳，可选（默认当前时间）
            timezone: IANA 时区名，默认 Asia/Shanghai

        Returns:
            包含卦象分析结果的字典
        """
        trace = []  # 推导路径记录

        # 1. 解析时间
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                if dt.tzinfo is None:
                    tz = pytz.timezone(timezone)
                    dt = tz.localize(dt)
                trace.append(f"使用指定时间: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            except Exception as e:
                raise ValueError(f"时间戳格式错误: {e}")
        else:
            tz = pytz.timezone(timezone)
            dt = datetime.now(tz)
            trace.append(f"使用当前时间: {dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # 2. 解析上下卦
        try:
            upper = self.hexagram_analyzer.parse_trigram_input(upper_trigram)
            trace.append(f"上卦解析: {upper_trigram} → {upper['name']}（{upper['element']}）")
        except Exception as e:
            raise ValueError(f"上卦解析失败: {e}")

        try:
            lower = self.hexagram_analyzer.parse_trigram_input(lower_trigram)
            trace.append(f"下卦解析: {lower_trigram} → {lower['name']}（{lower['element']}）")
        except Exception as e:
            raise ValueError(f"下卦解析失败: {e}")

        # 3. 获取本卦
        hexagram = self.hexagram_analyzer.get_hexagram(upper, lower)
        if not hexagram:
            raise ValueError(f"未找到卦象: {upper['name']}上{lower['name']}下")

        trace.append(f"本卦: 第{hexagram['id']}卦 {hexagram['name']}卦")

        # 4. 识别场景
        scenario_code = self._identify_scenario(question_type, question_text)
        if scenario_code:
            source_text = question_type if question_type else question_text
            trace.append(f"场景识别: {source_text} → {scenario_code}")
        else:
            scenario_code = "fortune"  # 默认使用命运场景
            trace.append(f"场景识别: 未指定问题类型，使用默认场景 fortune")

        # 5. 五行分析
        element_analysis = self.hexagram_analyzer.analyze_element_relation(hexagram)
        trace.append(f"五行关系: {element_analysis['description']}")

        # 6. 节气影响
        solar_term_info = self.solar_calculator.get_current_solar_term(dt, timezone)
        solar_influence = self.solar_calculator.get_solar_term_influence(dt, timezone)
        trace.append(f"当前节气: {solar_term_info['name']}（太阳黄经 {solar_term_info['solar_longitude']:.2f}°）")

        # 7. 获取场景数据
        scenario_data = self.data_loader.get_scenario_data(scenario_code)
        scenario_hexagram = self.data_loader.get_scenario_hexagram(scenario_code, hexagram['id'])

        # 8. 生成解释（使用新的场景化方式或回退到旧方式）
        if scenario_hexagram:
            trace.append(f"使用场景化数据: {scenario_code}")
            interpretation = self._generate_scenario_interpretation(
                hexagram,
                scenario_hexagram,
                scenario_data
            )
        else:
            trace.append(f"场景数据不完整，使用通用解释")
            interpretation = self.hexagram_analyzer.generate_interpretation(
                hexagram,
                question_type
            )

        # 9. 变卦分析（如果有）
        changing_hexagram = None
        if changing_line:
            if not (1 <= changing_line <= 6):
                raise ValueError(f"变爻位置必须在 1-6 之间，当前值: {changing_line}")

            changing_analysis = self.hexagram_analyzer.analyze_changing_line(
                hexagram,
                changing_line
            )
            changing_hexagram = changing_analysis['changed_hexagram']
            trace.append(f"变爻: 第{changing_line}爻变 → {changing_hexagram['name']}卦")

        # 10. 构建输出
        result = {
            "main_hexagram": {
                "id": hexagram['id'],
                "name": hexagram['name'],
                "symbol": self._get_hexagram_symbol(hexagram),
                "judgment": hexagram['judgment_summary'],
                "image": hexagram['image_summary'],
                "upper_trigram": hexagram['upper_trigram'],
                "lower_trigram": hexagram['lower_trigram']
            },
            "scenario": {
                "code": scenario_code,
                "name": scenario_data.get('scenario_info', {}).get('name', question_type) if scenario_data else question_type
            },
            "five_elements": element_analysis['description'],
            "solar_term_influence": solar_influence,
            "fortune_advice": interpretation.get('advice', ''),
            "trace": trace
        }

        # 添加场景化分析结果
        if scenario_hexagram:
            result["scenario_analysis"] = {
                "overall_tendency": scenario_hexagram.get('overall_tendency', ''),
                "rating": scenario_hexagram.get(f'{scenario_code}_rating', 3),
                "key_points": scenario_hexagram.get('key_points', [])
            }
            result["scenario_specific"] = scenario_hexagram.get("scenario_specific", {})
            if "convention" in scenario_hexagram.get("source_ref", []):
                trace.append("注记: 场景化结论含 convention 归纳规则")

        # 添加变卦信息
        if changing_hexagram:
            result["changing_hexagram"] = {
                "id": changing_hexagram.get('id'),
                "name": changing_hexagram.get('name'),
                "judgment": changing_hexagram.get('judgment_summary', ''),
                "interpretation": changing_analysis.get('interpretation', '')
            }
            result["do_dont"] = self._generate_do_dont(
                hexagram,
                changing_hexagram,
                element_analysis,
                scenario_hexagram,
                trace
            )
        else:
            result["do_dont"] = self._generate_do_dont(
                hexagram,
                None,
                element_analysis,
                scenario_hexagram,
                trace
            )

        # 添加免责声明（如果需要）
        if scenario_data:
            scenario_name = scenario_data.get('scenario_info', {}).get('name', '')
            disclaimer = self.data_loader.get_disclaimer_by_scenario(scenario_name)
            if disclaimer and disclaimer.get('level') in ['critical', 'high']:
                result["disclaimer"] = disclaimer.get('text', '')

        # 权威映射替换（如有）
        mapped_sources = self._apply_authoritative_mappings(
            result,
            hexagram_id=hexagram["id"],
            scenario_code=scenario_code,
            trace=trace
        )

        # 添加来源信息
        result["sources"] = self._get_sources(extra_source_ids=mapped_sources)

        return result

    def _identify_scenario(
        self,
        question_type: Optional[str],
        question_text: Optional[str]
    ) -> Optional[str]:
        """
        识别场景代码

        Args:
            question_type: 问题类型

        Returns:
            场景代码（如 fortune, career, love）
        """
        if not question_type:
            # 使用问题原文做关键词匹配
            if not question_text:
                return None
            for key, value in self.QUESTION_TYPE_MAPPING.items():
                if key in question_text:
                    return value
            return None

        # 直接匹配
        if question_type in self.QUESTION_TYPE_MAPPING:
            return self.QUESTION_TYPE_MAPPING[question_type]

        # 模糊匹配
        for key, value in self.QUESTION_TYPE_MAPPING.items():
            if key in question_type or question_type in key:
                return value

        return None

    def _generate_scenario_interpretation(
        self,
        hexagram: Dict[str, Any],
        scenario_hexagram: Dict[str, Any],
        scenario_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成场景化解释

        Args:
            hexagram: 卦象数据
            scenario_hexagram: 场景卦象数据
            scenario_data: 场景数据

        Returns:
            解释字典
        """
        # 提取关键信息
        key_points = scenario_hexagram.get('key_points', [])
        opportunities = scenario_hexagram.get('opportunities', [])
        challenges = scenario_hexagram.get('challenges', [])

        # 构建建议
        advice_parts = []

        if key_points:
            advice_parts.append("**核心要点**：")
            for point in key_points:
                advice_parts.append(f"- {point}")
            advice_parts.append("")

        if opportunities:
            advice_parts.append("**机遇**：")
            for opp in opportunities:
                advice_parts.append(f"- {opp}")
            advice_parts.append("")

        if challenges:
            advice_parts.append("**挑战**：")
            for chal in challenges:
                advice_parts.append(f"- {chal}")

        return {
            "advice": "\n".join(advice_parts) if advice_parts else "请参考卦辞和象辞进行分析。"
        }

    def _get_hexagram_symbol(self, hexagram: Dict[str, Any]) -> str:
        """
        获取卦象符号

        Args:
            hexagram: 卦象数据

        Returns:
            卦象符号（如 ䷀）
        """
        # 卦象符号 Unicode 范围: U+4DC0 - U+4DFF
        # 第1卦（乾）= U+4DC0, 第2卦（坤）= U+4DC1, ...
        hexagram_id = hexagram['id']
        if 1 <= hexagram_id <= 64:
            return chr(0x4DC0 + hexagram_id - 1)
        return ""

    def _generate_do_dont(
        self,
        hexagram: Dict[str, Any],
        changing_hexagram: Optional[Dict[str, Any]],
        element_analysis: Dict[str, Any],
        scenario_hexagram: Optional[Dict[str, Any]] = None,
        trace: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        生成宜忌建议

        Args:
            hexagram: 本卦
            changing_hexagram: 变卦（可选）
            element_analysis: 五行分析
            scenario_hexagram: 场景卦象数据（可选）

        Returns:
            包含 do 和 dont 列表的字典
        """
        do_list: List[str] = []
        dont_list: List[str] = []

        tone = self._determine_guidance_tone(
            hexagram=hexagram,
            element_analysis=element_analysis,
            scenario_hexagram=scenario_hexagram,
        )
        if trace is not None:
            tone_label = {"guard": "守势", "attack": "攻势", "neutral": "中性"}.get(tone, tone)
            trace.append(f"建议基调: {tone_label}")

        # 1) 场景优先：使用 opportunities/challenges 或 scenario_specific advice
        if scenario_hexagram:
            do_candidates, dont_candidates = self._collect_scenario_candidates(scenario_hexagram)
            do_list.extend(do_candidates)
            dont_list.extend(dont_candidates)

        # 2) 通用兜底：仅在场景数据不足时补齐，不再无条件注入“进取模板”
        if len(do_list) < 3 or len(dont_list) < 3:
            do_fallback, dont_fallback = self._build_generic_fallback(element_analysis, tone)
            do_list.extend(do_fallback)
            dont_list.extend(dont_fallback)

        # 3) 卦象级补充（保留历史行为，但走基调过滤）
        special_do, special_dont = self._get_special_advice(hexagram["name"])
        do_list.extend(special_do)
        dont_list.extend(special_dont)

        # 4) 变卦提示（按基调区分）
        if changing_hexagram:
            if tone == "guard":
                do_list.append("顺势微调，先守后动")
                dont_list.append("情绪化转向，频繁折腾")
            elif tone == "attack":
                do_list.append("顺势加速，动态校正")
                dont_list.append("固守旧法，错失窗口")
            else:
                do_list.append("顺应变化，灵活调整")
                dont_list.append("固守成规，拒绝改变")

        # 5) 一致性过滤 + 模板补齐
        do_list = self._filter_by_tone(do_list, tone, item_type="do")
        dont_list = self._filter_by_tone(dont_list, tone, item_type="dont")

        template = self.TONE_TEMPLATES.get(tone, self.TONE_TEMPLATES["neutral"])
        do_list = self._fill_with_template(do_list, template["do"])
        dont_list = self._fill_with_template(dont_list, template["dont"])

        return {"do": do_list[:5], "dont": dont_list[:5]}

    def _determine_guidance_tone(
        self,
        hexagram: Dict[str, Any],
        element_analysis: Dict[str, Any],
        scenario_hexagram: Optional[Dict[str, Any]],
    ) -> str:
        """判定建议基调：guard/attack/neutral。"""
        hexagram_name = hexagram.get("name", "")
        if hexagram_name in self.GUARD_HEXAGRAMS:
            return "guard"
        if hexagram_name in self.ATTACK_HEXAGRAMS:
            return "attack"

        tone = "neutral"
        if scenario_hexagram:
            tendency = scenario_hexagram.get("overall_tendency", "")
            if tendency in ("凶", "不利"):
                tone = "guard"
            elif tendency in ("大吉", "吉"):
                tone = "attack"

            key_points = " ".join(scenario_hexagram.get("key_points", []))
            if self._contains_any(key_points, self.GUARD_HINTS):
                tone = "guard"
            elif tone != "guard" and self._contains_any(key_points, self.ATTACK_HINTS):
                tone = "attack"

        # 仅在仍无法判定时，退回五行关系
        if tone == "neutral":
            relation_type = element_analysis.get("relation_type", "")
            if relation_type == "克":
                tone = "guard"
            elif relation_type == "生":
                tone = "attack"

        return tone

    def _collect_scenario_candidates(self, scenario_hexagram: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """从场景数据提取宜忌候选。"""
        do_list: List[str] = []
        dont_list: List[str] = []

        for opp in scenario_hexagram.get("opportunities", [])[:4]:
            if opp and opp not in do_list:
                do_list.append(opp)
        for chal in scenario_hexagram.get("challenges", [])[:4]:
            if chal and chal not in dont_list:
                dont_list.append(chal)

        # 非 fortune 场景通常没有 opportunities/challenges，退回 scenario_specific.advice
        scenario_specific = scenario_hexagram.get("scenario_specific", {})
        if isinstance(scenario_specific, dict):
            for detail in scenario_specific.values():
                if not isinstance(detail, dict):
                    continue
                for advice in detail.get("advice", []):
                    if advice and advice not in do_list:
                        do_list.append(advice)

        return do_list, dont_list

    def _build_generic_fallback(
        self, element_analysis: Dict[str, Any], tone: str
    ) -> Tuple[List[str], List[str]]:
        """构建通用兜底建议（受基调约束）。"""
        relation_type = element_analysis.get("relation_type", "")

        if tone == "guard":
            return (["谨慎行事，优先稳住局面"], ["盲目冒进，强行推进"])
        if tone == "attack":
            return (["顺势推进，把握关键机会"], ["犹豫拖延，坐失窗口"])

        # neutral：按五行给轻量补充
        if relation_type == "克":
            return (["谨慎行事，化解冲突"], ["硬碰硬，激化矛盾"])
        if relation_type == "生":
            return (["顺势而为，稳步推进"], ["忽视边界，过度冒险"])
        return (["稳扎稳打，持续发展"], ["急于求成，冒进行事"])

    def _get_special_advice(self, hexagram_name: str) -> Tuple[List[str], List[str]]:
        special_advice = {
            "乾": (["自强不息", "积极进取"], ["骄傲自满", "刚愎自用"]),
            "坤": (["厚德载物", "包容谦逊"], ["过于被动", "失去原则"]),
            "泰": (["把握时机", "促进交流"], ["得意忘形", "忽视隐患"]),
            "否": (["韬光养晦", "等待时机"], ["强行突破", "意气用事"]),
            "既济": (["居安思危", "保持警惕"], ["松懈大意", "停滞不前"]),
            "未济": (["谨慎前行", "做好准备"], ["急于求成", "盲目乐观"]),
        }
        return special_advice.get(hexagram_name, ([], []))

    def _filter_by_tone(self, items: List[str], tone: str, item_type: str) -> List[str]:
        filtered: List[str] = []
        for item in items:
            if not item:
                continue
            if tone == "guard":
                if item_type == "do" and self._contains_any(item, self.ATTACK_HINTS):
                    continue
                if item_type == "dont" and self._contains_any(item, self.GUARD_CONFLICT_DONT):
                    continue
            elif tone == "attack":
                if item_type == "do" and self._contains_any(item, self.ATTACK_CONFLICT_DO):
                    continue
                if item_type == "dont" and self._contains_any(item, self.ATTACK_HINTS):
                    continue

            if item not in filtered:
                filtered.append(item)
        return filtered

    @staticmethod
    def _fill_with_template(items: List[str], template_items: List[str], target_len: int = 3) -> List[str]:
        result = list(items)
        for template_item in template_items:
            if len(result) >= target_len:
                break
            if template_item not in result:
                result.append(template_item)
        return result

    @staticmethod
    def _contains_any(text: str, keywords: List[str]) -> bool:
        return any(keyword in text for keyword in keywords)

    def _get_sources(self, extra_source_ids: Optional[List[str]] = None) -> List[str]:
        """
        获取数据来源信息

        Returns:
            来源列表
        """
        sources = []

        extra_source_ids = extra_source_ids or []

        # 获取主要来源
        ctext = self.data_loader.get_source_by_id('ctext_yijing')
        if ctext:
            sources.append(f"卦辞象辞: {ctext['title']} ({ctext['url_or_archive']})")

        cma = self.data_loader.get_source_by_id('cma_24_terms')
        if cma:
            sources.append(f"节气数据: {cma['title']}")

        # 追加映射来源
        for sid in extra_source_ids:
            if sid in ("ctext_yijing", "cma_24_terms"):
                continue
            src = self.data_loader.get_source_by_id(sid)
            if src:
                label = src.get("title", sid)
                sources.append(f"权威映射: {label}")

        return sources

    def _apply_authoritative_mappings(
        self,
        result: Dict[str, Any],
        hexagram_id: int,
        scenario_code: Optional[str],
        trace: List[str]
    ) -> List[str]:
        mapping = self.data_loader.get_authoritative_text_map()
        items = mapping.get("items", [])
        if not items:
            return []

        applied_sources: List[str] = []

        for item in items:
            match = match_mapping_item(item, hexagram_id, scenario_code)
            if not match:
                continue

            text_kind = item.get("text_kind")
            content = item.get("content")
            source_ref = item.get("source_ref", [])

            if text_kind == "citation_only":
                trace.append(f"权威映射: {match['field_path']} (citation_only)")
            elif content:
                target = match["target"]
                if target == "main_hexagram.judgment":
                    result["main_hexagram"]["judgment"] = content
                    trace.append(f"权威映射: {match['field_path']}")
                elif target == "main_hexagram.image":
                    result["main_hexagram"]["image"] = content
                    trace.append(f"权威映射: {match['field_path']}")
                elif target.startswith("scenario_analysis.") or target.startswith("scenario_specific."):
                    # 场景字段级映射不直接覆盖原结论，统一以 authoritative_notes 暴露给前端。
                    result.setdefault("authoritative_notes", {})
                    result["authoritative_notes"][target] = content
                    trace.append(f"权威补充: {match['field_path']}")
                else:
                    trace.append(f"权威映射: {match['field_path']} (ignored_target)")

            for sid in source_ref:
                if sid not in applied_sources:
                    applied_sources.append(sid)

            if "scenario_analysis" in result and "convention" in source_ref:
                trace.append("注记: 权威映射仍含 convention 归纳规则")

        return applied_sources


def create_tool() -> FengshuiDivinationTool:
    """创建风水占卜工具实例"""
    return FengshuiDivinationTool()
