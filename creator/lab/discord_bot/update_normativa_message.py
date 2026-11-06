import os
import json
import requests

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
env_path = os.path.join(script_dir, ".env")

token = ""
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

thread_id = "1568202151186927646"
img_path = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\minecraft_knowledge_book.png"

headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 1.0.0)"
}

# 1. Borrar mensajes antiguos en el hilo
res_list = requests.get(f"https://discord.com/api/v10/channels/{thread_id}/messages?limit=10", headers=headers)
if res_list.status_code == 200:
    for m in res_list.json():
        if m.get("type") == 0:
            del_res = requests.delete(f"https://discord.com/api/v10/channels/{thread_id}/messages/{m['id']}", headers=headers)
            print(f"Mensaje {m['id']} eliminado: status {del_res.status_code}")

# 2. Preparar el payload completo con dropdown y botones
payload = {
    "flags": 32768,
    "allowed_mentions": {
        "parse": []
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
                                "## <:th_normativa_w:1568228499129630740> Normativa Oficial⸻\n"
                                "-# ᴄᴏɴᴏᴄᴇ ᴇʟ ʀᴇɢʟᴀᴍᴇɴᴛᴏ ᴘᴀʀᴀ ᴜɴᴀ ᴇxᴘᴇʀɪᴇɴᴄɪᴀ ʟɪᴍᴘɪᴀ, ᴊᴜꜱᴛᴀ ʏ ꜱᴇɢᴜʀᴀ\n\n"
                                "`⚠️` **Aviso Importante**\n"
                                "> Al acceder a ThunderMC, aceptas cumplir estas normas. Las reglas pueden modificarse en cualquier momento y el criterio del staff prevalece ante situaciones no contempladas explícitamente en este documento.\n\n"
                                "`📝` **Cláusula de criterio del staff:** \n"
                                "> Cualquier comportamiento que rompa la experiencia de juego, sea considerado injusto o vaya contra el espíritu del servidor puede ser sancionado aunque no esté escrito explícitamente en estas normas, siempre bajo el criterio del staff.\n\n"
                                "Nuestro objetivo es mantener un ambiente competitivo, divertido y justo, no limitar la experiencia del jugador."
                            )
                        }
                    ],
                    "accessory": {
                        "type": 11,
                        "media": {
                            "url": "attachment://minecraft_knowledge_book.png"
                        }
                    }
                }
            ]
        },
        {
            "type": 1,
            "components": [
                {
                    "type": 3,
                    "custom_id": "select_reglas_normativa",
                    "placeholder": "Selecciona qué reglamento deseas consultar...",
                    "options": [
                        {
                            "label": "Reglas Generales",
                            "value": "reglas_generales",
                            "description": "Normas de convivencia, sanciones, chat y juego limpio",
                            "emoji": {
                                "id": "1568228500262096937",
                                "name": "th_reglas_gen_w"
                            }
                        },
                        {
                            "label": "Reglas de Discord",
                            "value": "reglas_discord",
                            "description": "Normativa específica para la comunidad de Discord",
                            "emoji": {
                                "id": "1568228501729845368",
                                "name": "th_reglas_dc_w"
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
                    "url": "https://discord.com/channels/1552715004669726802/1552723526996336724/1568202169633603704",
                    "emoji": {
                        "name": "⬅️"
                    }
                },
                {
                    "type": 2,
                    "style": 5,
                    "label": "Reportar Infracción (Ticket)",
                    "url": "https://discord.com/channels/1552715004669726802/1374644365758169178",
                    "emoji": {
                        "name": "⚠️"
                    }
                }
            ]
        }
    ],
    "attachments": [
        {
            "id": 0,
            "filename": "minecraft_knowledge_book.png"
        }
    ]
}

# 3. Enviar multipart a Discord
with open(img_path, "rb") as f_img:
    files = {
        "files[0]": ("minecraft_knowledge_book.png", f_img, "image/png")
    }
    data = {
        "payload_json": json.dumps(payload, ensure_ascii=False)
    }
    
    post_res = requests.post(
        f"https://discord.com/api/v10/channels/{thread_id}/messages",
        headers=headers,
        data=data,
        files=files
    )

print(f"Status POST: {post_res.status_code}")
res_json = post_res.json()
print("Respuesta:", json.dumps(res_json, indent=2, ensure_ascii=False))

# Si fue exitoso, obtener la URL persistente asignada por Discord y actualizar los archivos locales
if post_res.status_code in [200, 201]:
    cdn_url = ""
    if res_json.get("attachments") and len(res_json["attachments"]) > 0:
        cdn_url = res_json["attachments"][0]["url"]
        print(f"CDN URL permanente obtenida: {cdn_url}")
    
    # Payload para exportar (con URL de CDN fija si se necesita importar externamente)
    clean_payload = {
        "flags": 32768,
        "allowed_mentions": {
            "parse": []
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
                                "content": payload["components"][0]["components"][0]["components"][0]["content"]
                            }
                        ],
                        "accessory": {
                            "type": 11,
                            "media": {
                                "url": cdn_url if cdn_url else "attachment://minecraft_knowledge_book.png"
                            }
                        }
                    }
                ]
            },
            payload["components"][1], # Dropdown
            payload["components"][2]  # Botones
        ]
    }

    # Guardar en output/discord y en descargas/reglas
    out_file1 = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\menu_normativa_v2.json"
    with open(out_file1, "w", encoding="utf-8") as f:
        json.dump(clean_payload, f, ensure_ascii=False, indent=2)

    out_file2 = r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\normativa oficial v2.json"
    with open(out_file2, "w", encoding="utf-8") as f:
        json.dump(clean_payload, f, ensure_ascii=False, indent=2)

    print("Archivos JSON actualizados exitosamente.")
