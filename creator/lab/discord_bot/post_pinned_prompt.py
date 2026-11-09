import os
import json
import urllib.request

env_path = r"creator\lab\discord_bot\.env"
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

channel_id = "1569343101544300664"
log_channel_id = "1569343103255716011"
headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 2.0.0)",
    "Content-Type": "application/json; charset=utf-8"
}

prompt_text = (
    "Beacon, genera el paquete ZIP de despliegue de Fabio con los cambios actuales. "
    "Empaqueta directamente en la raíz (sin carpetas intermedias) los archivos .py y .json modificados, "
    "validando sintaxis con py_compile y excluyendo bases de datos vivas (*_db.json) y el .env. "
    "Dame el archivo listo para subir a #admin-panel."
)

embed = {
    "title": "🚀 Panel de Despliegue en Caliente | Bot Fabio (Vultam)",
    "description": (
        "Este canal permite actualizar el código del bot en producción de forma automática e instantánea.\n\n"
        "**¿Cómo funciona?**\n"
        "`1️⃣` Sube un archivo `.zip` directamente a este canal.\n"
        "`2️⃣` El sistema inspecciona los archivos, verifica la firma SHA-256 y compila cada script Python en un entorno sandbox.\n"
        "`3️⃣` Si la sintaxis es 100% válida, realiza backup preventivo (`.bak`), reemplaza **únicamente los archivos modificados** y reinicia el proceso del bot en caliente (`os.execv`).\n"
        f"`4️⃣` El resultado detallado de la operación se enviará automáticamente a <#{log_channel_id}>.\n\n"
        "**🛡️ Protecciones de Seguridad Activas:**\n"
        "> `🔒` **Whitelist:** Solo se aceptan despliegues autorizados por el Sr Ramos.\n"
        "> `🗄️` **Datos Vivos Intocables:** Las bases de datos (`postulaciones_db.json`, `sorteos_db.json`) y el `.env` están blindados y jamás se sobrescriben.\n"
        "> `⚠️` **Zero-Crash Sandbox:** Si un script tiene un error de sintaxis, el bot aborta el despliegue y mantiene la versión anterior intacta sin crashear el contenedor de Pterodactyl.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "### 📋 Prompt Oficial para Generar el ZIP\n"
        "Copia y pega este prompt exacto en el chat de trabajo cuando necesites un nuevo paquete de despliegue:"
    ),
    "color": 16762880,
    "fields": [
        {
            "name": "💬 Prompt para el Agente",
            "value": f"```{prompt_text}```",
            "inline": False
        },
        {
            "name": "📌 Formato Requerido del ZIP",
            "value": (
                "> • Archivos en la raíz del zip (ej: `gateway_bot.py`, `reglas_*.json`).\n"
                "> • Sin subcarpetas envolventes.\n"
                "> • Solo archivos de código y configuración permitidos."
            ),
            "inline": False
        }
    ],
    "footer": {
        "text": "ThunderMC Automation Engine • Despliegues Autónomos Seguros"
    }
}

# Post message
url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
data = json.dumps({"embeds": [embed]}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers, method="POST")
with urllib.request.urlopen(req) as resp:
    msg = json.loads(resp.read().decode("utf-8"))
    msg_id = msg.get("id")
    print("Posted prompt message ID:", msg_id)

# Pin message
pin_url = f"https://discord.com/api/v10/channels/{channel_id}/pins/{msg_id}"
pin_req = urllib.request.Request(pin_url, data=b"", headers=headers, method="PUT")
with urllib.request.urlopen(pin_req) as resp:
    print("Message pinned successfully!")
