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

# 1. Limpiar mensajes antiguos dentro del hilo de normativa
msgs = discord_api("GET", f"/channels/{thread_reglas_id}/messages?limit=10")
for m in msgs:
    if m.get("type") == 0:
        try:
            discord_api("DELETE", f"/channels/{thread_reglas_id}/messages/{m['id']}")
            print(f"Eliminado mensaje {m['id']} del hilo de reglas")
        except Exception as e:
            print(f"Aviso al borrar: {e}")

# 2. Construir el embed con el menú dropdown interactivo
payload = {
    "allowed_mentions": {
        "parse": []
    },
    "embeds": [
        {
            "title": "📜 Normativa Oficial & Convivencia | ThunderMC",
            "description": (
                "¡Bienvenid@ al centro de normativas oficiales de ThunderMC!\n"
                "-# ᴄᴏɴᴏᴄᴇ ᴇʟ ʀᴇɢʟᴀᴍᴇɴᴛᴏ ᴘᴀʀᴀ ᴜɴᴀ ᴇxᴘᴇʀɪᴇɴᴄɪᴀ ʟɪᴍᴘɪᴀ, ᴊᴜꜱᴛᴀ ʏ ꜱᴇɢᴜʀᴀ\n\n"
                "> ⚖️ **Aviso:** Al jugar en ThunderMC o interactuar en nuestro Discord, aceptas acatar nuestras normas de convivencia. "
                "El criterio del staff prevalece ante situaciones no tipificadas explícitamente.\n\n"
                "## 📋 Consulta de Normativa:\n"
                "Selecciona una categoría en el menú desplegable inferior para visualizar su reglamento completo:\n\n"
                "`⚔️` **Reglas Generales:** Normas del servidor de Minecraft (PvP, juego limpio, modificaciones y economía).\n"
                "`💬` **Reglas de Discord:** Normas de convivencia en texto y voz, spam, privacidad y respeto."
            ),
            "color": 16706304,
            "thumbnail": {
                "url": "https://cdn.discordapp.com/attachments/1552723526996336724/1560474539547299901/minecraft_compass_transparent.png?ex=6aee882a&is=6aed36aa&hm=26bfe9a9a2dd5bdde582e426e6958b6fb095e524ad1fe597e06460f7ae1b8bd1&"
            }
        }
    ],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 3,
                    "custom_id": "select_reglas_normativa",
                    "placeholder": "Elige la normativa que deseas consultar...",
                    "min_values": 1,
                    "max_values": 1,
                    "options": [
                        {
                            "label": "Reglas Generales (Minecraft)",
                            "value": "reglas_generales",
                            "description": "Juego limpio, combate, modificaciones y economía",
                            "emoji": {
                                "name": "⚔️"
                            }
                        },
                        {
                            "label": "Reglas de Discord",
                            "value": "reglas_discord",
                            "description": "Convivencia, canales, respeto y privacidad",
                            "emoji": {
                                "name": "💬"
                            }
                        }
                    ]
                }
            ]
        },
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

out_p = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\menu_normativa_interactivo.json"
with open(out_p, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

res = discord_api("POST", f"/channels/{thread_reglas_id}/messages", payload)
print(f"Enviado menu dropdown al hilo {thread_reglas_id} con ID: {res['id']}")
