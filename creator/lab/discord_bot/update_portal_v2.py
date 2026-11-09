#!/usr/bin/env python3
"""
Actualiza el mensaje principal del portal en #embeds (1552723526996336724 / 1568202169633603704)
con el diseño unificado de 1 solo contenedor y la sección 'Verificación Minecraft'.
"""

import os
import json
import urllib.request
import urllib.error

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

channel_id = "1552723526996336724"
msg_id = "1568202169633603704"
payload_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_thundermc_v2.json"

with open(payload_file, "r", encoding="utf-8") as f:
    payload = json.load(f)

url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_id}"
headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 2.0.0)",
    "Content-Type": "application/json; charset=utf-8"
}

data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print(f"SUCCESS! Mensaje del portal actualizado ({res.get('id')}). Contenedores raíz: {len(res.get('components', []))}")
except urllib.error.HTTPError as e:
    err_body = e.read().decode("utf-8", errors="replace")
    print(f"HTTP Error {e.code}: {err_body}")
