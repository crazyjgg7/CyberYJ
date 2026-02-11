# 数据目录说明（V2）

本目录采用分层设计，将数据按用途分类存储。所有数据项必须包含 `source_ref`，并在 `sources.json` 中可追溯。

## 📁 目录结构

```
data/
├── core/                      # 核心数据（通用）
│   ├── trigrams.json         # 八卦基础信息
│   ├── hexagrams.json        # 六十四卦信息
│   ├── solar_terms.json      # 二十四节气
│   ├── sources.json          # 权威来源索引
│   └── hexagram_keywords.json # 关键词解析库（待创建）
│
├── scenarios/                 # 场景框架（分场景）
│   ├── fortune.json          # 命运场景框架（待创建）
│   ├── career.json           # 事业场景框架（待创建）
│   ├── love.json             # 感情场景框架（待创建）
│   ├── wealth.json           # 财运场景框架
│   ├── health.json           # 健康场景框架
│   ├── study.json            # 学业场景框架
│   ├── family.json           # 家庭场景框架
│   ├── travel.json           # 出行场景框架
│   └── lawsuit.json          # 诉讼场景框架
│
├── templates/                 # 输出模板
│   ├── output_structures.json # 输出结构定义（待创建）
│   └── disclaimers.json      # 免责声明库（待创建）
│
├── prompts/                   # Prompt模板
│   └── base_prompt.txt       # 基础Prompt模板（待创建）
│
└── fengshui/                  # 风水专用数据
    ├── luopan.json           # 二十四山向与角度映射
    ├── ba_zhai.json          # 八宅规则
    └── flying_stars.json     # 流年飞星年盘规则
```

## 📋 数据分层说明

### 第一层：核心数据（core/）
存储权威原文和基础数据，这些数据是所有场景分析的基础。

- **trigrams.json**：八卦基础信息
- **hexagrams.json**：六十四卦信息（卦辞、象辞、五行关系）
- **solar_terms.json**：二十四节气
- **sources.json**：数据来源索引
- **hexagram_keywords.json**：关键词解析库（如"利西南"、"利见大人"等）

### 第二层：场景框架（scenarios/）
针对不同占卜场景的分析框架和输出结构定义。

每个场景文件包含：
- 场景信息（名称、描述、子场景）
- 分析框架（分析维度、关注点）
- 输出结构（sections、格式）
- 64卦在该场景下的核心数据

### 第三层：输出模板（templates/）
定义输出格式和免责声明。

- **output_structures.json**：各场景的输出结构模板
- **disclaimers.json**：特殊场景的免责声明（健康、财运、诉讼等）

### 第四层：Prompt模板（prompts/）
用于构建大模型分析Prompt的模板。

### 风水数据（fengshui/）
风水专用的数据文件（罗盘、八宅、飞星）。

## 🔧 字段约定

### core/trigrams.json
```json
{
  "id": "string",
  "name": "string",
  "symbol": "string",
  "element": "string",
  "direction": "string",
  "source_ref": "string"
}
```

### core/hexagrams.json
```json
{
  "id": "number",
  "name": "string",
  "upper_trigram": "string",
  "lower_trigram": "string",
  "judgment_summary": "string",
  "image_summary": "string",
  "element_relation": "string",
  "source_ref": "string | array"
}
```

### core/solar_terms.json
```json
{
  "id": "string",
  "name": "string",
  "solar_longitude_deg": "number",
  "source_ref": "string"
}
```

### core/sources.json
```json
{
  "source_id": "string",
  "title": "string",
  "edition": "string",
  "section": "string",
  "url_or_archive": "string",
  "license": "string",
  "notes": "string"
}
```

### fengshui/luopan.json
```json
{
  "id": "string",
  "name": "string",
  "start_deg": "number",
  "end_deg": "number",
  "direction_group": "string",
  "source_ref": "string"
}
```
角度约定：0°=正北，顺时针递增，范围 [0,360)

### fengshui/ba_zhai.json
```json
{
  "house_gua": "string",
  "auspicious_positions": "array",
  "inauspicious_positions": "array",
  "source_ref": "string"
}
```

### fengshui/flying_stars.json
```json
{
  "year": "number",
  "central_star": "number",
  "palace_map": "object",
  "source_ref": "string"
}
```

### fengshui/flying_stars_periods.json
```json
{
  "period": "number",
  "start_year": "number",
  "end_year": "number",
  "source_ref": "string"
}
```

### fengshui/flying_stars_house.json
```json
{
  "period": "number",
  "sitting_mountain": "string",
  "palace_map": "object",
  "source_ref": "string"
}
```

### fengshui/flying_stars_scoring.json
```json
{
  "version": "string",
  "stars": "object",
  "source_ref": "string"
}
```

## 📝 更新日志

### V2 (2026-02-10)
- 重构目录结构，采用分层设计
- 将数据按用途分类：core、scenarios、templates、prompts、fengshui
- 为多场景分析系统做准备

### V1 (2026-02-09)
- 初始版本，所有数据文件在同一目录
