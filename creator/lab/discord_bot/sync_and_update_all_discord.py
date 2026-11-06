import os
import json
import base64
import time
import requests

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"

env_path = os.path.join(script_dir, ".env")
token = ""
with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("DISCORD_BOT_TOKEN="):
            token = line.split("=", 1)[1].strip()

app_id = "1552716487100342404"
channel_main_id = "1552723526996336724"
main_msg_id = "1568202169633603704"

thread_jugar_id = "1568202142278352989"
jugar_msg_id = "1568208495835226146"

headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 1.0.0)",
    "Content-Type": "application/json; charset=utf-8"
}

# 1. Obtener emojis existentes de la aplicación
existing = {e["name"]: e["id"] for e in requests.get(f"https://discord.com/api/v10/applications/{app_id}/emojis", headers=headers).json().get("items", [])}
print(f"Total emojis existentes en la aplicacion: {len(existing)}")

# Lista de emojis 2x2 a actualizar
emojis_map = {}
for name in ["jugar", "voz", "reglas", "post", "tienda", "soporte"]:
    for q in ["tl", "tr", "bl", "br"]:
        emojis_map[f"qo_{name}_{q}"] = os.path.join(icons_dir, f"quad_{name}_{q}.png")

emojis_map["th_jugar_w"] = os.path.join(icons_dir, "icon_jugar_w.png")

synced_ids = {}
for ename, fpath in emojis_map.items():
    with open(fpath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    # Si ya existe, podemos eliminarlo y recrearlo para que Discord refresque la imagen inmediatamente en la CDN
    if ename in existing:
        old_id = existing[ename]
        del_r = requests.delete(f"https://discord.com/api/v10/applications/{app_id}/emojis/{old_id}", headers=headers)
        time.sleep(0.15)

    post_r = requests.post(
        f"https://discord.com/api/v10/applications/{app_id}/emojis",
        headers=headers,
        json={"name": ename, "image": f"data:image/png;base64,{b64}"}
    )
    if post_r.status_code in (200, 201):
        new_id = post_r.json()["id"]
        synced_ids[ename] = new_id
        print(f"Emoji {ename} actualizado con nuevo ID: {new_id}")
    else:
        print(f"Error subiendo {ename}: {post_r.status_code} {post_r.text}")
    time.sleep(0.2)

# 2. Actualizar el Mensaje Principal en #embeds
r_main = requests.get(f"https://discord.com/api/v10/channels/{channel_main_id}/messages/{main_msg_id}", headers=headers)
main_data = r_main.json()
c2_components = main_data["components"][1]["components"]

# Actualizar cada sección con los nuevos IDs de emojis
sections_config = [
    ("¿Cómo jugar?", "jugar", "Entra a jugar rápidamente."),
    ("Chat de Voz", "voz", "Comunícate por proximidad."),
    ("Normativa", "reglas", "Reglas y directrices de juego."),
    ("Postulaciones", "post", "Únete al equipo de ThunderMC."),
    ("Tienda Oficial", "tienda", "Visita nuestra tienda web."),
    ("Soporte Flash", "soporte", "¿Problemas? Crea un ticket.")
]

for title_part, prefix, desc in sections_config:
    tl = f"<:qo_{prefix}_tl:{synced_ids[f'qo_{prefix}_tl']}>"
    tr = f"<:qo_{prefix}_tr:{synced_ids[f'qo_{prefix}_tr']}>"
    bl = f"<:qo_{prefix}_bl:{synced_ids[f'qo_{prefix}_bl']}>"
    br = f"<:qo_{prefix}_br:{synced_ids[f'qo_{prefix}_br']}>"

    # Buscar la sección correspondiente
    for comp in c2_components:
        if comp.get("type") == 9:
            inner_txt = comp.get("components", [{}])[0].get("content", "")
            if title_part in inner_txt:
                comp["components"][0]["content"] = f"{tl}{tr} **{title_part}**\n{bl}{br} {desc}"
                print(f"Actualizada sección en memoria: {title_part}")
                break

# Enviar patch al mensaje principal
patch_main = requests.patch(
    f"https://discord.com/api/v10/channels/{channel_main_id}/messages/{main_msg_id}",
    headers=headers,
    data=json.dumps(main_data, ensure_ascii=False).encode("utf-8")
)
print("Patch Main Message status:", patch_main.status_code)

# 3. Actualizar Hilo "empezar-a-jugar" con el nuevo icono de Mando Gamepad (<:th_jugar_w:...>)
r_jugar = requests.get(f"https://discord.com/api/v10/channels/{thread_jugar_id}/messages/{jugar_msg_id}", headers=headers)
jugar_msg = r_jugar.json()

c_jugar = jugar_msg["components"][0]["components"][0]["components"][0]["content"]
lines_j = c_jugar.split("\n")
new_jugar_w_id = synced_ids["th_jugar_w"]
lines_j[0] = f"### <:th_jugar_w:{new_jugar_w_id}> Entra a ThunderMC"
jugar_msg["components"][0]["components"][0]["components"][0]["content"] = "\n".join(lines_j)

patch_jugar = requests.patch(
    f"https://discord.com/api/v10/channels/{thread_jugar_id}/messages/{jugar_msg_id}",
    headers=headers,
    data=json.dumps(jugar_msg, ensure_ascii=False).encode("utf-8")
)
print("Patch Jugar Thread status:", patch_jugar.status_code)
print("All Discord components and icons synchronized successfully!")
