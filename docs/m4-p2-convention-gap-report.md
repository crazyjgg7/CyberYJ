# M4-P2 Convention 缺口报告（基线）

更新时间：2026-02-12

## 目标

识别 `authoritative_text_map` 中仍仅依赖 `convention` 的条目，作为下一轮替换批次输入。

## 结果

- `total_summary_items=157`
- `convention_only_items=18`
- `mixed_convention_items=0`
- `unexpected_convention_only_items=0`（基于 allowlist）
- `convention_only_ratio=0.1146`
- 结论：`PASS`（无 mixed convention；阈值 `<=18`）

## 分布

- `scenarios`: 18
- `core/fengshui/other`: 0

## 条目类型

当前 18 条全部为场景输出模板字段：
- `data.scenarios.<scene>.output_structure`
- `data.scenarios.<scene>.prompt_template`

涉及场景：`fortune/career/love/wealth/health/study/family/travel/lawsuit`。

allowlist 文件：`/Users/apple/dev/CyberYJ/data/core/convention_allowlist.json`。

## 命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_convention_gap.py
python3 /Users/apple/dev/CyberYJ/scripts/generate_authoritative_convention_gap_report.py
```
