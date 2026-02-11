"""
luopan_orientation MCP 工具处理器
"""

from typing import Any, Dict, Optional

from cyberYJ.tools.luopan_orientation import LuopanOrientationTool
from cyberYJ.server.validation import (
    require_fields,
    get_timezone,
    optional_type,
    validate_enum,
)


class CompassHandler:
    """罗盘坐向处理器"""

    def __init__(self, tool: Optional[LuopanOrientationTool] = None):
        self._tool = tool or LuopanOrientationTool()

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        require_fields(arguments, ["sitting_direction", "building_type"])
        timezone = get_timezone(arguments.get("timezone"))

        optional_type(arguments.get("sitting_direction"), str, "sitting_direction")
        optional_type(arguments.get("owner_birth"), str, "owner_birth")
        validate_enum(
            arguments.get("building_type"),
            ["住宅", "办公室", "商铺", "工厂"],
            "building_type"
        )

        return self._tool.execute(
            sitting_direction=arguments["sitting_direction"],
            building_type=arguments["building_type"],
            owner_birth=arguments.get("owner_birth"),
            timestamp=arguments.get("timestamp"),
            timezone=timezone
        )
