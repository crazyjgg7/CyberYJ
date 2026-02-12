# M4-P2 本地权威知识库报告（基线）

更新时间：2026-02-12

## 目标

将 `authoritative_text_map` 中可合法落地的摘要条目批量归档到本地 `data/authoritative`，
形成可复核、可校验、可追踪的知识库基线。

## 新增能力

- 生成模块：`/Users/apple/dev/CyberYJ/src/cyberYJ/utils/authoritative_local_kb.py`
- 生成脚本：`/Users/apple/dev/CyberYJ/scripts/generate_authoritative_local_kb.py`
- 校验脚本：`/Users/apple/dev/CyberYJ/scripts/check_authoritative_local_kb.py`

## 产物

- 索引：`/Users/apple/dev/CyberYJ/data/authoritative/index.json`
- 条目：`/Users/apple/dev/CyberYJ/data/authoritative/entries.jsonl`

## 基线结果

- `total_entries=264`
- `convention_only=18`
- `unknown_source_refs=0`
- `source_count_mismatches=0`
- `count_mismatch=false`
- 结论：`PASS`

补充：
- 展开版字段知识库见 `docs/m4-p2-effective-local-kb-report.md`（`610/610`）。

## 验证命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/generate_authoritative_local_kb.py
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_local_kb.py
```

## 说明

- 当前为“首版本地归档基线”，条目来源于 `summary_only` 映射项。
- 后续将继续提升非高频字段 locator 精度与审计粒度。
