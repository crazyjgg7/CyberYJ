# CyberYJ MCP Server 配置指南

## 安装

### 1. 安装依赖

```bash
cd /Users/apple/dev/CyberYJ
pip install -e .
pip install -e ".[dev]"
pip install mcp ephem pytz
```

### 2. 配置 Claude Desktop

编辑 Claude Desktop 配置文件：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "cyberYJ": {
      "command": "python3",
      "args": [
        "/Users/apple/dev/CyberYJ/run_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/apple/dev/CyberYJ/src"
      }
    }
  }
}
```

### 3. 重启 Claude Desktop

配置完成后，重启 Claude Desktop 应用。

## 使用方法

### 关键词路由（可选）

可直接用本地路由将“风水/罗盘”关键词文本转换为 MCP 调用参数：

```bash
PYTHONPATH=src python3 - <<'PY'
from cyberYJ.dialog.router import route_message

print(route_message("风水：上坤下乾，问事业"))
print(route_message("罗盘：坐北朝南 住宅"))
PY
```

### 最小 CLI 演示（keyword_dispatch）

```bash
PYTHONPATH=src python3 /Users/apple/dev/CyberYJ/demo_cli.py "风水：上坤下乾，问事业"
PYTHONPATH=src python3 /Users/apple/dev/CyberYJ/demo_cli.py "罗盘：坐北朝南 住宅"
```

### 端到端 MCP 演示（keyword_dispatch）

```bash
python3 /Users/apple/dev/CyberYJ/demo_mcp_dispatch.py "风水：上坤下乾，问事业"
python3 /Users/apple/dev/CyberYJ/demo_mcp_dispatch.py "罗盘：坐北朝南 住宅"
```

### 工具 1: fengshui_divination（易经解卦）

**功能**: 易经六十四卦解卦分析

**参数**:
- `upper_trigram` (必需): 上卦，支持卦名/数字/方位
  - 示例: "乾"、"1"、"西北"
- `lower_trigram` (必需): 下卦，支持卦名/数字/方位
  - 示例: "坤"、"2"、"西南"
- `question_type` (可选): 问题类型
  - 可选值: "命运"、"流年"、"运势"、"事业"、"工作"、"职业"、"求职"、"创业"、"感情"、"爱情"、"婚姻"、"恋爱"、"财运"、"财富"、"投资"、"健康"、"学业"、"考试"、"家庭"、"出行"、"诉讼"
- `question_text` (可选): 用户问题原文（用于智能场景识别）
- `changing_line` (可选): 变爻位置（1-6）
- `timestamp` (可选): RFC3339 时间戳
- `timezone` (可选): 时区，默认 "Asia/Shanghai"

**示例对话**:

```
用户: 帮我占卜一下事业运势，上卦乾，下卦乾

Claude 会调用: fengshui_divination
参数: {
  "upper_trigram": "乾",
  "lower_trigram": "乾",
  "question_type": "事业"
}
```

```
用户: 我想问感情，上卦是西北方，下卦是西南方，初爻变

Claude 会调用: fengshui_divination
参数: {
  "upper_trigram": "西北",
  "lower_trigram": "西南",
  "question_type": "感情",
  "changing_line": 1
}
```

**关键词入口示例（风水：）**:

```
用户: 风水：上坤下乾，问事业

Claude 会调用: fengshui_divination
参数: {
  "upper_trigram": "坤",
  "lower_trigram": "乾",
  "question_type": "事业",
  "question_text": "上坤下乾，问事业"
}
```

### 工具 2: luopan_orientation（罗盘坐向）

**功能**: 罗盘坐向分析，提供八宅吉凶方位、宅盘 + 流年叠加与布局建议

**参数**:
- `sitting_direction` (必需): 坐向
  - 支持格式: "坐北朝南"、"坐340向160"、"坐亥向巳"
- `building_type` (必需): 建筑类型
  - 可选值: "住宅"、"办公室"、"商铺"、"工厂"
- `owner_birth` (可选): 公历生日（YYYY-MM-DD）
- `timestamp` (可选): RFC3339 时间戳
- `timezone` (可选): 时区，默认 "Asia/Shanghai"

**示例对话**:

```
用户: 我家坐北朝南，帮我分析一下风水

Claude 会调用: luopan_orientation
参数: {
  "sitting_direction": "坐北朝南",
  "building_type": "住宅"
}
```

```
用户: 我的办公室坐西北向东南，我是1990年5月15日出生的，帮我看看风水

Claude 会调用: luopan_orientation
参数: {
  "sitting_direction": "坐西北向东南",
  "building_type": "办公室",
  "owner_birth": "1990-05-15"
}
```

**关键词入口示例（罗盘：）**:

```
用户: 罗盘：坐北朝南 住宅

Claude 会调用: luopan_orientation
参数: {
  "sitting_direction": "坐北朝南",
  "building_type": "住宅"
}
```

### 工具 3: solar_terms_lookup（节气查询）

**功能**: 查询当前节气与下一节气

**参数**:
- `timestamp` (可选): RFC3339 时间戳
- `timezone` (可选): 时区，默认 "Asia/Shanghai"

**示例对话**:

```
用户: 现在是什么节气？

Claude 会调用: solar_terms_lookup
参数: {
  "timestamp": "2026-02-11T10:00:00+08:00",
  "timezone": "Asia/Shanghai"
}
```

### 工具 4: keyword_router（关键词路由）

**功能**: 将“风水/罗盘”关键词文本转换为 MCP 调用参数

**参数**:
- `text` (必选): 原始用户输入文本

**示例对话**:

```
用户: 风水：上坤下乾，问事业

Claude 会调用: keyword_router
参数: {
  "text": "风水：上坤下乾，问事业"
}
```

### 工具 5: keyword_dispatch（关键词一键调用）

**功能**: 自动路由并调用对应工具，直接返回最终结果

**参数**:
- `text` (必选): 原始用户输入文本

**示例对话**:

```
用户: 罗盘：坐北朝南 住宅

Claude 会调用: keyword_dispatch
参数: {
  "text": "罗盘：坐北朝南 住宅"
}
```

## 测试 MCP Server

### 方法 1: 使用 MCP Inspector

```bash
# 安装 MCP Inspector
npm install -g @modelcontextprotocol/inspector

# 运行 Inspector
mcp-inspector python3 /Users/apple/dev/CyberYJ/run_server.py
```

### 方法 2: 直接测试

```bash
cd /Users/apple/dev/CyberYJ
PYTHONPATH=src python3 run_server.py
```

然后通过 stdin/stdout 发送 JSON-RPC 请求。

### 方法 3: 单元测试

```bash
cd /Users/apple/dev/CyberYJ
PYTHONPATH=src pytest tests/ -v
```

## 输出格式（JSON + meta）

### 风水占卜输出

```json
{
  "tool": "fengshui_divination",
  "data": {
    "main_hexagram": {
      "id": 1,
      "name": "乾",
      "symbol": "䷀",
      "judgment": "元亨，利贞。",
      "image": "天行健，君子以自强不息。",
      "upper_trigram": "乾",
      "lower_trigram": "乾"
    },
    "five_elements": "上下卦比和（金）",
    "solar_term_influence": "当前节气为立春",
    "fortune_advice": "宜积极进取",
    "do_dont": {
      "do": ["自强不息"],
      "dont": ["骄傲自满"]
    },
    "trace": ["步骤1", "步骤2"],
    "sources": ["来源1"]
  },
  "meta": {
    "success": true,
    "schema_version": "1.0",
    "trace_count": 2,
    "sources_count": 1
  }
}
```

### 罗盘坐向输出

```json
{
  "tool": "luopan_orientation",
  "data": {
    "direction_class": "壬山 (北方)",
    "house_gua": "坎宅",
    "sitting_degree": 0.0,
    "facing_degree": 180.0,
    "auspicious_positions": ["生气位（东南方）"],
    "inauspicious_positions": ["绝命位（西方）"],
    "annual_flying_stars": {
      "year": 2026,
      "central_star": 2,
      "palace_map": {"中宫": 2, "坎": 1}
    },
    "house_flying_stars": {
      "period": 9,
      "sitting_mountain": "壬",
      "palace_map": {"中宫": {"mountain_star": 9, "facing_star": 9}}
    },
    "combined_flying_stars": {
      "中宫": {"mountain_star": 9, "facing_star": 9, "annual_star": 2, "score": 2, "level": "auspicious"}
    },
    "current_auspicious_positions": ["中宫"],
    "current_inauspicious_positions": ["坎"],
    "layout_tips": ["主卧宜设在生气位"],
    "trace": ["步骤1", "步骤2"],
    "sources": ["来源1"]
  },
  "meta": {
    "success": true,
    "schema_version": "1.0",
    "trace_count": 2,
    "sources_count": 1
  }
}
```

## 错误输出（统一格式）

MCP 工具错误会返回 JSON 字符串：

```json
{
  "tool": "fengshui_divination",
  "data": {},
  "meta": {
    "success": false,
    "schema_version": "1.0",
    "error": {
      "type": "ValueError",
      "message": "upper_trigram 为必填参数"
    }
  }
}
```

## 故障排查

### 问题 1: Server 无法启动

**检查**:
1. Python 版本是否 >= 3.8
2. 依赖是否全部安装
3. PYTHONPATH 是否正确设置

```bash
python3 --version
pip3 list | grep mcp
echo $PYTHONPATH
```

### 问题 2: 工具调用失败

**检查**:
1. 查看 Claude Desktop 日志
2. 检查数据文件是否完整

```bash
ls -la /Users/apple/dev/CyberYJ/data/
```

### 问题 3: 输出乱码

**检查**:
1. 确保终端支持 UTF-8
2. 检查 locale 设置

```bash
locale
export LANG=zh_CN.UTF-8
```

## 高级配置

### 自定义时区

在配置文件中添加环境变量：

```json
{
  "mcpServers": {
    "cyberYJ": {
      "command": "python3",
      "args": ["/Users/apple/dev/CyberYJ/run_server.py"],
      "env": {
        "PYTHONPATH": "/Users/apple/dev/CyberYJ/src",
        "TZ": "Asia/Shanghai"
      }
    }
  }
}
```

### 日志配置

修改 `src/cyberYJ/server/mcp_server.py` 中的日志级别：

```python
logging.basicConfig(level=logging.DEBUG)  # 更详细的日志
```

## 数据来源

所有分析结果均基于权威来源：

- **卦辞象辞**: CTP《周易》(https://ctext.org/book-of-changes)
- **节气数据**: 中国气象局
- **罗盘山向**: 青囊奥语
- **八宅规则**: 八宅明镜
- **玄空飞星**: 地理辨正疏

## 支持

如有问题，请查看：
- 项目文档: `/Users/apple/dev/CyberYJ/docs/`
- 测试用例: `/Users/apple/dev/CyberYJ/tests/`
- 项目进度: `/Users/apple/dev/CyberYJ/docs/project-progress.md`
