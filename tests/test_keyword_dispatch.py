import json

import pytest

pytest.importorskip("mcp")

from cyberYJ.server.mcp_server import call_tool


@pytest.mark.asyncio
async def test_keyword_dispatch_fengshui():
    resp = await call_tool("keyword_dispatch", {"text": "风水：上坤下乾，问事业"})
    payload = json.loads(resp[0].text)
    assert payload["tool"] == "fengshui_divination"
    assert payload["meta"]["success"] is True


@pytest.mark.asyncio
async def test_keyword_dispatch_luopan():
    resp = await call_tool("keyword_dispatch", {"text": "罗盘：坐北朝南 住宅"})
    payload = json.loads(resp[0].text)
    assert payload["tool"] == "luopan_orientation"
    assert payload["meta"]["success"] is True
