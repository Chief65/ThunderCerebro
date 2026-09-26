const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

files.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // 1. Set size: 45 (5 rows)
    content = content.replace(/size:\s*\d+/g, 'size: 45');
    
    // 2. Set buttons to row 5 (39, 40, 41)
    const newButtons = `buttons:
    goBack:
      slot: 40
    previousPage:
      slot: 39
    nextPage:
      slot: 41`;
    content = content.replace(/buttons:\s*\r?\n\s*goBack:\s*\r?\n\s*slot:\s*\d+\r?\n\s*previousPage:\s*\r?\n\s*slot:\s*\d+\r?\n\s*nextPage:\s*\r?\n\s*slot:\s*\d+/g, newButtons);
    
    // 3. Find max pages
    let maxPage = 1;
    const pageMatches = content.matchAll(/pages:\s*\r?\n\s*-\s*(\d+)/g);
    for (const m of pageMatches) {
        let p = parseInt(m[1]);
        if (p > maxPage) maxPage = p;
    }
    
    // 4. Remove all previous dummy entries
    content = content.replace(/\s+\d+:\s*\r?\n\s+type:\s*dummy[\s\S]*?(?=\s+\d+:|$)/g, '');
    
    // 5. Find max item id
    let maxId = 0;
    const idMatches = content.matchAll(/^\s+(\d+):/gm);
    for (const m of idMatches) {
        let id = parseInt(m[1]);
        if (id > maxId) maxId = id;
    }
    
    // 6. Generate top navbar (row 1: slots 0 to 8) and bottom navbar (row 5: slots 36,37,38, 42,43,44 + 39,41 if no arrow) for all pages
    let dummySection = '';
    const topSlots = [0, 1, 2, 3, 4, 5, 6, 7, 8];
    const bottomSlots = [36, 37, 38, 42, 43, 44];
    
    for (let page = 1; page <= maxPage; page++) {
        // Top glass panes (row 1)
        topSlots.forEach(slot => {
            maxId++;
            dummySection += `
    ${maxId}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: ${slot}
      pages:
        - ${page}`;
        });
        
        // Bottom glass panes (row 5 sides)
        bottomSlots.forEach(slot => {
            maxId++;
            dummySection += `
    ${maxId}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: ${slot}
      pages:
        - ${page}`;
        });
        
        // Fallback glass pane on slot 39 if page 1 (no previous page arrow)
        if (page === 1) {
            maxId++;
            dummySection += `
    ${maxId}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 39
      pages:
        - 1`;
        }
        
        // Fallback glass pane on slot 41 if last page (no next page arrow)
        if (page === maxPage) {
            maxId++;
            dummySection += `
    ${maxId}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 41
      pages:
        - ${page}`;
        }
    }
    
    content = content.trimEnd() + dummySection + '\n';
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated 5-row shop ${file} (max pages: ${maxPage})`);
});
