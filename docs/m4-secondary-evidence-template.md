# M4 二次复核证据模板（页码/段落级）

更新时间：2026-02-12

## 目标

为 `rule_review_evidence.json` 的 `confirmed` 条目补齐“可复核页码/段落级”证据，并完成二次复核签署。

## 必填字段（confirmed 条目）

- `locator`：必须可定位到页码/段落（示例：`第12页` / `p. 12` / `§ 3` / `第2段`）
- `second_reviewer`：二次复核人
- `second_reviewed_at`：二次复核日期（`YYYY-MM-DD`）

## 建议补充字段

- `edition`：具体版本信息（出版社/年份/ISBN 或权威站点版本）
- `section`：章节或条目标识
- `summary`：合法摘要（不复制受版权保护原文）
- `notes`：差异说明与处理结论

## 单条示例

```json
{
  "group": "luopan_24_mountains",
  "id": "壬",
  "source_target": "qingnang_aoyu",
  "evidence_status": "confirmed",
  "source_id": "qingnang_aoyu",
  "edition": "四库全书本",
  "section": "卷1",
  "locator": "第12页",
  "summary": "二十四山方位条目与现有规则一致。",
  "reviewed_by": "codex",
  "reviewed_at": "2026-02-12",
  "second_reviewer": "apple",
  "second_reviewed_at": "2026-02-13",
  "notes": "已完成页码级二次复核。"
}
```

## 校验命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_secondary_gate.py
```
