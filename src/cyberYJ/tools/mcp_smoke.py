"""
MCP 冒烟测试运行器（多 IDE 通用）
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import anyio


DEFAULT_SMOKE_CASES: List[Dict[str, str]] = [
    {
        "name": "fengshui_keyword_entry",
        "text": "风水：上坤下乾，问事业",
        "expected_tool": "fengshui_divination",
    },
    {
        "name": "luopan_keyword_entry",
        "text": "罗盘：坐北朝南 住宅",
        "expected_tool": "luopan_orientation",
    },
]


def validate_response_payload(payload: Dict[str, Any], expected_tool: str) -> List[str]:
    """
    校验统一前端响应协议：tool + data + meta（含 trace/sources）
    """
    errors: List[str] = []

    if not isinstance(payload, dict):
        return ["payload must be an object"]

    for key in ("tool", "data", "meta"):
        if key not in payload:
            errors.append(f"missing field: {key}")

    if "tool" in payload and payload["tool"] != expected_tool:
        errors.append(f"tool mismatch: expected {expected_tool}, got {payload['tool']}")

    data = payload.get("data")
    if isinstance(data, dict):
        if "trace" not in data:
            errors.append("data.trace must exist")
        elif not isinstance(data.get("trace"), list):
            errors.append("data.trace must be a list")

        if "sources" not in data:
            errors.append("data.sources must exist")
        elif not isinstance(data.get("sources"), list):
            errors.append("data.sources must be a list")
    elif "data" in payload:
        errors.append("data must be an object")

    meta = payload.get("meta")
    if isinstance(meta, dict):
        if "success" not in meta:
            errors.append("meta.success must exist")
        elif meta.get("success") is not True:
            errors.append("meta.success must be true")
    elif "meta" in payload:
        errors.append("meta must be an object")

    return errors


async def run_smoke_cases(
    cases: Optional[List[Dict[str, str]]] = None,
    root: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    """
    通过真实 MCP stdio 调用 keyword_dispatch，执行固定冒烟用例。
    """
    root_path = root or Path(__file__).resolve().parents[3]
    use_cases = cases or DEFAULT_SMOKE_CASES

    try:
        from mcp.client.session import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client
    except Exception as exc:  # pragma: no cover - runtime env dependent
        return _run_cases_via_demo_subprocess(
            use_cases=use_cases,
            root_path=root_path,
            bootstrap_error=str(exc),
        )

    results: List[Dict[str, Any]] = []

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(root_path / "run_server.py")],
        env={"PYTHONPATH": str(root_path / "src")},
        cwd=str(root_path),
    )

    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                for case in use_cases:
                    case_result = {
                        "name": case["name"],
                        "text": case["text"],
                        "expected_tool": case["expected_tool"],
                        "ok": False,
                        "errors": [],
                        "payload": None,
                    }
                    try:
                        response = await session.call_tool(
                            "keyword_dispatch",
                            {"text": case["text"]},
                        )
                        if not response.content:
                            case_result["errors"].append("empty response content")
                        else:
                            content = response.content[0]
                            text_payload = getattr(content, "text", None)
                            if text_payload is None:
                                case_result["errors"].append("response content has no text payload")
                            else:
                                payload = json.loads(text_payload)
                                case_result["payload"] = payload
                                case_result["errors"] = validate_response_payload(
                                    payload,
                                    case["expected_tool"],
                                )
                    except Exception as exc:  # pragma: no cover - runtime env dependent
                        case_result["errors"].append(str(exc))

                    case_result["ok"] = len(case_result["errors"]) == 0
                    results.append(case_result)
    except Exception as exc:  # pragma: no cover - runtime env dependent
        return [
            {
                "name": "session",
                "text": "",
                "expected_tool": "",
                "ok": False,
                "errors": [str(exc)],
                "payload": None,
            }
        ]

    return results


def _run_cases_via_demo_subprocess(
    use_cases: List[Dict[str, str]],
    root_path: Path,
    bootstrap_error: str,
) -> List[Dict[str, Any]]:
    """
    当当前解释器无法导入 mcp 时，回退到项目 venv 子进程执行 demo_mcp_dispatch.py。
    """
    venv_python = root_path / "venv" / "bin" / "python"
    results: List[Dict[str, Any]] = []

    for case in use_cases:
        case_result: Dict[str, Any] = {
            "name": case["name"],
            "text": case["text"],
            "expected_tool": case["expected_tool"],
            "ok": False,
            "errors": [f"mcp import fallback: {bootstrap_error}"],
            "payload": None,
        }

        if not venv_python.exists():
            case_result["errors"].append(f"venv python not found: {venv_python}")
            results.append(case_result)
            continue

        proc = subprocess.run(
            [str(venv_python), str(root_path / "demo_mcp_dispatch.py"), case["text"]],
            cwd=str(root_path),
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            case_result["errors"].append(f"demo subprocess failed: rc={proc.returncode}")
            stderr_text = (proc.stderr or "").strip()
            if stderr_text:
                case_result["errors"].append(stderr_text)
            results.append(case_result)
            continue

        stdout_text = (proc.stdout or "").strip()
        try:
            payload = json.loads(stdout_text)
            case_result["payload"] = payload
            case_result["errors"] = validate_response_payload(payload, case["expected_tool"])
        except Exception as exc:
            case_result["errors"].append(f"invalid json payload: {exc}")

        case_result["ok"] = len(case_result["errors"]) == 0
        results.append(case_result)

    return results


def run_smoke_cases_sync(
    cases: Optional[List[Dict[str, str]]] = None,
    root: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    return anyio.run(run_smoke_cases, cases, root)
