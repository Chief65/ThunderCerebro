const fs = require("fs");

let cfg = fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", "utf8");

const xpMenus = [
  { key: "xp_trims", file: "menusIA/xp_trims.yml" },
  { key: "xp_encantamientos", file: "menusIA/xp_encantamientos.yml" }
];

xpMenus.forEach(m => {
  if (!cfg.includes(`  ${m.key}:`)) {
    cfg += `  ${m.key}:\n    file: ${m.file}\n`;
    console.log(`Añadido ${m.key}`);
  }
});

fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", cfg, "utf8");
