/**
 * 学习主题配置
 * 主题 ID 复用后端现有枚举，前端统一以“国学学习”表达展示。
 */

const SCENES = {
    career: {
        id: 'career',
        name: '结构入门',
        icon: 'career',
        defaultQuestion: '这组卦象的结构特点是什么？',
        quickQuestions: ['上下卦如何组合？', '这一卦适合先看哪部分？', '新手如何快速读懂卦象结构？']
    },
    love: {
        id: 'love',
        name: '卦辞精读',
        icon: 'love',
        defaultQuestion: '请解释卦辞中的关键句。',
        quickQuestions: ['卦辞重点词有哪些？', '可以给出白话解释吗？', '有哪些常见误读？']
    },
    wealth: {
        id: 'wealth',
        name: '象辞研读',
        icon: 'wealth',
        defaultQuestion: '请解释象辞与卦象关系。',
        quickQuestions: ['象辞在说什么图景？', '如何从象辞理解经典语境？', '有哪些关联阅读建议？']
    },
    health: {
        id: 'health',
        name: '爻位理解',
        icon: 'health',
        defaultQuestion: '请说明六爻位置的基础含义。',
        quickQuestions: ['初爻到上爻如何理解？', '动爻在学习中怎么读？', '有没有简化记忆方法？']
    },
    study: {
        id: 'study',
        name: '五行基础',
        icon: 'study',
        defaultQuestion: '请从五行角度做基础讲解。',
        quickQuestions: ['五行关系如何入门？', '如何避免过度解读？', '推荐哪些经典入门材料？']
    },
    fortune: {
        id: 'fortune',
        name: '综合学习',
        icon: 'other',
        defaultQuestion: '请给我一份这卦的学习提纲。',
        quickQuestions: ['先看卦辞还是象辞？', '如何建立系统学习路径？', '请给出复习要点。']
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
