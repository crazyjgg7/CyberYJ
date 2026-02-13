/* components/music-control.js */
const app = getApp();

Component({
    properties: {},
    data: {
        isPlaying: false
    },
    lifetimes: {
        attached() {
            // Register callback to sync state
            if (app.registerMusicCallback) {
                app.registerMusicCallback((isPlaying) => {
                    this.setData({ isPlaying });
                });
            } else {
                // Fallback check
                this.setData({
                    isPlaying: app.globalData.isMusicPlaying
                });
            }
        }
    },

    pageLifetimes: {
        show() {
            // Double check state on show
            if (app.globalData) {
                this.setData({
                    isPlaying: app.globalData.isMusicPlaying
                });
            }
        }
    },

    methods: {
        toggleMusic() {
            if (this.data.isPlaying) {
                app.pauseMusic();
                this.setData({ isPlaying: false }); // Optimistic update
            } else {
                app.playMusic();
                this.setData({ isPlaying: true }); // Optimistic update
            }
        }
    }
});
