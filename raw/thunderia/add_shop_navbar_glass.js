const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

files.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Check if fillItem is defined, if so, remove it or ensure it does not conflict
    // Add dummy glass panes at slots 45, 46, 47, 51, 52, 53
    // First let us find the highest item id
    let maxId = 0;
    const idMatches = content.matchAll(/^\s+(\d+):/gm);
    for (const m of idMatches) {
        let id = parseInt(m[1]);
        if (id > maxId) maxId = id;
    }
    
    // Check if dummy items already exist
    if (!content.includes('material: GRAY_STAINED_GLASS_PANE')) {
        let dummyItems = `
    ${maxId + 1}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 45
    ${maxId + 2}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 46
    ${maxId + 3}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 47
    ${maxId + 4}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 51
    ${maxId + 5}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 52
    ${maxId + 6}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 53`;
        
        content = content.trimEnd() + dummyItems + '\n';
        fs.writeFileSync(filePath, content, 'utf8');
        console.log('Added navbar glass panes to shop:', file);
    }
});
