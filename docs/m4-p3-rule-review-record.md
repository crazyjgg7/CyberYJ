# M4-P3 规则逐条核对记录（启动版）

更新时间：2026-02-12

## 当前基线

- 规则矩阵文件：`/Users/apple/dev/CyberYJ/data/review/rule_review_matrix.json`
- 进度检查脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py`
- 当前统计：`35` 条待核对（24 山向 + 8 八宅 + 3 飞星）
- 已完成状态分流：`24`（blocked）
- 已核对通过：`0`（verified）
- 当前状态：`blocked=24`，`pending=11`，`verified=0`

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

## 操作流程

1. 在 `rule_review_matrix.json` 对应条目更新 `status/notes`。
2. 如有差异，追加到本文件“差异记录模板”表格。
3. 执行进度检查：

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py
```
