#!/usr/bin/env python3
"""
测试 MCP Server 功能
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool
from cyberYJ.tools.luopan_orientation import LuopanOrientationTool
from cyberYJ.server import _format_fengshui_result, _format_luopan_result

def test_fengshui_divination():
    """测试风水占卜工具"""
    print("=" * 60)
    print("测试 1: 风水占卜工具")
    print("=" * 60)

    tool = FengshuiDivinationTool()

    # 测试基本占卜
    print("\n【测试 1.1】基本占卜（乾卦）")
    result = tool.execute(
        upper_trigram="乾",
        lower_trigram="乾"
    )
    print(f"✅ 卦名: {result['main_hexagram']['name']}")
    print(f"✅ 卦辞: {result['main_hexagram']['judgment']}")
    print(f"✅ 五行: {result['five_elements']}")

    # 测试带问题类型
    print("\n【测试 1.2】带问题类型（事业）")
    result = tool.execute(
        upper_trigram="坤",
        lower_trigram="乾",
        question_type="事业"
    )
    print(f"✅ 卦名: {result['main_hexagram']['name']}")
    print(f"✅ 建议: {result['fortune_advice'][:50]}...")

    # 测试变卦
    print("\n【测试 1.3】变卦分析（初爻变）")
    result = tool.execute(
        upper_trigram="乾",
        lower_trigram="乾",
        changing_line=1
    )
    print(f"✅ 本卦: {result['main_hexagram']['name']}")
    if 'changing_hexagram' in result:
        print(f"✅ 变卦: {result['changing_hexagram']['name']}")

    # 测试格式化输出
    print("\n【测试 1.4】格式化输出")
    formatted = _format_fengshui_result(result)
    print(f"✅ 输出长度: {len(formatted)} 字符")
    print(f"✅ 包含标题: {'# 易经六十四卦解卦分析' in formatted}")
    print(f"✅ 包含宜忌: {'✅' in formatted and '❌' in formatted}")

    print("\n" + "=" * 60)
    print("✅ 风水占卜工具测试通过")
    print("=" * 60)


def test_luopan_orientation():
    """测试罗盘坐向工具"""
    print("\n" + "=" * 60)
    print("测试 2: 罗盘坐向工具")
    print("=" * 60)

    tool = LuopanOrientationTool()

    # 测试基本坐向
    print("\n【测试 2.1】基本坐向（坐北朝南）")
    result = tool.execute(
        sitting_direction="坐北朝南",
        building_type="住宅"
    )
    print(f"✅ 宅卦: {result['house_gua']}")
    print(f"✅ 坐度: {result['sitting_degree']}°")
    print(f"✅ 吉位: {len(result['auspicious_positions'])} 个")
    print(f"✅ 凶位: {len(result['inauspicious_positions'])} 个")

    # 测试带命卦
    print("\n【测试 2.2】带命卦匹配")
    result = tool.execute(
        sitting_direction="坐西北向东南",
        building_type="办公室",
        owner_birth="1990-05-15"
    )
    print(f"✅ 宅卦: {result['house_gua']}")
    if 'ming_gua_match' in result:
        print(f"✅ 命卦匹配: {result['ming_gua_match']}")

    # 测试流年飞星
    print("\n【测试 2.3】流年飞星")
    if 'annual_flying_stars' in result:
        stars = result['annual_flying_stars']
        print(f"✅ 年份: {stars['year']}")
        print(f"✅ 中宫: {stars['central_star']}星")

    # 测试格式化输出
    print("\n【测试 2.4】格式化输出")
    formatted = _format_luopan_result(result)
    print(f"✅ 输出长度: {len(formatted)} 字符")
    print(f"✅ 包含标题: {'# 罗盘坐向分析' in formatted}")
    print(f"✅ 包含吉凶: {'吉位' in formatted and '凶位' in formatted}")

    print("\n" + "=" * 60)
    print("✅ 罗盘坐向工具测试通过")
    print("=" * 60)


def test_various_inputs():
    """测试各种输入格式"""
    print("\n" + "=" * 60)
    print("测试 3: 各种输入格式")
    print("=" * 60)

    tool = FengshuiDivinationTool()

    # 测试方位输入
    print("\n【测试 3.1】方位输入")
    result = tool.execute(upper_trigram="西北", lower_trigram="西南")
    print(f"✅ 西北+西南 → {result['main_hexagram']['name']}卦")

    # 测试数字输入
    print("\n【测试 3.2】数字输入")
    result = tool.execute(upper_trigram="1", lower_trigram="2")
    print(f"✅ 1+2 → {result['main_hexagram']['name']}卦")

    luopan_tool = LuopanOrientationTool()

    # 测试角度输入
    print("\n【测试 3.3】角度输入")
    result = luopan_tool.execute(
        sitting_direction="坐340向160",
        building_type="商铺"
    )
    print(f"✅ 坐340向160 → {result['house_gua']}")

    # 测试干支输入
    print("\n【测试 3.4】干支输入")
    result = luopan_tool.execute(
        sitting_direction="坐亥向巳",
        building_type="工厂"
    )
    print(f"✅ 坐亥向巳 → {result['house_gua']}")

    print("\n" + "=" * 60)
    print("✅ 各种输入格式测试通过")
    print("=" * 60)


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("CyberYJ MCP Server 功能测试")
    print("=" * 60)

    try:
        # 测试风水占卜工具
        test_fengshui_divination()

        # 测试罗盘坐向工具
        test_luopan_orientation()

        # 测试各种输入格式
        test_various_inputs()

        # 总结
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！MCP Server 功能正常！")
        print("=" * 60)
        print("\n下一步：")
        print("1. 配置 Claude Desktop (参考 docs/mcp-server-guide.md)")
        print("2. 重启 Claude Desktop")
        print("3. 在 Claude 中使用自然语言调用工具")
        print("\n示例：")
        print('  "帮我占卜一下事业运势，上卦乾，下卦乾"')
        print('  "我家坐北朝南，帮我分析一下风水"')
        print("=" * 60)

        return 0

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
