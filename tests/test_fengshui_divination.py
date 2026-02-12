"""
测试风水占卜工具
"""

import pytest
from datetime import datetime
from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool


class TestFengshuiDivinationTool:
    """测试风水占卜工具"""

    def setup_method(self):
        """每个测试方法前执行"""
        self.tool = FengshuiDivinationTool()

    def test_basic_divination(self):
        """测试基本占卜功能"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="乾"
        )

        assert result is not None
        assert 'main_hexagram' in result
        assert result['main_hexagram']['name'] == '乾'
        assert result['main_hexagram']['id'] == 1
        assert 'judgment' in result['main_hexagram']
        assert 'five_elements' in result
        assert 'solar_term_influence' in result
        assert 'fortune_advice' in result
        assert 'trace' in result
        assert len(result['trace']) > 0

    def test_divination_with_question_type(self):
        """测试带问题类型的占卜"""
        for question_type in ['事业', '财运', '感情', '健康']:
            result = self.tool.execute(
                upper_trigram="坤",
                lower_trigram="乾",
                question_type=question_type
            )

            assert result is not None
            # 检查问题类型是否在 trace 中
            trace_text = ' '.join(result['trace'])
            assert question_type in trace_text

    def test_divination_with_changing_line(self):
        """测试带变爻的占卜"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="乾",
            changing_line=1
        )

        assert result is not None
        assert 'changing_hexagram' in result
        assert 'do_dont' in result
        assert 'do' in result['do_dont']
        assert 'dont' in result['do_dont']
        assert len(result['do_dont']['do']) > 0
        assert len(result['do_dont']['dont']) > 0

    def test_divination_with_timestamp(self):
        """测试指定时间的占卜"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="坤",
            timestamp="2024-02-04T10:00:00+08:00"
        )

        assert result is not None
        assert '2024-02-04' in result['trace'][0]

    def test_divination_with_direction_input(self):
        """测试使用方位输入"""
        result = self.tool.execute(
            upper_trigram="西北",
            lower_trigram="西南"
        )

        assert result is not None
        assert result['main_hexagram']['name'] == '否'

    def test_divination_with_number_input(self):
        """测试使用数字输入"""
        result = self.tool.execute(
            upper_trigram="1",  # 乾
            lower_trigram="1"   # 乾
        )

        assert result is not None
        assert result['main_hexagram']['name'] == '乾'

    def test_hexagram_symbol(self):
        """测试卦象符号生成"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="乾"
        )

        assert 'symbol' in result['main_hexagram']
        assert result['main_hexagram']['symbol'] == '䷀'

    def test_invalid_upper_trigram(self):
        """测试无效的上卦输入"""
        with pytest.raises(ValueError, match="上卦解析失败"):
            self.tool.execute(
                upper_trigram="无效卦名",
                lower_trigram="乾"
            )

    def test_invalid_lower_trigram(self):
        """测试无效的下卦输入"""
        with pytest.raises(ValueError, match="下卦解析失败"):
            self.tool.execute(
                upper_trigram="乾",
                lower_trigram="无效卦名"
            )

    def test_invalid_changing_line(self):
        """测试无效的变爻位置"""
        with pytest.raises(ValueError, match="变爻位置必须在 1-6 之间"):
            self.tool.execute(
                upper_trigram="乾",
                lower_trigram="乾",
                changing_line=7
            )

    def test_invalid_timestamp(self):
        """测试无效的时间戳"""
        with pytest.raises(ValueError, match="时间戳格式错误"):
            self.tool.execute(
                upper_trigram="乾",
                lower_trigram="乾",
                timestamp="invalid-timestamp"
            )

    def test_all_64_hexagrams(self):
        """测试主要卦象都能正常占卜"""
        # 测试一些代表性的卦象组合
        test_cases = [
            ('乾', '乾'),  # 纯阳
            ('坤', '坤'),  # 纯阴
            ('乾', '坤'),  # 否卦
            ('坤', '乾'),  # 泰卦
            ('震', '坎'),  # 屯卦
            ('坎', '震'),  # 解卦
        ]

        for upper, lower in test_cases:
            result = self.tool.execute(
                upper_trigram=upper,
                lower_trigram=lower
            )
            assert result is not None
            assert 'main_hexagram' in result

    def test_do_dont_generation(self):
        """测试宜忌建议生成"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="乾",
            changing_line=1
        )

        assert 'do_dont' in result
        do_list = result['do_dont']['do']
        dont_list = result['do_dont']['dont']

        assert isinstance(do_list, list)
        assert isinstance(dont_list, list)
        assert len(do_list) > 0
        assert len(dont_list) > 0
        assert len(do_list) <= 5
        assert len(dont_list) <= 5

    def test_sources_included(self):
        """测试来源信息包含"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="乾"
        )

        assert 'sources' in result
        assert isinstance(result['sources'], list)
        assert len(result['sources']) > 0

    def test_authoritative_mapping_scenario_specific_note(self, monkeypatch):
        """测试场景字段级权威映射写入 authoritative_notes"""
        monkeypatch.setattr(
            self.tool.data_loader,
            "get_authoritative_text_map",
            lambda: {
                "version": "1.0.0",
                "items": [
                    {
                        "field_path": "data.scenarios.career.hexagrams['11'].scenario_specific.求职.situation",
                        "text_kind": "summary",
                        "license": "summary_only",
                        "content": "求职建议需结合行业周期与岗位要求综合判断。",
                        "source_ref": ["ctext_yijing", "convention"]
                    }
                ]
            }
        )

        result = self.tool.execute(
            upper_trigram="坤",
            lower_trigram="乾",
            question_type="事业",
            timestamp="2026-02-11T10:00:00+08:00"
        )

        assert "authoritative_notes" in result
        assert (
            result["authoritative_notes"]["scenario_specific.求职.situation"] ==
            "求职建议需结合行业周期与岗位要求综合判断。"
        )
        assert any(
            "权威补充: data.scenarios.career.hexagrams['11'].scenario_specific.求职.situation" in step
            for step in result["trace"]
        )

    def test_authoritative_mapping_judgment_replacement(self, monkeypatch):
        """测试卦辞字段映射仍保持替换逻辑"""
        monkeypatch.setattr(
            self.tool.data_loader,
            "get_authoritative_text_map",
            lambda: {
                "version": "1.0.0",
                "items": [
                    {
                        "field_path": "hexagrams[?(@.id==11)].judgment_summary",
                        "text_kind": "summary",
                        "license": "summary_only",
                        "content": "小往大来，吉亨（授权摘要版）",
                        "source_ref": ["ctext_yijing"]
                    }
                ]
            }
        )

        result = self.tool.execute(
            upper_trigram="坤",
            lower_trigram="乾",
            question_type="事业",
            timestamp="2026-02-11T10:00:00+08:00"
        )

        assert result["main_hexagram"]["judgment"] == "小往大来，吉亨（授权摘要版）"
        assert any(
            "权威映射: hexagrams[?(@.id==11)].judgment_summary" in step
            for step in result["trace"]
        )

    def test_authoritative_mapping_scenario_wildcard_note(self, monkeypatch):
        """测试场景 wildcard 映射写入 authoritative_notes"""
        monkeypatch.setattr(
            self.tool.data_loader,
            "get_authoritative_text_map",
            lambda: {
                "version": "1.0.0",
                "items": [
                    {
                        "field_path": "data.scenarios.career.hexagrams[*].overall_tendency",
                        "text_kind": "summary",
                        "license": "summary_only",
                        "content": "事业趋势应结合行业周期与组织阶段综合研判。",
                        "source_ref": ["ctext_yijing", "convention"]
                    },
                    {
                        "field_path": "data.scenarios.career.hexagrams[*].scenario_specific[*].advice",
                        "text_kind": "summary",
                        "license": "summary_only",
                        "content": "行动建议应按目标拆解并分阶段验证。",
                        "source_ref": ["ctext_yijing", "convention"]
                    }
                ]
            }
        )

        result = self.tool.execute(
            upper_trigram="坤",
            lower_trigram="乾",
            question_type="事业",
            timestamp="2026-02-11T10:00:00+08:00"
        )

        assert "authoritative_notes" in result
        assert (
            result["authoritative_notes"]["scenario_analysis.overall_tendency"] ==
            "事业趋势应结合行业周期与组织阶段综合研判。"
        )
        assert (
            result["authoritative_notes"]["scenario_specific.*.advice"] ==
            "行动建议应按目标拆解并分阶段验证。"
        )

    def test_trace_completeness(self):
        """测试推导路径完整性"""
        result = self.tool.execute(
            upper_trigram="乾",
            lower_trigram="坤",
            question_type="事业",
            changing_line=3
        )

        trace = result['trace']
        assert len(trace) >= 7  # 至少包含：时间、上卦、下卦、本卦、五行、节气、问题类型

        # 检查关键信息是否在 trace 中
        trace_text = ' '.join(trace)
        assert '上卦解析' in trace_text
        assert '下卦解析' in trace_text
        assert '本卦' in trace_text
        assert '五行关系' in trace_text
        assert '当前节气' in trace_text


class TestFengshuiDivinationIntegration:
    """集成测试"""

    def test_complete_divination_workflow(self):
        """测试完整的占卜流程"""
        tool = FengshuiDivinationTool()

        # 场景：问事业，得乾卦，初爻变
        result = tool.execute(
            upper_trigram="西北",  # 乾
            lower_trigram="西北",  # 乾
            question_type="事业",
            changing_line=1,
            timestamp="2024-03-20T10:00:00+08:00"
        )

        # 验证完整性
        assert result['main_hexagram']['name'] == '乾'
        assert '事业' in str(result['trace'])
        assert 'changing_hexagram' in result
        # 乾卦初爻变，验证变卦存在即可
        assert result['changing_hexagram']['name'] is not None
        assert 'do_dont' in result
        assert '自强不息' in str(result['do_dont']['do'])


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
