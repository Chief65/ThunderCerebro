import os
import math
from PIL import Image, ImageDraw

out_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(out_dir, exist_ok=True)

# Color amarillo-anaranjado de ThunderMC (#FFC800 -> RGB: 255, 200, 0) para los apartados 2x2
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)

# Color blanco puro (#FFFFFF) para iconos de título, botón de ir e iconos simples del footer
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

SIZE = 512
FINAL_SINGLE = 128
FINAL_QUAD_MASTER = 256  # Se divide en 4 cuadrantes de 128x128 (TL, TR, BL, BR)

def clean_rgba(img, target_size, solid_color, transparent_color):
    resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    alpha = resized.split()[3]
    clean = Image.new("RGBA", (target_size, target_size), transparent_color)
    solid = Image.new("RGBA", (target_size, target_size), solid_color)
    clean.paste(solid, mask=alpha)
    return clean

def add_corner_anchors(tile, rgb=(254, 235, 0)):
    """Añade 1 píxel alfa=1 invisible en las 4 esquinas para impedir cualquier auto-crop del CDN de Discord."""
    px = tile.load()
    w, h = tile.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if px[x, y][3] == 0:
            px[x, y] = (rgb[0], rgb[1], rgb[2], 1)
    return tile

def save_single_icon(img, name, color=WHITE, trans=TRANSPARENT_WHITE):
    clean = clean_rgba(img, FINAL_SINGLE, color, trans)
    clean = add_corner_anchors(clean, color[:3])
    path = os.path.join(out_dir, name)
    clean.save(path, "PNG")
    print(f"Saved single icon: {path}")
    return path

def save_quad_icon(img, prefix, color=YELLOW, trans=TRANSPARENT_YELLOW):
    """Convierte un icono 512x512 en un master 256x256 en #FEEB00 y lo corta en 4 partes 128x128 exactas."""
    master = clean_rgba(img, FINAL_QUAD_MASTER, color, trans)
    preview = Image.new("RGBA", (FINAL_QUAD_MASTER, FINAL_QUAD_MASTER), (43, 45, 49, 255))
    preview.alpha_composite(master)
    preview.save(os.path.join(out_dir, f"preview_{prefix}.png"), "PNG")

    quads = {
        "tl": master.crop((0,   0,   128, 128)),
        "tr": master.crop((128, 0,   256, 128)),
        "bl": master.crop((0,   128, 128, 256)),
        "br": master.crop((128, 128, 256, 256)),
    }
    paths = {}
    for qname, tile in quads.items():
        tile = add_corner_anchors(tile, color[:3])
        p = os.path.join(out_dir, f"{prefix}_{qname}.png")
        tile.save(p, "PNG")
        paths[qname] = p
    print(f"Saved 2x2 quad icon set: {prefix}_[tl,tr,bl,br].png")
    return paths

def draw_thick_line(draw, p1, p2, width, color):
    draw.line([p1, p2], fill=color, width=width)
    r = width // 2
    for x, y in (p1, p2):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)

# ── 5 ICONOS FRAGMENTADOS EN 4 PARTES (2x2) EN AMARILLO THUNDER (#FEEB00) ──

# 1. EMPEZAR A JUGAR (2x2): Joystick Arcade Clásico (como el emoji 🕹️) en #FEEB00
def make_arcade_joystick_quad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)

    # Palanca / eje central conectando la bola con la base
    draw.rounded_rectangle((234, 170, 278, 336), radius=20, fill=YELLOW)

    # Bola superior del joystick (esfera grande y limpia centrada en X=256, Y=128)
    bx, by, br = 256, 126, 78
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=YELLOW)
    # Brillo curvo recortado en la esquina superior izquierda de la bola para darle volumen de 🕹️
    draw.arc((bx - 52, by - 52, bx + 28, by + 28), start=195, end=265, fill=TRANSPARENT_YELLOW, width=16)

    # Anillo / fuelle de goma en la base de la palanca (con separación limpia de la carcasa)
    draw.rounded_rectangle((176, 304, 336, 348), radius=22, fill=YELLOW)
    draw.rectangle((160, 346, 352, 358), fill=TRANSPARENT_YELLOW)

    # Base arcade inferior (plataforma robusta redondeada)
    draw.rounded_rectangle((76, 358, 436, 462), radius=42, fill=YELLOW)

    # Botones arcade en relieve sobre el lado izquierdo/derecho de la base
    draw.rounded_rectangle((112, 336, 168, 366), radius=12, fill=YELLOW)
    draw.rounded_rectangle((344, 336, 400, 366), radius=12, fill=YELLOW)

    # Dos recortes circulares o indicadores frontales en la base para detalle visual limpio
    draw.ellipse((132, 392, 168, 428), fill=TRANSPARENT_YELLOW)
    draw.ellipse((344, 392, 380, 428), fill=TRANSPARENT_YELLOW)
    draw.rounded_rectangle((204, 402, 308, 420), radius=9, fill=TRANSPARENT_YELLOW)

    return save_quad_icon(img, "quad_jugar", YELLOW, TRANSPARENT_YELLOW)

# 2. CHAT DE VOZ (2x2): Micrófono grande y centrado en #FEEB00
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
    return save_quad_icon(img, "quad_voz", YELLOW, TRANSPARENT_YELLOW)

# 3. NORMATIVA Y REGLAS (2x2): Documento de reglas grande y centrado en #FEEB00
def make_rules_quad():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_YELLOW)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((96, 52, 416, 464), radius=52, fill=YELLOW)
    line_specs = [
        (156, 146, 356, 186),
        (156, 238, 356, 278),
        (156, 330, 290, 370),
    ]
    for x1, y1, x2, y2 in line_specs:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=20, fill=TRANSPARENT_YELLOW)
    return save_quad_icon(img, "quad_reglas", YELLOW, TRANSPARENT_YELLOW)

# 4. POSTULACIONES (2x2): Persona con casco y chaqueta de trabajador en #FEEB00
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

    return save_quad_icon(img, "quad_post", YELLOW, TRANSPARENT_YELLOW)

# 5. SOPORTE (2x2): Auriculares de Soporte / Headset con micrófono en #FEEB00
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

    return save_quad_icon(img, "quad_soporte", YELLOW, TRANSPARENT_YELLOW)

# ── ICONOS SIMPLES EN BLANCO PURO (#FFFFFF) PARA TÍTULOS, BOTÓN DE IR Y FOOTER ──

def make_signpost_icon():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((234, 56, 278, 456), radius=22, fill=WHITE)
    draw.rounded_rectangle((176, 420, 336, 456), radius=18, fill=WHITE)
    sign_right = [(104, 108), (384, 108), (444, 158), (384, 208), (104, 208)]
    draw.polygon(sign_right, fill=WHITE)
    for i in range(len(sign_right)):
        draw_thick_line(draw, sign_right[i], sign_right[(i+1) % len(sign_right)], 20, WHITE)
    sign_left = [(408, 248), (128, 248), (68, 298), (128, 348), (408, 348)]
    draw.polygon(sign_left, fill=WHITE)
    for i in range(len(sign_left)):
        draw_thick_line(draw, sign_left[i], sign_left[(i+1) % len(sign_left)], 20, WHITE)
    draw.ellipse((242, 144, 270, 172), fill=TRANSPARENT_WHITE)
    draw.ellipse((242, 284, 270, 312), fill=TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_cartel_w.png", WHITE, TRANSPARENT_WHITE)

# Icono de Libro Guía en blanco (#FFFFFF) para el título de Información
def make_guide_book_icon():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    # Página izquierda y página derecha de un libro abierto
    left_page = [(56, 92), (232, 122), (232, 424), (56, 394)]
    right_page = [(456, 92), (280, 122), (280, 424), (456, 394)]
    draw.polygon(left_page, fill=WHITE)
    for i in range(len(left_page)):
        draw_thick_line(draw, left_page[i], left_page[(i+1) % len(left_page)], 28, WHITE)
    draw.polygon(right_page, fill=WHITE)
    for i in range(len(right_page)):
        draw_thick_line(draw, right_page[i], right_page[(i+1) % len(right_page)], 28, WHITE)
    # Líneas de guía redondeadas recortadas en la página izquierda
    draw_thick_line(draw, (102, 186), (190, 201), 28, TRANSPARENT_WHITE)
    draw_thick_line(draw, (102, 256), (190, 271), 28, TRANSPARENT_WHITE)
    draw_thick_line(draw, (102, 326), (162, 336), 28, TRANSPARENT_WHITE)
    # Marcapáginas recortado en la parte superior de la página derecha
    bookmark = [(336, 90), (396, 80), (396, 250), (366, 222), (336, 250)]
    draw.polygon(bookmark, fill=TRANSPARENT_WHITE)
    return save_single_icon(img, "icon_libro_w.png", WHITE, TRANSPARENT_WHITE)

# Icono para el botón "Ir" (reemplaza "Click para ir"): Flecha moderna de acceso / ir (➔) en blanco
def make_go_arrow_icon():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    # Línea horizontal gruesa + punta de flecha redondeada hacia la derecha
    draw_thick_line(draw, (84, 256), (404, 256), 64, WHITE)
    draw_thick_line(draw, (268, 120), (416, 256), 64, WHITE)
    draw_thick_line(draw, (268, 392), (416, 256), 64, WHITE)
    return save_single_icon(img, "icon_ir_w.png", WHITE, TRANSPARENT_WHITE)

# Icono de Tienda Oficial (Carrito de compra minimalista en blanco)
def make_store_bag_icon():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    # Mango superior izquierdo + brazo inclinado hasta la base del chasis
    draw_thick_line(draw, (42, 82), (108, 82), 40, WHITE)
    draw_thick_line(draw, (108, 82), (168, 344), 40, WHITE)
    draw_thick_line(draw, (168, 344), (404, 344), 38, WHITE)
    # Cesta del carrito (trapezoide sólido con bordes redondeados)
    basket_pts = [(126, 140), (460, 140), (414, 290), (156, 290)]
    draw.polygon(basket_pts, fill=WHITE)
    for i in range(len(basket_pts)):
        draw_thick_line(draw, basket_pts[i], basket_pts[(i+1) % len(basket_pts)], 32, WHITE)
    # Dos ranuras verticales recortadas en la cesta para darle silueta de carrito
    draw_thick_line(draw, (238, 178), (246, 254), 26, TRANSPARENT_WHITE)
    draw_thick_line(draw, (334, 178), (326, 254), 26, TRANSPARENT_WHITE)
    # Dos ruedas circulares inferiores
    for wx in (196, 380):
        wy, wr = 424, 42
        draw.ellipse((wx - wr, wy - wr, wx + wr, wy + wr), fill=WHITE)
    return save_single_icon(img, "icon_carrito_w.png", WHITE, TRANSPARENT_WHITE)

# Icono 2x2 de TikTok (Nota musical característica de TikTok en blanco dividida en 4 partes)
def make_tiktok_icon():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    # Tallo vertical de la nota TikTok
    draw.rounded_rectangle((256, 56, 326, 356), radius=32, fill=WHITE)
    # Anillo circular inferior izquierdo (el loop de la 'd' de TikTok)
    draw.ellipse((88, 236, 326, 464), fill=WHITE)
    draw.ellipse((156, 304, 256, 400), fill=TRANSPARENT_WHITE)
    # Bandera curva superior derecha de TikTok saliendo de la cima del tallo (90° a 180° de un círculo superior derecho)
    draw.arc((256, -72, 540, 212), start=90, end=180, fill=WHITE, width=70)
    draw.ellipse((370, 142, 438, 212), fill=WHITE)
    save_single_icon(img, "icon_tiktok_w.png", WHITE, TRANSPARENT_WHITE)
    return save_quad_icon(img, "quad_tiktok", WHITE, TRANSPARENT_WHITE)

# Icono 2x2 de YouTube (Pantalla redondeada con triángulo Play recortado en el centro dividida en 4 partes)
def make_youtube_icon():
    img = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((44, 108, 468, 404), radius=82, fill=WHITE)
    # Triángulo Play recortado en el centro
    play_pts = [(214, 188), (214, 324), (336, 256)]
    draw.polygon(play_pts, fill=TRANSPARENT_WHITE)
    save_single_icon(img, "icon_youtube_w.png", WHITE, TRANSPARENT_WHITE)
    return save_quad_icon(img, "quad_youtube", WHITE, TRANSPARENT_WHITE)

def create_base_hand_white():
    hand = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
    d = ImageDraw.Draw(hand)
    d.rounded_rectangle((176, 228, 364, 412), radius=84, fill=WHITE)
    draw_thick_line(d, (196, 270), (196, 126), 36, WHITE)
    draw_thick_line(d, (246, 265), (246, 98),  36, WHITE)
    draw_thick_line(d, (296, 270), (296, 114), 36, WHITE)
    draw_thick_line(d, (344, 285), (344, 154), 34, WHITE)
    draw_thick_line(d, (206, 344), (118, 244), 40, WHITE)
    return hand

def draw_sparkle_white(draw, cx, cy, size):
    if size <= 2:
        return
    pts = [
        (cx, cy - size),
        (cx + size * 0.28, cy - size * 0.28),
        (cx + size, cy),
        (cx + size * 0.28, cy + size * 0.28),
        (cx, cy + size),
        (cx - size * 0.28, cy + size * 0.28),
        (cx - size, cy),
        (cx - size * 0.28, cy - size * 0.28),
    ]
    draw.polygon(pts, fill=WHITE)

def make_animated_welcome_gif_white():
    base_hand = create_base_hand_white()
    frames = []
    num_frames = 16
    for i in range(num_frames):
        t = (i / num_frames) * 2 * math.pi
        angle = math.sin(t) * 14.0
        rotated = base_hand.rotate(angle, resample=Image.Resampling.BICUBIC, center=(266, 368))
        
        overlay = Image.new("RGBA", (SIZE, SIZE), TRANSPARENT_WHITE)
        od = ImageDraw.Draw(overlay)
        
        if math.sin(t) > 0.15:
            od.arc((48, 72, 218, 242), start=195, end=255, fill=WHITE, width=26)
        elif math.sin(t) < -0.15:
            od.arc((304, 72, 474, 242), start=285, end=345, fill=WHITE, width=26)
            
        s1 = int(max(0, math.sin(t) * 40))
        s2 = int(max(0, -math.sin(t) * 40))
        draw_sparkle_white(od, 84, 124, s1)
        draw_sparkle_white(od, 434, 124, s2)
        
        combined = Image.alpha_composite(rotated, overlay)
        small = combined.resize((FINAL_SINGLE, FINAL_SINGLE), Image.Resampling.LANCZOS)
        
        alpha = small.split()[3]
        bw_mask = alpha.point(lambda a: 255 if a > 95 else 0)
        p_img = Image.new("P", (FINAL_SINGLE, FINAL_SINGLE), 0)
        palette = [0, 0, 0, 255, 255, 255] + [0] * (256 * 3 - 6)
        p_img.putpalette(palette)
        p_img.paste(1, mask=bw_mask)
        p_img.info["transparency"] = 0
        frames.append(p_img)
    
    gif_path = os.path.join(out_dir, "icon_bienvenida_w.gif")
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        transparency=0,
        disposal=2
    )
    print(f"Saved white animated GIF {gif_path}")

make_arcade_joystick_quad()
make_mic_quad()
make_rules_quad()
make_apply_quad()
make_support_quad()
make_signpost_icon()
make_guide_book_icon()
make_go_arrow_icon()
make_store_bag_icon()
make_tiktok_icon()
make_youtube_icon()
make_animated_welcome_gif_white()

# Preparar copias con anclaje de esquina (alpha=1) del logo limpio de 10 partes (5x2) para evitar auto-crop de Discord
emojis_10_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\emojis_thunder\10_partes_5x2"
for i in range(1, 11):
    fname = f"thunder_5x2_limpio_{i}.png"
    src = os.path.join(emojis_10_dir, fname)
    im = Image.open(src).convert("RGBA")
    im = add_corner_anchors(im, (255, 255, 255))
    dst = os.path.join(out_dir, f"anchored_{fname}")
    im.save(dst, "PNG")
    print(f"Saved anchored 10-part logo tile: {dst}")
