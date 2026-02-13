const { interpretHexagram } = require('../../services/api.js');
const storage = require('../../utils/storage.js');

Page({
    data: {
        loading: true,
        error: false,
        errorMsg: '',
        result: null, // Full API response
        isHistory: false,
        sceneId: '',
        sceneName: '',
        question: ''
    },

    onLoad(options) {
        // 接收场景和问题参数
        const sceneId = options.scene || '';
        const sceneName = decodeURIComponent(options.sceneName || '');
        const question = decodeURIComponent(options.question || '');

        // Compute theme class
        const themeClass = sceneId ? `theme-${sceneId}` : '';

        this.setData({
            sceneId: sceneId,
            sceneName: sceneName,
            question: question,
            themeClass: themeClass
        });

        if (options.id) {
            // Load from History
            const record = storage.getHistoryById(options.id);
            if (record) {
                // Format timestamp for display if needed, but wxml can handle or use wxs
                this.setData({
                    result: record.result,
                    sceneId: record.sceneId || '',
                    sceneName: record.sceneName || '',
                    question: record.question || '',
                    loading: false,
                    isHistory: true
                });
            } else {
                this.setError('记录不存在');
            }
        } else if (options.coins) {
            // New Divination
            try {
                const coins = JSON.parse(options.coins);
                this.fetchResult(coins);
            } catch (e) {
                this.setError('无效的数据格式');
            }
        } else {
            this.setError('缺少卦象数据');
        }
    },

    retryFetch() {
        // Retry logic depends on context (history or fresh)
        // If history failed loading (n/a), just go back.
        // If fresh failed, we need coins.
        // For simplicity, we assume retry is for fetch failure.
        // We need to store coins in data if we want retry support.
        // But options logic covers it mostly.
        this.setError('请重新起卦');
    },

    fetchResult(coins) {
        this.setData({ loading: true, error: false });

        interpretHexagram(coins, this.data.question, this.data.sceneId)
            .then(res => {
                // Enrich result with metadata for storage
                const enrichedResult = {
                    timestamp: Date.now(),
                    id: Date.now().toString(),
                    coins: coins,
                    sceneId: this.data.sceneId,
                    sceneName: this.data.sceneName,
                    question: this.data.question,
                    result: res // API response
                };

                // Save to History
                storage.saveHistory(enrichedResult);

                this.setData({
                    loading: false,
                    result: res, // Use API response directly for display
                    isHistory: false
                });
            })
            .catch(err => {
                console.error(err);
                this.setData({
                    loading: false,
                    error: true,
                    errorMsg: err.message || '解卦失败，请检查网络'
                });
            });
    },

    setError(msg) {
        this.setData({
            loading: false,
            error: true,
            errorMsg: msg
        });
    },

    goHome() {
        wx.reLaunch({
            url: '/pages/index/index'
        });
    },

    generatePoster() {
        if (!this.data.result) return;
        wx.showLoading({ title: '生成海报中...' });

        const query = wx.createSelectorQuery().in(this);
        query.select('#posterCanvas')
            .fields({ node: true, size: true })
            .exec((res) => {
                if (!res || !res[0]) {
                    wx.hideLoading();
                    wx.showToast({ title: 'Canvas 错误', icon: 'none' });
                    return;
                }
                const canvas = res[0].node;
                const ctx = canvas.getContext('2d');
                const dpr = wx.getSystemInfoSync().pixelRatio;

                // Set canvas size for high-res
                canvas.width = res[0].width * dpr;
                canvas.height = res[0].height * dpr;
                ctx.scale(dpr, dpr);

                const w = res[0].width;
                const h = res[0].height;

                // --- Drawing ---
                // Background
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(0, 0, w, h);

                // Border
                ctx.lineWidth = 4;
                ctx.strokeStyle = '#bd9759'; // Primary color
                ctx.strokeRect(10, 10, w - 20, h - 20);

                // Title
                ctx.fillStyle = '#333333';
                ctx.font = 'bold 20px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'top';
                ctx.fillText('CyberYJ 六爻卜卦', w / 2, 40);

                // Hexagram Symbol
                ctx.fillStyle = '#bd9759';
                ctx.font = 'bold 80px sans-serif'; // Using standard font
                ctx.fillText(this.data.result.hexagram.symbol, w / 2, 120);

                // Hexagram Name
                ctx.fillStyle = '#333333';
                ctx.font = 'bold 32px sans-serif';
                ctx.fillText(this.data.result.hexagram.name + '卦', w / 2, 220);

                // Judgment
                ctx.font = '16px sans-serif';
                ctx.fillStyle = '#666666';

                const text = this.data.result.hexagram.judgment;
                const maxWidth = w - 60;
                const lineHeight = 24;
                let y = 280;

                // Split text for word wrap
                let line = '';
                for (let i = 0; i < text.length; i++) {
                    const testLine = line + text[i];
                    if (ctx.measureText(testLine).width > maxWidth && i > 0) {
                        ctx.fillText(line, w / 2, y);
                        line = text[i];
                        y += lineHeight;
                    } else {
                        line = testLine;
                    }
                }
                ctx.fillText(line, w / 2, y);

                // Footer
                ctx.fillStyle = '#999999';
                ctx.font = '12px sans-serif';
                ctx.fillText('—— 长按识别，问吉凶 ——', w / 2, h - 50);

                // Save
                setTimeout(() => {
                    wx.canvasToTempFilePath({
                        canvas: canvas,
                        success: (res) => {
                            wx.saveImageToPhotosAlbum({
                                filePath: res.tempFilePath,
                                success: () => {
                                    wx.hideLoading();
                                    wx.showToast({ title: '已保存到相册', icon: 'success' });
                                },
                                fail: (err) => {
                                    wx.hideLoading();
                                    if (err.errMsg.includes('auth')) {
                                        wx.showModal({
                                            title: '提示',
                                            content: '需要保存图片权限',
                                            success: (res) => {
                                                if (res.confirm) wx.openSetting();
                                            }
                                        });
                                    } else {
                                        wx.showToast({ title: '保存失败', icon: 'none' });
                                    }
                                }
                            });
                        },
                        fail: (err) => {
                            wx.hideLoading();
                            wx.showToast({ title: '生成图片失败', icon: 'none' });
                            console.error(err);
                        }
                    });
                }, 200);
            });
    },

    onShareAppMessage() {
        const title = this.data.result ? `我在 CyberYJ 求得一卦：【${this.data.result.hexagram.name}】，你也来试试？` : 'CyberYJ 六爻卜卦';
        const path = this.data.result ? `/pages/result/result?coins=${JSON.stringify(this.data.result.coins)}` : '/pages/index/index';
        return {
            title: title,
            path: path
        };
    },

    onShareTimeline() {
        const title = this.data.result ? `我在 CyberYJ 求得一卦：【${this.data.result.hexagram.name}】` : 'CyberYJ 六爻卜卦';
        return {
            title: title,
            query: this.data.result ? `coins=${JSON.stringify(this.data.result.coins)}` : ''
        };
    }
});
