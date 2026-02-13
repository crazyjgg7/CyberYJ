/* Storage Service for History Persistence */

const KEY_HISTORY = 'divination_history';
const MAX_HISTORY = 50;

/**
 * Save a divination record
 * @param {object} record - The divination result object
 * @returns {boolean} success
 */
const saveHistory = (record) => {
    try {
        const history = wx.getStorageSync(KEY_HISTORY) || [];

        // Ensure record has ID and Timestamp
        if (!record.id) {
            record.id = Date.now().toString();
        }
        if (!record.timestamp) {
            record.timestamp = Date.now();
        }

        // Add new record to front
        history.unshift(record);

        // Limit size
        if (history.length > MAX_HISTORY) {
            history.pop(); // Remove oldest
        }

        wx.setStorageSync(KEY_HISTORY, history);
        return true;
    } catch (e) {
        console.error('Save history failed:', e);
        return false;
    }
};

/**
 * Get all history records
 * @returns {Array} history list
 */
const getHistory = () => {
    try {
        return wx.getStorageSync(KEY_HISTORY) || [];
    } catch (e) {
        console.error('Get history failed:', e);
        return [];
    }
};

/**
 * Get specific record by ID
 * @param {string} id 
 * @returns {object|undefined}
 */
const getHistoryById = (id) => {
    const list = getHistory();
    return list.find(item => item.id === id);
};

/**
 * Clear all history
 */
const clearHistory = () => {
    try {
        wx.removeStorageSync(KEY_HISTORY);
    } catch (e) {
        console.error('Clear history failed:', e);
    }
};

module.exports = {
    saveHistory,
    getHistory,
    getHistoryById,
    clearHistory
};
