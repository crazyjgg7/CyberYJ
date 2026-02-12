# CyberYJ 项目进度（单一口径）

**项目名称**: 玄学知识库 + MCP 服务  
**更新时间**: 2026-02-13  
**版本**: v0.9

---

## 状态定义

- 已完成：M1 + M2 + M3 + M4 + V2（宅盘/流年叠加）+ RC1（多 IDE 冒烟）
- 进行中：无阻塞项（进入 M4 维护阶段）

## 已完成（当前可用）

- 两个核心入口可用：
  - `风水：` -> `fengshui_divination`
  - `罗盘：` -> `luopan_orientation`
- `keyword_dispatch` 可用（文本自动路由）
- 输出协议统一：`tool + data + meta`
- Wechat 小程序 HTTP 适配接口已落地：`POST /v1/divination/interpret`
- Wechat HTTP API 安全基线（D2）已完成：`X-API-Key` + 固定窗口限流
- Wechat HTTP API 可观测性（D3）已完成：`X-Request-ID`、结构化日志、错误计数追踪
- 全场景数据已补齐（命运/事业/感情/财运/健康/学业/家庭/出行/诉讼）
- 玄空飞星 V2（宅盘 + 流年叠加 + 当前吉凶位）已上线
- 权威来源索引与映射机制已接入（书目级 + 字段级首批）
- 本地权威知识库基线已落地（`data/authoritative/index.json` + `data/authoritative/entries.jsonl`）
- 本地权威知识库展开版已落地（`data/authoritative/effective_index.json` + `data/authoritative/effective_entries.jsonl`）
- 多 IDE 配置模板与冒烟脚本已完成
- 测试通过：`pytest` 全量通过

## M4 完成态

- 权威文本/许可摘要已完成本地落地（264 条规则条目 + 610 条字段展开条目）
- 字段级映射覆盖已达成（610/610），`citation_only=0`，`summary_only` locator `264/264`
- 来源合规、`source_ref` 一致性、locator 精度、convention 缺口门禁均已通过
- 24 山向、八宅、飞星规则已完成最终权威替换（35/35）

## M4 阶段进展（P4 已完成：二次复核门禁）

- 已新增二次复核校验模块：`src/cyberYJ/utils/rule_review_secondary_gate.py`
- 已新增二次复核校验脚本：`scripts/check_rule_review_secondary_gate.py`
- 已新增二次复核模板：`docs/m4-secondary-evidence-template.md`
- 当前二次复核准备度：`total_confirmed_records=35`，`secondary_ready_records=35`
- 结论：二次复核门禁已达标（`ready_for_full_secondary_review=true`）

## M4 阶段进展（P4-B7 已完成：最终权威版替换追踪）

- 已新增最终权威替换评估模块：`src/cyberYJ/utils/rule_review_final_authority.py`
- 已新增检查脚本：`scripts/check_rule_review_final_authority.py`
- 已新增替换清单导出脚本：`scripts/generate_rule_review_final_replacement_report.py`
- 已新增批次清单导出脚本：`scripts/generate_rule_review_final_replacement_batches.py`
- 已新增替换清单报告：`data/review/rule_review_final_replacement_report.json`
- 已新增批次清单报告：`data/review/rule_review_final_replacement_batches.json`
- 当前基线（2026-02-12）：
  - `total_confirmed_records=35`
  - `transitional_records_count=0`
  - `final_authority_ready_records=35`
  - `ready_for_final_authority_closeout=true`
- 批次进展：`A/B/C1/C2/C3(done)=0/0/0/0/0`
- 结论：已完成全部 35 条最终权威替换（飞星 3 条 + 八宅 8 条 + 山向 24 条）。
- 阶段报告：`docs/m4-p4-final-authority-replacement-report.md`

## M4 阶段进展（P3 已完成：首轮）

- 已新增规则核对矩阵：`data/review/rule_review_matrix.json`
- 已新增进度校验模块：`src/cyberYJ/utils/rule_review_progress.py`
- 已新增进度脚本：`scripts/check_rule_review_progress.py`
- 已新增结构预核对模块：`src/cyberYJ/utils/rule_review_precheck.py`
- 已新增结构预核对脚本：`scripts/check_rule_review_precheck.py`
- 已新增证据门禁模块：`src/cyberYJ/utils/rule_review_evidence.py`
- 已新增证据门禁脚本：`scripts/check_rule_review_evidence.py`
- 已新增证据台账：`data/review/rule_review_evidence.json`
- 已新增状态同步模块：`src/cyberYJ/utils/rule_review_status_sync.py`
- 已新增状态同步脚本：`scripts/sync_rule_review_matrix.py`
- 已新增核对记录模板：`docs/m4-p3-rule-review-record.md`
- 当前基线：35 条规则
- 当前结构预核对：PASS（24 山向一致、8 宅卦一致、飞星 9 运 × 24 山向 = 216 条）
- P3-B1/B2/B3/B4/B5（24 山向 + 8 八宅 + 3 飞星）已完成状态分流：`blocked=35`，`pending=0`，`verified=0`
- P3-B8（飞星 3 条）已通过证据同步转 `verified`：`blocked=32`，`pending=0`，`verified=3`
- P3-B9（八宅 8 条）已通过证据同步转 `verified`：`blocked=24`，`pending=0`，`verified=11`
- P3-B10（二十四山首批 8 条）已通过证据同步转 `verified`：`blocked=16`，`pending=0`，`verified=19`
- P3-B11（二十四山第二批 8 条）已通过证据同步转 `verified`：`blocked=8`，`pending=0`，`verified=27`
- P3-B12（二十四山第三批 8 条）已通过证据同步转 `verified`：`blocked=0`，`pending=0`，`verified=35`
- 当前证据门禁：PASS（35/35 规则已建立证据记录，source_target 对齐）
- 当前状态同步（dry-run）：PASS（`confirmed_records=35`，`would_update_count=0`，已与 matrix 对齐）
- 说明：P3 当前为“书目级索引 + 合法摘要”口径的首轮完成态；权威页码/段落级证据补全后需做二次复核

## M4 阶段进展（P1 已完成）

- 覆盖率目标已确定：80%
- 已新增覆盖率基线：`data/mappings/authoritative_coverage_targets.json`（21 个高频字段）
- 已新增校验脚本：`scripts/check_authoritative_coverage.py`
- 已新增校验模块：`src/cyberYJ/utils/authoritative_coverage.py`
- 当前覆盖率：21/21 = 100%（>= 80%）
- 说明：该结果仅代表“字段映射覆盖率达标”，不代表 M4 全部完成

## M4 阶段进展（P2 已完成）

- 已新增来源合规策略：`data/core/source_compliance_policy.json`
- 已新增来源合规扩展策略：`data/core/source_compliance_policy_extended.json`
- 已新增来源合规校验模块：`src/cyberYJ/utils/source_compliance.py`
- 已新增来源合规脚本：`scripts/check_source_compliance.py`
- 已新增来源合规扩展脚本：`scripts/check_source_compliance_extended.py`
- 当前核心来源合规检查：PASS（5/5 必选来源，缺失与非法字段为 0）
- 已新增 `source_ref` 一致性校验模块：`src/cyberYJ/utils/source_ref_integrity.py`
- 已新增 `source_ref` 一致性脚本：`scripts/check_source_ref_integrity.py`
- 当前 `source_ref` 一致性检查：PASS（45 个 JSON 文件，1138 处 source_ref，未知来源 0）
- 已新增来源变更审计模板：`docs/source-change-audit-template.md`
- 已新增证据映射校验模块：`src/cyberYJ/utils/source_evidence_check.py`
- 已新增证据映射校验脚本：`scripts/check_source_evidence.py`
- 当前高频字段证据映射检查：PASS（21/21）
- 已新增 locator 质量校验模块：`src/cyberYJ/utils/authoritative_locator_quality.py`
- 已新增 locator 质量校验脚本：`scripts/check_authoritative_locator_quality.py`
- 当前高频字段 locator 覆盖：PASS（21/21）
- 已新增 locator 精度校验模块：`src/cyberYJ/utils/authoritative_locator_precision.py`
- 已新增 locator 精度校验脚本：`scripts/check_authoritative_locator_precision.py`
- 当前高频字段 locator 精度：PASS（21/21）
- 已新增全量 locator 精度校验模块：`src/cyberYJ/utils/authoritative_locator_precision_full.py`
- 已新增全量 locator 精度校验脚本：`scripts/check_authoritative_locator_precision_full.py`
- 已新增全量 locator 精度报告：`data/review/m4_locator_precision_full_report.json`
- 当前全量 locator 精度：PASS（264/264）
- 书籍来源字段页码定位覆盖：21/21
- 已新增字段清单与缺口分析模块：`src/cyberYJ/utils/m4_mapping_gap.py`
- 已新增自动导出脚本：`scripts/generate_m4_mapping_gap_report.py`
- 已新增盘点产物：`data/review/m4_field_inventory.json`
- 已新增缺口报告：`data/review/m4_mapping_gap_report.json`
- 当前盘点口径：`total_fields=610`，`mapped_fields=610`，`unmapped_fields=0`，`coverage_ratio=1.0`
- 当前映射文本口径：`summary=264`，`citation_only=0`，`summary_with_locator=264`
- 当前映射来源口径：`convention_only=18`（已清理 mixed convention 条目）
- 已完成 locator 精细化替换批次 1：历史通用定位文案 `110 -> 0`
- 已完成 locator 精细化替换批次 2：场景通用定位文案 `108 -> 0`，按场景与字段类别细分（`hexagrams/analysis_framework/notes/meta`）
- 已完成 locator 精细化替换批次 3：场景 URL 索引型定位全部补充 `映射字段=field_path`（`108/108`）
- 已完成 locator 精细化替换批次 4：summary 级 URL 索引型定位全部补充 `映射字段=field_path`（`112/112`）
- 已完成 summary 扩展批次 1：`career` 场景 wildcard 派生显式字段 `+15`（总 summary `157 -> 172`）
- 已完成 summary 扩展批次 2：`love/fortune/wealth` 场景 wildcard 派生显式字段 `+37`（总 summary `172 -> 209`）
- 已完成 summary 扩展批次 3：`family/health/lawsuit/study/travel` 场景 wildcard 派生显式字段 `+55`（总 summary `209 -> 264`）
- 已新增定位精细化报告：`data/review/m4_locator_refinement_batch1_report.json`、`data/review/m4_locator_refinement_batch2_report.json`、`data/review/m4_locator_refinement_batch3_report.json`、`data/review/m4_locator_refinement_batch4_report.json`
- 已新增 summary 扩展报告：`data/review/m4_summary_expansion_batch1_report.json`、`data/review/m4_summary_expansion_batch2_report.json`、`data/review/m4_summary_expansion_batch3_report.json`
- 当前 URL 索引型 locator：`112/264`，且字段锚点补充完成 `112/112`（其余主要为书籍页码或内部 convention 模板定位）
- 已新增 summary 扩展候选清单：`data/review/m4_summary_expansion_backlog.json`（seed `54` 条，pending explicit `0`）
- 已新增本地知识库生成模块：`src/cyberYJ/utils/authoritative_local_kb.py`
- 已新增生成脚本：`scripts/generate_authoritative_local_kb.py`
- 已新增校验脚本：`scripts/check_authoritative_local_kb.py`
- 已新增本地知识库产物：`data/authoritative/index.json`、`data/authoritative/entries.jsonl`
- 当前本地知识库口径：`total_entries=264`，`unknown_source_refs=0`
- 已新增展开版知识库模块：`src/cyberYJ/utils/authoritative_local_kb_effective.py`
- 已新增展开版生成脚本：`scripts/generate_authoritative_local_kb_effective.py`
- 已新增展开版校验脚本：`scripts/check_authoritative_local_kb_effective.py`
- 已新增展开版产物：`data/authoritative/effective_index.json`、`data/authoritative/effective_entries.jsonl`
- 当前展开版口径：`total_fields=610`，`resolved=610`，`unresolved=0`，`allowed_convention_fields=214`，`unexpected_convention_fields=0`
- 已新增 convention 缺口校验模块：`src/cyberYJ/utils/authoritative_convention_gap.py`
- 已新增 convention 缺口脚本：`scripts/check_authoritative_convention_gap.py`
- 已新增 convention 缺口报告：`data/review/m4_convention_gap_report.json`
- 已新增 convention 白名单：`data/core/convention_allowlist.json`
- 当前 convention 缺口：`convention_only=18`，`mixed_convention=0`，`unexpected=0`（全部位于 scenario 输出模板字段）

## M4 维护清单

1. 继续把非高频字段 locator 从索引级逐步升级到页码/段落/章节级。
2. 按季度执行来源审计与白名单漂移检查（`source_ref` / convention allowlist）。
3. 对新增业务字段保持 `unmapped=0`，并同步本地知识库与校验报告。

执行细则见：`/Users/apple/dev/CyberYJ/docs/m4-checklist.md`
阶段验收见：`/Users/apple/dev/CyberYJ/docs/m4-acceptance-report.md`
最终收口见：`/Users/apple/dev/CyberYJ/docs/m4-final-closeout-report.md`

---

**备注**：`docs/final-report.md` 与 `docs/completion-report.md` 为历史阶段文档，不作为当前状态口径；当前以本文件与 `docs/requirements.md` 为准。
