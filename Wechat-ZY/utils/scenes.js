/**
 * 学习主题配置
 * 主题 ID 复用后端现有枚举，前端统一以“国学学习”表达展示。
 */

const SCENES = {
    career: {
        id: 'career',
        name: '职场主题',
        icon: 'career',
        defaultQuestion: '请从职场主题做学习解读。',
        quickQuestions: [
            '协作',
            '规划',
            '成长'
        ]
    },
    love: {
        id: 'love',
        name: '关系主题',
        icon: 'love',
        defaultQuestion: '请从关系主题做学习解读。',
        quickQuestions: [
            '沟通',
            '信任',
            '边界'
        ]
    },
    wealth: {
        id: 'wealth',
        name: '财务主题',
        icon: 'wealth',
        defaultQuestion: '请从财务主题做学习解读。',
        quickQuestions: [
            '预算',
            '风险',
            '取舍'
        ]
    },
    health: {
        id: 'health',
        name: '身心主题',
        icon: 'health',
        defaultQuestion: '请从身心主题做学习解读。',
        quickQuestions: [
            '作息',
            '压力',
            '恢复'
        ]
    },
    study: {
        id: 'study',
        name: '学习主题',
        icon: 'study',
        defaultQuestion: '请从学习主题做学习解读。',
        quickQuestions: [
            '入门',
            '术语',
            '复盘'
        ]
    },
    fortune: {
        id: 'fortune',
        name: '综合主题',
        icon: 'other',
        defaultQuestion: '请从综合主题做学习解读。',
        quickQuestions: [
            '框架',
            '重点',
            '误区'
        ]
    }
};

/**
 * 获取所有场景列表
 */
function getAllScenes() {
    return Object.values(SCENES);
}

/**
 * 根据场景 ID 获取场景信息
 * @param {string} sceneId - 场景 ID
 * @returns {object|null} 场景对象
 */
function getSceneById(sceneId) {
    return SCENES[sceneId] || null;
}

/**
 * 获取场景的默认问题
 * @param {string} sceneId - 场景 ID
 * @returns {string} 默认问题
 */
function getDefaultQuestion(sceneId) {
    const scene = getSceneById(sceneId);
    return scene ? scene.defaultQuestion : '请解释这组卦象的基础含义。';
}

module.exports = {
    SCENES,
    getAllScenes,
    getSceneById,
    getDefaultQuestion
};
