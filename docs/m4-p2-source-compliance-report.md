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
- `source_ref` 扫描文件：`30`
- `source_ref` 总计：`1031`
- 未知来源：`0`
- 非法 source_ref 条目：`0`
- 高频字段证据映射：`21/21`
- 映射文本类型：`summary=157`，`citation_only=0`
- 高频字段 locator 覆盖：`21/21`
- summary locator 覆盖：`157/157`
- 高频字段 locator 精度：`21/21`
- 证据映射失败字段：`0`
- 结论：`PASS`

## 校验命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_source_compliance.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_compliance_extended.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_ref_integrity.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_evidence.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_locator_quality.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_locator_precision.py
```

## 后续工作

1. 将 `source_ref` 高频命中字段与来源证据做一对一映射检查（字段级）✅
2. 扩展到非必选来源并补全版本细节字段（edition/section 精细化）✅
3. 建立“来源变更审计”记录模板（增量差异 + 责任人 + 时间戳）✅  
   模板文件：`/Users/apple/dev/CyberYJ/docs/source-change-audit-template.md`
4. 新增字段盘点与映射缺口自动报告（`scripts/generate_m4_mapping_gap_report.py`）✅  
   产物文件：`/Users/apple/dev/CyberYJ/data/review/m4_field_inventory.json`、`/Users/apple/dev/CyberYJ/data/review/m4_mapping_gap_report.json`
