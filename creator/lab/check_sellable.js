const fs = require("fs");
const path = require("path");

const files = ["farmeo.yml", "mobs.yml", "bloques.yml", "comida.yml", "equipo.yml", "miscellaneo.yml", "redstone.yml", "tintes.yml", "banners.yml"];
const dir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/raw";

const sellable = [];
const nonSellable = [];
const stats = {};

for (const file of files) {
  const content = fs.readFileSync(path.join(dir, file), "utf8");
  const lines = content.split("\n");
  let currentItem = null;
  let inItem = false;
  let shopName = file.replace(".yml", "");
  stats[shopName] = { total: 0, sellable: 0, buyOnly: 0 };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const itemMatch = line.match(/^\s+(\d+):/);
    if (itemMatch) {
      if (currentItem && currentItem.material) {
        processItem(currentItem, shopName);
      }
      currentItem = { id: itemMatch[1], shop: shopName };
      inItem = true;
      continue;
    }
    if (!inItem || !currentItem) continue;

    const matMatch = line.match(/material:\s*([A-Z0-9_]+)/);
    if (matMatch) currentItem.material = matMatch[1];

    const nameMatch = line.match(/name:\s*["\x27]?([^"\x27\r\n]+)["\x27]?/);
    if (nameMatch) currentItem.name = nameMatch[1];

    const buyMatch = line.match(/buyPrice:\s*([-\d.]+)/);
    if (buyMatch) currentItem.buyPrice = parseFloat(buyMatch[1]);

    const sellMatch = line.match(/sellPrice:\s*([-\d.]+)/);
    if (sellMatch) currentItem.sellPrice = parseFloat(sellMatch[1]);

    const typeMatch = line.match(/type:\s*([a-zA-Z_]+)/);
    if (typeMatch) currentItem.type = typeMatch[1];
  }
  if (currentItem && currentItem.material) {
    processItem(currentItem, shopName);
  }
}

function processItem(item, shop) {
  if (item.type === "dummy" || item.type === "special") return;
  if (!item.material) return;
  stats[shop].total++;
  if (item.sellPrice && item.sellPrice > 0) {
    stats[shop].sellable++;
    sellable.push(item);
  } else {
    stats[shop].buyOnly++;
    nonSellable.push(item);
  }
}

console.log("=== ESTADISTICAS POR TIENDA ===");
console.log(JSON.stringify(stats, null, 2));
console.log(`Total items con venta: ${sellable.length}`);
console.log("=== LISTA DE ITEMS CON VENTA ===");
sellable.forEach(s => console.log(`${s.shop}: ${s.material} (${s.name || ""}) -> buy: ${s.buyPrice}, sell: ${s.sellPrice}`));
