const fs = require("fs");
const path = require("path");

const labDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab";

// Balance para menus de 36 slots (slot 35): mercado_xp
const balance35 = `  'Info_Balance':
    material: head-%player_name%
    slot: 35
    item_flags:
      - HIDE_ATTRIBUTES
    display_name: '&#FFF275Tu Economía'
    lore:
      - '&8Tu Economía'
      - ''
      - ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%'
      - ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas%🔥'
      - ' &8| &fZafiros: &#1E6BFF%thundercurrencys_zafiros%💎'
      - ' &8| &fXP: &#D48BFF%player_level% LVL'
      - ''
      - '&7▶ Click para más información'
    left_click_commands:
      - '[openguimenu] info_economia'
      - '[sound] UI_BUTTON_CLICK'
`;

// Balance para menus de 45 slots (slot 44): xp_trims y xp_encantamientos
const balance44 = `  'Info_Balance':
    material: head-%player_name%
    slot: 44
    item_flags:
      - HIDE_ATTRIBUTES
    display_name: '&#FFF275Tu Economía'
    lore:
      - '&8Tu Economía'
      - ''
      - ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%'
      - ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas%🔥'
      - ' &8| &fZafiros: &#1E6BFF%thundercurrencys_zafiros%💎'
      - ' &8| &fXP: &#D48BFF%player_level% LVL'
      - ''
      - '&7▶ Click para más información'
    left_click_commands:
      - '[openguimenu] info_economia'
      - '[sound] UI_BUTTON_CLICK'
`;

// 1. mercado_xp.yml
let mxp = fs.readFileSync(path.join(labDir, "mercado_xp.yml"), "utf8");
mxp = mxp.replace(/  'Info_Balance':[\s\S]*?'Filtro_Navbar':/, `${balance35}\n  'Filtro_Navbar':`);
fs.writeFileSync(path.join(labDir, "mercado_xp.yml"), mxp, "utf8");
console.log("Actualizado mercado_xp.yml");

// 2. xp_trims.yml y xp_encantamientos.yml
["xp_trims.yml", "xp_encantamientos.yml"].forEach(f => {
  const filePath = path.join(labDir, f);
  let content = fs.readFileSync(filePath, "utf8");
  const idx = content.indexOf("  'Info_Balance':");
  if (idx !== -1) {
    content = content.substring(0, idx) + balance44;
    fs.writeFileSync(filePath, content, "utf8");
    console.log(`Actualizado ${f}`);
  }
});
