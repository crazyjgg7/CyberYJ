# M4 阶段验收报告（P1-P3）

更新时间：2026-02-12

## 验收范围

- P1：核心字段权威映射覆盖率
- P2：来源合规与 `source_ref` 一致性
- P3：规则核对闭环（结构预核对 + 证据门禁 + 状态同步）

## 阶段结果

### P1 覆盖率

- 覆盖率阈值：`80%`
- 统计对象：`authoritative_coverage_targets.json` 10 个核心字段
- 结果：`10/10`，覆盖率 `100%`
- 结论：`PASS`

### P2 合规与一致性

- 必选来源合规：`5/5` PASS
- 全量来源合规：`13/13` PASS
- `source_ref` 一致性：`26` 个 JSON，`884` 处引用，未知来源 `0`
- 高频字段证据映射：`10/10` PASS
- 结论：`PASS`

### P3 规则核对闭环（首轮）

- 规则总数：`35`（24 山向 + 8 八宅 + 3 飞星）
- 结构预核对：PASS（24/8/3 结构一致）
- 证据门禁：PASS（35/35 有证据记录）
- 状态同步：PASS（`confirmed_records=35`，`would_update_count=0`）
- 当前矩阵状态：`verified=35`，`blocked=0`，`pending=0`
- 结论：`PASS`（首轮）

## 验收命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_coverage.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_compliance.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_compliance_extended.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_ref_integrity.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_evidence.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_precheck.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_evidence.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py
python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py
```

## 当前结论

- M4 已完成 P1-P3 的阶段目标。
- M4 仍未完成，主要缺口是“权威文本/许可摘要规模化本地落地”与“页码/段落级证据二次复核”。
- P4（二次复核门禁）已启动：`confirmed=35`，`secondary_ready=0`。

## M4 剩余可执行项

1. 为 5 个权威来源补齐“可复核页码/段落”证据并回填 `rule_review_evidence.json`。
2. 扩展 `authoritative_text_map.json` 到全模块字段级覆盖（超出当前核心字段集）。
3. 形成最终 M4 完成报告：覆盖率、证据口径、风险收敛、未决事项。
