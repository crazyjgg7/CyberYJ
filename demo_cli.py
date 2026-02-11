#!/usr/bin/env python3
"""
最小演示：关键词一键调用
用法:
  PYTHONPATH=src python3 demo_cli.py "风水：上坤下乾，问事业"
  PYTHONPATH=src python3 demo_cli.py "罗盘：坐北朝南 住宅"
"""

import json
import sys

from cyberYJ.dialog.router import route_message
from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool
from cyberYJ.tools.luopan_orientation import LuopanOrientationTool
from cyberYJ.server.mcp_server import _wrap_response


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 demo_cli.py \"风水：上坤下乾，问事业\"")
        return 1

    text = sys.argv[1].strip()
    route = route_message(text)

    if "error" in route:
        payload = _wrap_response(
            "keyword_dispatch",
            route,
            success=False,
            error={"type": "RouteError", "message": route["error"]},
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    tool = route["tool"]
    args = route.get("arguments", {})

    if tool == "fengshui_divination":
        result = FengshuiDivinationTool().execute(**args)
        payload = _wrap_response("fengshui_divination", result)
    elif tool == "luopan_orientation":
        result = LuopanOrientationTool().execute(**args)
        payload = _wrap_response("luopan_orientation", result)
    else:
        payload = _wrap_response(
            "keyword_dispatch",
            route,
            success=False,
            error={"type": "RouteError", "message": f"未知工具: {tool}"},
        )

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
