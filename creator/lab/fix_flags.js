const fs = require("fs");
const path = require("path");

const rawDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/raw";
const labDir = "C:/Users/tecno/Desktop/ThunderCerebro/creator/lab";
const files = ["warps.yml", "warps_minas.yml", "warps_dungeons.yml", "warps_rtp.yml"];

files.forEach(file => {
  let content = fs.readFileSync(path.join(rawDir, file), "utf8");
  
  // Reemplazar hide_attributes y hide_enchantments con item_flags
  const lines = content.split("\n");
  const newLines = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    if (/^\s*hide_attributes:\s*true/i.test(line)) {
      const indent = line.match(/^\s*/)[0];
      // Si la línea anterior o siguiente ya tiene item_flags, o si no tiene
      newLines.push(`${indent}item_flags:`);
      newLines.push(`${indent}  - HIDE_ATTRIBUTES`);
      continue;
    }
    
    if (/^\s*hide_enchantments:\s*true/i.test(line)) {
      const indent = line.match(/^\s*/)[0];
      // Si ya pusimos item_flags en la línea previa
      const lastLine = newLines[newLines.length - 1];
      if (lastLine && lastLine.includes("item_flags:")) {
        newLines.push(`${indent}  - HIDE_ENCHANTS`);
      } else if (lastLine && lastLine.includes("HIDE_ATTRIBUTES")) {
        newLines.push(`${indent}  - HIDE_ENCHANTS`);
      } else {
        newLines.push(`${indent}item_flags:`);
        newLines.push(`${indent}  - HIDE_ENCHANTS`);
      }
      continue;
    }
    
    newLines.push(line);
  }
  
  // Limpiar duplicados de item_flags si se generaron pegados
  let cleanContent = newLines.join("\n");
  cleanContent = cleanContent.replace(/item_flags:\s*\n\s*-\s*HIDE_ATTRIBUTES\s*\n\s*item_flags:\s*\n\s*-\s*HIDE_ENCHANTS/g, "item_flags:\n      - HIDE_ATTRIBUTES\n      - HIDE_ENCHANTS");
  
  fs.writeFileSync(path.join(labDir, file), cleanContent, "utf8");
  console.log(`Corregido ${file}`);
});
