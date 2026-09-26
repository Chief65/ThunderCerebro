import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) process.exit(1);
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

const payloadPath = process.argv[2] 
  ? path.resolve(process.cwd(), process.argv[2])
  : path.join(__dirname, 'payload.json');

const imagePath = process.argv[3]
  ? path.resolve(process.cwd(), process.argv[3])
  : null;

const payloadData = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));

async function sendMessage() {
  const url = `https://discord.com/api/v10/channels/${channelId}/messages`;
  console.log(`📡 Enviando mensaje a canal [${channelId}]...`);

  try {
    let res;
    if (imagePath && fs.existsSync(imagePath)) {
      console.log(`📎 Adjuntando archivo local: ${imagePath}`);
      const formData = new FormData();
      const fileBytes = fs.readFileSync(imagePath);
      const fileName = path.basename(imagePath);
      const blob = new Blob([fileBytes], { type: 'image/png' });

      formData.append('files[0]', blob, fileName);
      formData.append('payload_json', JSON.stringify(payloadData));

      res = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bot ${token}`
        },
        body: formData
      });
    } else {
      res = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bot ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payloadData)
      });
    }

    const body = await res.json();

    if (!res.ok) {
      console.error('❌ Fallo al enviar mensaje:', res.status, res.statusText);
      console.error(JSON.stringify(body, null, 2));
      process.exit(1);
    }

    console.log('✅ ¡Mensaje enviado con éxito!');
    console.log(`ID del mensaje: ${body.id}`);
  } catch (err) {
    console.error('❌ Error de conexión:', err);
    process.exit(1);
  }
}

sendMessage();
