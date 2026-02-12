# CyberYJ - 玄学知识库 + MCP 服务

易经 + 风水（八宅、玄空飞星）结构化 MCP 工具能力

## 项目概述

将易经与风水知识结构化为 MCP 工具，提供可解释、可追溯的结果输出。

## 功能特性

- **易经六十四卦解卦分析**：基于 CTP《周易》的权威卦辞与象辞
- **罗盘坐向分析**：八宅 + 玄空飞星体系
- **节气影响分析**：基于天文算法的节气计算
- **数据可追溯**：所有数据标注权威来源

## 项目结构

```
CyberYJ/
├── data/                   # 数据文件
│   ├── trigrams.json      # 八卦数据
│   ├── hexagrams.json     # 六十四卦数据
│   ├── solar_terms.json   # 二十四节气
│   ├── luopan.json        # 二十四山向
│   ├── ba_zhai.json       # 八宅规则
│   ├── flying_stars.json  # 玄空飞星年盘
│   └── sources.json       # 数据来源索引
├── src/cyberYJ/           # 源代码
│   ├── core/              # 核心计算模块
│   ├── tools/             # MCP 工具实现
│   └── utils/             # 辅助工具
│       └── data_loader.py # 数据加载器
├── tests/                 # 测试文件
├── docs/                  # 文档
│   ├── requirements.md    # 需求文档
│   └── project-progress.md # 项目进度
└── schemas/               # Schema 定义
    └── mcp-tools.json     # MCP 工具 schema
```

## 安装

```bash
# 克隆项目
git clone <repository-url>
cd CyberYJ

# 安装依赖
pip install -e .

# 安装开发依赖
pip install -e ".[dev]"

# 安装天文计算依赖
pip install -e ".[astronomy]"
```

## 使用示例

### 示例 1: 数据查询

```python
from cyberYJ.utils.data_loader import get_data_loader

# 获取数据加载器
loader = get_data_loader()

# 查询卦象
hexagram = loader.get_hexagram_by_trigrams('乾', '乾')
print(f"卦名: {hexagram['name']}")
print(f"卦辞: {hexagram['judgment_summary']}")
print(f"象辞: {hexagram['image_summary']}")

# 查询节气
solar_term = loader.get_solar_term_by_longitude(315)
print(f"节气: {solar_term['name']}")  # 立春

# 查询罗盘山向
mountain = loader.get_luopan_by_degree(0)
print(f"山向: {mountain['name']}")  # 壬
```

### 示例 2: 节气计算

```python
from cyberYJ.core.solar_calculator import SolarCalculator
from datetime import datetime

calculator = SolarCalculator()

# 计算太阳黄经
longitude = calculator.get_solar_longitude(datetime(2024, 3, 20))
print(f"太阳黄经: {longitude}°")  # 约 0° (春分)

# 查询当前节气
term_info = calculator.get_current_solar_term(datetime(2024, 2, 4))
print(f"当前节气: {term_info['name']}")  # 立春
print(f"距离下一节气: {term_info['days_to_next']} 天")

# 计算节气时间
term_time = calculator.calculate_solar_term_time(2024, '春分')
print(f"2024年春分时间: {term_time}")
```

### 示例 3: 卦象分析

```python
from cyberYJ.core.hexagram_analyzer import HexagramAnalyzer

analyzer = HexagramAnalyzer()

# 解析输入（支持多种格式）
upper = analyzer.parse_trigram_input("西北")  # 乾
lower = analyzer.parse_trigram_input("西南")  # 坤

# 获取卦象
hexagram = analyzer.get_hexagram(upper, lower)
print(f"卦名: {hexagram['name']}")  # 否

# 分析五行关系
element = analyzer.analyze_element_relation(hexagram)
print(f"五行关系: {element['description']}")

# 生成解释（针对不同问题类型）
interpretation = analyzer.generate_interpretation(hexagram, "事业")
print(f"卦辞: {interpretation['judgment']}")
print(f"建议: {interpretation['advice']}")

# 分析变卦
changing = analyzer.analyze_changing_line(hexagram, 1)
print(f"变卦: {changing['changed_hexagram']['name']}")
```

### 示例 4: 罗盘计算

```python
from cyberYJ.core.luopan_calculator import LuopanCalculator
from datetime import datetime

calculator = LuopanCalculator()

# 解析坐向（支持多种格式）
direction = calculator.parse_sitting_direction("坐北朝南")
print(f"坐向角度: {direction['sitting_degree']}°")
print(f"山向: {direction['mountain']}")

# 计算宅卦
house_gua = calculator.calculate_house_gua(direction['sitting_degree'])
print(f"宅卦: {house_gua}")  # 坎宅

# 查询吉凶方位
positions = calculator.get_auspicious_positions(house_gua)
print(f"吉位: {positions['auspicious']}")
print(f"凶位: {positions['inauspicious']}")

# 计算命卦
ming_gua = calculator.calculate_ming_gua(datetime(1990, 5, 15), 'male')
print(f"命卦: {ming_gua['gua']}")
print(f"东四/西四: {ming_gua['group']}")

# 检查宅命匹配
compatibility = calculator.check_house_compatibility(house_gua, ming_gua)
print(f"匹配度: {compatibility['compatible']}")
```

### 示例 5: Wechat 小程序 HTTP API

```bash
# 安装 HTTP API 可选依赖
pip install -e ".[api]"

# 双击脚本启动（推荐）
/Users/apple/Desktop/start-cyberYJ-http-api.command

# 启动 HTTP 适配服务
python run_http_api.py
```

```bash
curl -X POST "http://127.0.0.1:8080/v1/divination/interpret" \
  -H "Content-Type: application/json" \
  -d '{"coins":[6,7,8,9,7,7],"question":"事业发展"}'
```

接口文档见 `docs/api/wechat-divination-http-api.md`。

更多示例请查看 `examples/` 目录。

## 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_data_loader.py

# 运行测试并显示覆盖率
pytest --cov=src/cyberYJ --cov-report=html
```

## 开发进度

详见 [项目进度文档](docs/project-progress.md) 和 [完成报告](docs/completion-report.md)

- ✅ 数据层（100%）- 7 个数据文件，143 条数据
- ✅ 逻辑层（100%）- 4 个核心模块，119 个测试通过
- ⏳ 服务层（0%）- MCP Server 待开发
- ✅ 测试层（100%）- 单元测试全部完成

**总进度**: 75%

### 已实现功能

#### 数据层
- ✅ 八卦数据（8 条）
- ✅ 六十四卦数据（64 条，含卦辞、象辞、五行关系）
- ✅ 二十四节气数据（24 条，含太阳黄经）
- ✅ 二十四山向数据（24 条，含角度映射）
- ✅ 八宅规则数据（8 条，含吉凶方位）
- ✅ 玄空飞星年盘（2024-2030 年）
- ✅ 数据来源索引（8 个权威来源）

#### 逻辑层
- ✅ **数据加载器** (`data_loader.py`)
  - 统一的数据访问接口
  - 内存缓存机制
  - 丰富的查询方法
  - 23 个测试通过

- ✅ **节气计算器** (`solar_calculator.py`)
  - 太阳黄经计算（精度 0.01°）
  - 24 节气查询
  - 节气时间计算
  - 节气影响分析
  - 31 个测试通过

- ✅ **卦象分析器** (`hexagram_analyzer.py`)
  - 灵活的输入解析（名称/方位/数字）
  - 64 卦查询
  - 五行生克关系分析
  - 变卦分析（6 爻）
  - 针对性解释生成（事业/财运/感情/健康）
  - 43 个测试通过

- ✅ **罗盘计算器** (`luopan_calculator.py`)
  - 多格式坐向解析（中文/角度/干支）
  - 24 山向查询
  - 八宅卦计算
  - 吉凶方位查询
  - 命卦计算与宅命匹配
  - 22 个测试通过

### 待实现功能

#### 服务层（M3 里程碑）
- ⏳ MCP Server 骨架
- ⏳ `fengshui_divination` 工具（易经解卦）
- ⏳ `luopan_orientation` 工具（罗盘坐向分析）
- ⏳ MCP 工具集成测试

## 数据来源

所有数据均标注权威来源，包括：

- **CTP《周易》**：六十四卦卦辞、象辞
- **中国气象局**：二十四节气黄经数据
- **青囊奥语**：二十四山向概念
- **八宅明镜**：八宅规则
- **地理辨正疏**：玄空飞星规则

详见 `data/sources.json`

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
