const fs = require("fs");

let cfg = fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", "utf8");

if (!cfg.includes("  compra_cantidad:")) {
  cfg += "  compra_cantidad:\n    file: menusIA/compra_cantidad.yml\n";
  fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", cfg, "utf8");
}
console.log("Registrado compra_cantidad en config.");
