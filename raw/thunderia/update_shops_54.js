const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

files.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Set size: 54
    content = content.replace(/size:\s*\d+/g, 'size: 54');
    
    // Set fillItem to AIR
    content = content.replace(/fillItem:\s*\r?\n\s*material:\s*[A-Z_]+\s*\r?\n\s*name:\s*["'][^"']*["']/g, 
        'fillItem:\n    material: AIR\n    name: " "');
    
    // Update buttons to row 6 (48, 49, 50)
    const newButtons = `buttons:
    goBack:
      slot: 49
    previousPage:
      slot: 48
    nextPage:
      slot: 50`;
    
    content = content.replace(/buttons:\s*\r?\n\s*goBack:\s*\r?\n\s*slot:\s*\d+\r?\n\s*previousPage:\s*\r?\n\s*slot:\s*\d+\r?\n\s*nextPage:\s*\r?\n\s*slot:\s*\d+/g, newButtons);
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Processed shop file to 54 slots & AIR fillItem:', file);
});
