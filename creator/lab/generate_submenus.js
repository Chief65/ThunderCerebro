const fs = require("fs");
const path = require("path");

const rawDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/raw";
const outDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab";

// Definición canónica de las 7 categorías exclusivas de compra
const categories = [
  { id: "bloques", name: "Bloques", file: "bloques.yml", pages: 12 },
  { id: "comida", name: "Comida", file: "comida.yml", pages: 1 },
  { id: "equipo", name: "Equipo", file: "equipo.yml", pages: 1 },
  { id: "redstone", name: "Redstone", file: "redstone.yml", pages: 1 },
  { id: "misc", name: "Misceláneo", file: "miscellaneo.yml", pages: 1 },
  { id: "tintes", name: "Tintes", file: "tintes.yml", pages: 1 },
  { id: "banners", name: "Banners", file: "banners.yml", pages: 4 }
];

// Parser genérico de ítems de ShopGUIPlus
function parseShopItems(filePath) {
  const content = fs.readFileSync(filePath, "utf8");
  const lines = content.split("\n");
  const items = [];
  let current = null;
  let inItem = false;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const match = line.match(/^\s+(\d+):/);
    if (match) {
      if (current && current.material && current.type !== "dummy" && current.type !== "special") {
        items.push(current);
      }
      current = { rawId: match[1], page: 1 };
      inItem = true;
      continue;
    }
    if (!inItem || !current) continue;

    const mat = line.match(/material:\s*([A-Z0-9_]+)/);
    if (mat) current.material = mat[1];

    const name = line.match(/name:\s*["\x27]?([^"\x27\r\n]+)["\x27]?/);
    if (name) current.name = name[1];

    const buy = line.match(/buyPrice:\s*([-\d.]+)/);
    if (buy) current.buyPrice = parseFloat(buy[1]);

    const type = line.match(/type:\s*([a-zA-Z_]+)/);
    if (type) current.type = type[1];

    const page = line.match(/page:\s*(\d+)/);
    if (page) current.page = parseInt(page[1], 10);
  }
  if (current && current.material && current.type !== "dummy" && current.type !== "special") {
    items.push(current);
  }
  return items;
}

// Generador de Menú DeluxeMenus para categoría
function buildCategoryMenu(catId, catName, catIndex, pageNum, totalPages, itemsInPage) {
  const menuKey = totalPages > 1 ? (pageNum === 1 ? `compra_${catId}` : `compra_${catId}_${pageNum}`) : `compra_${catId}`;
  const title = `&0&l|&r &0Compra ▶ &8${catName} &7(${pageNum}/${totalPages})`;
  
  // Siguiente categoría para el ciclo de COMPARATOR
  const nextCat = categories[(catIndex + 1) % categories.length];
  const nextMenu = `compra_${nextCat.id}`;

  let out = `menu_title: '${title}'\n`;
  out += `open_command:\n`;
  out += `  - ${menuKey}\n`;
  out += `size: 45\nopen_requirement:\n  requirements: {}\nregister_command: true\nupdate: true\n\nitems:\n`;

  // Fila 1: Filtro superior paneles
  out += `  'Filtro_Top':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 0\n      - 1\n      - 2\n      - 3\n      - 4\n      - 5\n      - 6\n      - 7\n      - 8\n\n`;

  // Filas 2, 3, 4: Catálogo de ítems (Slots 9 a 35)
  for (let i = 0; i < itemsInPage.length; i++) {
    const it = itemsInPage[i];
    const slot = 9 + i;
    const cleanName = it.name ? it.name.replace(/^[#&][0-9a-fA-F]{6}/, '').replace(/^&[0-9a-fk-or]/, '') : it.material;
    const buyUnit = it.buyPrice > 0 ? it.buyPrice.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 }) : "10";
    const buyStack = it.buyPrice > 0 ? (it.buyPrice * 64).toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 }) : "640";

    out += `  'item_${i + 1}':\n`;
    out += `    material: ${it.material}\n`;
    out += `    slot: ${slot}\n`;
    out += `    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n`;
    out += `    display_name: '&#FFF275${cleanName}'\n`;
    out += `    lore:\n`;
    out += `      - '&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴄᴏᴍᴘʀᴀ'\n`;
    out += `      - ''\n`;
    out += `      - ' &8| &fUnidad: &#59E91F&l$&r&#59E91F${buyUnit}'\n`;
    out += `      - ' &8| &fStack x64: &#59E91F&l$&r&#59E91F${buyStack}'\n`;
    out += `      - ''\n`;
    out += `      - '&7▶ Click para comprar'\n`;
    out += `    left_click_commands:\n`;
    out += `      - '[sound] UI_BUTTON_CLICK'\n\n`;
  }

  // Si no se llenaron los 27 slots de items, rellenar con paneles grises
  if (itemsInPage.length < 27) {
    const emptySlots = [];
    for (let s = 9 + itemsInPage.length; s <= 35; s++) emptySlots.push(s);
    out += `  'Filtro_Items_Vacios':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n`;
    emptySlots.forEach(s => out += `      - ${s}\n`);
    out += `\n`;
  }

  // Fila 5 (Navbar):
  // Slot 36: Botón COMPARATOR (Filtro de Categoría)
  out += `  'Boton_Filtro':\n`;
  out += `    material: COMPARATOR\n`;
  out += `    slot: 36\n`;
  out += `    item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS\n`;
  out += `    enchantments:\n      - DURABILITY;1\n`;
  out += `    display_name: '&#FFF275Filtrar Categoría'\n`;
  out += `    lore:\n`;
  out += `      - '&8ᴇʟɪɢᴇ ᴄᴀᴛᴇɢᴏʀɪᴀ'\n`;
  out += `      - ''\n`;
  categories.forEach(c => {
    if (c.id === catId) {
      out += `      - ' &#FFF275● ${c.name}'\n`;
    } else {
      out += `      - ' &7● ${c.name}'\n`;
    }
  });
  out += `      - ''\n`;
  out += `      - '&7▶ Click para cambiar'\n`;
  out += `    left_click_commands:\n`;
  out += `      - '[openguimenu] ${nextMenu}'\n`;
  out += `      - '[sound] UI_BUTTON_CLICK'\n\n`;

  // Paneles de decoración en navbar: 37, 38, 42, 43
  out += `  'Filtro_Navbar_L':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 37\n      - 38\n\n`;

  // Paginación: Slot 39 Anterior, Slot 40 Volver, Slot 41 Siguiente
  if (totalPages > 1 && pageNum > 1) {
    const prevMenu = pageNum === 2 ? `compra_${catId}` : `compra_${catId}_${pageNum - 1}`;
    out += `  'Pagina_Anterior':\n    material: ARROW\n    slot: 39\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&#FFF275◀ Página Anterior'\n    lore:\n      - '&8| &fPágina: &7${pageNum}&8/&7${totalPages}'\n      - ''\n      - '&7▶ Click para retroceder'\n    left_click_commands:\n      - '[openguimenu] ${prevMenu}'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;
  } else {
    out += `  'Pagina_Anterior_Off':\n    material: GRAY_STAINED_GLASS_PANE\n    slot: 39\n    display_name: ' '\n\n`;
  }

  // Volver (Slot 40)
  out += `  'Boton_Volver':\n    material: DARK_OAK_DOOR\n    slot: 40\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&cVolver Atrás'\n    lore:\n      - '&7Regresar al menú anterior'\n    left_click_commands:\n      - '[openguimenu] mercado_dinero'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;

  if (totalPages > 1 && pageNum < totalPages) {
    const nextPgMenu = `compra_${catId}_${pageNum + 1}`;
    out += `  'Pagina_Siguiente':\n    material: ARROW\n    slot: 41\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&#FFF275Página Siguiente ▶'\n    lore:\n      - '&8| &fPágina: &7${pageNum}&8/&7${totalPages}'\n      - ''\n      - '&7▶ Click para avanzar'\n    left_click_commands:\n      - '[openguimenu] ${nextPgMenu}'\n      - '[sound] UI_BUTTON_CLICK'\n\n`;
  } else {
    out += `  'Pagina_Siguiente_Off':\n    material: GRAY_STAINED_GLASS_PANE\n    slot: 41\n    display_name: ' '\n\n`;
  }

  out += `  'Filtro_Navbar_R':\n    material: GRAY_STAINED_GLASS_PANE\n    display_name: ' '\n    slots:\n      - 42\n      - 43\n\n`;

  // Balance (Slot 44)
  out += `  'Info_Balance':\n    material: KELP\n    slot: 44\n    item_flags:\n      - HIDE_ATTRIBUTES\n    display_name: '&#FFF275Tu Economía'\n    lore:\n      - '&8Tu Economía'\n      - ''\n      - ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%'\n      - ''\n      - '&7▶ Click para más información'\n    left_click_commands:\n      - '[openguimenu] info_economia'\n      - '[sound] UI_BUTTON_CLICK'\n`;

  return { menuKey, out };
}

// Proceso principal
const generatedMenus = [];
for (let c = 0; c < categories.length; c++) {
  const cat = categories[c];
  const items = parseShopItems(path.join(rawDir, cat.file));
  console.log(`Categoria ${cat.name}: ${items.length} items leídos.`);

  const pageSize = 27;
  const totalPages = Math.max(1, Math.ceil(items.length / pageSize));

  for (let p = 1; p <= totalPages; p++) {
    const pageItems = items.slice((p - 1) * pageSize, p * pageSize);
    const { menuKey, out } = buildCategoryMenu(cat.id, cat.name, c, p, totalPages, pageItems);
    fs.writeFileSync(path.join(outDir, `${menuKey}.yml`), out, "utf8");
    generatedMenus.push(menuKey);
  }
}

console.log(`Total menús generados: ${generatedMenus.length}`);
fs.writeFileSync(path.join(outDir, "generated_menus_list.json"), JSON.stringify(generatedMenus, null, 2), "utf8");
