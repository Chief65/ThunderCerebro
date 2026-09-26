const fs = require("fs");

const farmeoItems = [
  { mat: "CACTUS", name: "Cactus", base: 5, var: "+18%", dir: "▲", hist: "↗ ↗ ↗ ↗ ↗", txt1: "ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ", cons: "Vender", txt2: "ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ", color: "&#59E91F", glow: true },
  { mat: "SUGAR_CANE", name: "Caña de Azúcar", base: 3, var: "+16%", dir: "▲", hist: "↗ ↗ ↗ ↗ ↗", txt1: "ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ", cons: "Vender", txt2: "ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ", color: "&#59E91F", glow: true },
  { mat: "MELON", name: "Sandía (Bloque)", base: 7, var: "+14%", dir: "▲", hist: "↗ ↗ ↗ ↗ ↗", txt1: "ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ", cons: "Vender", txt2: "ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ", color: "&#59E91F", glow: true },
  { mat: "MELON_SLICE", name: "Rodaja de Sandía", base: 1, var: "+12%", dir: "▲", hist: "↗ ↗ ↗ ↗ ↗", txt1: "ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ", cons: "Vender", txt2: "ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ", color: "&#59E91F", glow: true },
  { mat: "COCOA_BEANS", name: "Granos de Cacao", base: 30, var: "+10%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "NETHER_WART", name: "Verruga del Nether", base: 20, var: "+8%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "WHEAT", name: "Trigo", base: 20, var: "+5%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "CARROT", name: "Zanahoria", base: 15, var: "+3%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "POTATO", name: "Patata", base: 15, var: "0%", dir: "=", hist: "→ → → → →", txt1: "ᴍᴇʀᴄᴀᴅᴏ ᴇꜱᴛᴀʙʟᴇ", cons: "Esperar", txt2: "ᴘʀᴇᴄɪᴏ ʀᴇɢᴜʟᴀʀ", color: "&7" },
  { mat: "PUMPKIN", name: "Calabaza", base: 7, var: "0%", dir: "=", hist: "→ → → → →", txt1: "ᴍᴇʀᴄᴀᴅᴏ ᴇꜱᴛᴀʙʟᴇ", cons: "Esperar", txt2: "ᴘʀᴇᴄɪᴏ ʀᴇɢᴜʟᴀʀ", color: "&7" },
  { mat: "CHORUS_FLOWER", name: "Flor del Chorus", base: 1, var: "0%", dir: "=", hist: "→ → → → →", txt1: "ᴍᴇʀᴄᴀᴅᴏ ᴇꜱᴛᴀʙʟᴇ", cons: "Esperar", txt2: "ᴘʀᴇᴄɪᴏ ʀᴇɢᴜʟᴀʀ", color: "&7" },
  { mat: "CHORUS_FRUIT", name: "Fruta del Chorus", base: 1, var: "-2%", dir: "▼", hist: "→ ↘ ↘ ↘ ↘", txt1: "ʙᴀᴊᴀᴅᴀ ʟᴇᴠᴇ", cons: "Monitorear", txt2: "ʀɪᴇꜱɢᴏ ᴅᴇ ᴄᴀɪᴅᴀ", color: "&#FF4D4D" },
  { mat: "BROWN_MUSHROOM", name: "Champiñón Marrón", base: 1, var: "-4%", dir: "▼", hist: "→ ↘ ↘ ↘ ↘", txt1: "ʙᴀᴊᴀᴅᴀ ʟᴇᴠᴇ", cons: "Monitorear", txt2: "ʀɪᴇꜱɢᴏ ᴅᴇ ᴄᴀɪᴅᴀ", color: "&#FF4D4D" },
  { mat: "RED_MUSHROOM", name: "Champiñón Rojo", base: 1, var: "-5%", dir: "▼", hist: "→ ↘ ↘ ↘ ↘", txt1: "ʙᴀᴊᴀᴅᴀ ʟᴇᴠᴇ", cons: "Monitorear", txt2: "ʀɪᴇꜱɢᴏ ᴅᴇ ᴄᴀɪᴅᴀ", color: "&#FF4D4D" },
  { mat: "SWEET_BERRIES", name: "Bayas Dulces", base: 7, var: "-8%", dir: "▼", hist: "→ ↘ ↘ ↘ ↘", txt1: "ᴄᴀɪᴅᴀ ᴄᴏɴᴛɪɴᴜᴀ", cons: "Guardar", txt2: "ᴇꜱᴘᴇʀᴀʀ ʀᴇʙᴏᴛᴇ", color: "&#FF4D4D" },
  { mat: "BEETROOT", name: "Remolacha", base: 20, var: "-12%", dir: "▼", hist: "→ ↘ ↘ ↘ ↘", txt1: "ᴄᴀɪᴅᴀ ᴄᴏɴᴛɪɴᴜᴀ", cons: "Guardar", txt2: "ᴇꜱᴘᴇʀᴀʀ ʀᴇʙᴏᴛᴇ", color: "&#FF4D4D" },
  { mat: "BAMBOO", name: "Bambú", base: 1, var: "-15%", dir: "▼", hist: "↘ ↘ ↘ ↘ ↘", txt1: "ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ", cons: "Guardar", txt2: "ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ", color: "&#FF4D4D" },
  { mat: "KELP", name: "Algas", base: 2, var: "-16%", dir: "▼", hist: "↘ ↘ ↘ ↘ ↘", txt1: "ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ", cons: "Guardar", txt2: "ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ", color: "&#FF4D4D" },
  { mat: "PUMPKIN_SEEDS", name: "Semillas de Calabaza", base: 1, var: "-18%", dir: "▼", hist: "↘ ↘ ↘ ↘ ↘", txt1: "ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ", cons: "Guardar", txt2: "ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ", color: "&#FF4D4D" },
  { mat: "MELON_SEEDS", name: "Semillas de Sandía", base: 1, var: "-19%", dir: "▼", hist: "↘ ↘ ↘ ↘ ↘", txt1: "ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ", cons: "Guardar", txt2: "ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ", color: "&#FF4D4D" },
  { mat: "BEETROOT_SEEDS", name: "Semillas de Remolacha", base: 1, var: "-20%", dir: "▼", hist: "↘ ↘ ↘ ↘ ↘", txt1: "ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ", cons: "Guardar", txt2: "ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ", color: "&#FF4D4D" },
  // 6 Mobs destacados para completar 27 slots de la Página 1:
  { mat: "BLAZE_ROD", name: "Vara de Blaze", base: 2, var: "+18%", dir: "▲", hist: "↗ ↗ ↗ ↗ ↗", txt1: "ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ", cons: "Vender", txt2: "ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ", color: "&#59E91F", glow: true },
  { mat: "GUNPOWDER", name: "Pólvora", base: 4, var: "+15%", dir: "▲", hist: "↗ ↗ ↗ ↗ ↗", txt1: "ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ", cons: "Vender", txt2: "ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ", color: "&#59E91F", glow: true },
  { mat: "ENDER_PEARL", name: "Perla de Ender", base: 5, var: "+12%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "LEATHER", name: "Cuero", base: 3, var: "+8%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "BONE", name: "Hueso", base: 4, var: "+4%", dir: "▲", hist: "→ ↗ ↗ ↗ ↗", txt1: "ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ", cons: "Vender", txt2: "ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ", color: "&#59E91F" },
  { mat: "WHEAT_SEEDS", name: "Semillas de Trigo", base: 1, var: "-20%", dir: "▼", hist: "↘ ↘ ↘ ↘ ↘", txt1: "ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ", cons: "Guardar", txt2: "ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ", color: "&#FF4D4D" }
];

console.log("Total Pagina 1:", farmeoItems.length);
