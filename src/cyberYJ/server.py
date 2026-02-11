"""
DEPRECATED: 该模块已迁移至 `cyberYJ.server.mcp_server`。
请使用 `from cyberYJ.server import main` 或直接导入新的模块。

CyberYJ MCP Server

提供易经风水分析的 MCP 服务，包含两个工具：
1. fengshui_divination - 易经六十四卦解卦分析
2. luopan_orientation - 罗盘坐向分析
"""

import asyncio
import logging
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool
from cyberYJ.tools.luopan_orientation import LuopanOrientationTool

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cyberYJ-mcp-server")

# 创建 MCP Server 实例
app = Server("cyberYJ-mcp-server")

# 初始化工具实例
fengshui_tool = FengshuiDivinationTool()
luopan_tool = LuopanOrientationTool()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """列出所有可用的工具"""
    return [
        Tool(
            name="fengshui_divination",
            description="易经六十四卦解卦分析（八宅 + 玄空飞星体系下的节气影响解释）",
            inputSchema={
                "type": "object",
                "properties": {
                    "upper_trigram": {
                        "type": "string",
                        "description": "上卦（卦名/数字/方位），如：乾、1、西北"
                    },
                    "lower_trigram": {
                        "type": "string",
                        "description": "下卦（卦名/数字/方位），如：坤、2、西南"
                    },
                    "question_type": {
                        "type": "string",
                        "enum": ["事业", "财运", "感情", "健康"],
                        "description": "问题类型（可选）"
                    },
                    "changing_line": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 6,
                        "description": "变爻位置（1-6，可选）"
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "RFC3339 时间戳（可选，默认当前时间）"
                    },
                    "timezone": {
                        "type": "string",
                        "description": "IANA 时区名（可选，默认 Asia/Shanghai）"
                    }
                },
                "required": ["upper_trigram", "lower_trigram"]
            }
        ),
        Tool(
            name="luopan_orientation",
            description="罗盘坐向分析（八宅 + 玄空飞星）",
            inputSchema={
                "type": "object",
                "properties": {
                    "sitting_direction": {
                        "type": "string",
                        "description": "坐向，支持多种格式：坐北朝南 / 坐340向160 / 坐亥向巳"
                    },
                    "building_type": {
                        "type": "string",
                        "enum": ["住宅", "办公室", "商铺", "工厂"],
                        "description": "建筑类型"
                    },
                    "owner_birth": {
                        "type": "string",
                        "description": "公历生日（YYYY-MM-DD，可选，用于命卦匹配）"
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "RFC3339 时间戳（可选，默认当前时间）"
                    },
                    "timezone": {
                        "type": "string",
                        "description": "IANA 时区名（可选，默认 Asia/Shanghai）"
                    }
                },
                "required": ["sitting_direction", "building_type"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """调用工具"""
    try:
        if name == "fengshui_divination":
            # 调用风水占卜工具
            result = fengshui_tool.execute(
                upper_trigram=arguments["upper_trigram"],
                lower_trigram=arguments["lower_trigram"],
                question_type=arguments.get("question_type"),
                changing_line=arguments.get("changing_line"),
                timestamp=arguments.get("timestamp"),
                timezone=arguments.get("timezone", "Asia/Shanghai")
            )

            # 格式化输出
            output = _format_fengshui_result(result)

            return [TextContent(type="text", text=output)]

        elif name == "luopan_orientation":
            # 调用罗盘坐向工具
            result = luopan_tool.execute(
                sitting_direction=arguments["sitting_direction"],
                building_type=arguments["building_type"],
                owner_birth=arguments.get("owner_birth"),
                timestamp=arguments.get("timestamp"),
                timezone=arguments.get("timezone", "Asia/Shanghai")
            )

            # 格式化输出
            output = _format_luopan_result(result)

            return [TextContent(type="text", text=output)]

        else:
            raise ValueError(f"未知的工具: {name}")

    except Exception as e:
        logger.error(f"工具调用失败: {name}, 错误: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=f"❌ 工具调用失败: {str(e)}"
        )]


def _format_fengshui_result(result: dict) -> str:
    """格式化风水占卜结果"""
    lines = []

    # 标题
    lines.append("# 易经六十四卦解卦分析")
    lines.append("")

    # 本卦信息
    hexagram = result["main_hexagram"]
    lines.append(f"## 本卦：第{hexagram['id']}卦 {hexagram['symbol']} {hexagram['name']}卦")
    lines.append("")
    lines.append(f"**上卦**: {hexagram['upper_trigram']} | **下卦**: {hexagram['lower_trigram']}")
    lines.append("")
    lines.append(f"**卦辞**: {hexagram['judgment']}")
    lines.append("")
    lines.append(f"**象辞**: {hexagram['image']}")
    lines.append("")

    # 五行分析
    lines.append("## 五行分析")
    lines.append("")
    lines.append(result["five_elements"])
    lines.append("")

    # 节气影响
    lines.append("## 节气影响")
    lines.append("")
    lines.append(result["solar_term_influence"])
    lines.append("")

    # 变卦（如果有）
    if "changing_hexagram" in result:
        changing = result["changing_hexagram"]
        lines.append(f"## 变卦：第{changing['id']}卦 {changing['name']}卦")
        lines.append("")
        lines.append(f"**卦辞**: {changing['judgment']}")
        lines.append("")
        lines.append(f"**解释**: {changing['interpretation']}")
        lines.append("")

    # 趋吉避凶建议
    lines.append("## 趋吉避凶建议")
    lines.append("")
    lines.append(result["fortune_advice"])
    lines.append("")

    # 宜忌
    if "do_dont" in result:
        do_dont = result["do_dont"]
        lines.append("### 宜")
        for item in do_dont["do"]:
            lines.append(f"- ✅ {item}")
        lines.append("")

        lines.append("### 忌")
        for item in do_dont["dont"]:
            lines.append(f"- ❌ {item}")
        lines.append("")

    # 推导路径
    lines.append("## 推导路径")
    lines.append("")
    for i, step in enumerate(result["trace"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    # 数据来源
    if "sources" in result and result["sources"]:
        lines.append("## 数据来源")
        lines.append("")
        for source in result["sources"]:
            lines.append(f"- {source}")
        lines.append("")

    return "\n".join(lines)


def _format_luopan_result(result: dict) -> str:
    """格式化罗盘坐向结果"""
    lines = []

    # 标题
    lines.append("# 罗盘坐向分析")
    lines.append("")

    # 基本信息
    lines.append("## 基本信息")
    lines.append("")
    lines.append(f"**坐向**: {result['direction_class']}")
    lines.append(f"**坐度**: {result['sitting_degree']:.1f}°")
    lines.append(f"**向度**: {result['facing_degree']:.1f}°")
    lines.append(f"**宅卦**: {result['house_gua']}")
    lines.append("")

    # 命卦匹配（如果有）
    if "ming_gua_match" in result:
        lines.append(f"**命卦匹配**: {result['ming_gua_match']}")
        if "compatibility_advice" in result:
            lines.append(f"**建议**: {result['compatibility_advice']}")
        lines.append("")

    # 吉凶方位
    lines.append("## 八宅吉凶方位")
    lines.append("")

    lines.append("### 吉位（四吉）")
    for pos in result["auspicious_positions"]:
        lines.append(f"- ✅ {pos}")
    lines.append("")

    lines.append("### 凶位（四凶）")
    for pos in result["inauspicious_positions"]:
        lines.append(f"- ❌ {pos}")
    lines.append("")

    # 流年飞星（如果有）
    if "annual_flying_stars" in result:
        stars = result["annual_flying_stars"]
        lines.append(f"## {stars['year']}年流年飞星")
        lines.append("")
        lines.append(f"**中宫**: {stars['central_star']}星")
        lines.append("")
        lines.append("**九宫分布**:")
        palace_map = stars["palace_map"]
        for palace, star in palace_map.items():
            lines.append(f"- {palace}: {star}星")
        lines.append("")

    # 布局建议
    lines.append("## 布局建议")
    lines.append("")
    for i, tip in enumerate(result["layout_tips"], 1):
        lines.append(f"{i}. {tip}")
    lines.append("")

    # 推导路径
    lines.append("## 推导路径")
    lines.append("")
    for i, step in enumerate(result["trace"], 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    # 数据来源
    if "sources" in result and result["sources"]:
        lines.append("## 数据来源")
        lines.append("")
        for source in result["sources"]:
            lines.append(f"- {source}")
        lines.append("")

    return "\n".join(lines)


async def main():
    """主函数"""
    logger.info("启动 CyberYJ MCP Server...")

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
