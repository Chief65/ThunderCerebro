const fs = require("fs");

let cfg = fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", "utf8");

const almasMenus = [
  { key: "almas_spawners", file: "menusIA/almas_spawners.yml" },
  { key: "almas_llaves", file: "menusIA/almas_llaves.yml" },
  { key: "almas_protecciones", file: "menusIA/almas_protecciones.yml" }
];

almasMenus.forEach(m => {
  if (!cfg.includes(`  ${m.key}:`)) {
    cfg += `  ${m.key}:\n    file: ${m.file}\n`;
    console.log(`Añadido ${m.key}`);
  }
});

fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", cfg, "utf8");
