# Wechat Mini Program HTTP API（MVP）

更新时间：2026-02-12

## 1. 接口概览

- URL：`POST /v1/divination/interpret`
- Content-Type：`application/json`
- 用途：小程序传入六次投掷结果（`coins`），后端返回本卦/变卦与解读结构

## 2. 请求体

```json
{
  "coins": [6, 7, 8, 9, 7, 7],
  "question": "事业发展"
}
```

说明：
- `coins` 必填，长度固定 6，顺序为 `初爻 -> 上爻`
- 允许值：`6/7/8/9`
- `question` 选填，用于场景化解读辅助

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
  "trace": [
    "Step 0: mapped coins to yin/yang bits and trigrams"
  ],
  "sources": [
    "卦辞象辞: 周易（易经）"
  ]
}
```

## 4. 错误响应

`400 INVALID_INPUT`

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "coins数组必须包含6个元素 (6/7/8/9)"
  }
}
```

`500 INTERNAL_ERROR`

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "..."
  }
}
```

## 5. 启动方式

安装（可选依赖组）：

```bash
pip install -e ".[api]"
```

启动 HTTP API：

```bash
python run_http_api.py
```

默认监听：`http://0.0.0.0:8080`

## 6. 联调建议（小程序）

- 生产环境必须走 HTTPS，且将域名加入小程序 request 合法域名
- 前端超时建议：10 秒
- 前端重试建议：弱网场景最多 2 次
- `coins` 由前端负责生成并按 `初爻->上爻` 顺序提交

## 7. curl 示例

```bash
curl -X POST "http://127.0.0.1:8080/v1/divination/interpret" \
  -H "Content-Type: application/json" \
  -d '{"coins":[6,7,8,9,7,7],"question":"事业发展"}'
```

