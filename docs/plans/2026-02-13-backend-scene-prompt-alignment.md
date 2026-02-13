# Backend Scene Prompt Alignment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 对齐前端 `backend_scene_prompt_requirements.md`，把 `scene_type` 驱动、场景差异化表达、逻辑一致性校验落到当前 HTTP API 主链路，并保持向后兼容。

**Architecture:** 不新增远程 LLM 依赖，继续使用现有规则引擎为主。新增“场景策略层”与“一致性校验层”：`scene_type -> 场景策略 -> 解卦结果整形 -> 一致性过滤`，并输出前端可渲染字段（`keywords/advice_tags/score`）。

**Tech Stack:** Python 3.10+, FastAPI, existing `FengshuiDivinationTool`, pytest

---

### Task 1: 接口入参扩展（scene_type）

**Files:**
- Modify: `src/cyberYJ/api/models.py`
- Modify: `tests/test_api_models.py`

**Step 1: Write the failing test**

```python
def test_divination_request_accepts_scene_type():
    req = DivinationRequest(
        coins=[6, 7, 8, 9, 7, 8],
        question="最近感情如何",
        scene_type="love",
    )
    assert req.scene_type == "love"


def test_divination_request_rejects_invalid_scene_type():
    with pytest.raises(ValidationError):
        DivinationRequest(coins=[6, 7, 8, 9, 7, 8], scene_type="unknown")
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_api_models.py::test_divination_request_accepts_scene_type tests/test_api_models.py::test_divination_request_rejects_invalid_scene_type -v`  
Expected: FAIL（字段不存在或未校验）

**Step 3: Write minimal implementation**

- 在 `DivinationRequest` 新增字段：
  - `scene_type: Optional[str]`
  - 枚举：`fortune/career/love/wealth/health/study/family/travel/lawsuit`

**Step 4: Run test to verify it passes**

Run: 同 Step 2  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/models.py tests/test_api_models.py
git commit -m "feat(api): add scene_type request field for scene-driven interpretation"
```

---

### Task 2: scene_type 路由优先级打通

**Files:**
- Modify: `src/cyberYJ/api/divination_service.py`
- Modify: `src/cyberYJ/api/http_app.py`
- Modify: `tests/test_divination_service.py`
- Modify: `tests/test_http_divination_api.py`

**Step 1: Write the failing test**

```python
def test_scene_type_has_priority_over_question_keyword():
    service = DivinationService()
    result = service.interpret(
        coins=[6, 7, 8, 9, 7, 8],
        question="我想问事业",
        scene_type="love",
    )
    assert result["scene_type"] == "love"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_divination_service.py::test_scene_type_has_priority_over_question_keyword -v`  
Expected: FAIL（无 `scene_type` 输出或优先级不对）

**Step 3: Write minimal implementation**

- `DivinationService.interpret(...)` 增加 `scene_type` 参数。
- 调用 `FengshuiHandler.execute(...)` 时：
  - `question_type` 使用映射后的中文场景（如 `love -> 感情`）
  - `question_text` 继续透传 `question`
- 优先级：
  1. `scene_type`（显式）
  2. `question` 关键词识别（隐式）
  3. 默认 `fortune`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_divination_service.py tests/test_http_divination_api.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/divination_service.py src/cyberYJ/api/http_app.py tests/test_divination_service.py tests/test_http_divination_api.py
git commit -m "feat(api): wire scene_type routing with explicit priority"
```

---

### Task 3: 场景差异化输出字段（keywords/advice_tags/score）

**Files:**
- Create: `src/cyberYJ/api/scene_output.py`
- Modify: `src/cyberYJ/api/divination_service.py`
- Modify: `tests/test_divination_service.py`

**Step 1: Write the failing test**

```python
def test_response_contains_scene_enhancement_fields():
    service = DivinationService()
    result = service.interpret([6, 7, 8, 9, 7, 8], question="问事业", scene_type="career")
    assert "scene_type" in result
    assert "keywords" in result and isinstance(result["keywords"], list)
    assert "advice_tags" in result and isinstance(result["advice_tags"], list)
    assert "score" in result and isinstance(result["score"], int)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_divination_service.py::test_response_contains_scene_enhancement_fields -v`  
Expected: FAIL

**Step 3: Write minimal implementation**

- `scene_output.py`：
  - 从 `scenario_analysis.key_points` 与 `scenario_specific` 提取 `keywords`
  - 生成 `advice_tags`（如 `守势/进取/防风险/沟通`）
  - `score` 映射规则：`rating (1-5) * 20`
- 在 service 响应顶层追加：
  - `scene_type`
  - `keywords`
  - `advice_tags`
  - `score`

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_divination_service.py -v`  
Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/scene_output.py src/cyberYJ/api/divination_service.py tests/test_divination_service.py
git commit -m "feat(api): add scene enhancement fields keywords/advice_tags/score"
```

---

### Task 4: 逻辑一致性校验器（CRITICAL）

**Files:**
- Create: `src/cyberYJ/api/consistency_guard.py`
- Modify: `src/cyberYJ/api/divination_service.py`
- Modify: `tests/test_divination_service.py`
- Modify: `tests/test_fengshui_divination.py`

**Step 1: Write the failing test**

```python
def test_guard_tone_has_no_attack_phrase_conflict():
    service = DivinationService()
    result = service.interpret(
        coins=[0, 0, 0, 1, 0, 1],  # 对应明夷路径可替换为稳定输入
        question="问感情",
        scene_type="love",
    )
    conflict = result["consistency"]["conflict_count"]
    assert conflict == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_divination_service.py::test_guard_tone_has_no_attack_phrase_conflict -v`  
Expected: FAIL

**Step 3: Write minimal implementation**

- `consistency_guard.py`：
  - 定义冲突词对（守势 vs 进攻词）
  - 扫描 `analysis.advice + do_dont`
  - 输出 `consistency`：
    - `status`: `pass|adjusted`
    - `tone`: `guard|attack|neutral`
    - `conflict_count`
    - `adjustments`
- 在 service 层统一执行 guard，并回写修正后的 `do_dont`

**Step 4: Run test to verify it passes**

Run:
- `pytest tests/test_divination_service.py tests/test_fengshui_divination.py -v`

Expected: PASS

**Step 5: Commit**

```bash
git add src/cyberYJ/api/consistency_guard.py src/cyberYJ/api/divination_service.py tests/test_divination_service.py tests/test_fengshui_divination.py
git commit -m "fix(api): enforce scene consistency guard across advice and do_dont"
```

---

### Task 5: 前后端接口文档同步（给前端同事）

**Files:**
- Create: `docs/api/wechat-scene-interface-adjustments.md`
- Modify: `docs/api/wechat-divination-http-api.md`
- Modify: `docs/project-progress.md`

**Step 1: Write the failing test**

用文档关键词校验：

```bash
rg -n "scene_type|keywords|advice_tags|score|consistency|X-Request-ID" docs/api/wechat-scene-interface-adjustments.md
```

**Step 2: Run check to verify it fails**

Run: 上述命令  
Expected: FAIL（文档不存在）

**Step 3: Write minimal implementation**

前端接口文档必须包含：
- 请求字段新增：`scene_type`
- 响应字段新增：`scene_type/keywords/advice_tags/score/consistency`
- 向后兼容策略：不传 `scene_type` 仍可工作
- 版本切换建议：`v1.2`（兼容） -> `v1.3`（可选强化）

**Step 4: Run check to verify it passes**

Run: 同 Step 1  
Expected: PASS

**Step 5: Commit**

```bash
git add docs/api/wechat-scene-interface-adjustments.md docs/api/wechat-divination-http-api.md docs/project-progress.md
git commit -m "docs(api): add frontend-facing scene interface adjustment guide"
```

---

### Task 6: 最终回归与联调样例

**Files:**
- Modify: `README.md`

**Step 1: Write the failing test**

无新增单测，执行全量回归。

**Step 2: Run test to verify baseline**

Run: `pytest -q`  
Expected: 全量 PASS

**Step 3: Write minimal implementation**

README 补充：
- `scene_type` 请求示例
- 前端调用示例（携带 `scene_type`）
- 常见错误对照（`UNAUTHORIZED/RATE_LIMITED/INVALID_INPUT`）

**Step 4: Run verification**

Run:
- `pytest -q`
- 本地请求样例：
  `curl -X POST http://127.0.0.1:18080/v1/divination/interpret -H 'X-API-Key: ...' -d '{...}'`

Expected:
- 测试通过
- 返回新增字段

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: update README with scene_type integration examples"
```

---

## 验收标准（本计划完成后）

1. 前端可显式传 `scene_type`，且后端按该场景执行，不被 `question` 关键词误导。
2. 输出包含 `keywords/advice_tags/score`，用于前端体验优化。
3. `analysis`、`do_dont`、`key_points` 无明显逻辑冲突（守势场景不再出现进攻建议）。
4. 全量测试通过，且接口文档可直接交给前端使用。

