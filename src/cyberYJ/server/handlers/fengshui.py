"""
fengshui_divination MCP 工具处理器
"""

from typing import Any, Dict, Optional

from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool
from cyberYJ.server.validation import (
    require_fields,
    get_timezone,
    optional_type,
    validate_int_range,
)


class FengshuiHandler:
    """风水占卜处理器"""

    def __init__(self, tool: Optional[FengshuiDivinationTool] = None):
        self._tool = tool or FengshuiDivinationTool()

    def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        require_fields(arguments, ["upper_trigram", "lower_trigram"])
        timezone = get_timezone(arguments.get("timezone"))

        optional_type(arguments.get("question_type"), str, "question_type")
        optional_type(arguments.get("question_text"), str, "question_text")
        validate_int_range(arguments.get("changing_line"), 1, 6, "changing_line")

        return self._tool.execute(
            upper_trigram=arguments["upper_trigram"],
            lower_trigram=arguments["lower_trigram"],
            question_type=arguments.get("question_type"),
            question_text=arguments.get("question_text"),
            changing_line=arguments.get("changing_line"),
            timestamp=arguments.get("timestamp"),
            timezone=timezone
        )
