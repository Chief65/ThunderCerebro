const fs = require("fs");

// 18 Trims
const trimsItems = [
  { mat: "SENTRY_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Sentry Armor Trim", price: "10", slot: 9 },
  { mat: "VEX_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Vex Armor Trim", price: "10", slot: 10 },
  { mat: "WILD_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Wild Armor Trim", price: "10", slot: 11 },
  { mat: "COAST_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Coast Armor Trim", price: "10", slot: 12 },
  { mat: "DUNE_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Dune Armor Trim", price: "10", slot: 13 },
  { mat: "WAYFINDER_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Wayfinder Armor Trim", price: "10", slot: 14 },
  { mat: "RAISER_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Raiser Armor Trim", price: "10", slot: 15 },
  { mat: "SHAPER_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Shaper Armor Trim", price: "10", slot: 16 },
  { mat: "HOST_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Host Armor Trim", price: "10", slot: 17 },
  { mat: "WARD_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Ward Armor Trim", price: "10", slot: 18 },
  { mat: "SILENCE_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Silence Armor Trim", price: "10", slot: 19 },
  { mat: "TIDE_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Tide Armor Trim", price: "10", slot: 20 },
  { mat: "SNOUT_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Snout Armor Trim", price: "10", slot: 21 },
  { mat: "RIB_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Rib Armor Trim", price: "10", slot: 22 },
  { mat: "EYE_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Eye Armor Trim", price: "10", slot: 23 },
  { mat: "SPIRE_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Spire Armor Trim", price: "10", slot: 24 },
  { mat: "FLOW_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Flow Armor Trim", price: "10", slot: 25 },
  { mat: "BOLT_ARMOR_TRIM_SMITHING_TEMPLATE", name: "Bolt Armor Trim", price: "10", slot: 26 }
];

// 9 Encantamientos
const encantamientosItems = [
  { mat: "ENCHANTED_BOOK", name: "Libro Reparación (Mending)", price: "50", slot: 9 },
  { mat: "ENCHANTED_BOOK", name: "Libro Infinidad (Infinity)", price: "50", slot: 10 },
  { mat: "ENCHANTED_BOOK", name: "Libro Irrompibilidad III", price: "50", slot: 11 },
  { mat: "ENCHANTED_BOOK", name: "Libro Protección IV", price: "50", slot: 12 },
  { mat: "ENCHANTED_BOOK", name: "Libro Filo V (Sharpness V)", price: "50", slot: 13 },
  { mat: "ENCHANTED_BOOK", name: "Libro Fortuna III", price: "50", slot: 14 },
  { mat: "ENCHANTED_BOOK", name: "Libro Botín III (Looting III)", price: "50", slot: 15 },
  { mat: "ENCHANTED_BOOK", name: "Libro Eficiencia V", price: "50", slot: 16 },
  { mat: "ENCHANTED_BOOK", name: "Libro Toque de Seda (Silk Touch)", price: "50", slot: 17 }
];

function buildXpMenu(key, catName, activeIndex, items, nextKey) {
  let out = `menu_title: '&0&l|&r &0Mercado ▶ &8${catName} &8(&#D48BFF✦&8)'\n`;
  out += `open_command:\n`;
  out += `  - ${key}\n`;
  out += `size: 45\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n`;

  // Fila 1: Paneles decorativos
  out += `  'Filtro_Top':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 0\n      - 1\n      - 2\n      - 3\n      - 4\n      - 5\n      - 6\n      - 7\n      - 8\n\n`;

  // Items
  items.forEach((it, idx) => {
    out += `  'item_${idx + 1}':\n`;
    out += `    material: ${it.mat}\n`;
    out += `    slot: ${it.slot}\n`;
    out += `    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n`;
    out += `    display_name: '&#FFF275${it.name}'\n`;
    out += `    lore:\n`;
    out += `      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴄᴀɴᴊᴇ'\n`;
    out += `      - ''\n`;
    out += `      - ' &8| &fPrecio: &#D48BFF${it.price} Niveles (⭐)'\n`;
    out += `      - ''\n`;
    out += `      - '&7▶ Click para comprar'\n`;
    out += `    left_click_commands:\n`;
    out += `      - '[sound] UI_BUTTON_CLICK'\n\n`;
  });

  // Fila 5: Navbar
  // Slot 36: Comparador / Filtrador
  out += `  'Boton_Filtro':\n`;
  out += `    material: COMPARATOR\n`;
  out += `    slot: 36\n`;
  out += `    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n`;
  out += `    enchantments:\n      - DURABILITY;1\n`;
  out += `    display_name: '&#FFF275Filtrar Categoría'\n`;
  out += `    lore:\n`;
  out += `      - '&8ᴇʟɪɢᴇ ᴄᴀᴛᴇɢᴏʀɪᴀ'\n`;
  out += `      - ''\n`;
  const cats = ["Trims", "Encantamientos"];
  cats.forEach((c, idx) => {
    if (idx === activeIndex) {
      out += `      - ' &#FFF275● ${c}'\n`;
    } else {
      out += `      - ' &7● ${c}'\n`;
    }
  });
  out += `      - ''\n`;
  out += `      - '&7▶ Click para cambiar'\n`;
  out += `    left_click_commands:\n`;
  out += `      - '[openguimenu] ${nextKey}'\n`;
  out += `      - '[sound] UI_BUTTON_CLICK'\n\n`;

  // Paneles de decoración navbar
  out += `  'Filtro_Navbar':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 37\n      - 38\n      - 39\n      - 41\n      - 42\n      - 43\n\n`;

  // Volver (Slot 40)
  out += `  'Boton_Volver':\n    material: DARK_OAK_DOOR\n    slot: 40\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&cVolver Atrás'\n    lore:\n      - '&7Regresar a la selección de XP'\n    left_click_commands:\n      - '[openguimenu] mercado_xp'\n      - '[sound] BLOCK_NOTE_BLOCK_BASS'\n\n`;

  // Balance (Slot 44)
  out += `  'Info_Balance':\n    material: EXPERIENCE_BOTTLE\n    slot: 44\n    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n    enchantments:\n      - DURABILITY;1\n    display_name: '&#D48BFFTu Experiencia'\n    lore:\n      - '&8Tu Economía'\n      - ''\n      - ' &8| &fExperiencia: &#D48BFF%player_level% LVL DE XP'\n      - ''\n      - '&7▶ Click para más información'\n    left_click_commands:\n      - '[openguimenu] info_economia'\n      - '[sound] UI_BUTTON_CLICK'\n`;

  return out;
}

const trimsYaml = buildXpMenu("xp_trims", "Trims", 0, trimsItems, "xp_encantamientos");
fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/xp_trims.yml", trimsYaml, "utf8");

const encYaml = buildXpMenu("xp_encantamientos", "Encantamientos", 1, encantamientosItems, "xp_trims");
fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/xp_encantamientos.yml", encYaml, "utf8");

console.log("Generados xp_trims.yml y xp_encantamientos.yml con éxito.");
