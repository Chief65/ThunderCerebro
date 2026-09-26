const fs = require('fs');
const path = require('path');

const sguipPath = 'raw/thunderia/ShopGUIPlus/config.yml';
let sguip = fs.readFileSync(sguipPath, 'utf8');

const correctLore = `shopItemLoreFormat:
  # This lore will be applied to items
  item:
    - "&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴄᴏᴍᴘʀᴀ"
    - ""
    - " &8| &fPrecio: &#59E91F&l$&r&#59E91F%buy%"
    - ""
    - "&7▶ Click para comprar"
  # This lore will be applied to items in the buy GUI (when enableBuyGUI is set to true)
  itemBuyGUI:
    - "&8ᴄᴏᴍᴘʀᴀ ᴇɴ ᴄᴀɴᴛɪᴅᴀᴅ"
    - ""
    - " &8| &fCantidad: &e%amount%"
    - " &8| &fTotal: &#59E91F&l$&r&#59E91F%buy%"
  # This lore will be applied to items in the sell GUI (when enableSellGUI is set to true)
  itemSellGUI:
    - "&8ᴠᴇɴᴛᴀ ᴇɴ ᴄᴀɴᴛɪᴅᴀᴅ"
    - ""
    - " &8| &fCantidad: &e%amount%"
    - " &8| &fTotal: &#59E91F&l$&r&#59E91F%sell%"
  # This lore will be applied to the sell all button in the sell GUI (when enableSellGUI and enableSellGUISellAll are set to true)
  itemSellGUISellAll:
    - "&8| &fVender todo por: &#59E91F&l$&r&#59E91F%sell%"
  # This one to permissions
  permission:
    - "&8| &fPrecio: &#59E91F&l$&r&#59E91F%buy%"
  # And this one to enchantments
  enchantment:
    - "&8| &fPrecio: &#59E91F&l$&r&#59E91F%buy%"
  # And the last one to commands
  command:
    - "&8| &fPrecio: &#59E91F&l$&r&#59E91F%buy%"`;

sguip = sguip.replace(/shopItemLoreFormat:[\s\S]*?(?=\r?\n# Logging settings|\r?\nlog:)/, correctLore);
fs.writeFileSync(sguipPath, sguip, 'utf8');
console.log('Updated ShopGUIPlus shopItemLoreFormat with bold $ and reset regular number.');

// Update DeluxeMenus files
const dmFiles = [
    'creator/output/MenusIA/tienda_principal.yml',
    'creator/output/MenusIA/precios_farmeo.yml',
    'creator/output/MenusIA/precios_mobs.yml',
    'creator/output/MenusIA/precios_especiales.yml'
];

dmFiles.forEach(f => {
    if (fs.existsSync(f)) {
        let c = fs.readFileSync(f, 'utf8');
        // Update Dinero line
        c = c.replace(/ &8\| &fDinero: [^\r\n]+/g, ' &8| &fDinero: &#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%');
        // Update Almas line
        c = c.replace(/ &8\| &fAlmas: [^\r\n]+/g, ' &8| &fAlmas: &#34B0F3%thundercurrencys_almas%🔥');
        // Update Zafiros line to Premium Royal Blue &#1E6BFF with 💎
        c = c.replace(/ &8\| &fZafiros: [^\r\n]+/g, ' &8| &fZafiros: &#1E6BFF%thundercurrencys_zafiros%💎');
        fs.writeFileSync(f, c, 'utf8');
        console.log('Updated DM economy lore in:', f);
    }
});
