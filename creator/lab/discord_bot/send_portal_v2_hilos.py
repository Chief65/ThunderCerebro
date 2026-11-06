import os
import json
import time
import base64
import urllib.request

script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

token = None
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

guild_id = "1552715004669726802"
channel_id = "1552723526996336724"
app_id = "1552716487100342404"
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
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP Error {e.code} on {method} {endpoint}: {err_body}")
        raise

def discord_api_multipart(endpoint, body, file_path, file_name, mime_type="image/gif"):
    url = f"https://discord.com/api/v10{endpoint}"
    boundary = "----ThunderBoundary7MA4YWxkTrZu0gW"
    parts = []
    # Parte 1: payload_json
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="payload_json"\r\n'
        f"Content-Type: application/json; charset=utf-8\r\n\r\n"
        f"{json.dumps(body, ensure_ascii=False)}\r\n".encode("utf-8")
    )
    # Parte 2: files[0]
    with open(file_path, "rb") as bf:
        file_bytes = bf.read()
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files[0]"; filename="{file_name}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8")
        + file_bytes
        + f"\r\n--{boundary}--\r\n".encode("utf-8")
    )
    data = b"".join(parts)
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": user_agent,
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP Error {e.code} on POST {endpoint}: {err_body}")
        raise

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"

# 1. Títulos blancos (flechas cartel arriba en ThunderMC + libro guía en Información), botón de ir blanco, iconos de botones del footer blancos (carrito + tiktok + youtube) + Logo THUNDER en 10 partes (5x2)
icon_files = {
    "cartel_w":     ("th_cartel_w",     os.path.join(icons_dir, "icon_cartel_w.png"),     "image/png"),
    "libro_w":      ("th_libro_w",      os.path.join(icons_dir, "icon_libro_w.png"),      "image/png"),
    "ir_w":         ("th_ir_w",         os.path.join(icons_dir, "icon_ir_w.png"),         "image/png"),
    "carrito_w":    ("th_carrito_w",    os.path.join(icons_dir, "icon_carrito_w.png"),    "image/png"),
    "tiktok_w":     ("th_tiktok_w",     os.path.join(icons_dir, "icon_tiktok_w.png"),     "image/png"),
    "youtube_w":    ("th_youtube_w",    os.path.join(icons_dir, "icon_youtube_w.png"),    "image/png"),
}

for i in range(1, 11):
    icon_files[f"th52_{i}"] = (f"th52_{i}", os.path.join(icons_dir, f"anchored_thunder_5x2_limpio_{i}.png"), "image/png")

# 2. Cinco iconos 2x2 principales (20 fragmentos) en AMARILLO-ANARANJADO (#FFC800 -> qo_*)
for prefix in ("jugar", "voz", "reglas", "post", "soporte"):
    for q in ("tl", "tr", "bl", "br"):
        key = f"{prefix}_{q}"
        ename = f"qo_{prefix}_{q}"
        fpath = os.path.join(icons_dir, f"quad_{prefix}_{q}.png")
        icon_files[key] = (ename, fpath, "image/png")

print("0. Sincronizando emojis en Discord (títulos actualizados + carrito de compra + logo 10 partes 5x2)...")
existing_emojis_resp = discord_api("GET", f"/applications/{app_id}/emojis")
existing_emojis = {e["name"]: e["id"] for e in existing_emojis_resp.get("items", [])}

# Eliminar emojis antiguos que ya no se usan para mantener limpio el panel
for ename, eid in list(existing_emojis.items()):
    if ename in ("th_tienda_w", "th_bienvenida_w"):
        try:
            discord_api("DELETE", f"/applications/{app_id}/emojis/{eid}")
            del existing_emojis[ename]
            print(f"   Emoji antiguo eliminado: :{ename}:")
            time.sleep(0.15)
        except Exception:
            pass

emoji_ids = {}
for key, (ename, fpath, mime) in icon_files.items():
    if ename in existing_emojis:
        emoji_ids[key] = existing_emojis[ename]
        print(f"   Emoji existente reutilizado: :{ename}: -> {emoji_ids[key]}")
    else:
        with open(fpath, "rb") as bf:
            b64 = base64.b64encode(bf.read()).decode("ascii")
        res = discord_api("POST", f"/applications/{app_id}/emojis", {
            "name": ename,
            "image": f"data:{mime};base64,{b64}"
        })
        emoji_ids[key] = res["id"]
        print(f"   Emoji subido: :{ename}: -> {res['id']}")
        time.sleep(0.2)

# Limpiar mensaje y hilos anteriores de #embeds
old_ids_to_clean = [
    ("message", "1568201387836317700"),
    ("thread",  "1568201360854351932"),
    ("thread",  "1568201364851658844"),
    ("thread",  "1568201370752917635"),
    ("thread",  "1568201375387615272"),
    ("thread",  "1568201381146398740"),
]
for kind, oid in old_ids_to_clean:
    try:
        if kind == "message":
            discord_api("DELETE", f"/channels/{channel_id}/messages/{oid}")
        else:
            discord_api("DELETE", f"/channels/{oid}")
    except Exception:
        pass

print("1. Creando los 5 hilos informativos en #embeds...")
threads_to_create = [
    ("jugar",         "🕹️・empezar-a-jugar"),
    ("voicechat",     "🎙️・chat-de-voz"),
    ("reglas",        "📜・normativa-y-reglas"),
    ("postulaciones", "🔎・postulaciones"),
    ("tickets",       "🎫・soporte-y-tickets"),
]

thread_ids = {}
for key, name in threads_to_create:
    res = discord_api("POST", f"/channels/{channel_id}/threads", {
        "name": name,
        "auto_archive_duration": 10080,
        "type": 11
    })
    tid = res["id"]
    thread_ids[key] = tid
    print(f"   Hilo creado: {name} -> {tid}")
    try:
        discord_api("DELETE", f"/channels/{channel_id}/messages/{tid}")
    except Exception:
        pass
    time.sleep(0.35)

url_jugar         = f"https://discord.com/channels/{guild_id}/{thread_ids['jugar']}"
url_voicechat     = f"https://discord.com/channels/{guild_id}/{thread_ids['voicechat']}"
url_reglas        = f"https://discord.com/channels/{guild_id}/{thread_ids['reglas']}"
url_postulaciones = f"https://discord.com/channels/{guild_id}/{thread_ids['postulaciones']}"
url_tickets       = f"https://discord.com/channels/{guild_id}/1374644365758169178"

em_cartel_w = f"<:th_cartel_w:{emoji_ids['cartel_w']}>"
em_libro_w  = f"<:th_libro_w:{emoji_ids['libro_w']}>"

# Nuevo logo de Thunder dividido en 10 partes (5 arriba + 5 abajo)
logo_10_top = (
    f"<:th52_1:{emoji_ids['th52_1']}>"
    f"<:th52_2:{emoji_ids['th52_2']}>"
    f"<:th52_3:{emoji_ids['th52_3']}>"
    f"<:th52_4:{emoji_ids['th52_4']}>"
    f"<:th52_5:{emoji_ids['th52_5']}>"
)
logo_10_bot = (
    f"<:th52_6:{emoji_ids['th52_6']}>"
    f"<:th52_7:{emoji_ids['th52_7']}>"
    f"<:th52_8:{emoji_ids['th52_8']}>"
    f"<:th52_9:{emoji_ids['th52_9']}>"
    f"<:th52_10:{emoji_ids['th52_10']}>"
)

def quad_str(prefix, tag_prefix="qo"):
    tl = f"<:{tag_prefix}_{prefix}_tl:{emoji_ids[f'{prefix}_tl']}>"
    tr = f"<:{tag_prefix}_{prefix}_tr:{emoji_ids[f'{prefix}_tr']}>"
    bl = f"<:{tag_prefix}_{prefix}_bl:{emoji_ids[f'{prefix}_bl']}>"
    br = f"<:{tag_prefix}_{prefix}_br:{emoji_ids[f'{prefix}_br']}>"
    return f"{tl}{tr}", f"{bl}{br}"

j_top, j_bot = quad_str("jugar", "qo")
v_top, v_bot = quad_str("voz", "qo")
r_top, r_bot = quad_str("reglas", "qo")
p_top, p_bot = quad_str("post", "qo")
s_top, s_bot = quad_str("soporte", "qo")

LINEA_FINA = "⸻"
COLOR_FEEB00 = 16762880  # #FFC800 para los embeds internos de los hilos

def go_button(target_url):
    return {
        "type": 2,
        "style": 5,
        "emoji": {
            "id": emoji_ids["ir_w"],
            "name": "th_ir_w"
        },
        "url": target_url
    }

print("2. Construyendo payload Components v2...")
v2_payload = {
    "flags": 32768,
    "allowed_mentions": {
        "parse": [
            "everyone"
        ]
    },
    "components": [
        # CONTENEDOR 1: GIF recortado de pollitos arriba + ThunderMC (con el icono de las flechas th_cartel_w a su lado)
        {
            "type": 17,
            "components": [
                {
                    "type": 12,
                    "items": [
                        {
                            "media": {
                                "url": "attachment://stampede_wide.gif"
                            }
                        }
                    ]
                },
                {
                    "type": 10,
                    "content": (
                        f"## {em_cartel_w} ThunderMC {LINEA_FINA}\n"
                        "**¡Juega a lo Grande!**\n"
                        "Sumérgete en un mundo donde las mazmorras y los jefes son la mecánica principal.\n\n"
                        "> `🏰` **Dungeons Únicas:** Explora mazmorras inmersivas diseñadas al detalle con desafíos y recompensas exclusivas.\n"
                        "> `🐉` **Jefes Custom:** Enfréntate a criaturas colosales con mecánicas, fases de combate y ataques propios.\n"
                        "> `🔮` **Objetos Mágicos:** Forja y colecciona armas, armaduras y reliquias con habilidades especiales.\n"
                        "> `🎍` **Y mucho más:** Economía balanceada, eventos dinámicos y actualizaciones constantes junto a la comunidad.\n\n"
                        "**Juega donde quieras**\n"
                        "Entra desde Java 1.21.1+ (IP: `thundermc.es`) o Bedrock (Puerto: `19132`)"
                    )
                }
            ]
        },
        # CONTENEDOR 2: Información (con el icono de libro guía th_libro_w donde iban las flechas)
        {
            "type": 17,
            "components": [
                {
                    "type": 10,
                    "content": (
                        f"## {em_libro_w} Información {LINEA_FINA}\n"
                        "-# Todo lo que necesitas tener a tu alcance aquí:"
                    )
                },
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": f"{j_top} **¿Cómo jugar?**\n{j_bot} Entra a jugar rápidamente."
                        }
                    ],
                    "accessory": go_button(url_jugar)
                },
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": f"{v_top} **Chat de Voz**\n{v_bot} Instala y configura Simple Voice Chat. "
                        }
                    ],
                    "accessory": go_button(url_voicechat)
                },
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": f"{r_top} **Normativa Oficial**\n{r_bot} Conoce el reglamento."
                        }
                    ],
                    "accessory": go_button(url_reglas)
                },
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": f"{p_top} **Postulaciones**\n{p_bot} Postúlate para entrar a nuestro equipo"
                        }
                    ],
                    "accessory": go_button(url_postulaciones)
                },
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": f"{s_top} **Soporte Flash**\n{s_bot} Abre un ticket para recibir soporte"
                        }
                    ],
                    "accessory": go_button(url_tickets)
                },
                # Espaciador extra + línea divisoria amplia para separar bien Soporte y Tickets del footer
                {
                    "type": 14,
                    "divider": False,
                    "spacing": 1
                },
                {
                    "type": 14,
                    "divider": True,
                    "spacing": 2
                },
                # Footer con el logo de 10 partes y únicamente Links Interesantes (Tienda • Tiktok • YouTube) a su derecha
                {
                    "type": 10,
                    "content": (
                        f"{logo_10_top}⠀ **Links Interesantes:**\n"
                        f"{logo_10_bot}⠀ [Tienda](https://tienda.thundermc.es/) • [Tiktok](https://www.tiktok.com/@somosthundermc_?lang=es) • [YouTube](https://www.youtube.com/@somosthundermc/featured)"
                    )
                }
            ]
        }
    ]
}

payload_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_info_components_v2.json"
with open(payload_path, "w", encoding="utf-8") as f:
    json.dump(v2_payload, f, ensure_ascii=False, indent=2)

print("3. Enviando mensaje principal Components v2 (con stampede_wide.gif) a #embeds...")
gif_path = os.path.join(script_dir, "stampede_wide.gif")
main_msg = discord_api_multipart(f"/channels/{channel_id}/messages", v2_payload, gif_path, "stampede_wide.gif", "image/gif")
main_msg_id = main_msg["id"]
back_url = f"https://discord.com/channels/{guild_id}/{channel_id}/{main_msg_id}"
print(f"   SUCCESS: Mensaje principal enviado con ID: {main_msg_id}")
print(f"   URL de retorno: {back_url}")

print("4. Poblando los 5 hilos con sus Embeds informativos + Botón de Volver Atrás...")

# Hilo 1: Empezar a Jugar (Components v2 sin barra de color y sin imagen grande)
discord_api("POST", f"/channels/{thread_ids['jugar']}/messages", {
    "flags": 32768,
    "allowed_mentions": {
        "parse": [
            "everyone"
        ]
    },
    "components": [
        {
            "type": 17,
            "components": [
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": (
                                "### 👋 ¡Bienvenid@ a ThunderMC!\n"
                                "¡Estamos muy felices de que estés aquí!\n"
                                "-# ᴇᴍᴘɪᴇᴢᴀ ᴛᴜ ᴀᴠᴇɴᴛᴜʀᴀ ᴜɴɪᴇɴᴅᴏᴛᴇ ᴀʟ ꜱᴇʀᴠɪᴅᴏʀ\n\n"
                                "**Encontraras:**\n"
                                "`🏰` Dungeons Unicas\n"
                                "`🐉` Jefes Custom\n"
                                "`🔮` Objetos Magicos\n"
                                "`🎍` Y mucho más"
                            )
                        }
                    ],
                    "accessory": {
                        "type": 11,
                        "media": {
                            "url": "https://cdn.discordapp.com/attachments/1552723526996336724/1560474539547299901/minecraft_compass_transparent.png?ex=6aee882a&is=6aed36aa&hm=26bfe9a9a2dd5bdde582e426e6958b6fb095e524ad1fe597e06460f7ae1b8bd1&"
                        }
                    }
                },
                {
                    "type": 10,
                    "content": (
                        "↓ IP del Servidor (Version 1.21.1+  ) ↓\n"
                        "```text\nthundermc.es\n```\n"
                        "-# 📱 Puerto Bedrock: `19132` | 🎮 Java: Puerto por defecto\n\n"
                        "**Links Interesantes:**\n"
                        "-# [Tienda](https://tienda.thundermc.es/) • [Tiktok](https://www.tiktok.com/@somosthundermc_?lang=es) • [YouTube](https://www.youtube.com/@somosthundermc/featured)"
                    )
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
                    "emoji": {"name": "⬅️"},
                    "url": back_url
                }
            ]
        }
    ]
})

# Hilo 2: Chat de Voz (Components v2 sin barra de color y sin imagen grande)
discord_api("POST", f"/channels/{thread_ids['voicechat']}/messages", {
    "flags": 32768,
    "allowed_mentions": {
        "parse": [
            "everyone"
        ]
    },
    "components": [
        {
            "type": 17,
            "components": [
                {
                    "type": 9,
                    "components": [
                        {
                            "type": 10,
                            "content": (
                                "### 🎙️ Chat de Voz por Proximidad\n"
                                "¡Habla y escucha a los jugadores cercanos dentro del juego!\n"
                                "-# ᴄᴏᴍᴜɴɪ́ᴄᴀᴛᴇ ᴇɴ ᴛɪᴇᴍᴘᴏ ʀᴇᴀʟ ᴄᴏɴ ʟᴀ ᴄᴏᴍᴜɴɪᴅᴀᴅ\n\n"
                                "**Instalación (Solo Java):**\n"
                                "`1️⃣` Descarga **Simple Voice Chat** (Versión 1.21+) para Fabric o Forge.\n"
                                "`2️⃣` Arrastra el mod a tu carpeta `.minecraft/mods`.\n"
                                "`3️⃣` Entra al servidor y presiona la tecla `V` para configurar tu micrófono."
                            )
                        }
                    ],
                    "accessory": {
                        "type": 11,
                        "media": {
                            "url": "https://discord-webhook.com/uploads/41b520d24d1e2e07d03a472e445a83ef.png"
                        }
                    }
                },
                {
                    "type": 10,
                    "content": (
                        "**Compatibilidad:**\n"
                        "`💻` **Java:** Compatible con voz por proximidad y canales de grupo.\n"
                        "`📱` **Bedrock:** El mod no está disponible para Bedrock. ¡Únete a los **canales de voz de Discord** para hablar mientras juegas!\n\n"
                        "> Ver tutorial recomendado: [¡Click Aquí!](https://www.youtube.com/watch?v=nEVSaJjMPKs)\n\n"
                        "↓ IP del Servidor (Version 1.21.1+  ) ↓\n"
                        "```text\nthundermc.es\n```\n"
                        "-# 📱 Puerto Bedrock: `19132` | 🎮 Java: Puerto por defecto\n\n"
                        "-# [Tienda](https://tienda.thundermc.es/) • [Tiktok](https://www.tiktok.com/@somosthundermc_?lang=es) • [YouTube](https://www.youtube.com/@somosthundermc/featured)"
                    )
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
                    "emoji": {"name": "⬅️"},
                    "url": back_url
                },
                {
                    "type": 2,
                    "style": 5,
                    "label": "Descargar Simple Voice Chat (Modrinth)",
                    "emoji": {"name": "📥"},
                    "url": "https://modrinth.com/mod/simple-voice-chat"
                }
            ]
        }
    ]
})

# Hilo 3: Normativa y Reglas (Components v2 actualizado según especificación del Sr Ramos)
with open(r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\menu_normativa_v2.json", "r", encoding="utf-8") as f:
    normativa_v2_payload = json.load(f)

discord_api("POST", f"/channels/{thread_ids['reglas']}/messages", normativa_v2_payload)

# Hilo 4: Postulaciones
discord_api("POST", f"/channels/{thread_ids['postulaciones']}/messages", {
    "embeds": [
        {
            "title": "🔎 Postulaciones al Staff | ThunderMC",
            "description": (
                "¿Te gustaría formar parte del equipo de Moderación y Soporte de ThunderMC?\n"
                "-# ᴜɴᴇᴛᴇ ᴀ ɴᴜᴇꜱᴛʀᴏ ᴇQᴜɪᴘᴏ ᴏꜰɪᴄɪᴀʟ\n\n"
                "**Requisitos Principales:**\n"
                "`✅` Conocimiento sólido de las mecánicas del servidor y su normativa.\n"
                "`🎙️` Disponer de micrófono funcional y disponibilidad en Discord.\n"
                "`⚖️` Madurez, imparcialidad y trato respetuoso hacia los jugadores.\n"
                "`🛡️` Historial libre de sanciones graves dentro de la red.\n\n"
                "> 📝 Cuando las convocatorias estén abiertas, podrás enviar tu formulario desde el canal de tickets o avisos oficiales."
            ),
            "color": COLOR_FEEB00
        }
    ],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 5,
                    "label": "Volver al Inicio",
                    "emoji": {"name": "⬅️"},
                    "url": back_url
                }
            ]
        }
    ]
})

# Hilo 5: Soporte y Tickets
discord_api("POST", f"/channels/{thread_ids['tickets']}/messages", {
    "embeds": [
        {
            "title": "🎫 Soporte Flash V.1 | ThunderMC",
            "description": (
                "¿Necesitas asistencia técnica, reportar a un jugador o ayuda con una compra de la tienda?\n"
                "-# ᴀᴛᴇɴᴄɪᴏɴ ᴏꜰɪᴄɪᴀʟ ʏ ʀᴇꜱᴏʟᴜᴄɪᴏɴ ᴅᴇ ɪɴᴄɪᴅᴇɴᴄɪᴀꜱ\n\n"
                "**¿Cómo funciona nuestro soporte?**\n"
                "`1️⃣` Dirígete al canal de soporte o pulsa el botón de apertura de ticket.\n"
                "`2️⃣` Describe tu caso adjuntando pruebas (capturas o vídeo si es un reporte).\n"
                "`3️⃣` Un miembro del Staff te atenderá de forma privada a la mayor brevedad.\n\n"
                "> ⚠️ Por favor, evita abrir múltiples tickets por el mismo motivo."
            ),
            "color": COLOR_FEEB00
        }
    ],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 5,
                    "label": "Volver al Inicio",
                    "emoji": {"name": "⬅️"},
                    "url": back_url
                }
            ]
        }
    ]
})

print("DONE! Todo el flujo actualizado y enviado a #embeds.")
