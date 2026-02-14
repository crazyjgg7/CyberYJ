const { generateLine } = require('../../utils/divination.js');
const gyroService = require('../../services/gyro.js');

Page({
    data: {
        lines: [], // [bottom, ..., top]
        status: 'idle', // 'idle' | 'shaking' | 'complete'
        mode: 'gyro', // 'gyro' | 'touch' | 'input'
        isGyroSupported: true,
        showGuide: false,
        manualCoins: [2, 2, 2], // Default Yang (2)
        sceneId: '', // 场景 ID
        sceneName: '', // 场景名称
        question: '' // 用户输入
    },

    onLoad(options) {
        // 接收主题和输入参数
        const sceneId = options.scene || 'other';
        const question = decodeURIComponent(options.question || '');

        // 获取场景信息
        const { getSceneById, getDefaultQuestion } = require('../../utils/scenes.js');
        const scene = getSceneById(sceneId);
        const finalQuestion = question || getDefaultQuestion(sceneId);

        this.setData({
            sceneId: sceneId,
            sceneName: scene ? scene.name : '其他',
            question: finalQuestion
        });

        // Check Gyro Support
        const supported = gyroService.isSupported();
        this.setData({
            isGyroSupported: supported,
            mode: supported ? 'gyro' : 'touch'
        });

        if (supported) {
            this.initGyroListeners();
        }

        // Check if guide seen
        const seen = wx.getStorageSync('has_seen_guide');
        if (!seen) {
            this.setData({ showGuide: true });
        }

        // Init Audio
        this.shakeAudio = wx.createInnerAudioContext();
        this.shakeAudio.src = '/audio/shake.mp3'; // Optimized to mp3
        this.shakeAudio.onError((res) => {
            console.log('Audio Error:', res.errMsg);
        });
    },

    closeGuide() {
        this.setData({ showGuide: false });
        wx.setStorageSync('has_seen_guide', true);
    },

    dummy() { }, // Prevent tap propagation

    onShow() {
        if (this.data.mode === 'gyro') {
            gyroService.start().catch(err => {
                console.error('Start Gyro Error:', err);
                wx.showToast({ title: '感应开启失败，请重试', icon: 'none' });
            });
        }
    },

    onHide() {
        gyroService.stop();
    },

    onUnload() {
        gyroService.stop();
    },

    initGyroListeners() {
        gyroService.onShake(() => {
            this.handleGyroShake();
        });

        gyroService.onSettle(() => {
            this.handleGyroSettle();
        });
    },

    toggleMode() {
        wx.showActionSheet({
            itemList: ['感应生成 (摇一摇)', '手动生成 (点击)', '手动输入 (自选)'],
            success: (res) => {
                const index = res.tapIndex;
                let newMode = 'gyro';
                if (index === 0) newMode = 'gyro';
                if (index === 1) newMode = 'touch';
                if (index === 2) newMode = 'input';

                this.switchMode(newMode);
            },
            fail: (res) => {
                console.log('ActionSheet cancelled:', res.errMsg);
            }
        });
    },

    switchMode(mode) {
        // Stop gyro if leaving gyro mode
        if (this.data.mode === 'gyro' && mode !== 'gyro') {
            gyroService.stop();
        }

        // Start gyro if entering gyro mode
        if (mode === 'gyro') {
            if (!this.data.isGyroSupported) {
                wx.showToast({ title: '设备不支持陀螺仪，建议使用点击生成', icon: 'none' });
            }
            gyroService.start().catch(err => {
                console.error('Start Gyro Error:', err);
                wx.showToast({ title: '感应开启失败，切换至点击模式', icon: 'none' });
                this.switchMode('touch');
                return;
            });
        }

        // Reset state for new mode
        this.setData({
            mode: mode,
            manualCoins: [2, 2, 2], // Reset for input mode
            showGuide: false
        });

        // Show toast for mode feedback
        let modeName = '感应模式';
        if (mode === 'touch') modeName = '点击生成';
        if (mode === 'input') modeName = '手动输入';
        wx.showToast({ title: `已切换至${modeName}`, icon: 'none' });
    },

    // --- Touch Mode Logic ---
    handleTouchShake() {
        if (this.data.status !== 'idle' && this.data.status !== 'complete') return;
        if (this.data.lines.length >= 6) return;

        this.setData({ status: 'shaking' });
        wx.vibrateShort({ type: 'medium' });

        // Play Sound
        if (this.shakeAudio) {
            this.shakeAudio.stop();
            this.shakeAudio.play();
        }

        // Simulate Settle after delay
        setTimeout(() => {
            this.handleGyroSettle();
        }, 800);
    },

    // --- Manual Input Logic ---
    toggleCoin(e) {
        const idx = e.currentTarget.dataset.index;
        const currentCoins = this.data.manualCoins;
        const newVal = currentCoins[idx] === 2 ? 3 : 2;

        currentCoins[idx] = newVal;
        this.setData({ manualCoins: currentCoins });
        wx.vibrateShort({ type: 'light' });
    },

    confirmManualLine() {
        if (this.data.lines.length >= 6) return;

        const coins = this.data.manualCoins;
        const sum = coins.reduce((a, b) => a + b, 0);

        const newLine = {
            value: sum,
            coins: [...coins]
        };

        const newLines = [...this.data.lines, newLine];
        this.setData({ lines: newLines });

        if (newLines.length >= 6) {
            this.setData({ status: 'complete' });
            wx.vibrateLong();
        }
    },

    // --- Logic ---

    handleGyroShake() {
        if (this.data.status === 'complete') return;

        if (this.data.status !== 'shaking') {
            this.setData({ status: 'shaking' });
            wx.vibrateShort({ type: 'medium' });

            // Play Sound
            if (this.shakeAudio) {
                this.shakeAudio.stop();
                this.shakeAudio.play();
            }
        }
    },

    handleGyroSettle() {
        if (this.data.status === 'complete') return;

        // Relaxed check: Trust gyroService's settle event
        this.shakeOnce();

        // Reset to idle
        if (this.data.lines.length < 6) {
            this.setData({ status: 'idle' });
        }
    },

    handleAction() {
        if (this.data.status === 'complete') {
            this.goToResult();
        } else {
            // Touch Mode Trigger
            if (this.data.mode === 'touch' || this.data.mode === 'button') {
                this.handleTouchShake();
            }
        }
    },

    shakeOnce() {
        if (this.data.lines.length >= 6) return;

        // ... vibrate ...
        if (this.data.mode === 'button' || this.data.mode === 'touch') {
            wx.vibrateShort({ type: 'light' });
        } else {
            wx.vibrateShort({ type: 'heavy' });
        }

        const newLine = generateLine(); // Returns object {value, coins}
        const newLines = [...this.data.lines, newLine];

        this.setData({
            lines: newLines
        });

        if (newLines.length >= 6) {
            this.setData({ status: 'complete' });
            wx.vibrateLong();
            gyroService.stop();
        }
    },

    goToResult() {
        const lines = this.data.lines;
        const coinsValues = lines.map(l => l.value);
        const coinsStr = JSON.stringify(coinsValues);

        wx.navigateTo({
            url: `/pages/result/result?coins=${coinsStr}&scene=${this.data.sceneId}&sceneName=${encodeURIComponent(this.data.sceneName)}&question=${encodeURIComponent(this.data.question)}`
        });
    }
});
