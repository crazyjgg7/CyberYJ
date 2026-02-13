# [Phase 2] Gyroscope Interaction Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 基于微信小程序 `wx.startDeviceMotionListening` API，实现“摇一摇”起卦功能，提供更具仪式感的交互体验。

**Architecture:** 
- **Service Layer**: `services/gyro.js` (单例模式) 负责监听设备运动数据，封装 Shake/Settle 事件。
- **UI Layer**: `pages/divination/divination` 增加陀螺仪模式状态机 (Idle -> Listening -> Shaking -> Thrown -> Settled)。
- **Feedback**: 结合 `wx.vibrateShort` (轻触反馈) 和 `wx.vibrateLong` (成功反馈)。

**Tech Stack:** 微信小程序 DeviceMotion API, CSS Animation.

**Relevant Skills:**
- @mobile-design: 权限申请流程（优雅降级），节流（Throttle）防止频繁触发。
- @ui-ux-pro-max: 视觉反馈与震动反馈的同步。

---

### Task 1: GyroService 基础服务
**Files:**
- Create: `services/gyro.js`
- Modify: `app.json` (permission declaration)

**Step 1: 创建 GyroService**
实现监听逻辑：
- `start()`: 调用 `wx.startDeviceMotionListening({ interval: 'game' })`。
- `stop()`: 停止监听。
- `onShake(cb)`: 当加速度矢量长度 > 1.5g 时触发。
- `onSettle(cb)`: 当加速度恢复平稳维持 500ms 时触发。

**Step 2: 权限配置**
在 `app.json` 中添加 `permission` 字段（如果需要，微信小程序部分API需声明）。
*注：`DeviceMotion` 通常无需显式声明，但在 iOS 下需处理用户授权回调。*

---

### Task 2: 卜卦页面状态机升级
**Files:**
- Modify: `pages/divination/divination.js`
- Modify: `pages/divination/divination.wxml`

**Step 1: 引入 GyroService**
在 `onLoad` 初始化，`onUnload` 销毁。
- **Check**: `@mobile-design` - 确保页面隐藏 (`onHide`) 时停止监听，节省电量。

**Step 2: 实现交互状态机**
- **Idle**: 提示“摇动手机”。
- **Shaking**: 监测到摇动 -> 播放震动 `wx.vibrateShort(medium)` -> 更新 UI“摇动中”。
- **Thrown**: 监测到停止（Settle）-> 触发 `generateLine()` -> 播放震动 `wx.vibrateLong` -> 动画展示结果。

**Step 3: 模式切换**
添加“切换手动/自动”按钮，允许用户降级到按钮模式。

---

### Task 3: 视觉与触觉反馈优化
**Files:**
- Modify: `pages/divination/divination.wxss`

**Step 1: 摇动动画**
添加 CSS 动画 `.shaking`，使铜钱/提示图标左右晃动。

**Step 2: 结果展示动画**
新生成的爻线使用 Slide-In 动画出现。

---

### Task 4: 真机调试与验证
**验证方案**:
由于模拟器无法完美模拟加速度变化（只能简单模拟），需使用 **微信开发者工具-真机调试**。
- Case 1: 快速摇动 -> 触发 Shaking。
- Case 2: 停止摇动 -> 触发 Settled -> 生成爻。
- Case 3: 拒绝权限 -> 提示并切回按钮模式。
