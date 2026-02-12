# M4-P3 规则逐条核对记录（启动版）

更新时间：2026-02-12

## 当前基线

- 规则矩阵文件：`/Users/apple/dev/CyberYJ/data/review/rule_review_matrix.json`
- 进度检查脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py`
- 当前统计：`35` 条待核对（24 山向 + 8 八宅 + 3 飞星）
- 已完成状态分流：`35`（历史）
- 已核对通过：`35`（verified）
- 当前状态：`blocked=0`，`pending=0`，`verified=35`

## 完成说明

- P3 已完成首轮规则核对闭环：结构预核对 + 证据门禁 + 自动状态同步。
- 当前 `verified=35` 代表“书目级索引 + 合法摘要 + 结构一致性”口径下可追踪通过。
- 后续仍需在 M4 中补齐“权威页码/段落级”证据并执行二次复核。

## 结构预核对结果（2026-02-12）

- 执行命令：`python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_precheck.py`
- 结果：`passed = true`
- 明细：
  - `luopan`：矩阵 `24`，数据 `24`，`missing=0`，`extra=0`
  - `bazhai`：矩阵 `8`，数据 `8`，`missing=0`，`extra=0`
  - `flying_star`：`period_count=9`，`house_expected_pairs=216`，`house_pair_count=216`，`scoring_star_count=9`

## 核对口径

1. `verified`：已根据权威版本核对并通过。
2. `blocked`：当前无法核对（缺版本/缺材料/口径冲突）。
3. `pending`：待核对。

## 差异记录模板

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | luopan_24_mountains | 壬 | ... | ... | 保留/替换/待定 | verified/blocked | source_id + section |

## P3-B1 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | luopan_24_mountains | 壬 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 子 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 癸 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 丑 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 艮 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 寅 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 甲 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 卯 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |

## P3-B2 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | luopan_24_mountains | 乙 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 辰 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 巽 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 巳 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 丙 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 午 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 丁 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 未 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |

## P3-B3 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | luopan_24_mountains | 坤 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 申 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 庚 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 酉 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 辛 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 戌 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 乾 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |
| 2026-02-12 | luopan_24_mountains | 亥 | `luopan.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `qingnang_aoyu`（书目级） |

## P3-B4 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | bazhai_rules | 乾宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 兑宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 离宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 震宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 巽宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 坎宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 艮宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |
| 2026-02-12 | bazhai_rules | 坤宅 | `ba_zhai.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_bazhai_mingjing`（书目级） |

## P3-B5 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | flying_star_rules | periods_table | `flying_stars_periods.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_dili_bianzheng_shu`（书目级） |
| 2026-02-12 | flying_star_rules | house_rules_24x9 | `flying_stars_house.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_dili_bianzheng_shu`（书目级） |
| 2026-02-12 | flying_star_rules | scoring_thresholds | `flying_stars_scoring.json` 现值 | 待补可复核页码/段落 | 保留现值，等待证据补全 | blocked | `cinii_dili_bianzheng_shu`（书目级） |

## P3-B8 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | flying_star_rules | periods_table | `flying_stars_periods.json` 现值 | 书目级索引 + 合法摘要 + 结构一致性核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_dili_bianzheng_shu` |
| 2026-02-12 | flying_star_rules | house_rules_24x9 | `flying_stars_house.json` 现值 | 书目级索引 + 合法摘要 + 结构一致性核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_dili_bianzheng_shu` |
| 2026-02-12 | flying_star_rules | scoring_thresholds | `flying_stars_scoring.json` 现值 | 书目级索引 + 合法摘要 + 结构一致性核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_dili_bianzheng_shu` |

## P3-B9 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | bazhai_rules | 乾宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 兑宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 离宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 震宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 巽宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 坎宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 艮宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |
| 2026-02-12 | bazhai_rules | 坤宅 | `ba_zhai.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `cinii_bazhai_mingjing` |

## P3-B10 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | luopan_24_mountains | 壬 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 子 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 癸 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 丑 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 艮 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 寅 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 甲 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 卯 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |

## P3-B11 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | luopan_24_mountains | 乙 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 辰 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 巽 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 巳 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 丙 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 午 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 丁 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 未 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |

## P3-B12 记录（2026-02-12）

| 日期 | 规则组 | 规则 ID | 当前值 | 权威口径 | 处理结论 | 状态 | 证据来源 |
|---|---|---|---|---|---|---|---|
| 2026-02-12 | luopan_24_mountains | 坤 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 申 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 庚 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 酉 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 辛 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 戌 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 乾 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |
| 2026-02-12 | luopan_24_mountains | 亥 | `luopan.json` 现值 | 书目级索引 + 合法摘要 + 规则映射核对 | 证据已 confirmed，自动同步为 verified（待权威页码二次复核） | verified | `qingnang_aoyu` |

## 操作流程

1. 在 `rule_review_matrix.json` 对应条目更新 `status/notes`。
2. 如有差异，追加到本文件“差异记录模板”表格。
3. 执行进度检查：

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py
```

4. 执行证据门禁检查：

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_evidence.py
```

## 证据门禁结果（2026-02-12）

- 证据台账：`/Users/apple/dev/CyberYJ/data/review/rule_review_evidence.json`
- 校验脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_evidence.py`
- 当前结果：
  - `total_rules=35`
  - `total_records=35`
  - `missing_records=0`
  - `extra_records=0`
  - `source_target_mismatches=0`
  - `invalid_verified_records=0`
  - `invalid_blocked_records=0`
  - `invalid_pending_records=0`
  - `passed=true`

## 状态同步结果（2026-02-12）

- 同步脚本：`/Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py`
- 同步口径：`evidence_status=confirmed` 且字段完整 -> 自动将 `blocked` 更新为 `verified`
- apply 结果（五批累计）：
  - `confirmed_records=35`
  - `would_update_count=8`（最近一批）
  - `updated_count=8`（最近一批）
  - `passed=true`
- 当前 dry-run 结果：
  - `confirmed_records=35`
  - `would_update_count=0`
  - `updated_count=0`
  - `passed=true`

## 二次复核门禁结果（2026-02-12）

- 校验脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_secondary_gate.py`
- 当前结果：
  - `total_confirmed_records=35`
  - `secondary_ready_records=19`
  - `ready_for_full_secondary_review=false`
- 说明：当前 verified 为首轮口径；已完成飞星 3 条 + 八宅 8 条 + 二十四山首批 8 条二次复核准备，剩余 16 条待补页码/段落级证据。
