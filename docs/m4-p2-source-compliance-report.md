# M4-P2 来源合规报告（第二批）

更新时间：2026-02-11

## 范围

- 必选来源：`ctext_yijing` / `cma_24_terms` / `qingnang_aoyu` / `cinii_bazhai_mingjing` / `cinii_dili_bianzheng_shu`
- 校验维度：`title/edition/section/url_or_archive/license/notes`
- 校验规则：非空、非 `TBD`、URL 为 HTTP(S)
- `data` 全量 `source_ref` 一致性（source_id 存在、字段类型合法）

## 结果

- 必选来源存在性：`5/5`
- 缺失来源：`0`
- 非法字段：`0`
- `source_ref` 扫描文件：`24`
- `source_ref` 总计：`884`
- 未知来源：`0`
- 非法 source_ref 条目：`0`
- 结论：`PASS`

## 校验命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_source_compliance.py
python3 /Users/apple/dev/CyberYJ/scripts/check_source_ref_integrity.py
```

## 后续工作

1. 将 `source_ref` 高频命中字段与来源证据做一对一映射检查（字段级）。
2. 扩展到非必选来源并补全版本细节字段（edition/section 精细化）。
3. 建立“来源变更审计”记录模板（增量差异 + 责任人 + 时间戳）。
