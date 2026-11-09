import os
import zipfile
import json
import urllib.request
from datetime import datetime, timezone

base_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
out_zip = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\fabio_codigo_actual.zip"
os.makedirs(r"C:\Users\PC\Desktop\ThunderCerebro\creator\output", exist_ok=True)

files_to_pack = [
    "gateway_bot.py",
    "main.py",
    "bot.py",
    "requirements.txt",
    "reglas_generales.json",
    "reglas_discord.json",
    "sorteo_config.json",
    "test_fabio.py",
    "README_DESPLIEGUE.md",
]

with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for fname in sorted(set(files_to_pack)):
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            zf.write(fpath, fname)
            print(f"Packed: {fname} ({os.path.getsize(fpath)} bytes)")

print(f"Package created: {out_zip} ({os.path.getsize(out_zip)} bytes)")

# Send updated ZIP to #admin-panel via PATCH
env_path = os.path.join(base_dir, ".env")
token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

channel_id = "1569343101544300664"
msg_id = "1569344094554292364"
url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_id}"

now_str = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
embed = {
    "title": "📦 Código Actual de Fabio en Producción (Descarga Directa)",
    "description": (
        "Este archivo representa la **versión activa y en tiempo real** del bot en el contenedor de Vultam.\n\n"
        "**Detalles del Paquete:**\n"
        "> `📁` Archivos incluidos: `gateway_bot.py`, `main.py`, `bot.py`, `requirements.txt` y configuraciones JSON.\n"
        "> `🛡️` **Excluidos:** `.env` y bases de datos vivas (`postulaciones_db.json`, `sorteos_db.json`).\n"
        "> `🔄` **Auto-Actualización:** Cada vez que se aplique un cambio exitoso en este canal, este mensaje se mantendrá al día con la última versión operativa."
    ),
    "color": 3066993,
    "footer": {
        "text": f"ThunderMC Bot • Producción Vultam (Miami) • Actualizado: {now_str}"
    }
}

boundary = "----ThunderBoundary7MA4YWxkTrZu0gW"
payload = {
    "embeds": [embed],
    "attachments": [{"id": 0, "filename": "fabio_codigo_actual.zip"}]
}

with open(out_zip, "rb") as bf:
    zip_bytes = bf.read()

parts = [
    f"--{boundary}\r\n".encode("utf-8")
    + b'Content-Disposition: form-data; name="payload_json"\r\n'
    + b'Content-Type: application/json; charset=utf-8\r\n\r\n'
    + json.dumps(payload, ensure_ascii=False).encode("utf-8")
    + b"\r\n",
    f"--{boundary}\r\n".encode("utf-8")
    + b'Content-Disposition: form-data; name="files[0]"; filename="fabio_codigo_actual.zip"\r\n'
    + b'Content-Type: application/zip\r\n\r\n'
    + zip_bytes
    + f"\r\n--{boundary}--\r\n".encode("utf-8")
]

body_bytes = b"".join(parts)
headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 2.0.0)",
    "Content-Type": f"multipart/form-data; boundary={boundary}"
}

req = urllib.request.Request(url, data=body_bytes, headers=headers, method="PATCH")
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("SUCCESS! Mensaje con ZIP actual actualizado en #admin-panel. ID:", res.get("id"))
