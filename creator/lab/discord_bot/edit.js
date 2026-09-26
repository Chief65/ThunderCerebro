import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadEnv() {
  const envPath = path.join(__dirname, '.env');
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
const messageId = process.argv[2];
const payloadFile = process.argv[3];
const imagePath = process.argv[4] ? path.resolve(process.cwd(), process.argv[4]) : null;

if (!messageId || !payloadFile) {
  console.error('Uso: node edit.js <MESSAGE_ID> <PAYLOAD_JSON> [IMAGE_PATH]');
  process.exit(1);
}

const payloadPath = path.resolve(process.cwd(), payloadFile);
const payloadData = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));

async function editMessage() {
  const url = `https://discord.com/api/v10/channels/${channelId}/messages/${messageId}`;
  console.log(`✏️ Editando mensaje [${messageId}] en canal [${channelId}]...`);

  try {
    let res;
    if (imagePath && fs.existsSync(imagePath)) {
      console.log(`📎 Adjuntando archivo: ${imagePath}`);
      const formData = new FormData();
      const fileBytes = fs.readFileSync(imagePath);
      const fileName = path.basename(imagePath);
      const blob = new Blob([fileBytes], { type: 'image/gif' });

      formData.append('files[0]', blob, fileName);
      formData.append('payload_json', JSON.stringify(payloadData));

      res = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bot ${token}`
        },
        body: formData
      });
    } else {
      res = await fetch(url, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bot ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payloadData)
      });
    }

    const body = await res.json();

    if (!res.ok) {
      console.error('❌ Fallo al editar mensaje:', res.status, res.statusText);
      console.error(JSON.stringify(body, null, 2));
      process.exit(1);
    }

    console.log('✅ ¡Mensaje editado con éxito!');
  } catch (err) {
    console.error('❌ Error de conexión:', err);
    process.exit(1);
  }
}

editMessage();
