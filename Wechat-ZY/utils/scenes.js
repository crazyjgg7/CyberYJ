/**
 * 场景配置文件
 * 定义六爻占卜的各个场景
 * Backend Spec: fortune, career, love, wealth, health, study
 */

const SCENES = {
    career: {
        id: 'career',
        name: '问事业',
        icon: 'briefcase',
        defaultQuestion: '我的事业运势如何？',
        quickQuestions: ['近期能否升职加薪？', '是否适合跳槽？', '创业机会如何？']
    },
    love: {
        id: 'love',
        name: '问感情',
        icon: 'heart',
        defaultQuestion: '我的感情运势如何？',
        quickQuestions: ['我和TA会有结果吗？', '近期有桃花运吗？', '如何挽回这段感情？']
    },
    wealth: {
        id: 'wealth',
        name: '问财运',
        icon: 'coins',
        defaultQuestion: '我的财运如何？',
        quickQuestions: ['近期财运走势？', '这个投资项目靠谱吗？', '如何提升偏财运？']
    },
    health: {
        id: 'health',
        name: '问健康',
        icon: 'heart-pulse',
        defaultQuestion: '我的健康状况如何？',
        quickQuestions: ['近期身体状况如何？', '如何调理身体？', '家人的健康运势？']
    },
    study: {
        id: 'study',
        name: '问学业',
        icon: 'book',
        defaultQuestion: '我的学业运势如何？',
        quickQuestions: ['这次考试能过吗？', '适合考研还是工作？', '留学申请顺利吗？']
    },
    // Map 'other' -> 'fortune' (Backend Requirement)
    fortune: {
        id: 'fortune',
        name: '综合运势', // Was '其他'
        icon: 'ellipsis',
        defaultQuestion: '近期运势如何？',
        quickQuestions: ['最近运气怎么样？', '这件事能成吗？', '未来三个月运势？']
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
    return scene ? scene.defaultQuestion : '此事发展如何？';
}

module.exports = {
    SCENES,
    getAllScenes,
    getSceneById,
    getDefaultQuestion
};
