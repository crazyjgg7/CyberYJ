# 易经六爻卜卦微信小程序 - API 接口规范 (MVP 版)

> **文档版本**: v1.0
> **创建日期**: 2026-02-12
> **适用方**: 后端 MCP 开发团队 / 前端小程序开发团队

## 1. 概述

本文档定义了微信小程序前端与后端服务（基于 CyberYJ MCP）之间的通信接口。
**目标**：实现从前端提交六次铜钱投掷结果，由后端进行卦象计算、变卦分析并返回完整解读。

## 2. 接口定义

### 2.1 六爻解卦接口

将用户的六次投掷结果（数字）转换为卦象并解读。

- **URL**: `/v1/divination/interpret`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### 请求参数 (Request Body)

```json
{
  "coins": [6, 7, 8, 9, 7, 7],     // 必填，长度为6的数组，表示从初爻到上爻的投掷结果
                                   // 6: 老阴 (变爻)
                                   // 7: 少阳 (不变)
                                   // 8: 少阴 (不变)
                                   // 9: 老阳 (变爻)
  "question": "事业发展"            // 选填，用户的问题，用于辅助解读生成
}
```

#### 响应参数 (Response Body)

```json
{
  "hexagram": {
      "code": "101010",           // 本卦二进制 (初爻->上爻)
      "name": "未济",
      "symbol": "䷿",
      "judgment": "未济：亨，小狐汔济...",
      "image": "火在水上，未济...",
      "upper_trigram": "离",
      "lower_trigram": "坎"
  },
  
  "changing_hexagram": {          // 变卦 (若无变爻则为 null)
      "code": "111111",
      "name": "乾",
      "symbol": "䷀",
      "judgment": "乾：元亨利贞...",
      "image": "天行健..."
  },
  
  "analysis": {
      "overall": "...",           // 综合解读
      "active_lines": ["初六：濡其尾，吝。"], // 动爻爻辞
      "five_elements": "...",     // 五行生克分析
      "solar_term": "...",        // 节气旺衰分析
      "advice": "..."             // 趋吉避凶建议
  },

  "do_dont": {
      "do": ["..."],
      "dont": ["..."]
  },

  "trace": [                      // 推导过程 (调试用)
      "Step 1: Generated hexagram...",
      "Step 2: Analyzed changing lines..."
  ]
}
```

#### 错误响应

```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "coins数组必须包含6个元素 (6/7/8/9)"
  }
}
```

## 3. 核心逻辑要求 (Backend Implementation)

后端服务需实现 `CyberYJ` 工具链的适配器模式：

1.  **输入转换**:
    - 前端传入 `coins` 数组 `[6,7,8,9,7,7]`。
    - 后端需将其转换为 `CyberYJ.FengshuiDivinationTool` 所需的 `upper_trigram` / `lower_trigram` / `changing_line`。
    - **转换规则**:
      - 6 (老阴) -> 0 (阴, 变)
      - 7 (少阳) -> 1 (阳, 不变)
      - 8 (少阴) -> 0 (阴, 不变)
      - 9 (老阳) -> 1 (阳, 变)
      - 将6爻分为下三爻(Lower)和上三爻(Upper)，计算对应的八卦名 (e.g., 001 -> 震)。

2.  **调用工具**:
    - 使用 `FengshuiDivinationTool.execute(...)`。
    - 传入参数包括 `upper_trigram`, `lower_trigram`, `changing_line` (根据 6/9 的位置确定，1-based index)。

3.  **结果映射**:
    - 将 `FengshuiDivinationTool` 返回的 Dict 结构映射到上述 JSON 响应格式。
    - 注意：Markdown 格式的字段 (如 `interpretation`) 可直接透传，或解析为纯文本。

## 4. 示例

**Example Request:**
```json
{
    "coins": [8,8,8, 9,8,8], // 第四爻变 (9)
    "question": "测试变卦"
}
```

**Example Response:**
```json
{
    "hexagram": { "name": "豫", "symbol": "䷏" },
    "changing_hexagram": { "name": "坤", "symbol": "䷁" },
    "analysis": {
        "overall": "豫卦变为坤卦，象征快乐之后通过顺从而获得安宁...",
        "advice": "宜居安思危..."
    }
    // ...
}
```
