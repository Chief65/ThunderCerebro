import fs from 'node:fs';

const env = fs.readFileSync('.env', 'utf8');
const token = env.match(/DISCORD_BOT_TOKEN=(.+)/)[1].trim();

// Canales a escanear (embeds y general)
const channels = ['1552723526996336724', '1552715006259232880'];

for (const cId of channels) {
  const res = await fetch(`https://discord.com/api/v10/channels/${cId}/messages?limit=50`, {
    headers: { Authorization: `Bot ${token}` }
  });
  const msgs = await res.json();
  if (Array.isArray(msgs)) {
    for (const m of msgs) {
      if (m.attachments && m.attachments.length > 0) {
        console.log(`Canal ${cId} attachments:`, m.attachments.map(a => a.url));
      }
      if (m.embeds && m.embeds.length > 0) {
        for (const e of m.embeds) {
          if (e.image) console.log(`Canal ${cId} embed image:`, e.image.url);
          if (e.video) console.log(`Canal ${cId} embed video:`, e.video.url);
        }
      }
    }
  }
}
