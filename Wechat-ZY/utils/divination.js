/**
 * 六爻生成工具 (Divination Utility)
 * 
 * Coins Protocol:
 * - Front (Word/Yin) = 2
 * - Back (Flower/Yang) = 3
 * 
 * Logic:
 * - 3 Backs (Yang) = 9 (Old Yang, Changing)
 * - 3 Fronts (Yin) = 6 (Old Yin, Changing)
 * - 1 Back, 2 Fronts = 7 (Shao Yang, Static Yang)
 * - 2 Backs, 1 Front = 8 (Shao Yin, Static Yin)
 */

/**
 * Generate a single line result
 * @returns {object} { value: number, coins: number[] }
 */
const generateLine = () => {
    const coin1 = Math.random() < 0.5 ? 2 : 3;
    const coin2 = Math.random() < 0.5 ? 2 : 3;
    const coin3 = Math.random() < 0.5 ? 2 : 3;

    return {
        value: coin1 + coin2 + coin3,
        coins: [coin1, coin2, coin3]
    };
};

/**
 * Generate 6 lines for a full hexagram
 * @returns {object[]} Array of line objects
 */
const generateSixLines = () => {
    const lines = [];
    for (let i = 0; i < 6; i++) {
        lines.push(generateLine());
    }
    return lines;
};

module.exports = {
    generateSixLines,
    generateLine
};
