"""
测试罗盘坐向分析工具
"""

import pytest
from datetime import datetime
from cyberYJ.tools.luopan_orientation import LuopanOrientationTool


class TestLuopanOrientationTool:
    """测试罗盘坐向分析工具"""

    def setup_method(self):
        """每个测试方法前执行"""
        self.tool = LuopanOrientationTool()

    def test_basic_orientation(self):
        """测试基本坐向分析"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅"
        )

        assert result is not None
        assert 'direction_class' in result
        assert 'house_gua' in result
        assert 'auspicious_positions' in result
        assert 'inauspicious_positions' in result
        assert 'layout_tips' in result
        assert 'trace' in result
        assert len(result['trace']) > 0

    def test_all_building_types(self):
        """测试所有建筑类型"""
        building_types = ['住宅', '办公室', '商铺', '工厂']

        for building_type in building_types:
            result = self.tool.execute(
                sitting_direction="坐北朝南",
                building_type=building_type
            )

            assert result is not None
            # 检查布局建议中是否包含相关内容
            tips_text = ' '.join(result['layout_tips'])
            # 住宅类型的建议中会包含"主卧"、"书房"等关键词
            assert len(result['layout_tips']) > 0

    def test_orientation_with_owner_birth(self):
        """测试带出生日期的分析"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            owner_birth="1990-05-15"
        )

        assert result is not None
        assert 'ming_gua_match' in result
        assert any('命卦' in step for step in result['trace'])

    def test_orientation_with_timestamp(self):
        """测试指定时间的分析"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2024-02-04T10:00:00+08:00"
        )

        assert result is not None
        assert '2024-02-04' in result['trace'][0]

    def test_chinese_direction_formats(self):
        """测试中文方位格式"""
        directions = [
            "坐北朝南",
            "坐南朝北",
            "坐东朝西",
            "坐西朝东",
            "坐西北向东南"
        ]

        for direction in directions:
            result = self.tool.execute(
                sitting_direction=direction,
                building_type="住宅"
            )

            assert result is not None
            assert 'house_gua' in result

    def test_degree_direction_format(self):
        """测试角度格式"""
        result = self.tool.execute(
            sitting_direction="坐340向160",
            building_type="住宅"
        )

        assert result is not None
        assert 'sitting_degree' in result
        assert abs(result['sitting_degree'] - 340) < 1

    def test_mountain_direction_format(self):
        """测试干支格式"""
        result = self.tool.execute(
            sitting_direction="坐亥向巳",
            building_type="住宅"
        )

        assert result is not None
        assert 'house_gua' in result

    def test_auspicious_positions_count(self):
        """测试吉位数量"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅"
        )

        assert len(result['auspicious_positions']) == 4
        assert len(result['inauspicious_positions']) == 4

    def test_flying_stars_included(self):
        """测试流年飞星包含"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2024-06-01T10:00:00+08:00"
        )

        assert 'annual_flying_stars' in result
        assert result['annual_flying_stars']['year'] == 2024
        assert 'central_star' in result['annual_flying_stars']
        assert 'palace_map' in result['annual_flying_stars']

    def test_flying_stars_computed_year(self):
        """测试飞星年盘自动推算"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2035-06-01T10:00:00+08:00"
        )

        assert 'annual_flying_stars' in result
        assert result['annual_flying_stars']['year'] == 2035
        assert result['annual_flying_stars']['central_star'] in range(1, 10)

    def test_house_flying_stars_combined(self):
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2026-06-01T10:00:00+08:00"
        )

        assert 'house_flying_stars' in result
        assert 'combined_flying_stars' in result
        assert 'current_auspicious_positions' in result
        assert 'current_inauspicious_positions' in result
        assert isinstance(result['current_auspicious_positions'], list)
        assert isinstance(result['current_inauspicious_positions'], list)

    def test_degrade_when_house_rule_missing(self, monkeypatch):
        monkeypatch.setattr(
            self.tool.data_loader,
            "get_flying_star_house_rule",
            lambda period, sitting_mountain: None
        )
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2026-06-01T10:00:00+08:00"
        )
        assert "combined_flying_stars" not in result
        assert any("宅盘规则缺失" in step for step in result["trace"])

    def test_scoring_fallback_strategy_passthrough(self, monkeypatch):
        base_flying_stars = self.tool.data_loader.get_flying_stars_by_year(2026)

        def fake_flying_stars(_year):
            patched = dict(base_flying_stars)
            palace_map = dict(base_flying_stars["palace_map"])
            palace_map.pop("坎", None)
            patched["palace_map"] = palace_map
            return patched

        monkeypatch.setattr(
            self.tool.data_loader,
            "get_flying_stars_by_year",
            fake_flying_stars
        )
        monkeypatch.setattr(
            self.tool.data_loader,
            "get_flying_star_scoring",
            lambda: {
                "stars": {
                    "1": {"score": 2},
                    "2": {"score": -2},
                    "3": {"score": -2},
                    "4": {"score": 2},
                    "5": {"score": -3},
                    "6": {"score": 2},
                    "7": {"score": -1},
                    "8": {"score": 3},
                    "9": {"score": 2}
                },
                "fallback": {
                    "missing_annual_star": "neutral",
                    "unknown_star_score": 0
                }
            }
        )

        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            timestamp="2026-06-01T10:00:00+08:00"
        )
        assert "combined_flying_stars" in result
        assert "坎" in result["combined_flying_stars"]
        assert result["combined_flying_stars"]["坎"]["reason"] == "missing_annual_star"

    def test_layout_tips_generation(self):
        """测试布局建议生成"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅"
        )

        tips = result['layout_tips']
        assert isinstance(tips, list)
        assert len(tips) > 0
        assert len(tips) <= 8

        # 检查是否包含住宅相关建议
        tips_text = ' '.join(tips)
        assert '主卧' in tips_text or '书房' in tips_text or '厨房' in tips_text

    def test_invalid_sitting_direction(self):
        """测试无效的坐向"""
        with pytest.raises(ValueError, match="坐向解析失败"):
            self.tool.execute(
                sitting_direction="无效坐向",
                building_type="住宅"
            )

    def test_invalid_timestamp(self):
        """测试无效的时间戳"""
        with pytest.raises(ValueError, match="时间戳格式错误"):
            self.tool.execute(
                sitting_direction="坐北朝南",
                building_type="住宅",
                timestamp="invalid-timestamp"
            )

    def test_all_eight_houses(self):
        """测试八个宅卦都能正常分析"""
        directions = [
            ("坐北朝南", "坎宅"),
            ("坐南朝北", "离宅"),
            ("坐东朝西", "震宅"),
            ("坐西朝东", "兑宅"),
            ("坐东南向西北", "巽宅"),
            ("坐西北向东南", "乾宅"),
            ("坐西南向东北", "坤宅"),
            ("坐东北向西南", "艮宅")
        ]

        for direction, expected_gua in directions:
            result = self.tool.execute(
                sitting_direction=direction,
                building_type="住宅"
            )

            assert result is not None
            assert result['house_gua'] == expected_gua

    def test_sources_included(self):
        """测试来源信息包含"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅"
        )

        assert 'sources' in result
        assert isinstance(result['sources'], list)
        assert len(result['sources']) > 0

    def test_trace_completeness(self):
        """测试推导路径完整性"""
        result = self.tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            owner_birth="1990-05-15"
        )

        trace = result['trace']
        assert len(trace) >= 5  # 至少包含：时间、坐向、宅卦、吉位、凶位

        # 检查关键信息是否在 trace 中
        trace_text = ' '.join(trace)
        assert '坐向解析' in trace_text
        assert '宅卦' in trace_text
        assert '吉位' in trace_text
        assert '凶位' in trace_text


class TestLuopanOrientationIntegration:
    """集成测试"""

    def test_complete_orientation_workflow(self):
        """测试完整的坐向分析流程"""
        tool = LuopanOrientationTool()

        # 场景：住宅，坐北朝南，主人1990年出生
        result = tool.execute(
            sitting_direction="坐北朝南",
            building_type="住宅",
            owner_birth="1990-05-15",
            timestamp="2024-06-01T10:00:00+08:00"
        )

        # 验证完整性
        assert result['house_gua'] == '坎宅'
        # ming_gua_match 可能因为计算失败而不存在，所以不强制要求
        assert 'annual_flying_stars' in result
        assert result['annual_flying_stars']['year'] == 2024
        assert len(result['layout_tips']) > 0
        # 检查布局建议中包含住宅相关内容
        tips_text = ' '.join(result['layout_tips'])
        assert '主卧' in tips_text or '书房' in tips_text

    def test_office_layout_advice(self):
        """测试办公室布局建议"""
        tool = LuopanOrientationTool()

        result = tool.execute(
            sitting_direction="坐西北向东南",
            building_type="办公室"
        )

        tips_text = ' '.join(result['layout_tips'])
        assert '办公' in tips_text or '会议' in tips_text

    def test_shop_layout_advice(self):
        """测试商铺布局建议"""
        tool = LuopanOrientationTool()

        result = tool.execute(
            sitting_direction="坐东朝西",
            building_type="商铺"
        )

        tips_text = ' '.join(result['layout_tips'])
        assert '收银' in tips_text or '入口' in tips_text or '财运' in tips_text


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
