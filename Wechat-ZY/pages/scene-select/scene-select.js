const app = getApp();
const { getAllScenes } = require('../../utils/scenes.js');

Page({
    data: {
        scenes: getAllScenes(), // Ensure it's an array for .find() and wx:for order
        selectedScene: 'career', // Default selection
        selectedIndex: 0,        // Index 0 is Career
        question: '',
        showQuestionInput: true, // Always show standard input below/overlay
        quickQuestions: [],

        // Bagua Wheel Data
        wheelAngle: 0,           // Current rotation of the wheel
        isDragging: false,

        // Touch tracking
        lastX: 0,
        lastY: 0,
        centerX: 0,
        centerY: 0
    },

    onLoad() {
        this.updateQuickQuestions(this.data.selectedScene);
        this.calculateCenter();
    },

    onShow() {
        // Reset or refresh if needed
    },

    // Calculate center of the wheel for angle math
    calculateCenter() {
        const query = wx.createSelectorQuery();
        query.select('.bagua-wheel').boundingClientRect(rect => {
            if (rect) {
                this.setData({
                    centerX: rect.left + rect.width / 2,
                    centerY: rect.top + rect.height / 2
                });
            }
        }).exec();
    },

    // --- Touch Interaction ---
    onWheelTouchStart(e) {
        this.setData({ isDragging: true });
        const touch = e.touches[0];

        // Stop any existing inertia
        if (this._inertiaInterval) {
            clearInterval(this._inertiaInterval);
            this._inertiaInterval = null;
        }

        this.setData({
            lastX: touch.clientX,
            lastY: touch.clientY
        });

        // Track velocity
        this._lastMoveTime = Date.now();
        this._lastMoveAngle = this.data.wheelAngle;
        this._velocity = 0;
    },

    onWheelTouchMove(e) {
        if (!this.data.isDragging) return;
        const touch = e.touches[0];
        const { centerX, centerY, lastX, lastY, wheelAngle } = this.data;

        // Calculate angle change
        const startAngle = Math.atan2(lastY - centerY, lastX - centerX);
        const endAngle = Math.atan2(touch.clientY - centerY, touch.clientX - centerX);

        let delta = (endAngle - startAngle) * (180 / Math.PI);

        // Track velocity for inertia
        const now = Date.now();
        const dt = now - this._lastMoveTime;
        if (dt > 0) {
            this._velocity = delta / dt; // degrees per ms
            this._lastMoveTime = now;
        }

        let newAngle = wheelAngle + delta;
        this.setData({
            wheelAngle: newAngle,
            lastX: touch.clientX,
            lastY: touch.clientY
        });

        // Haptic Feedback while dragging (Tick effect)
        // Check if we crossed a 60-degree boundary
        this.checkHapticRhythm(newAngle, wheelAngle);
    },

    onWheelTouchEnd(e) {
        this.setData({ isDragging: false });

        // Apply Inertia
        if (Math.abs(this._velocity) > 0.1) {
            this.applyInertia();
        } else {
            this.snapToNearest();
        }
    },

    applyInertia() {
        let { wheelAngle } = this.data;
        let velocity = this._velocity * 16; // Convert to deg per frame (approx 60fps)
        const friction = 0.95; // Decay factor

        this._inertiaInterval = setInterval(() => {
            velocity *= friction;
            wheelAngle += velocity;

            this.setData({ wheelAngle });
            // this.checkHapticRhythm(wheelAngle, wheelAngle - velocity); // Optional: Haptic during inertia

            // Stop when slow enough
            if (Math.abs(velocity) < 0.5) {
                clearInterval(this._inertiaInterval);
                this._inertiaInterval = null;
                this.snapToNearest();
            }
        }, 16);
    },

    checkHapticRhythm(newAngle, oldAngle) {
        // Trigger haptic every 60 degrees (passing a sector)
        // Normalize to positive
        const step = 60;
        const oldSector = Math.floor(oldAngle / step);
        const newSector = Math.floor(newAngle / step);

        if (oldSector !== newSector) {
            wx.vibrateShort({ type: 'light' });
        }
    },

    // Snap to the nearest 60-degree increment
    snapToNearest() {
        // Stop any inertia if invoked directly (e.g. tap)
        if (this._inertiaInterval) {
            clearInterval(this._inertiaInterval);
            this._inertiaInterval = null;
        }

        const { wheelAngle } = this.data;
        const step = 60;

        let targetAngle = Math.round(wheelAngle / step) * step;

        this.setData({
            wheelAngle: targetAngle
        });

        this.updateSelectionFromAngle(targetAngle);
    },

    updateSelectionFromAngle(angle) {
        // Math to find which index is at Top (0 deg visual)
        // Normalized angle relative to 0
        // angle = k * 60.
        // If angle = 0, index = 0.
        // If angle = 60, wheel rotated CW 60 deg. Item 0 is at 60 deg. Item 5 (300 deg) is at 0 deg.
        // So Index = (0 - (angle/60)) % 6

        let steps = Math.round(angle / 60);
        // JS modulo of negative numbers is weird. ((a % n) + n) % n
        let index = ((0 - steps) % 6 + 6) % 6;

        if (this.data.selectedIndex !== index) {
            // Haptic feedback on change
            wx.vibrateShort({ type: 'light' });

            const selectedScene = this.data.scenes[index];
            this.setData({
                selectedIndex: index,
                selectedScene: selectedScene.id
            });
            this.updateQuickQuestions(selectedScene.id);
        }
    },

    // Direct tap on an item
    onItemTap(e) {
        const index = e.currentTarget.dataset.index;
        // We want to rotate this index to Top (0 deg effective)
        // Current Index is selectedIndex.
        // Target is index.
        // Diff = index - selectedIndex.
        // If selected is 0, target is 1. We need to rotate -60 deg (CCW) to bring 1 to Top.
        // So deltaAngle = - (index - selectedIndex) * 60 ?? 
        // Wait, simpler: Target Angle => specific angle where index is at Top.

        // We know: index = (-steps) % 6.
        // So steps = -index (mod 6).
        // But we want nearest rotation.

        // Let's just calculate the shortest path.
        // Current Step position: currentSteps = Math.round(wheelAngle / 60)
        // Current Virtual Index derived from currentSteps.
        // Target Index `index`.
        // diff = index - currentIndex.
        // If diff is +1 (e.g. 0 -> 1), we need to rotate -60.
        // So angleChange = -diff * 60.

        // Handle wrap around for shortest path (e.g. 0 to 5 should be +1 * 60, not -5 * 60)

        let { selectedIndex, wheelAngle } = this.data;
        let diff = index - selectedIndex;

        // Shortest path logic
        if (diff > 3) diff -= 6;
        if (diff < -3) diff += 6;

        let targetAngle = wheelAngle + (-diff * 60);

        this.setData({
            wheelAngle: targetAngle,
            selectedIndex: index,
            selectedScene: this.data.scenes[index].id
        });
        this.updateQuickQuestions(this.data.scenes[index].id);
    },

    updateQuickQuestions(sceneId) {
        if (!this.data.scenes) return;
        const scene = this.data.scenes.find(s => s.id === sceneId);
        if (scene) {
            this.setData({
                quickQuestions: scene.quickQuestions || []
            });
        }
    },

    onQuestionInput(e) {
        this.setData({ question: e.detail.value });
    },

    fillQuestion(e) {
        const q = e.currentTarget.dataset.question;
        this.setData({ question: q });
    },

    startDivination() {
        const { selectedScene, question } = this.data;
        wx.navigateTo({
            url: `/pages/divination/divination?scene=${selectedScene}&question=${question}`
        });
    }
});
