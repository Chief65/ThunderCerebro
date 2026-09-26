import fs from 'node:fs';

const env = fs.readFileSync('.env', 'utf8');
const token = env.match(/DISCORD_BOT_TOKEN=(.+)/)[1].trim();
const channelId = env.match(/DISCORD_CHANNEL_ID=(.+)/)[1].trim();

const res = await fetch(`https://discord.com/api/v10/channels/${channelId}`, {
  headers: { Authorization: `Bot ${token}` }
});
const channel = await res.json();
console.log('Guild ID:', channel.guild_id);

const resChannels = await fetch(`https://discord.com/api/v10/guilds/${channel.guild_id}/channels`, {
  headers: { Authorization: `Bot ${token}` }
});
const channels = await resChannels.json();
const matches = channels.filter(c => /anuncio|regla|ticket|soporte/i.test(c.name));
console.log(JSON.stringify(matches.map(c => ({ id: c.id, name: c.name, type: c.type })), null, 2));
