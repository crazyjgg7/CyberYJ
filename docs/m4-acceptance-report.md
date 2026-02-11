# M4 验收报告（P1：覆盖率）

更新时间：2026-02-11

## 验收范围

- 仅验收 M4 第一阶段（P1）：核心字段“权威映射覆盖率”
- 不包含：权威版本逐条校核、文本合法获取规模化落地

## 验收标准

- 覆盖率阈值：`80%`
- 统计对象：`data/mappings/authoritative_coverage_targets.json` 定义的 10 个核心字段
- 统计来源：`data/mappings/authoritative_text_map.json`

## 验收结果

- 总目标字段：10
- 已覆盖字段：10
- 覆盖率：`100%`
- 阈值：`80%`
- 结论：`PASS`

## 验收命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_authoritative_coverage.py
```

## 当前结论

- M4-P1（覆盖率）已达标。
- M4 总体仍未完成，后续进入：
  1. 权威版本与 license 证据补齐
  2. 24 山向/八宅/飞星规则逐条校核
  3. 权威文本/许可摘要规模化本地落地
