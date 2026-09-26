const fs = require('fs');
const path = require('path');

// 1. Update DeluxeMenus files in creator/output/MenusIA
const dmDir = 'creator/output/MenusIA';
const dmTitles = {
    'tienda_principal.yml': '&0&l|&r &0Tienda ▶ &8Menu',
    'precios_farmeo.yml': '&0&l|&r &0Venta ▶ &8Cultivos',
    'precios_mobs.yml': '&0&l|&r &0Venta ▶ &8Mobs',
    'precios_especiales.yml': '&0&l|&r &0Venta ▶ &8Especiales'
};

Object.keys(dmTitles).forEach(f => {
    const p = path.join(dmDir, f);
    if (fs.existsSync(p)) {
        let content = fs.readFileSync(p, 'utf8');
        content = content.replace(/menu_title:\s*['"][^'"]+['"]/g, `menu_title: '${dmTitles[f]}'`);
        fs.writeFileSync(p, content, 'utf8');
        console.log(`Updated DM title in ${f} -> ${dmTitles[f]}`);
    }
});

// 2. Update ShopGUIPlus config.yml
const sguipConfig = 'raw/thunderia/ShopGUIPlus/config.yml';
let sguip = fs.readFileSync(sguipConfig, 'utf8');
sguip = sguip.replace(/shopMenuName:\s*["'][^"']+["']/g, 'shopMenuName: "&0&l|&r &0Tienda ▶ &8Categorias"');
fs.writeFileSync(sguipConfig, sguip, 'utf8');
console.log('Updated ShopGUIPlus shopMenuName -> &0&l|&r &0Tienda ▶ &8Categorias');

// 3. Update ShopGUIPlus lang.yml dialog titles
const sguipLang = 'raw/thunderia/ShopGUIPlus/lang.yml';
let lang = fs.readFileSync(sguipLang, 'utf8');
lang = lang.replace(/NAME:\s*['"]&0&l\|&r &0ThunderMC &0▶ &8Comprar['"]/g, "NAME: '&0&l|&r &0Tienda ▶ &8Comprar'");
lang = lang.replace(/NAME:\s*['"]&0&l\|&r &0ThunderMC &0▶ &8Vender['"]/g, "NAME: '&0&l|&r &0Tienda ▶ &8Vender'");
lang = lang.replace(/NAME:\s*['"]&0&l\|&r &0ThunderMC &0▶ &8Comprar Lotes['"]/g, "NAME: '&0&l|&r &0Tienda ▶ &8Lotes'");
lang = lang.replace(/NAME:\s*['"]&0&l\|&r &0ThunderMC &0▶ &8Vender Lotes['"]/g, "NAME: '&0&l|&r &0Tienda ▶ &8Lotes'");
fs.writeFileSync(sguipLang, lang, 'utf8');
console.log('Updated ShopGUIPlus lang.yml dialog titles.');

// 4. Update ShopGUIPlus shops subcategories titles
const shopsDir = 'raw/thunderia/ShopGUIPlus/shops';
const shopTitles = {
    'bloques.yml': '&0&l|&r &0Tienda ▶ &8Bloques',
    'comida.yml': '&0&l|&r &0Tienda ▶ &8Comida',
    'encantamientos.yml': '&0&l|&r &0Tienda ▶ &8Libros',
    'equipo.yml': '&0&l|&r &0Tienda ▶ &8Equipo',
    'farmeo.yml': '&0&l|&r &0Tienda ▶ &8Farmeo',
    'miscellaneo.yml': '&0&l|&r &0Tienda ▶ &8Misc',
    'mobs.yml': '&0&l|&r &0Tienda ▶ &8Mobs',
    'redstone.yml': '&0&l|&r &0Tienda ▶ &8Redstone',
    'tintes.yml': '&0&l|&r &0Tienda ▶ &8Tintes',
    'trims.yml': '&0&l|&r &0Tienda ▶ &8Trims',
    'venta.yml': '&0&l|&r &0Tienda ▶ &8Venta'
};

Object.keys(shopTitles).forEach(f => {
    const p = path.join(shopsDir, f);
    if (fs.existsSync(p)) {
        let content = fs.readFileSync(p, 'utf8');
        content = content.replace(/name:\s*["'][^"']+["']/g, `name: "${shopTitles[f]}"`);
        fs.writeFileSync(p, content, 'utf8');
        console.log(`Updated shop title in ${f} -> ${shopTitles[f]}`);
    }
});
