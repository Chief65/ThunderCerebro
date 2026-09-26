const fs = require("fs");

// ============================================================================
// PÁGINA 1: LOS 7 CULTIVOS OFICIALES
// ============================================================================
const page1Cultivos = [
  // 1. Verruga del Nether (Alza: Verde)
  { mat: "NETHER_WART", name: "Verruga del Nether", u: "18.00", s: "1,152.00", cat: "ᴅɪꜰɪᴄᴜʟᴛᴀᴅ ᴀʟᴛᴀ", glassMat: "LIME_STAINED_GLASS_PANE", glassName: "&#59E91F▲ En Auge (+15%)", glow: true },
  // 2. Granos de Cacao (Alza: Verde)
  { mat: "COCOA_BEANS", name: "Granos de Cacao", u: "16.00", s: "1,024.00", cat: "ᴅɪꜰɪᴄᴜʟᴛᴀᴅ ᴀʟᴛᴀ", glassMat: "LIME_STAINED_GLASS_PANE", glassName: "&#59E91F▲ En Auge (+12%)", glow: true },
  // 3. Trigo (Alza: Verde)
  { mat: "WHEAT", name: "Trigo", u: "10.00", s: "640.00", cat: "ᴅɪꜰɪᴄᴜʟᴛᴀᴅ ᴍᴇᴅɪᴀ", glassMat: "LIME_STAINED_GLASS_PANE", glassName: "&#59E91F▲ En Auge (+8%)" },
  // 4. Zanahoria (Estable: Amarillo)
  { mat: "CARROT", name: "Zanahoria", u: "5.50", s: "352.00", cat: "ᴅɪꜰɪᴄᴜʟᴛᴀᴅ ʙᴀᴊᴀ", glassMat: "YELLOW_STAINED_GLASS_PANE", glassName: "&#FFF275= Estable (+4%)" },
  // 5. Patata (Estable: Amarillo)
  { mat: "POTATO", name: "Patata", u: "5.00", s: "320.00", cat: "ᴅɪꜰɪᴄᴜʟᴛᴀᴅ ʙᴀᴊᴀ", glassMat: "YELLOW_STAINED_GLASS_PANE", glassName: "&#FFF275= Estable (+2%)" },
  // 6. Calabaza (Estable: Gris)
  { mat: "PUMPKIN", name: "Calabaza", u: "4.00", s: "256.00", cat: "ᴀᴜᴛᴏᴍᴀᴛɪᴢᴀʙʟᴇ", glassMat: "GRAY_STAINED_GLASS_PANE", glassName: "&7= Regular (0%)" },
  // 7. Caña de Azúcar (Baja: Rojo)
  { mat: "SUGAR_CANE", name: "Caña de Azúcar", u: "2.50", s: "160.00", cat: "ᴀᴜᴛᴏᴍᴀᴛɪᴢᴀʙʟᴇ", glassMat: "RED_STAINED_GLASS_PANE", glassName: "&#FF4D4D▼ A la Baja (-4%)" }
];

// ============================================================================
// PÁGINA 2: LOS 6 DROPS DE MOBS OFICIALES
// ============================================================================
const page2MobDrops = [
  // 1. Breeze (Limited - Alza: Verde)
  { mat: "BREEZE_ROD", name: "Vara de Breeze", u: "45.00", s: "2,880.00", cat: "ᴛɪᴇʀ ʟɪᴍɪᴛᴇᴅ", glassMat: "LIME_STAINED_GLASS_PANE", glassName: "&#59E91F▲ En Auge (+18%)", glow: true },
  // 2. Magma Cube (Mítica - Alza: Verde)
  { mat: "MAGMA_CREAM", name: "Crema de Magma", u: "32.00", s: "2,048.00", cat: "ᴛɪᴇʀ ᴍɪᴛɪᴄᴏ", glassMat: "LIME_STAINED_GLASS_PANE", glassName: "&#59E91F▲ En Auge (+14%)", glow: true },
  // 3. Blaze (Legend - Alza: Verde)
  { mat: "BLAZE_ROD", name: "Vara de Blaze", u: "22.00", s: "1,408.00", cat: "ᴛɪᴇʀ ʟᴇɢᴇɴᴅ", glassMat: "LIME_STAINED_GLASS_PANE", glassName: "&#59E91F▲ En Auge (+10%)" },
  // 4. Enderman (Épica - Estable: Amarillo)
  { mat: "ENDER_PEARL", name: "Perla de Ender", u: "14.00", s: "224.00", cat: "ᴛɪᴇʀ ᴇᴘɪᴄᴏ", glassMat: "YELLOW_STAINED_GLASS_PANE", glassName: "&#FFF275= Estable (+5%)" },
  // 5. Slime (Rara - Estable: Gris)
  { mat: "SLIME_BALL", name: "Bola de Slime", u: "6.50", s: "416.00", cat: "ᴛɪᴇʀ ʀᴀʀᴏ", glassMat: "GRAY_STAINED_GLASS_PANE", glassName: "&7= Regular (0%)" },
  // 6. Zombie (Super - Baja: Rojo)
  { mat: "ROTTEN_FLESH", name: "Carne Podrida", u: "1.50", s: "96.00", cat: "ᴛɪᴇʀ ꜱᴜᴘᴇʀ", glassMat: "RED_STAINED_GLASS_PANE", glassName: "&#FF4D4D▼ A la Baja (-8%)" }
];

function generateCleanMenu(isLonja, title, pageNum, totalPages, items, targetMenu) {
  let out = `menu_title: '${title}'\n`;
  out += `open_command:\n`;
  if (isLonja) {
    if (pageNum === 1) {
      out += `  - lonja\n  - mercadoventa\n  - bolsaventa\n  - lonja_venta\n`;
    } else {
      out += `  - lonja_venta_2\n  - lonja_2\n`;
    }
  } else {
    if (pageNum === 1) {
      out += `  - objetosdeventa\n  - objetosventa\n  - testventa\n`;
    } else {
      out += `  - objetosdeventa_2\n  - objetosventa_2\n`;
    }
  }
  out += `size: 54\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n`;
  
  // MARCO SUPERIOR DE CRISTALES GRISES (Slots 0, 1, 2, 3, 5, 6, 7, 8)
  out += `  'Marco_Top':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 0\n      - 1\n      - 2\n      - 3\n      - 5\n      - 6\n      - 7\n      - 8\n\n`;

  // Cabecera slot 4
  const headerMat = pageNum === 1 ? "WHEAT" : "SPAWNER";
  const headerTitle = pageNum === 1 ? "&#59E91FCultivos: Macrogranjas Activas" : "&#FFAA00Spawners: Renta Pasiva";
  const headerSub = pageNum === 1 ? "ᴍᴀᴄʀᴏɢʀᴀɴᴊᴀꜱ ᴀᴄᴛɪᴠᴀꜱ" : "ᴅʀᴏᴘꜱ ᴅᴇ ᴍᴏʙꜱ";
  out += `  'Cabecera_Info':\n    material: ${headerMat}\n    slot: 4\n    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n    enchantments:\n      - DURABILITY;1\n    display_name: '${headerTitle}'\n    lore:\n      - '&8${headerSub}'\n      - ''\n      - ' &8| &fPágina: &e${pageNum}/${totalPages}'\n      - ' &8| &fTotal: &7${items.length} ítems oficiales'\n      - ' &8| &fPrecios: &7100% unificados'\n      - ''\n      - '&7ThunderMC 1.21.11 SMP'\n\n`;

  // Asignar slots:
  // Fila 3: slots 19 a 25 para 7 items, slots 20 a 25 para 6 items.
  // Fila 4: slots inmediatamente debajo (slot + 9) con el cristal de tendencia.
  let itemSlots = [];
  if (items.length === 7) {
    itemSlots = [19, 20, 21, 22, 23, 24, 25];
  } else {
    itemSlots = [20, 21, 22, 23, 24, 25];
  }

  for (let i = 0; i < items.length; i++) {
    const it = items[i];
    const slot = itemSlots[i];
    const glassSlot = slot + 9; // Fila inmediatamente debajo

    // Item de venta (sin bloque de tendencia en lore)
    out += `  'item_${i + 1}':\n`;
    out += `    material: ${it.mat}\n`;
    out += `    slot: ${slot}\n`;
    out += `    item_flags:\n      - HIDE_ATTRIBUTES\n`;
    if (it.glow) {
      out += `      - HIDE_ENCHANTS\n    enchantments:\n      - DURABILITY;1\n`;
    }
    out += `    display_name: '&#FFF275${it.name}'\n`;
    out += `    lore:\n`;
    out += `      - '&8${it.cat}'\n`;
    out += `      - ''\n`;
    out += `      - ' &8| &fUnidad: &#59E91F&l$&r&#59E91F${it.u}'\n`;
    out += `      - ' &8| &fStack: &#59E91F&l$&r&#59E91F${it.s}'\n`;
    out += `      - ''\n`;
    out += `      - '&7▶ Clic para vender'\n`;
    out += `    left_click_commands:\n`;
    out += `      - '[sound] ENTITY_EXPERIENCE_ORB_PICKUP'\n\n`;

    // Cristal del color de tendencia debajo
    out += `  'cristal_tendencia_${i + 1}':\n`;
    out += `    material: ${it.glassMat}\n`;
    out += `    slot: ${glassSlot}\n`;
    out += `    item_flags:\n      - HIDE_ATTRIBUTES\n`;
    out += `    display_name: '${it.glassName}'\n`;
    out += `    lore:\n`;
    out += `      - '&8ɪɴᴅɪᴄᴀᴅᴏʀ ᴅᴇ ᴍᴇʀᴄᴀᴅᴏ'\n`;
    out += `      - ''\n`;
    out += `      - ' &8| &fEstado: ${it.glassName}'\n`;
    out += `      - ' &8| &fÍtem: &#FFF275${it.name}'\n\n`;
  }

  // =========================================================================
  // FILA 6: NAVBAR INFERIOR (CON CRISTALES GRISES EN HUECOS VACÍOS):
  // Slot 45: Botón alternar menú
  // Slot 49: Botón volver
  // Slot 52: Venta Rápida
  // Slot 53: Tu Economía
  // Cristales grises en: 46, 47, 48, 50, 51
  // =========================================================================

  // Slot 45: Botón alternar
  if (pageNum === 1) {
    out += `  'Boton_Alternar':\n    material: SPAWNER\n    slot: 45\n    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n    enchantments:\n      - DURABILITY;1\n    display_name: '&#FFAA00Ver Mob Drops y Spawners'\n    lore:\n      - '&8ᴄᴀᴍʙɪᴀʀ ᴄᴀᴛᴇɢᴏʀɪᴀ'\n      - ''\n      - ' &8| &fDestino: &#FFAA00Página 2 (Spawners)'\n      - ''\n      - '&7▶ Clic para alternar menú'\n    left_click_commands:\n      - '[openguimenu] ${targetMenu}'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;
  } else {
    out += `  'Boton_Alternar':\n    material: WHEAT\n    slot: 45\n    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n    enchantments:\n      - DURABILITY;1\n    display_name: '&#59E91FVer Cultivos y Cosechas'\n    lore:\n      - '&8ᴄᴀᴍʙɪᴀʀ ᴄᴀᴛᴇɢᴏʀɪᴀ'\n      - ''\n      - ' &8| &fDestino: &#59E91FPágina 1 (Cultivos)'\n      - ''\n      - '&7▶ Clic para alternar menú'\n    left_click_commands:\n      - '[openguimenu] ${targetMenu}'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;
  }

  // Slot 49: Volver
  out += `  'Boton_Volver':\n    material: DARK_OAK_DOOR\n    slot: 49\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&cVolver Atrás'\n    lore:\n      - '&7Regresar al mercado'\n    left_click_commands:\n      - '[openguimenu] mercado_comercio'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;

  // Slot 52: Venta Rápida (HOPPER)
  out += `  'Boton_SellGUI':\n    material: HOPPER\n    slot: 52\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&#59E91FVenta Rápida'\n    lore:\n      - '&8ᴠᴇɴᴛᴀ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀ'\n      - ''\n      - ' &fVende todo tu inventario'\n      - ' &fde forma instantánea.'\n      - ''\n      - '&7▶ Clic para abrir'\n    left_click_commands:\n      - '[close]'\n      - '[player] sellgui'\n      - '[sound] ENTITY_EXPERIENCE_ORB_PICKUP'\n\n`;

  // Slot 53: Tu Economía (head-%player_name%)
  out += `  'Info_Balance':\n    material: head-%player_name%\n    slot: 53\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&#FFF275Tu Economía'\n    lore:\n      - '&8Tu Economía'\n      - ''\n      - ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%'\n      - ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas%🔥'\n      - ' &8| &fZafiros: &#1E6BFF%thundercurrencys_zafiros%💎'\n      - ' &8| &fXP: &#D48BFF%player_level% LVL'\n      - ''\n      - '&7▶ Clic para más información'\n    left_click_commands:\n      - '[openguimenu] info_economia'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;

  // Cristales grises en la barra inferior (slots 46, 47, 48, 50, 51)
  out += `  'Marco_Bottom':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 46\n      - 47\n      - 48\n      - 50\n      - 51\n`;

  return out;
}

// 1. Generar lonja_venta.yml
fs.writeFileSync("creator/lab/lonja_venta.yml", generateCleanMenu(true, "&0&l|&r &0Mercado ▶ &8Cultivos &7[1/2]", 1, 2, page1Cultivos, "lonja_venta_2"));

// 2. Generar lonja_venta_2.yml
fs.writeFileSync("creator/lab/lonja_venta_2.yml", generateCleanMenu(true, "&0&l|&r &0Mercado ▶ &8Mob Drops &7[2/2]", 2, 2, page2MobDrops, "lonja_venta"));

// 3. Generar deluxemenus_objetosdeventa.yml
fs.writeFileSync("creator/lab/deluxemenus_objetosdeventa.yml", generateCleanMenu(false, "&0&l|&r &0Mercado ▶ &8Cultivos &7[1/2]", 1, 2, page1Cultivos, "objetosdeventa_2"));

// 4. Generar deluxemenus_objetosdeventa_2.yml
fs.writeFileSync("creator/lab/deluxemenus_objetosdeventa_2.yml", generateCleanMenu(false, "&0&l|&r &0Mercado ▶ &8Mob Drops &7[2/2]", 2, 2, page2MobDrops, "objetosdeventa"));

console.log("Los 4 menús actualizados con marcos de cristales grises en navbar superior e inferior.");
