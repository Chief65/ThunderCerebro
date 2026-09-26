const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

files.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Fix fillItem name to " "
    content = content.replace(/fillItem:\s*\r?\n\s*material:\s*[A-Z_]+\s*\r?\n\s*name:\s*["'][^"']*["']/g, 
        'fillItem:\n    material: AIR\n    name: " "');
        
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Fixed fillItem in:', file);
});
