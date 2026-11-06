import os
import json
import base64
import requests
from PIL import Image, ImageDraw

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
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

thread_voz_id = "1568202146611204137"
voz_msg_id = "1568208937487044700"

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(icons_dir, exist_ok=True)

headers = {
    "Authorization": f"Bot {token}",
    "User-Agent": "DiscordBot (https://thundermc.es, 1.0.0)",
    "Content-Type": "application/json; charset=utf-8"
}

# --- 1. GENERACIÓN DE ICONOS ---
SIZE = 512
FINAL_SINGLE = 128
FINAL_QUAD_MASTER = 256
YELLOW = (254, 235, 0, 255)
TRANSPARENT_YELLOW = (254, 235, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

def draw_thick_line(draw, p1, p2, width, color):
    draw.line([p1, p2], fill=color, width=width)
    r = width // 2
    for x, y in (p1, p2):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

def clean_rgba(img, target_size, solid_color, transparent_color):
    resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    alpha = resized.split()[3]
    clean = Image.new("RGBA", (target_size, target_size), transparent_color)
    solid = Image.new("RGBA", (target_size, target_size), solid_color)
    clean.paste(solid, mask=alpha)
    return clean

def add_corner_anchors(tile, rgb=(254, 235, 0)):
    px = tile.load()
    w, h = tile.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if px[x, y][3] == 0:
            px[x, y] = (rgb[0], rgb[1], rgb[2], 1)
    return tile

def save_single_icon(img, name, color=WHITE, trans=TRANSPARENT_WHITE):
    clean = clean_rgba(img, FINAL_SINGLE, color, trans)
    clean = add_corner_anchors(clean, color[:3])
    path = os.path.join(icons_dir, name)
    clean.save(path, "PNG")
    print(f"Saved single icon: {path}")
    return path

def save_quad_icon(img, prefix, color=YELLOW, trans=TRANSPARENT_YELLOW):
    master = clean_rgba(img, FINAL_QUAD_MASTER, color, trans)
    preview = Image.new("RGBA", (FINAL_QUAD_MASTER, FINAL_QUAD_MASTER), (43, 45, 49, 255))
    preview.alpha_composite(master)
    preview.save(os.path.join(icons_dir, f"preview_{prefix}.png"), "PNG")

    quads = {
        "tl": master.crop((0,   0,   128, 128)),
        "tr": master.crop((128, 0,   256, 128)),
        "bl": master.crop((0,   128, 128, 256)),
        "br": master.crop((128, 128, 256, 256)),
    }
    paths = {}
    for qname, tile in quads.items():
        tile = add_corner_anchors(tile, color[:3])
        p = os.path.join(icons_dir, f"{prefix}_{qname}.png")
        tile.save(p, "PNG")
        paths[qname] = p
    print(f"Saved 2x2 quad icon set: {prefix}_[tl,tr,bl,br].png")
    return paths

# 1.1 Joystick Arcade (Blanco 1x1 para el título del hilo)
def make_arcade_joystick_white():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    # Palanca / eje central
    draw.rounded_rectangle((234, 170, 278, 336), radius=20, fill=WHITE)
    # Bola superior
    bx, by, br = 256, 126, 78
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=WHITE)
    draw.arc((bx - 52, by - 52, bx + 28, by + 28), start=195, end=265, fill=TRANSPARENT_WHITE, width=16)
    # Fuelle de goma
    draw.rounded_rectangle((176, 304, 336, 348), radius=22, fill=WHITE)
    draw.rectangle((160, 346, 352, 358), fill=TRANSPARENT_WHITE)
    # Base arcade
    draw.rounded_rectangle((76, 358, 436, 462), radius=42, fill=WHITE)
    # Botones arcade
    draw.rounded_rectangle((112, 336, 168, 366), radius=12, fill=WHITE)
    draw.rounded_rectangle((344, 336, 400, 366), radius=12, fill=WHITE)
    # Recortes
    draw.ellipse((132, 392, 168, 428), fill=TRANSPARENT_WHITE)
    draw.ellipse((344, 392, 380, 428), fill=TRANSPARENT_WHITE)
    draw.rounded_rectangle((204, 402, 308, 420), radius=9, fill=TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_joystick_w.png", WHITE, TRANSPARENT_WHITE)

# 1.2 Carrito de Compra (Amarillo 2x2 para el panel principal)
def make_store_cart_yellow():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    # Mango + brazo
    draw_thick_line(draw, (42, 82), (108, 82), 40, YELLOW)
    draw_thick_line(draw, (108, 82), (168, 344), 40, YELLOW)
    draw_thick_line(draw, (168, 344), (404, 344), 38, YELLOW)
    # Cesta del carrito
    basket_pts = [(126, 140), (460, 140), (414, 290), (156, 290)]
    draw.polygon(basket_pts, fill=YELLOW)
    for i in range(len(basket_pts)):
        draw_thick_line(draw, basket_pts[i], basket_pts[(i+1) % len(basket_pts)], 32, YELLOW)
    # Ranuras
    draw_thick_line(draw, (238, 178), (246, 254), 26, TRANSPARENT_YELLOW)
    draw_thick_line(draw, (334, 178), (326, 254), 26, TRANSPARENT_YELLOW)
    # Ruedas
    for wx in (196, 380):
        wy, wr = 424, 42
        draw.ellipse((wx - wr, wy - wr, wx + wr, wy + wr), fill=YELLOW)
    return save_quad_icon(img, "quad_tienda", YELLOW, TRANSPARENT_YELLOW)

p_joy = make_arcade_joystick_white()
p_cart = make_store_cart_yellow()

# --- 2. SUBIR EMOJIS A DISCORD APPLICATION ---
existing = {e["name"]: e["id"] for e in requests.get(f"https://discord.com/api/v10/applications/{app_id}/emojis", headers=headers).json().get("items", [])}

emojis_to_upload = {
    "th_joystick_w": p_joy,
    "qo_tienda_tl": p_cart["tl"],
    "qo_tienda_tr": p_cart["tr"],
    "qo_tienda_bl": p_cart["bl"],
    "qo_tienda_br": p_cart["br"]
}

synced_ids = {}
for name, path in emojis_to_upload.items():
    if name in existing:
        synced_ids[name] = existing[name]
        print(f"Emoji {name} ya existe: {existing[name]}")
    else:
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        r = requests.post(
            f"https://discord.com/api/v10/applications/{app_id}/emojis",
            headers=headers,
            json={"name": name, "image": f"data:image/png;base64,{b64}"}
        )
        if r.status_code in [200, 201]:
            emoji_id = r.json()["id"]
            synced_ids[name] = emoji_id
            print(f"Emoji {name} creado exitosamente: {emoji_id}")
        else:
            print(f"Error subiendo {name}: {r.text}")

# --- 3. ACTUALIZAR HILO 🕹️・empezar-a-jugar ---
joy_id = synced_ids.get("th_joystick_w", existing.get("th_joystick_w"))
jugar_json_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\entrar_a_jugar_v2.json"
with open(jugar_json_file, "r", encoding="utf-8") as f:
    jugar_data = json.load(f)

c_jugar = jugar_data["components"][0]["components"][0]["components"][0]["content"]
lines_j = c_jugar.split("\n")
lines_j[0] = f"### <:th_joystick_w:{joy_id}> Entra a ThunderMC"
jugar_data["components"][0]["components"][0]["components"][0]["content"] = "\n".join(lines_j)

with open(jugar_json_file, "w", encoding="utf-8") as f:
    json.dump(jugar_data, f, ensure_ascii=False, indent=2)
with open(r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\entrar a jugar v2.json", "w", encoding="utf-8") as f:
    json.dump(jugar_data, f, ensure_ascii=False, indent=2)

r_patch_j = requests.patch(
    f"https://discord.com/api/v10/channels/{thread_jugar_id}/messages/{jugar_msg_id}",
    headers=headers,
    data=json.dumps(jugar_data, ensure_ascii=False).encode("utf-8")
)
print("Patch Jugar status:", r_patch_j.status_code)

# --- 4. ACTUALIZAR HILO 🎙️・chat-de-voz ---
voz_emoji_id = "1568162713224355840" # th_voz
voz_json_file = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\voicechat_setup_v2.json"
with open(voz_json_file, "r", encoding="utf-8") as f:
    voz_data = json.load(f)

c_voz = voz_data["components"][0]["components"][0]["components"][0]["content"]
lines_v = c_voz.split("\n")
# Cambiar el emoji del microfono clásico por <:th_voz:1568162713224355840>
lines_v[0] = f"### <:th_voz:{voz_emoji_id}> Chat de Voz por Proximidad"
voz_data["components"][0]["components"][0]["components"][0]["content"] = "\n".join(lines_v)

with open(voz_json_file, "w", encoding="utf-8") as f:
    json.dump(voz_data, f, ensure_ascii=False, indent=2)
with open(r"C:\Users\PC\OneDrive\Escritorio\descargas\reglas\chat de voz v2.json", "w", encoding="utf-8") as f:
    json.dump(voz_data, f, ensure_ascii=False, indent=2)

r_patch_v = requests.patch(
    f"https://discord.com/api/v10/channels/{thread_voz_id}/messages/{voz_msg_id}",
    headers=headers,
    data=json.dumps(voz_data, ensure_ascii=False).encode("utf-8")
)
print("Patch Voz status:", r_patch_v.status_code)

# --- 5. ACTUALIZAR PANEL PRINCIPAL EN #embeds ---
# Obtener mensaje actual de #embeds
r_main = requests.get(f"https://discord.com/api/v10/channels/{channel_main_id}/messages/{main_msg_id}", headers=headers)
main_data = r_main.json()

# Components de Container 2 (Information)
# Buscar el índice de Soporte Flash para insertar Tienda Oficial justo antes (penúltima posición)
c2_components = main_data["components"][1]["components"]

# Comprobar si ya existe una seccion de Tienda Oficial para no duplicarla
has_tienda = any("Tienda Oficial" in c.get("components", [{}])[0].get("content", "") for c in c2_components if c.get("type") == 9)

if not has_tienda:
    soporte_idx = -1
    for idx, comp in enumerate(c2_components):
        if comp.get("type") == 9 and "Soporte Flash" in comp.get("components", [{}])[0].get("content", ""):
            soporte_idx = idx
            break
    
    t_tl = f"<:qo_tienda_tl:{synced_ids['qo_tienda_tl']}>"
    t_tr = f"<:qo_tienda_tr:{synced_ids['qo_tienda_tr']}>"
    t_bl = f"<:qo_tienda_bl:{synced_ids['qo_tienda_bl']}>"
    t_br = f"<:qo_tienda_br:{synced_ids['qo_tienda_br']}>"

    tienda_section = {
        "type": 9,
        "components": [
            {
                "type": 10,
                "content": f"{t_tl}{t_tr} **Tienda Oficial**\n{t_bl}{t_br} Visita nuestra tienda web."
            }
        ],
        "accessory": {
            "type": 2,
            "style": 5,
            "emoji": {
                "id": "1568181296654590023",
                "name": "th_ir_w"
            },
            "url": "https://tienda.thundermc.es/"
        }
    }

    if soporte_idx != -1:
        c2_components.insert(soporte_idx, tienda_section)
        print(f"Insertada Tienda Oficial en la posición {soporte_idx} (penúltima)")
    else:
        c2_components.append(tienda_section)
        print("Insertada Tienda Oficial al final")

# Parchear el mensaje principal
# Limpiar campos de sistema antes de reenviar el payload
clean_main_payload = {
    "flags": main_data.get("flags", 32768),
    "allowed_mentions": {"parse": []},
    "components": main_data["components"]
}

r_patch_main = requests.patch(
    f"https://discord.com/api/v10/channels/{channel_main_id}/messages/{main_msg_id}",
    headers=headers,
    data=json.dumps(clean_main_payload, ensure_ascii=False).encode("utf-8")
)
print("Patch Main Panel status:", r_patch_main.status_code)
if r_patch_main.status_code != 200:
    print("Error main panel patch:", r_patch_main.text)
else:
    print("Main panel actualizado exitosamente con Tienda Oficial en posición penúltima.")

# Guardar payload del panel principal actualizado en creator/output/discord/portal_thundermc_v2.json
with open(r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\discord\portal_thundermc_v2.json", "w", encoding="utf-8") as f:
    json.dump(clean_main_payload, f, ensure_ascii=False, indent=2)
