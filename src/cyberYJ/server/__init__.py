"""
cyberYJ.server 包入口
采用延迟导入，避免在未安装 mcp 时触发导入错误。
"""

from typing import Any

__all__ = [
    "app",
    "main",
    "_format_fengshui_result",
    "_format_luopan_result",
    "_format_solar_terms_result",
]


def __getattr__(name: str) -> Any:
    if name in __all__:
        from cyberYJ.server import mcp_server
        return getattr(mcp_server, name)
    raise AttributeError(f"module 'cyberYJ.server' has no attribute '{name}'")
