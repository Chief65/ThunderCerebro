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
    let lines = [];
    lines.push("menu_title: '" + activeCat.title + "'");
    lines.push("open_command:");
    if (activeCat.id === 'precios_farmeo') {
        lines.push("  - shopvender");
        lines.push("  - preciosvender");
        lines.push("  - " + activeCat.id);
    } else {
        lines.push("  - " + activeCat.id);
    }
    lines.push("size: 45");
    lines.push("open_requirement:");
    lines.push("  requirements: {}");
    lines.push("register_command: true");
    lines.push("update: true");
    lines.push("");
    lines.push("items:");
    lines.push("  # ============================================================================");
    lines.push("  # NAVBAR SUPERIOR: PESTAÑAS (FILA 1)");
    lines.push("  # ============================================================================");
    
    categories.forEach(cat => {
        const isActive = cat.id === activeCat.id;
        lines.push("  'Tab_" + cat.id + "':");
        lines.push("    material: " + cat.mat);
        lines.push("    slot: " + cat.slot);
        lines.push("    item_flags:");
        lines.push("      - HIDE_ATTRIBUTES");
        if (isActive) {
            lines.push("      - HIDE_ENCHANTS");
            lines.push("    enchantments:");
            lines.push("      - DURABILITY;1");
            lines.push("    display_name: '" + cat.color + cat.name + " &a✔'");
            lines.push("    lore:");
            lines.push("      - '&8ᴘᴇꜱᴛᴀñᴀ ᴀᴄᴛɪᴠᴀ'");
            lines.push("      - ''");
            lines.push("      - ' &aViendo esta categoría.'");
            lines.push("");
        } else {
            lines.push("    display_name: '&7" + cat.name + "'");
            lines.push("    lore:");
            lines.push("      - '&8ᴘᴇꜱᴛᴀñᴀ'");
            lines.push("      - ''");
            lines.push("      - '&7▶ Click para cambiar'");
            lines.push("    left_click_commands:");
            lines.push("      - '[openguimenu] " + cat.id + "'");
            lines.push("      - '[sound] UI_BUTTON_CLICK'");
            lines.push("");
        }
    });
    
    lines.push("  'Filtro_Top':");
    lines.push("    material: GRAY_STAINED_GLASS_PANE");
    lines.push("    display_name: ' '");
    lines.push("    slots:");
    lines.push("      - 0\n      - 1\n      - 2\n      - 6\n      - 7\n      - 8");
    lines.push("");
    
    // Items grid
    lines.push("  # ============================================================================");
    lines.push("  # CATÁLOGO DE ÍTEMS (FILAS 2, 3, 4: SLOTS 9 A 35)");
    lines.push("  # ============================================================================");
    
    let rawItems = [];
    if (activeCat.id === 'precios_especiales') {
        rawItems = [
            {
                material: 'AMETHYST_CLUSTER',
                name: '&#E727F5Cristal Estelar',
                customLore: [
                    "&8ᴏʙᴊᴇᴛᴏ ᴇꜱᴘᴇᴄɪᴀʟ",
                    "",
                    " &8| &fUnidad: &#59E91F&l$&r&#59E91F10",
                    " &8| &fStack x64: &#59E91F&l$&r&#59E91F640",
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
            lines.push("  'item_" + (idx + 1) + "':");
            lines.push("    material: " + it.material);
            lines.push("    slot: " + actualSlot);
            lines.push("    item_flags:");
            lines.push("      - HIDE_ATTRIBUTES");
            lines.push("    display_name: '" + it.name + "'");
            lines.push("    lore:");
            if (it.customLore) {
                it.customLore.forEach(l => lines.push("      - '" + l + "'"));
            } else {
                lines.push("      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴠᴇɴᴛᴀ'");
                lines.push("      - ''");
                lines.push("      - ' &8| &fUnidad: &#59E91F&l$&r&#59E91F" + it.sell + "'");
                lines.push("      - ' &8| &fStack x64: &#59E91F&l$&r&#59E91F" + (it.sell * 64) + "'");
            }
            lines.push("");
        }
    });
    
    // Bottom navbar
    lines.push("  # ============================================================================");
    lines.push("  # NAVBAR INFERIOR (FILA 5: SLOTS 36 A 44)");
    lines.push("  # ============================================================================");
    lines.push("  'Boton_Volver':");
    lines.push("    material: DARK_OAK_DOOR");
    lines.push("    slot: 40");
    lines.push("    item_flags:");
    lines.push("      - HIDE_ATTRIBUTES");
    lines.push("    display_name: '&cVolver Atrás'");
    lines.push("    lore:");
    lines.push("      - '&8Regresar al menú principal'");
    lines.push("    left_click_commands:");
    lines.push("      - '[openguimenu] tienda_principal'");
    lines.push("      - '[sound] UI_BUTTON_CLICK'");
    lines.push("");
    
    lines.push("  'Boton_SellGUI':");
    lines.push("    material: HOPPER");
    lines.push("    slot: 43");
    lines.push("    item_flags:");
    lines.push("      - HIDE_ATTRIBUTES");
    lines.push("    display_name: '&#00B7FFVenta Rápida'");
    lines.push("    lore:");
    lines.push("      - '&8ᴠᴇɴᴛᴀ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀ'");
    lines.push("      - ''");
    lines.push("      - ' &fVende tu inventario.'");
    lines.push("      - ''");
    lines.push("      - '&7▶ Click para abrir'");
    lines.push("    left_click_commands:");
    lines.push("      - '[close]'");
    lines.push("      - '[player] sellgui'");
    lines.push("      - '[sound] ENTITY_EXPERIENCE_ORB_PICKUP'");
    lines.push("");
    
    lines.push("  'Info_Balance':");
    lines.push("    material: SUNFLOWER");
    lines.push("    slot: 44");
    lines.push("    item_flags:");
    lines.push("      - HIDE_ATTRIBUTES");
    lines.push("    display_name: '&#FFD700Tu Economía'");
    lines.push("    lore:");
    lines.push("      - '&8ᴛᴜ ᴇᴄᴏɴᴏᴍɪᴀ'");
    lines.push("      - ''");
    lines.push("      - ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%'");
    lines.push("      - ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas%🔥'");
    lines.push("      - ' &8| &fZafiros: &#1E6BFF%thundercurrencys_zafiros%💎'");
    lines.push("      - ''");
    lines.push("");
    
    lines.push("  'Filtro_Bottom':");
    lines.push("    material: GRAY_STAINED_GLASS_PANE");
    lines.push("    display_name: ' '");
    lines.push("    slots:");
    lines.push("      - 36\n      - 37\n      - 38\n      - 39\n      - 41\n      - 42");
    lines.push("");
    
    return lines.join('\n');
}

// Generate tienda_principal.yml cleanly
const tiendaPrincipalLines = [
    "menu_title: '&0&l|&r &0Tienda ▶ &8Menu'",
    "open_command:",
    "  - shop",
    "  - tienda",
    "  - mercado",
    "size: 36",
    "open_requirement:",
    "  requirements: {}",
    "register_command: true",
    "update: true",
    "",
    "items:",
    "  'Boton_Comprar':",
    "    material: EMERALD",
    "    slot: 12",
    "    item_flags:",
    "      - HIDE_ENCHANTS",
    "      - HIDE_ATTRIBUTES",
    "    enchantments:",
    "      - DURABILITY;1",
    "    display_name: '&#00FF88Comprar Artículos'",
    "    lore:",
    "      - '&8ᴛɪᴇɴᴅᴀ ᴅᴇ ᴄᴏᴍᴘʀᴀ'",
    "      - ''",
    "      - ' &fAdquiere bloques,'",
    "      - ' &fequipo y consumibles.'",
    "      - ''",
    "      - '&7▶ Click para abrir'",
    "    left_click_commands:",
    "      - '[close]'",
    "      - '[player] shopgui'",
    "      - '[sound] UI_BUTTON_CLICK'",
    "",
    "  'Boton_Vender':",
    "    material: SPYGLASS",
    "    slot: 14",
    "    item_flags:",
    "      - HIDE_ENCHANTS",
    "      - HIDE_ATTRIBUTES",
    "    enchantments:",
    "      - DURABILITY;1",
    "    display_name: '&#FFAA00Catálogo de Precios'",
    "    lore:",
    "      - '&8ᴄᴀᴛᴀʟᴏɢᴏ ᴅᴇ ᴠᴇɴᴛᴀ'",
    "      - ''",
    "      - ' &fConsulta el valor de'",
    "      - ' &ftus excedentes.'",
    "      - ''",
    "      - '&7▶ Click para ver precios'",
    "    left_click_commands:",
    "      - '[openguimenu] precios_farmeo'",
    "      - '[sound] UI_BUTTON_CLICK'",
    "",
    "  'Boton_Subastas':",
    "    material: BELL",
    "    slot: 27",
    "    item_flags:",
    "      - HIDE_ATTRIBUTES",
    "    display_name: '&#FEEB00Mercado de Subastas'",
    "    lore:",
    "      - '&8ꜱᴜʙᴀꜱᴛᴀꜱ'",
    "      - ''",
    "      - ' &fComercia con otros'",
    "      - ' &fjugadores.'",
    "      - ''",
    "      - '&7▶ Click para abrir'",
    "    left_click_commands:",
    "      - '[close]'",
    "      - '[player] ah'",
    "      - '[sound] UI_BUTTON_CLICK'",
    "",
    "  'Boton_Almas':",
    "    material: SOUL_CAMPFIRE",
    "    slot: 28",
    "    item_flags:",
    "      - HIDE_ATTRIBUTES",
    "    display_name: '&#00FFFFTienda de Almas'",
    "    lore:",
    "      - '&8ᴛɪᴇɴᴅᴀ ᴇꜱᴘᴇᴄɪᴀʟ'",
    "      - ''",
    "      - ' &fCanjea tus almas por'",
    "      - ' &frecompensas únicas.'",
    "      - ''",
    "      - '&7▶ Click para abrir'",
    "    left_click_commands:",
    "      - '[close]'",
    "      - '[player] shop almas'",
    "      - '[sound] UI_BUTTON_CLICK'",
    "",
    "  'Boton_Cerrar':",
    "    material: DARK_OAK_DOOR",
    "    slot: 31",
    "    item_flags:",
    "      - HIDE_ATTRIBUTES",
    "    display_name: '&cSalir'",
    "    left_click_commands:",
    "      - '[close]'",
    "      - '[sound] BLOCK_NOTE_BLOCK_BASS'",
    "",
    "  'Boton_SellGUI':",
    "    material: HOPPER",
    "    slot: 34",
    "    item_flags:",
    "      - HIDE_ATTRIBUTES",
    "    display_name: '&#00B7FFVenta Rápida'",
    "    lore:",
    "      - '&8ᴠᴇɴᴛᴀ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀ'",
    "      - ''",
    "      - ' &fVende ítems en masa'",
    "      - ' &fde forma instantánea.'",
    "      - ''",
    "      - '&7▶ Click para abrir'",
    "    left_click_commands:",
    "      - '[close]'",
    "      - '[player] sellgui'",
    "      - '[sound] ENTITY_EXPERIENCE_ORB_PICKUP'",
    "",
    "  'Info_Balance':",
    "    material: SUNFLOWER",
    "    slot: 35",
    "    item_flags:",
    "      - HIDE_ATTRIBUTES",
    "    display_name: '&#FFD700Tu Economía'",
    "    lore:",
    "      - '&8ᴛᴜ ᴇᴄᴏɴᴏᴍɪᴀ'",
    "      - ''",
    "      - ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%'",
    "      - ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas%🔥'",
    "      - ' &8| &fZafiros: &#1E6BFF%thundercurrencys_zafiros%💎'",
    "      - ''",
    "",
    "  'Filtro_Navbar':",
    "    material: GRAY_STAINED_GLASS_PANE",
    "    display_name: ' '",
    "    slots:",
    "      - 29",
    "      - 30",
    "      - 32",
    "      - 33",
    ""
];

fs.writeFileSync('creator/output/MenusIA/tienda_principal.yml', tiendaPrincipalLines.join('\n'), 'utf8');

categories.forEach(cat => {
    fs.writeFileSync('creator/output/MenusIA/' + cat.id + '.yml', generate5RowCatalog(cat), 'utf8');
});

console.log('All DeluxeMenus files compiled cleanly.');

// Update ShopGUIPlus config.yml cleanly
const sguipPath = 'raw/thunderia/ShopGUIPlus/config.yml';
let sguip = fs.readFileSync(sguipPath, 'utf8');

const sguipLore = `shopItemLoreFormat:
  # This lore will be applied to items
  item:
    - "&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴄᴏᴍᴘʀᴀ"
    - ""
    - " &8| &fPrecio: &a&l%buy%"
    - ""
    - "&7▶ Click para comprar"
  # This lore will be applied to items in the buy GUI (when enableBuyGUI is set to true)
  itemBuyGUI:
    - "&8ᴄᴏᴍᴘʀᴀ ᴇɴ ᴄᴀɴᴛɪᴅᴀᴅ"
    - ""
    - " &8| &fCantidad: &e%amount%"
    - " &8| &fTotal: &a&l%buy%"
  # This lore will be applied to items in the sell GUI (when enableSellGUI is set to true)
  itemSellGUI:
    - "&8ᴠᴇɴᴛᴀ ᴇɴ ᴄᴀɴᴛɪᴅᴀᴅ"
    - ""
    - " &8| &fCantidad: &e%amount%"
    - " &8| &fTotal: &a&l%sell%"
  # This lore will be applied to the sell all button in the sell GUI (when enableSellGUI and enableSellGUISellAll are set to true)
  itemSellGUISellAll:
    - "&8| &fVender todo por: &a&l%sell%"
  # This one to permissions
  permission:
    - "&8| &fPrecio: &a&l%buy%"
  # And this one to enchantments
  enchantment:
    - "&8| &fPrecio: &a&l%buy%"
  # And the last one to commands
  command:
    - "&8| &fPrecio: &a&l%buy%"`;

sguip = sguip.replace(/shopItemLoreFormat:[\s\S]*?(?=\r?\n# Logging settings|\r?\nlog:)/, sguipLore);
fs.writeFileSync(sguipPath, sguip, 'utf8');
console.log('ShopGUIPlus config.yml updated cleanly.');
