const fs = require("fs");
const list = JSON.parse(fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/generated_menus_list.json", "utf8"));
let sftpBatch = "";

list.forEach(m => {
  sftpBatch += `put "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/${m}.yml" "plugins/DeluxeMenus/gui_menus/menusIA/${m}.yml"\n`;
});
sftpBatch += `put "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/compra_cantidad.yml" "plugins/DeluxeMenus/gui_menus/menusIA/compra_cantidad.yml"\n`;
sftpBatch += `put "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/DeluxeMenus_config.yml" "plugins/DeluxeMenus/config.yml"\n`;
sftpBatch += `exit\n`;

fs.writeFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/upload_batch_cantidad.txt", sftpBatch, "utf8");
console.log("Generado batch upload cantidad.");
