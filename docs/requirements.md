# 玄学知识库 + MCP 服务 需求文档（v0.6）

更新时间：2026-02-11
默认时区：Asia/Shanghai（北京时间）

**1. 项目概述**
目标：将易经 + 风水（八宅、玄空飞星）结构化为 MCP 工具能力，提供可解释、可追溯的结果输出。

**2. 范围（V1）**
包含：
- 结构化数据：八卦、六十四卦、五行、节气、二十四山向、八宅规则、流年飞星年盘规则
- 两个 MCP 工具：`fengshui_divination` 与 `luopan_orientation`
- `fengshui_divination` 覆盖全部场景（命运/事业/感情/财运/健康/学业/家庭/出行/诉讼）
- 输出含推导路径摘要与来源标签（JSON 输出）

不包含：
- 紫微斗数、六壬、择日、个性化命盘
- 玄空飞星运盘/宅盘叠加（V1 仅流年年盘）

**3. 固定决策**
- 默认流派：八宅 + 玄空飞星
- 输出风格：JSON（tool + data）
- 节气：按天文算法计算（太阳黄经每 15°）

**4. 用户场景（业务话术）**
- 用户说：“风水：上坤下乾，问事业”，系统给出卦象解读 + 节气影响 + 事业场景建议
- 用户说：“风水：上乾下坤，感情如何”，系统给出卦象解读 + 场景化建议
- 用户说：“罗盘：坐北朝南 住宅”，系统给出宅卦、吉凶位与布局建议
- 开发者可直接通过 MCP 调用工具并得到标准化 JSON

**4.1 两个关键词入口示例**

**入口A：风水：**
- 文本输入示例：
  - `风水：上坤下乾，问事业`
  - `风水：上乾下坤，感情如何`
- MCP 调用示例（JSON）：
```json
{
  "tool": "fengshui_divination",
  "arguments": {
    "upper_trigram": "坤",
    "lower_trigram": "乾",
    "question_type": "事业",
    "question_text": "上坤下乾，问事业"
  }
}
```

**入口B：罗盘：**
- 文本输入示例：
  - `罗盘：坐北朝南 住宅`
  - `罗盘：坐亥向巳 办公室`
- MCP 调用示例（JSON）：
```json
{
  "tool": "luopan_orientation",
  "arguments": {
    "sitting_direction": "坐北朝南",
    "building_type": "住宅"
  }
}
```

**5. 功能需求**

**5.1 `fengshui_divination`**
输入字段：
- `upper_trigram`：上卦（卦名/数字/方位）
- `lower_trigram`：下卦（卦名/数字/方位）
- `question_type`：可选（命运/事业/感情/财运/健康/学业/家庭/出行/诉讼）
- `question_text`：可选（用户问题原文，用于智能场景识别）
- `changing_line`：可选（1-6）
- `timestamp`：可选（缺省为服务器时间）
- `timezone`：可选（缺省为 Asia/Shanghai）

输出字段：
- `main_hexagram`：卦象信息
- `five_elements`：五行分析
- `solar_term_influence`：节气影响
- `scenario`：场景识别结果
- `scenario_analysis` / `scenario_specific`：场景化建议
- `trace`：推导路径摘要
- `sources`：来源列表
- 其它字段（如 `do_dont`、`disclaimer`）按需要返回

**5.2 `luopan_orientation`**
输入字段：
- `sitting_direction`：坐向（坐北朝南 / 坐340向160 / 坐亥向巳）
- `building_type`：住宅/办公室/商铺/工厂
- `owner_birth`：可选（生辰，用于命卦匹配）
- `timestamp`：可选（用于流年飞星）
- `timezone`：可选（缺省为 Asia/Shanghai）

输出字段：
- `house_gua`：宅卦
- `auspicious_positions` / `inauspicious_positions`：吉凶方位
- `annual_flying_stars`：流年飞星年盘
- `layout_tips`：布局建议
- `trace`：推导路径摘要
- `sources`：来源列表

**6. 输出规范**
- 默认输出 JSON：`{ "tool": "...", "data": { ... } }`
- 结论层简明、解释层可追溯
- 结果必须稳定，同输入同输出

**7. 数据模型与出处标注**
- 所有规则与解释项必须含 `source_ref`
- 统一来源索引 `data/sources.json`
- 经典文本作为理论依据；无法唯一对应出处的规则标记为 `convention`

**权威来源替换（简化）**
- 当前阶段仅书目级索引 + 归纳规则
- 采用映射表（`authoritative_text_map.json`）逐步替换为合法摘要/许可文本

**权威来源清单（固定）**
- CTP《周易》：六十四卦卦辞、象辞
- 中国气象局：二十四节气黄经数据
- 《青囊奥语》：二十四山向概念
- 《八宅明镜》：八宅规则
- 《地理辨正疏》：玄空飞星规则

**8. 计算规则（V1）**
- 节气：按太阳视黄经每 15° 计算，输出节气名与时间
- 二十四山向：支持中文坐向、角度、干支坐向，统一映射 24 山向
- 八宅：宅卦与东四/西四判定规则
- 玄空飞星：仅输出流年年盘（不做运盘/宅盘叠加）

**9. 质量要求**
- 可解释：每条结论须能溯源
- 可控：输入异常必须返回清晰错误
- 可扩展：数据与规则分离，方便迭代
- 合规：当前阶段仅使用“书目级索引 + 归纳规则”，不录入受版权保护的原文

**10. 里程碑**
- M1：数据结构 + 规则表 + `sources.json`
- M2：MCP schema + 基础计算逻辑
- M3：输出模板与示例测试
- M4：权威文本合法获取与本地数据落地（后续评估）
  - 交付物：本地 `data` 目录的权威文本摘要/许可文本
  - 形式：`authoritative_text_map.json` + 分模块映射文件
  - 范围：卦辞/象辞/规则条目（按字段级映射）
  - 校验：source_ref 可追溯、license 合规、trace 可标注

**当前进度摘要（2026-02-11）**
- 所有场景数据已补齐（命运/事业/感情/财运/健康/学业/家庭/出行/诉讼）✅
- `fengshui_divination` / `luopan_orientation` 已完成并可运行 ✅
- MCP 输出统一 JSON ✅
- 权威书目索引已建立（非原文录入）✅

**场景覆盖**
- 命运 / 事业 / 感情 / 财运 / 健康 / 学业 / 家庭 / 出行 / 诉讼

**11. 风险与开放问题**
- 权威出处的具体版本需统一
- 权威文本合法获取的方式与成本待评估
- 节气天文算法需要选型（库或自研）
- 玄空飞星年盘规则表需确认
