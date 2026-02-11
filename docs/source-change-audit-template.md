# 来源变更审计模板（M4-P2）

更新时间：2026-02-11

## 使用说明

- 每次 `data/core/sources.json` 或 `data/mappings/authoritative_text_map.json` 发生变更时新增一条记录。
- 记录应与提交哈希绑定，确保可追溯。

## 审计记录表

| 日期 | 提交哈希 | 变更文件 | 变更类型 | 影响范围 | 变更人 | 审核人 | 备注 |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | `<commit>` | `data/core/sources.json` | 新增/修改/删除 | 来源索引/映射规则/运行输出 | name | name | 说明风险与回滚方式 |

## 最低审计字段

- 变更前后 `source_id` 差异
- 受影响 `field_path` 差异（若变更映射表）
- 是否影响 `trace/sources/authoritative_notes`
- 回滚策略（可回退到哪个提交）
