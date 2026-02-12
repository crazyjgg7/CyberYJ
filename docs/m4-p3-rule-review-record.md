# M4-P3 规则逐条核对记录（启动版）

更新时间：2026-02-12

## 当前基线

- 规则矩阵文件：`/Users/apple/dev/CyberYJ/data/review/rule_review_matrix.json`
- 进度检查脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py`
- 当前统计：`35` 条待核对（24 山向 + 8 八宅 + 3 飞星）
- 已核对：`0`
- 完成率：`0%`

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

## 操作流程

1. 在 `rule_review_matrix.json` 对应条目更新 `status/notes`。
2. 如有差异，追加到本文件“差异记录模板”表格。
3. 执行进度检查：

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py
```
