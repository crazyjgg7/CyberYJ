# M4 执行清单（权威数据本地落地）

更新时间：2026-02-12

## 目标

完成“权威文本合法获取与本地 `data` 知识库落地”，并让运行时输出可追踪、可审计。

## 执行步骤

1. 确认来源版本  
产出：更新后的 `data/core/sources.json`（`edition/section/license` 完整）。

2. 导出字段映射清单  
产出：字段盘点表（hexagram/scenario/ba_zhai/flying_star/solar_term）。

3. 定义覆盖率标准  
产出：覆盖率目标文档（核心输出字段目标值与统计口径）。

4. 扩充映射表  
产出：`data/mappings/authoritative_text_map.json` 批量新增条目。

5. 增加自动校验  
产出：映射覆盖率与合规校验脚本 + 测试用例。

6. 运行时一致性校验  
产出：验证 `trace` / `sources` / `authoritative_notes` 三者一致的测试。

7. 规则逐条校核  
产出：24 山向、八宅、飞星规则核对记录（含差异与处理结论）。

8. M4 验收报告  
产出：`docs/m4-acceptance-report.md`（覆盖率、未覆盖字段、风险、后续计划）。

## 完成判定

- 映射覆盖率达到预设阈值（核心字段）。
- 关键输出字段均能追溯 `source_ref`。
- 合规字段（license/source）无校验错误。

## 当前阶段状态

- P1（覆盖率基线与校验）：已完成（见 `docs/m4-acceptance-report.md`）
- P2（版本与合规材料完备）：进行中（已落地来源合规、全量来源扩展校验、source_ref 一致性、证据映射校验）
- P3（规则逐条校核与规模化替换）：已启动（已落地规则核对矩阵、进度脚本、结构预核对脚本）

P2 阶段报告：`docs/m4-p2-source-compliance-report.md`
P3 核对记录：`docs/m4-p3-rule-review-record.md`

### P3 结构预核对（已完成）

- 命令：`python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_precheck.py`
- 结果：PASS
  - luopan：矩阵 24 / 数据 24（无缺失、无冗余）
  - bazhai：矩阵 8 / 数据 8（无缺失、无冗余）
  - flying_star：`period_count=9`，`house_pair_count=216`，`scoring_star_count=9`

### P3-B1 状态分流（已完成）

- 范围：`luopan_24_mountains` 前 8 条（壬/子/癸/丑/艮/寅/甲/卯）
- 动作：状态从 `pending` 更新为 `blocked`
- 口径：已通过结构预核对，但缺“可复核的权威文本页码/段落”证据，不提前标记 `verified`
- 校验结果：`total=35`，`blocked=8`，`pending=27`，`verified=0`

### P3-B2 状态分流（已完成）

- 范围：`luopan_24_mountains` 第 9-16 条（乙/辰/巽/巳/丙/午/丁/未）
- 动作：状态从 `pending` 更新为 `blocked`
- 口径：已通过结构预核对，但缺“可复核的权威文本页码/段落”证据，不提前标记 `verified`
- 校验结果：`total=35`，`blocked=16`，`pending=19`，`verified=0`

### P3-B3 状态分流（已完成）

- 范围：`luopan_24_mountains` 第 17-24 条（坤/申/庚/酉/辛/戌/乾/亥）
- 动作：状态从 `pending` 更新为 `blocked`
- 口径：已通过结构预核对，但缺“可复核的权威文本页码/段落”证据，不提前标记 `verified`
- 校验结果：`total=35`，`blocked=24`，`pending=11`，`verified=0`
