"""
Prompt构建器模块

根据卦象、场景、模板动态构建分析Prompt，整合关键词解析和场景框架。
"""

from typing import Dict, List, Any, Optional
from ..utils.data_loader import DataLoader, get_data_loader


class PromptBuilder:
    """Prompt构建器，负责动态构建卦象分析Prompt"""

    def __init__(self, data_loader: Optional[DataLoader] = None):
        """
        初始化Prompt构建器

        Args:
            data_loader: 数据加载器实例，默认使用全局单例
        """
        self.data_loader = data_loader or get_data_loader()

    def build_analysis_prompt(
        self,
        hexagram_id: int,
        scenario_code: str,
        user_question: Optional[str] = None
    ) -> str:
        """
        构建卦象分析Prompt

        Args:
            hexagram_id: 卦象ID（1-64）
            scenario_code: 场景代码（如"fortune"、"career"、"love"）
            user_question: 用户问题描述（可选）

        Returns:
            构建好的Prompt字符串
        """
        # 1. 获取基础数据
        hexagram = self.data_loader.get_hexagram_by_id(hexagram_id)
        if not hexagram:
            raise ValueError(f"卦象ID {hexagram_id} 不存在")

        scenario_data = self.data_loader.get_scenario_data(scenario_code)
        if not scenario_data:
            raise ValueError(f"场景 {scenario_code} 不存在")

        scenario_hexagram = self.data_loader.get_scenario_hexagram(scenario_code, hexagram_id)

        # 2. 构建Prompt各部分
        system_role = self._build_system_role(scenario_data)
        hexagram_info = self._build_hexagram_info(hexagram)
        keywords_analysis = self._build_keywords_analysis(hexagram, scenario_data)
        scenario_framework = self._build_scenario_framework(scenario_data, scenario_hexagram)
        output_structure = self._build_output_structure(scenario_data)
        requirements = self._build_requirements(scenario_data)

        # 3. 组装完整Prompt
        prompt_parts = [
            system_role,
            "",
            "# 卦象信息",
            hexagram_info,
            "",
            "# 关键词解析",
            keywords_analysis,
            "",
            "# 场景分析框架",
            scenario_framework,
            "",
            "# 输出结构要求",
            output_structure,
            "",
            "# 分析要求",
            requirements
        ]

        if user_question:
            prompt_parts.extend([
                "",
                "# 用户问题",
                user_question
            ])

        return "\n".join(prompt_parts)

    def _build_system_role(self, scenario_data: Dict[str, Any]) -> str:
        """构建系统角色描述"""
        prompt_template = scenario_data.get('prompt_template', {})
        system_role = prompt_template.get('system_role', '你是一位精通易经的大师。')
        return system_role

    def _build_hexagram_info(self, hexagram: Dict[str, Any]) -> str:
        """构建卦象基本信息"""
        lines = [
            f"- **卦名**：第{hexagram['id']}卦 {hexagram['name']}卦",
            f"- **卦象**：上卦{hexagram['upper_trigram']}，下卦{hexagram['lower_trigram']}",
            f"- **卦辞**：{hexagram['judgment_summary']}",
            f"- **象辞**：{hexagram['image_summary']}",
            f"- **五行关系**：{hexagram['element_relation']}"
        ]
        return "\n".join(lines)

    def _build_keywords_analysis(
        self,
        hexagram: Dict[str, Any],
        scenario_data: Dict[str, Any]
    ) -> str:
        """构建关键词解析"""
        # 从卦辞中提取关键词
        judgment = hexagram.get('judgment_summary', '')
        keywords = self._extract_keywords(judgment)

        if not keywords:
            return "（本卦无特殊关键词需要解析）"

        scenario_name = scenario_data.get('scenario_info', {}).get('name', '')
        lines = []

        for keyword in keywords:
            keyword_data = self.data_loader.get_keyword_by_name(keyword)
            if keyword_data:
                lines.append(f"**{keyword}**：")
                lines.append(f"- 字面意思：{keyword_data.get('literal', '')}")
                lines.append(f"- 象征意义：{keyword_data.get('symbolic', '')}")

                # 获取场景应用
                application = keyword_data.get('scenario_applications', {}).get(scenario_name)
                if application:
                    lines.append(f"- 在{scenario_name}中的应用：{application}")
                lines.append("")

        return "\n".join(lines) if lines else "（本卦无特殊关键词需要解析）"

    def _extract_keywords(self, judgment: str) -> List[str]:
        """从卦辞中提取关键词"""
        # 常见关键词列表
        common_keywords = [
            "元亨", "利贞", "利西南", "不利东北", "利见大人", "贞吉",
            "勿用", "有攸往", "无攸利", "先迷后得", "利涉大川", "不利涉大川",
            "无咎", "悔亡", "终吉", "凶", "吉"
        ]

        found_keywords = []
        for keyword in common_keywords:
            if keyword in judgment:
                found_keywords.append(keyword)

        return found_keywords

    def _build_scenario_framework(
        self,
        scenario_data: Dict[str, Any],
        scenario_hexagram: Optional[Dict[str, Any]]
    ) -> str:
        """构建场景分析框架"""
        framework = scenario_data.get('analysis_framework', {})
        scenario_info = scenario_data.get('scenario_info', {})

        lines = [
            f"**场景**：{scenario_info.get('name', '')}",
            f"**分析维度**：{', '.join(framework.get('dimensions', []))}",
            f"**关注重点**：{framework.get('focus', '')}",
            ""
        ]

        # 如果有场景卦象数据，添加关键点
        if scenario_hexagram:
            lines.append("**本卦在此场景的关键点**：")
            for point in scenario_hexagram.get('key_points', []):
                lines.append(f"- {point}")
            lines.append("")

        # 添加子场景
        sub_scenarios = scenario_info.get('sub_scenarios', [])
        if sub_scenarios:
            lines.append(f"**需要分析的子场景**：{', '.join(sub_scenarios)}")

        return "\n".join(lines)

    def _build_output_structure(self, scenario_data: Dict[str, Any]) -> str:
        """构建输出结构要求"""
        output_structure = scenario_data.get('output_structure', {})
        sections = output_structure.get('sections', [])

        if not sections:
            return "请按照标准结构输出分析结果。"

        lines = ["请按照以下结构输出分析结果：", ""]

        for i, section in enumerate(sections, 1):
            title = section.get('title', '')
            section_type = section.get('type', '')
            required = "（必需）" if section.get('required', False) else "（可选）"

            lines.append(f"{i}. **{title}** {required}")

            # 添加详细说明
            if section_type == 'scenarios':
                scenarios = section.get('scenarios', [])
                lines.append(f"   - 针对以下人群分别分析：{', '.join(scenarios)}")
                each_includes = section.get('each_includes', [])
                if each_includes:
                    lines.append(f"   - 每个人群包含：{', '.join(each_includes)}")

            elif section_type == 'advice':
                format_info = section.get('format', {})
                lines.append(f"   - 格式：{format_info}")

            lines.append("")

        return "\n".join(lines)

    def _build_requirements(self, scenario_data: Dict[str, Any]) -> str:
        """构建分析要求"""
        prompt_template = scenario_data.get('prompt_template', {})

        lines = ["**分析重点**："]
        for focus in prompt_template.get('analysis_focus', []):
            lines.append(f"- {focus}")

        lines.append("")
        lines.append("**输出要求**：")
        for req in prompt_template.get('output_requirements', []):
            lines.append(f"- {req}")

        return "\n".join(lines)

    def build_simple_prompt(
        self,
        hexagram_id: int,
        question_type: Optional[str] = None
    ) -> str:
        """
        构建简单Prompt（用于向后兼容）

        Args:
            hexagram_id: 卦象ID（1-64）
            question_type: 问题类型（可选）

        Returns:
            简单的Prompt字符串
        """
        hexagram = self.data_loader.get_hexagram_by_id(hexagram_id)
        if not hexagram:
            raise ValueError(f"卦象ID {hexagram_id} 不存在")

        prompt = f"""请分析第{hexagram['id']}卦 {hexagram['name']}卦。

卦辞：{hexagram['judgment_summary']}
象辞：{hexagram['image_summary']}
五行关系：{hexagram['element_relation']}
"""

        if question_type:
            prompt += f"\n请重点分析{question_type}方面的运势。"

        return prompt
