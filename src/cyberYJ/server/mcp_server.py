"""
CyberYJ MCP Server

提供易经风水分析的 MCP 服务，包含两个工具：
1. fengshui_divination - 易经六十四卦解卦分析
2. luopan_orientation - 罗盘坐向分析
"""

import asyncio
import json
import logging
from typing import Optional
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent

from cyberYJ.server.handlers.fengshui import FengshuiHandler
from cyberYJ.server.handlers.compass import CompassHandler
from cyberYJ.server.handlers.solar_terms import SolarTermsHandler
from cyberYJ.server.schema import get_tools
from cyberYJ.dialog.router import route_message

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cyberYJ-mcp-server")

# 创建 MCP Server 实例
app = Server("cyberYJ-mcp-server")

# 初始化工具实例
fengshui_handler = FengshuiHandler()
compass_handler = CompassHandler()
solar_terms_handler = SolarTermsHandler()


@app.list_tools()
async def list_tools():
    """列出所有可用的工具"""
    return get_tools()


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """调用工具"""
    try:
        if name == "fengshui_divination":
            result = fengshui_handler.execute(arguments)
            output = _format_fengshui_result(result)
            return [TextContent(type="text", text=output)]

        if name == "luopan_orientation":
            result = compass_handler.execute(arguments)
            output = _format_luopan_result(result)
            return [TextContent(type="text", text=output)]

        if name == "solar_terms_lookup":
            result = solar_terms_handler.execute(arguments)
            output = _format_solar_terms_result(result)
            return [TextContent(type="text", text=output)]

        if name == "keyword_router":
            route = route_message(arguments.get("text", ""))
            success = "error" not in route
            error = None
            if not success:
                error = {"type": "RouteError", "message": route.get("error", "unknown")}
            output = json.dumps(
                _wrap_response("keyword_router", route, success=success, error=error),
                ensure_ascii=False
            )
            return [TextContent(type="text", text=output)]

        if name == "keyword_dispatch":
            route = route_message(arguments.get("text", ""))
            if "error" in route:
                output = json.dumps(
                    _wrap_response(
                        "keyword_dispatch",
                        route,
                        success=False,
                        error={"type": "RouteError", "message": route.get("error", "unknown")},
                    ),
                    ensure_ascii=False
                )
                return [TextContent(type="text", text=output)]

            tool_name = route.get("tool")
            tool_args = route.get("arguments", {})

            if tool_name == "fengshui_divination":
                result = fengshui_handler.execute(tool_args)
                payload = _wrap_response("fengshui_divination", result)
            elif tool_name == "luopan_orientation":
                result = compass_handler.execute(tool_args)
                payload = _wrap_response("luopan_orientation", result)
            else:
                payload = _wrap_response(
                    "keyword_dispatch",
                    route,
                    success=False,
                    error={"type": "RouteError", "message": f"未知工具: {tool_name}"},
                )

            output = json.dumps(payload, ensure_ascii=False)
            return [TextContent(type="text", text=output)]

        raise ValueError(f"未知的工具: {name}")

    except Exception as e:
        logger.error(f"工具调用失败: {name}, 错误: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps(
                _wrap_response(
                    name,
                    data={},
                    success=False,
                    error={
                        "type": type(e).__name__,
                        "message": str(e),
                    },
                ),
                ensure_ascii=False
            )
        )]


def _format_fengshui_result(result: dict) -> str:
    """格式化风水占卜结果（JSON 输出）"""
    return json.dumps(_wrap_response("fengshui_divination", result), ensure_ascii=False)


def _format_luopan_result(result: dict) -> str:
    """格式化罗盘坐向结果（JSON 输出）"""
    return json.dumps(_wrap_response("luopan_orientation", result), ensure_ascii=False)


def _format_solar_terms_result(result: dict) -> str:
    """格式化节气查询结果（JSON 输出）"""
    return json.dumps(_wrap_response("solar_terms_lookup", result), ensure_ascii=False)


def _wrap_response(tool: str, data: dict, success: bool = True, error: Optional[dict] = None) -> dict:
    meta = {"success": success, "schema_version": "1.0"}
    if isinstance(data, dict):
        trace = data.get("trace")
        sources = data.get("sources")
        if isinstance(trace, list):
            meta["trace_count"] = len(trace)
        if isinstance(sources, list):
            meta["sources_count"] = len(sources)
    if error:
        meta["error"] = error
    return {"tool": tool, "data": data, "meta": meta}


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
