const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

let allSellItems = [];

files.forEach(file => {
    const category = file.replace('.yml', '');
    const content = fs.readFileSync(path.join(shopsDir, file), 'utf8');
    const lines = content.split('\n');
    let mat = '', name = '', buy = -1, sell = -1;
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let matMatch = line.match(/^\s+material:\s*([A-Z0-9_]+)/);
        if (matMatch) mat = matMatch[1].trim();
        
        let nameMatch = line.match(/^\s+name:\s*(.+)$/);
        if (nameMatch) name = nameMatch[1].trim();
        
        let buyMatch = line.match(/^\s+buyPrice:\s*([0-9.-]+)/);
        if (buyMatch) buy = parseFloat(buyMatch[1]);
        
        let sellMatch = line.match(/^\s+sellPrice:\s*([0-9.-]+)/);
        if (sellMatch) {
            sell = parseFloat(sellMatch[1]);
            if (sell > 0) {
                allSellItems.push({ category, material: mat, name, buy, sell });
            }
            mat = ''; name = ''; buy = -1; sell = -1;
        }
    }
});

console.log('Total sellable items found:', allSellItems.length);
const catCounts = {};
allSellItems.forEach(item => {
    catCounts[item.category] = (catCounts[item.category] || 0) + 1;
});
console.log('Counts per category:', JSON.stringify(catCounts, null, 2));
fs.writeFileSync('raw/thunderia/sell_items.json', JSON.stringify(allSellItems, null, 2));
