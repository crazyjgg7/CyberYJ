# M4-P4 最终权威版替换报告（基线）

更新时间：2026-02-12

## 目标

识别并清理 `rule_review_evidence.json` 中“过渡证据”记录，形成替换清单并完成最终权威版收口。

## 新增能力

- 评估模块：`/Users/apple/dev/CyberYJ/src/cyberYJ/utils/rule_review_final_authority.py`
- 检查脚本：`/Users/apple/dev/CyberYJ/scripts/check_rule_review_final_authority.py`
- 清单导出：`/Users/apple/dev/CyberYJ/scripts/generate_rule_review_final_replacement_report.py`
- 批次清单导出：`/Users/apple/dev/CyberYJ/scripts/generate_rule_review_final_replacement_batches.py`
- 清单产物：`/Users/apple/dev/CyberYJ/data/review/rule_review_final_replacement_report.json`
- 批次产物：`/Users/apple/dev/CyberYJ/data/review/rule_review_final_replacement_batches.json`

## 基线结果（2026-02-12）

- `total_confirmed_records=35`
- `transitional_records_count=0`
- `final_authority_ready_records=35`
- `ready_for_final_authority_closeout=true`
- 批次状态：`A/B/C1/C2/C3(done)=0/0/0/0/0`

分组完成：
- `luopan_24_mountains`: 24/24
- `bazhai_rules`: 8/8
- `flying_star_rules`: 3/3

## 执行命令

```bash
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_final_authority.py
python3 /Users/apple/dev/CyberYJ/scripts/generate_rule_review_final_replacement_report.py
python3 /Users/apple/dev/CyberYJ/scripts/generate_rule_review_final_replacement_batches.py
python3 /Users/apple/dev/CyberYJ/scripts/check_rule_review_final_authority.py --strict
```

说明：
- 默认模式仅校验数据结构与替换清单生成能力。
- `--strict` 要求全部条目完成最终权威替换，否则返回非零退出码。

## 下一步批次建议

1. P4-B7 已完成，后续进入抽检与审计留痕阶段。
