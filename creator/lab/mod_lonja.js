const fs = require('fs');
let c = fs.readFileSync('creator/lab/lonja_venta.yml', 'utf8');

c = c.replace(/ &8\| &fU: /g, ' &8| &fUnidad: ');
c = c.replace(/\s+- ' &8\| &fTrend:[^\r\n]*\r?\n\s+- ' &8\| &fAccion:[^\r\n]*\r?\n\s+- ''/g, '');
c = c.replace(/   &8&o\(ᴅᴇᴠᴀʟᴜᴀᴄɪᴏɴ: ʜᴀꜱᴛᴀ -15%\)/g, ' &8&o(ᴅᴇᴠᴀʟᴜᴀᴄɪᴏɴ: ʜᴀꜱᴛᴀ -15%)');
c = c.replace(/\s+- '&7▶ Click Izq: Vender todo'\r?\n\s+- '&7▶ Click Der: Vender x64'/g, " \n - &7▶ Click para vender \);

fs.writeFileSync('creator/lab/lonja_venta.yml', c, 'utf8');
console.log('Finished updating lonja_venta.yml');
