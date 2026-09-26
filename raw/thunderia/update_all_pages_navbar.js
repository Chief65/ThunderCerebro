const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const files = fs.readdirSync(shopsDir).filter(f => f.endsWith('.yml'));

files.forEach(file => {
    const filePath = path.join(shopsDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Find all pages mentioned in the file
    let maxPage = 1;
    const pageMatches = content.matchAll(/pages:\s*\r?\n\s*-\s*(\d+)/g);
    for (const m of pageMatches) {
        let p = parseInt(m[1]);
        if (p > maxPage) maxPage = p;
    }
    
    // Remove old dummy entries if any
    content = content.replace(/\s+\d+:\s*\r?\n\s+type:\s*dummy[\s\S]*?(?=\s+\d+:|$)/g, '');
    
    // Find the highest item index
    let maxId = 0;
    const idMatches = content.matchAll(/^\s+(\d+):/gm);
    for (const m of idMatches) {
        let id = parseInt(m[1]);
        if (id > maxId) maxId = id;
    }
    
    // Generate dummy glass panes for all pages for slots 45, 46, 47, 51, 52, 53
    // Also if maxPage === 1 (or on page 1 without previous, or last page without next),
    // we can add glass panes where arrows would be absent if desired, or let arrows handle it.
    let dummySection = '';
    const navbarSlots = [45, 46, 47, 51, 52, 53];
    
    for (let page = 1; page <= maxPage; page++) {
        navbarSlots.forEach(slot => {
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
        
        // If single page or page 1, slot 48 has no arrow -> put glass pane
        if (page === 1) {
            maxId++;
            dummySection += `
    ${maxId}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 48
      pages:
        - 1`;
        }
        
        // If last page (or single page), slot 50 has no arrow -> put glass pane
        if (page === maxPage) {
            maxId++;
            dummySection += `
    ${maxId}:
      type: dummy
      item:
        material: GRAY_STAINED_GLASS_PANE
        quantity: 1
        name: " "
      slot: 50
      pages:
        - ${page}`;
        }
    }
    
    content = content.trimEnd() + dummySection + '\n';
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated shop ${file} (max pages: ${maxPage}) with full navbar on all pages.`);
});
