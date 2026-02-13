/**
 * API Service
 * 真实后端优先，网络失败时回退 Mock 数据，保证小程序可用性。
 * @module services/api
 */

/**
 * 解释六爻卦象
 * @param {number[]} coins - 长度为 6 的数组，元素为 6, 7, 8, 9
 * @param {string} question - 用户问题
 * @param {string} sceneType - 场景类型（fortune/career/love/wealth/health/study/family/travel/lawsuit）
 * @returns {Promise<object>} - 解析结果
 */
const { config } = require('../config/env.js');
const API_BASE_URL = config.baseUrl;
const API_KEY = config.apiKey || 'cyberyj-dev-key';
const USE_MOCK = config.useMock;

const normalizeResponse = (payload) => {
    // 兼容两种后端返回：
    // 1) 业务直出：{ hexagram, analysis, ... }
    // 2) 包装协议：{ tool, data, meta }
    if (payload && typeof payload === 'object' && payload.data && (payload.tool || payload.meta)) {
        return payload.data;
    }
    return payload;
};

const interpretHexagram = (coins, question, sceneType = 'fortune') => {
    return new Promise((resolve, reject) => {
        // Mock Mode check
        if (USE_MOCK) {
            console.log('[Mock API] Interpret:', { coins, question, sceneType });
            setTimeout(() => {
                const mockResponse = getMockResponse(coins, sceneType);
                resolve(mockResponse);
            }, 1000);
            return;
        }

        // Real API Call
        wx.request({
            url: `${API_BASE_URL}/v1/divination/interpret`,
            method: 'POST',
            timeout: 10000,
            header: {
                'Content-Type': 'application/json',
                'X-API-Key': API_KEY
            },
            data: {
                coins,
                question,
                scene_type: sceneType // explicit scene type
            },
            success: (res) => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    console.log('API Response (Real):', res.data);
                    resolve(normalizeResponse(res.data));
                } else {
                    console.error('API Error (HTTP):', res);
                    // Fallback to Mock if 500 or 404 (optional, depending on preference)
                    // For now, reject to show error UI
                    reject(res.data?.error || { code: 'HTTP_ERROR', message: `status=${res.statusCode}` });
                }
            },
            fail: (err) => {
                console.warn('API Network Error (Fallback to Mock):', err);

                // Fallback to Mock Data (Simulated)
                // This ensures app works even if backend is not running
                const mockResponse = getMockResponse(coins, sceneType);
                resolve(mockResponse);

                // Or reject if you prefer strict mode:
                // reject({ code: 'NETWORK_ERROR', message: err.errMsg });
            }
        });
    });
};

// Mock Response Helper (Moved from original function)
const getMockResponse = (coins, sceneType = 'fortune') => {
    return {
        hexagram: {
            code: "101010",
            name: "未济 (Mock Fallback)",
            symbol: "䷿",
            judgment: "未济：亨，小狐汔济，濡其尾，无攸利。",
            image: "火在水上，未济；君子以慎辨物居方。",
            upper_trigram: "离",
            lower_trigram: "坎"
        },
        changing_hexagram: {
            code: "111111",
            name: "乾",
            symbol: "䷀",
            judgment: "乾：元亨利贞。",
            image: "天行健，君子以自强不息。",
            interpretation: "【变卦】乾卦象征刚健不息，充满活力。表示目前正处于上升期，应积极进取。"
        },
        analysis: {
            overall: "【注意：后端服务未连接，显示模拟数据】未济卦象征事未成，但这也意味着无限的可能性。此时不宜急进，需审慎行事，等待时机成熟。",
            active_lines: ["初六：濡其尾，吝。", "九四：贞吉，悔亡，震用伐鬼方，三年有赏于大国。"],
            five_elements: "本卦属火，变卦属金。火克金，需注意...",
            solar_term: "当前节气立春，万物复苏，此卦象显示生机勃勃...",
            advice: "宜：筹备规划，蓄势待发。\n忌：轻举妄动，涉水过河。"
        },
        do_dont: {
            do: ["制定长远计划", "韬光养晦", "结交益友"],
            dont: ["即刻行动", "强行推进", "与人争执"]
        },
        scene_type: sceneType,
        score: 75,
        keywords: ["时机未到", "潜龙勿用", "蓄势待发"],
        advice_tags: ["守势", "规划", "防风险"],
        consistency: {
            status: "pass",
            tone: "guard",
            adjustments: []
        }
    };
};

module.exports = {
    interpretHexagram
};
