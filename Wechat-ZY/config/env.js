/**
 * 环境配置文件
 * 切换环境时修改 currentEnv 即可
 */

const ENV = {
    dev: {
        baseUrl: 'http://127.0.0.1:18080',
        apiKey: 'cyberyj-dev-key',
        useMock: false,
        mockFallbackOnError: true,
        timeoutMs: 7000,
        apiPaths: ['/v1/divination/interpret'],
        debug: true
    },
    prod: {
        // Replace with your actual production domain (Must be HTTPS)
        baseUrl: 'https://youtang.128228.xyz',
        apiKey: 'cyberyj-dev-key',
        useMock: false,
        mockFallbackOnError: false,
        timeoutMs: 7000,
        apiPaths: ['/v1/divination/interpret'],
        debug: false
    }
};

const currentEnv = 'prod'; // 'dev' or 'prod'

const config = ENV[currentEnv];

module.exports = {
    config,
    currentEnv
};
