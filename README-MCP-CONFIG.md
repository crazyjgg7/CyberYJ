# CyberYJ MCP Server 配置指南

易经风水 MCP 服务的配置说明，适用于不同的 IDE 和工具。

## 📦 MCP Server 信息

- **名称**: CyberYJ
- **描述**: 易经风水 MCP 服务 - 提供六十四卦解卦分析和罗盘坐向分析
- **版本**: 0.1.0
- **协议**: stdio (标准输入输出)

## 🔧 核心配置参数

所有 IDE 的配置都需要这三个核心参数：

```json
{
  "command": "/Users/apple/dev/CyberYJ/venv/bin/python",
  "args": ["/Users/apple/dev/CyberYJ/run_server.py"],
  "env": {
    "PYTHONPATH": "/Users/apple/dev/CyberYJ/src"
  }
}
```

### 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| `command` | Python 解释器路径（使用虚拟环境） | ✅ 是 |
| `args` | 启动脚本路径 | ✅ 是 |
| `env.PYTHONPATH` | Python 模块搜索路径 | ✅ 是 |

## 🎯 不同 IDE 的配置方法

### 1. Claude Desktop (macOS)

**配置文件位置**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**配置内容**: 参考 `mcp-config-claude-desktop.json`

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

**配置步骤**:
1. 打开配置文件
2. 在 `mcpServers` 对象中添加 `CyberYJ` 配置
3. 保存文件
4. 重启 Claude Desktop

---

### 2. Claude Code CLI

**配置方法**: 使用命令行

```bash
cd /Users/apple/dev/CyberYJ
claude mcp add CyberYJ -- /Users/apple/dev/CyberYJ/venv/bin/python /Users/apple/dev/CyberYJ/run_server.py
```

**验证配置**:
```bash
claude mcp list
claude mcp get CyberYJ
```

**配置文件位置**: `~/.claude.json` (自动生成，不需要手动编辑)

---

### 3. Cursor IDE

**配置文件位置**: `~/.cursor/mcp.json` 或项目根目录的 `.cursor/mcp.json`

**配置内容**: 参考 `mcp-config-cursor.json`

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

**配置步骤**:
1. 打开 Cursor 设置
2. 找到 MCP 配置选项
3. 添加上述配置
4. 重启 Cursor

---

### 4. VS Code (需要 MCP 扩展)

**配置文件位置**: `.vscode/settings.json` (项目级) 或 `~/Library/Application Support/Code/User/settings.json` (全局)

**配置内容**: 参考 `mcp-config-vscode.json`

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

**前置要求**:
- 需要安装支持 MCP 的 VS Code 扩展
- 目前 VS Code 对 MCP 的支持还在发展中

---

### 5. Windsurf IDE

**配置文件位置**: `~/.windsurf/mcp.json`

**配置内容**: 与 Cursor 相同

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

---

### 6. Zed Editor

**配置文件位置**: `~/.config/zed/settings.json`

**配置内容**:
```json
{
  "language_models": {
    "mcp_servers": {
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

---

## 🛠️ 提供的工具

配置成功后，以下工具将可用：

### 1. `fengshui_divination` - 易经六十四卦解卦

**参数**:
- `upper_trigram` (必需): 上卦，如 "乾"、"坤"、"西北"、"1"
- `lower_trigram` (必需): 下卦，如 "巽"、"坎"、"东南"、"5"
- `question_type` (可选): 问题类型，可选值: "事业"、"财运"、"感情"、"健康"
- `changing_line` (可选): 变爻位置，1-6
- `timestamp` (可选): RFC3339 时间戳
- `timezone` (可选): 时区，默认 "Asia/Shanghai"

**示例提问**:
- "帮我占卜一下事业运势，上卦乾，下卦巽"
- "我想问财运，上卦坤，下卦乾，第三爻动"
- "解读一下天风姤卦"

### 2. `luopan_orientation` - 罗盘坐向分析

**参数**:
- `sitting_direction` (必需): 坐向，如 "坐北朝南"、"坐340向160"、"坐亥向巳"
- `building_type` (必需): 建筑类型，可选值: "住宅"、"办公室"、"商铺"、"工厂"
- `owner_birth` (可选): 公历生日，格式 "YYYY-MM-DD"
- `timestamp` (可选): RFC3339 时间戳
- `timezone` (可选): 时区，默认 "Asia/Shanghai"

**示例提问**:
- "我家坐北朝南，是住宅，帮我分析风水"
- "办公室坐西北向东南，我是1990年5月15日出生的，合适吗？"
- "坐340向160的商铺，风水如何？"

---

## ✅ 验证配置

### 方法 1: 命令行测试

```bash
cd /Users/apple/dev/CyberYJ
./venv/bin/python test_server.py
```

### 方法 2: 直接调用

```bash
cd /Users/apple/dev/CyberYJ
./venv/bin/python -c "
import sys
sys.path.insert(0, 'src')
from cyberYJ.tools.fengshui_divination import FengshuiDivinationTool

tool = FengshuiDivinationTool()
result = tool.execute(upper_trigram='乾', lower_trigram='巽')
print(f'✅ 测试成功！卦名: {result[\"main_hexagram\"][\"name\"]}')
"
```

### 方法 3: 在 IDE 中测试

配置完成后，在 IDE 中直接提问：
- "帮我占卜一下，上卦乾，下卦巽"

如果看到详细的卦象分析，说明配置成功！

---

## 🐛 常见问题

### 1. 提示 "ModuleNotFoundError: No module named 'mcp'"

**解决方案**:
```bash
cd /Users/apple/dev/CyberYJ
./venv/bin/pip install mcp pytz ephem
```

### 2. 提示 "架构不兼容" (x86_64 vs arm64)

**解决方案**: 使用虚拟环境的 Python，而不是系统 Python
```bash
# 确保使用虚拟环境
/Users/apple/dev/CyberYJ/venv/bin/python
```

### 3. IDE 检测不到 MCP server

**解决方案**:
1. 检查配置文件路径是否正确
2. 重启 IDE
3. 查看 IDE 的 MCP 日志（如果有）

### 4. 工具调用失败

**解决方案**:
```bash
# 检查 MCP server 是否能正常启动
cd /Users/apple/dev/CyberYJ
./venv/bin/python run_server.py
# 应该等待输入，不报错
```

---

## 📚 数据来源

所有占卜结果基于以下权威来源：

- **周易（易经）** - https://ctext.org/book-of-changes
- **二十四节气那些事儿**
- **青囊奥语** - 二十四山向
- **八宅明镜** - 八宅规则
- **地理辨正疏** - 玄空飞星规则

---

## 📞 支持

如有问题，请查看：
- 项目 README: `/Users/apple/dev/CyberYJ/README.md`
- 测试脚本: `/Users/apple/dev/CyberYJ/test_server.py`
- 桌面启动脚本: `/Users/apple/Desktop/start-cyberYJ-mcp.command`

---

## 📄 许可证

MIT License

---

**版本**: 0.1.0
**更新日期**: 2026-02-09
