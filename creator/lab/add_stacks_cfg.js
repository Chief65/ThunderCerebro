const fs = require("fs");

let cfg = fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", "utf8");

if (!cfg.includes("  compra_stacks:")) {
  cfg += "  compra_stacks:\n    file: menusIA/compra_stacks.yml\n";
  fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml", cfg, "utf8");
}
console.log("Registrado compra_stacks en DeluxeMenus_config.yml.");
