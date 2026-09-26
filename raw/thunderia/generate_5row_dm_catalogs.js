const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';

function getItems(filename) {
    const content = fs.readFileSync(path.join(shopsDir, filename), 'utf8');
    const lines = content.split('\n');
    let mat = '', name = '', buy = -1, sell = -1;
    let items = [];
    
    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        let matMatch = line.match(/^\s+material:\s*([A-Z0-9_]+)/);
        if (matMatch) mat = matMatch[1].trim();
        
        let nameMatch = line.match(/^\s+name:\s*(.+)$/);
        if (nameMatch) name = nameMatch[1].trim().replace(/^['"]|['"]$/g, '');
        
        let buyMatch = line.match(/^\s+buyPrice:\s*([0-9.-]+)/);
        if (buyMatch) buy = parseFloat(buyMatch[1]);
        
        let sellMatch = line.match(/^\s+sellPrice:\s*([0-9.-]+)/);
        if (sellMatch) {
            sell = parseFloat(sellMatch[1]);
            if (sell > 0) {
                items.push({ material: mat, name, buy, sell });
            }
            mat = ''; name = ''; buy = -1; sell = -1;
        }
    }
    return items;
}

const categories = [
    { id: 'precios_farmeo', title: '&0&l|&r &0Venta ▶ &8Cultivos', name: 'Cultivos', mat: 'WHEAT', color: '&#FFAA00', slot: 3, file: 'farmeo.yml' },
    { id: 'precios_mobs', title: '&0&l|&r &0Venta ▶ &8Mobs', name: 'Drops de Mobs', mat: 'GUNPOWDER', color: '&#00FF88', slot: 4, file: 'mobs.yml' },
    { id: 'precios_especiales', title: '&0&l|&r &0Venta ▶ &8Especiales', name: 'Especiales', mat: 'AMETHYST_CLUSTER', color: '&#E727F5', slot: 5, file: 'venta.yml' }
];

function generate5RowCatalog(activeCat) {
    let yaml = "menu_title: '" + activeCat.title + "'\n";
    yaml += "open_command:\n";
    if (activeCat.id === 'precios_farmeo') {
        yaml += "  - shopvender\n  - preciosvender\n  - " + activeCat.id + "\n";
    } else {
        yaml += "  - " + activeCat.id + "\n";
    }
    yaml += "size: 45\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n";
    
    // 1. TOP NAVBAR (FILA 1: SLOTS 0 A 8)
    yaml += "  # ============================================================================\n";
    yaml += "  # NAVBAR SUPERIOR: PESTAÑAS (FILA 1)\n";
    yaml += "  # ============================================================================\n";
    
    categories.forEach(cat => {
        const isActive = cat.id === activeCat.id;
        yaml += "  'Tab_" + cat.id + "':\n";
        yaml += "    material: " + cat.mat + "\n";
        yaml += "    slot: " + cat.slot + "\n";
        yaml += "    hide_attributes: true\n";
        
        if (isActive) {
            yaml += "    hide_enchantments: true\n";
            yaml += "    enchantments:\n";
            yaml += "      - DURABILITY;1\n";
            yaml += "    display_name: '" + cat.color + cat.name + " &a✔'\n";
            yaml += "    lore:\n";
            yaml += "      - '&8ᴘᴇꜱᴛᴀñᴀ ᴀᴄᴛɪᴠᴀ'\n";
            yaml += "      - ''\n";
            yaml += "      - ' &aViendo esta categoría.'\n\n";
        } else {
            yaml += "    display_name: '&7" + cat.name + "'\n";
            yaml += "    lore:\n";
            yaml += "      - '&8ᴘᴇꜱᴛᴀñᴀ'\n";
            yaml += "      - ''\n";
            yaml += "      - '&7▶ Click para cambiar'\n";
            yaml += "    left_click_commands:\n";
            yaml += "      - '[openguimenu] " + cat.id + "'\n";
            yaml += "      - '[sound] UI_BUTTON_CLICK'\n\n";
        }
    });
    
    yaml += "  'Filtro_Top':\n";
    yaml += "    material: GRAY_STAINED_GLASS_PANE\n";
    yaml += "    display_name: ' '\n";
    yaml += "    slots:\n";
    yaml += "      - 0\n      - 1\n      - 2\n      - 6\n      - 7\n      - 8\n\n";
    
    // 2. ITEMS GRID (FILAS 2, 3, 4: SLOTS 9 A 35 -> 27 SLOTS DISPONIBLES)
    yaml += "  # ============================================================================\n";
    yaml += "  # CATÁLOGO DE ÍTEMS (FILAS 2, 3, 4: SLOTS 9 A 35)\n";
    yaml += "  # ============================================================================\n";
    
    const rawItems = getItems(activeCat.file);
    
    rawItems.forEach((it, idx) => {
        if (idx < 27) {
            let actualSlot = 9 + idx;
            let itemName = it.name ? it.name.replace(/&l/g, '') : ("&#00FF88" + it.material.replace(/_/g, " "));
            yaml += "  'item_" + (idx + 1) + "':\n";
            yaml += "    material: " + it.material + "\n";
            yaml += "    slot: " + actualSlot + "\n";
            yaml += "    hide_attributes: true\n";
            yaml += "    display_name: '" + itemName + "'\n";
            yaml += "    lore:\n";
            yaml += "      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴠᴇɴᴛᴀ'\n";
            yaml += "      - ''\n";
            yaml += "      - ' &8▶ &fUnidad: &a$" + it.sell + "'\n";
            yaml += "      - ' &8▶ &fStack x64: &a$" + (it.sell * 64) + "'\n\n";
        }
    });
    
    // 3. BOTTOM NAVBAR (FILA 5: SLOTS 36 A 44)
    yaml += "  # ============================================================================\n";
    yaml += "  # NAVBAR INFERIOR (FILA 5: SLOTS 36 A 44)\n";
    yaml += "  # ============================================================================\n";
    yaml += "  'Boton_Volver':\n";
    yaml += "    material: DARK_OAK_DOOR\n";
    yaml += "    slot: 40\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&cVolver Atrás'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8Regresar al menú principal'\n";
    yaml += "    left_click_commands:\n";
    yaml += "      - '[openguimenu] tienda_principal'\n";
    yaml += "      - '[sound] UI_BUTTON_CLICK'\n\n";
    
    yaml += "  'Boton_SellGUI':\n";
    yaml += "    material: HOPPER\n";
    yaml += "    slot: 43\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&#00B7FFVenta Rápida'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8ᴠᴇɴᴛᴀ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀ'\n";
    yaml += "      - ''\n";
    yaml += "      - ' &fVende tu inventario.'\n";
    yaml += "      - ''\n";
    yaml += "      - '&7▶ Click para abrir'\n";
    yaml += "    left_click_commands:\n";
    yaml += "      - '[close]'\n";
    yaml += "      - '[player] sellgui'\n";
    yaml += "      - '[sound] ENTITY_EXPERIENCE_ORB_PICKUP'\n\n";
    
    yaml += "  'Info_Balance':\n";
    yaml += "    material: SUNFLOWER\n";
    yaml += "    slot: 44\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&#FFD700Tu Economía'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8ʙᴀʟᴀɴᴄᴇ'\n";
    yaml += "      - ''\n";
    yaml += "      - ' &8▶ &a$%vault_eco_balance_formatted%'\n\n";
    
    yaml += "  'Filtro_Bottom':\n";
    yaml += "    material: GRAY_STAINED_GLASS_PANE\n";
    yaml += "    display_name: ' '\n";
    yaml += "    slots:\n";
    yaml += "      - 36\n      - 37\n      - 38\n      - 39\n      - 41\n      - 42\n";
    
    return yaml;
}

categories.forEach(cat => {
    const yaml = generate5RowCatalog(cat);
    fs.writeFileSync('creator/output/MenusIA/' + cat.id + '.yml', yaml, 'utf8');
    console.log('Updated 5-row catalog for:', cat.id);
});
