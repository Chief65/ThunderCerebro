import os
import json
import urllib.request

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

thread_reglas_id = "1568202151186927646"
guild_id = "1552715004669726802"
channel_id = "1552723526996336724"
main_msg_id = "1568202169633603704"
back_url = f"https://discord.com/channels/{guild_id}/{channel_id}/{main_msg_id}"
ticket_url = f"https://discord.com/channels/{guild_id}/1374644365758169178"
user_agent = "DiscordBot (https://thundermc.es, 1.0.0)"

def discord_api(method, endpoint, body=None):
    url = f"https://discord.com/api/v10{endpoint}"
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": user_agent,
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else {}

# 1. Cargar las 2 reglas originales
with open(r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\reglas generales.json", "r", encoding="utf-8") as f:
    rg_embed = json.load(f)["embeds"][0]

with open(r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\reglas discord.json", "r", encoding="utf-8") as f:
    rd_embed = json.load(f)["embeds"][0]

# 2. Limpiar mensajes antiguos dentro del hilo de normativa
msgs = discord_api("GET", f"/channels/{thread_reglas_id}/messages?limit=10")
for m in msgs:
    if m.get("type") == 0:
        try:
            discord_api("DELETE", f"/channels/{thread_reglas_id}/messages/{m['id']}")
            print(f"Eliminado mensaje {m['id']} del hilo de reglas")
        except Exception as e:
            print(f"Aviso al borrar: {e}")

# 3. Construir payload con los 2 embeds + botones de Volver al Inicio y Reportar/Ticket
payload = {
    "allowed_mentions": {
        "parse": []
    },
    "embeds": [
        rg_embed,
        rd_embed
    ],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 5,
                    "label": "Volver al Inicio",
                    "emoji": {
                        "name": "⬅️"
                    },
                    "url": back_url
                },
                {
                    "type": 2,
                    "style": 5,
                    "label": "Reportar Infracción (Ticket)",
                    "emoji": {
                        "name": "🎫"
                    },
                    "url": ticket_url
                }
            ]
        }
    ]
}

# Guardar payload en output
out_p = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\normativa_oficial_hilo.json"
with open(out_p, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

res = discord_api("POST", f"/channels/{thread_reglas_id}/messages", payload)
print(f"Enviadas las 2 reglas al hilo {thread_reglas_id} con ID: {res['id']}")
