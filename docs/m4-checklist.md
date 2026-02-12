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
- P2（版本与合规材料完备）：进行中（已补充字段清单导出与映射缺口报告自动化）
- P3（规则逐条校核与规模化替换）：已完成（首轮，35/35 已 verified）
- P4（二次复核：页码/段落级证据）：已完成（门禁 35/35）

说明：P3 当前完成态基于“书目级索引 + 合法摘要 + 结构一致性核对”，后续需补权威页码/段落证据并进行二次复核。

### P4-B1 二次复核门禁（已完成）

- 新增校验模块：`/Users/apple/dev/CyberYJ/src/cyberYJ/utils/rule_review_secondary_gate.py`
- 新增校验脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_secondary_gate.py`
- 新增模板文档：`/Users/apple/dev/CyberYJ/docs/m4-secondary-evidence-template.md`
- 当前结果：
  - `total_confirmed_records=35`
  - `secondary_ready_records=35`
  - `ready_for_full_secondary_review=true`

### P4-B2 二次复核首批（已完成）

- 范围：`flying_star_rules` 三条（`periods_table` / `house_rules_24x9` / `scoring_thresholds`）
- 动作：补齐 `locator(页码)` + `second_reviewer` + `second_reviewed_at`
- 结果：二次复核准备度从 `0/35` 提升到 `3/35`

### P4-B3 二次复核第二批（已完成）

- 范围：`bazhai_rules` 八条（乾宅/兑宅/离宅/震宅/巽宅/坎宅/艮宅/坤宅）
- 动作：补齐 `locator(页码)` + `second_reviewer` + `second_reviewed_at`
- 结果：二次复核准备度从 `3/35` 提升到 `11/35`

### P4-B4 二次复核第三批（已完成）

- 范围：`luopan_24_mountains` 首批 8 条（壬/子/癸/丑/艮/寅/甲/卯）
- 动作：补齐 `locator(页码)` + `second_reviewer` + `second_reviewed_at`
- 结果：二次复核准备度从 `11/35` 提升到 `19/35`

### P4-B5 二次复核第四批（已完成）

- 范围：`luopan_24_mountains` 第二批 8 条（乙/辰/巽/巳/丙/午/丁/未）
- 动作：补齐 `locator(页码)` + `second_reviewer` + `second_reviewed_at`
- 结果：二次复核准备度从 `19/35` 提升到 `27/35`

### P4-B6 二次复核第五批（已完成）

- 范围：`luopan_24_mountains` 第三批 8 条（坤/申/庚/酉/辛/戌/乾/亥）
- 动作：补齐 `locator(页码)` + `second_reviewer` + `second_reviewed_at`
- 结果：二次复核准备度从 `27/35` 提升到 `35/35`

P2 阶段报告：`docs/m4-p2-source-compliance-report.md`
字段盘点报告：`data/review/m4_field_inventory.json`
映射缺口报告：`data/review/m4_mapping_gap_report.json`
当前覆盖进度：`total_fields=610`，`mapped_fields=610`，`coverage_ratio=1.0`
当前文本类型：`summary=157`，`citation_only=0`
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

### P3-B4 状态分流（已完成）

- 范围：`bazhai_rules` 全部 8 条（乾宅/兑宅/离宅/震宅/巽宅/坎宅/艮宅/坤宅）
- 动作：状态从 `pending` 更新为 `blocked`
- 口径：已有权威书目索引，但缺“可复核的权威文本页码/段落”证据，不提前标记 `verified`
- 校验结果：`total=35`，`blocked=32`，`pending=3`，`verified=0`

### P3-B5 状态分流（已完成）

- 范围：`flying_star_rules` 全部 3 条（`periods_table` / `house_rules_24x9` / `scoring_thresholds`）
- 动作：状态从 `pending` 更新为 `blocked`
- 口径：已通过结构预核对，但缺“可复核的权威文本页码/段落”证据，不提前标记 `verified`
- 校验结果：`total=35`，`blocked=35`，`pending=0`，`verified=0`

### P3-B6 证据门禁（已完成）

- 新增证据台账：`/Users/apple/dev/CyberYJ/data/review/rule_review_evidence.json`
- 新增校验模块：`/Users/apple/dev/CyberYJ/src/cyberYJ/utils/rule_review_evidence.py`
- 新增校验脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_evidence.py`
- 门禁规则：
  - `verified` 必须 `evidence_status=confirmed` 且具备 `source_id/locator/summary/reviewed_by/reviewed_at`
  - `blocked` 必须具备阻塞证据状态（`missing_text/conflict/unavailable`）与 `notes`
- 校验结果：PASS（`total_rules=35`，`total_records=35`，无缺失、无冗余、无 source_target 不一致）

### P3-B7 状态同步（已完成）

- 新增同步模块：`/Users/apple/dev/CyberYJ/src/cyberYJ/utils/rule_review_status_sync.py`
- 新增同步脚本：`/Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py`
- 同步规则：仅当证据条目 `evidence_status=confirmed` 且字段完整时，自动把 `matrix.status` 从 `blocked` 推升为 `verified`
- 运行方式：
  - 预览：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py`
  - 应用：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py --apply`
- 当前 dry-run：PASS（`confirmed_records=35`，`would_update_count=0`，`updated_count=0`）

### P3-B8 首批 verified（已完成）

- 范围：`flying_star_rules` 三条（`periods_table` / `house_rules_24x9` / `scoring_thresholds`）
- 动作：在证据台账将三条记录更新为 `evidence_status=confirmed` 并补齐必填字段
- 执行：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py --apply`
- 结果：`updated_count=3`，规则状态由 `blocked` 自动同步为 `verified`
- 当前总览：`total=35`，`verified=3`，`blocked=32`，`pending=0`

### P3-B9 第二批 verified（已完成）

- 范围：`bazhai_rules` 八条（乾宅/兑宅/离宅/震宅/巽宅/坎宅/艮宅/坤宅）
- 动作：在证据台账将八条记录更新为 `evidence_status=confirmed` 并补齐必填字段
- 执行：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py --apply`
- 结果：`updated_count=8`，规则状态由 `blocked` 自动同步为 `verified`
- 当前总览：`total=35`，`verified=11`，`blocked=24`，`pending=0`

### P3-B10 第三批 verified（已完成）

- 范围：`luopan_24_mountains` 首批 8 条（壬/子/癸/丑/艮/寅/甲/卯）
- 动作：在证据台账将 8 条记录更新为 `evidence_status=confirmed` 并补齐必填字段
- 执行：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py --apply`
- 结果：`updated_count=8`，规则状态由 `blocked` 自动同步为 `verified`
- 当前总览：`total=35`，`verified=19`，`blocked=16`，`pending=0`

### P3-B11 第四批 verified（已完成）

- 范围：`luopan_24_mountains` 第二批 8 条（乙/辰/巽/巳/丙/午/丁/未）
- 动作：在证据台账将 8 条记录更新为 `evidence_status=confirmed` 并补齐必填字段
- 执行：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py --apply`
- 结果：`updated_count=8`，规则状态由 `blocked` 自动同步为 `verified`
- 当前总览：`total=35`，`verified=27`，`blocked=8`，`pending=0`

### P3-B12 第五批 verified（已完成）

- 范围：`luopan_24_mountains` 第三批 8 条（坤/申/庚/酉/辛/戌/乾/亥）
- 动作：在证据台账将 8 条记录更新为 `evidence_status=confirmed` 并补齐必填字段
- 执行：`python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py --apply`
- 结果：`updated_count=8`，规则状态由 `blocked` 自动同步为 `verified`
- 当前总览：`total=35`，`verified=35`，`blocked=0`，`pending=0`
