import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Cargar variables de .env
function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) {
    console.error('❌ No se encontro el archivo .env');
    process.exit(1);
  }
  const lines = fs.readFileSync(envPath, 'utf8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const splitIndex = trimmed.indexOf('=');
    if (splitIndex !== -1) {
      process.env[trimmed.slice(0, splitIndex).trim()] = trimmed.slice(splitIndex + 1).trim();
    }
  }
}

loadEnv();

const token = process.env.DISCORD_BOT_TOKEN;
const channelId = process.env.DISCORD_CHANNEL_ID;
const PORT = process.env.PORT || 3050;
const TEBEX_SECRET = process.env.TEBEX_WEBHOOK_SECRET || '';

// Funcion para despachar el embed a Discord
async function sendDiscordEmbed(purchase) {
  const imagePath = path.resolve(__dirname, '../../output/renders/campamento_dia/campamento_dia_1138x640.jpg');
  const tempPayloadPath = path.join(__dirname, 'temp_tebex_dispatch.json');
  
  const payload = {
    allowed_mentions: {
      parse: ["everyone"]
    },
    embeds: [
      {
        title: `🛒 ¡Nueva Compra de ${purchase.player}!`,
        description: `¡Agradecemos enormemente el apoyo!\n-# ɢʀᴀᴄɪᴀꜱ ᴘᴏʀ ʜᴀᴄᴇʀ ᴄʀᴇᴄᴇʀ ᴛʜᴜɴᴅᴇʀ\n\n**Detalles de la Adquisición:**\n\`👤\` Comprador: \`${purchase.player}\`\n\`📦\` Paquete: \`${purchase.package}\`\n\n↓ Conéctate para disfrutar de tus recompensas ↓\n\`\`\`text\nthundermc.es\n\`\`\`\n-# 📱 Puerto Bedrock: \`19132\` | 🎮 Java: Puerto por defecto\n\n-# [Tienda](https://tienda.thundermc.es/) • [Tiktok](https://www.tiktok.com/@somosthundermc_?lang=es) • [YouTube](https://www.youtube.com/@somosthundermc/featured)`,
        color: 16706304,
        thumbnail: {
          url: `https://minotar.net/bust/${encodeURIComponent(purchase.player)}/100`
        },
        image: {
          url: "attachment://campamento_dia_1138x640.jpg"
        }
      }
    ],
    components: [
      {
        type: 1,
        components: [
          {
            type: 2,
            style: 5,
            label: "Click para ver la tienda oficial de ThunderMc",
            url: "https://tienda.thundermc.es/",
            emoji: {
              name: "🪙"
            }
          }
        ]
      }
    ]
  };

  fs.writeFileSync(tempPayloadPath, JSON.stringify(payload, null, 2), 'utf8');

  // Ejecutar curl para envio multipart garantizado
  const { execFile } = await import('node:child_process');
  const curlArgs = [
    '-s',
    '-X', 'POST',
    `https://discord.com/api/v10/channels/${channelId}/messages`,
    '-H', `Authorization: Bot ${token}`,
    '-H', 'User-Agent: DiscordBot (https://thundermc.es, 1.0.0)',
    '-F', `files[0]=@${imagePath}`,
    '-F', `payload_json=<${tempPayloadPath};type=application/json`
  ];

  execFile('curl.exe', curlArgs, (err, stdout, stderr) => {
    try { fs.unlinkSync(tempPayloadPath); } catch {}
    if (err) {
      console.error('❌ [Discord] Error al ejecutar curl:', err);
      return;
    }
    try {
      const resObj = JSON.parse(stdout);
      if (resObj.id) {
        console.log(`✅ [Discord] Embed enviado con éxito! ID: ${resObj.id}`);
      } else {
        console.error('❌ [Discord] Error en respuesta de Discord:', stdout);
      }
    } catch {
      console.error('❌ [Discord] Fallo parseando respuesta:', stdout);
    }
  });
}

// Servidor HTTP receptor de Webhooks
const server = http.createServer((req, res) => {
  if (req.method === 'POST' && (req.url === '/tebex' || req.url === '/')) {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const data = JSON.parse(body);
        console.log(`📥 [Tebex Webhook] Evento recibido: ${data.type || 'desconocido'}`);

        // Verificacion opcional de secret si esta configurado
        if (TEBEX_SECRET) {
          const authHeader = req.headers['x-bc-signature'] || req.headers['authorization'];
          if (!authHeader) {
            console.warn('⚠️ Webhook rechazado: falta firma o secreto');
            res.writeHead(401);
            return res.end('Unauthorized');
          }
        }

        // Procesar evento de pago completado
        if (data.type === 'payment.completed' || data.event === 'payment.completed' || data.subject) {
          const subject = data.subject || data;
          
          let player = 'Desconocido';
          if (subject.customer) {
            if (typeof subject.customer.username === 'string') player = subject.customer.username;
            else if (subject.customer.username?.username) player = subject.customer.username.username;
            else if (subject.customer.ign) player = subject.customer.ign;
          }

          let packageName = 'Paquete ThunderMC';
          if (Array.isArray(subject.products) && subject.products.length > 0) {
            packageName = subject.products.map(p => p.name).join(', ');
          }

          let priceStr = 'N/A';
          if (subject.price) {
            priceStr = `${subject.price.amount} ${subject.price.currency}`;
          }

          const txId = subject.transaction_id || data.id || 'N/A';

          console.log(`💰 Compra confirmada: Jugador: ${player} | Paquete: ${packageName} | Precio: ${priceStr}`);
          
          // Despachar embed a Discord
          await sendDiscordEmbed({
            player,
            package: packageName,
            price: priceStr,
            transaction: txId
          });
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'success' }));
      } catch (err) {
        console.error('❌ Error al procesar JSON de Tebex:', err);
        res.writeHead(400);
        res.end('Bad Request');
      }
    });
  } else if (req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ThunderMC Tebex Webhook Listener Activo');
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(PORT, () => {
  console.log(`🚀 [Tebex Listener] Servidor escuchando en puerto ${PORT}`);
  console.log(`📡 Esperando eventos POST en http://localhost:${PORT}/tebex`);
});
