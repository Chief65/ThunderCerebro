const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = process.env.PORT || 3838;
const PUBLIC_DIR = path.join(__dirname, 'public');
const DATA_DIR = path.join(__dirname, 'data');

if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Datos iniciales de benchmark y telemetría de muestra
const DEFAULT_METRICS = {
    metadata: {
        serverName: "Thunder Survival 1.21.x",
        lastUpdated: new Date().toISOString(),
        networkMode: "Híbrido (Java + Bedrock Geyser / Premium + No-Premium)",
        region: "España & LATAM"
    },
    // Semáforos y KPIs principales
    kpis: {
        currentCcu: 184,
        peakCcuToday: 268,
        activePlayersMonth: 28450,
        newPlayersToday: 142,
        avgPlaytimeMinutes: 68.4,
        retentionD1: 28.5,    // %
        retentionD7: 11.2,    // %
        retentionD30: 4.8,    // %
        currentTps: 19.94,
        avgMspt: 31.8,        // ms
        monthlyRevenueEur: 2430.00,
        storeConversionRate: 1.85, // %
        arppuEur: 4.60
    },
    // Desglose por plataforma y tipo de cuenta
    platformBreakdown: {
        bedrockMobile: 46.5,
        javaNoPremium: 32.0,
        javaPremium: 15.5,
        bedrockConsole: 6.0
    },
    // Procedencia geográfica de los jugadores (%)
    geography: [
        { country: "México", share: 38.5, ccuAvg: 71 },
        { country: "España", share: 22.0, ccuAvg: 40 },
        { country: "Argentina", share: 15.2, ccuAvg: 28 },
        { country: "Colombia", share: 11.8, ccuAvg: 22 },
        { country: "Chile", share: 7.0, ccuAvg: 13 },
        { country: "Otros LATAM", share: 5.5, ccuAvg: 10 }
    ],
    // Histórico de 7 días (Nuevos vs Concurrentes vs MSPT)
    weeklyTrend: [
        { day: "Lunes", newPlayers: 110, peakCcu: 210, avgMspt: 29.4, revenue: 290 },
        { day: "Martes", newPlayers: 98, peakCcu: 195, avgMspt: 28.1, revenue: 215 },
        { day: "Miércoles", newPlayers: 135, peakCcu: 240, avgMspt: 33.2, revenue: 340 },
        { day: "Jueves", newPlayers: 122, peakCcu: 225, avgMspt: 30.5, revenue: 280 },
        { day: "Viernes", newPlayers: 180, peakCcu: 295, avgMspt: 36.8, revenue: 510 },
        { day: "Sábado", newPlayers: 245, peakCcu: 340, avgMspt: 41.2, revenue: 680 },
        { day: "Domingo", newPlayers: 210, peakCcu: 315, avgMspt: 38.4, revenue: 590 }
    ],
    // Cohortes de retención (Curva de vida)
    retentionCurve: [
        { day: "Día 1 (24h)", actual: 28.5, benchmarkMin: 20.0, benchmarkOptimal: 25.0 },
        { day: "Día 3 (72h)", actual: 18.2, benchmarkMin: 12.0, benchmarkOptimal: 16.0 },
        { day: "Día 7 (1 sem)", actual: 11.2, benchmarkMin: 7.0, benchmarkOptimal: 10.0 },
        { day: "Día 14 (2 sem)", actual: 7.5, benchmarkMin: 4.5, benchmarkOptimal: 7.0 },
        { day: "Día 30 (1 mes)", actual: 4.8, benchmarkMin: 2.5, benchmarkOptimal: 4.0 }
    ],
    // Métodos de pago en tienda
    paymentMethods: [
        { method: "Mercado Pago (LATAM)", share: 44.0, volumeEur: 1069.20 },
        { method: "OXXO / Efectivo (México)", share: 23.5, volumeEur: 571.05 },
        { method: "PayPal / Tarjetas Internacionales", share: 22.0, volumeEur: 534.60 },
        { method: "Pago Fácil / Rapipago (Argentina)", share: 6.5, volumeEur: 157.95 },
        { method: "Otros métodos locales", share: 4.0, volumeEur: 97.20 }
    ],
    // Correlación de estrés técnico: CCU vs MSPT
    stressTestProfile: [
        { ccu: 25, mspt: 18.5, status: "Óptimo" },
        { ccu: 50, mspt: 22.1, status: "Óptimo" },
        { ccu: 100, mspt: 27.4, status: "Óptimo" },
        { ccu: 150, mspt: 32.0, status: "Saludable" },
        { ccu: 200, mspt: 37.8, status: "Alerta Ligera" },
        { ccu: 250, mspt: 44.5, status: "Alerta Alta" },
        { ccu: 300, mspt: 52.3, status: "Sobrecarga (Lag)" }
    ]
};

const METRICS_FILE = path.join(DATA_DIR, 'current_metrics.json');
if (!fs.existsSync(METRICS_FILE)) {
    fs.writeFileSync(METRICS_FILE, JSON.stringify(DEFAULT_METRICS, null, 2), 'utf8');
}

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;

    // CORS headers para llamadas locales
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    // API ENDPOINTS
    if (pathname === '/api/metrics' && req.method === 'GET') {
        try {
            const rawData = fs.readFileSync(METRICS_FILE, 'utf8');
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(rawData);
        } catch (err) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: "Error al leer métricas", details: err.message }));
        }
        return;
    }

    if (pathname === '/api/metrics/reset' && req.method === 'POST') {
        fs.writeFileSync(METRICS_FILE, JSON.stringify(DEFAULT_METRICS, null, 2), 'utf8');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true, message: "Métricas restablecidas a benchmark oficial" }));
        return;
    }

    if (pathname === '/api/metrics' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
            try {
                const updated = JSON.parse(body);
                fs.writeFileSync(METRICS_FILE, JSON.stringify(updated, null, 2), 'utf8');
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ success: true, updated: new Date().toISOString() }));
            } catch (err) {
                res.writeHead(400, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: "JSON inválido", details: err.message }));
            }
        });
        return;
    }

    // SERVIR ARCHIVOS ESTÁTICOS
    let safePath = path.normalize(pathname).replace(/^(\.\.[\/\\])+/, '');
    if (safePath === '/' || safePath === '\\') {
        safePath = '/index.html';
    }

    const filePath = path.join(PUBLIC_DIR, safePath);

    fs.stat(filePath, (err, stats) => {
        if (err || !stats.isFile()) {
            res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end('404 No Encontrado');
            return;
        }

        const ext = path.extname(filePath).toLowerCase();
        const contentType = MIME_TYPES[ext] || 'application/octet-stream';

        res.writeHead(200, { 'Content-Type': contentType });
        const stream = fs.createReadStream(filePath);
        stream.pipe(res);
    });
});

server.listen(PORT, () => {
    console.log(`\n======================================================`);
    console.log(`⚡ THUNDER-DASHBOARD INICIADO CON ÉXITO`);
    console.log(`======================================================`);
    console.log(`🌐 Acceso local: http://localhost:${PORT}`);
    console.log(`📁 Carpeta de datos: ${DATA_DIR}`);
    console.log(`📊 Benchmarks cargados y listos.`);
    console.log(`Presiona Ctrl+C para detener el servidor.\n`);
});
