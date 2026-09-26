const fs = require('fs');
const sguipPath = 'raw/thunderia/ShopGUIPlus/config.yml';
let sguip = fs.readFileSync(sguipPath, 'utf8');

const correctLore = `shopItemLoreFormat:
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
    - "&8| &fVender todo por: &a%sell%"
  # This one to permissions
  permission:
    - "&8| &fPrecio: &a%buy%"
  # And this one to enchantments
  enchantment:
    - "&8| &fPrecio: &a%buy%"
  # And the last one to commands
  command:
    - "&8| &fPrecio: &a%buy%"`;

sguip = sguip.replace(/shopItemLoreFormat:[\s\S]*?(?=\r?\n# Logging settings|\r?\nlog:)/, correctLore);
fs.writeFileSync(sguipPath, sguip, 'utf8');
console.log('Fixed quotes in shopItemLoreFormat');
