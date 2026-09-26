/**
 * Schema Discovery Script — Plan Player Analytics Database
 * 
 * Propósito: Descubrir la estructura de la base de datos Plan antes del análisis.
 * Uso: node schema_discovery.js [ruta_a_database.db]
 * 
 * Si no se proporciona ruta, busca database.db en el directorio actual.
 */

const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = process.argv[2] || path.join(__dirname, '..', '..', 'database.db');
console.log(`Abriendo base de datos: ${DB_PATH}`);

const db = new Database(DB_PATH, { readonly: true });

// ============================================================
// 1. SCHEMA DISCOVERY
// ============================================================
console.log("\n=== SCHEMA DE LA BASE DE DATOS ===\n");
const tables = db.prepare("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").all();
console.log("Tablas encontradas:", tables.map(t => t.name).join(', '));

for (const table of tables) {
    const cols = db.prepare(`PRAGMA table_info("${table.name}")`).all();
    const count = db.prepare(`SELECT COUNT(*) as c FROM "${table.name}"`).get();
    console.log(`\n--- ${table.name} (${count.c} filas) ---`);
    cols.forEach(c => console.log(`  ${c.name} (${c.type})`));
}

// ============================================================
// 2. IDENTIFY KEY TABLES
// ============================================================
console.log("\n\n=== TABLAS CLAVE ===");
const sessionTables = tables.filter(t => t.name.toLowerCase().includes('session'));
const userTables = tables.filter(t => t.name.toLowerCase().includes('user'));
const tpsTables = tables.filter(t => t.name.toLowerCase().includes('tps'));
const worldTables = tables.filter(t => t.name.toLowerCase().includes('world'));
const killTables = tables.filter(t => t.name.toLowerCase().includes('kill'));
const pingTables = tables.filter(t => t.name.toLowerCase().includes('ping'));

console.log("Sesiones:", sessionTables.map(t => t.name));
console.log("Usuarios:", userTables.map(t => t.name));
console.log("TPS:", tpsTables.map(t => t.name));
console.log("Mundos:", worldTables.map(t => t.name));
console.log("Kills:", killTables.map(t => t.name));
console.log("Ping:", pingTables.map(t => t.name));

// ============================================================
// 3. SAMPLE DATA FROM KEY TABLES
// ============================================================
console.log("\n\n=== MUESTRAS DE DATOS CLAVE ===");
const keyTables = ['plan_sessions', 'plan_users', 'plan_user_info', 'plan_tps', 'plan_kills', 'plan_ping'];
for (const tname of keyTables) {
    try {
        const sample = db.prepare(`SELECT * FROM "${tname}" LIMIT 3`).all();
        console.log(`\n--- Muestra de ${tname} ---`);
        console.log(JSON.stringify(sample, null, 2));
    } catch (e) {
        console.log(`Tabla ${tname} no encontrada: ${e.message}`);
    }
}

// ============================================================
// 4. DATE RANGES
// ============================================================
console.log("\n\n=== RANGOS TEMPORALES ===");
for (const table of tables) {
    const cols = db.prepare(`PRAGMA table_info("${table.name}")`).all();
    const timeCols = cols.filter(c =>
        c.name.toLowerCase().includes('date') ||
        c.name.toLowerCase().includes('time') ||
        c.name.toLowerCase().includes('session_start') ||
        c.name.toLowerCase().includes('session_end') ||
        c.name.toLowerCase().includes('registered')
    );
    for (const col of timeCols) {
        try {
            const range = db.prepare(`SELECT MIN("${col.name}") as min_val, MAX("${col.name}") as max_val FROM "${table.name}"`).get();
            if (range.min_val) {
                const minDate = new Date(Number(range.min_val));
                const maxDate = new Date(Number(range.max_val));
                if (minDate.getFullYear() > 2020 && minDate.getFullYear() < 2035) {
                    console.log(`${table.name}.${col.name}: ${minDate.toISOString()} → ${maxDate.toISOString()}`);
                } else {
                    console.log(`${table.name}.${col.name}: ${range.min_val} → ${range.max_val} (raw)`);
                }
            }
        } catch (e) { /* skip */ }
    }
}

db.close();
console.log("\n=== FIN DEL DESCUBRIMIENTO ===");
