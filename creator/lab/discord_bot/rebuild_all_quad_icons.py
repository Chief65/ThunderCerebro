import os
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(icons_dir, exist_ok=True)

SIZE = 512
FINAL_SINGLE = 128
FINAL_QUAD_MASTER = 256

# Amarillo Oficial ThunderMC puro (#FEEB00 / 254, 235, 0)
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
        p = os.path.join(icons_dir, f"quad_{prefix}_{qname}.png")
        tile.save(p, "PNG")
        paths[qname] = p
    print(f"Saved 2x2 quad: quad_{prefix}_[tl,tr,bl,br].png")
    return paths

def save_single_icon(img, name, color=WHITE, trans=TRANSPARENT_WHITE):
    clean = clean_rgba(img, FINAL_SINGLE, color, trans)
    clean = add_corner_anchors(clean, color[:3])
    path = os.path.join(icons_dir, name)
    clean.save(path, "PNG")
    print(f"Saved single: {name}")
    return path

# 1. JUGAR: Control Gamer ergonómico moderno (Gamepad)
def make_gamepad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((74, 110, 438, 330), radius=90, fill=YELLOW)
    draw.polygon([(74, 210), (150, 210), (180, 440), (84, 430)], fill=YELLOW)
    draw.ellipse((68, 380, 156, 456), fill=YELLOW)
    draw.polygon([(438, 210), (362, 210), (332, 440), (428, 430)], fill=YELLOW)
    draw.ellipse((356, 380, 444, 456), fill=YELLOW)
    draw.ellipse((170, 250, 342, 450), fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((104, 76, 212, 118), radius=18, fill=YELLOW)
    draw.rounded_rectangle((300, 76, 408, 118), radius=18, fill=YELLOW)
    draw.line([(100, 114), (216, 114)], fill=TRANSPARENT_YELLOW, width=8)
    draw.line([(296, 114), (412, 114)], fill=TRANSPARENT_YELLOW, width=8)
    # D-pad
    cx, cy, arm, w = 158, 216, 36, 24
    draw.rounded_rectangle((cx - w//2, cy - arm, cx + w//2, cy + arm), radius=6, fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((cx - arm, cy - w//2, cx + arm, cy + w//2), radius=6, fill=TRANSPARENT_YELLOW)
    # Botones A B X Y
    bx, by, b_r, spread = 354, 216, 11, 28
    draw.ellipse((bx - b_r, by - spread - b_r, bx + b_r, by - spread + b_r), fill=TRANSPARENT_YELLOW)
    draw.ellipse((bx - b_r, by + spread - b_r, bx + b_r, by + spread + b_r), fill=TRANSPARENT_YELLOW)
    draw.ellipse((bx - spread - b_r, by - b_r, bx - spread + b_r, by + b_r), fill=TRANSPARENT_YELLOW)
    draw.ellipse((bx + spread - b_r, by - b_r, bx + spread + b_r, by + b_r), fill=TRANSPARENT_YELLOW)
    # Select, Start & Home
    draw.ellipse((220 - 7, 206 - 7, 220 + 7, 206 + 7), fill=TRANSPARENT_YELLOW)
    draw.ellipse((292 - 7, 206 - 7, 292 + 7, 206 + 7), fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((226, 136, 286, 164), radius=8, fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "jugar", YELLOW, TRANSPARENT_YELLOW)

# 2. VOZ: Micrófono minimalista
def make_mic():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((176, 52, 336, 296), radius=80, fill=YELLOW)
    stroke = 42
    bbox = (104, 132, 408, 384)
    draw.arc(bbox, start=0, end=180, fill=YELLOW, width=stroke)
    r = stroke // 2
    draw.ellipse((104, 258 - r, 104 + stroke, 258 + r), fill=YELLOW)
    draw.ellipse((408 - stroke, 258 - r, 408, 258 + r), fill=YELLOW)
    draw.line([(256, 376), (256, 456)], fill=YELLOW, width=stroke)
    draw.rounded_rectangle((160, 434, 352, 472), radius=19, fill=YELLOW)
    return save_quad_icon(img, "voz", YELLOW, TRANSPARENT_YELLOW)

# 3. REGLAS: Documento normativo
def make_rules():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((96, 52, 416, 464), radius=52, fill=YELLOW)
    for x1, y1, x2, y2 in [(156, 146, 356, 186), (156, 238, 356, 278), (156, 330, 290, 370)]:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=20, fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "reglas", YELLOW, TRANSPARENT_YELLOW)

# 4. POSTULACIONES: Birrete académico
def make_post():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.polygon([(256, 52), (436, 148), (256, 244), (76, 148)], fill=YELLOW)
    draw.line([(256, 52), (436, 148)], fill=YELLOW, width=28)
    draw.line([(436, 148), (256, 244)], fill=YELLOW, width=28)
    draw.line([(256, 244), (76, 148)], fill=YELLOW, width=28)
    draw.line([(76, 148), (256, 52)], fill=YELLOW, width=28)
    draw.polygon([(144, 206), (368, 206), (338, 334), (174, 334)], fill=YELLOW)
    draw_thick_line(draw, (384, 178), (384, 396), 24, YELLOW)
    draw.ellipse((384 - 24, 396 - 16, 384 + 24, 396 + 32), fill=YELLOW)
    return save_quad_icon(img, "post", YELLOW, TRANSPARENT_YELLOW)

# 5. TIENDA: Carrito proporcionado armonioso
def make_tienda():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw_thick_line(draw, (84, 100), (140, 100), 34, YELLOW)
    draw_thick_line(draw, (140, 100), (190, 330), 34, YELLOW)
    draw_thick_line(draw, (190, 330), (394, 330), 32, YELLOW)
    basket_pts = [(154, 150), (432, 150), (396, 286), (180, 286)]
    draw.polygon(basket_pts, fill=YELLOW)
    for i in range(len(basket_pts)):
        draw_thick_line(draw, basket_pts[i], basket_pts[(i+1) % len(basket_pts)], 28, YELLOW)
    for rx in (236, 294, 350):
        draw_thick_line(draw, (rx, 178), (rx - 4, 258), 18, TRANSPARENT_YELLOW)
    for wx in (226, 368):
        wy, wr = 398, 38
        draw.ellipse((wx - wr, wy - wr, wx + wr, wy + wr), fill=YELLOW)
        draw.ellipse((wx - 14, wy - 14, wx + 14, wy + 14), fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "tienda", YELLOW, TRANSPARENT_YELLOW)

# 6. SOPORTE: Salvavidas / aro
def make_soporte():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.ellipse((68, 68, 444, 444), fill=YELLOW)
    draw.ellipse((172, 172, 340, 340), fill=TRANSPARENT_YELLOW)
    for p1, p2 in [((256, 68), (256, 172)), ((256, 340), (256, 444)), ((68, 256), (172, 256)), ((340, 256), (444, 256))]:
        draw.line([p1, p2], fill=TRANSPARENT_YELLOW, width=28)
    return save_quad_icon(img, "soporte", YELLOW, TRANSPARENT_YELLOW)

# Icono blanco 1x1 para el hilo "Entra a ThunderMC" (reemplazando el joystick)
def make_gamepad_single_w():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((74, 110, 438, 330), radius=90, fill=WHITE)
    draw.polygon([(74, 210), (150, 210), (180, 440), (84, 430)], fill=WHITE)
    draw.ellipse((68, 380, 156, 456), fill=WHITE)
    draw.polygon([(438, 210), (362, 210), (332, 440), (428, 430)], fill=WHITE)
    draw.ellipse((356, 380, 444, 456), fill=WHITE)
    draw.ellipse((170, 250, 342, 450), fill=TRANSPARENT_WHITE)
    draw.rounded_rectangle((104, 76, 212, 118), radius=18, fill=WHITE)
    draw.rounded_rectangle((300, 76, 408, 118), radius=18, fill=WHITE)
    draw.line([(100, 114), (216, 114)], fill=TRANSPARENT_WHITE, width=8)
    draw.line([(296, 114), (412, 114)], fill=TRANSPARENT_WHITE, width=8)
    cx, cy, arm, w = 158, 216, 36, 24
    draw.rounded_rectangle((cx - w//2, cy - arm, cx + w//2, cy + arm), radius=6, fill=TRANSPARENT_WHITE)
    draw.rounded_rectangle((cx - arm, cy - w//2, cx + arm, cy + w//2), radius=6, fill=TRANSPARENT_WHITE)
    bx, by, b_r, spread = 354, 216, 11, 28
    draw.ellipse((bx - b_r, by - spread - b_r, bx + b_r, by - spread + b_r), fill=TRANSPARENT_WHITE)
    draw.ellipse((bx - b_r, by + spread - b_r, bx + b_r, by + spread + b_r), fill=TRANSPARENT_WHITE)
    draw.ellipse((bx - spread - b_r, by - b_r, bx - spread + b_r, by + b_r), fill=TRANSPARENT_WHITE)
    draw.ellipse((bx + spread - b_r, by - b_r, bx + spread + b_r, by + b_r), fill=TRANSPARENT_WHITE)
    draw.ellipse((220 - 7, 206 - 7, 220 + 7, 206 + 7), fill=TRANSPARENT_WHITE)
    draw.ellipse((292 - 7, 206 - 7, 292 + 7, 206 + 7), fill=TRANSPARENT_WHITE)
    draw.rounded_rectangle((226, 136, 286, 164), radius=8, fill=TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_jugar_w.png", WHITE, TRANSPARENT_WHITE)

make_gamepad()
make_mic()
make_rules()
make_post()
make_tienda()
make_soporte()
make_gamepad_single_w()
print("All 6 quads and single white icons re-rendered in unified #FEEB00 successfully!")
