import os
import json
import urllib.request
import urllib.error

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

master_prompt = (
    "Actúa como Ingeniero Senior de Software especializado en Python y Discord.\n"
    "Genera el paquete ZIP de despliegue para el bot 'Fabio' de ThunderMC (alojado en Pterodactyl Linux) bajo estas reglas estrictas:\n\n"
    "1. ESTRUCTURA PLANA EN RAÍZ: Todos los archivos modificados (.py, .json, etc.) deben ubicarse directamente en la RAÍZ del ZIP, sin carpetas contenedoras intermedias (ej: gateway_bot.py en raíz, nunca en /src/).\n"
    "2. EXCLUSIÓN PROTEGIDA: NUNCA incluyas .env ni bases de datos vivas (*_db.json como postulaciones_db.json o sorteos_db.json). Se mantienen intactas en producción.\n"
    "3. SINTAXIS ESTRICTA: El código debe ser 100% válido para Python 3.12 y pasar py_compile sin errores.\n"
    "4. ARCHIVOS LIMPIOS: Excluye metadatos como __pycache__, .git o .DS_Store.\n"
    "5. ENTREGA: Proporciona el archivo .zip listo para subir al canal #admin-panel."
)

embed = {
    "title": "🚀 Panel de Despliegue en Caliente | Bot Fabio (Vultam)",
    "description": (
        "Este canal procesa automáticamente cualquier paquete `.zip` que subas, actualizando en caliente el código de producción sin requerir acceso al panel de control ni SFTP.\n\n"
        "**Mecanismo de Despliegue Seguro (Pipeline):**\n"
        "`1️⃣` Arrastra y sube el archivo `.zip` directamente a este canal.\n"
        "`2️⃣` El bot descarga el archivo en un entorno sandbox aislado y verifica que no contenga rutas maliciosas (Zip Slip) ni sobrescriba datos vivos.\n"
        "`3️⃣` Se ejecuta una compilación estricta de prueba (`py_compile`) sobre cada archivo `.py`. Si hay un solo error de sintaxis, el despliegue se cancela inmediatamente manteniendo la versión previa activa (cero caídas del servidor).\n"
        "`4️⃣` Se calcula el hash SHA-256 de cada archivo: se crea backup `.bak` previo y se reemplazan **únicamente los archivos que hayan cambiado**.\n"
        f"`5️⃣` Se reinicia el proceso del bot en memoria (`os.execv`) y se publica el reporte detallado en <#{log_channel_id}>.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "### 📋 Prompt Universal para cualquier IA Externa\n"
        "Copia y pega este prompt a cualquier IA (ChatGPT, Claude, DeepSeek, etc.) para que te devuelva el ZIP en el formato exacto requerido:"
    ),
    "color": 16762880,
    "fields": [
        {
            "name": "🤖 Prompt para la IA Externa (Copiar y Pegar)",
            "value": f"```{master_prompt}```",
            "inline": False
        },
        {
            "name": "📌 Requisitos de Aceptación del ZIP",
            "value": (
                "> `✅` Archivos planos en la raíz del zip (sin subcarpetas).\n"
                "> `✅` Compatible con Python 3.12.\n"
                "> `⛔` Sin `.env` ni `*_db.json` (protegidos por seguridad).\n"
                "> `🔔` Feedback instantáneo: Reacción `⏳` (procesando) → `✅` (éxito) o `❌` (error)."
            ),
            "inline": False
        }
    ],
    "footer": {
        "text": "ThunderMC Automation Engine • Despliegues Autónomos Seguros"
    }
}

url = f"https://discord.com/api/v10/channels/{channel_id}/pins"
req = urllib.request.Request(url, headers=headers, method="GET")
with urllib.request.urlopen(req) as resp:
    pins = json.loads(resp.read().decode("utf-8"))
    for pin in pins:
        pid = pin.get("id")
        edit_url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{pid}"
        edit_data = json.dumps({"embeds": [embed]}).encode("utf-8")
        edit_req = urllib.request.Request(edit_url, data=edit_data, headers=headers, method="PATCH")
        with urllib.request.urlopen(edit_req) as edit_resp:
            print("Successfully updated pinned message ID:", pid)
