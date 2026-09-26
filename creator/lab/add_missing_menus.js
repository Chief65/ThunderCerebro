const fs = require("fs");

let cfg = fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", "utf8");

const missing = [
  { key: "tienda_almas_fija", file: "menusIA/tienda_almas_fija.yml" },
  { key: "night_market", file: "menusIA/night_market.yml" },
  { key: "nightmarket_premios", file: "menusIA/nightmarket_premios.yml" }
];

missing.forEach(m => {
  if (!cfg.includes(`  ${m.key}:`)) {
    cfg += `  ${m.key}:\n    file: ${m.file}\n`;
    console.log(`Añadido ${m.key}`);
  }
});

fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", cfg, "utf8");
