"""
卦象分析器模块

提供卦象解析、五行分析和卦辞解释功能。
支持多种输入格式，包括卦名、方位、数字等。
"""

from typing import Dict, List, Any, Optional, Union
from ..utils.data_loader import get_data_loader, DataLoader


class HexagramAnalyzer:
    """卦象分析器，提供卦象解析、五行分析和卦辞解释功能"""

    # 八卦序数映射（先天八卦序）
    TRIGRAM_NUMBERS = {
        1: "乾", 2: "兌", 3: "離", 4: "震",
        5: "巽", 6: "坎", 7: "艮", 8: "坤"
    }

    # 五行生克关系
    ELEMENT_RELATIONS = {
        ("金", "金"): "比和",
        ("木", "木"): "比和",
        ("水", "水"): "比和",
        ("火", "火"): "比和",
        ("土", "土"): "比和",
        ("木", "火"): "生",
        ("火", "土"): "生",
        ("土", "金"): "生",
        ("金", "水"): "生",
        ("水", "木"): "生",
        ("金", "木"): "克",
        ("木", "土"): "克",
        ("土", "水"): "克",
        ("水", "火"): "克",
        ("火", "金"): "克",
    }

    # 问题类型对应的解释模板
    QUESTION_TYPES = {
        "事业": {
            "keywords": ["发展", "机遇", "挑战", "决策", "合作"],
            "focus": "事业运势"
        },
        "财运": {
            "keywords": ["财富", "投资", "收益", "风险", "理财"],
            "focus": "财富运势"
        },
        "感情": {
            "keywords": ["关系", "姻缘", "和谐", "沟通", "情感"],
            "focus": "感情运势"
        },
        "健康": {
            "keywords": ["身体", "养生", "调理", "平衡", "休息"],
            "focus": "健康运势"
        }
    }

    def __init__(self, data_loader: Optional[DataLoader] = None):
        """
        初始化卦象分析器

        Args:
            data_loader: 数据加载器实例，默认使用全局单例
        """
        self.data_loader = data_loader or get_data_loader()

    def parse_trigram_input(self, input_str: str) -> Optional[Dict[str, Any]]:
        """
        解析八卦输入（支持名称/方位/数字）

        Args:
            input_str: 输入字符串，可以是：
                - 卦名："乾"、"坤"、"震"等
                - 方位："西北"、"东南"、"北"等
                - 数字："1"、"2"等（1-8）

        Returns:
            八卦数据字典，包含 id, name, symbol, element, direction
            未找到返回 None
        """
        input_str = input_str.strip()

        # 尝试作为数字解析
        try:
            num = int(input_str)
            if 1 <= num <= 8:
                trigram_name = self.TRIGRAM_NUMBERS[num]
                return self.data_loader.get_trigram_by_name(trigram_name)
        except ValueError:
            pass

        # 尝试作为卦名查找
        trigram = self.data_loader.get_trigram_by_name(input_str)
        if trigram:
            return trigram

        # 尝试作为方位查找
        trigrams = self.data_loader.get_trigrams()
        for trigram in trigrams:
            if trigram.get('direction') == input_str:
                return trigram

        return None

    def get_hexagram(
        self,
        upper_trigram: Union[str, Dict],
        lower_trigram: Union[str, Dict]
    ) -> Optional[Dict[str, Any]]:
        """
        根据上下卦获取卦象

        Args:
            upper_trigram: 上卦，可以是卦名字符串或八卦数据字典
            lower_trigram: 下卦，可以是卦名字符串或八卦数据字典

        Returns:
            卦象数据字典，包含 id, name, upper_trigram, lower_trigram,
            judgment_summary, image_summary, element_relation
            未找到返回 None
        """
        # 处理输入格式
        if isinstance(upper_trigram, dict):
            upper_name = upper_trigram['name']
        else:
            upper_name = upper_trigram

        if isinstance(lower_trigram, dict):
            lower_name = lower_trigram['name']
        else:
            lower_name = lower_trigram

        # 查找卦象
        return self.data_loader.get_hexagram_by_trigrams(upper_name, lower_name)

    def analyze_element_relation(self, hexagram: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析卦象的五行关系

        Args:
            hexagram: 卦象数据字典

        Returns:
            五行分析结果，包含：
            - upper_element: 上卦五行
            - lower_element: 下卦五行
            - relation_type: 关系类型（生/克/比和）
            - relation: 关系描述
            - description: 详细说明
        """
        upper_trigram_name = hexagram['upper_trigram']
        lower_trigram_name = hexagram['lower_trigram']

        # 获取上下卦的五行属性，使用辅助方法处理繁简体
        upper_trigram = self._find_trigram_by_name(upper_trigram_name)
        lower_trigram = self._find_trigram_by_name(lower_trigram_name)

        if not upper_trigram or not lower_trigram:
            return {
                'relation': hexagram.get('element_relation', '未知'),
                'relation_type': '未知',
                'description': f'无法获取五行信息 (上卦:{upper_trigram_name}, 下卦:{lower_trigram_name})'
            }

        upper_element = upper_trigram['element']
        lower_element = lower_trigram['element']

        # 分析五行关系 - 需要检查两个方向
        # 先检查下卦对上卦的关系
        lower_to_upper = self._get_element_relation(lower_element, upper_element)
        # 再检查上卦对下卦的关系
        upper_to_lower = self._get_element_relation(upper_element, lower_element)

        # 确定主要关系（优先使用生克关系，其次是比和）
        if lower_to_upper in ['生', '克']:
            relation_type = lower_to_upper
            description = self._generate_element_description(
                lower_element, upper_element, relation_type
            )
        elif upper_to_lower in ['生', '克']:
            relation_type = upper_to_lower
            description = self._generate_element_description(
                upper_element, lower_element, relation_type, reverse=True
            )
        else:
            # 比和关系
            relation_type = lower_to_upper
            description = self._generate_element_description(
                lower_element, upper_element, relation_type
            )

        return {
            'upper_element': upper_element,
            'lower_element': lower_element,
            'relation_type': relation_type,
            'relation': hexagram.get('element_relation', ''),
            'description': description
        }

    def _find_trigram_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        查找八卦，支持繁简体转换

        Args:
            name: 八卦名称

        Returns:
            八卦数据字典，未找到返回 None
        """
        # 繁简体映射
        variant_map = {
            '離': ['離', '离'],
            '离': ['離', '离'],
            '兌': ['兌', '兑'],
            '兑': ['兌', '兑'],
        }

        # 首先尝试直接匹配
        trigram = self.data_loader.get_trigram_by_name(name)
        if trigram:
            return trigram

        # 如果没找到，尝试繁简体变体
        variants = variant_map.get(name, [name])
        for variant in variants:
            trigram = self.data_loader.get_trigram_by_name(variant)
            if trigram:
                return trigram

        return None

    def _get_element_relation(self, element1: str, element2: str) -> str:
        """
        获取两个五行之间的关系

        Args:
            element1: 第一个五行（下卦）
            element2: 第二个五行（上卦）

        Returns:
            关系类型：生/克/比和
        """
        return self.ELEMENT_RELATIONS.get((element1, element2), "未知")

    def _generate_element_description(
        self,
        element1: str,
        element2: str,
        relation_type: str,
        reverse: bool = False
    ) -> str:
        """
        生成五行关系的详细描述

        Args:
            element1: 第一个五行
            element2: 第二个五行
            relation_type: 关系类型
            reverse: 是否为反向关系（上对下）

        Returns:
            详细描述文本
        """
        if relation_type == "比和":
            return f"上下卦五行相同，均为{element1}，气势纯一，力量集中。"
        elif relation_type == "生":
            if reverse:
                return f"上卦{element1}生下卦{element2}，上助下势，有利发展，但需注意上方消耗。"
            else:
                return f"下卦{element1}生上卦{element2}，下助上势，有利发展，但需注意下方消耗。"
        elif relation_type == "克":
            if reverse:
                return f"上卦{element1}克下卦{element2}，上制下势，存在冲突，需谨慎行事。"
            else:
                return f"下卦{element1}克上卦{element2}，下制上势，存在冲突，需谨慎行事。"
        else:
            return "五行关系复杂，需综合分析。"

    def generate_interpretation(
        self,
        hexagram: Dict[str, Any],
        question_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        生成卦辞解释

        Args:
            hexagram: 卦象数据字典
            question_type: 问题类型（事业/财运/感情/健康），可选

        Returns:
            解释结果，包含：
            - hexagram_name: 卦名
            - judgment: 卦辞
            - image: 象辞
            - element_analysis: 五行分析
            - advice: 针对性建议
            - question_type: 问题类型
        """
        # 基础信息
        result = {
            'hexagram_name': hexagram['name'],
            'hexagram_id': hexagram['id'],
            'judgment': hexagram['judgment_summary'],
            'image': hexagram['image_summary'],
        }

        # 五行分析
        element_analysis = self.analyze_element_relation(hexagram)
        result['element_analysis'] = element_analysis

        # 生成针对性建议
        if question_type and question_type in self.QUESTION_TYPES:
            result['question_type'] = question_type
            result['advice'] = self._generate_advice(
                hexagram, element_analysis, question_type
            )
        else:
            result['question_type'] = "通用"
            result['advice'] = self._generate_general_advice(
                hexagram, element_analysis
            )

        return result

    def _generate_advice(
        self,
        hexagram: Dict[str, Any],
        element_analysis: Dict[str, Any],
        question_type: str
    ) -> str:
        """
        根据问题类型生成针对性建议

        Args:
            hexagram: 卦象数据
            element_analysis: 五行分析结果
            question_type: 问题类型

        Returns:
            建议文本
        """
        type_info = self.QUESTION_TYPES[question_type]
        relation_type = element_analysis.get('relation_type', '')

        advice_parts = [f"【{type_info['focus']}】"]

        # 根据五行关系给出建议
        if relation_type == "比和":
            advice_parts.append("当前气势纯正，力量集中。")
            if question_type == "事业":
                advice_parts.append("适合专注主业，发挥专长，稳步推进。")
            elif question_type == "财运":
                advice_parts.append("财运稳定，适合守成，不宜冒险投资。")
            elif question_type == "感情":
                advice_parts.append("关系和谐，双方志同道合，宜珍惜维护。")
            elif question_type == "健康":
                advice_parts.append("身体状态平稳，保持规律作息即可。")

        elif relation_type == "生":
            advice_parts.append("下助上势，有利发展。")
            if question_type == "事业":
                advice_parts.append("适合积极进取，把握机遇，但需注意资源投入。")
            elif question_type == "财运":
                advice_parts.append("财运上升，可适当投资，但要量力而行。")
            elif question_type == "感情":
                advice_parts.append("关系发展顺利，付出会有回报，宜主动表达。")
            elif question_type == "健康":
                advice_parts.append("身体恢复良好，适当调养可增强体质。")

        elif relation_type == "克":
            advice_parts.append("存在冲突制约，需谨慎应对。")
            if question_type == "事业":
                advice_parts.append("遇到阻力，宜以柔克刚，避免正面冲突。")
            elif question_type == "财运":
                advice_parts.append("财运受阻，不宜大额投资，需控制开支。")
            elif question_type == "感情":
                advice_parts.append("关系紧张，需加强沟通，化解矛盾。")
            elif question_type == "健康":
                advice_parts.append("注意身体警示，及时调理，避免过度劳累。")

        # 添加卦象特定建议
        advice_parts.append(f"\n卦象提示：{hexagram['image_summary']}")

        return " ".join(advice_parts)

    def _generate_general_advice(
        self,
        hexagram: Dict[str, Any],
        element_analysis: Dict[str, Any]
    ) -> str:
        """
        生成通用建议

        Args:
            hexagram: 卦象数据
            element_analysis: 五行分析结果

        Returns:
            建议文本
        """
        relation_type = element_analysis.get('relation_type', '')

        advice_parts = ["【综合建议】"]

        if relation_type == "比和":
            advice_parts.append("当前局势稳定，气势纯正。宜坚守正道，稳步前行。")
        elif relation_type == "生":
            advice_parts.append("形势有利发展，宜积极进取，但需注意资源平衡。")
        elif relation_type == "克":
            advice_parts.append("存在制约因素，宜谨慎行事，以智慧化解矛盾。")

        advice_parts.append(f"\n{element_analysis.get('description', '')}")
        advice_parts.append(f"\n象曰：{hexagram['image_summary']}")

        return " ".join(advice_parts)

    def analyze_changing_line(
        self,
        hexagram: Dict[str, Any],
        line_position: int
    ) -> Dict[str, Any]:
        """
        分析变爻

        Args:
            hexagram: 本卦数据
            line_position: 变爻位置（1-6，从下往上数）

        Returns:
            变卦分析结果，包含：
            - original_hexagram: 本卦信息
            - changing_line: 变爻位置
            - changed_hexagram: 变卦信息
            - interpretation: 变化解释
        """
        if not 1 <= line_position <= 6:
            raise ValueError("变爻位置必须在 1-6 之间")

        # 获取本卦的上下卦
        upper_trigram_name = hexagram['upper_trigram']
        lower_trigram_name = hexagram['lower_trigram']

        # 计算变卦
        # 变爻在下卦（1-3爻）
        if line_position <= 3:
            # 下卦需要变化
            changed_lower = self._change_trigram_line(
                lower_trigram_name, line_position
            )
            changed_upper = upper_trigram_name
        else:
            # 上卦需要变化（4-6爻对应上卦的1-3爻）
            changed_upper = self._change_trigram_line(
                upper_trigram_name, line_position - 3
            )
            changed_lower = lower_trigram_name

        # 获取变卦
        changed_hexagram = self.get_hexagram(changed_upper, changed_lower)

        if not changed_hexagram:
            return {
                'original_hexagram': {
                    'id': hexagram['id'],
                    'name': hexagram['name']
                },
                'changing_line': line_position,
                'changed_hexagram': None,
                'interpretation': '无法确定变卦'
            }

        # 生成变化解释
        interpretation = self._generate_changing_interpretation(
            hexagram, changed_hexagram, line_position
        )

        return {
            'original_hexagram': {
                'id': hexagram['id'],
                'name': hexagram['name'],
                'judgment': hexagram['judgment_summary']
            },
            'changing_line': line_position,
            'changed_hexagram': {
                'id': changed_hexagram['id'],
                'name': changed_hexagram['name'],
                'judgment': changed_hexagram['judgment_summary'],
                'upper_trigram': changed_hexagram['upper_trigram'],
                'lower_trigram': changed_hexagram['lower_trigram']
            },
            'interpretation': interpretation
        }

    def _change_trigram_line(self, trigram_name: str, line_position: int) -> str:
        """
        改变八卦中的某一爻

        Args:
            trigram_name: 八卦名称
            line_position: 爻位（1-3）

        Returns:
            变化后的八卦名称
        """
        # 八卦的二进制表示（从下往上，阳爻=1，阴爻=0）
        trigram_binary = {
            "乾": [1, 1, 1],  # ☰
            "兑": [0, 1, 1],  # ☱
            "離": [1, 0, 1],  # ☲
            "震": [0, 0, 1],  # ☳
            "巽": [1, 1, 0],  # ☴
            "坎": [0, 1, 0],  # ☵
            "艮": [1, 0, 0],  # ☶
            "坤": [0, 0, 0],  # ☷
        }

        # 反向映射
        binary_to_trigram = {
            tuple(v): k for k, v in trigram_binary.items()
        }

        # 获取当前八卦的二进制表示
        current = trigram_binary.get(trigram_name, [0, 0, 0]).copy()

        # 改变指定爻（翻转）
        current[line_position - 1] = 1 - current[line_position - 1]

        # 查找对应的八卦
        return binary_to_trigram.get(tuple(current), trigram_name)

    def _generate_changing_interpretation(
        self,
        original: Dict[str, Any],
        changed: Dict[str, Any],
        line_position: int
    ) -> str:
        """
        生成变爻解释

        Args:
            original: 本卦
            changed: 变卦
            line_position: 变爻位置

        Returns:
            解释文本
        """
        position_names = {
            1: "初爻", 2: "二爻", 3: "三爻",
            4: "四爻", 5: "五爻", 6: "上爻"
        }

        interpretation = [
            f"本卦为《{original['name']}》，{position_names[line_position]}发动，",
            f"变为《{changed['name']}》卦。",
            f"\n\n本卦提示：{original['judgment_summary']}",
            f"\n变卦指引：{changed['judgment_summary']}",
            f"\n\n变化意义：从《{original['name']}》到《{changed['name']}》，",
            "表示事态正在发生转变，需要顺应变化，调整策略。"
        ]

        return "".join(interpretation)

    def parse_hexagram_input(self, input_str: str) -> Optional[Dict[str, Any]]:
        """
        解析卦象输入（支持多种格式）

        Args:
            input_str: 输入字符串，可以是：
                - 卦名："乾"、"坤"
                - 上下卦组合："乾上乾下"、"坤上乾下"
                - 卦序号："1"、"64"

        Returns:
            卦象数据字典，未找到返回 None
        """
        input_str = input_str.strip()

        # 尝试作为卦序号解析
        try:
            hexagram_id = int(input_str)
            if 1 <= hexagram_id <= 64:
                return self.data_loader.get_hexagram_by_id(hexagram_id)
        except ValueError:
            pass

        # 尝试作为卦名查找
        hexagram = self.data_loader.get_hexagram_by_name(input_str)
        if hexagram:
            return hexagram

        # 尝试解析上下卦组合格式（格式：上卦名+上+下卦名+下）
        if "上" in input_str and "下" in input_str:
            parts = input_str.split("上")
            if len(parts) == 2:
                upper = parts[0].strip()
                lower = parts[1].replace("下", "").strip()
                # 如果格式是"乾上乾下"，则upper="乾"，lower="乾"
                # 如果格式是"坤上乾下"，则upper="坤"，lower="乾"
                return self.get_hexagram(upper, lower)

        return None
