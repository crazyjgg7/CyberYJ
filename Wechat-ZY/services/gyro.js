/**
 * Gyroscope Service
 * Encapsulates wx.startGyroscope for shake detection.
 * Provides onShake and onSettle callbacks.
 */

class GyroService {
    constructor() {
        this.isListening = false;
        this.isShaking = false;
        this.callbacks = {
            shake: [],
            settle: []
        };
        this.settleTimer = null;
        this.threshold = 1.5; // rad/s (Lowered from 3.0 for better sensitivity)
        this.settleThreshold = 1.0; // rad/s (Relaxed from 0.5)
        this.settleTime = 500; // ms

        // Bind in constructor so we can effectively unbind
        this._handleGyroChange = this.handleGyroChange.bind(this);
    }

    isSupported() {
        return wx.canIUse('onGyroscopeChange');
    }

    start() {
        return new Promise((resolve, reject) => {
            if (this.isListening) {
                resolve();
                return;
            }

            // Check support
            if (!this.isSupported()) {
                console.warn('Gyroscope API not supported');
                reject(new Error('Device not supported'));
                return;
            }

            wx.startGyroscope({
                interval: 'game',
                success: () => {
                    this.isListening = true;
                    wx.onGyroscopeChange(this._handleGyroChange);
                    console.log('GyroService started');
                    resolve();
                },
                fail: (err) => {
                    console.error('Failed to start gyro:', err);
                    reject(err);
                }
            });
        });
    }

    stop() {
        if (!this.isListening) return;

        // Remove listener
        wx.offGyroscopeChange(this._handleGyroChange);
        wx.stopGyroscope();

        this.isListening = false;
        this.isShaking = false;

        if (this.settleTimer) {
            clearTimeout(this.settleTimer);
            this.settleTimer = null;
        }

        console.log('GyroService stopped');
    }

    onShake(cb) {
        if (typeof cb === 'function') {
            this.callbacks.shake.push(cb);
        }
    }

    onSettle(cb) {
        if (typeof cb === 'function') {
            this.callbacks.settle.push(cb);
        }
    }

    handleGyroChange(res) {
        // res: {x, y, z} rad/s
        const magnitude = Math.sqrt(res.x ** 2 + res.y ** 2 + res.z ** 2);

        if (magnitude > this.threshold) {
            // START SHAKING
            if (!this.isShaking) {
                this.isShaking = true;
                this.emit('shake');
            }

            // Reset settle timer if currently shaking strongly
            if (this.settleTimer) {
                clearTimeout(this.settleTimer);
                this.settleTimer = null;
            }
        } else if (magnitude < this.settleThreshold) {
            // MAYBE SETTLING
            if (this.isShaking) {
                if (!this.settleTimer) {
                    // Start settle timer
                    this.settleTimer = setTimeout(() => {
                        // CONFIRMED SETTLED
                        this.isShaking = false;
                        this.emit('settle');
                        this.settleTimer = null;
                    }, this.settleTime);
                }
            }
        }
    }

    emit(event, data) {
        const list = this.callbacks[event] || [];
        list.forEach(cb => {
            try {
                cb(data);
            } catch (e) {
                console.error(`Error in GyroService ${event} callback:`, e);
            }
        });
    }
}

// Export singleton instance
module.exports = new GyroService();
