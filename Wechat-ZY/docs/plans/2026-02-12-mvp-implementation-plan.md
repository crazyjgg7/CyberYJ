# [MVP] 易经六爻卜卦微信小程序 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 基于微信小程序原生框架，实现"按钮六爻起卦" -> "调用 Mock API" -> "展示解卦结果" 的最小可行链路。

**Architecture:** 
- **前端**: 原生微信小程序 (WXML/WXSS/JS)。
- **逻辑**: 包含一个 `DivinationService` 用于生成六爻数据和调用 API。
- **UI/UX**: 遵循 @mobile-design (Touch-First) 和 @frontend-design (Intentional Aesthetic) 原则。
- **接口**: 暂时使用 Mock 服务模拟后端返回，后期替换为真实 HTTPS 请求。

**Tech Stack:** 微信小程序原生开发, JavaScript (ES6+), wx.request, CSS Variables (Design Tokens).

**Relevant Skills:**
- @mobile-design: 确保触摸目标 >= 44px，处理离线状态，避免 ScrollView 性能陷阱。
- @frontend-design: 定义清晰的设计令牌（颜色、字体），避免通用 AI UI 风格。
- @ui-ux-pro-max: 检查无障碍性（对比度、alt 文本）、Loading 状态和错误反馈。

---

### Task 1: 项目初始化与基础设计架构
**Files:**
- Create: `app.json`
- Create: `project.config.json`
- Create: `app.js`
- Create: `app.wxss` (Design Tokens)
- Create: `pages/index/index.{wxml,wxss,js,json}`

**Step 1: 创建 app.json 与项目配置**
初始化小程序的基本配置。
- **Check**: `@ui-ux-pro-max` - 确保导航栏标题清晰，颜色对比度符合无障碍标准。

**Step 2: 定义 Design Tokens (app.wxss)**
依据 `@frontend-design`，定义全局 CSS 变量。
- 颜色：定义主色（Primary）、背景色（Background）、文本色（Text）。
- 字体：定义字号层级。
- 间距：定义标准间距单位。
```css
/* app.wxss */
page {
  --primary-color: #D4AF37; /* 示例金色 */
  --bg-color: #FAFAFA;
  --text-main: #333333;
  --spacing-unit: 16rpx;
}
```

**Step 3: 创建首页 (Index Page)**
创建一个简单的首页，包含一个"开始卜卦"的按钮。
- **Check**: `@mobile-design` - 按钮高度至少 44px (88rpx)，有明确的点击态（active state）。

**Step 4: 运行与验证**
Run: `ls -R` 检查文件结构。

---

### Task 2: 六爻生成逻辑与 API Service (Mock)
**Files:**
- Create: `utils/divination.js`
- Create: `services/api.js`
- Test: `tests/divination_test.js`

**Step 1: 实现六爻随机生成逻辑**
在 `utils/divination.js` 中实现 `generateSixLines()`。
- **Check**: `@clean-code` - 逻辑清晰，函数单一职责。

**Step 2: 实现 API Service Mock**
在 `services/api.js` 中实现 `interpretHexagram(coins)`。
- **Check**: `@ui-ux-pro-max` - 模拟网络延迟（1s-3s），以便前端展示 Loading 状态。

**Step 3: 编写测试脚本验证逻辑**
Run: `node tests/divination_test.js`

---

### Task 3: 卜卦页面 (Divination Page)
**Files:**
- Create: `pages/divination/divination.{wxml,wxss,js,json}`

**Step 1: 页面布局**
- 顶部提示："请诚心默念问题，点击按钮6次"。
- 中间区域：展示已生成的爻（从下往上堆叠）。
- 底部按钮："点击摇卦"。

**Step 2: 交互逻辑**
- 点击按钮调用 `utils/divination.js`。
- **Check**: `@mobile-design` - 按钮置于"拇指热区"（Thumb Zone）。
- **Check**: `@ui-ux-pro-max` - 点击时提供触觉反馈（`wx.vibrateShort`）或视觉反馈。

**Step 3: 状态管理**
- 当 `lines.length === 6` 时，按钮变更为"查看结果"。
- **Check**: `@ui-ux-pro-max` - 状态切换时应有过渡动画（Transition），避免突变。

---

### Task 4: 结果展示页面 (Result Page)
**Files:**
- Create: `pages/result/result.{wxml,wxss,js,json}`

**Step 1: 页面布局**
- Loading 状态界面：使用 Skeleton 或 Spinner。
- 结果展示界面：卦名、卦辞、解读。

**Step 2: 业务逻辑**
- `onLoad` 时获取数据。
- **Check**: `@ui-ux-pro-max` - 处理错误状态（如 API 失败），提供"重试"按钮。
- **Check**: `@frontend-design` - 排版要有呼吸感（White space），重点突出卦辞。

---

### Task 5: 集成测试与验证
**Files:**
- Modify: `app.json`

**Step 1: 完整链路测试**
- 手动验证流程：
  1. 首页 -> 卜卦页（检查按钮热区、反馈）。
  2. 摇卦6次（检查动画/过渡）。
  3. 结果页（检查 Loading、错误重试、排版阅读体验）。
- **Check**: `@mobile-design` - 在真机或模拟器上检查触摸体验。

**Step 2: 提交代码**
```bash
git add .
git commit -m "feat(mvp): implement basic flow with mobile-first design principles"
```
