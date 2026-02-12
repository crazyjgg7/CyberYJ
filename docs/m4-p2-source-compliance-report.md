# M4-P2 来源合规报告（第二批）

更新时间：2026-02-12

## 范围

- 必选来源：`ctext_yijing` / `cma_24_terms` / `qingnang_aoyu` / `cinii_bazhai_mingjing` / `cinii_dili_bianzheng_shu`
- 校验维度：`title/edition/section/url_or_archive/license/notes`
- 校验规则：非空、非 `TBD`、URL 为 HTTP(S)
- `data` 全量 `source_ref` 一致性（source_id 存在、字段类型合法）
- 高频输出字段与来源证据一对一映射（21 个高频字段）

## 结果

- 必选来源存在性：`5/5`
- 缺失来源：`0`
- 非法字段：`0`
- 全量来源合规（扩展策略）：`13/13`（缺失 0，非法字段 0）
- `source_ref` 扫描文件：`45`
- `source_ref` 总计：`1138`
- 未知来源：`0`
- 非法 source_ref 条目：`0`
- 高频字段证据映射：`21/21`
- 映射文本类型：`summary=264`，`citation_only=0`
- 映射来源口径：已清理混合引用，当前 `convention_only=18`
- convention 缺口检查：`convention_only=18`，`mixed_convention=0`，`unexpected=0`
- 高频字段 locator 覆盖：`21/21`
- summary locator 覆盖：`264/264`
- 高频字段 locator 精度：`21/21`
- 全量 locator 精度：`264/264`
- locator 精细化批次 1：历史通用定位文案 `110 -> 0`
- locator 精细化批次 2：场景通用定位文案 `108 -> 0`（按场景与字段类别细分）
- locator 精细化批次 3：场景 URL 索引型定位补充字段锚点 `108/108`
- locator 精细化批次 4：summary 级 URL 索引型定位补充字段锚点 `112/112`
- summary 中 URL 索引型 locator：`112/264`（字段锚点完成 `112/112`）
- 书籍来源字段页码定位覆盖：`21/21`
- 证据映射失败字段：`0`
- 本地权威知识库：`entries=264`，`unknown_source_refs=0`
- 展开版知识库：`fields=610`，`resolved=610`，`unresolved=0`
- 结论：`PASS`

## 校验命令

```bash
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
```

精细化报告：`/Users/apple/dev/CyberYJ/data/review/m4_locator_refinement_batch1_report.json`、`/Users/apple/dev/CyberYJ/data/review/m4_locator_refinement_batch2_report.json`、`/Users/apple/dev/CyberYJ/data/review/m4_locator_refinement_batch3_report.json`、`/Users/apple/dev/CyberYJ/data/review/m4_locator_refinement_batch4_report.json`
summary 扩展报告：`/Users/apple/dev/CyberYJ/data/review/m4_summary_expansion_batch1_report.json`、`/Users/apple/dev/CyberYJ/data/review/m4_summary_expansion_batch2_report.json`、`/Users/apple/dev/CyberYJ/data/review/m4_summary_expansion_batch3_report.json`

## 后续工作

1. 将 `source_ref` 高频命中字段与来源证据做一对一映射检查（字段级）✅
2. 扩展到非必选来源并补全版本细节字段（edition/section 精细化）✅
3. 建立“来源变更审计”记录模板（增量差异 + 责任人 + 时间戳）✅  
   模板文件：`/Users/apple/dev/CyberYJ/docs/source-change-audit-template.md`
4. 新增字段盘点与映射缺口自动报告（`scripts/generate_m4_mapping_gap_report.py`）✅  
   产物文件：`/Users/apple/dev/CyberYJ/data/review/m4_field_inventory.json`、`/Users/apple/dev/CyberYJ/data/review/m4_mapping_gap_report.json`
5. 新增本地权威知识库生成与校验（`generate_authoritative_local_kb.py` / `check_authoritative_local_kb.py`）✅  
   产物文件：`/Users/apple/dev/CyberYJ/data/authoritative/index.json`、`/Users/apple/dev/CyberYJ/data/authoritative/entries.jsonl`
6. 新增展开版知识库生成与校验（`generate_authoritative_local_kb_effective.py` / `check_authoritative_local_kb_effective.py`）✅  
   产物文件：`/Users/apple/dev/CyberYJ/data/authoritative/effective_index.json`、`/Users/apple/dev/CyberYJ/data/authoritative/effective_entries.jsonl`
