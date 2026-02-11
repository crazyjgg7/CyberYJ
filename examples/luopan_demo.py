"""
罗盘计算器使用示例

演示如何使用 LuopanCalculator 进行坐向解析、宅卦计算和吉凶方位查询
"""

from datetime import datetime
from cyberYJ.core.luopan_calculator import LuopanCalculator


def main():
    """主函数"""
    calculator = LuopanCalculator()

    print("=" * 60)
    print("罗盘计算器使用示例")
    print("=" * 60)

    # 示例1：解析中文方位描述
    print("\n【示例1】解析中文方位描述")
    print("-" * 60)
    direction = calculator.parse_sitting_direction("坐北朝南")
    print(f"输入: 坐北朝南")
    print(f"坐向角度: {direction['sitting_degree']}°")
    print(f"朝向角度: {direction['facing_degree']}°")
    print(f"坐山: {direction['sitting_mountain']}")
    print(f"向山: {direction['facing_mountain']}")
    print(f"坐向方位: {direction['sitting_direction_group']}")
    print(f"朝向方位: {direction['facing_direction_group']}")

    # 示例2：解析角度格式
    print("\n【示例2】解析角度格式")
    print("-" * 60)
    direction = calculator.parse_sitting_direction("坐340向160")
    print(f"输入: 坐340向160")
    print(f"坐向角度: {direction['sitting_degree']}°")
    print(f"朝向角度: {direction['facing_degree']}°")
    print(f"坐山: {direction['sitting_mountain']}")
    print(f"向山: {direction['facing_mountain']}")

    # 示例3：解析干支格式
    print("\n【示例3】解析干支格式")
    print("-" * 60)
    direction = calculator.parse_sitting_direction("坐亥向巳")
    print(f"输入: 坐亥向巳")
    print(f"坐向角度: {direction['sitting_degree']}°")
    print(f"朝向角度: {direction['facing_degree']}°")
    print(f"坐山: {direction['sitting_mountain']}")
    print(f"向山: {direction['facing_mountain']}")

    # 示例4：计算宅卦
    print("\n【示例4】计算宅卦")
    print("-" * 60)
    test_cases = [
        ("坐北朝南", 0),
        ("坐南朝北", 180),
        ("坐东朝西", 90),
        ("坐西朝东", 270),
        ("坐西北向东南", 315),
    ]

    for desc, degree in test_cases:
        house_gua = calculator.calculate_house_gua(degree)
        print(f"{desc} ({degree}°) → {house_gua}")

    # 示例5：查询吉凶方位
    print("\n【示例5】查询吉凶方位")
    print("-" * 60)
    house_gua = "坎宅"
    positions = calculator.get_auspicious_positions(house_gua)
    print(f"宅卦: {house_gua}")
    print(f"\n吉位:")
    for pos in positions['auspicious']:
        print(f"  - {pos}")
    print(f"\n凶位:")
    for pos in positions['inauspicious']:
        print(f"  - {pos}")

    # 示例6：计算命卦
    print("\n【示例6】计算命卦")
    print("-" * 60)
    birth_date = datetime(1990, 5, 15)

    # 男命
    ming_gua_male = calculator.calculate_ming_gua(birth_date, 'male')
    print(f"出生日期: {birth_date.strftime('%Y年%m月%d日')}")
    print(f"性别: 男")
    print(f"命卦: {ming_gua_male['ming_gua']}")
    print(f"命宅: {ming_gua_male['ming_gua_house']}")
    print(f"类型: {ming_gua_male['group']}")

    # 女命
    ming_gua_female = calculator.calculate_ming_gua(birth_date, 'female')
    print(f"\n出生日期: {birth_date.strftime('%Y年%m月%d日')}")
    print(f"性别: 女")
    print(f"命卦: {ming_gua_female['ming_gua']}")
    print(f"命宅: {ming_gua_female['ming_gua_house']}")
    print(f"类型: {ming_gua_female['group']}")

    # 示例7：检查宅命匹配
    print("\n【示例7】检查宅命匹配")
    print("-" * 60)
    house_gua = "坎宅"
    compatibility = calculator.check_house_compatibility(house_gua, ming_gua_male)
    print(f"宅卦: {house_gua} ({compatibility['house_group']})")
    print(f"命卦: {ming_gua_male['ming_gua']}宅 ({compatibility['ming_group']})")
    print(f"是否匹配: {'是' if compatibility['compatible'] else '否'}")
    print(f"建议: {compatibility['recommendation']}")

    # 示例8：完整工作流程
    print("\n【示例8】完整工作流程")
    print("-" * 60)
    print("场景: 为1990年出生的男性选择合适的房屋坐向")
    print()

    # 1. 解析房屋坐向
    direction_input = "坐西北向东南"
    direction = calculator.parse_sitting_direction(direction_input)
    print(f"1. 房屋坐向: {direction_input}")
    print(f"   坐向角度: {direction['sitting_degree']}°")
    print(f"   坐山: {direction['sitting_mountain']}")

    # 2. 计算宅卦
    house_gua = calculator.calculate_house_gua(direction['sitting_degree'])
    print(f"\n2. 宅卦: {house_gua}")

    # 3. 查询吉凶方位
    positions = calculator.get_auspicious_positions(house_gua)
    print(f"\n3. 吉凶方位:")
    print(f"   吉位: {', '.join([p.split('（')[0] for p in positions['auspicious']])}")
    print(f"   凶位: {', '.join([p.split('（')[0] for p in positions['inauspicious']])}")

    # 4. 计算命卦
    birth_date = datetime(1990, 5, 15)
    ming_gua_info = calculator.calculate_ming_gua(birth_date, 'male')
    print(f"\n4. 命卦: {ming_gua_info['ming_gua']} ({ming_gua_info['group']})")

    # 5. 检查宅命匹配
    compatibility = calculator.check_house_compatibility(house_gua, ming_gua_info)
    print(f"\n5. 宅命匹配:")
    print(f"   {compatibility['recommendation']}")

    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
