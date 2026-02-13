const { generateSixLines } = require('../utils/divination.js');

console.log('Running Divination Logic Tests...');

let passed = true;

// Test 1: Generate 100 times, check validity
for (let i = 0; i < 100; i++) {
    const lines = generateSixLines();

    // Check Length
    if (lines.length !== 6) {
        console.error(`FAIL: Length is ${lines.length}, expected 6`);
        passed = false;
        break;
    }

    // Check Values (must be 6, 7, 8, 9)
    const validValues = [6, 7, 8, 9];
    if (!lines.every(l => validValues.includes(l))) {
        console.error('FAIL: Invalid values found', lines);
        passed = false;
        break;
    }
}

if (passed) {
    console.log('PASS: Generated 100 valid hexagrams.');
    console.log('Sample Output:', generateSixLines());
} else {
    console.error('FAIL: Test failed.');
    process.exit(1);
}
