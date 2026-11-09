#!/usr/bin/env python3
import os
import json
import time
import base64
import urllib.request
import urllib.error
from PIL import Image

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
env_path = os.path.join(script_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

app_id = "1552716487100342404"
channel_id = "1552723526996336724"
msg_id = "1568202169633603704"

headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 2.0.0)",
    "Content-Type": "application/json; charset=utf-8"
}

def discord_api(method, endpoint, body=None):
    url = f"https://discord.com/api/v10{endpoint}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        res = resp.read().decode("utf-8")
        return json.loads(res) if res else {}

# 1. Eliminar emojis anteriores de qo_mc_*
print("1. Buscando y eliminando emojis antiguos qo_mc_*...")
existing = discord_api("GET", f"/applications/{app_id}/emojis")
for e in existing.get("items", []):
    if e["name"].startswith("qo_mc_"):
        print(f"   Eliminando {e['name']} ({e['id']})...")
        discord_api("DELETE", f"/applications/{app_id}/emojis/{e['id']}")
        time.sleep(0.25)

# 2. Generar los 4 cuadrantes del auténtico Grass Block de Minecraft
print("2. Procesando grass_block.png...")
src_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\grass_block.png"
im = Image.open(src_path).convert("RGBA")
bbox = im.getbbox()
cropped = im.crop(bbox)
w, h = cropped.size
max_dim = max(w, h)
pad = int(max_dim * 0.04)
side = max_dim + pad * 2

sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(cropped, ((side - w) // 2, (side - h) // 2))
master = sq.resize((256, 256), Image.Resampling.LANCZOS)
master.save(os.path.join(icons_dir, "master_grass_block_256.png"))

def add_anchors(tile):
    px = tile.load()
    w, h = tile.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if px[x, y][3] == 0:
            px[x, y] = (0, 0, 0, 1)  # Pixel invisible de anclaje
    return tile

quads = {
    "tl": add_anchors(master.crop((0,   0,   128, 128))),
    "tr": add_anchors(master.crop((128, 0,   256, 128))),
    "bl": add_anchors(master.crop((0,   128, 128, 256))),
    "br": add_anchors(master.crop((128, 128, 256, 256))),
}

emoji_ids = {}
for qname, tile in quads.items():
    p = os.path.join(icons_dir, f"quad_mc_{qname}.png")
    tile.save(p, "PNG")
    ename = f"qo_mc_{qname}"
    with open(p, "rb") as bf:
        b64 = base64.b64encode(bf.read()).decode("ascii")
    
    res = discord_api("POST", f"/applications/{app_id}/emojis", {
        "name": ename,
        "image": f"data:image/png;base64,{b64}"
    })
    emoji_ids[qname] = res["id"]
    print(f"   Subido {ename} -> {res['id']}")
    time.sleep(0.3)

mc_top = f"<:qo_mc_tl:{emoji_ids['tl']}><:qo_mc_tr:{emoji_ids['tr']}>"
mc_bot = f"<:qo_mc_bl:{emoji_ids['bl']}><:qo_mc_br:{emoji_ids['br']}>"
print(f"3. Emojis ensamblados: {mc_top} / {mc_bot}")

# 3. Cargar y actualizar portal_thundermc_v2.json
payload_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_thundermc_v2.json"
with open(payload_file, "r", encoding="utf-8") as f:
    payload = json.load(f)

# Asegurar media attachment para el GIF
payload["components"][0]["components"][0]["items"][0]["media"] = {
    "url": "attachment://stampede_wide.gif"
}

# Modificar el texto de verificación
for comp in payload["components"][0]["components"]:
    if comp.get("type") == 9:
        for inner in comp.get("components", []):
            if "Verificación Minecraft" in inner.get("content", ""):
                inner["content"] = f"{mc_top} **Verificación Minecraft**\n{mc_bot} Conecta tu cuenta de Discord con Minecraft."
                print("   Sección Verificación actualizada con nuevo texto y emojis!")

# Guardar en local
with open(payload_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

info_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_info_components_v2.json"
with open(info_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

# 4. Enviar PATCH con multipart incluyendo stampede_wide.gif
print("4. Enviando PATCH multipart con stampede_wide.gif a Discord...")
gif_path = os.path.join(script_dir, "stampede_wide.gif")
boundary = "----ThunderBoundary7MA4YWxkTrZu0gW"
parts = []

parts.append(
    f"--{boundary}\r\n".encode("utf-8")
    + b'Content-Disposition: form-data; name="payload_json"\r\n'
    + b'Content-Type: application/json; charset=utf-8\r\n\r\n'
    + json.dumps(payload, ensure_ascii=False).encode("utf-8")
    + b"\r\n"
)

with open(gif_path, "rb") as bf:
    gif_bytes = bf.read()

parts.append(
    f"--{boundary}\r\n".encode("utf-8")
    + b'Content-Disposition: form-data; name="files[0]"; filename="stampede_wide.gif"\r\n'
    + b'Content-Type: image/gif\r\n\r\n'
    + gif_bytes
    + f"\r\n--{boundary}--\r\n".encode("utf-8")
)

body_bytes = b"".join(parts)
patch_headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 2.0.0)",
    "Content-Type": f"multipart/form-data; boundary={boundary}"
}

patch_url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{msg_id}"
req = urllib.request.Request(patch_url, data=body_bytes, headers=patch_headers, method="PATCH")

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("SUCCESS! Mensaje actualizado en Discord.")
    print("Adjuntos en mensaje:", len(res.get("attachments", [])))
    if res.get("attachments"):
        print("URL del GIF:", res["attachments"][0].get("url"))
    print("Media en componente:", res["components"][0]["components"][0]["items"][0]["media"].get("url"))
