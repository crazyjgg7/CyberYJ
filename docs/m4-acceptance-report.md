# M4 阶段验收报告（P1-P4）

更新时间：2026-02-12

## 验收范围

- P1：高频字段权威映射覆盖率
- P2：来源合规与 `source_ref` 一致性
- P3：规则核对闭环（结构预核对 + 证据门禁 + 状态同步）

## 阶段结果

### P1 覆盖率

- 覆盖率阈值：`80%`
- 统计对象：`authoritative_coverage_targets.json` 21 个高频字段
- 结果：`21/21`，覆盖率 `100%`
- 结论：`PASS`

### P2 合规与一致性

- 必选来源合规：`5/5` PASS
- 全量来源合规：`13/13` PASS
- `source_ref` 一致性：`45` 个 JSON，`1138` 处引用，未知来源 `0`
- 高频字段证据映射：`21/21` PASS
- 映射文本类型：`summary=264`，`citation_only=0`
- 映射来源口径：已清理“authoritative + convention”混合引用；当前 `convention_only=18`
- convention 缺口检查：`convention_only=18`，`mixed_convention=0`，`unexpected=0` PASS
- 高频字段 locator 覆盖：`21/21` PASS（当前 summary locator 覆盖 `264/264`）
- 高频字段 locator 精度：`21/21` PASS
- 全量 locator 精度：`264/264` PASS
- 书籍来源字段页码定位覆盖：`21/21` PASS
- locator 精细化批次 1：历史通用定位文案 `110 -> 0`
- locator 精细化批次 2：场景通用定位文案 `108 -> 0`（按场景与字段类别细分）
- locator 精细化批次 3：场景 URL 索引定位补充字段锚点 `108/108`
- locator 精细化批次 4：summary URL 索引定位补充字段锚点 `112/112`
- summary 扩展批次 1：`career` 场景 wildcard 派生显式字段 `+15`
- summary 扩展批次 2：`love/fortune/wealth` 场景 wildcard 派生显式字段 `+37`
- summary 扩展批次 3：`family/health/lawsuit/study/travel` 场景 wildcard 派生显式字段 `+55`
- 本地权威知识库（`data/authoritative`）：`entries=264`，`unknown_source_refs=0`
- 展开版知识库（`data/authoritative/effective_*`）：`fields=610`，`resolved=610`，`unresolved=0`
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
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_locator_quality.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_locator_precision.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_locator_precision_full.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_convention_gap.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_local_kb.py --refresh
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_local_kb_effective.py --refresh
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_precheck.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_evidence.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_progress.py
python3 /Users/apple/dev/CyberYJ/scripts/sync_rule_review_matrix.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_final_authority.py --strict
```

## 当前结论

- M4 已完成 P1-P3 的阶段目标。
- M4 阶段目标已完成：核心门禁全部通过，规则层已收口，知识库已完成规模化落地。
- P4（二次复核门禁）已完成：`confirmed=35`，`secondary_ready=35`。
- 当前阶段完成度评估：`100%`（进入维护阶段）。

## M4 维护项

1. 非高频来源定位继续从索引级升级到页码/段落/章节级。
2. 对新增条目持续执行来源审计、白名单审计与门禁校验。
3. 维持 `unmapped=0`、`unknown_source_refs=0`、`mixed_convention=0` 的稳定状态。
