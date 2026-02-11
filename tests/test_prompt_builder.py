"""
测试Prompt构建器模块
"""

import pytest
from pathlib import Path
from cyberYJ.core.prompt_builder import PromptBuilder
from cyberYJ.utils.data_loader import DataLoader


# 测试数据目录
DATA_DIR = Path(__file__).parent.parent / "data"


class TestPromptBuilder:
    """测试 PromptBuilder 类"""

    def setup_method(self):
        """每个测试方法前执行"""
        self.loader = DataLoader(DATA_DIR)
        self.builder = PromptBuilder(self.loader)

    def test_init(self):
        """测试初始化"""
        assert self.builder.data_loader is not None

    def test_build_analysis_prompt_fortune(self):
        """测试构建命运场景的分析Prompt"""
        prompt = self.builder.build_analysis_prompt(1, 'fortune')

        # 验证Prompt包含必要的部分
        assert '乾' in prompt
        assert '卦象信息' in prompt
        assert '关键词解析' in prompt
        assert '场景分析框架' in prompt
        assert '输出结构要求' in prompt
        assert '分析要求' in prompt
        assert '元亨' in prompt or '利贞' in prompt

    def test_build_analysis_prompt_career(self):
        """测试构建事业场景的分析Prompt"""
        prompt = self.builder.build_analysis_prompt(1, 'career')

        assert '乾' in prompt
        assert '事业' in prompt
        assert '求职者' in prompt or '在职者' in prompt

    def test_build_analysis_prompt_love(self):
        """测试构建感情场景的分析Prompt"""
        prompt = self.builder.build_analysis_prompt(1, 'love')

        assert '乾' in prompt
        assert '感情' in prompt
        assert '单身者' in prompt or '恋爱中' in prompt

    def test_build_analysis_prompt_with_user_question(self):
        """测试构建带用户问题的Prompt"""
        user_question = "我最近工作不顺，想知道是否适合跳槽？"
        prompt = self.builder.build_analysis_prompt(1, 'career', user_question)

        assert user_question in prompt
        assert '用户问题' in prompt

    def test_build_analysis_prompt_invalid_hexagram(self):
        """测试无效的卦象ID"""
        with pytest.raises(ValueError, match="卦象ID .* 不存在"):
            self.builder.build_analysis_prompt(999, 'fortune')

    def test_build_analysis_prompt_invalid_scenario(self):
        """测试无效的场景代码"""
        with pytest.raises(ValueError, match="场景 .* 不存在"):
            self.builder.build_analysis_prompt(1, 'nonexistent')

    def test_extract_keywords(self):
        """测试关键词提取"""
        judgment = "元亨，利贞。"
        keywords = self.builder._extract_keywords(judgment)

        assert '元亨' in keywords
        assert '利贞' in keywords

    def test_extract_keywords_complex(self):
        """测试复杂卦辞的关键词提取"""
        judgment = "元亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞，吉。"
        keywords = self.builder._extract_keywords(judgment)

        assert '元亨' in keywords
        assert '利西南' in keywords
        assert '有攸往' in keywords
        assert '先迷后得' in keywords
        assert '吉' in keywords

    def test_build_simple_prompt(self):
        """测试构建简单Prompt"""
        prompt = self.builder.build_simple_prompt(1)

        assert '乾' in prompt
        assert '卦辞' in prompt
        assert '象辞' in prompt
        assert '五行关系' in prompt

    def test_build_simple_prompt_with_question_type(self):
        """测试构建带问题类型的简单Prompt"""
        prompt = self.builder.build_simple_prompt(1, '事业')

        assert '乾' in prompt
        assert '事业' in prompt

    def test_build_simple_prompt_invalid_hexagram(self):
        """测试简单Prompt的无效卦象ID"""
        with pytest.raises(ValueError, match="卦象ID .* 不存在"):
            self.builder.build_simple_prompt(999)

    def test_build_hexagram_info(self):
        """测试构建卦象信息"""
        hexagram = self.loader.get_hexagram_by_id(1)
        info = self.builder._build_hexagram_info(hexagram)

        assert '乾' in info
        assert '卦辞' in info
        assert '象辞' in info

    def test_build_keywords_analysis(self):
        """测试构建关键词解析"""
        hexagram = self.loader.get_hexagram_by_id(1)
        scenario_data = self.loader.get_scenario_data('fortune')

        analysis = self.builder._build_keywords_analysis(hexagram, scenario_data)

        # 乾卦的卦辞包含"元亨"和"利贞"
        assert len(analysis) > 0

    def test_build_scenario_framework(self):
        """测试构建场景框架"""
        scenario_data = self.loader.get_scenario_data('fortune')
        scenario_hexagram = self.loader.get_scenario_hexagram('fortune', 1)

        framework = self.builder._build_scenario_framework(scenario_data, scenario_hexagram)

        assert '命运' in framework
        assert '分析维度' in framework

    def test_build_output_structure(self):
        """测试构建输出结构"""
        scenario_data = self.loader.get_scenario_data('fortune')

        structure = self.builder._build_output_structure(scenario_data)

        assert '输出分析结果' in structure or '结构' in structure

    def test_build_requirements(self):
        """测试构建分析要求"""
        scenario_data = self.loader.get_scenario_data('fortune')

        requirements = self.builder._build_requirements(scenario_data)

        assert '分析重点' in requirements
        assert '输出要求' in requirements

    def test_prompt_completeness(self):
        """测试Prompt的完整性"""
        prompt = self.builder.build_analysis_prompt(39, 'love')

        # 验证所有关键部分都存在
        required_parts = [
            '卦象信息',
            '关键词解析',
            '场景分析框架',
            '输出结构要求',
            '分析要求'
        ]

        for part in required_parts:
            assert part in prompt, f"Prompt缺少必要部分: {part}"

    def test_different_hexagrams(self):
        """测试不同卦象的Prompt构建"""
        hexagram_ids = [1, 2, 11, 12, 39]

        for hex_id in hexagram_ids:
            prompt = self.builder.build_analysis_prompt(hex_id, 'fortune')
            assert len(prompt) > 0
            assert f'第{hex_id}卦' in prompt


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
