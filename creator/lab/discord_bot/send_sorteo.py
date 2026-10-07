import json
import urllib.request
import urllib.error

# Cargar .env
env = {}
with open('creator/lab/discord_bot/.env', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

token = env.get('DISCORD_BOT_TOKEN')
channel_id = env.get('DISCORD_CHANNEL_ID')

# Leer embed actualizado
with open('creator/lab/discord_bot/sorteo_embed.json', 'r', encoding='utf-8') as f:
    payload = json.load(f)

url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
headers = {
    "Authorization": f"Bot {token}",
    "Content-Type": "application/json",
    "User-Agent": "DiscordBot (ThunderMC, 1.0)"
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        res_data = response.read().decode('utf-8')
        res_json = json.loads(res_data)
        print("SUCCESS_MESSAGE_ID:", res_json.get('id'))
except urllib.error.HTTPError as e:
    print("HTTP_ERROR:", e.code, e.read().decode('utf-8'))
except Exception as e:
    print("ERROR:", str(e))
