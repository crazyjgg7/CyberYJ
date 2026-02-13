# Wechat 前后端接口调整说明（场景化 Prompt 对齐）

更新时间：2026-02-13  
适用范围：`/v1/divination/interpret`（HTTP API）

## 1. 背景

前端体验测试反馈：同一结果中出现“核心建议偏守势”但“宜做偏进攻”的逻辑冲突。  
本次接口调整目标：

1. 支持前端显式传入 `scene_type`，避免仅依赖关键词推断。
2. 输出前端可直接渲染的场景增强字段（`keywords/advice_tags/score`）。
3. 输出一致性标记（`consistency`），便于前端灰度监控与问题追踪。

---

## 2. 请求参数调整

## 2.1 新增字段

- `scene_type`（可选，推荐传）
  - 枚举：
    - `fortune`
    - `career`
    - `love`
    - `wealth`
    - `health`
    - `study`
    - `family`
    - `travel`
    - `lawsuit`

## 2.2 现有字段

- `coins`：必填，长度 6，仅 `6/7/8/9`
- `question`：选填，用户原始问题

## 2.3 处理优先级（后端）

1. `scene_type`（显式优先）
2. `question` 关键词识别
3. 默认 `fortune`

---

## 3. 响应字段调整

## 3.1 兼容保留（不变）

- `hexagram`
- `changing_hexagram`
- `analysis`
- `do_dont`
- `trace`
- `sources`

## 3.2 新增字段

- `scene_type`: string  
  最终生效场景（便于前端回显）

- `keywords`: string[]  
  场景关键词（可用于标签区）

- `advice_tags`: string[]  
  建议标签（如：`守势`、`防风险`、`沟通`）

- `score`: number (0-100)  
  场景相关评分（用于前端进度条/雷达图）

- `consistency`:
  - `status`: `pass | adjusted`
  - `tone`: `guard | attack | neutral`
  - `conflict_count`: number
  - `adjustments`: string[]

---

## 4. 新旧请求示例

### 4.1 旧请求（兼容）

```json
{
  "coins": [6, 7, 8, 9, 7, 7],
  "question": "问感情"
}
```

### 4.2 新请求（推荐）

```json
{
  "coins": [6, 7, 8, 9, 7, 7],
  "question": "问感情",
  "scene_type": "love"
}
```

---

## 5. 新响应示例（关键片段）

```json
{
  "scene_type": "love",
  "analysis": {
    "overall": "不利",
    "advice": "..."
  },
  "do_dont": {
    "do": ["保持低调", "先稳关系"],
    "dont": ["盲目冒进", "高调冲突"]
  },
  "keywords": ["感情易受伤", "低调守护", "避免冲突"],
  "advice_tags": ["守势", "防风险", "关系修复"],
  "score": 40,
  "consistency": {
    "status": "pass",
    "tone": "guard",
    "conflict_count": 0,
    "adjustments": []
  }
}
```

---

## 6. 前端改造建议（最小）

1. 请求时始终带 `scene_type`（用户在页面选择的场景）。
2. 若 `consistency.status != "pass"`，前端可埋点告警（仅监控，不阻断）。
3. UI 优先使用：
   - `keywords` -> 标签流
   - `advice_tags` -> 建议分类
   - `score` -> 指数条

---

## 7. 上线与兼容策略

1. 本次为兼容增量，不删除旧字段。
2. 前端可分两步灰度：
   - 第一步：只传 `scene_type`，忽略新响应字段。
   - 第二步：启用 `keywords/advice_tags/score/consistency` 展示。
3. 错误响应保持不变：`INVALID_INPUT/UNAUTHORIZED/RATE_LIMITED/INTERNAL_ERROR`。

