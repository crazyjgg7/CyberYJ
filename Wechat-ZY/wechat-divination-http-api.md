# Wechat Mini Program HTTP API（MVP+）

更新时间：2026-02-13（scene_type 对齐版）

## 1. 接口概览

- URL：`POST /v1/divination/interpret`
- Content-Type：`application/json`
- Header：`X-API-Key: <your_api_key>`
- Header（可选）：`X-Request-ID: <client_trace_id>`
- 用途：小程序传入六次投掷结果（`coins`），后端返回本卦/变卦与解读结构

## 1.1 安全与限流（MVP）

- 鉴权：必须提供 `X-API-Key`
- 限流：固定窗口限流（默认 60 次/60 秒，按 `API-Key + IP` 统计）
- 请求追踪：每个响应都返回 `X-Request-ID`，便于问题排查
- 可配置环境变量：
  - `CYBERYJ_API_KEY`（默认：`cyberyj-dev-key`，上线必须替换）
  - `CYBERYJ_RATE_LIMIT_MAX`（默认：`60`）
  - `CYBERYJ_RATE_LIMIT_WINDOW_SECONDS`（默认：`60`）

## 2. 请求体

```json
{
  "coins": [6, 7, 8, 9, 7, 7],
  "question": "事业发展",
  "scene_type": "career"
}
```

说明：
- `coins` 必填，长度固定 6，顺序为 `初爻 -> 上爻`
- 允许值：`6/7/8/9`
- `question` 选填，用于场景化解读辅助
- `scene_type` 选填，建议传入，枚举：
  - `fortune`
  - `career`
  - `love`
  - `wealth`
  - `health`
  - `study`
  - `family`
  - `travel`
  - `lawsuit`

场景优先级：
1. 显式 `scene_type`
2. `question` 关键词推断
3. 默认 `fortune`

## 3. 响应体（成功）

```json
{
  "hexagram": {
    "code": "110111",
    "name": "大有",
    "symbol": "䷍",
    "judgment": "元亨。",
    "image": "火在天上，大有；君子以遏恶扬善，顺天休命。",
    "upper_trigram": "離",
    "lower_trigram": "乾"
  },
  "changing_hexagram": {
    "code": "010011",
    "name": "屯",
    "symbol": "䷂",
    "judgment": "元亨利贞，勿用有攸往，利建侯。",
    "image": "云雷，屯；君子以经纶。"
  },
  "scene_type": "career",
  "analysis": {
    "overall": "...",
    "active_lines": ["第1爻动（老阴）"],
    "five_elements": "...",
    "solar_term": "...",
    "advice": "..."
  },
  "do_dont": {
    "do": ["..."],
    "dont": ["..."]
  },
  "keywords": ["稳扎稳打", "贵人助力", "避免冒进"],
  "advice_tags": ["进取", "职场", "防风险"],
  "score": 80,
  "consistency": {
    "status": "pass",
    "tone": "attack",
    "conflict_count": 0,
    "adjustments": []
  },
  "trace": [
    "Step 0: mapped coins to yin/yang bits and trigrams"
  ],
  "sources": [
    "卦辞象辞: 周易（易经）"
  ]
}
```

字段说明（新增）：
- `scene_type`：后端最终生效场景
- `keywords`：从场景 key points / advice 提炼的前端标签词
- `advice_tags`：建议标签（例如 `守势/进取/防风险/沟通`）
- `score`：场景评分（`rating*20`，范围 20~100）
- `consistency`：建议一致性元数据（`status/tone/conflict_count/adjustments`）

## 4. 错误响应

`400 INVALID_INPUT`

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "coins数组必须包含6个元素 (6/7/8/9)",
    "request_id": "e71af9d87fdb4bb0b8f2c7fcd74cd2d8"
  }
}
```

`500 INTERNAL_ERROR`

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "...",
    "request_id": "e71af9d87fdb4bb0b8f2c7fcd74cd2d8"
  }
}
```

`401 UNAUTHORIZED`

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "missing or invalid X-API-Key",
    "request_id": "e71af9d87fdb4bb0b8f2c7fcd74cd2d8"
  }
}
```

`429 RATE_LIMITED`

```json
{
  "error": {
    "code": "RATE_LIMITED",
    "message": "rate limit exceeded, retry in 42s",
    "request_id": "e71af9d87fdb4bb0b8f2c7fcd74cd2d8"
  }
}
```

并返回响应头：
- `X-Request-ID`
- `Retry-After`
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

## 4.1 结构化日志与错误追踪

- 日志格式：JSON 行日志（单行可解析）
- 关键事件：
  - `request.received`
  - `request.completed`
  - `request.rejected`
  - `request.error`
- 关键字段：
  - `request_id`
  - `method` / `path`
  - `status_code`
  - `duration_ms`
  - `error_code`（错误时）

## 5. 启动方式

安装（可选依赖组）：

```bash
pip install -e ".[api]"
```

方式 A（推荐，双击脚本）：

```bash
/Users/apple/Desktop/start-cyberYJ-http-api.command
```

说明：
- 脚本会自动检查 `venv`、`fastapi/uvicorn`、以及路由自检
- 默认端口 `18080`，如被占用会自动切到 `18081`

方式 B（命令行）：

```bash
python run_http_api.py
```

默认监听：`http://0.0.0.0:18080`

## 6. 联调建议（小程序）

- 生产环境必须走 HTTPS，且将域名加入小程序 request 合法域名
- 前端超时建议：10 秒
- 前端重试建议：弱网场景最多 2 次
- `coins` 由前端负责生成并按 `初爻->上爻` 顺序提交

## 7. curl 示例

```bash
curl -X POST "http://127.0.0.1:18080/v1/divination/interpret" \
  -H "X-API-Key: cyberyj-dev-key" \
  -H "X-Request-ID: req-demo-001" \
  -H "Content-Type: application/json" \
  -d '{"coins":[6,7,8,9,7,7],"question":"事业发展","scene_type":"career"}'
```

## 8. 小程序前端调用示例

```javascript
// services/api.js
function interpretHexagram({ coins, question, sceneType, baseUrl }) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${baseUrl}/v1/divination/interpret`,
      method: 'POST',
      timeout: 10000,
      header: {
        'Content-Type': 'application/json',
        'X-API-Key': '<your_api_key>'
      },
      data: {
        coins,
        question,
        scene_type: sceneType // 推荐显式透传
      },
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
          return
        }
        reject(res.data?.error || { code: 'HTTP_ERROR', message: `status=${res.statusCode}` })
      },
      fail(err) {
        reject({ code: 'NETWORK_ERROR', message: err?.errMsg || 'request failed' })
      }
    })
  })
}
```

## 9. 如何让前端“正常调用”

1. 本地联调：启动 API 后，把 `baseUrl` 配成你机器可访问地址（同局域网 IP + 端口）。
2. 远程联调：把 API 暴露为公网 HTTPS（云服务器或内网穿透 + HTTPS）。
3. 小程序后台配置：把该 HTTPS 域名加入“request 合法域名”。
4. 前端发布配置：使用线上 `baseUrl`，不要写死本地地址。

兼容说明：
- 不传 `scene_type` 仍可调用，后端会退回关键词推断/默认场景。
- 前端可分阶段接入新增响应字段：先只传 `scene_type`，再启用 `keywords/advice_tags/score/consistency` 展示。
