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

function generatePureCatalogYaml(menuId, title, items) {
    let yaml = "menu_title: '&0&l|&r &0ThunderMC &0▶ &8" + title + "'\n";
    yaml += "size: 45\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n";
    
    items.forEach((it, idx) => {
        if (idx < 21) {
            let actualSlot = 10 + (idx % 7) + Math.floor(idx / 7) * 9;
            let itemName = it.name ? it.name : ("&#00FF88" + it.material.replace(/_/g, " "));
            yaml += "  'item_" + (idx + 1) + "':\n";
            yaml += "    material: " + it.material + "\n";
            yaml += "    slot: " + actualSlot + "\n";
            yaml += "    hide_attributes: true\n";
            yaml += "    display_name: '" + itemName + "'\n";
            yaml += "    lore:\n";
            yaml += "      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴠᴇɴᴛᴀ'\n";
            yaml += "      - ''\n";
            yaml += "      - ' &8▶ &fPrecio Unitario: &a$" + it.sell + "'\n";
            yaml += "      - ' &8▶ &fPrecio Stack (x64): &a$" + (it.sell * 64) + "'\n\n";
        }
    });
    
    // Navbar
    yaml += "  # ============================================================================\n";
    yaml += "  # NAVBAR INFERIOR (FILA 5)\n";
    yaml += "  # ============================================================================\n";
    yaml += "  'Boton_Volver':\n";
    yaml += "    material: DARK_OAK_DOOR\n";
    yaml += "    slot: 40\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&cVolver Atrás'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8Regresar a categorías de venta'\n";
    yaml += "    left_click_commands:\n";
    yaml += "      - '[openguimenu] tienda_vender'\n";
    yaml += "      - '[sound] UI_BUTTON_CLICK'\n\n";
    
    yaml += "  'Boton_SellGUI':\n";
    yaml += "    material: HOPPER\n";
    yaml += "    slot: 43\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&#00B7FF&lVenta Rápida (SellGUI)'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8ᴠᴇɴᴛᴀ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀ'\n";
    yaml += "      - ''\n";
    yaml += "      - ' &fAbre SellGUI para vender'\n";
    yaml += "      - ' &ftodo tu inventario.'\n";
    yaml += "      - ''\n";
    yaml += "      - '&7▶ Click para abrir SellGUI'\n";
    yaml += "    left_click_commands:\n";
    yaml += "      - '[close]'\n";
    yaml += "      - '[player] sellgui'\n";
    yaml += "      - '[sound] ENTITY_EXPERIENCE_ORB_PICKUP'\n\n";
    
    yaml += "  'Info_Balance':\n";
    yaml += "    material: SUNFLOWER\n";
    yaml += "    slot: 44\n";
    yaml += "    hide_attributes: true\n";
    yaml += "    display_name: '&#FFD700&lTu Economía'\n";
    yaml += "    lore:\n";
    yaml += "      - '&8▶ &a$%vault_eco_balance_formatted%'\n\n";
    
    yaml += "  'Filtro_Navbar':\n";
    yaml += "    material: GRAY_STAINED_GLASS_PANE\n";
    yaml += "    display_name: ' '\n";
    yaml += "    slots:\n";
    yaml += "      - 36\n      - 37\n      - 38\n      - 39\n      - 41\n      - 42\n";
    
    return yaml;
}

const configs = [
    { id: 'precios_farmeo', title: 'Precios ▶ Farmeo', file: 'farmeo.yml' },
    { id: 'precios_mobs', title: 'Precios ▶ Drops Mobs', file: 'mobs.yml' },
    { id: 'precios_comida', title: 'Precios ▶ Comida', file: 'comida.yml' },
    { id: 'precios_misc', title: 'Precios ▶ Misceláneo', file: 'miscellaneo.yml' },
    { id: 'precios_redstone', title: 'Precios ▶ Redstone', file: 'redstone.yml' }
];

configs.forEach(c => {
    const items = getItems(c.file);
    const yaml = generatePureCatalogYaml(c.id, c.title, items);
    fs.writeFileSync('creator/output/MenusIA/' + c.id + '.yml', yaml, 'utf8');
    console.log('Updated creator/output/MenusIA/' + c.id + '.yml as pure catalog');
});

// Equipo + Venta Especial
const equipoItems = getItems('equipo.yml');
const ventaItems = getItems('venta.yml');
const comboItems = [...equipoItems, ...ventaItems];
const equipoYaml = generatePureCatalogYaml('precios_equipo', 'Precios ▶ Equipo & Especiales', comboItems);
fs.writeFileSync('creator/output/MenusIA/precios_equipo.yml', equipoYaml, 'utf8');
console.log('Updated creator/output/MenusIA/precios_equipo.yml as pure catalog');
