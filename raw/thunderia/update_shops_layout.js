const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

files.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // 1. Update title format to clean compact style if needed
    // e.g. "&0&l| &0Tienda ▶ &8Bloques " -> "&0&l|&r &0ThunderMC &0▶ &8Bloques"
    content = content.replace(/name:\s*["']&0&l\| &0Tienda ▶ &8([^"']+)["']/g, (match, p1) => {
        return `name: "&0&l|&r &0ThunderMC &0▶ &8${p1.trim()}"`;
    });
    
    // 2. Ensure buttons section is at 48, 49, 50
    const buttonsRegex = /buttons:\s*\r?\n\s*goBack:\s*\r?\n\s*slot:\s*\d+\r?\n\s*previousPage:\s*\r?\n\s*slot:\s*\d+\r?\n\s*nextPage:\s*\r?\n\s*slot:\s*\d+/g;
    
    const newButtons = `buttons:
    goBack:
      slot: 49
    previousPage:
      slot: 48
    nextPage:
      slot: 50`;
      
    if (content.match(buttonsRegex)) {
        content = content.replace(buttonsRegex, newButtons);
    }
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Updated shop file layout:', file);
});
