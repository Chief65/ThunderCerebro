const express = require('express');
const nunjucks = require('nunjucks');
const path = require('path');

const app = express();
const PORT = 3000;

// Configuración Nunjucks sin caché (lectura en vivo desde disco)
const env = new nunjucks.Environment(
    new nunjucks.FileSystemLoader([
        path.join(__dirname),
        path.join(__dirname, 'Assets')
    ], { noCache: true }),
    { autoescape: false, noCache: true }
);

// Middleware No-Cache global para desarrollo en vivo
app.use((req, res, next) => {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    next();
});

// Helpers y Variables globales de Tebex
env.addGlobal('config', (k) => {
    const map = {
        'theme-color': '#facc15',
        'site-description': 'Tienda Oficial de ThunderMC - Minecraft 1.21.11 RPG & Network',
        'og-image': '/Assets/spawn_bg.png',
        'background-image': '/Assets/spawn_bg.png',
        'store_theme': 'default',
        'modal_type': 'sidebar',
        'currency': 'EUR',
        'category_navigation': 'topbar',
        'announcement': 'enabled',
        'announcementText': '⚡ OFERTAS DE TEMPORADA: Hasta 35% de descuento en todos los Rangos VIP',
        'announcementLink': '/#cat-1',
        'announcementLinkText': 'Ver Rangos',
        'sidebar_position': 'right',
        'header_layout': 'modern',
        'serverType': 'Minecraft',
        'bedrockPrefix': '*',
        'discord_invite': 'https://discord.gg/thundermc',
    };
    return map[k] !== undefined ? map[k] : '';
});

env.addGlobal('__', (k) => k);
env.addGlobal('asset', (k) => '/Assets/' + k);
env.addFilter('money', (v) => Number(v || 0).toFixed(2));
env.addFilter('raw', (v) => v);
env.addFilter('date', (v, f) => '2026');

// Mock Data
const mockStore = {
    name: 'ThunderMC',
    currency: 'EUR',
    currency_symbol: '€',
    logo: '/Assets/thunder_logo.png',
    favicon: '/Assets/favicon.png',
    subdomain: 'tienda.thundermc.net',
    categories: [
        { id: 1, name: 'Rangos VIP', slug: 'rangos', active: true, subcategories: [] },
        { id: 2, name: 'Dungeons & Jefes', slug: 'dungeons', active: false, subcategories: [] },
        { id: 3, name: 'Catamines & Minas', slug: 'minas', active: false, subcategories: [] },
        { id: 4, name: 'Items & Llaves', slug: 'items', active: false, subcategories: [] }
    ],
    pages: [
        { slug: 'reglas', title: 'Reglas' },
        { slug: 'contacto', title: 'Soporte' }
    ],
    online_players: 148,
    server_ip: 'thundermc.es'
};

const mockBasket = {
    ign: 'Jordan',
    packages: [
        { id: 101, name: 'Rango VIP Thunder+', price: '14.99', quantity: 1 }
    ],
    price: '14.99',
    currency: 'EUR'
};

const mockPage = {
    title: 'Inicio',
    category: 1,
    message: { display: false }
};

// Packages Data
const mockPackages = {
    '1': {
        id: 1,
        name: 'Rango VIP',
        price: 7.49,
        discount: { applied: true, original: 9.99 },
        image: { url: 'https://dunb17ur4ymx4.cloudfront.net/packages/images/627911b9d1fc3d05619a58846649d6f231253039.png' },
        description: `
            <div class="tz-modal-perks">
                <h4 style="color:#facc15;font-family:'Bakbak One',sans-serif;margin-top:0;font-size:18px;">⚡ BENEFICIOS DEL RANGO VIP</h4>
                <ul style="list-style:none;padding:0;margin:0 0 20px 0;display:flex;flex-direction:column;gap:10px;">
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Prefijo VIP</strong> dorado exclusivo en el chat y tabulador.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Kit VIP Mensual:</strong> Set completo de armadura de Diamante Reforzado.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Acceso a Catamines:</strong> Entrada permanente a la mina VIP nivel 1.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>+3 Homes</strong> adicionales (/sethome vip1, vip2, vip3).</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> Prioridad de acceso cuando el servidor esté lleno.</li>
                </ul>
                <div style="background:rgba(250,204,21,0.08);border:1px solid rgba(250,204,21,0.25);border-radius:10px;padding:12px;color:#94a3b8;font-size:12.5px;">
                    💡 <em>Este rango es 100% permanente para toda la temporada 1.21.11.</em>
                </div>
            </div>
        `,
        purchasable: true,
        disable_gifting: false,
        storeGiftingEnabled: true
    },
    '2': {
        id: 2,
        name: 'Rango MVP',
        price: 13.99,
        discount: { applied: true, original: 19.99 },
        image: { url: 'https://dunb17ur4ymx4.cloudfront.net/packages/images/627911b9d1fc3d05619a58846649d6f231253039.png' },
        description: `
            <div class="tz-modal-perks">
                <h4 style="color:#facc15;font-family:'Bakbak One',sans-serif;margin-top:0;font-size:18px;">⚡ BENEFICIOS DEL RANGO MVP</h4>
                <ul style="list-style:none;padding:0;margin:0 0 20px 0;display:flex;flex-direction:column;gap:10px;">
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Todos los beneficios del Rango VIP</strong> incluidos.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Kit MVP Quincenal:</strong> Armadura Netherite Encantada + 32 Manzanas Doradas.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Comando /fly</strong> en tus parcelas y mundos de construcción.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Acceso a Dungeons Tier 2</strong> sin pagar tasa de entrada.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>+6 Homes</strong> adicionales (/sethome).</li>
                </ul>
            </div>
        `,
        purchasable: true,
        disable_gifting: false,
        storeGiftingEnabled: true
    },
    '3': {
        id: 3,
        name: 'Rango THUNDER',
        price: 25.99,
        discount: { applied: true, original: 39.99 },
        image: { url: 'https://dunb17ur4ymx4.cloudfront.net/packages/images/627911b9d1fc3d05619a58846649d6f231253039.png' },
        description: `
            <div class="tz-modal-perks">
                <h4 style="color:#facc15;font-family:'Bakbak One',sans-serif;margin-top:0;font-size:18px;">⚡ BENEFICIOS MÁXIMOS RANGO THUNDER</h4>
                <ul style="list-style:none;padding:0;margin:0 0 20px 0;display:flex;flex-direction:column;gap:10px;">
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Todos los beneficios VIP y MVP</strong> desbloqueados.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Multiplicador x2.0 de Almas</strong> en todas las Mazmorras y Catamines.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Comandos VIP Especiales:</strong> /feed, /heal, /craft, /enderchest, /anvil.</li>
                    <li style="display:flex;align-items:center;gap:8px;color:#f1f5f9;font-weight:600;"><span style="color:#4ade80;">✓</span> <strong>Efecto de Partículas Legendario</strong> de Rayo en tus pasos.</li>
                </ul>
            </div>
        `,
        purchasable: true,
        disable_gifting: false,
        storeGiftingEnabled: true
    }
};

// RUTA MODAL DE PAQUETES (FETCH DINÁMICO DE TEBEX)
app.get('/package/:id', (req, res) => {
    const pkgId = req.params.id;
    const pkg = mockPackages[pkgId] || mockPackages['1'];
    
    env.render('package.html', {
        package: pkg,
        store: mockStore,
        basket: mockBasket,
        lang: {
            remove_from_cart: 'Eliminar del Carrito',
            item_is_free: 'Gratis',
            choosePrice: 'Elige un precio',
            giftButton: 'Comprar para un amigo',
            giftPackageTo: 'Nick del destinatario'
        }
    }, (err, html) => {
        if (err) {
            console.error('Error render package modal:', err);
            return res.status(500).send(err.stack);
        }
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.send(html);
    });
});

// RUTA DINÁMICA PRINCIPAL
app.get('/', (req, res) => {
    env.render('index.html', {
        store: mockStore,
        basket: mockBasket,
        page: mockPage,
        categories: mockStore.categories,
        lang: {
            guest: 'Iniciar Sesión',
            empty_cart: 'Carrito vacío',
            click_to_login: 'Ingresa tu Nick',
            free_basket: 'Gratis'
        }
    }, (err, html) => {
        if (err) {
            console.error('Error render:', err);
            return res.status(500).send(`<pre style="color:#f87171;background:#0f172a;padding:24px;border-radius:8px;font-family:monospace;">${err.stack}</pre>`);
        }
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.send(html);
    });
});

// Estáticos
app.use('/Assets', express.static(path.join(__dirname, 'Assets')));
app.use(express.static(__dirname, { index: false }));

app.listen(PORT, () => {
    console.log(`\n🚀 Servidor de Preview Tebex (Full Dynamic Engine) activo en: http://localhost:${PORT}\n`);
});
