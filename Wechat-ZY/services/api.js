/**
 * API Service
 * 优先调用后端接口，失败时回退本地示例数据，保证学习流程可用。
 * @module services/api
 */

/**
 * 解析六爻数据并生成学习解读
 * @param {number[]} coins - 长度为 6 的数组，元素为 6, 7, 8, 9
 * @param {string} question - 用户输入问题
 * @param {string} sceneType - 主题类型（fortune/career/love/wealth/health/study/family/travel/lawsuit）
 * @returns {Promise<object>} - 学习解读结果
 */
const { config } = require('../config/env.js');

const API_BASE_URL = config.baseUrl;
const API_KEY = config.apiKey || 'cyberyj-dev-key';
const USE_MOCK = config.useMock;
const API_PATHS = ['/v1/learning/interpret', '/v1/divination/interpret'];

const TOPIC_NAME = {
    fortune: '综合学习',
    career: '结构入门',
    love: '卦辞精读',
    wealth: '象辞研读',
    health: '爻位理解',
    study: '五行基础',
    family: '家庭主题',
    travel: '出行主题',
    lawsuit: '规则主题'
};

const sanitizeText = (value) => {
    let text = String(value || '').trim();
    const replacements = [
        ['\u8d8b\u5409\u907f\u51f6', '学习建议'],
        ['\u8fd0\u52bf', '主题'],
        ['\u5409\u51f6', '内容'],
        ['\u535c\u5366', '学习'],
        ['\u5360\u535c', '学习']
    ];
    replacements.forEach(([from, to]) => {
        text = text.split(from).join(to);
    });
    return text;
};

const normalizeResponse = (payload) => {
    // 兼容两种后端返回：
    // 1) 业务直出：{ hexagram, analysis, ... }
    // 2) 包装协议：{ tool, data, meta }
    if (payload && typeof payload === 'object' && payload.data && (payload.tool || payload.meta)) {
        return payload.data;
    }
    return payload;
};

const toLearningPayload = (payload, sceneType = 'fortune') => {
    const raw = normalizeResponse(payload) || {};
    const hexagram = raw.hexagram || {};
    const analysis = raw.analysis || {};
    const activeLines = Array.isArray(analysis.active_lines)
        ? analysis.active_lines.map((line) => sanitizeText(line))
        : [];

    const keywords = Array.isArray(raw.keywords)
        ? raw.keywords.map((item) => sanitizeText(item)).filter(Boolean)
        : [];

    return {
        hexagram: {
            code: hexagram.code || '000000',
            name: sanitizeText(hexagram.name || '未命名'),
            symbol: hexagram.symbol || '䷿',
            judgment: sanitizeText(hexagram.judgment || '无卦辞数据。'),
            image: sanitizeText(hexagram.image || '无象辞数据。'),
            upper_trigram: sanitizeText(hexagram.upper_trigram || '-'),
            lower_trigram: sanitizeText(hexagram.lower_trigram || '-')
        },
        changing_hexagram: raw.changing_hexagram
            ? {
                code: raw.changing_hexagram.code || '000000',
                name: sanitizeText(raw.changing_hexagram.name || '未命名'),
                symbol: raw.changing_hexagram.symbol || '䷿',
                judgment: sanitizeText(raw.changing_hexagram.judgment || ''),
                image: sanitizeText(raw.changing_hexagram.image || '')
            }
            : null,
        scene_type: sceneType,
        analysis: {
            overall: `当前主题：${TOPIC_NAME[sceneType] || TOPIC_NAME.fortune}。本页面用于《周易》经典学习，展示卦象结构、卦辞与象辞基础释义。`,
            active_lines: activeLines,
            five_elements: sanitizeText(analysis.five_elements || '可结合五行基础概念理解卦象符号关系。'),
            solar_term: sanitizeText(analysis.solar_term || '可结合节气背景理解传统文本语境。'),
            advice: '建议结合经典原文与注释资料进行学习记录，不作为现实决策依据。'
        },
        keywords: keywords.length ? keywords : ['卦象结构', '经典文本', '术语入门'],
        topic_tags: [TOPIC_NAME[sceneType] || TOPIC_NAME.fortune, '国学学习', '经典研读']
    };
};

const buildMockPayload = (sceneType = 'fortune') => ({
    hexagram: {
        code: '101010',
        name: '未济',
        symbol: '䷿',
        judgment: '未济：亨，小狐汔济，濡其尾，无攸利。',
        image: '火在水上，未济；君子以慎辨物居方。',
        upper_trigram: '离',
        lower_trigram: '坎'
    },
    changing_hexagram: {
        code: '111111',
        name: '乾',
        symbol: '䷀',
        judgment: '乾：元亨利贞。',
        image: '天行健，君子以自强不息。'
    },
    analysis: {
        active_lines: ['初六：濡其尾，吝。', '九四：贞吉，悔亡。'],
        five_elements: '可从五行关系切入，先理解“生克”与“平衡”的基础概念。',
        solar_term: '可结合当前节气学习古人对时令与自然节奏的观察。'
    },
    keywords: ['文本学习', '基础释义', '结构观察'],
    scene_type: sceneType
});

const interpretHexagram = (coins, question, sceneType = 'fortune') => (
    new Promise((resolve, reject) => {
        if (USE_MOCK) {
            console.log('[Mock API] Interpret:', { coins, question, sceneType });
            setTimeout(() => {
                resolve(toLearningPayload(buildMockPayload(sceneType), sceneType));
            }, 300);
            return;
        }

        const requestByIndex = (idx) => {
            const path = API_PATHS[idx];
            wx.request({
                url: `${API_BASE_URL}${path}`,
                method: 'POST',
                timeout: 10000,
                header: {
                    'Content-Type': 'application/json',
                    'X-API-Key': API_KEY
                },
                data: {
                    coins,
                    question,
                    scene_type: sceneType
                },
                success: (res) => {
                    if (res.statusCode >= 200 && res.statusCode < 300) {
                        resolve(toLearningPayload(res.data, sceneType));
                        return;
                    }
                    if (res.statusCode === 404 && idx + 1 < API_PATHS.length) {
                        requestByIndex(idx + 1);
                        return;
                    }
                    reject(res.data?.error || { code: 'HTTP_ERROR', message: `status=${res.statusCode}` });
                },
                fail: (err) => {
                    if (idx + 1 < API_PATHS.length) {
                        requestByIndex(idx + 1);
                        return;
                    }
                    console.warn('API Network Error (Fallback to Mock):', err);
                    resolve(toLearningPayload(buildMockPayload(sceneType), sceneType));
                }
            });
        };

        requestByIndex(0);
    })
);

module.exports = {
    interpretHexagram
};
