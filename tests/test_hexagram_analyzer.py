"""
测试卦象分析器模块
"""

import pytest
from cyberYJ.core.hexagram_analyzer import HexagramAnalyzer
from cyberYJ.utils.data_loader import get_data_loader


@pytest.fixture
def analyzer():
    """创建卦象分析器实例"""
    return HexagramAnalyzer()


@pytest.fixture
def data_loader():
    """创建数据加载器实例"""
    return get_data_loader()


class TestTrigramInputParsing:
    """测试八卦输入解析"""

    def test_parse_by_name(self, analyzer):
        """测试通过卦名解析"""
        trigram = analyzer.parse_trigram_input("乾")
        assert trigram is not None
        assert trigram['name'] == "乾"
        assert trigram['element'] == "金"
        assert trigram['direction'] == "西北"

    def test_parse_by_direction(self, analyzer):
        """测试通过方位解析"""
        trigram = analyzer.parse_trigram_input("西北")
        assert trigram is not None
        assert trigram['name'] == "乾"
        assert trigram['direction'] == "西北"

    def test_parse_by_number(self, analyzer):
        """测试通过数字解析"""
        # 1 = 乾
        trigram = analyzer.parse_trigram_input("1")
        assert trigram is not None
        assert trigram['name'] == "乾"

        # 8 = 坤
        trigram = analyzer.parse_trigram_input("8")
        assert trigram is not None
        assert trigram['name'] == "坤"

    def test_parse_all_trigrams_by_number(self, analyzer):
        """测试所有八卦数字解析"""
        expected = {
            1: "乾", 2: "兌", 3: "離", 4: "震",
            5: "巽", 6: "坎", 7: "艮", 8: "坤"
        }
        for num, name in expected.items():
            trigram = analyzer.parse_trigram_input(str(num))
            assert trigram is not None
            assert trigram['name'] == name

    def test_parse_invalid_input(self, analyzer):
        """测试无效输入"""
        assert analyzer.parse_trigram_input("无效") is None
        assert analyzer.parse_trigram_input("0") is None
        assert analyzer.parse_trigram_input("9") is None
        assert analyzer.parse_trigram_input("") is None

    def test_parse_with_whitespace(self, analyzer):
        """测试带空格的输入"""
        trigram = analyzer.parse_trigram_input("  乾  ")
        assert trigram is not None
        assert trigram['name'] == "乾"


class TestHexagramQuery:
    """测试卦象查询"""

    def test_get_hexagram_by_names(self, analyzer):
        """测试通过卦名获取卦象"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        assert hexagram is not None
        assert hexagram['id'] == 1
        assert hexagram['name'] == "乾"
        assert hexagram['upper_trigram'] == "乾"
        assert hexagram['lower_trigram'] == "乾"

    def test_get_hexagram_by_dict(self, analyzer):
        """测试通过字典获取卦象"""
        upper = analyzer.parse_trigram_input("乾")
        lower = analyzer.parse_trigram_input("坤")
        hexagram = analyzer.get_hexagram(upper, lower)
        assert hexagram is not None
        assert hexagram['name'] == "否"
        assert hexagram['id'] == 12

    def test_get_hexagram_mixed_input(self, analyzer):
        """测试混合输入格式"""
        upper = analyzer.parse_trigram_input("西北")  # 乾
        hexagram = analyzer.get_hexagram(upper, "坤")
        assert hexagram is not None
        assert hexagram['name'] == "否"

    def test_get_all_pure_hexagrams(self, analyzer):
        """测试所有纯卦（上下卦相同）"""
        # 使用实际数据中的字符
        pure_hexagrams = [
            ("乾", "乾", "乾"),
            ("坤", "坤", "坤"),
            ("震", "震", "震"),
            ("巽", "巽", "巽"),
            ("坎", "坎", "坎"),
            ("離", "離", "离"),
            ("艮", "艮", "艮"),
            ("兑", "兑", "兑"),
        ]
        for upper, lower, expected_name in pure_hexagrams:
            hexagram = analyzer.get_hexagram(upper, lower)
            assert hexagram is not None, f"Failed to find hexagram for {upper}/{lower}"
            assert hexagram['name'] == expected_name

    def test_get_hexagram_not_found(self, analyzer):
        """测试查询不存在的卦象"""
        # 使用无效的卦名
        hexagram = analyzer.get_hexagram("无效", "无效")
        assert hexagram is None


class TestElementAnalysis:
    """测试五行分析"""

    def test_analyze_same_element(self, analyzer):
        """测试相同五行（比和）"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        analysis = analyzer.analyze_element_relation(hexagram)

        assert analysis['upper_element'] == "金"
        assert analysis['lower_element'] == "金"
        assert analysis['relation_type'] == "比和"
        assert "比和" in analysis['relation']

    def test_analyze_generating_relation(self, analyzer):
        """测试相生关系"""
        # 木生火：震（木）下，離（火）上
        hexagram = analyzer.get_hexagram("離", "震")
        analysis = analyzer.analyze_element_relation(hexagram)

        assert analysis['lower_element'] == "木"
        assert analysis['upper_element'] == "火"
        assert analysis['relation_type'] == "生"
        assert "生" in analysis['description']

    def test_analyze_controlling_relation(self, analyzer):
        """测试相克关系"""
        # 金克木：乾（金）下，震（木）上
        hexagram = analyzer.get_hexagram("震", "乾")
        analysis = analyzer.analyze_element_relation(hexagram)

        assert analysis['lower_element'] == "金"
        assert analysis['upper_element'] == "木"
        assert analysis['relation_type'] == "克"
        assert "克" in analysis['description'] or "制" in analysis['description']

    def test_analyze_all_generating_cycles(self, analyzer):
        """测试所有相生关系"""
        generating_pairs = [
            ("震", "離", "木", "火"),  # 木生火
            ("離", "坤", "火", "土"),  # 火生土
            ("坤", "乾", "土", "金"),  # 土生金
            ("乾", "坎", "金", "水"),  # 金生水
            ("坎", "震", "水", "木"),  # 水生木
        ]

        for lower, upper, lower_elem, upper_elem in generating_pairs:
            hexagram = analyzer.get_hexagram(upper, lower)
            analysis = analyzer.analyze_element_relation(hexagram)
            assert analysis['lower_element'] == lower_elem
            assert analysis['upper_element'] == upper_elem
            assert analysis['relation_type'] == "生"

    def test_analyze_all_controlling_cycles(self, analyzer):
        """测试所有相克关系"""
        controlling_pairs = [
            ("乾", "震", "金", "木"),  # 金克木
            ("震", "坤", "木", "土"),  # 木克土
            ("坤", "坎", "土", "水"),  # 土克水
            ("坎", "離", "水", "火"),  # 水克火
            ("離", "乾", "火", "金"),  # 火克金
        ]

        for lower, upper, lower_elem, upper_elem in controlling_pairs:
            hexagram = analyzer.get_hexagram(upper, lower)
            analysis = analyzer.analyze_element_relation(hexagram)
            assert analysis['lower_element'] == lower_elem
            assert analysis['upper_element'] == upper_elem
            assert analysis['relation_type'] == "克"


class TestInterpretationGeneration:
    """测试卦辞解释生成"""

    def test_generate_general_interpretation(self, analyzer):
        """测试生成通用解释"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        interpretation = analyzer.generate_interpretation(hexagram)

        assert interpretation['hexagram_name'] == "乾"
        assert interpretation['hexagram_id'] == 1
        assert interpretation['judgment'] == "元亨，利贞。"
        assert interpretation['image'] == "天行健，君子以自强不息。"
        assert 'element_analysis' in interpretation
        assert interpretation['question_type'] == "通用"
        assert 'advice' in interpretation

    def test_generate_career_interpretation(self, analyzer):
        """测试生成事业解释"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        interpretation = analyzer.generate_interpretation(hexagram, "事业")

        assert interpretation['question_type'] == "事业"
        assert '事业运势' in interpretation['advice']

    def test_generate_wealth_interpretation(self, analyzer):
        """测试生成财运解释"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        interpretation = analyzer.generate_interpretation(hexagram, "财运")

        assert interpretation['question_type'] == "财运"
        assert '财富运势' in interpretation['advice']

    def test_generate_relationship_interpretation(self, analyzer):
        """测试生成感情解释"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        interpretation = analyzer.generate_interpretation(hexagram, "感情")

        assert interpretation['question_type'] == "感情"
        assert '感情运势' in interpretation['advice']

    def test_generate_health_interpretation(self, analyzer):
        """测试生成健康解释"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        interpretation = analyzer.generate_interpretation(hexagram, "健康")

        assert interpretation['question_type'] == "健康"
        assert '健康运势' in interpretation['advice']

    def test_interpretation_includes_element_analysis(self, analyzer):
        """测试解释包含五行分析"""
        hexagram = analyzer.get_hexagram("離", "震")  # 木生火
        interpretation = analyzer.generate_interpretation(hexagram, "事业")

        element_analysis = interpretation['element_analysis']
        assert element_analysis['relation_type'] == "生"
        # 建议中应该包含相关的积极词汇
        assert '进取' in interpretation['advice'] or '发展' in interpretation['advice']

    def test_interpretation_for_conflicting_elements(self, analyzer):
        """测试相克五行的解释"""
        hexagram = analyzer.get_hexagram("震", "乾")  # 金克木
        interpretation = analyzer.generate_interpretation(hexagram, "事业")

        element_analysis = interpretation['element_analysis']
        assert element_analysis['relation_type'] == "克"
        assert '阻力' in interpretation['advice'] or '谨慎' in interpretation['advice']


class TestChangingLineAnalysis:
    """测试变爻分析"""

    def test_analyze_first_line_change(self, analyzer):
        """测试初爻变化"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        result = analyzer.analyze_changing_line(hexagram, 1)

        assert result['original_hexagram']['name'] == "乾"
        assert result['changing_line'] == 1
        assert result['changed_hexagram'] is not None
        assert 'interpretation' in result

    def test_analyze_all_line_changes(self, analyzer):
        """测试所有爻位变化"""
        hexagram = analyzer.get_hexagram("乾", "乾")

        for line in range(1, 7):
            result = analyzer.analyze_changing_line(hexagram, line)
            assert result['changing_line'] == line
            assert result['changed_hexagram'] is not None

    def test_changing_line_creates_different_hexagram(self, analyzer):
        """测试变爻产生不同卦象"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        result = analyzer.analyze_changing_line(hexagram, 1)

        # 乾卦初爻变应该变成姤卦
        assert result['original_hexagram']['id'] != result['changed_hexagram']['id']

    def test_invalid_line_position(self, analyzer):
        """测试无效的爻位"""
        hexagram = analyzer.get_hexagram("乾", "乾")

        with pytest.raises(ValueError):
            analyzer.analyze_changing_line(hexagram, 0)

        with pytest.raises(ValueError):
            analyzer.analyze_changing_line(hexagram, 7)

    def test_changing_line_interpretation_content(self, analyzer):
        """测试变爻解释内容"""
        hexagram = analyzer.get_hexagram("乾", "乾")
        result = analyzer.analyze_changing_line(hexagram, 1)

        interpretation = result['interpretation']
        assert "乾" in interpretation
        assert "变为" in interpretation
        assert result['changed_hexagram']['name'] in interpretation

    def test_lower_trigram_changes(self, analyzer):
        """测试下卦变化（1-3爻）"""
        hexagram = analyzer.get_hexagram("乾", "坤")

        # 测试下卦的三个爻
        for line in [1, 2, 3]:
            result = analyzer.analyze_changing_line(hexagram, line)
            assert result['changed_hexagram'] is not None
            # 上卦应该保持不变
            assert result['changed_hexagram']['upper_trigram'] == "乾"

    def test_upper_trigram_changes(self, analyzer):
        """测试上卦变化（4-6爻）"""
        hexagram = analyzer.get_hexagram("乾", "坤")

        # 测试上卦的三个爻
        for line in [4, 5, 6]:
            result = analyzer.analyze_changing_line(hexagram, line)
            assert result['changed_hexagram'] is not None
            # 下卦应该保持不变
            assert result['changed_hexagram']['lower_trigram'] == "坤"


class TestHexagramInputParsing:
    """测试卦象输入解析"""

    def test_parse_by_name(self, analyzer):
        """测试通过卦名解析"""
        hexagram = analyzer.parse_hexagram_input("乾")
        assert hexagram is not None
        assert hexagram['name'] == "乾"
        assert hexagram['id'] == 1

    def test_parse_by_id(self, analyzer):
        """测试通过序号解析"""
        hexagram = analyzer.parse_hexagram_input("1")
        assert hexagram is not None
        assert hexagram['name'] == "乾"
        assert hexagram['id'] == 1

        hexagram = analyzer.parse_hexagram_input("64")
        assert hexagram is not None
        assert hexagram['name'] == "未济"
        assert hexagram['id'] == 64

    def test_parse_by_trigram_combination(self, analyzer):
        """测试通过上下卦组合解析"""
        hexagram = analyzer.parse_hexagram_input("乾上乾下")
        assert hexagram is not None
        assert hexagram['name'] == "乾"

        # 坤上乾下 = 上卦坤，下卦乾 = 泰卦
        hexagram = analyzer.parse_hexagram_input("坤上乾下")
        assert hexagram is not None
        assert hexagram['name'] == "泰"

    def test_parse_invalid_hexagram_input(self, analyzer):
        """测试无效卦象输入"""
        assert analyzer.parse_hexagram_input("无效") is None
        assert analyzer.parse_hexagram_input("0") is None
        assert analyzer.parse_hexagram_input("65") is None

    def test_parse_with_whitespace(self, analyzer):
        """测试带空格的输入"""
        hexagram = analyzer.parse_hexagram_input("  乾  ")
        assert hexagram is not None
        assert hexagram['name'] == "乾"


class TestIntegration:
    """集成测试"""

    def test_complete_divination_workflow(self, analyzer):
        """测试完整占卜流程"""
        # 1. 解析输入
        upper = analyzer.parse_trigram_input("西北")
        lower = analyzer.parse_trigram_input("西南")

        assert upper['name'] == "乾"
        assert lower['name'] == "坤"

        # 2. 获取卦象
        hexagram = analyzer.get_hexagram(upper, lower)
        assert hexagram['name'] == "否"

        # 3. 五行分析
        element_analysis = analyzer.analyze_element_relation(hexagram)
        assert element_analysis['relation_type'] == "生"

        # 4. 生成解释
        interpretation = analyzer.generate_interpretation(hexagram, "事业")
        assert interpretation['question_type'] == "事业"
        assert 'advice' in interpretation

        # 5. 变爻分析
        changing_result = analyzer.analyze_changing_line(hexagram, 1)
        assert changing_result['changed_hexagram'] is not None

    def test_multiple_question_types(self, analyzer):
        """测试多种问题类型"""
        hexagram = analyzer.get_hexagram("乾", "乾")

        question_types = ["事业", "财运", "感情", "健康"]
        for q_type in question_types:
            interpretation = analyzer.generate_interpretation(hexagram, q_type)
            assert interpretation['question_type'] == q_type
            assert len(interpretation['advice']) > 0

    def test_all_64_hexagrams_accessible(self, analyzer, data_loader):
        """测试所有64卦都可访问"""
        hexagrams = data_loader.get_hexagrams()
        assert len(hexagrams) == 64

        for hexagram in hexagrams:
            # 测试可以生成解释
            interpretation = analyzer.generate_interpretation(hexagram)
            assert interpretation['hexagram_name'] == hexagram['name']

            # 测试可以分析五行
            element_analysis = analyzer.analyze_element_relation(hexagram)
            assert 'relation_type' in element_analysis

    def test_element_relation_consistency(self, analyzer, data_loader):
        """测试五行关系一致性"""
        hexagrams = data_loader.get_hexagrams()

        for hexagram in hexagrams:
            analysis = analyzer.analyze_element_relation(hexagram)
            stored_relation = hexagram.get('element_relation', '')

            # 验证分析结果与存储的关系描述一致
            if '比和' in stored_relation:
                assert analysis.get('relation_type') == "比和"
            elif '生' in stored_relation:
                assert analysis.get('relation_type') == "生"
            elif '克' in stored_relation:
                assert analysis.get('relation_type') == "克"
            # 如果无法确定，至少应该有relation_type字段
            assert 'relation_type' in analysis or analysis.get('relation_type') == '未知'


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_input(self, analyzer):
        """测试空输入"""
        assert analyzer.parse_trigram_input("") is None
        assert analyzer.parse_hexagram_input("") is None

    def test_special_characters(self, analyzer):
        """测试特殊字符"""
        assert analyzer.parse_trigram_input("@#$") is None
        assert analyzer.parse_hexagram_input("!@#") is None

    def test_case_sensitivity(self, analyzer):
        """测试大小写（中文不区分大小写）"""
        # 中文输入应该正常工作
        trigram = analyzer.parse_trigram_input("乾")
        assert trigram is not None

    def test_unicode_handling(self, analyzer):
        """测试Unicode字符处理"""
        # 測試繁體字
        trigram = analyzer.parse_trigram_input("離")
        assert trigram is not None
        assert trigram['name'] == "離"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
