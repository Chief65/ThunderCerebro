#!/usr/bin/env python3
"""
Despliega el diseño simplificado del Portal en #embeds:
- GIF superior: cartel-thundermc-degradado-tag-v5_1.gif (Logo animado ThunderMC)
- Título: ## <:th_cartel_w:1568175356861743235> ThunderMC | ¡Juega a lo Grande! ⸻
- Icono minimalista #FFC800 de Minecraft Grass Block para Verificación Minecraft
- Texto conciso: "Conecta tu cuenta de Discord con Minecraft."
- Eliminado completamente el bloque previo de dungeons/jefes
"""

import os
import json
import urllib.request
import urllib.error

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
env_path = os.path.join(script_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

channel_id = "1552723526996336724"
msg_id = "1568202169633603704"
gif_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\cartel-thundermc-degradado-tag-v5_1.gif"
gif_name = "cartel_thundermc.gif"

mc_top = "<:qo_mc_tl:1569337083556790343><:qo_mc_tr:1569337086312579112>"
mc_bot = "<:qo_mc_bl:1569337088841875507><:qo_mc_br:1569337091513516164>"

# Componentes interactivos reutilizados
j_top = "<:qo_jugar_tl:1568267685660463234><:qo_jugar_tr:1568267692467818498>"
j_bot = "<:qo_jugar_bl:1568267699316986006><:qo_jugar_br:1568267705939660910>"

v_top = "<:qo_voz_tl:1568237980756213765><:qo_voz_tr:1568237988394176552>"
v_bot = "<:qo_voz_bl:1568237997672108052><:qo_voz_br:1568238004483399792>"

r_top = "<:qo_reglas_tl:1568238011794067466><:qo_reglas_tr:1568238018995949720>"
r_bot = "<:qo_reglas_bl:1568238026222731366><:qo_reglas_br:1568238033013047511>"

p_top = "<:qo_post_tl:1568238040021991437><:qo_post_tr:1568238047730995241>"
p_bot = "<:qo_post_bl:1568238054865637556><:qo_post_br:1568238061555556375>"

t_top = "<:qo_tienda_tl:1568238068941590600><:qo_tienda_tr:1568238077757882571>"
t_bot = "<:qo_tienda_bl:1568238085337120880><:qo_tienda_br:1568238093155180655>"

s_top = "<:qo_soporte_tl:1568238102051422288><:qo_soporte_tr:1568238110070808636>"
s_bot = "<:qo_soporte_bl:1568238119801720912><:qo_soporte_br:1568238128391786577>"

ir_emoji = {"id": "1568181296654590023", "name": "th_ir_w"}

def make_section(content, url):
    return {
        "type": 9,
        "components": [{"type": 10, "content": content}],
        "accessory": {
            "type": 2,
            "style": 5,
            "emoji": ir_emoji,
            "url": url
        }
    }

container_components = [
    # 1. GIF Logo animado ThunderMC
    {
        "type": 12,
        "items": [
            {
                "media": {
                    "url": f"attachment://{gif_name}"
                }
            }
        ]
    },
    # 2. Título simplificado unificado
    {
        "type": 10,
        "content": (
            "## <:th_cartel_w:1568175356861743235> ThunderMC | ¡Juega a lo Grande! ⸻\n"
            "-# Todo lo que necesitas tener a tu alcance aquí:"
        )
    },
    # 3. Secciones interactivas
    make_section(f"{j_top} **¿Cómo jugar?**\n{j_bot} Entra a jugar rápidamente.", "https://discord.com/channels/1552715004669726802/1568202142278352989"),
    make_section(f"{mc_top} **Verificación Minecraft**\n{mc_bot} Conecta tu cuenta de Discord con Minecraft.", "https://discord.com/channels/1552715004669726802/1568311086321631273"),
    make_section(f"{v_top} **Chat de Voz**\n{v_bot} Comunícate por proximidad.", "https://discord.com/channels/1552715004669726802/1568202146611204137"),
    make_section(f"{r_top} **Normativa Oficial**\n{r_bot} Conoce el reglamento.", "https://discord.com/channels/1552715004669726802/1568202151186927646"),
    make_section(f"{p_top} **Postulaciones**\n{p_bot} Postúlate para entrar a nuestro equipo", "https://discord.com/channels/1552715004669726802/1568202156090073101"),
    make_section(f"{t_top} **Tienda Oficial**\n{t_bot} Visita nuestra tienda web.", "https://tienda.thundermc.es/"),
    make_section(f"{s_top} **Soporte Flash**\n{s_bot} Abre un ticket para recibir soporte", "https://discord.com/channels/1552715004669726802/1374644365758169178"),
    # 4. Separadores
    {"type": 14, "divider": False, "spacing": 1},
    {"type": 14, "divider": True, "spacing": 2},
    # 5. Footer con Logo Thunder de 10 partes
    {
        "type": 10,
        "content": (
            "<:th52_1:1568184263633805392><:th52_2:1568184265739604088><:th52_3:1568184268025241611><:th52_4:1568184270152015893><:th52_5:1568184272651550780>⠀ **Links Interesantes:**\n"
            "<:th52_6:1568184274748837928><:th52_7:1568184276766429234><:th52_8:1568184278720970815><:th52_9:1568184281203871754><:th52_10:1568184283087241218>⠀ [Tienda](https://tienda.thundermc.es/) • [Tiktok](https://www.tiktok.com/@somosthundermc_?lang=es) • [YouTube](https://www.youtube.com/@somosthundermc/featured)"
        )
    }
]

payload = {
    "flags": 32768,
    "allowed_mentions": {"parse": []},
    "components": [
        {
            "type": 17,
            "components": container_components
        }
    ]
}

# Guardar archivos JSON
p1 = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_thundermc_v2.json"
p2 = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_info_components_v2.json"

with open(p1, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

with open(p2, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print("JSONs guardados exitosamente. Preparando envío multipart...")

# Enviar PATCH multipart
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

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("SUCCESS! Mensaje actualizado en Discord.")
        media = res["components"][0]["components"][0]["items"][0]["media"]
        print(f"Media dimensions: {media.get('width')}x{media.get('height')}")
        print(f"Media URL: {media.get('url')[:80]}...")
except urllib.error.HTTPError as e:
    err_body = e.read().decode("utf-8", errors="replace")
    print(f"HTTP Error {e.code}: {err_body}")
