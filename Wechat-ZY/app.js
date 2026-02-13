App({
  onLaunch() {
    this.initMusic();
  },

  globalData: {
    userInfo: null,
    bgmManager: null, // InnerAudioContext instance
    isMusicPlaying: false,
    updateMusicState: null // Callback for components
  },

  initMusic() {
    // Check if manager already exists
    if (this.globalData.bgmManager) return;

    const innerAudioContext = wx.createInnerAudioContext();
    innerAudioContext.autoplay = true;
    innerAudioContext.loop = true; // Auto loop
    innerAudioContext.src = '/audio/bgm.mp3';
    innerAudioContext.volume = 0.5; // Set volume

    // Event Listeners
    innerAudioContext.onPlay(() => {
      console.log('BGM Started');
      this.globalData.isMusicPlaying = true;
      if (this.globalData.updateMusicState) {
        this.globalData.updateMusicState(true);
      }
    });

    innerAudioContext.onPause(() => {
      console.log('BGM Paused');
      this.globalData.isMusicPlaying = false;
      if (this.globalData.updateMusicState) {
        this.globalData.updateMusicState(false);
      }
    });

    innerAudioContext.onStop(() => {
      console.log('BGM Stopped');
      this.globalData.isMusicPlaying = false;
      if (this.globalData.updateMusicState) {
        this.globalData.updateMusicState(false);
      }
    });

    innerAudioContext.onError((res) => {
      console.error('BGM Error:', res.errMsg);
      // Retry or handle error
    });

    this.globalData.bgmManager = innerAudioContext;
  },

  // Public API for components
  playMusic() {
    const manager = this.globalData.bgmManager;
    if (manager) {
      if (manager.paused) {
        manager.play();
      }
    } else {
      this.initMusic(); // Re-init if missing
    }
  },

  pauseMusic() {
    const manager = this.globalData.bgmManager;
    if (manager) {
      manager.pause();
    }
  },

  // Helper to register callback
  registerMusicCallback(callback) {
    this.globalData.updateMusicState = callback;
    // Immediately valid state
    callback(this.globalData.isMusicPlaying);
  }
})
