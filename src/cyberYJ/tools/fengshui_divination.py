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
from typing import Dict, Any, Optional, List
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
                scenario_hexagram
            )
        else:
            result["do_dont"] = self._generate_do_dont(
                hexagram,
                None,
                element_analysis,
                scenario_hexagram
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
        scenario_hexagram: Optional[Dict[str, Any]] = None
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
        do_list = []
        dont_list = []

        # 优先使用场景化数据（如果有）
        if scenario_hexagram:
            # 从场景数据中提取建议
            opportunities = scenario_hexagram.get('opportunities', [])
            challenges = scenario_hexagram.get('challenges', [])

            # 机遇转化为"宜做"
            for opp in opportunities[:3]:
                do_list.append(opp)

            # 挑战转化为"忌做"
            for chal in challenges[:3]:
                dont_list.append(chal)

        # 如果场景数据不足，使用通用建议
        if len(do_list) < 3:
            # 根据五行关系给出建议
            relation_type = element_analysis.get('relation_type', '')

            if relation_type == '生':
                do_list.append("顺势而为，借助外力")
                do_list.append("积极进取，把握机遇")
                dont_list.append("过于保守，错失良机")
            elif relation_type == '克':
                do_list.append("谨慎行事，化解冲突")
                do_list.append("以柔克刚，迂回前进")
                dont_list.append("硬碰硬，激化矛盾")
            else:  # 比和
                do_list.append("稳扎稳打，持续发展")
                do_list.append("团结协作，共同进步")
                dont_list.append("急于求成，冒进行事")

            # 根据卦象特点添加建议
            hexagram_name = hexagram['name']

            # 特殊卦象的建议
            special_advice = {
                '乾': (['自强不息', '积极进取'], ['骄傲自满', '刚愎自用']),
                '坤': (['厚德载物', '包容谦逊'], ['过于被动', '失去原则']),
                '泰': (['把握时机', '促进交流'], ['得意忘形', '忽视隐患']),
                '否': (['韬光养晦', '等待时机'], ['强行突破', '意气用事']),
                '既济': (['居安思危', '保持警惕'], ['松懈大意', '停滞不前']),
                '未济': (['谨慎前行', '做好准备'], ['急于求成', '盲目乐观'])
            }

            if hexagram_name in special_advice:
                do_add, dont_add = special_advice[hexagram_name]
                do_list.extend(do_add)
                dont_list.extend(dont_add)

        # 如果有变卦，添加变化相关建议
        if changing_hexagram:
            do_list.append("顺应变化，灵活调整")
            dont_list.append("固守成规，拒绝改变")

        return {
            "do": do_list[:5],  # 最多5条
            "dont": dont_list[:5]
        }

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
                elif target == "main_hexagram.image":
                    result["main_hexagram"]["image"] = content
                elif target == "scenario_analysis.key_points":
                    result["scenario_analysis"]["key_points"] = [content]
                elif target.startswith("scenario_specific."):
                    parts = target.split(".")
                    if len(parts) == 3:
                        _, sub, field = parts
                        if "scenario_specific" not in result:
                            result["scenario_specific"] = {}
                        if sub not in result["scenario_specific"]:
                            result["scenario_specific"][sub] = {}
                        result["scenario_specific"][sub][field] = content
                trace.append(f"权威映射: {match['field_path']}")

            for sid in source_ref:
                if sid not in applied_sources:
                    applied_sources.append(sid)

            if "scenario_analysis" in result and "convention" in source_ref:
                trace.append("注记: 权威映射仍含 convention 归纳规则")

        return applied_sources


def create_tool() -> FengshuiDivinationTool:
    """创建风水占卜工具实例"""
    return FengshuiDivinationTool()
