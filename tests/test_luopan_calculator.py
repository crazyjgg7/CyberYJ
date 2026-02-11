"""
测试罗盘坐向解析模块
"""

import pytest
from datetime import datetime

from cyberYJ.core.luopan_calculator import LuopanCalculator


class TestLuopanCalculator:
    """测试罗盘计算器"""

    @pytest.fixture
    def calculator(self):
        """创建罗盘计算器实例"""
        return LuopanCalculator()

    def test_parse_chinese_direction_basic(self, calculator):
        """测试基本中文方位解析"""
        # 坐北朝南
        result = calculator.parse_sitting_direction("坐北朝南")
        assert result['sitting_degree'] == 0
        assert result['facing_degree'] == 180
        assert result['sitting_direction_group'] == '北'
        assert result['facing_direction_group'] == '南'

        # 坐南朝北
        result = calculator.parse_sitting_direction("坐南朝北")
        assert result['sitting_degree'] == 180
        assert result['facing_degree'] == 0

        # 坐东朝西
        result = calculator.parse_sitting_direction("坐东朝西")
        assert result['sitting_degree'] == 90
        assert result['facing_degree'] == 270

        # 坐西朝东
        result = calculator.parse_sitting_direction("坐西朝东")
        assert result['sitting_degree'] == 270
        assert result['facing_degree'] == 90

    def test_parse_chinese_direction_compound(self, calculator):
        """测试复合中文方位解析"""
        # 坐西北向东南
        result = calculator.parse_sitting_direction("坐西北向东南")
        assert result['sitting_degree'] == 315
        assert result['facing_degree'] == 135

        # 坐东北朝西南
        result = calculator.parse_sitting_direction("坐东北朝西南")
        assert result['sitting_degree'] == 45
        assert result['facing_degree'] == 225

    def test_parse_degree_format(self, calculator):
        """测试角度格式解析"""
        # 坐340向160
        result = calculator.parse_sitting_direction("坐340向160")
        assert result['sitting_degree'] == 340
        assert result['facing_degree'] == 160

        # 坐340度（自动计算朝向）
        result = calculator.parse_sitting_direction("坐340度")
        assert result['sitting_degree'] == 340
        assert result['facing_degree'] == 160

        # 坐0度
        result = calculator.parse_sitting_direction("坐0度")
        assert result['sitting_degree'] == 0
        assert result['facing_degree'] == 180

    def test_parse_mountain_format(self, calculator):
        """测试干支格式解析"""
        # 坐亥向巳
        result = calculator.parse_sitting_direction("坐亥向巳")
        assert result['sitting_mountain'] == '亥'
        assert result['facing_mountain'] == '巳'
        assert result['sitting_direction_group'] == '西北'
        assert result['facing_direction_group'] == '东南'

        # 坐壬向丙
        result = calculator.parse_sitting_direction("坐壬向丙")
        assert result['sitting_mountain'] == '壬'
        assert result['facing_mountain'] == '丙'
        assert result['sitting_direction_group'] == '北'
        assert result['facing_direction_group'] == '南'

        # 只指定坐山
        result = calculator.parse_sitting_direction("坐子")
        assert result['sitting_mountain'] == '子'
        assert result['sitting_direction_group'] == '北'

    def test_parse_invalid_format(self, calculator):
        """测试无效格式"""
        with pytest.raises(ValueError, match="无法解析的坐向格式"):
            calculator.parse_sitting_direction("无效格式")

        with pytest.raises(ValueError, match="无法解析的坐向格式"):
            calculator.parse_sitting_direction("")

    def test_get_mountain_by_degree(self, calculator):
        """测试根据角度获取山向"""
        # 测试子山（7.5-22.5度）
        mountain = calculator.get_mountain_by_degree(15)
        assert mountain is not None
        assert mountain['name'] == '子'
        assert mountain['direction_group'] == '北'

        # 测试午山（187.5-202.5度）
        mountain = calculator.get_mountain_by_degree(195)
        assert mountain is not None
        assert mountain['name'] == '午'
        assert mountain['direction_group'] == '南'

        # 测试壬山（跨越0度：352.5-7.5度）
        mountain = calculator.get_mountain_by_degree(0)
        assert mountain is not None
        assert mountain['name'] == '壬'
        assert mountain['direction_group'] == '北'

        mountain = calculator.get_mountain_by_degree(355)
        assert mountain is not None
        assert mountain['name'] == '壬'

    def test_get_mountain_by_degree_boundaries(self, calculator):
        """测试山向边界情况"""
        # 测试边界值
        mountain = calculator.get_mountain_by_degree(7.5)
        assert mountain['name'] in ['壬', '子']  # 边界可能属于任一山向

        # 测试跨越360度
        mountain = calculator.get_mountain_by_degree(360)
        assert mountain is not None
        assert mountain['name'] == '壬'

        mountain = calculator.get_mountain_by_degree(720)  # 720度 = 0度
        assert mountain is not None
        assert mountain['name'] == '壬'

    def test_calculate_house_gua(self, calculator):
        """测试宅卦计算"""
        # 坐北（子山）→ 坎宅
        house_gua = calculator.calculate_house_gua(15)
        assert house_gua == '坎宅'

        # 坐南（午山）→ 离宅
        house_gua = calculator.calculate_house_gua(195)
        assert house_gua == '离宅'

        # 坐东（卯山）→ 震宅
        house_gua = calculator.calculate_house_gua(105)
        assert house_gua == '震宅'

        # 坐西（酉山）→ 兑宅
        house_gua = calculator.calculate_house_gua(285)
        assert house_gua == '兑宅'

        # 坐西北（乾山）→ 乾宅
        house_gua = calculator.calculate_house_gua(330)
        assert house_gua == '乾宅'

        # 坐西南（坤山）→ 坤宅
        house_gua = calculator.calculate_house_gua(240)
        assert house_gua == '坤宅'

        # 坐东北（艮山）→ 艮宅
        house_gua = calculator.calculate_house_gua(60)
        assert house_gua == '艮宅'

        # 坐东南（巽山）→ 巽宅
        house_gua = calculator.calculate_house_gua(150)
        assert house_gua == '巽宅'

    def test_calculate_house_gua_all_mountains(self, calculator):
        """测试所有山向的宅卦计算"""
        # 乾宅：戌、乾、亥
        assert calculator.calculate_house_gua(315) == '乾宅'  # 戌
        assert calculator.calculate_house_gua(330) == '乾宅'  # 乾
        assert calculator.calculate_house_gua(345) == '乾宅'  # 亥

        # 坎宅：壬、子、癸
        assert calculator.calculate_house_gua(0) == '坎宅'    # 壬
        assert calculator.calculate_house_gua(15) == '坎宅'   # 子
        assert calculator.calculate_house_gua(30) == '坎宅'   # 癸

        # 艮宅：丑、艮、寅
        assert calculator.calculate_house_gua(45) == '艮宅'   # 丑
        assert calculator.calculate_house_gua(60) == '艮宅'   # 艮
        assert calculator.calculate_house_gua(75) == '艮宅'   # 寅

        # 震宅：甲、卯、乙
        assert calculator.calculate_house_gua(90) == '震宅'   # 甲
        assert calculator.calculate_house_gua(105) == '震宅'  # 卯
        assert calculator.calculate_house_gua(120) == '震宅'  # 乙

        # 巽宅：辰、巽、巳
        assert calculator.calculate_house_gua(135) == '巽宅'  # 辰
        assert calculator.calculate_house_gua(150) == '巽宅'  # 巽
        assert calculator.calculate_house_gua(165) == '巽宅'  # 巳

        # 离宅：丙、午、丁
        assert calculator.calculate_house_gua(180) == '离宅'  # 丙
        assert calculator.calculate_house_gua(195) == '离宅'  # 午
        assert calculator.calculate_house_gua(210) == '离宅'  # 丁

        # 坤宅：未、坤、申
        assert calculator.calculate_house_gua(225) == '坤宅'  # 未
        assert calculator.calculate_house_gua(240) == '坤宅'  # 坤
        assert calculator.calculate_house_gua(255) == '坤宅'  # 申

        # 兑宅：庚、酉、辛
        assert calculator.calculate_house_gua(270) == '兑宅'  # 庚
        assert calculator.calculate_house_gua(285) == '兑宅'  # 酉
        assert calculator.calculate_house_gua(300) == '兑宅'  # 辛

    def test_get_auspicious_positions(self, calculator):
        """测试吉凶方位查询"""
        # 测试坎宅
        positions = calculator.get_auspicious_positions('坎宅')
        assert 'auspicious' in positions
        assert 'inauspicious' in positions
        assert len(positions['auspicious']) == 4
        assert len(positions['inauspicious']) == 4
        assert '生气位（东南方）' in positions['auspicious']
        assert '绝命位（西方）' in positions['inauspicious']

        # 测试乾宅
        positions = calculator.get_auspicious_positions('乾宅')
        assert '生气位（西方）' in positions['auspicious']
        assert '绝命位（东方）' in positions['inauspicious']

    def test_get_auspicious_positions_all_gua(self, calculator):
        """测试所有宅卦的吉凶方位"""
        gua_list = ['乾宅', '坤宅', '震宅', '巽宅', '坎宅', '离宅', '艮宅', '兑宅']

        for gua in gua_list:
            positions = calculator.get_auspicious_positions(gua)
            assert 'auspicious' in positions
            assert 'inauspicious' in positions
            assert len(positions['auspicious']) == 4
            assert len(positions['inauspicious']) == 4

    def test_get_auspicious_positions_invalid_gua(self, calculator):
        """测试无效宅卦"""
        with pytest.raises(ValueError, match="未找到宅卦数据"):
            calculator.get_auspicious_positions('无效宅')

    def test_calculate_ming_gua_male(self, calculator):
        """测试男命命卦计算"""
        # 1990年男命
        birth_date = datetime(1990, 1, 1)
        result = calculator.calculate_ming_gua(birth_date, 'male')
        assert result['birth_year'] == 1990
        assert result['ming_gua'] in ['乾', '坤', '震', '巽', '坎', '离', '艮', '兑']
        assert result['group'] in ['东四命', '西四命']
        assert result['ming_gua_house'] == f"{result['ming_gua']}宅"

        # 1985年男命
        birth_date = datetime(1985, 6, 15)
        result = calculator.calculate_ming_gua(birth_date, 'male')
        assert result['birth_year'] == 1985

    def test_calculate_ming_gua_female(self, calculator):
        """测试女命命卦计算"""
        # 1990年女命
        birth_date = datetime(1990, 1, 1)
        result = calculator.calculate_ming_gua(birth_date, 'female')
        assert result['birth_year'] == 1990
        assert result['ming_gua'] in ['乾', '坤', '震', '巽', '坎', '离', '艮', '兑']
        assert result['group'] in ['东四命', '西四命']

        # 1988年女命
        birth_date = datetime(1988, 3, 20)
        result = calculator.calculate_ming_gua(birth_date, 'female')
        assert result['birth_year'] == 1988

    def test_calculate_ming_gua_special_cases(self, calculator):
        """测试命卦计算的特殊情况"""
        # 测试数字5的情况（男为坤，女为艮）
        # 需要找到会产生5的年份
        # 男命：(100 - year_last_two) % 9 = 5 → year_last_two = 95 或 5
        birth_date = datetime(2005, 1, 1)
        result_male = calculator.calculate_ming_gua(birth_date, 'male')
        # (100 - 5) % 9 = 95 % 9 = 5
        assert result_male['ming_gua'] == '坤'

        # 女命：(year_last_two - 4) % 9 = 5 → year_last_two = 9
        birth_date = datetime(2009, 1, 1)
        result_female = calculator.calculate_ming_gua(birth_date, 'female')
        # (9 - 4) % 9 = 5
        assert result_female['ming_gua'] == '艮'

    def test_calculate_ming_gua_invalid_gender(self, calculator):
        """测试无效性别参数"""
        birth_date = datetime(1990, 1, 1)
        with pytest.raises(ValueError, match="性别必须是"):
            calculator.calculate_ming_gua(birth_date, 'invalid')

    def test_check_house_compatibility(self, calculator):
        """测试宅命匹配"""
        # 东四命配东四宅
        birth_date = datetime(1990, 1, 1)
        ming_gua_info = calculator.calculate_ming_gua(birth_date, 'male')

        # 如果是东四命，测试震宅（东四宅）
        if ming_gua_info['group'] == '东四命':
            result = calculator.check_house_compatibility('震宅', ming_gua_info)
            assert result['compatible'] is True
            assert result['house_group'] == '东四宅'
            assert result['ming_group'] == '东四命'
            assert '吉利' in result['recommendation']

            # 测试不匹配的情况（西四宅）
            result = calculator.check_house_compatibility('乾宅', ming_gua_info)
            assert result['compatible'] is False
            assert result['house_group'] == '西四宅'
            assert '不配' in result['recommendation']
        else:
            # 西四命配西四宅
            result = calculator.check_house_compatibility('乾宅', ming_gua_info)
            assert result['compatible'] is True
            assert result['house_group'] == '西四宅'
            assert result['ming_group'] == '西四命'

            # 测试不匹配的情况（东四宅）
            result = calculator.check_house_compatibility('震宅', ming_gua_info)
            assert result['compatible'] is False
            assert result['house_group'] == '东四宅'

    def test_check_house_compatibility_all_combinations(self, calculator):
        """测试所有宅命组合"""
        dong_si_house = ['震宅', '巽宅', '离宅', '坎宅']
        xi_si_house = ['乾宅', '坤宅', '艮宅', '兑宅']

        # 创建一个东四命
        birth_date = datetime(1990, 1, 1)
        ming_gua_info = calculator.calculate_ming_gua(birth_date, 'male')

        # 根据命卦调整测试
        if ming_gua_info['group'] == '东四命':
            # 东四命应该与东四宅匹配
            for house in dong_si_house:
                result = calculator.check_house_compatibility(house, ming_gua_info)
                assert result['compatible'] is True

            # 东四命不应该与西四宅匹配
            for house in xi_si_house:
                result = calculator.check_house_compatibility(house, ming_gua_info)
                assert result['compatible'] is False
        else:
            # 西四命应该与西四宅匹配
            for house in xi_si_house:
                result = calculator.check_house_compatibility(house, ming_gua_info)
                assert result['compatible'] is True

            # 西四命不应该与东四宅匹配
            for house in dong_si_house:
                result = calculator.check_house_compatibility(house, ming_gua_info)
                assert result['compatible'] is False

    def test_integration_full_workflow(self, calculator):
        """测试完整工作流程"""
        # 1. 解析坐向
        direction = calculator.parse_sitting_direction("坐北朝南")
        assert direction['sitting_degree'] == 0
        assert direction['sitting_mountain'] == '壬'

        # 2. 计算宅卦
        house_gua = calculator.calculate_house_gua(direction['sitting_degree'])
        assert house_gua == '坎宅'

        # 3. 查询吉凶方位
        positions = calculator.get_auspicious_positions(house_gua)
        assert len(positions['auspicious']) == 4
        assert len(positions['inauspicious']) == 4

        # 4. 计算命卦
        birth_date = datetime(1990, 1, 1)
        ming_gua_info = calculator.calculate_ming_gua(birth_date, 'male')
        assert 'ming_gua' in ming_gua_info

        # 5. 检查宅命匹配
        compatibility = calculator.check_house_compatibility(house_gua, ming_gua_info)
        assert 'compatible' in compatibility
        assert 'recommendation' in compatibility

    def test_edge_cases_zero_degree(self, calculator):
        """测试0度边界情况"""
        # 0度应该在壬山范围内（352.5-7.5度）
        mountain = calculator.get_mountain_by_degree(0)
        assert mountain is not None
        assert mountain['name'] == '壬'

        # 测试解析
        result = calculator.parse_sitting_direction("坐0度")
        assert result['sitting_degree'] == 0
        assert result['sitting_mountain'] == '壬'

    def test_edge_cases_360_degree(self, calculator):
        """测试360度边界情况"""
        # 360度应该等同于0度
        mountain = calculator.get_mountain_by_degree(360)
        assert mountain is not None
        assert mountain['name'] == '壬'

        # 测试大于360度的角度
        mountain = calculator.get_mountain_by_degree(375)  # 375 = 15度
        assert mountain is not None
        assert mountain['name'] == '子'

    def test_data_loader_integration(self, calculator):
        """测试与数据加载器的集成"""
        # 确保数据加载器正常工作
        luopan_data = calculator.data_loader.get_luopan()
        assert len(luopan_data) == 24  # 二十四山向

        ba_zhai_data = calculator.data_loader.get_ba_zhai()
        assert len(ba_zhai_data) == 8  # 八宅

        trigrams = calculator.data_loader.get_trigrams()
        assert len(trigrams) == 8  # 八卦


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
