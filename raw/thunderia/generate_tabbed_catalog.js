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
    { id: 'precios_farmeo', name: 'Agricultura', mat: 'WHEAT', color: '&#FFAA00', slot: 1, file: 'farmeo.yml' },
    { id: 'precios_mobs', name: 'Drops de Mobs', mat: 'GUNPOWDER', color: '&#00FF88', slot: 2, file: 'mobs.yml' },
    { id: 'precios_comida', name: 'Comida', mat: 'COOKED_BEEF', color: '&#FF5555', slot: 3, file: 'comida.yml' },
    { id: 'precios_misc', name: 'Misceláneo', mat: 'AMETHYST_SHARD', color: '&#CF27F5', slot: 4, file: 'miscellaneo.yml' },
    { id: 'precios_redstone', name: 'Redstone', mat: 'REDSTONE', color: '&#FF3333', slot: 5, file: 'redstone.yml' },
    { id: 'precios_equipo', name: 'Equipo & Minería', mat: 'DIAMOND_SWORD', color: '&#E727F5', slot: 6, file: 'equipo.yml' },
    { id: 'precios_bloques', name: 'Bloques', mat: 'GRASS_BLOCK', color: '&#00B7FF', slot: 7, file: 'bloques.yml' }
];

function generateTabbedCatalog(activeCat) {
    let yaml = "menu_title: '&0&l|&r &0ThunderMC &0▶ &8Precios ▶ " + activeCat.name + "'\n";
    yaml += "open_command:\n";
    if (activeCat.id === 'precios_farmeo') {
        yaml += "  - shopvender\n  - preciosvender\n  - " + activeCat.id + "\n";
    } else {
        yaml += "  - " + activeCat.id + "\n";
    }
    yaml += "size: 54\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n";
    
    // 1. TOP NAVBAR (FILA 1: SLOTS 1 A 7)
    yaml += "  # ============================================================================\n";
    yaml += "  # NAVBAR SUPERIOR: PESTAÑAS DE CATEGORÍAS (FILA 1)\n";
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
            yaml += "      - ' &aActualmente viendo'\n";
            yaml += "      - ' &aesta categoría.'\n\n";
        } else {
            yaml += "    display_name: '&7" + cat.name + "'\n";
            yaml += "    lore:\n";
            yaml += "      - '&8ᴘᴇꜱᴛᴀñᴀ'\n";
            yaml += "      - ''\n";
            yaml += "      - ' &fVer catálogo de'\n";
            yaml += "      - ' &f" + cat.name.toLowerCase() + ".'\n";
            yaml += "      - ''\n";
            yaml += "      - '&7▶ Click para cambiar'\n";
            yaml += "    left_click_commands:\n";
            yaml += "      - '[openguimenu] " + cat.id + "'\n";
            yaml += "      - '[sound] UI_BUTTON_CLICK'\n\n";
        }
    });
    
    // Top separator
    yaml += "  'Separador_Top':\n";
    yaml += "    material: BLACK_STAINED_GLASS_PANE\n";
    yaml += "    display_name: ' '\n";
    yaml += "    slots:\n";
    yaml += "      - 0\n      - 8\n      - 9\n      - 10\n      - 11\n      - 12\n      - 13\n      - 14\n      - 15\n      - 16\n      - 17\n\n";
    
    // 2. ITEMS GRID (FILAS 3, 4, 5: SLOTS 19-25, 28-34, 37-43 -> 21 SLOTS)
    yaml += "  # ============================================================================\n";
    yaml += "  # CATÁLOGO DE ÍTEMS DE LA CATEGORÍA (FILAS 3 A 5)\n";
    yaml += "  # ============================================================================\n";
    
    let rawItems = [];
    if (activeCat.id === 'precios_equipo') {
        rawItems = [...getItems('equipo.yml'), ...getItems('venta.yml')];
    } else {
        rawItems = getItems(activeCat.file);
    }
    
    const itemSlots = [
        19, 20, 21, 22, 23, 24, 25,
        28, 29, 30, 31, 32, 33, 34,
        37, 38, 39, 40, 41, 42, 43
    ];
    
    rawItems.forEach((it, idx) => {
        if (idx < itemSlots.length) {
            let actualSlot = itemSlots[idx];
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
    
    // Side borders
    yaml += "  'Bordes_Laterales':\n";
    yaml += "    material: GRAY_STAINED_GLASS_PANE\n";
    yaml += "    display_name: ' '\n";
    yaml += "    slots:\n";
    yaml += "      - 18\n      - 26\n      - 27\n      - 35\n      - 36\n      - 44\n\n";
    
    // 3. BOTTOM NAVBAR (FILA 6: SLOTS 45 A 53)
    yaml += "  # ============================================================================\n";
    yaml += "  # NAVBAR INFERIOR (FILA 6)\n";
    yaml += "  # ============================================================================\n";
    yaml += "  'Boton_Volver':\n";
    yaml += "    material: DARK_OAK_DOOR\n";
    yaml += "    slot: 49\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&cVolver Atrás'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8Regresar al menú principal'\n";
    yaml += "    left_click_commands:\n";
    yaml += "      - '[openguimenu] tienda_principal'\n";
    yaml += "      - '[sound] UI_BUTTON_CLICK'\n\n";
    
    yaml += "  'Boton_SellGUI':\n";
    yaml += "    material: HOPPER\n";
    yaml += "    slot: 52\n";
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
    yaml += "    slot: 53\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&#FFD700Tu Economía'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8ʙᴀʟᴀɴᴄᴇ'\n";
    yaml += "      - ''\n";
    yaml += "      - ' &8▶ &a$%vault_eco_balance_formatted%'\n\n";
    
    yaml += "  'Filtro_Navbar_Bottom':\n";
    yaml += "    material: GRAY_STAINED_GLASS_PANE\n";
    yaml += "    display_name: ' '\n";
    yaml += "    slots:\n";
    yaml += "      - 45\n      - 46\n      - 47\n      - 48\n      - 50\n      - 51\n";
    
    return yaml;
}

categories.forEach(cat => {
    const yaml = generateTabbedCatalog(cat);
    fs.writeFileSync('creator/output/MenusIA/' + cat.id + '.yml', yaml, 'utf8');
    console.log('Generated tabbed menu: ' + cat.id);
});
