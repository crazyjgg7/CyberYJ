# M4 执行清单（权威数据本地落地）

更新时间：2026-02-11

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
- P2（版本与合规材料完备）：进行中（已落地来源合规策略与自动校验）
- P3（规则逐条校核与规模化替换）：未完成

P2 阶段报告：`docs/m4-p2-source-compliance-report.md`
