const fs = require("fs");

const spawners = [
  { mat: "SPAWNER", name: "Spawner de Cerdo", price: "150", slot: 10, glow: false },
  { mat: "SPAWNER", name: "Spawner de Vaca", price: "300", slot: 11, glow: false },
  { mat: "SPAWNER", name: "Spawner de Zombie", price: "450", slot: 12, glow: false },
  { mat: "SPAWNER", name: "Spawner de Araña", price: "600", slot: 13, glow: false },
  { mat: "SPAWNER", name: "Spawner de Esqueleto", price: "800", slot: 14, glow: false },
  { mat: "SPAWNER", name: "Spawner de Blaze", price: "1,200", slot: 15, glow: false },
  { mat: "SPAWNER", name: "Spawner de Slime", price: "1,600", slot: 16, glow: false },
  { mat: "SPAWNER", name: "Spawner de Magma Cube", price: "2,000", slot: 19, glow: false }
];

const llaves = [
  { mat: "TRIPWIRE_HOOK", name: "x1 Llave Super", price: "100", slot: 11, glow: true },
  { mat: "TRIPWIRE_HOOK", name: "x1 Llave Rara", price: "400", slot: 12, glow: true },
  { mat: "TRIPWIRE_HOOK", name: "x1 Llave Gadgets", price: "600", slot: 13, glow: true },
  { mat: "TRIAL_KEY", name: "x1 Llave Mítica", price: "3,000", slot: 14, glow: true },
  { mat: "OMINOUS_TRIAL_KEY", name: "x1 Llave Limited", price: "10,000", slot: 15, glow: true }
];

const protecciones = [
  { mat: "COAL_ORE", name: "x1 Prote Carbón 8x8", price: "10", slot: 10, glow: true },
  { mat: "IRON_ORE", name: "x1 Prote Hierro 16x16", price: "100", slot: 11, glow: true },
  { mat: "GOLD_ORE", name: "x1 Prote Oro 32x32", price: "200", slot: 12, glow: true },
  { mat: "EMERALD_ORE", name: "x1 Prote Esmeralda 64x64", price: "500", slot: 13, glow: true },
  { mat: "DIAMOND_ORE", name: "x1 Prote Diamante 128x128", price: "1,000", slot: 14, glow: true },
  { mat: "ANCIENT_DEBRIS", name: "x1 Prote Netherite 256x256", price: "15,000", slot: 15, glow: true }
];

function buildAlmasMenu(key, catName, activeIndex, items, nextKey) {
  let out = `menu_title: '&0&l|&r &0Mercado ▶ &8${catName} &8(&#34B0F3🔥&8)'\n`;
  out += `open_command:\n`;
  out += `  - ${key}\n`;
  out += `size: 45\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n`;

  // Fila 1: Paneles decorativos
  out += `  'Filtro_Top':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 0\n      - 1\n      - 2\n      - 3\n      - 4\n      - 5\n      - 6\n      - 7\n      - 8\n\n`;

  // Ítems
  items.forEach((it, idx) => {
    out += `  'item_${idx + 1}':\n`;
    out += `    material: ${it.mat}\n`;
    out += `    slot: ${it.slot}\n`;
    out += `    item_flags:\n      - HIDE_ATTRIBUTES\n`;
    if (it.glow) {
      out += `      - HIDE_ENCHANTS\n    enchantments:\n      - DURABILITY;1\n`;
    }
    out += `    display_name: '&#FFF275${it.name}'\n`;
    out += `    lore:\n`;
    out += `      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴄᴀɴᴊᴇ'\n`;
    out += `      - ''\n`;
    out += `      - ' &8| &fPrecio: &#34B0F3${it.price} Almas (🔥)'\n`;
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
  const cats = ["Spawners", "Llaves", "Protecciones"];
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
  out += `  'Boton_Volver':\n    material: DARK_OAK_DOOR\n    slot: 40\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&cVolver Atrás'\n    lore:\n      - '&7Regresar a la selección de almas'\n    left_click_commands:\n      - '[openguimenu] tienda_almas_fija'\n      - '[sound] BLOCK_NOTE_BLOCK_BASS'\n\n`;

  // Balance (Slot 44)
  out += `  'Info_Balance':\n    material: SOUL_CAMPFIRE\n    slot: 44\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&#34B0F3Tus Almas'\n    lore:\n      - '&8Tu Economía'\n      - ''\n      - ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas% 🔥'\n      - ''\n      - '&7▶ Click para más información'\n    left_click_commands:\n      - '[openguimenu] info_economia'\n      - '[sound] UI_BUTTON_CLICK'\n`;

  return out;
}

const spYaml = buildAlmasMenu("almas_spawners", "Spawners", 0, spawners, "almas_llaves");
fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/almas_spawners.yml", spYaml, "utf8");

const llYaml = buildAlmasMenu("almas_llaves", "Llaves", 1, llaves, "almas_protecciones");
fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/almas_llaves.yml", llYaml, "utf8");

const prYaml = buildAlmasMenu("almas_protecciones", "Protecciones", 2, protecciones, "almas_spawners");
fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/almas_protecciones.yml", prYaml, "utf8");

console.log("Generados almas_spawners, almas_llaves, almas_protecciones con éxito.");
