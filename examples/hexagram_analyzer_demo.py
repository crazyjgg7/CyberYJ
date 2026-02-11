"""
卦象分析器使用示例

演示如何使用 HexagramAnalyzer 进行卦象分析
"""

from cyberYJ.core.hexagram_analyzer import HexagramAnalyzer


def main():
    # 创建分析器实例
    analyzer = HexagramAnalyzer()

    print("=" * 60)
    print("卦象分析器使用示例")
    print("=" * 60)

    # 示例 1: 解析八卦输入
    print("\n【示例 1】解析八卦输入")
    print("-" * 60)

    # 通过卦名
    trigram = analyzer.parse_trigram_input("乾")
    print(f"卦名输入 '乾': {trigram['name']} - {trigram['element']}行 - {trigram['direction']}")

    # 通过方位
    trigram = analyzer.parse_trigram_input("西北")
    print(f"方位输入 '西北': {trigram['name']} - {trigram['element']}行 - {trigram['direction']}")

    # 通过数字
    trigram = analyzer.parse_trigram_input("1")
    print(f"数字输入 '1': {trigram['name']} - {trigram['element']}行 - {trigram['direction']}")

    # 示例 2: 获取卦象
    print("\n【示例 2】获取卦象")
    print("-" * 60)

    hexagram = analyzer.get_hexagram("乾", "乾")
    print(f"乾上乾下: 第{hexagram['id']}卦 - {hexagram['name']}卦")
    print(f"卦辞: {hexagram['judgment_summary']}")
    print(f"象辞: {hexagram['image_summary']}")

    # 示例 3: 五行分析
    print("\n【示例 3】五行分析")
    print("-" * 60)

    hexagram = analyzer.get_hexagram("離", "震")
    element_analysis = analyzer.analyze_element_relation(hexagram)
    print(f"卦象: {hexagram['name']}卦 (離上震下)")
    print(f"上卦五行: {element_analysis['upper_element']}")
    print(f"下卦五行: {element_analysis['lower_element']}")
    print(f"关系类型: {element_analysis['relation_type']}")
    print(f"关系描述: {element_analysis['description']}")

    # 示例 4: 生成卦辞解释（事业）
    print("\n【示例 4】生成卦辞解释 - 事业运势")
    print("-" * 60)

    hexagram = analyzer.get_hexagram("乾", "乾")
    interpretation = analyzer.generate_interpretation(hexagram, "事业")
    print(f"卦象: {interpretation['hexagram_name']}卦")
    print(f"卦辞: {interpretation['judgment']}")
    print(f"建议: {interpretation['advice']}")

    # 示例 5: 生成卦辞解释（财运）
    print("\n【示例 5】生成卦辞解释 - 财运")
    print("-" * 60)

    hexagram = analyzer.get_hexagram("坤", "乾")
    interpretation = analyzer.generate_interpretation(hexagram, "财运")
    print(f"卦象: {interpretation['hexagram_name']}卦")
    print(f"卦辞: {interpretation['judgment']}")
    print(f"建议: {interpretation['advice']}")

    # 示例 6: 变爻分析
    print("\n【示例 6】变爻分析")
    print("-" * 60)

    hexagram = analyzer.get_hexagram("乾", "乾")
    changing_result = analyzer.analyze_changing_line(hexagram, 1)
    print(f"本卦: {changing_result['original_hexagram']['name']}卦")
    print(f"变爻: 初爻")
    print(f"变卦: {changing_result['changed_hexagram']['name']}卦")
    print(f"解释: {changing_result['interpretation'][:100]}...")

    # 示例 7: 解析卦象输入（多种格式）
    print("\n【示例 7】解析卦象输入")
    print("-" * 60)

    # 通过卦名
    hexagram = analyzer.parse_hexagram_input("乾")
    print(f"卦名输入 '乾': 第{hexagram['id']}卦 - {hexagram['name']}卦")

    # 通过序号
    hexagram = analyzer.parse_hexagram_input("64")
    print(f"序号输入 '64': 第{hexagram['id']}卦 - {hexagram['name']}卦")

    # 通过上下卦组合
    hexagram = analyzer.parse_hexagram_input("坤上乾下")
    print(f"组合输入 '坤上乾下': 第{hexagram['id']}卦 - {hexagram['name']}卦")

    # 示例 8: 完整占卜流程
    print("\n【示例 8】完整占卜流程")
    print("-" * 60)

    # 1. 解析输入
    upper = analyzer.parse_trigram_input("西北")
    lower = analyzer.parse_trigram_input("西南")
    print(f"上卦: {upper['name']} ({upper['direction']})")
    print(f"下卦: {lower['name']} ({lower['direction']})")

    # 2. 获取卦象
    hexagram = analyzer.get_hexagram(upper, lower)
    print(f"\n得卦: 第{hexagram['id']}卦 - {hexagram['name']}卦")

    # 3. 五行分析
    element_analysis = analyzer.analyze_element_relation(hexagram)
    print(f"五行关系: {element_analysis['relation_type']}")

    # 4. 生成解释
    interpretation = analyzer.generate_interpretation(hexagram, "事业")
    print(f"\n卦辞: {interpretation['judgment']}")
    print(f"象辞: {interpretation['image']}")
    print(f"\n{interpretation['advice']}")

    print("\n" + "=" * 60)
    print("示例演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
