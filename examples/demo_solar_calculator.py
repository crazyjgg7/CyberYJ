"""
节气天文计算器演示脚本

展示 SolarCalculator 的主要功能
"""

from datetime import datetime
from cyberYJ.core.solar_calculator import SolarCalculator


def main():
    """演示 SolarCalculator 的功能"""

    # 创建计算器实例
    calculator = SolarCalculator()

    print("=" * 60)
    print("节气天文计算器演示")
    print("=" * 60)

    # 1. 计算太阳黄经
    print("\n【1. 计算太阳黄经】")
    test_dates = [
        (datetime(2024, 3, 20, 12, 0, 0), "春分"),
        (datetime(2024, 6, 21, 12, 0, 0), "夏至"),
        (datetime(2024, 9, 22, 12, 0, 0), "秋分"),
        (datetime(2024, 12, 21, 12, 0, 0), "冬至"),
    ]

    for dt, name in test_dates:
        longitude = calculator.get_solar_longitude(dt)
        print(f"{dt.strftime('%Y-%m-%d')} ({name}): 太阳黄经 = {longitude}°")

    # 2. 查询当前节气
    print("\n【2. 查询当前节气】")
    dt = datetime(2024, 2, 4, 12, 0, 0)
    term_info = calculator.get_current_solar_term(dt)
    print(f"日期: {dt.strftime('%Y-%m-%d')}")
    print(f"当前节气: {term_info['name']}")
    print(f"节气黄经: {term_info['longitude']}°")
    print(f"当前太阳黄经: {term_info['solar_longitude']}°")
    print(f"距离下一节气【{term_info['next_term']}】: {term_info['days_to_next']} 天")

    # 3. 计算节气精确时间
    print("\n【3. 计算2024年节气时间】")
    important_terms = ['立春', '春分', '立夏', '夏至', '立秋', '秋分', '立冬', '冬至']

    for term_name in important_terms:
        term_time = calculator.calculate_solar_term_time(2024, term_name)
        print(f"{term_name}: {term_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 4. 节气影响分析
    print("\n【4. 节气影响分析】")
    dt = datetime(2024, 2, 4, 12, 0, 0)
    influence = calculator.get_solar_term_influence(dt)
    print(f"\n日期: {dt.strftime('%Y-%m-%d')}")
    print(influence)

    # 5. 获取全年节气
    print("\n【5. 2024年全部节气时间】")
    all_terms = calculator.get_all_solar_terms_for_year(2024)

    # 按时间排序
    sorted_terms = sorted(all_terms.items(), key=lambda x: x[1])

    for term_name, term_time in sorted_terms:
        print(f"{term_name:4s}: {term_time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
