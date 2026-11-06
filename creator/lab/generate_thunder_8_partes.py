import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_erosion, binary_fill_holes

out_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\emojis_thunder\8_partes_4x2"
os.makedirs(out_dir, exist_ok=True)

# 1. Load clean THUNDER logo, remove stray x=0 pixels, and decontaminate outer perimeter
raw_logo = Image.open(r"C:\Users\PC\Desktop\ThunderCerebro\raw\assets\thunder_full_logo.png").convert("RGBA")
arr = np.array(raw_logo)
arr[:, :7, :] = 0
clean_bbox = Image.fromarray(arr).getbbox()  # (9, 24, 500, 131) -> 491 x 107
logo_crop = np.array(Image.fromarray(arr).crop(clean_bbox)).astype(np.float32)

alpha = logo_crop[:, :, 3]
filled_silhouette = binary_fill_holes(alpha > 80)
inner_core = binary_erosion(filled_silhouette, iterations=2)
outer_rim = (alpha > 0) & (~inner_core)

h_c, w_c, _ = logo_crop.shape
for y in range(h_c):
    for x in range(w_c):
        if outer_rim[y, x]:
            r, g, b, a = logo_crop[y, x]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            if lum > 45:
                if 194 <= x <= 282:
                    logo_crop[y, x, :3] = [62, 11, 4]
                else:
                    logo_crop[y, x, :3] = [10, 18, 34]
            if a < 110:
                logo_crop[y, x] = [0, 0, 0, 0]
            else:
                logo_crop[y, x, 3] = 255

for y in range(90, 105):
    for x in range(12, 28):
        r, g, b, a = logo_crop[y, x]
        if a > 0 and (r > 65 and g > 65 and b > 65):
            logo_crop[y, x, :3] = [14, 27, 48]

logo_clean = Image.fromarray(logo_crop.astype(np.uint8))
# Original clean aspect ratio: 491 x 107 (4.588 : 1)


# ==============================================================================
# LIENZO 4x2 (4 EMOJIS ARRIBA + 4 EMOJIS ABAJO = 8 PARTES DE 256x256 -> 1024 x 512 px)
# ==============================================================================
W, H = 1024, 512

# ------------------------------------------------------------------------------
# OPCION A: CON PLACA PIXEL-ART 3D + BORDE DORADO + CHISPAS (4x2 -> 1024 x 512)
# Construida nativamente en rejilla cuadrada 256 x 128 (escala 4x exacta, CERO estiramiento)
# ------------------------------------------------------------------------------
gw, gh = 256, 128
grid = np.zeros((gh, gw, 4), dtype=np.uint8)

def set_px(x, y, rgba):
    if 0 <= x < gw and 0 <= y < gh:
        grid[y, x] = rgba

# Muescas del borde dorado superior
notches = [(66, 75), (128, 136), (184, 193)]
def in_notch(x):
    return any(a <= x <= b for a, b in notches)
def notch_edge(x):
    return any(x == a - 1 or x == b + 1 for a, b in notches)

# La placa ocupa desde y = 16 hasta y = 112 en la rejilla de 128 (es decir, y = 64..448 en 512px)
# Con las chispas desde y = 4 hasta y = 123 (y = 16..492 en 512px), ocupando las 2 líneas completas
# mientras las letras THUNDER mantienen su proporción natural sin estirar.
top_base = 17
front_bot = 94
ext_bot = 111

for y in range(top_base, ext_bot + 1):
    if y <= front_bot:
        t = (y - top_base) / float(front_bot - top_base)
        inset = int(round(10 * (1.0 - t)))
        left = 8 + inset
        right = (gw - 9) - inset
    else:
        dy = y - front_bot
        left = 8 + int(round(dy * 1.25))
        right = (gw - 9) - int(round(dy * 1.25))

    for x in range(left, right + 1):
        # Escalones inferiores 3D (estilo ConcordMC)
        if y >= 109 and (50 <= x <= 156 or x < 30 or x > 225):
            continue
        if y >= 106 and (66 <= x <= 142 or x < 22 or x > 233):
            continue
        if y >= 110 and (157 <= x <= 184):
            continue

        top_y = (top_base + 3) if in_notch(x) else top_base
        if y < top_y:
            continue

        is_left_border = (x == left) or (x == left + 1)
        is_right_border = (x == right) or (x == right - 1)
        is_bottom_border = (
            y == ext_bot
            or (y == 108 and (50 <= x <= 156 or x < 30 or x > 225))
            or (y == 105 and (66 <= x <= 142 or x < 22 or x > 233))
            or (y == 109 and (157 <= x <= 184))
        )

        # Contorno exterior oscuro
        if is_left_border or is_right_border or is_bottom_border or y in (top_y, top_y + 1):
            set_px(x, y, (24, 7, 3, 255))
            continue

        # Borde superior dorado biselado (3 unidades de grosor en la rejilla: top_y+2..top_y+4)
        if top_y + 2 <= y <= top_y + 4:
            if y == top_y + 2:
                set_px(x, y, (246, 236, 102, 255))
            elif y == top_y + 3:
                set_px(x, y, (224, 210, 82, 255))
            else:
                set_px(x, y, (188, 172, 62, 255))
            continue

        # Bisel dorado lateral que baja degradándose hacia el terracota
        if y < 64 and (x in (left + 2, left + 3, left + 4, right - 2, right - 3, right - 4)):
            fade = max(0.0, 1.0 - (y - (top_base + 4)) / 44.0)
            r = int(232 * fade + 162 * (1 - fade))
            g = int(214 * fade + 68 * (1 - fade))
            b = int(86 * fade + 36 * (1 - fade))
            set_px(x, y, (r, g, b, 255))
            continue

        # Línea oscura separadora bajo el borde dorado
        if y in (top_y + 5, top_y + 6) or (y in range(top_base + 2, top_base + 8) and notch_edge(x)):
            set_px(x, y, (28, 6, 2, 255))
            continue

        # Cara frontal de piedra/terracota (y = top_y+7 .. front_bot)
        if y <= front_bot:
            fy = (y - (top_base + 7)) / float(front_bot - (top_base + 7))
            if fy < 0.52:
                t2 = fy / 0.52
                r = int(196 * (1 - t2) + 170 * t2)
                g = int(96 * (1 - t2) + 72 * t2)
                b = int(50 * (1 - t2) + 38 * t2)
            else:
                t2 = (fy - 0.52) / 0.48
                r = int(170 * (1 - t2) + 108 * t2)
                g = int(72 * (1 - t2) + 38 * t2)
                b = int(38 * (1 - t2) + 30 * t2)
            set_px(x, y, (r, g, b, 255))
        else:
            # Extrusión 3D inferior en sombra marrón-rojiza muy oscura
            if y in (front_bot + 1, front_bot + 2):
                set_px(x, y, (74, 22, 15, 255))
            else:
                fy2 = (y - (front_bot + 3)) / float(ext_bot - (front_bot + 3))
                r = int(52 * (1 - fy2) + 30 * fy2)
                g = int(12 * (1 - fy2) + 6 * fy2)
                b = int(5 * (1 - fy2) + 2 * fy2)
                set_px(x, y, (r, g, b, 255))

# Líneas de bloques/ladrillos pixel-art arriba y abajo del texto
brick_H = [
    (28, 22, 64), (30, 102, 168), (28, 192, 234),
    (34, 48, 118), (34, 154, 218),
    (82, 18, 86), (84, 98, 168), (82, 180, 238),
    (89, 34, 124), (89, 144, 222),
]
for by, x1, x2 in brick_H:
    for x in range(x1, x2 + 1):
        if grid[by, x, 3] > 0 and by <= front_bot:
            grid[by, x] = (88, 30, 22, 255)
            if by + 1 <= front_bot and grid[by + 1, x, 3] > 0:
                c = grid[by + 1, x]
                grid[by + 1, x] = (min(255, int(c[0] * 1.15)), min(255, int(c[1] * 1.15)), min(255, int(c[2] * 1.15)), 255)

brick_V = [
    (38, 24, 34), (82, 24, 36), (118, 24, 34), (168, 24, 35), (210, 24, 35),
    (46, 78, 94), (86, 80, 94), (124, 80, 94), (168, 78, 94), (204, 80, 94),
]
for bx, y1, y2 in brick_V:
    for y in range(y1, y2 + 1):
        if grid[y, bx, 3] > 0 and y <= front_bot:
            grid[y, bx] = (84, 28, 20, 255)

# Grietas triangulares bajo el borde dorado
for cx in [44, 82, 154, 212]:
    for dy in range(3):
        for dx in range(3 - dy):
            set_px(cx + dx, top_base + 7 + dy, (28, 6, 2, 255))

# Partículas/chispas cuadradas (sin deformación) arriba, abajo y a los lados
sparks = [
    # Arriba (Fila 1)
    (20, 11, 3), (36, 6, 2), (64, 4, 3), (88, 10, 2), (112, 5, 3),
    (148, 7, 3), (176, 4, 2), (198, 9, 3), (224, 5, 2), (244, 16, 2),
    # Lados
    (5, 42, 2), (249, 38, 2), (4, 78, 2), (250, 82, 2),
    # Abajo (Fila 2)
    (24, 102, 3), (48, 115, 2), (76, 118, 3), (118, 112, 3),
    (152, 119, 2), (188, 114, 3), (218, 117, 2), (240, 101, 3),
]
for sx, sy, sz in sparks:
    for dy in range(sz):
        for dx in range(sz):
            is_core = (dx < sz - 1 and dy < sz - 1) if sz > 1 else True
            color = (242, 130, 28, 255) if is_core else (175, 82, 22, 215)
            set_px(sx + dx, sy + dy, color)

plate_4x2 = Image.fromarray(grid).resize((W, H), Image.Resampling.NEAREST)

# Colocar el logo THUNDER con su proporción 100% ORIGINAL (sin estirar verticalmente)
# Ancho 868 px -> Alto natural = 868 * (107 / 491) = 189 px
logo_w_placa = 868
logo_h_placa = int(round(logo_clean.height * (logo_w_placa / logo_clean.width)))  # 189 px (proporción 1:1 exacta)
logo_for_placa = logo_clean.resize((logo_w_placa, logo_h_placa), Image.Resampling.LANCZOS)

lx = (W - logo_w_placa) // 2
ly = 136  # Centrado en la placa frontal (y=68..376), cruzando limpiamente ambas filas (y=256)

alpha_mask = logo_for_placa.split()[3]
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dark_silhouette = Image.new("RGBA", (logo_w_placa, logo_h_placa), (24, 5, 2, 255))

for sdx in [-4, 0, 4]:
    for sdy in [-4, 0, 4, 8, 12]:
        shadow_layer.paste(dark_silhouette, (lx + sdx, ly + sdy), alpha_mask)

combined_4x2_placa = Image.alpha_composite(plate_4x2, shadow_layer)
combined_4x2_placa.paste(logo_for_placa, (lx, ly), logo_for_placa)

combined_4x2_placa.save(os.path.join(out_dir, "thunder_4x2_placa_full.png"))
idx = 1
for row in range(2):
    for col in range(4):
        tile = combined_4x2_placa.crop((col * 256, row * 256, (col + 1) * 256, (row + 1) * 256))
        tile.save(os.path.join(out_dir, f"thunder_4x2_placa_{idx}.png"))
        idx += 1


# ------------------------------------------------------------------------------
# OPCION B: LOGO LIMPIO EN 4x2 SIN ESTIRAR (1024 x 512)
# Proporción original: Ancho 1008 px -> Alto 220 px (centrado en la unión de las 2 filas)
# ------------------------------------------------------------------------------
canvas_4x2_limpio = Image.new("RGBA", (W, H), (0, 0, 0, 0))
logo_w_limpio = 1008
logo_h_limpio = int(round(logo_clean.height * (logo_w_limpio / logo_clean.width)))  # 220 px
logo_for_limpio = logo_clean.resize((logo_w_limpio, logo_h_limpio), Image.Resampling.LANCZOS)
canvas_4x2_limpio.paste(logo_for_limpio, ((W - logo_w_limpio) // 2, (H - logo_h_limpio) // 2), logo_for_limpio)

canvas_4x2_limpio.save(os.path.join(out_dir, "thunder_4x2_limpio_full.png"))
idx = 1
for row in range(2):
    for col in range(4):
        tile = canvas_4x2_limpio.crop((col * 256, row * 256, (col + 1) * 256, (row + 1) * 256))
        tile.save(os.path.join(out_dir, f"thunder_4x2_limpio_{idx}.png"))
        idx += 1


# ==============================================================================
# PREVIEW SHEET (ESCALA REAL DISCORD JUMBO 4x2 = 192x96 px + ESCALA COMPLETA 1024x512)
# ==============================================================================
def alpha_paste(dst, src, pos):
    tmp = Image.new("RGBA", dst.size, (0, 0, 0, 0))
    tmp.paste(src, pos)
    return Image.alpha_composite(dst, tmp)

preview = Image.new("RGBA", (1100, 1220), (49, 51, 56, 255))

# Arriba: Escala real en Discord (4 emojis de 48x48 arriba + 4 de 48x48 abajo = 192 x 96 px)
sm_placa = combined_4x2_placa.resize((192, 96), Image.Resampling.LANCZOS)
sm_limpio = canvas_4x2_limpio.resize((192, 96), Image.Resampling.LANCZOS)
preview = alpha_paste(preview, sm_placa, (180, 24))
preview = alpha_paste(preview, sm_limpio, (680, 24))

# Debajo: Lienzos completos 1024 x 512 con la cuadrícula 4x2 marcada
y_p1 = 145
preview = alpha_paste(preview, combined_4x2_placa, (38, y_p1))

y_p2 = 685
preview = alpha_paste(preview, canvas_4x2_limpio, (38, y_p2))

draw = ImageDraw.Draw(preview)
for base_y in [y_p1, y_p2]:
    # 3 cortes verticales (dividiendo en 4 columnas de 256px)
    for col in range(1, 4):
        cx = 38 + col * 256
        for yd in range(base_y + 10, base_y + 502, 8):
            draw.line([(cx, yd), (cx, yd + 4)], fill=(255, 255, 255, 95), width=2)
    # 1 corte horizontal central (dividiendo Fila 1 y Fila 2 en y=256)
    cy = base_y + 256
    for xd in range(38, 38 + 1024, 8):
        draw.line([(xd, cy), (xd + 4, cy)], fill=(255, 200, 80, 115), width=2)

preview.save(os.path.join(out_dir, "preview_8_partes_4x2.png"))
print("Generated 8-part (4x2) un-stretched emoji sets successfully!")
