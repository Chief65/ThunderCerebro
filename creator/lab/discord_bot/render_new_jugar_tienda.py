import os
from PIL import Image, ImageDraw

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(icons_dir, exist_ok=True)

SIZE = 512
FINAL_SINGLE = 128
FINAL_QUAD_MASTER = 256

YELLOW = (254, 235, 0, 255)  # #FEEB00 Amarillo oficial ThunderMC
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

# ==============================================================================
# 1. CONTROL GAMER / GAMEPAD MODERNO (Reemplazo del Joystick Arcade)
# Dimensiones master: ~180px ancho x ~190px alto en 256x256 (proporción perfecta)
# ==============================================================================
def draw_gamepad(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Cuerpo principal ergonómico del mando
    # Parte superior rectangular con bordes muy redondeados
    draw.rounded_rectangle((74, 110, 438, 330), radius=90, fill=color)

    # Agarres inferiores izquierdo y derecho (grips inclinados)
    # Grip izquierdo
    draw.polygon([(74, 210), (150, 210), (180, 440), (84, 430)], fill=color)
    draw.ellipse((68, 380, 156, 456), fill=color)
    # Grip derecho
    draw.polygon([(438, 210), (362, 210), (332, 440), (428, 430)], fill=color)
    draw.ellipse((356, 380, 444, 456), fill=color)

    # Suavizar el centro inferior (recorte en arco entre los dos agarres)
    draw.ellipse((170, 250, 342, 450), fill=trans)

    # Gatillos superiores L1/R1 (bumpers redondeados sutiles)
    draw.rounded_rectangle((104, 76, 212, 118), radius=18, fill=color)
    draw.rounded_rectangle((300, 76, 408, 118), radius=18, fill=color)

    # Ranura decorativa separando gatillos del cuerpo
    draw.line([(100, 114), (216, 114)], fill=trans, width=8)
    draw.line([(296, 114), (412, 114)], fill=trans, width=8)

    # D-PAD (Cruceta direccional a la izquierda)
    cx, cy, arm, w = 158, 216, 36, 24
    draw.rounded_rectangle((cx - w//2, cy - arm, cx + w//2, cy + arm), radius=6, fill=trans)
    draw.rounded_rectangle((cx - arm, cy - w//2, cx + arm, cy + w//2), radius=6, fill=trans)

    # BOTONES DE ACCIÓN (4 botones en rombo a la derecha: A, B, X, Y)
    bx, by, b_r, spread = 354, 216, 11, 28
    draw.ellipse((bx - b_r, by - spread - b_r, bx + b_r, by - spread + b_r), fill=trans)  # Arriba (Y)
    draw.ellipse((bx - b_r, by + spread - b_r, bx + b_r, by + spread + b_r), fill=trans)  # Abajo (A)
    draw.ellipse((bx - spread - b_r, by - b_r, bx - spread + b_r, by + b_r), fill=trans)  # Izquierda (X)
    draw.ellipse((bx + spread - b_r, by - b_r, bx + spread + b_r, by + b_r), fill=trans)  # Derecha (B)

    # Dos botones centrales (Select & Start / Menú)
    draw.ellipse((220 - 7, 206 - 7, 220 + 7, 206 + 7), fill=trans)
    draw.ellipse((292 - 7, 206 - 7, 292 + 7, 206 + 7), fill=trans)

    # Touchpad / Botón Home central superior redondeado
    draw.rounded_rectangle((226, 136, 286, 164), radius=8, fill=trans)

    return img

def make_gamepad_quad():
    img = draw_gamepad(YELLOW, TRANSPARENT_YELLOW)
    return save_quad_icon(img, "quad_jugar", YELLOW, TRANSPARENT_YELLOW)

def make_gamepad_single_white():
    img = draw_gamepad(WHITE, TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_jugar_w.png", WHITE, TRANSPARENT_WHITE)

# ==============================================================================
# 2. ICONO DE TIENDA OFICIAL REDISEÑADO CON DIMENSIONES Y COLOR ARMONIZADOS
# Ancho master contenido a ~180px (en vez de 229px) y color exacto #FEEB00
# ==============================================================================
def draw_store_cart(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Proporciones contenidas y centradas (x entre 80 y 432 en 512px -> ~176px en 256px)
    # Mango superior izquierdo
    draw_thick_line(draw, (84, 100), (140, 100), 34, color)
    draw_thick_line(draw, (140, 100), (190, 330), 34, color)
    draw_thick_line(draw, (190, 330), (394, 330), 32, color)

    # Cesta del carrito (trapecio con esquinas suavizadas)
    basket_pts = [(154, 150), (432, 150), (396, 286), (180, 286)]
    draw.polygon(basket_pts, fill=color)
    for i in range(len(basket_pts)):
        draw_thick_line(draw, basket_pts[i], basket_pts[(i+1) % len(basket_pts)], 28, color)

    # 3 Ranuras verticales limpias para efecto de rejilla de carrito
    for rx in (236, 294, 350):
        draw_thick_line(draw, (rx, 178), (rx - 4, 258), 18, trans)

    # Ruedas circulares inferiores estilizadas con hueco central
    for wx in (226, 368):
        wy, wr = 398, 38
        draw.ellipse((wx - wr, wy - wr, wx + wr, wy + wr), fill=color)
        draw.ellipse((wx - 14, wy - 14, wx + 14, wy + 14), fill=trans)

    return img

def make_store_cart_quad():
    img = draw_store_cart(YELLOW, TRANSPARENT_YELLOW)
    return save_quad_icon(img, "quad_tienda", YELLOW, TRANSPARENT_YELLOW)

def make_store_cart_single_white():
    img = draw_store_cart(WHITE, TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_tienda_w.png", WHITE, TRANSPARENT_WHITE)

make_gamepad_quad()
make_gamepad_single_white()
make_store_cart_quad()
make_store_cart_single_white()
print("All updated icons generated successfully!")
