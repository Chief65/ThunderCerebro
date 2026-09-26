const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const filesToDisable = ['bloques.yml', 'comida.yml', 'miscellaneo.yml', 'redstone.yml', 'equipo.yml'];

filesToDisable.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Replace all sellPrice: <number> with sellPrice: -1
    // but keep buyPrice intact
    const modified = content.replace(/(\s+sellPrice:\s*)([0-9]+(\.[0-9]+)?)/g, '$1-1');
    fs.writeFileSync(filePath, modified, 'utf8');
    console.log('Disabled sellPrice in:', file);
});
