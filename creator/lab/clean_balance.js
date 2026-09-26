const fs = require("fs");
const path = require("path");

const labDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab";

const balanceBlock = `  'Info_Balance':
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

const files = ["almas_spawners.yml", "almas_llaves.yml", "almas_protecciones.yml"];

files.forEach(f => {
  const filePath = path.join(labDir, f);
  let content = fs.readFileSync(filePath, "utf8");
  
  // Cortar todo desde 'Info_Balance': hasta el final
  const idx = content.indexOf("  'Info_Balance':");
  if (idx !== -1) {
    content = content.substring(0, idx) + balanceBlock;
    fs.writeFileSync(filePath, content, "utf8");
    console.log(`Limpio y reemplazado en ${f}`);
  }
});
