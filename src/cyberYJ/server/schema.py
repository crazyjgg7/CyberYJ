"""
MCP 工具 schema 生成
"""

from typing import List

from mcp.types import Tool


def get_fengshui_tool() -> Tool:
    return Tool(
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
                    "enum": [
                        "命运", "流年", "运势",
                        "事业", "工作", "职业", "求职", "创业",
                        "感情", "爱情", "婚姻", "恋爱",
                        "财运", "财富", "投资",
                        "健康",
                        "学业", "考试",
                        "家庭",
                        "出行",
                        "诉讼"
                    ],
                    "description": "问题类型（可选）"
                },
                "question_text": {
                    "type": "string",
                    "description": "用户问题原文（用于智能场景识别，可选）"
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
    )


def get_luopan_tool() -> Tool:
    return Tool(
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


def get_solar_terms_tool() -> Tool:
    return Tool(
        name="solar_terms_lookup",
        description="节气查询（当前节气与下一个节气）",
        inputSchema={
            "type": "object",
            "properties": {
                "timestamp": {
                    "type": "string",
                    "description": "RFC3339 时间戳（可选，默认当前时间）"
                },
                "timezone": {
                    "type": "string",
                    "description": "IANA 时区名（可选，默认 Asia/Shanghai）"
                }
            },
            "required": []
        }
    )


def get_tools() -> List[Tool]:
    return [
        get_fengshui_tool(),
        get_luopan_tool(),
        get_solar_terms_tool(),
        get_keyword_router_tool(),
        get_keyword_dispatch_tool(),
    ]


def get_keyword_router_tool() -> Tool:
    return Tool(
        name="keyword_router",
        description="关键词路由（风水/罗盘）输入转 MCP 调用参数",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "原始用户输入文本（如：风水：上坤下乾，问事业）"
                }
            },
            "required": ["text"]
        }
    )


def get_keyword_dispatch_tool() -> Tool:
    return Tool(
        name="keyword_dispatch",
        description="关键词一键调用（风水/罗盘）",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "原始用户输入文本（如：风水：上坤下乾，问事业）"
                }
            },
            "required": ["text"]
        }
    )
