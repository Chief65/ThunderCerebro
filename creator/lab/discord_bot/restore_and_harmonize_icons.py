import os
import json
import base64
import time
import requests
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(icons_dir, exist_ok=True)

SIZE = 512
FINAL_SINGLE = 128
FINAL_QUAD_MASTER = 256

# COLOR OFICIAL ANARANJADO (#FFC800 / RGB: 255, 200, 0)
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)
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
    print(f"Saved 2x2 quad icon set: quad_{prefix}_[tl,tr,bl,br].png in {color[:3]}")
    return paths

def save_single_icon(img, name, color=WHITE, trans=TRANSPARENT_WHITE):
    clean = clean_rgba(img, FINAL_SINGLE, color, trans)
    clean = add_corner_anchors(clean, color[:3])
    path = os.path.join(icons_dir, name)
    clean.save(path, "PNG")
    print(f"Saved single icon: {path}")
    return path

# 1. JUGAR: Bloque / Cubo Isométrico de Minecraft (Grass Block oficial)
def make_minecraft_cube_quad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    top_face = [(256, 76), (426, 174), (256, 272), (86, 174)]
    draw.polygon(top_face, fill=YELLOW)
    left_face = [(86, 174), (256, 272), (256, 436), (86, 338)]
    draw.polygon(left_face, fill=YELLOW)
    right_face = [(256, 272), (426, 174), (426, 338), (256, 436)]
    draw.polygon(right_face, fill=YELLOW)

    draw.line([(256, 76), (256, 272)], fill=TRANSPARENT_YELLOW, width=14)
    draw.line([(86, 174), (256, 272)], fill=TRANSPARENT_YELLOW, width=14)
    draw.line([(426, 174), (256, 272)], fill=TRANSPARENT_YELLOW, width=14)
    draw.line([(256, 272), (256, 436)], fill=TRANSPARENT_YELLOW, width=14)

    draw.polygon([(114, 258), (146, 276), (146, 306), (114, 288)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(168, 288), (200, 306), (200, 336), (168, 318)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(220, 318), (248, 334), (248, 364), (220, 348)], fill=TRANSPARENT_YELLOW)

    draw.polygon([(264, 334), (292, 318), (292, 348), (264, 364)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(312, 306), (344, 288), (344, 318), (312, 336)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(366, 276), (398, 258), (398, 288), (366, 306)], fill=TRANSPARENT_YELLOW)

    draw.polygon([(136, 330), (164, 346), (164, 370), (136, 354)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(348, 346), (376, 330), (376, 354), (348, 370)], fill=TRANSPARENT_YELLOW)

    draw.polygon([(236, 142), (256, 130), (276, 142), (256, 154)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(176, 196), (196, 184), (216, 196), (196, 208)], fill=TRANSPARENT_YELLOW)
    draw.polygon([(296, 216), (316, 204), (336, 216), (316, 228)], fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "jugar", YELLOW, TRANSPARENT_YELLOW)

def make_minecraft_cube_white():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    top_face = [(256, 76), (426, 174), (256, 272), (86, 174)]
    draw.polygon(top_face, fill=WHITE)
    left_face = [(86, 174), (256, 272), (256, 436), (86, 338)]
    draw.polygon(left_face, fill=WHITE)
    right_face = [(256, 272), (426, 174), (426, 338), (256, 436)]
    draw.polygon(right_face, fill=WHITE)

    draw.line([(256, 76), (256, 272)], fill=TRANSPARENT_WHITE, width=14)
    draw.line([(86, 174), (256, 272)], fill=TRANSPARENT_WHITE, width=14)
    draw.line([(426, 174), (256, 272)], fill=TRANSPARENT_WHITE, width=14)
    draw.line([(256, 272), (256, 436)], fill=TRANSPARENT_WHITE, width=14)

    draw.polygon([(114, 258), (146, 276), (146, 306), (114, 288)], fill=TRANSPARENT_WHITE)
    draw.polygon([(168, 288), (200, 306), (200, 336), (168, 318)], fill=TRANSPARENT_WHITE)
    draw.polygon([(220, 318), (248, 334), (248, 364), (220, 348)], fill=TRANSPARENT_WHITE)

    draw.polygon([(264, 334), (292, 318), (292, 348), (264, 364)], fill=TRANSPARENT_WHITE)
    draw.polygon([(312, 306), (344, 288), (344, 318), (312, 336)], fill=TRANSPARENT_WHITE)
    draw.polygon([(366, 276), (398, 258), (398, 288), (366, 306)], fill=TRANSPARENT_WHITE)

    draw.polygon([(136, 330), (164, 346), (164, 370), (136, 354)], fill=TRANSPARENT_WHITE)
    draw.polygon([(348, 346), (376, 330), (376, 354), (348, 370)], fill=TRANSPARENT_WHITE)

    draw.polygon([(236, 142), (256, 130), (276, 142), (256, 154)], fill=TRANSPARENT_WHITE)
    draw.polygon([(176, 196), (196, 184), (216, 196), (196, 208)], fill=TRANSPARENT_WHITE)
    draw.polygon([(296, 216), (316, 204), (336, 216), (316, 228)], fill=TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_jugar_w.png", WHITE, TRANSPARENT_WHITE)

# 2. VOZ: Micrófono minimalista original
def make_mic_quad():
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

# 3. REGLAS: Documento normativo original
def make_rules_quad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((96, 52, 416, 464), radius=52, fill=YELLOW)
    for x1, y1, x2, y2 in [(156, 146, 356, 186), (156, 238, 356, 278), (156, 330, 290, 370)]:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=20, fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "reglas", YELLOW, TRANSPARENT_YELLOW)

# 4. POSTULACIONES: Trabajador con casco y chaqueta original
def make_apply_quad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.pieslice((152, 54, 360, 246), start=180, end=360, fill=YELLOW)
    draw.rounded_rectangle((234, 42, 278, 130), radius=18, fill=YELLOW)
    draw.rounded_rectangle((132, 134, 380, 166), radius=16, fill=YELLOW)
    draw.rectangle((128, 166, 384, 178), fill=TRANSPARENT_YELLOW)
    draw.pieslice((172, 110, 340, 276), start=0, end=180, fill=YELLOW)
    draw.rectangle((172, 178, 340, 200), fill=YELLOW)
    draw.pieslice((76, 286, 436, 610), start=180, end=360, fill=YELLOW)
    draw.rounded_rectangle((76, 396, 436, 464), radius=32, fill=YELLOW)
    v_neck = [(202, 282), (310, 282), (256, 382)]
    draw.polygon(v_neck, fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((246, 368, 266, 468), radius=8, fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((296, 382, 366, 412), radius=10, fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((146, 382, 216, 412), radius=10, fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "post", YELLOW, TRANSPARENT_YELLOW)

# 5. SOPORTE: Headset con micrófono original
def make_support_quad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.pieslice((92, 56, 420, 384), start=180, end=360, fill=YELLOW)
    draw.pieslice((140, 104, 372, 336), start=180, end=360, fill=TRANSPARENT_YELLOW)
    draw.rectangle((92, 220, 140, 310), fill=YELLOW)
    draw.rectangle((372, 220, 420, 310), fill=YELLOW)
    draw.rounded_rectangle((68, 224, 156, 372), radius=42, fill=YELLOW)
    draw.rounded_rectangle((356, 224, 444, 372), radius=42, fill=YELLOW)
    draw.arc((104, 276, 348, 454), start=90, end=180, fill=YELLOW, width=34)
    draw.rounded_rectangle((216, 418, 304, 462), radius=22, fill=YELLOW)
    return save_quad_icon(img, "soporte", YELLOW, TRANSPARENT_YELLOW)

# 6. TIENDA OFICIAL: Carrito proporcionado en el MISMO color anaranjado (#FFC800)
def make_tienda_quad():
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

make_minecraft_cube_quad()
make_minecraft_cube_white()
make_mic_quad()
make_rules_quad()
make_apply_quad()
make_support_quad()
make_tienda_quad()
print("All 6 original designs generated in identical #FFC800 successfully!")
