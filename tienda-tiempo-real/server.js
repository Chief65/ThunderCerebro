const express = require('express');
const nunjucks = require('nunjucks');
const path = require('path');
const https = require('https');

const app = express();
const PORT = process.env.PORT || 3001; // Puerto 3001 para tienda en tiempo real
const TEBEX_PUBLIC_TOKEN = 'p42r-a6e3b70e3dd621852bacd1346cd7aa605232ca82';

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

// Middleware para parsear formularios POST
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Estado de sesión del usuario en memoria para preview interactivo
let currentSessionUser = null;

// Helpers y Variables globales de Tebex
env.addGlobal('config', (k) => {
    const map = {
        'theme-color': '#facc15',
        'site-description': 'Tienda Oficial de ThunderMC - Minecraft 1.21.11 RPG & Network',
        'og-image': '/Assets/spawn_bg.png',
        'background-image': '/Assets/spawn_bg.png',
        'store_theme': 'default',
        'modal_type': 'sidebar',
        'currency': 'USD',
        'category_navigation': 'topbar',
        'announcement': 'enabled',
        'announcementText': '⚡ OFERTAS EN VIVO: Tienda sincronizada oficialmente con Tebex',
        'announcementLink': '/#cat-packs',
        'announcementLinkText': 'Ver Catálogo',
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

// Función para consultar API Headless de Tebex
function fetchTebex(pathEndpoint) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'headless.tebex.io',
            path: '/api/accounts/' + TEBEX_PUBLIC_TOKEN + pathEndpoint,
            method: 'GET',
            headers: { 'Accept': 'application/json' }
        };
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(data);
                    resolve(parsed);
                } catch (e) {
                    reject(e);
                }
            });
        });
        req.on('error', reject);
        req.end();
    });
}

// Mock Basket
const mockBasket = {
    ign: 'Jordan',
    packages: [
        { id: 7488054, name: 'PACK RECLUTA', price: '2.99', quantity: 1 }
    ],
    price: '2.99',
    currency: 'USD'
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

// RUTA LOGIN POST
app.post('/login', (req, res) => {
    const ign = req.body.ign ? req.body.ign.trim() : '';
    if (ign) {
        currentSessionUser = ign;
        mockBasket.ign = ign;
    }
    res.redirect(req.get('Referrer') || '/');
});

// RUTA LOGOUT
app.get('/checkout/logout', (req, res) => {
    currentSessionUser = null;
    mockBasket.ign = null;
    res.redirect('/');
});

// Cache en memoria para catálogo de Tebex
let tebexCache = {
    account: null,
    categories: [],
    packagesMap: {},
    lastFetch: 0
};

async function getTebexData() {
    const now = Date.now();
    // Cache de 30 segundos
    if (tebexCache.account && tebexCache.categories.length && (now - tebexCache.lastFetch < 30000)) {
        return tebexCache;
    }
    try {
        const [accRes, catRes] = await Promise.all([
            fetchTebex(''),
            fetchTebex('/categories?includePackages=1')
        ]);
        if (accRes && accRes.data) tebexCache.account = accRes.data;
        if (catRes && catRes.data) {
            tebexCache.categories = catRes.data;
            tebexCache.packagesMap = {};
            catRes.data.forEach(cat => {
                if (cat.packages) {
                    cat.packages.forEach(pkg => {
                        tebexCache.packagesMap[pkg.id.toString()] = pkg;
                    });
                }
            });
        }
        tebexCache.lastFetch = now;
    } catch (e) {
        console.error('Error fetching from Tebex API:', e);
    }
    return tebexCache;
}

// RUTA MODAL DE PAQUETES (FETCH DINÁMICO DE TEBEX EN TIEMPO REAL)
app.get('/package/:id', async (req, res) => {
    const pkgId = req.params.id;
    const tebex = await getTebexData();
    const realPkg = tebex.packagesMap[pkgId.toString()];

    const pkgToRender = realPkg ? {
        id: realPkg.id,
        name: realPkg.name,
        price: realPkg.total_price,
        discount: realPkg.discount ? { applied: true, original: realPkg.base_price } : { applied: false },
        image: { url: realPkg.image || (realPkg.media && realPkg.media[0] ? realPkg.media[0].url : '/Assets/cat_packs.webp') },
        description: realPkg.description,
        purchasable: true,
        disable_gifting: realPkg.disable_gifting || false,
        storeGiftingEnabled: true
    } : (mockPackages[pkgId] || mockPackages['1']);
    
    const storeInfo = tebex.account ? {
        name: tebex.account.name || 'ThunderMC',
        currency: tebex.account.currency || 'USD',
        currency_symbol: tebex.account.currency === 'EUR' ? '€' : '$',
        logo: tebex.account.logo || '/Assets/thunder_logo.png',
        favicon: '/Assets/favicon.png',
        subdomain: tebex.account.webstore_url || 'tienda.thundermc.es'
    } : mockStore;

    env.render('package.html', {
        package: pkgToRender,
        store: storeInfo,
        basket: { ...mockBasket, ign: currentSessionUser, currency: storeInfo.currency },
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

// RUTA CHECKOUT BASKET
app.get('/checkout/basket', async (req, res) => {
    const tebex = await getTebexData();
    const storeInfo = tebex.account ? {
        name: tebex.account.name || 'ThunderMC',
        currency: tebex.account.currency || 'USD',
        currency_symbol: tebex.account.currency === 'EUR' ? '€' : '$',
        logo: tebex.account.logo || '/Assets/thunder_logo.png',
        useCheckout: true
    } : { ...mockStore, useCheckout: true };

    env.render('checkout.html', {
        store: storeInfo,
        basket: {
            ...mockBasket,
            ign: currentSessionUser,
            ident: 'tbx-mock-session-12345',
            packages: [
                {
                    id: 7488054,
                    name: 'PACK RECLUTA (Oficial Tebex)',
                    price: 2.99,
                    quantity: 1,
                    image: { url: '/Assets/cat_packs.webp' }
                }
            ],
            price: '2.99',
            currency: storeInfo.currency,
            coupons: []
        },
        page: { title: 'Finalizar Compra', category: 'checkout' },
        lang: {
            checkout_loading: 'Cargando pasarela...',
            proceed_to_checkout: 'Continuar con el Pago',
            youMustTickAllBoxes: 'Debes aceptar los términos antes de continuar.'
        },
        theme_configuration: {
            checkoutUserAgreement: [
                { content: 'He leído y acepto los <strong>Términos del Servicio</strong> y la <strong>Política de Privacidad</strong> de ThunderMC.' },
                { content: 'Entiendo que las compras de rangos y paquetes virtuales son finales y no reembolsables.' }
            ]
        }
    }, (err, html) => {
        if (err) {
            console.error('Error render checkout:', err);
            return res.status(500).send(err.stack);
        }
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.send(html);
    });
});

// RUTA SOBRE THUNDER (/about)
app.get('/about', async (req, res) => {
    const tebex = await getTebexData();
    const storeInfo = tebex.account ? {
        name: tebex.account.name || 'ThunderMC',
        currency: tebex.account.currency || 'USD',
        logo: tebex.account.logo || '/Assets/thunder_logo.png'
    } : mockStore;

    env.render('cmspage.html', {
        store: storeInfo,
        basket: { ...mockBasket, ign: currentSessionUser },
        page: {
            title: 'Sobre ThunderMC',
            content: `
                <h2>⚡ La Red Definitiva de Minecraft 1.21.11</h2>
                <p><strong>ThunderMC</strong> nace con el objetivo de ofrecer una experiencia RPG de alta calidad donde cada logro, mineral y victoria en mazmorra tenga verdadero valor.</p>
                
                <div class="tz-cms-highlight-box">
                    <i class="mdi mdi-shield-crown tz-cms-hl-icon"></i>
                    <div class="tz-cms-hl-text">
                        <span class="tz-cms-hl-title">Infraestructura Dedicada de Alto Rendimiento</span>
                        <span>Servidores optimizados en hardware empresarial con protección Anti-DDoS avanzada y 20.0 TPS constantes para PvP y PvE fluido.</span>
                    </div>
                </div>

                <h3>🎮 Modalidades & Características Principales</h3>
                <ul style="padding-left: 20px; margin-bottom: 24px; display: flex; flex-direction: column; gap: 10px;">
                    <li><strong>⚔️ Dungeons Dinámicas:</strong> Enfréntate a oleadas de monstruos con mecánicas de jefe personalizadas y recompensas en Zafiros.</li>
                    <li><strong>⛏️ Sistema Catamines:</strong> Minas multinivel con picos evolucionables, gemas arcanas y boosters temporales.</li>
                    <li><strong>👑 Clanes & Guerras:</strong> Conquista territorios, sube de nivel tu clan y desbloquea cofres comunitarios.</li>
                    <li><strong>💎 Economía No Inflacionaria:</strong> Ajustada minuciosamente para evitar el empobrecimiento de nuevos jugadores.</li>
                </ul>

                <h3>📜 Compromiso y Transparencia</h3>
                <p>Todo el soporte económico recibido a través de esta tienda se reinvierte directamente en mejoras de hardware, desarrollo de mecánicas exclusivas y eventos con recompensas para toda la comunidad.</p>
            `
        }
    }, (err, html) => {
        if (err) return res.status(500).send(err.stack);
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.send(html);
    });
});

// RUTA SOPORTE Y FAQ (/help)
app.get('/help', async (req, res) => {
    const tebex = await getTebexData();
    const storeInfo = tebex.account ? {
        name: tebex.account.name || 'ThunderMC',
        currency: tebex.account.currency || 'USD',
        logo: tebex.account.logo || '/Assets/thunder_logo.png'
    } : mockStore;

    env.render('cmspage.html', {
        store: storeInfo,
        basket: { ...mockBasket, ign: currentSessionUser },
        page: {
            title: 'Centro de Ayuda & Soporte',
            content: `
                <h2>🛠️ ¿Tienes dudas con tu compra o el servidor?</h2>
                <p>Consulta nuestras respuestas rápidas o abre un ticket de atención al cliente en nuestro Discord oficial si necesitas asistencia directa con el equipo técnico.</p>

                <div class="tz-cms-highlight-box">
                    <i class="mdi mdi-clock-check tz-cms-hl-icon"></i>
                    <div class="tz-cms-hl-text">
                        <span class="tz-cms-hl-title">Activación Automática Garantizada</span>
                        <span>Las compras tardan normalmente entre 1 y 3 minutos en llegar a tu cuenta in-game. Recuerda tener espacio en el inventario al reclamar ítems.</span>
                    </div>
                </div>

                <h3>❓ Preguntas Frecuentes</h3>
                <div class="tz-faq-list">
                    <div class="tz-faq-item active">
                        <div class="tz-faq-question">
                            <span>¿Qué debo hacer si mi compra no llega tras 10 minutos?</span>
                            <i class="mdi mdi-chevron-down"></i>
                        </div>
                        <div class="tz-faq-answer">
                            Verifica que hayas introducido tu Nick exacto (distinguiendo mayúsculas y minúsculas). Si eres jugador de Bedrock, asegúrate de haber seleccionado dicha pestaña. Si el problema persiste, abre un ticket en Discord con tu ID de transacción de Tebex.
                        </div>
                    </div>
                    <div class="tz-faq-item">
                        <div class="tz-faq-question">
                            <span>¿Los rangos VIP son permanentes?</span>
                            <i class="mdi mdi-chevron-down"></i>
                        </div>
                        <div class="tz-faq-answer">
                            Sí, los rangos VIP, MVP, THUNDER y TITÁN son permanentes durante toda la temporada. Las suscripciones mensuales del Club VIP se especifican claramente en su tarjeta.
                        </div>
                    </div>
                    <div class="tz-faq-item">
                        <div class="tz-faq-question">
                            <span>¿Puedo transferir un rango a otra cuenta?</span>
                            <i class="mdi mdi-chevron-down"></i>
                        </div>
                        <div class="tz-faq-answer">
                            Por motivos de seguridad, las transferencias de rango solo se realizan en casos excepcionales de cambio de cuenta oficial de Mojang mediante verificación por ticket de soporte.
                        </div>
                    </div>
                </div>
            `
        }
    }, (err, html) => {
        if (err) return res.status(500).send(err.stack);
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.send(html);
    });
});

// RUTA DINÁMICA PRINCIPAL CON CATÁLOGO EN VIVO DE TEBEX
app.get('/', async (req, res) => {
    const tebex = await getTebexData();
    const storeInfo = tebex.account ? {
        name: tebex.account.name || 'ThunderMC',
        currency: tebex.account.currency || 'USD',
        currency_symbol: tebex.account.currency === 'EUR' ? '€' : '$',
        logo: tebex.account.logo || '/Assets/thunder_logo.png',
        favicon: '/Assets/favicon.png',
        subdomain: tebex.account.webstore_url || 'tienda.thundermc.es',
        categories: tebex.categories,
        online_players: 148,
        server_ip: 'thundermc.es'
    } : mockStore;

    env.render('index.html', {
        store: storeInfo,
        basket: { ...mockBasket, ign: currentSessionUser, currency: storeInfo.currency },
        page: mockPage,
        categories: tebex.categories.length ? tebex.categories : mockStore.categories,
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
    console.log(`\n⚡ Tienda en Tiempo Real (Tebex Live Synced) activa en: http://localhost:${PORT}\n`);
});
