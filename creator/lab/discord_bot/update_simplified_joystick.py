import os
import json
import base64
import time
import requests
from PIL import Image, ImageDraw

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(icons_dir, exist_ok=True)

SIZE = 512
FINAL_SINGLE = 128
FINAL_QUAD_MASTER = 256

YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

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

def clean_rgba(img, target_size, solid_color, transparent_color):
    resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    alpha = resized.split()[3]
    clean = Image.new("RGBA", (target_size, target_size), transparent_color)
    solid = Image.new("RGBA", (target_size, target_size), solid_color)
    clean.paste(solid, mask=alpha)
    return clean

def add_corner_anchors(tile, rgb=(255, 200, 0)):
    px = tile.load()
    w, h = tile.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if px[x, y][3] == 0:
            px[x, y] = (rgb[0], rgb[1], rgb[2], 1)
    return tile

def save_quad_icon(img, prefix, color=YELLOW, trans=TRANSPARENT_YELLOW):
    master = clean_rgba(img, FINAL_QUAD_MASTER, color, trans)
    preview = Image.new("RGBA", (FINAL_QUAD_MASTER, FINAL_QUAD_MASTER), (43, 45, 49, 255))
    preview.alpha_composite(master)
    preview.save(os.path.join(icons_dir, f"preview_quad_{prefix}.png"), "PNG")

    quads = {
        "tl": master.crop((0,   0,   128, 128)),
        "tr": master.crop((128, 0,   256, 128)),
        "bl": master.crop((0,   128, 128, 256)),
        "br": master.crop((128, 128, 256, 256)),
    }
    paths = {}
    for qname, tile in quads.items():
        tile = add_corner_anchors(tile, color[:3])
        p = os.path.join(icons_dir, f"quad_{prefix}_{qname}.png")
        tile.save(p, "PNG")
        paths[qname] = p
    print(f"Saved 2x2 quad: quad_{prefix}_[tl,tr,bl,br].png in {color[:3]}")
    return paths

def save_single_icon(img, name, color=WHITE, trans=TRANSPARENT_WHITE):
    clean = clean_rgba(img, FINAL_SINGLE, color, trans)
    clean = add_corner_anchors(clean, color[:3])
    path = os.path.join(icons_dir, name)
    clean.save(path, "PNG")
    print(f"Saved single: {name}")
    return path

def draw_simple_joystick(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((116, 360, 396, 444), radius=38, fill=color)
    collar_pts = [(188, 360), (324, 360), (292, 290), (220, 290)]
    draw.polygon(collar_pts, fill=color)
    draw.rounded_rectangle((232, 160, 280, 300), radius=18, fill=color)
    bx, by, br = 256, 134, 76
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)
    draw.ellipse((326, 384, 362, 420), fill=trans)
    draw.rounded_rectangle((150, 394, 210, 410), radius=8, fill=trans)
    return img

img_joy_y = draw_simple_joystick(YELLOW, TRANSPARENT_YELLOW)
paths_joy = save_quad_icon(img_joy_y, "jugar", YELLOW, TRANSPARENT_YELLOW)

img_joy_w = draw_simple_joystick(WHITE, TRANSPARENT_WHITE)
path_joy_w = save_single_icon(img_joy_w, "icon_jugar_w.png", WHITE, TRANSPARENT_WHITE)

# 2. Sincronizar con Discord Application
existing = {e["name"]: e["id"] for e in requests.get(f"https://discord.com/api/v10/applications/{app_id}/emojis", headers=headers).json().get("items", [])}

emojis_to_sync = {
    "qo_jugar_tl": paths_joy["tl"],
    "qo_jugar_tr": paths_joy["tr"],
    "qo_jugar_bl": paths_joy["bl"],
    "qo_jugar_br": paths_joy["br"],
    "th_jugar_w": path_joy_w
}

synced_ids = {}
for ename, fpath in emojis_to_sync.items():
    with open(fpath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    if ename in existing:
        requests.delete(f"https://discord.com/api/v10/applications/{app_id}/emojis/{existing[ename]}", headers=headers)
        time.sleep(0.15)

    res = requests.post(
        f"https://discord.com/api/v10/applications/{app_id}/emojis",
        headers=headers,
        json={"name": ename, "image": f"data:image/png;base64,{b64}"}
    )
    if res.status_code in (200, 201):
        synced_ids[ename] = res.json()["id"]
        print(f"Emoji {ename} subido con nuevo ID: {synced_ids[ename]}")
    else:
        print(f"Error subiendo {ename}: {res.status_code} {res.text}")
    time.sleep(0.2)

# 3. Actualizar Mensaje Principal en #embeds
r_main = requests.get(f"https://discord.com/api/v10/channels/{channel_main_id}/messages/{main_msg_id}", headers=headers)
main_data = r_main.json()
c2_components = main_data["components"][1]["components"]

tl = f"<:qo_jugar_tl:{synced_ids['qo_jugar_tl']}>"
tr = f"<:qo_jugar_tr:{synced_ids['qo_jugar_tr']}>"
bl = f"<:qo_jugar_bl:{synced_ids['qo_jugar_bl']}>"
br = f"<:qo_jugar_br:{synced_ids['qo_jugar_br']}>"

for comp in c2_components:
    if comp.get("type") == 9:
        inner_txt = comp.get("components", [{}])[0].get("content", "")
        if "¿Cómo jugar?" in inner_txt:
            comp["components"][0]["content"] = f"{tl}{tr} **¿Cómo jugar?**\n{bl}{br} Entra a jugar rápidamente."
            print("Sección ¿Cómo jugar? actualizada en mensaje principal.")
            break

patch_main = requests.patch(
    f"https://discord.com/api/v10/channels/{channel_main_id}/messages/{main_msg_id}",
    headers=headers,
    data=json.dumps(main_data, ensure_ascii=False).encode("utf-8")
)
print("Patch Main Message status:", patch_main.status_code)

# 4. Actualizar Hilo "empezar-a-jugar"
r_jugar = requests.get(f"https://discord.com/api/v10/channels/{thread_jugar_id}/messages/{jugar_msg_id}", headers=headers)
jugar_msg = r_jugar.json()

c_jugar = jugar_msg["components"][0]["components"][0]["components"][0]["content"]
lines_j = c_jugar.split("\n")
lines_j[0] = f"### <:th_jugar_w:{synced_ids['th_jugar_w']}> Entra a ThunderMC"
jugar_msg["components"][0]["components"][0]["components"][0]["content"] = "\n".join(lines_j)

patch_jugar = requests.patch(
    f"https://discord.com/api/v10/channels/{thread_jugar_id}/messages/{jugar_msg_id}",
    headers=headers,
    data=json.dumps(jugar_msg, ensure_ascii=False).encode("utf-8")
)
print("Patch Jugar Thread status:", patch_jugar.status_code)
print("Simplified joystick updated everywhere successfully!")
