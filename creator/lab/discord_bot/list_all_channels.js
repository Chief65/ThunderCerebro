import fs from 'node:fs';

const env = fs.readFileSync('.env', 'utf8');
const token = env.match(/DISCORD_BOT_TOKEN=(.+)/)[1].trim();

const resChannels = await fetch('https://discord.com/api/v10/guilds/1552715004669726802/channels', {
  headers: { Authorization: `Bot ${token}` }
});
const channels = await resChannels.json();
console.log(channels.map(c => `${c.id} -> ${c.name} (type ${c.type})`).join('\n'));
