#!/usr/bin/env python3
"""
CyberYJ MCP Server 启动脚本
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cyberYJ.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
