const fs = require("fs");
const path = require("path");

const list = JSON.parse(fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/generated_menus_list.json", "utf8"));
let cfg = fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", "utf8");

list.forEach(m => {
  const entry = `  ${m}:\n    file: menusIA/${m}.yml\n`;
  if (!cfg.includes(`  ${m}:`)) {
    cfg += entry;
  }
});

fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", cfg, "utf8");
console.log("Registrados los menús en DeluxeMenus_config.yml.");
