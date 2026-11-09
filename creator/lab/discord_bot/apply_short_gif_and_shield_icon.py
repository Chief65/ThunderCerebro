#!/usr/bin/env python3
import os
import json
import time
import base64
import urllib.request
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

# 1. Eliminar emojis anteriores qo_mc_*
print("1. Eliminando emojis anteriores qo_mc_*...")
existing = discord_api("GET", f"/applications/{app_id}/emojis")
for e in existing.get("items", []):
    if e.get("name", "").startswith("qo_mc_"):
        eid = e.get("id")
        print(f"   Eliminando {e['name']} ({eid})...")
        discord_api("DELETE", f"/applications/{app_id}/emojis/{eid}")
        time.sleep(0.2)

# 2. Rebanar el icono de Escudo de Verificación Minecraft con anclajes
print("2. Rebanando master_shield_check_256.png...")
master = Image.open(os.path.join(icons_dir, "master_shield_check_256.png")).convert("RGBA")

def add_corner_anchors(tile, rgb=(255, 200, 0)):
    px = tile.load()
    w, h = tile.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if px[x, y][3] == 0:
            px[x, y] = (rgb[0], rgb[1], rgb[2], 1)
    return tile

quads = {
    "tl": add_corner_anchors(master.crop((0,   0,   128, 128))),
    "tr": add_corner_anchors(master.crop((128, 0,   256, 128))),
    "bl": add_corner_anchors(master.crop((0,   128, 128, 256))),
    "br": add_corner_anchors(master.crop((128, 128, 256, 256))),
}

emoji_ids = {}
for qname, tile in quads.items():
    p = os.path.join(icons_dir, f"quad_shield_mc_{qname}.png")
    tile.save(p, "PNG")
    ename = f"qo_mc_{qname}"
    with open(p, "rb") as bf:
        b64 = base64.b64encode(bf.read()).decode("ascii")
    
    res = discord_api("POST", f"/applications/{app_id}/emojis", {
        "name": ename,
        "image": f"data:image/png;base64,{b64}"
    })
    eid = res.get("id")
    emoji_ids[qname] = eid
    print(f"   Subido {ename} -> {eid}")
    time.sleep(0.25)

mc_top = f"<:qo_mc_tl:{emoji_ids['tl']}><:qo_mc_tr:{emoji_ids['tr']}>"
mc_bot = f"<:qo_mc_bl:{emoji_ids['bl']}><:qo_mc_br:{emoji_ids['br']}>"

# 3. Actualizar JSON local
payload_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_thundermc_v2.json"
with open(payload_file, "r", encoding="utf-8") as f:
    payload = json.load(f)

# Asegurar nombre del archivo gif
gif_name = "cartel_thundermc_short.gif"
payload["components"][0]["components"][0]["items"][0]["media"] = {
    "url": f"attachment://{gif_name}"
}

# Actualizar contenido de la sección de verificación con los nuevos emojis
for comp in payload["components"][0]["components"]:
    if comp.get("type") == 9:
        for inner in comp.get("components", []):
            if "Verificación Minecraft" in inner.get("content", ""):
                inner["content"] = f"{mc_top} **Verificación Minecraft**\n{mc_bot} Conecta tu cuenta de Discord con Minecraft."
                break

with open(payload_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

info_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_info_components_v2.json"
with open(info_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("JSONs locales actualizados. Enviando PATCH a Discord con GIF recortado...")

# 4. Enviar PATCH multipart con el GIF recortado (964x270)
gif_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\cartel_thundermc_short.gif"
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
    + f'Content-Disposition: form-data; name="files[0]"; filename="{gif_name}"\r\n'.encode("utf-8")
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
    media = res["components"][0]["components"][0]["items"][0]["media"]
    print(f"Dimensiones GIF nuevo en Discord: {media.get('width')}x{media.get('height')}")
    print(f"URL: {media.get('url')[:70]}...")
