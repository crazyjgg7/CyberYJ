# M4 最终收口报告（Closeout）

更新时间：2026-02-12

## 1. 收口结论

- M4 核心门禁已全部通过：覆盖率、来源合规、source_ref 一致性、locator 精度、convention 缺口、规则核对与最终权威替换。
- 本轮已完成场景解释层的分批扩展：summary 条目从 `157` 提升到 `264`。
- M4 已完成并进入维护状态；剩余工作为持续维护型任务，而非阻塞门禁任务。

## 2. 核心指标（当前）

- 字段覆盖：`610/610`
- summary 条目：`264`
- citation_only：`0`
- 全量 locator 精度：`264/264`
- source_ref 一致性：`scanned_files=45`，`source_ref_count=1138`，`unknown=0`
- convention 缺口：`convention_only=18`，`mixed=0`，`unexpected=0`
- 本地知识库：`entries=264`，`unknown_source_refs=0`
- 展开版知识库：`resolved_fields=610`，`unresolved=0`
- 规则核对最终替换：`35/35`（`transitional=0`）

## 3. 本轮批次结果

- locator 精细化：batch1-4 完成
  - 历史通用定位 `110 -> 0`
  - 场景通用定位 `108 -> 0`
  - URL 索引型字段锚点 `112/112`
- summary 扩展：batch1-3 完成
  - batch1：career `+15`
  - batch2：love/fortune/wealth `+37`
  - batch3：family/health/lawsuit/study/travel `+55`

## 4. 剩余事项（非阻塞）

1. 对书籍来源的非高频字段，按维护节奏继续从“索引级定位”提升到“页码/段落级定位”。
2. 固化季度审计：source_ref 变更、locator 质量、convention 白名单漂移。
3. 持续补充新增业务字段的合法摘要映射，保持 `unmapped=0`。

## 5. 维护规则（建议）

- 每次新增/修改映射后，必须执行：
  - `python3 /Users/apple/dev/CyberYJ/scripts/check_source_ref_integrity.py`
  - `python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_locator_precision_full.py`
  - `python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_local_kb.py --refresh`
  - `python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_local_kb_effective.py --refresh`
  - `pytest -q`
- 若出现 `mixed_convention > 0` 或 `unexpected_convention > 0`，禁止合入。
- 若 `unknown_source_refs > 0` 或 `unresolved_fields > 0`，禁止发布。
