#!/usr/bin/env python3
"""
MCP 冒烟测试：
- 固定验证两个关键词入口：风水 / 罗盘
- 校验统一响应协议：tool + data + meta（含 trace/sources）
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cyberYJ.tools.mcp_smoke import run_smoke_cases_sync


def main() -> int:
    results = run_smoke_cases_sync(root=ROOT)

    print("=== CyberYJ MCP Smoke Test ===")
    ok_count = 0
    for item in results:
        status = "PASS" if item.get("ok") else "FAIL"
        print(f"[{status}] {item.get('name')} -> {item.get('expected_tool')}")
        if item.get("ok"):
            ok_count += 1
            continue
        for err in item.get("errors", []):
            print(f"  - {err}")
        payload = item.get("payload")
        if payload is not None:
            print("  payload:")
            print(json.dumps(payload, ensure_ascii=False, indent=2))

    total = len(results)
    print(f"Summary: {ok_count}/{total} passed")
    return 0 if ok_count == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
