# Wechat Mini Program Divination API Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在不影响现有 MCP Server 的前提下，新增一个可被微信小程序直接调用的 HTTP API：`POST /v1/divination/interpret`，输入 `coins[6]`，返回前端约定的解卦 JSON 结构。

**Architecture:** 保持当前 `stdio MCP` 架构不变，新增一层独立 `HTTP Adapter`（FastAPI）。适配层负责输入校验、`coins -> 卦象参数` 转换、调用现有 `FengshuiHandler`、以及响应字段映射。这样可复用现有解卦核心能力，同时把前后端协议稳定在 API 层，避免直接暴露 MCP 协议给小程序。

**Tech Stack:** Python 3.10+, FastAPI, Pydantic, Uvicorn, existing `cyberYJ.server.handlers.fengshui.FengshuiHandler`, pytest + TestClient

---

### Task 1: 固化 API 契约与输入校验模型

**Files:**
- Create: `src/cyberYJ/api/__init__.py`
- Create: `src/cyberYJ/api/models.py`
- Create: `tests/test_api_models.py`
- Modify: `pyproject.toml`

**Step 1: Write the failing test**

```python
from pydantic import ValidationError
from cyberYJ.api.models import DivinationRequest


def test_divination_request_rejects_invalid_coins():
    try:
        DivinationRequest(coins=[6, 7, 8])
        assert False, "expected ValidationError"
    except ValidationError:
        assert True


def test_divination_request_accepts_six_valid_coins():
    req = DivinationRequest(coins=[6, 7, 8, 9, 7, 8], question="事业")
    assert req.coins == [6, 7, 8, 9, 7, 8]
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_api_models.py -v`  
Expected: FAIL with `ModuleNotFoundError: No module named 'cyberYJ.api'`

**Step 3: Write minimal implementation**

```python
# src/cyberYJ/api/models.py
from pydantic import BaseModel, Field, field_validator


class DivinationRequest(BaseModel):
    coins: list[int] = Field(..., min_length=6, max_length=6)
    question: str | None = None

    @field_validator("coins")
    @classmethod
    def validate_coins(cls, value: list[int]) -> list[int]:
        if any(v not in (6, 7, 8, 9) for v in value):
            raise ValueError("coins数组必须包含6个元素 (6/7/8/9)")
        return value
```

并在 `pyproject.toml` 增加：

```toml
[project.optional-dependencies]
api = [
    "fastapi>=0.115.0",
    "uvicorn>=0.30.0",
    "httpx>=0.27.0",
]
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_api_models.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add pyproject.toml src/cyberYJ/api/__init__.py src/cyberYJ/api/models.py tests/test_api_models.py
git commit -m "feat(api): add request validation models for wechat divination endpoint"
```

---

### Task 2: 实现 coins -> 卦象参数转换器

**Files:**
- Create: `src/cyberYJ/api/coin_mapper.py`
- Create: `tests/test_coin_mapper.py`

**Step 1: Write the failing test**

```python
from cyberYJ.api.coin_mapper import map_coins_to_divination_input


def test_map_coins_to_trigrams_and_changing_lines():
    mapped = map_coins_to_divination_input([8, 8, 8, 9, 8, 8])
    assert mapped["lower_trigram"] == "坤"
    assert mapped["upper_trigram"] == "震"
    assert mapped["changing_lines"] == [4]
    assert mapped["primary_changing_line"] == 4
    assert mapped["hexagram_code"] == "000100"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_coin_mapper.py -v`  
Expected: FAIL with `ModuleNotFoundError` or `ImportError`

**Step 3: Write minimal implementation**

```python
# src/cyberYJ/api/coin_mapper.py
TRIGRAM_FROM_BITS = {
    (1, 1, 1): "乾",
    (0, 1, 1): "兌",
    (1, 0, 1): "離",
    (0, 0, 1): "震",
    (1, 1, 0): "巽",
    (0, 1, 0): "坎",
    (1, 0, 0): "艮",
    (0, 0, 0): "坤",
}


def map_coins_to_divination_input(coins: list[int]) -> dict:
    bits = [1 if v in (7, 9) else 0 for v in coins]
    lower_bits = tuple(bits[:3])
    upper_bits = tuple(bits[3:])
    changing_lines = [idx + 1 for idx, v in enumerate(coins) if v in (6, 9)]
    return {
        "line_bits": bits,
        "hexagram_code": "".join(str(b) for b in bits),
        "lower_trigram": TRIGRAM_FROM_BITS[lower_bits],
        "upper_trigram": TRIGRAM_FROM_BITS[upper_bits],
        "changing_lines": changing_lines,
        "primary_changing_line": changing_lines[0] if changing_lines else None,
    }
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_coin_mapper.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/coin_mapper.py tests/test_coin_mapper.py
git commit -m "feat(api): add coin-to-trigram mapping utility"
```

---

### Task 3: 实现解卦服务适配层（复用 FengshuiHandler）

**Files:**
- Create: `src/cyberYJ/api/divination_service.py`
- Create: `tests/test_divination_service.py`

**Step 1: Write the failing test**

```python
from cyberYJ.api.divination_service import DivinationService


def test_service_returns_contract_shape():
    service = DivinationService()
    result = service.interpret([6, 7, 8, 9, 7, 7], question="事业发展")
    assert "hexagram" in result
    assert "analysis" in result
    assert "do_dont" in result
    assert "trace" in result
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_divination_service.py -v`  
Expected: FAIL with missing service implementation

**Step 3: Write minimal implementation**

```python
# src/cyberYJ/api/divination_service.py
from cyberYJ.api.coin_mapper import map_coins_to_divination_input
from cyberYJ.server.handlers.fengshui import FengshuiHandler


class DivinationService:
    def __init__(self) -> None:
        self._handler = FengshuiHandler()

    def interpret(self, coins: list[int], question: str | None = None) -> dict:
        mapped = map_coins_to_divination_input(coins)
        tool_result = self._handler.execute(
            {
                "upper_trigram": mapped["upper_trigram"],
                "lower_trigram": mapped["lower_trigram"],
                "changing_line": mapped["primary_changing_line"],
                "question_text": question,
                "question_type": None,
            }
        )
        return self._to_api_response(mapped, tool_result)
```

`_to_api_response(...)` 需完成字段映射：
- `main_hexagram` -> `hexagram`
- `changing_hexagram` -> `changing_hexagram | null`
- `five_elements/solar_term_influence/fortune_advice` -> `analysis`
- `do_dont/trace/sources` 原样映射或轻度整理

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_divination_service.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/divination_service.py tests/test_divination_service.py
git commit -m "feat(api): add divination service adapter over fengshui handler"
```

---

### Task 4: 落地 HTTP API 入口与错误响应规范

**Files:**
- Create: `src/cyberYJ/api/http_app.py`
- Create: `run_http_api.py`
- Create: `tests/test_http_divination_api.py`

**Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient
from cyberYJ.api.http_app import create_app


def test_post_interpret_success():
    client = TestClient(create_app())
    resp = client.post("/v1/divination/interpret", json={"coins": [6, 7, 8, 9, 7, 7]})
    assert resp.status_code == 200
    body = resp.json()
    assert "hexagram" in body


def test_post_interpret_invalid_input():
    client = TestClient(create_app())
    resp = client.post("/v1/divination/interpret", json={"coins": [6, 7]})
    assert resp.status_code == 400
    assert resp.json()["error"]["code"] == "INVALID_INPUT"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_http_divination_api.py -v`  
Expected: FAIL with missing app factory / route

**Step 3: Write minimal implementation**

```python
# src/cyberYJ/api/http_app.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from cyberYJ.api.models import DivinationRequest
from cyberYJ.api.divination_service import DivinationService


def create_app() -> FastAPI:
    app = FastAPI(title="CyberYJ Wechat API", version="v1")
    service = DivinationService()

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request, exc):
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "INVALID_INPUT", "message": "coins数组必须包含6个元素 (6/7/8/9)"}},
        )

    @app.post("/v1/divination/interpret")
    async def interpret(req: DivinationRequest):
        return service.interpret(req.coins, req.question)

    return app
```

`run_http_api.py`:

```python
import uvicorn
from cyberYJ.api.http_app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="0.0.0.0", port=8080)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_http_divination_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/http_app.py run_http_api.py tests/test_http_divination_api.py
git commit -m "feat(api): expose /v1/divination/interpret via fastapi"
```

---

### Task 5: 补齐响应一致性与边界行为

**Files:**
- Modify: `src/cyberYJ/api/divination_service.py`
- Modify: `tests/test_divination_service.py`
- Modify: `tests/test_http_divination_api.py`

**Step 1: Write the failing test**

```python
def test_changing_hexagram_is_null_when_no_changing_lines():
    service = DivinationService()
    result = service.interpret([7, 7, 8, 8, 7, 8], question=None)
    assert result["changing_hexagram"] is None


def test_multiple_changing_lines_keep_array_shape():
    service = DivinationService()
    result = service.interpret([6, 9, 8, 9, 6, 7], question="测试")
    assert isinstance(result["analysis"]["active_lines"], list)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_divination_service.py tests/test_http_divination_api.py -v`  
Expected: FAIL on null handling / active_lines mapping

**Step 3: Write minimal implementation**

补充映射规则：
- `changing_hexagram`: 无动爻返回 `null`
- `analysis.active_lines`: 返回动爻数组文本（如 `["第1爻动", "第4爻动"]`）
- `analysis.overall`: 优先 `scenario_analysis.overall_tendency`，否则降级为 `fortune_advice`
- `analysis.advice`: 映射 `fortune_advice`
- `sources`: 保留字符串数组，保证前端可展示

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_divination_service.py tests/test_http_divination_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/divination_service.py tests/test_divination_service.py tests/test_http_divination_api.py
git commit -m "fix(api): normalize changing hexagram and active lines mapping"
```

---

### Task 6: 文档、联调样例与回归验证

**Files:**
- Create: `docs/api/wechat-divination-http-api.md`
- Modify: `docs/project-progress.md`
- Modify: `docs/requirements.md`

**Step 1: Write the failing test**

新增文档一致性检查（轻量）：

```bash
rg -n "/v1/divination/interpret|wechat|mini program" docs
```

若未找到新增文档字段即视为未完成。

**Step 2: Run check to verify it fails**

Run: `rg -n "/v1/divination/interpret" docs/api/wechat-divination-http-api.md`  
Expected: FAIL (file not found)

**Step 3: Write minimal implementation**

文档至少包含：
- 请求/响应 JSON 示例（与 `api_requirements.md` 对齐）
- 错误码（`INVALID_INPUT`, `INTERNAL_ERROR`）
- 启动方式（`python run_http_api.py`）
- 微信联调要点（HTTPS、超时、重试）

**Step 4: Run check to verify it passes**

Run: `rg -n "/v1/divination/interpret|INVALID_INPUT|run_http_api.py" docs/api/wechat-divination-http-api.md`  
Expected: PASS (matched lines)

**Step 5: Commit**

```bash
git add docs/api/wechat-divination-http-api.md docs/project-progress.md docs/requirements.md
git commit -m "docs(api): add wechat mini-program HTTP integration guide and progress updates"
```

---

### Task 7: 全量验证与交付

**Files:**
- Modify: `README.md`

**Step 1: Write the failing test**

无新增代码测试，执行全量回归作为交付门禁。

**Step 2: Run test to verify baseline**

Run: `pytest -q`  
Expected: 全量 PASS（含新增 API 测试）

**Step 3: Write minimal implementation**

在 `README.md` 增加：
- MCP 启动方式（已有）
- HTTP API 启动方式（新增）
- 面向微信小程序联调的最小 curl 示例

**Step 4: Run verification**

Run:
- `pytest -q`
- `python run_http_api.py`（本地启动观察日志）

Expected:
- tests PASS
- 服务启动成功，监听 `:8080`

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: add HTTP API startup and integration examples"
```

---

## 关键实现约束（执行时必须遵守）

1. 不修改现有 MCP 工具名与 schema（`fengshui_divination` / `luopan_orientation`），避免影响现有 IDE 客户端。
2. HTTP API 仅做适配，不重写核心解卦算法；核心计算继续复用现有 `FengshuiHandler`。
3. `coins` 数组顺序固定为“初爻 -> 上爻”；所有变爻位置输出使用 1-based。
4. 对“多动爻”场景，MVP 先输出 `active_lines` 列表并保持接口稳定；高级爻辞细化放后续迭代。
5. 错误响应统一为：

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "..."
  }
}
```

---

## 验收标准（MVP）

- 前端可稳定调用 `POST /v1/divination/interpret` 并拿到约定结构。
- 输入非法时返回 400 + 规范错误体。
- 现有 MCP 流程回归通过，不受 HTTP API 新增影响。
- 文档可指导前端直接联调（无需阅读后端源码）。

Plan complete and saved to `docs/plans/2026-02-12-wechat-miniapp-api.md`. Two execution options:

1. Subagent-Driven (this session) - I dispatch fresh subagent per task, review between tasks, fast iteration
2. Parallel Session (separate) - Open new session with executing-plans, batch execution with checkpoints

Which approach?
