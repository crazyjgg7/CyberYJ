Page({
    data: {
        showDisclaimer: false
    },

    onLoad() {
        this.checkDisclaimer();
    },

    checkDisclaimer() {
        const hasAccepted = wx.getStorageSync('hasAcceptedDisclaimer');
        if (!hasAccepted) {
            this.setData({ showDisclaimer: true });
        }
    },

    acceptDisclaimer() {
        this.setData({ showDisclaimer: false });
        wx.setStorageSync('hasAcceptedDisclaimer', true);
    },

    startDivination() {
        // Double check just in case, or allow anyway if modal is closed
        if (this.data.showDisclaimer) return;

        wx.navigateTo({
            url: '/pages/scene-select/scene-select'
        });
    }
})
