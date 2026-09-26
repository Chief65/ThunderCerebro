const fs = require("fs");
const path = require("path");

const list = JSON.parse(fs.readFileSync("C:/Users/tecno/Desktop/ThunderCerebro/creator/lab/generated_menus_list.json", "utf8"));
const labDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab";

list.forEach(m => {
  const filePath = path.join(labDir, `${m}.yml`);
  let content = fs.readFileSync(filePath, "utf8");
  
  // Reemplazar la acción del click para abrir compra_cantidad
  content = content.replace(/left_click_commands:\s*\n\s*-\s*'\s*\[sound\] UI_BUTTON_CLICK\s*'/g, "left_click_commands:\n      - '[openguimenu] compra_cantidad'\n      - '[sound] UI_BUTTON_CLICK'");
  
  fs.writeFileSync(filePath, content, "utf8");
});

console.log("Actualizados todos los 21 menús para apuntar a compra_cantidad.");
