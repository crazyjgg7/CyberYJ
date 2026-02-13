/* profile.js */
const storage = require('../../utils/storage.js');

Page({
    data: {
        gyroEnabled: true,
        historyCount: 0
    },

    onShow() {
        // Load settings
        const gyro = wx.getStorageSync('setting_gyro') !== false; // Default true if undefined
        const history = storage.getHistory() || [];
        this.setData({
            gyroEnabled: gyro,
            historyCount: history.length
        });
    },

    toggleGyro(e) {
        let value;
        if (e.type === 'change') {
            value = e.detail.value;
        } else {
            // Tap on cell, toggle current state
            value = !this.data.gyroEnabled;
        }

        wx.setStorageSync('setting_gyro', value);
        this.setData({ gyroEnabled: value });
        wx.showToast({ title: value ? '已开启摇一摇' : '已切换至按钮模式', icon: 'none' });
    },

    goToHistory() {
        wx.navigateTo({ url: '/pages/history/history' });
    },

    clearHistory() {
        wx.showModal({
            title: '清除缓存',
            content: '确定要清除所有卜卦记录吗？',
            success: (res) => {
                if (res.confirm) {
                    storage.clearHistory();
                    wx.showToast({ title: '已清除', icon: 'success' });
                    this.onShow();
                }
            }
        });
    },

    showAbout() {
        wx.showModal({
            title: '关于 CyberYJ',
            content: 'CyberYJ 六爻卜卦\nv1.0.0\n\n融合传统易经智慧与现代交互体验。\n\n技术支持: Antigravity AI',
            showCancel: false,
            confirmText: '我知道了',
            confirmColor: '#D4AF37'
        });
    }
});
