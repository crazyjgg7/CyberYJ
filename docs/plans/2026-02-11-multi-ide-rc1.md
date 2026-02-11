# Multi-IDE RC1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 提供可复用的多 IDE MCP 配置模板与一键冒烟脚本，验证“风水/罗盘”两个入口在统一输出协议下可稳定调用。

**Architecture:** 新增一个可测试的冒烟运行模块（`src`），脚本层仅做 CLI 封装；文档层新增多客户端配置模板并同步到现有 MCP 指南。通过 `keyword_dispatch` 执行固定两条用例，并校验返回结构 `tool + data + meta`（含 `trace`、`sources`）。

**Tech Stack:** Python 3.9+, MCP Python SDK（可选）, pytest

---

### Task 1: 冒烟校验模块（测试先行）

**Files:**
- Create: `/Users/apple/dev/CyberYJ/tests/test_mcp_smoke_runner.py`
- Create: `/Users/apple/dev/CyberYJ/src/cyberYJ/tools/mcp_smoke.py`

**Steps:**
1. 写失败测试：默认用例是否固定两条（风水/罗盘）与预期工具名。
2. 写失败测试：协议校验函数在缺失 `tool/data/meta` 或 `trace/sources` 时返回错误。
3. 实现最小模块：默认用例定义 + `validate_response_payload`。
4. 运行测试，确保由红转绿。

### Task 2: CLI 冒烟脚本

**Files:**
- Create: `/Users/apple/dev/CyberYJ/scripts/mcp_smoke_test.py`

**Steps:**
1. 脚本调用 `mcp_smoke.run_smoke_cases()`，默认执行两条关键词用例。
2. 输出每条用例的 PASS/FAIL 与错误详情。
3. 全部通过返回 0，否则返回 1。

### Task 3: 多 IDE 配置文档与主文档同步

**Files:**
- Create: `/Users/apple/dev/CyberYJ/docs/mcp-client-configs.md`
- Modify: `/Users/apple/dev/CyberYJ/docs/mcp-server-guide.md`
- Modify: `/Users/apple/dev/CyberYJ/docs/project-progress.md`

**Steps:**
1. 补充 Claude Desktop / Cursor / Cline 的配置模板与注意事项。
2. 在 MCP 指南中增加“多 IDE 配置索引”和“冒烟脚本”章节。
3. 在进度文档中标记 RC1 交付状态。

### Task 4: 验证与提交准备

**Files:**
- Modify: (none, verification only)

**Steps:**
1. 跑定向测试：`pytest tests/test_mcp_smoke_runner.py -v`
2. 跑全量测试：`pytest -q`
3. 执行冒烟脚本：`PYTHONPATH=src python3 scripts/mcp_smoke_test.py`
4. 汇总结果并准备提交说明。
