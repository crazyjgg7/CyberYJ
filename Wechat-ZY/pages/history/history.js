/* history.js */
const storage = require('../../utils/storage.js');

Page({
    data: {
        history: []
    },

    onShow() {
        this.loadHistory();
    },

    loadHistory() {
        const history = storage.getHistory() || [];
        // Format date for display
        // We use simple JS date string for now.
        const formatted = history.map(item => {
            const d = new Date(item.timestamp);
            return {
                ...item,
                dateStr: `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()} ${d.getHours()}:${d.getMinutes().toString().padStart(2, '0')}`
            };
        });
        this.setData({ history: formatted });
    },

    viewDetail(e) {
        const id = e.currentTarget.dataset.id;
        wx.navigateTo({
            url: `/pages/result/result?id=${id}`
        });
    },

    clearHistory() {
        wx.showModal({
            title: '提示',
            content: '确定清空所有卜卦记录吗？',
            success: (res) => {
                if (res.confirm) {
                    storage.clearHistory();
                    this.loadHistory();
                }
            }
        });
    }
});
