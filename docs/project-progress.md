# CyberYJ 项目进度（单一口径）

**项目名称**: 玄学知识库 + MCP 服务  
**更新时间**: 2026-02-12  
**版本**: v0.7

---

## 状态定义

- 已完成：M1 + M2 + M3 + V2（宅盘/流年叠加）+ RC1（多 IDE 冒烟）
- 未完成：M4（权威文本合法获取与本地 `data` 知识库规模化落地）

## 已完成（当前可用）

- 两个核心入口可用：
  - `风水：` -> `fengshui_divination`
  - `罗盘：` -> `luopan_orientation`
- `keyword_dispatch` 可用（文本自动路由）
- 输出协议统一：`tool + data + meta`
- 全场景数据已补齐（命运/事业/感情/财运/健康/学业/家庭/出行/诉讼）
- 玄空飞星 V2（宅盘 + 流年叠加 + 当前吉凶位）已上线
- 权威来源索引与映射机制已接入（书目级 + 字段级首批）
- 多 IDE 配置模板与冒烟脚本已完成
- 测试通过：`pytest` 全量通过

## 未完成（仅 M4）

- 权威文本/许可摘要尚未在 `data` 目录完成规模化落地
- 全模块字段级映射覆盖率目标（超出当前核心字段集）未完成
- 24 山向、八宅、飞星规则的权威版本逐条校核未完成

## M4 阶段进展（P3 已启动）

- 已新增规则核对矩阵：`data/review/rule_review_matrix.json`
- 已新增进度校验模块：`src/cyberYJ/utils/rule_review_progress.py`
- 已新增进度脚本：`scripts/check_rule_review_progress.py`
- 已新增结构预核对模块：`src/cyberYJ/utils/rule_review_precheck.py`
- 已新增结构预核对脚本：`scripts/check_rule_review_precheck.py`
- 已新增核对记录模板：`docs/m4-p3-rule-review-record.md`
- 当前基线：35 条规则
- 当前结构预核对：PASS（24 山向一致、8 宅卦一致、飞星 9 运 × 24 山向 = 216 条）
- P3-B1/B2/B3（24 山向）已完成状态分流：`blocked=24`，`pending=11`，`verified=0`

## M4 阶段进展（P1 已完成）

- 覆盖率目标已确定：80%
- 已新增覆盖率基线：`data/mappings/authoritative_coverage_targets.json`（10 个核心字段）
- 已新增校验脚本：`scripts/check_authoritative_coverage.py`
- 已新增校验模块：`src/cyberYJ/utils/authoritative_coverage.py`
- 当前覆盖率：10/10 = 100%（>= 80%）
- 说明：该结果仅代表“字段映射覆盖率达标”，不代表 M4 全部完成

## M4 阶段进展（P2 进行中）

- 已新增来源合规策略：`data/core/source_compliance_policy.json`
- 已新增来源合规扩展策略：`data/core/source_compliance_policy_extended.json`
- 已新增来源合规校验模块：`src/cyberYJ/utils/source_compliance.py`
- 已新增来源合规脚本：`scripts/check_source_compliance.py`
- 已新增来源合规扩展脚本：`scripts/check_source_compliance_extended.py`
- 当前核心来源合规检查：PASS（5/5 必选来源，缺失与非法字段为 0）
- 已新增 `source_ref` 一致性校验模块：`src/cyberYJ/utils/source_ref_integrity.py`
- 已新增 `source_ref` 一致性脚本：`scripts/check_source_ref_integrity.py`
- 当前 `source_ref` 一致性检查：PASS（26 个 JSON 文件，884 处 source_ref，未知来源 0）
- 已新增来源变更审计模板：`docs/source-change-audit-template.md`
- 已新增证据映射校验模块：`src/cyberYJ/utils/source_evidence_check.py`
- 已新增证据映射校验脚本：`scripts/check_source_evidence.py`
- 当前高频字段证据映射检查：PASS（10/10）

## M4 可执行清单

1. 固化权威版本：锁定来源版本并补全 `data/core/sources.json` 的版本字段。
2. 拉平字段清单：导出所有可映射输出字段（hexagram/scenario/fengshui/core）。
3. 设定覆盖率目标：定义核心字段最低覆盖率（建议 >= 80%）。
4. 批量补映射：扩展 `data/mappings/authoritative_text_map.json`。
5. 增加校验器：新增覆盖率 + source_ref + license 自动检查。
6. 校核关键规则：24 山向、八宅、飞星评分表按权威版本逐条核对。
7. 追踪可见化：确保命中映射时 `trace/sources/authoritative_notes` 一致输出。
8. 输出验收报告：形成 M4 完成报告（覆盖率、缺口、风险、待办）。

执行细则见：`/Users/apple/dev/CyberYJ/docs/m4-checklist.md`
阶段验收见：`/Users/apple/dev/CyberYJ/docs/m4-acceptance-report.md`

---

**备注**：`docs/final-report.md` 与 `docs/completion-report.md` 为历史阶段文档，不作为当前状态口径；当前以本文件与 `docs/requirements.md` 为准。
