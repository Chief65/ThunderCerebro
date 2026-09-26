const fs = require('fs');
const path = require('path');

const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';

const namesMap = {
    'BAMBOO': 'Bambú',
    'BEETROOT': 'Remolacha',
    'BEETROOT_SEEDS': 'Semillas de Remolacha',
    'BROWN_MUSHROOM': 'Champiñón Marrón',
    'CACTUS': 'Cactus',
    'CARROT': 'Zanahoria',
    'COCOA_BEANS': 'Granos de Cacao',
    'KELP': 'Alga',
    'MELON': 'Sandía',
    'MELON_SEEDS': 'Semillas de Sandía',
    'MELON_SLICE': 'Rodaja de Sandía',
    'NETHER_WART': 'Verruga del Nether',
    'POTATO': 'Patata',
    'PUMPKIN': 'Calabaza',
    'PUMPKIN_SEEDS': 'Semillas de Calabaza',
    'RED_MUSHROOM': 'Champiñón Rojo',
    'SUGAR_CANE': 'Caña de Azúcar',
    'SWEET_BERRIES': 'Bayas Dulces',
    'WHEAT': 'Trigo',
    'WHEAT_SEEDS': 'Semillas de Trigo',
    'GLOW_BERRIES': 'Bayas Luminosas',
    'ARROW': 'Flecha',
    'BLAZE_POWDER': 'Polvo de Blaze',
    'BLAZE_ROD': 'Vara de Blaze',
    'BREEZE_ROD': 'Vara de Breeze',
    'BONE': 'Hueso',
    'ENDER_PEARL': 'Perla de Ender',
    'FEATHER': 'Pluma',
    'GUNPOWDER': 'Pólvora',
    'MAGMA_CREAM': 'Crema de Magma',
    'PHANTOM_MEMBRANE': 'Membrana de Phantom',
    'RABBIT_FOOT': 'Pata de Conejo',
    'RABBIT_HIDE': 'Piel de Conejo',
    'ROTTEN_FLESH': 'Carne Podrida',
    'SLIME_BALL': 'Bola de Slime',
    'SPIDER_EYE': 'Ojo de Araña',
    'STRING': 'Hilo',
    'PRISMARINE_SHARD': 'Fragmento de Prismarina',
    'LEATHER': 'Cuero',
    'HONEYCOMB': 'Panal de Miel'
};

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
                let displayName = '';
                if (namesMap[mat]) {
                    displayName = '&#00FF88' + namesMap[mat];
                } else if (name && !name.includes('Tienda ▶') && !name.includes('Tier')) {
                    displayName = name;
                } else {
                    displayName = '&#00FF88' + mat.replace(/_/g, ' ');
                }
                items.push({ material: mat, name: displayName, buy, sell });
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
    
    // 1. TOP NAVBAR
    categories.forEach(cat => {
        const isActive = cat.id === activeCat.id;
        yaml += "  'Tab_" + cat.id + "':\n";
        yaml += "    material: " + cat.mat + "\n";
        yaml += "    slot: " + cat.slot + "\n";
        yaml += "    item_flags:\n";
        yaml += "      - HIDE_ATTRIBUTES\n";
        
        if (isActive) {
            yaml += "      - HIDE_ENCHANTS\n";
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
    
    // 2. ITEMS GRID
    let rawItems = [];
    if (activeCat.id === 'precios_especiales') {
        rawItems = [
            {
                material: 'AMETHYST_CLUSTER',
                name: '&#E727F5Cristal Estelar',
                sell: 10,
                customLore: [
                    "&8ᴏʙᴊᴇᴛᴏ ᴇꜱᴘᴇᴄɪᴀʟ",
                    "",
                    " &8▶ &fUnidad: &a$10",
                    " &8▶ &fStack x64: &a$640",
                    "",
                    " &7Obtenible en &e/minas",
                    " &7durante la excavación."
                ]
            }
        ];
    } else {
        rawItems = getItems(activeCat.file);
    }
    
    rawItems.forEach((it, idx) => {
        if (idx < 27) {
            let actualSlot = 9 + idx;
            yaml += "  'item_" + (idx + 1) + "':\n";
            yaml += "    material: " + it.material + "\n";
            yaml += "    slot: " + actualSlot + "\n";
            yaml += "    item_flags:\n";
            yaml += "      - HIDE_ATTRIBUTES\n";
            yaml += "    display_name: '" + it.name + "'\n";
            yaml += "    lore:\n";
            if (it.customLore) {
                it.customLore.forEach(l => {
                    yaml += "      - '" + l + "'\n";
                });
            } else {
                yaml += "      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴠᴇɴᴛᴀ'\n";
                yaml += "      - ''\n";
                yaml += "      - ' &8▶ &fUnidad: &a$" + it.sell + "'\n";
                yaml += "      - ' &8▶ &fStack x64: &a$" + (it.sell * 64) + "'\n";
            }
            yaml += "\n";
        }
    });
    
    // 3. BOTTOM NAVBAR
    yaml += "  'Boton_Volver':\n";
    yaml += "    material: DARK_OAK_DOOR\n";
    yaml += "    slot: 40\n";
    yaml += "    item_flags:\n";
    yaml += "      - HIDE_ATTRIBUTES\n";
    yaml += "    display_name: '&cVolver Atrás'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8Regresar al menú principal'\n";
    yaml += "    left_click_commands:\n";
    yaml += "      - '[openguimenu] tienda_principal'\n";
    yaml += "      - '[sound] UI_BUTTON_CLICK'\n\n";
    
    yaml += "  'Boton_SellGUI':\n";
    yaml += "    material: HOPPER\n";
    yaml += "    slot: 43\n";
    yaml += "    item_flags:\n";
    yaml += "      - HIDE_ATTRIBUTES\n";
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
    yaml += "    item_flags:\n";
    yaml += "      - HIDE_ATTRIBUTES\n";
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

// Also update tienda_principal.yml item_flags
let tpPath = 'creator/output/MenusIA/tienda_principal.yml';
let tpContent = fs.readFileSync(tpPath, 'utf8');
tpContent = tpContent.replace(/hide_attributes:\s*true/g, 'item_flags:\n      - HIDE_ATTRIBUTES');
tpContent = tpContent.replace(/hide_enchantments:\s*true/g, 'item_flags:\n      - HIDE_ENCHANTS\n      - HIDE_ATTRIBUTES');
fs.writeFileSync(tpPath, tpContent, 'utf8');
console.log('Updated tienda_principal item_flags');

categories.forEach(cat => {
    const yaml = generate5RowCatalog(cat);
    fs.writeFileSync('creator/output/MenusIA/' + cat.id + '.yml', yaml, 'utf8');
    console.log('Regenerated DM menu with modern item_flags:', cat.id);
});
