"""
测试节气天文算法模块
"""

import pytest
from datetime import datetime
import pytz

try:
    import ephem
    EPHEM_AVAILABLE = True
except ImportError:
    EPHEM_AVAILABLE = False

from cyberYJ.core.solar_calculator import SolarCalculator


# 如果 ephem 未安装，跳过所有测试
pytestmark = pytest.mark.skipif(
    not EPHEM_AVAILABLE,
    reason="ephem 库未安装，请运行: pip install ephem"
)


class TestSolarCalculator:
    """测试 SolarCalculator 类"""

    @pytest.fixture
    def calculator(self):
        """创建 SolarCalculator 实例"""
        return SolarCalculator()

    def test_initialization(self, calculator):
        """测试初始化"""
        assert calculator is not None
        assert calculator.data_loader is not None
        assert len(calculator.solar_terms) == 24
        assert len(calculator.term_name_to_longitude) == 24

    def test_get_solar_longitude_spring_equinox(self, calculator):
        """测试春分时的太阳黄经（应接近0度）"""
        # 2024年春分大约在3月20日
        dt = datetime(2024, 3, 20, 12, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        # 春分时太阳黄经应该接近0度（允许±5度误差）
        assert -5 <= longitude <= 5 or 355 <= longitude <= 360

    def test_get_solar_longitude_summer_solstice(self, calculator):
        """测试夏至时的太阳黄经（应接近90度）"""
        # 2024年夏至大约在6月21日
        dt = datetime(2024, 6, 21, 12, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        # 夏至时太阳黄经应该接近90度（允许±5度误差）
        assert 85 <= longitude <= 95

    def test_get_solar_longitude_autumn_equinox(self, calculator):
        """测试秋分时的太阳黄经（应接近180度）"""
        # 2024年秋分大约在9月22日
        dt = datetime(2024, 9, 22, 12, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        # 秋分时太阳黄经应该接近180度（允许±5度误差）
        assert 175 <= longitude <= 185

    def test_get_solar_longitude_winter_solstice(self, calculator):
        """测试冬至时的太阳黄经（应接近270度）"""
        # 2024年冬至大约在12月21日
        dt = datetime(2024, 12, 21, 12, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        # 冬至时太阳黄经应该接近270度（允许±5度误差）
        assert 265 <= longitude <= 275

    def test_get_solar_longitude_with_timezone(self, calculator):
        """测试时区处理"""
        # 同一时刻，不同时区表示
        dt_shanghai = datetime(2024, 3, 20, 12, 0, 0)
        dt_utc = datetime(2024, 3, 20, 4, 0, 0)  # 上海时间12点 = UTC 4点

        longitude_shanghai = calculator.get_solar_longitude(
            dt_shanghai, 'Asia/Shanghai'
        )
        longitude_utc = calculator.get_solar_longitude(dt_utc, 'UTC')

        # 两个时间点的黄经应该非常接近
        assert abs(longitude_shanghai - longitude_utc) < 1

    def test_get_solar_longitude_with_tzinfo(self, calculator):
        """测试带时区信息的 datetime"""
        tz = pytz.timezone('Asia/Shanghai')
        dt = tz.localize(datetime(2024, 3, 20, 12, 0, 0))

        longitude = calculator.get_solar_longitude(dt)
        assert isinstance(longitude, float)
        assert 0 <= longitude < 360

    def test_get_current_solar_term_lichun(self, calculator):
        """测试立春节气查询"""
        # 2024年立春大约在2月4日
        dt = datetime(2024, 2, 4, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        assert term_info['name'] == '立春'
        assert term_info['longitude'] == 315
        assert 'solar_longitude' in term_info
        assert 'days_to_next' in term_info
        assert term_info['next_term'] == '雨水'
        assert isinstance(term_info['days_to_next'], int)
        assert 0 <= term_info['days_to_next'] <= 20

    def test_get_current_solar_term_chunfen(self, calculator):
        """测试春分节气查询"""
        # 2024年春分大约在3月20日
        dt = datetime(2024, 3, 20, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        assert term_info['name'] == '春分'
        assert term_info['longitude'] == 0
        assert term_info['next_term'] == '清明'

    def test_get_current_solar_term_xiazhi(self, calculator):
        """测试夏至节气查询"""
        # 2024年夏至大约在6月21日
        dt = datetime(2024, 6, 21, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        assert term_info['name'] == '夏至'
        assert term_info['longitude'] == 90
        assert term_info['next_term'] == '小暑'

    def test_get_current_solar_term_qiufen(self, calculator):
        """测试秋分节气查询"""
        # 2024年秋分大约在9月22日
        dt = datetime(2024, 9, 22, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        assert term_info['name'] == '秋分'
        assert term_info['longitude'] == 180
        assert term_info['next_term'] == '寒露'

    def test_get_current_solar_term_dongzhi(self, calculator):
        """测试冬至节气查询"""
        # 2024年冬至大约在12月21日
        dt = datetime(2024, 12, 21, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        assert term_info['name'] == '冬至'
        assert term_info['longitude'] == 270
        assert term_info['next_term'] == '小寒'

    def test_calculate_solar_term_time_chunfen(self, calculator):
        """测试计算春分时间"""
        term_time = calculator.calculate_solar_term_time(2024, '春分')

        # 2024年春分应该在3月20日前后
        assert term_time.year == 2024
        assert term_time.month == 3
        assert 19 <= term_time.day <= 21

        # 验证计算的时间确实是春分（黄经接近0度）
        longitude = calculator.get_solar_longitude(term_time)
        assert abs(longitude) < 1 or abs(longitude - 360) < 1

    def test_calculate_solar_term_time_xiazhi(self, calculator):
        """测试计算夏至时间"""
        term_time = calculator.calculate_solar_term_time(2024, '夏至')

        # 2024年夏至应该在6月21日前后
        assert term_time.year == 2024
        assert term_time.month == 6
        assert 20 <= term_time.day <= 22

        # 验证计算的时间确实是夏至（黄经接近90度）
        longitude = calculator.get_solar_longitude(term_time)
        assert abs(longitude - 90) < 1

    def test_calculate_solar_term_time_qiufen(self, calculator):
        """测试计算秋分时间"""
        term_time = calculator.calculate_solar_term_time(2024, '秋分')

        # 2024年秋分应该在9月22日前后
        assert term_time.year == 2024
        assert term_time.month == 9
        assert 21 <= term_time.day <= 23

        # 验证计算的时间确实是秋分（黄经接近180度）
        longitude = calculator.get_solar_longitude(term_time)
        assert abs(longitude - 180) < 1

    def test_calculate_solar_term_time_dongzhi(self, calculator):
        """测试计算冬至时间"""
        term_time = calculator.calculate_solar_term_time(2024, '冬至')

        # 2024年冬至应该在12月21日前后
        assert term_time.year == 2024
        assert term_time.month == 12
        assert 20 <= term_time.day <= 22

        # 验证计算的时间确实是冬至（黄经接近270度）
        longitude = calculator.get_solar_longitude(term_time)
        assert abs(longitude - 270) < 1

    def test_calculate_solar_term_time_invalid_name(self, calculator):
        """测试无效的节气名称"""
        with pytest.raises(ValueError, match="未知的节气名称"):
            calculator.calculate_solar_term_time(2024, '无效节气')

    def test_calculate_solar_term_time_with_timezone(self, calculator):
        """测试不同时区的节气时间计算"""
        term_time_shanghai = calculator.calculate_solar_term_time(
            2024, '春分', 'Asia/Shanghai'
        )
        term_time_utc = calculator.calculate_solar_term_time(
            2024, '春分', 'UTC'
        )

        # 转换到同一时区比较
        term_time_shanghai_utc = term_time_shanghai.astimezone(pytz.UTC)

        # 时间差应该在几分钟内（由于计算精度）
        time_diff = abs(
            (term_time_shanghai_utc - term_time_utc).total_seconds()
        )
        assert time_diff < 600  # 10分钟内

    def test_get_solar_term_influence_lichun(self, calculator):
        """测试立春节气影响描述"""
        dt = datetime(2024, 2, 4, 12, 0, 0)
        influence = calculator.get_solar_term_influence(dt)

        assert isinstance(influence, str)
        assert '立春' in influence
        assert '万物复苏' in influence
        assert '雨水' in influence
        assert '天' in influence

    def test_get_solar_term_influence_chunfen(self, calculator):
        """测试春分节气影响描述"""
        dt = datetime(2024, 3, 20, 12, 0, 0)
        influence = calculator.get_solar_term_influence(dt)

        assert isinstance(influence, str)
        assert '春分' in influence
        assert '阴阳平衡' in influence
        assert '清明' in influence

    def test_get_solar_term_influence_all_terms(self, calculator):
        """测试所有节气都有影响描述"""
        for term in calculator.solar_terms:
            term_name = term['name']
            assert term_name in calculator.SOLAR_TERM_INFLUENCES

    def test_get_all_solar_terms_for_year(self, calculator):
        """测试获取全年所有节气时间"""
        all_terms = calculator.get_all_solar_terms_for_year(2024)

        # 应该有24个节气
        assert len(all_terms) == 24

        # 检查几个关键节气
        assert '春分' in all_terms
        assert '夏至' in all_terms
        assert '秋分' in all_terms
        assert '冬至' in all_terms

        # 验证时间顺序（大部分节气应该按顺序）
        spring_equinox = all_terms['春分']
        summer_solstice = all_terms['夏至']
        autumn_equinox = all_terms['秋分']
        winter_solstice = all_terms['冬至']

        assert spring_equinox < summer_solstice
        assert summer_solstice < autumn_equinox
        assert autumn_equinox < winter_solstice

    def test_solar_longitude_precision(self, calculator):
        """测试黄经计算精度"""
        dt = datetime(2024, 3, 20, 12, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        # 应该精确到小数点后2位
        assert isinstance(longitude, float)
        # 检查小数位数不超过2位（允许浮点误差）
        assert round(longitude, 2) == longitude

    def test_solar_longitude_range(self, calculator):
        """测试黄经范围"""
        # 测试一年中的多个时间点
        test_dates = [
            datetime(2024, 1, 1),
            datetime(2024, 3, 1),
            datetime(2024, 6, 1),
            datetime(2024, 9, 1),
            datetime(2024, 12, 1),
        ]

        for dt in test_dates:
            longitude = calculator.get_solar_longitude(dt)
            assert 0 <= longitude < 360

    def test_days_to_next_term_reasonable(self, calculator):
        """测试距离下一节气的天数是否合理"""
        # 节气间隔约15天
        dt = datetime(2024, 2, 4, 12, 0, 0)  # 立春
        term_info = calculator.get_current_solar_term(dt)

        # 距离下一节气应该在0-20天之间
        assert 0 <= term_info['days_to_next'] <= 20

    def test_term_name_to_longitude_mapping(self, calculator):
        """测试节气名称到黄经的映射"""
        assert calculator.term_name_to_longitude['春分'] == 0
        assert calculator.term_name_to_longitude['夏至'] == 90
        assert calculator.term_name_to_longitude['秋分'] == 180
        assert calculator.term_name_to_longitude['冬至'] == 270
        assert calculator.term_name_to_longitude['立春'] == 315

    def test_solar_term_cycle(self, calculator):
        """测试节气循环（大寒之后是立春）"""
        # 测试大寒时期
        dt = datetime(2024, 1, 20, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        if term_info['name'] == '大寒':
            assert term_info['next_term'] == '立春'


class TestSolarCalculatorEdgeCases:
    """测试边界情况"""

    @pytest.fixture
    def calculator(self):
        """创建 SolarCalculator 实例"""
        return SolarCalculator()

    def test_leap_year(self, calculator):
        """测试闰年的节气计算"""
        # 2024是闰年
        term_time = calculator.calculate_solar_term_time(2024, '春分')
        assert term_time.year == 2024

        # 2023不是闰年
        term_time = calculator.calculate_solar_term_time(2023, '春分')
        assert term_time.year == 2023

    def test_year_boundary(self, calculator):
        """测试跨年边界的节气"""
        # 立春通常在2月初，可能跨年
        dt = datetime(2024, 1, 1, 12, 0, 0)
        term_info = calculator.get_current_solar_term(dt)

        # 应该能正常返回节气信息
        assert term_info['name'] in ['小寒', '大寒', '冬至']

    def test_midnight(self, calculator):
        """测试午夜时间"""
        dt = datetime(2024, 3, 20, 0, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        assert 0 <= longitude < 360

    def test_noon(self, calculator):
        """测试正午时间"""
        dt = datetime(2024, 3, 20, 12, 0, 0)
        longitude = calculator.get_solar_longitude(dt)

        assert 0 <= longitude < 360


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
