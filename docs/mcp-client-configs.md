# CyberYJ 多 IDE MCP 配置模板（RC1）

更新时间：2026-02-11

目标：同一套服务在不同 IDE 使用一致配置，统一走 `run_server.py`。

## 通用参数（必须一致）

```json
{
  "command": "/Users/apple/dev/CyberYJ/venv/bin/python",
  "args": ["/Users/apple/dev/CyberYJ/run_server.py"],
  "env": {
    "PYTHONPATH": "/Users/apple/dev/CyberYJ/src"
  }
}
```

## 1) Claude Desktop

配置文件（macOS）：`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "CyberYJ": {
      "command": "/Users/apple/dev/CyberYJ/venv/bin/python",
      "args": ["/Users/apple/dev/CyberYJ/run_server.py"],
      "env": {
        "PYTHONPATH": "/Users/apple/dev/CyberYJ/src"
      }
    }
  }
}
```

## 2) Cursor

配置文件：`~/.cursor/mcp.json`（或项目 `.cursor/mcp.json`）

```json
{
  "mcpServers": {
    "CyberYJ": {
      "command": "/Users/apple/dev/CyberYJ/venv/bin/python",
      "args": ["/Users/apple/dev/CyberYJ/run_server.py"],
      "env": {
        "PYTHONPATH": "/Users/apple/dev/CyberYJ/src"
      }
    }
  }
}
```

## 3) Cline（VS Code 插件）

常见为 VS Code 全局 `settings.json` 中的 MCP 配置（不同版本可能键名不同，请以插件文档为准）：

```json
{
  "mcp": {
    "servers": {
      "CyberYJ": {
        "command": "/Users/apple/dev/CyberYJ/venv/bin/python",
        "args": ["/Users/apple/dev/CyberYJ/run_server.py"],
        "env": {
          "PYTHONPATH": "/Users/apple/dev/CyberYJ/src"
        }
      }
    }
  }
}
```

## 冒烟校验（统一）

执行：

```bash
cd /Users/apple/dev/CyberYJ
python3 scripts/mcp_smoke_test.py
```

预期：
- 固定 2 条用例均 `PASS`
- 返回结构满足 `tool + data + meta`
- `data.trace`、`data.sources` 均存在
