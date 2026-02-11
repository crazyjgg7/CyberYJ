#!/usr/bin/env python3
"""
端到端演示：通过 MCP 调用 keyword_dispatch
用法:
  python3 demo_mcp_dispatch.py "风水：上坤下乾，问事业"
  python3 demo_mcp_dispatch.py "罗盘：坐北朝南 住宅"
"""

import json
import sys
from pathlib import Path

import anyio

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


ROOT = Path(__file__).resolve().parent


async def _run(text: str) -> int:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "run_server.py")],
        env={"PYTHONPATH": str(ROOT / "src")},
        cwd=str(ROOT),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("keyword_dispatch", {"text": text})

            if not result.content:
                print(json.dumps({"error": "empty response"}, ensure_ascii=False))
                return 1

            content = result.content[0]
            text_payload = getattr(content, "text", None)
            if text_payload is None:
                print(json.dumps({"error": "unexpected content"}, ensure_ascii=False))
                return 1

            try:
                parsed = json.loads(text_payload)
                print(json.dumps(parsed, ensure_ascii=False, indent=2))
            except Exception:
                print(text_payload)
            return 0


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 demo_mcp_dispatch.py \"风水：上坤下乾，问事业\"")
        return 1
    return anyio.run(_run, sys.argv[1].strip())


if __name__ == "__main__":
    raise SystemExit(main())
