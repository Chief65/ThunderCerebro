/**
 * Full Analysis Script — Plan Player Analytics Database
 * Análisis mensual exhaustivo del servidor Minecraft
 * 
 * Uso: node full_analysis.js [ruta_a_database.db]
 * 
 * Genera output en consola con todas las métricas y un archivo JSON
 * con los datos estructurados para el informe.
 * 
 * Métricas calculadas:
 * - Progresión semana a semana (nuevos, activos, sesiones, playtime, AFK)
 * - Retención semanal y global (bounce rate, distribución de sesiones/playtime)
 * - Rendimiento (TPS, MSPT, CPU, RAM, entidades, chunks)
 * - Concurrencia (pico, media, por día de semana, por hora)
 * - Top jugadores por playtime
 * - Stickiness (DAU/WAU)
 * - Churn (activos, riesgo, abandonados)
 * - Mundos, ping, versiones, direcciones de conexión
 * - Jugadores únicos diarios y registros diarios (tendencias)
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

// ============================================================
// CONFIGURACIÓN
// ============================================================
const DB_PATH = process.argv[2] || path.join(process.cwd(), 'database.db');
const OUTPUT_DIR = process.argv[3] || process.cwd();

console.log(`Base de datos: ${DB_PATH}`);
console.log(`Output: ${OUTPUT_DIR}`);

const db = new Database(DB_PATH, { readonly: true });

// ============================================================
// UTILIDADES
// ============================================================
function msToHours(ms) { return (ms / 3600000).toFixed(2); }
function msToMinutes(ms) { return (ms / 60000).toFixed(1); }
function pct(a, b) { return b === 0 ? '0.0' : ((a / b) * 100).toFixed(1); }
function pctChange(curr, prev) {
    return prev === 0 ? (curr > 0 ? '+∞' : '0.0') : (((curr - prev) / prev) * 100).toFixed(1);
}
function weekLabel(d) {
    const date = new Date(d);
    const day = date.getDate();
    const month = date.toLocaleString('es-ES', { month: 'short' });
    return `${day} ${month}`;
}

// ============================================================
// DEFINIR SEMANAS (Lunes a Domingo)
// ============================================================
const sessions = db.prepare(`SELECT MIN(session_start) as min_s, MAX(session_end) as max_s FROM plan_sessions`).get();
const DATA_START = sessions.min_s;
const DATA_END = sessions.max_s;

console.log(`\nRango de datos: ${new Date(DATA_START).toISOString()} → ${new Date(DATA_END).toISOString()}\n`);

const weeks = [];
let weekStart = new Date(DATA_START);
weekStart.setUTCHours(0, 0, 0, 0);
while (weekStart.getUTCDay() !== 1) weekStart.setUTCDate(weekStart.getUTCDate() - 1);

while (weekStart.getTime() < DATA_END) {
    const weekEnd = new Date(weekStart);
    weekEnd.setUTCDate(weekEnd.getUTCDate() + 7);
    weeks.push({
        start: weekStart.getTime(),
        end: Math.min(weekEnd.getTime(), DATA_END + 1),
        label: `${weekLabel(weekStart)} - ${weekLabel(Math.min(weekEnd.getTime() - 1, DATA_END))}`,
        days: Math.min(7, Math.ceil((Math.min(weekEnd.getTime(), DATA_END + 1) - weekStart.getTime()) / 86400000))
    });
    weekStart = weekEnd;
}

console.log(`Semanas analizadas: ${weeks.length}`);
weeks.forEach((w, i) => console.log(`  Semana ${i + 1}: ${w.label} (${w.days} días)`));

// ============================================================
// ANÁLISIS POR SEMANA
// ============================================================
const output = { weeks: [], totals: {}, daily: {}, retention: {}, top: [], worlds: [], versions: [], joinAddresses: [] };

// === TOTAL COUNTS ===
const totalUsers = db.prepare(`SELECT COUNT(*) as c FROM plan_users`).get().c;
const totalSessions = db.prepare(`SELECT COUNT(*) as c FROM plan_sessions`).get().c;
const totalKills = db.prepare(`SELECT COUNT(*) as c FROM plan_kills`).get().c;

output.totals = { totalUsers, totalSessions, totalKills };

console.log(`\n========================================`);
console.log(`TOTALES GLOBALES`);
console.log(`========================================`);
console.log(`Jugadores únicos registrados: ${totalUsers}`);
console.log(`Sesiones totales: ${totalSessions}`);
console.log(`Kills totales (PvP): ${totalKills}`);

// === JOIN ADDRESSES ===
console.log(`\n========================================`);
console.log(`DIRECCIONES DE CONEXIÓN`);
console.log(`========================================`);
const joinAddresses = db.prepare(`
    SELECT join_address, COUNT(*) as cnt 
    FROM plan_user_info 
    GROUP BY join_address 
    ORDER BY cnt DESC 
    LIMIT 15
`).all();
joinAddresses.forEach(j => {
    console.log(`  ${j.join_address}: ${j.cnt} jugadores (${pct(j.cnt, totalUsers)}%)`);
});
output.joinAddresses = joinAddresses;

// === PER-WEEK ANALYSIS ===
console.log(`\n========================================`);
console.log(`ANÁLISIS SEMANA A SEMANA`);
console.log(`========================================`);

for (let i = 0; i < weeks.length; i++) {
    const w = weeks[i];
    const prev = i > 0 ? output.weeks[i - 1] : null;

    console.log(`\n--- Semana ${i + 1}: ${w.label} ---`);

    // 1. NEW PLAYERS
    const newPlayers = db.prepare(`
        SELECT COUNT(*) as c FROM plan_users 
        WHERE registered >= ? AND registered < ?
    `).get(w.start, w.end).c;

    // 2. ACTIVE PLAYERS
    const activePlayers = db.prepare(`
        SELECT COUNT(DISTINCT user_id) as c FROM plan_sessions 
        WHERE session_start >= ? AND session_start < ?
    `).get(w.start, w.end).c;

    // 3. SESSIONS
    const sessionStats = db.prepare(`
        SELECT 
            COUNT(*) as total_sessions,
            SUM(session_end - session_start) as total_playtime_ms,
            AVG(session_end - session_start) as avg_session_ms,
            MAX(session_end - session_start) as max_session_ms,
            SUM(mob_kills) as mob_kills,
            SUM(deaths) as deaths,
            SUM(afk_time) as total_afk_ms
        FROM plan_sessions 
        WHERE session_start >= ? AND session_start < ?
    `).get(w.start, w.end);

    // 4. PEAK CONCURRENT
    const peakPlayers = db.prepare(`
        SELECT MAX(players_online) as peak FROM plan_tps 
        WHERE date >= ? AND date < ?
    `).get(w.start, w.end);

    // 5. AVG CONCURRENT (active hours)
    const avgPlayers = db.prepare(`
        SELECT AVG(players_online) as avg_on FROM plan_tps 
        WHERE date >= ? AND date < ? AND players_online > 0
    `).get(w.start, w.end);

    // 6. PERFORMANCE
    const perfStats = db.prepare(`
        SELECT 
            AVG(tps) as avg_tps, MIN(tps) as min_tps,
            AVG(mspt_average) as avg_mspt, AVG(mspt_95th_percentile) as avg_mspt_p95,
            AVG(cpu_usage) as avg_cpu, AVG(ram_usage) as avg_ram,
            AVG(entities) as avg_entities, AVG(chunks_loaded) as avg_chunks
        FROM plan_tps 
        WHERE date >= ? AND date < ?
    `).get(w.start, w.end);

    // 7. PvP KILLS
    const pvpKills = db.prepare(`
        SELECT COUNT(*) as c FROM plan_kills 
        WHERE date >= ? AND date < ?
    `).get(w.start, w.end).c;

    // 8. RETENTION
    let retention = 'N/A';
    let retentionNum = null;
    let retentionDen = null;
    if (i > 0) {
        const prevNewPlayers = db.prepare(`
            SELECT id FROM plan_users WHERE registered >= ? AND registered < ?
        `).all(weeks[i - 1].start, weeks[i - 1].end);

        if (prevNewPlayers.length > 0) {
            const prevNewIds = prevNewPlayers.map(p => p.id);
            const returned = db.prepare(`
                SELECT COUNT(DISTINCT user_id) as c FROM plan_sessions 
                WHERE session_start >= ? AND session_start < ?
                AND user_id IN (${prevNewIds.join(',')})
            `).get(w.start, w.end).c;
            retentionNum = returned;
            retentionDen = prevNewPlayers.length;
            retention = `${returned}/${prevNewPlayers.length} (${pct(returned, prevNewPlayers.length)}%)`;
        }
    }

    // 9. RETURNING PLAYERS
    const returningPlayers = db.prepare(`
        SELECT COUNT(DISTINCT s.user_id) as c 
        FROM plan_sessions s JOIN plan_users u ON s.user_id = u.id
        WHERE s.session_start >= ? AND s.session_start < ? AND u.registered < ?
    `).get(w.start, w.end, w.start).c;

    // 10. PEAK HOURS
    const hourDist = db.prepare(`
        SELECT CAST((session_start / 3600000 + 2) % 24 AS INTEGER) as hour, COUNT(*) as cnt
        FROM plan_sessions WHERE session_start >= ? AND session_start < ?
        GROUP BY hour ORDER BY hour
    `).all(w.start, w.end);
    const peakHours = [...hourDist].sort((a, b) => b.cnt - a.cnt).slice(0, 3);

    // Store
    const weekData = {
        label: w.label, days: w.days,
        newPlayers, activePlayers, returningPlayers,
        totalSessions: sessionStats.total_sessions,
        totalPlaytimeHours: parseFloat(msToHours(sessionStats.total_playtime_ms || 0)),
        avgSessionMinutes: parseFloat(msToMinutes(sessionStats.avg_session_ms || 0)),
        maxSessionHours: parseFloat(msToHours(sessionStats.max_session_ms || 0)),
        mobKills: sessionStats.mob_kills || 0,
        deaths: sessionStats.deaths || 0,
        totalAfkHours: parseFloat(msToHours(sessionStats.total_afk_ms || 0)),
        afkPct: parseFloat(pct(sessionStats.total_afk_ms || 0, sessionStats.total_playtime_ms || 1)),
        peakConcurrent: peakPlayers.peak || 0,
        avgConcurrent: parseFloat((avgPlayers.avg_on || 0).toFixed(1)),
        avgTps: parseFloat((perfStats.avg_tps || 0).toFixed(2)),
        minTps: parseFloat((perfStats.min_tps || 0).toFixed(2)),
        avgMspt: parseFloat((perfStats.avg_mspt || 0).toFixed(2)),
        avgMsptP95: parseFloat((perfStats.avg_mspt_p95 || 0).toFixed(1)),
        avgCpu: parseFloat((perfStats.avg_cpu || 0).toFixed(1)),
        avgRam: parseFloat((perfStats.avg_ram || 0).toFixed(0)),
        avgEntities: parseFloat((perfStats.avg_entities || 0).toFixed(0)),
        avgChunks: parseFloat((perfStats.avg_chunks || 0).toFixed(0)),
        pvpKills,
        retention, retentionNum, retentionDen,
        peakHours: peakHours.map(h => `${h.hour}:00 (${h.cnt} sesiones)`)
    };
    output.weeks.push(weekData);

    // Print
    console.log(`  Jugadores nuevos: ${newPlayers}${prev ? ` (${pctChange(newPlayers, prev.newPlayers)}% vs sem ant.)` : ''}`);
    console.log(`  Jugadores activos: ${activePlayers}${prev ? ` (${pctChange(activePlayers, prev.activePlayers)}% vs sem ant.)` : ''}`);
    console.log(`  Jugadores recurrentes: ${returningPlayers}`);
    console.log(`  Retención sem. anterior: ${retention}`);
    console.log(`  Sesiones totales: ${sessionStats.total_sessions}${prev ? ` (${pctChange(sessionStats.total_sessions, prev.totalSessions)}% vs sem ant.)` : ''}`);
    console.log(`  Tiempo total jugado: ${msToHours(sessionStats.total_playtime_ms || 0)} horas`);
    console.log(`  Sesión promedio: ${msToMinutes(sessionStats.avg_session_ms || 0)} min`);
    console.log(`  Sesión más larga: ${msToHours(sessionStats.max_session_ms || 0)} horas`);
    console.log(`  Tiempo AFK: ${msToHours(sessionStats.total_afk_ms || 0)} horas (${pct(sessionStats.total_afk_ms || 0, sessionStats.total_playtime_ms || 1)}% del playtime)`);
    console.log(`  Mob kills: ${sessionStats.mob_kills || 0} | Deaths: ${sessionStats.deaths || 0} | PvP kills: ${pvpKills}`);
    console.log(`  Pico concurrencia: ${peakPlayers.peak || 0} | Media: ${(avgPlayers.avg_on || 0).toFixed(1)}`);
    console.log(`  TPS medio: ${(perfStats.avg_tps || 0).toFixed(2)} | TPS mínimo: ${(perfStats.min_tps || 0).toFixed(2)}`);
    console.log(`  MSPT medio: ${(perfStats.avg_mspt || 0).toFixed(2)} | MSPT P95: ${(perfStats.avg_mspt_p95 || 0).toFixed(1)}`);
    console.log(`  CPU: ${(perfStats.avg_cpu || 0).toFixed(1)}% | RAM: ${(perfStats.avg_ram || 0).toFixed(0)} MB`);
    console.log(`  Entidades: ${(perfStats.avg_entities || 0).toFixed(0)} | Chunks: ${(perfStats.avg_chunks || 0).toFixed(0)}`);
    console.log(`  Horas pico: ${peakHours.map(h => `${h.hour}:00`).join(', ')}`);
}

// ============================================================
// RETENCIÓN GLOBAL
// ============================================================
console.log(`\n========================================`);
console.log(`ANÁLISIS DE RETENCIÓN GLOBAL`);
console.log(`========================================`);

const oneSession = db.prepare(`
    SELECT COUNT(*) as c FROM (
        SELECT user_id, COUNT(*) as sess_count FROM plan_sessions GROUP BY user_id HAVING sess_count = 1
    )
`).get().c;
const multiSession = db.prepare(`
    SELECT COUNT(*) as c FROM (
        SELECT user_id, COUNT(*) as sess_count FROM plan_sessions GROUP BY user_id HAVING sess_count > 1
    )
`).get().c;
const totalActiveUsers = oneSession + multiSession;

console.log(`Bounce (1 sesión): ${oneSession} (${pct(oneSession, totalActiveUsers)}%)`);
console.log(`Retención (>1 sesión): ${multiSession} (${pct(multiSession, totalActiveUsers)}%)`);

const sessDistribution = db.prepare(`
    SELECT 
        CASE 
            WHEN sess_count = 1 THEN '1 sesión'
            WHEN sess_count BETWEEN 2 AND 5 THEN '2-5 sesiones'
            WHEN sess_count BETWEEN 6 AND 10 THEN '6-10 sesiones'
            WHEN sess_count BETWEEN 11 AND 25 THEN '11-25 sesiones'
            WHEN sess_count BETWEEN 26 AND 50 THEN '26-50 sesiones'
            WHEN sess_count BETWEEN 51 AND 100 THEN '51-100 sesiones'
            ELSE '100+ sesiones'
        END as bucket, COUNT(*) as players, MIN(sess_count) as sort_key
    FROM (SELECT user_id, COUNT(*) as sess_count FROM plan_sessions GROUP BY user_id)
    GROUP BY bucket ORDER BY sort_key
`).all();
console.log(`\nDistribución de sesiones:`);
sessDistribution.forEach(b => console.log(`  ${b.bucket}: ${b.players} (${pct(b.players, totalActiveUsers)}%)`));

const playtimeDist = db.prepare(`
    SELECT 
        CASE 
            WHEN total_time < 3600000 THEN '< 1 hora'
            WHEN total_time < 18000000 THEN '1-5 horas'
            WHEN total_time < 36000000 THEN '5-10 horas'
            WHEN total_time < 72000000 THEN '10-20 horas'
            WHEN total_time < 180000000 THEN '20-50 horas'
            ELSE '50+ horas'
        END as bucket, COUNT(*) as players, MIN(total_time) as sort_key
    FROM (SELECT user_id, SUM(session_end - session_start) as total_time FROM plan_sessions GROUP BY user_id)
    GROUP BY bucket ORDER BY sort_key
`).all();
console.log(`\nDistribución de playtime:`);
playtimeDist.forEach(b => console.log(`  ${b.bucket}: ${b.players} (${pct(b.players, totalActiveUsers)}%)`));

output.retention = {
    bounce: oneSession, bouncePct: parseFloat(pct(oneSession, totalActiveUsers)),
    retained: multiSession, retainedPct: parseFloat(pct(multiSession, totalActiveUsers)),
    sessDistribution, playtimeDist
};

// ============================================================
// TOP 15 JUGADORES
// ============================================================
console.log(`\n========================================`);
console.log(`TOP 15 JUGADORES POR PLAYTIME`);
console.log(`========================================`);
const topPlaytime = db.prepare(`
    SELECT u.name, COUNT(*) as sessions, 
           SUM(s.session_end - s.session_start) as total_ms,
           SUM(s.mob_kills) as kills, SUM(s.deaths) as deaths
    FROM plan_sessions s JOIN plan_users u ON s.user_id = u.id
    GROUP BY u.id ORDER BY total_ms DESC LIMIT 15
`).all();
topPlaytime.forEach((p, i) =>
    console.log(`  ${i + 1}. ${p.name}: ${msToHours(p.total_ms)}h (${p.sessions} ses, ${p.kills} mob kills, ${p.deaths} deaths)`)
);
output.top = topPlaytime.map(p => ({
    ...p, totalHours: parseFloat(msToHours(p.total_ms))
}));

// ============================================================
// CONCURRENCIA POR DÍA DE LA SEMANA
// ============================================================
console.log(`\n========================================`);
console.log(`CONCURRENCIA POR DÍA DE LA SEMANA`);
console.log(`========================================`);
const dayNames = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
const byDay = db.prepare(`
    SELECT CAST((date / 86400000 + 4) % 7 AS INTEGER) as dow,
           AVG(players_online) as avg_on, MAX(players_online) as peak
    FROM plan_tps WHERE players_online > 0 GROUP BY dow ORDER BY dow
`).all();
byDay.forEach(d => console.log(`  ${dayNames[d.dow]}: Media ${d.avg_on.toFixed(1)} | Pico ${d.peak}`));

// ============================================================
// JUGADORES ÚNICOS DIARIOS
// ============================================================
console.log(`\n========================================`);
console.log(`JUGADORES ÚNICOS DIARIOS`);
console.log(`========================================`);
const dailyUnique = db.prepare(`
    SELECT CAST(session_start / 86400000 AS INTEGER) as day_epoch,
           COUNT(DISTINCT user_id) as unique_players, COUNT(*) as sessions
    FROM plan_sessions GROUP BY day_epoch ORDER BY day_epoch
`).all();
dailyUnique.forEach(d => {
    const date = new Date(d.day_epoch * 86400000);
    console.log(`  ${date.toISOString().split('T')[0]}: ${d.unique_players} únicos, ${d.sessions} sesiones`);
});
output.daily.uniquePlayers = dailyUnique.map(d => ({
    date: new Date(d.day_epoch * 86400000).toISOString().split('T')[0],
    uniquePlayers: d.unique_players, sessions: d.sessions
}));

// ============================================================
// REGISTROS DIARIOS
// ============================================================
console.log(`\n========================================`);
console.log(`REGISTROS DIARIOS`);
console.log(`========================================`);
const dailyRegs = db.prepare(`
    SELECT CAST(registered / 86400000 AS INTEGER) as day_epoch, COUNT(*) as new_players
    FROM plan_users GROUP BY day_epoch ORDER BY day_epoch
`).all();
dailyRegs.forEach(d => {
    const date = new Date(d.day_epoch * 86400000);
    console.log(`  ${date.toISOString().split('T')[0]}: ${d.new_players} nuevos`);
});
output.daily.registrations = dailyRegs.map(d => ({
    date: new Date(d.day_epoch * 86400000).toISOString().split('T')[0],
    newPlayers: d.new_players
}));

// ============================================================
// PING
// ============================================================
console.log(`\n========================================`);
console.log(`ANÁLISIS DE PING`);
console.log(`========================================`);
try {
    const pingStats = db.prepare(`
        SELECT AVG(min_ping) as avg_min, AVG(max_ping) as avg_max,
               AVG((min_ping + max_ping) / 2.0) as avg_ping,
               COUNT(DISTINCT user_id) as players
        FROM plan_ping
    `).get();
    if (pingStats.avg_ping) {
        console.log(`  Ping medio: ${pingStats.avg_ping.toFixed(0)} ms`);
        console.log(`  Ping mín medio: ${pingStats.avg_min.toFixed(0)} ms`);
        console.log(`  Ping máx medio: ${pingStats.avg_max.toFixed(0)} ms`);
        console.log(`  Jugadores con datos: ${pingStats.players}`);
    }
} catch (e) { console.log(`  Tabla de ping no disponible`); }

// ============================================================
// MUNDOS
// ============================================================
console.log(`\n========================================`);
console.log(`MUNDOS Y TIEMPO POR MUNDO`);
console.log(`========================================`);
try {
    const worldStats = db.prepare(`
        SELECT w.world_name,
               SUM(wt.survival_time) as surv, SUM(wt.creative_time) as crea,
               SUM(wt.adventure_time) as adv, SUM(wt.spectator_time) as spec,
               COUNT(DISTINCT wt.user_id) as players
        FROM plan_world_times wt JOIN plan_worlds w ON wt.world_id = w.id
        GROUP BY w.world_name ORDER BY surv DESC
    `).all();
    worldStats.forEach(ws => {
        const total = ws.surv + ws.crea + ws.adv + ws.spec;
        console.log(`  ${ws.world_name}: ${msToHours(total)}h (${ws.players} jugadores)`);
        console.log(`    Surv: ${msToHours(ws.surv)}h | Crea: ${msToHours(ws.crea)}h | Adv: ${msToHours(ws.adv)}h | Spec: ${msToHours(ws.spec)}h`);
    });
    output.worlds = worldStats;
} catch (e) { console.log(`  Tabla de mundos no disponible`); }

// ============================================================
// VERSIONES
// ============================================================
console.log(`\n========================================`);
console.log(`DISTRIBUCIÓN DE VERSIONES`);
console.log(`========================================`);
try {
    const versionDist = db.prepare(`
        SELECT protocol_version, COUNT(*) as cnt 
        FROM plan_version_protocol GROUP BY protocol_version ORDER BY cnt DESC
    `).all();
    const protocolMap = {
        766: '1.21.1', 767: '1.21.2-1.21.4', 768: '1.21.5',
        769: '1.21.6', 770: '1.21.7-1.21.8', 771: '1.21.9-1.21.10',
        772: '1.21.11', 773: '1.21.12', 774: '1.21.13', 775: '1.21.14',
        776: '1.21.15', 765: '1.21.0', 764: '1.20.5-1.20.6',
        763: '1.20.4', 47: '1.8.x'
    };
    versionDist.forEach(v => {
        const mcVer = protocolMap[v.protocol_version] || `protocol ${v.protocol_version}`;
        console.log(`  ${mcVer} (${v.protocol_version}): ${v.cnt} jugadores (${pct(v.cnt, totalUsers)}%)`);
    });
    output.versions = versionDist;
} catch (e) { console.log(`  Tabla de versiones no disponible`); }

// ============================================================
// CRECIMIENTO
// ============================================================
console.log(`\n========================================`);
console.log(`MÉTRICAS DE CRECIMIENTO`);
console.log(`========================================`);
const fullWeeks = output.weeks.filter(w => w.days >= 6);
if (fullWeeks.length >= 2) {
    const avgNewPerWeek = fullWeeks.reduce((s, w) => s + w.newPlayers, 0) / fullWeeks.length;
    const avgActivePerWeek = fullWeeks.reduce((s, w) => s + w.activePlayers, 0) / fullWeeks.length;
    const avgSessionsPerWeek = fullWeeks.reduce((s, w) => s + w.totalSessions, 0) / fullWeeks.length;
    const avgPlaytimePerWeek = fullWeeks.reduce((s, w) => s + w.totalPlaytimeHours, 0) / fullWeeks.length;

    console.log(`  Media nuevos/semana: ${avgNewPerWeek.toFixed(1)}`);
    console.log(`  Media activos/semana: ${avgActivePerWeek.toFixed(1)}`);
    console.log(`  Media sesiones/semana: ${avgSessionsPerWeek.toFixed(0)}`);
    console.log(`  Media playtime/semana: ${avgPlaytimePerWeek.toFixed(1)} horas`);

    const halfIdx = Math.floor(fullWeeks.length / 2);
    if (halfIdx > 0) {
        const firstHalf = fullWeeks.slice(0, halfIdx);
        const secondHalf = fullWeeks.slice(halfIdx);
        const fhNew = firstHalf.reduce((s, w) => s + w.newPlayers, 0) / firstHalf.length;
        const shNew = secondHalf.reduce((s, w) => s + w.newPlayers, 0) / secondHalf.length;
        const fhActive = firstHalf.reduce((s, w) => s + w.activePlayers, 0) / firstHalf.length;
        const shActive = secondHalf.reduce((s, w) => s + w.activePlayers, 0) / secondHalf.length;

        console.log(`\n  Tendencia nuevos: ${fhNew.toFixed(1)} → ${shNew.toFixed(1)} (${pctChange(shNew, fhNew)}%)`);
        console.log(`  Tendencia activos: ${fhActive.toFixed(1)} → ${shActive.toFixed(1)} (${pctChange(shActive, fhActive)}%)`);
    }

    console.log(`\n  === PROYECCIÓN MES SIGUIENTE ===`);
    console.log(`  Estimado nuevos (4 sem): ${(avgNewPerWeek * 4).toFixed(0)}`);
    console.log(`  Total acumulado estimado: ${(totalUsers + avgNewPerWeek * 4).toFixed(0)}`);
}

// ============================================================
// STICKINESS (DAU/WAU)
// ============================================================
console.log(`\n========================================`);
console.log(`STICKINESS (DAU/WAU)`);
console.log(`========================================`);
for (let i = 0; i < weeks.length; i++) {
    const w = weeks[i];
    const wau = output.weeks[i].activePlayers;
    const dailyActives = db.prepare(`
        SELECT CAST(session_start / 86400000 AS INTEGER) as d, COUNT(DISTINCT user_id) as dau
        FROM plan_sessions WHERE session_start >= ? AND session_start < ? GROUP BY d
    `).all(w.start, w.end);
    const avgDau = dailyActives.length > 0 ? dailyActives.reduce((s, d) => s + d.dau, 0) / dailyActives.length : 0;
    const stickiness = wau > 0 ? (avgDau / wau * 100).toFixed(1) : '0';
    output.weeks[i].avgDau = parseFloat(avgDau.toFixed(1));
    output.weeks[i].stickiness = parseFloat(stickiness);
    console.log(`  Semana ${i + 1}: DAU ${avgDau.toFixed(1)} / WAU ${wau} = ${stickiness}%`);
}

// ============================================================
// CHURN
// ============================================================
console.log(`\n========================================`);
console.log(`ANÁLISIS DE CHURN`);
console.log(`========================================`);
const sevenDaysAgo = DATA_END - (7 * 86400000);
const fourteenDaysAgo = DATA_END - (14 * 86400000);

const recentlyActive = db.prepare(`
    SELECT COUNT(DISTINCT user_id) as c FROM plan_sessions WHERE session_end >= ?
`).get(sevenDaysAgo).c;
const churnedRecently = db.prepare(`
    SELECT COUNT(*) as c FROM (
        SELECT user_id, MAX(session_end) as last_seen FROM plan_sessions
        GROUP BY user_id HAVING last_seen < ? AND last_seen >= ?
    )
`).get(sevenDaysAgo, fourteenDaysAgo).c;
const churnedOld = db.prepare(`
    SELECT COUNT(*) as c FROM (
        SELECT user_id, MAX(session_end) as last_seen FROM plan_sessions
        GROUP BY user_id HAVING last_seen < ?
    )
`).get(fourteenDaysAgo).c;

console.log(`  Activos últimos 7 días: ${recentlyActive}`);
console.log(`  Riesgo churn (7-14 días): ${churnedRecently}`);
console.log(`  Churned (>14 días): ${churnedOld}`);
console.log(`  Tasa retención 7d: ${pct(recentlyActive, totalActiveUsers)}%`);

output.churn = { recentlyActive, churnedRecently, churnedOld, totalActiveUsers };

// ============================================================
// GUARDAR JSON
// ============================================================
const jsonPath = path.join(OUTPUT_DIR, 'analysis_output.json');
fs.writeFileSync(jsonPath, JSON.stringify(output, null, 2));
console.log(`\nDatos exportados a: ${jsonPath}`);

db.close();
console.log("\n=== FIN DEL ANÁLISIS ===");
