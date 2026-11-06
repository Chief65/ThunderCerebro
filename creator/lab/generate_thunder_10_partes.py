import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_erosion, binary_fill_holes

out_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\emojis_thunder\10_partes_5x2"
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


# ==============================================================================
# LIENZO 5x2 (5 EMOJIS ARRIBA + 5 EMOJIS ABAJO = 10 PIEZAS DE 256x256 -> 1280 x 512 px)
# ==============================================================================
W, H = 1280, 512

# ------------------------------------------------------------------------------
# OPCION A: CON PLACA PIXEL-ART 3D OCUPANDO EL BLOQUE MAXIMO (1280 x 512)
# Y CON EL TEXTO "THUNDER" CENTRADO EXACTAMENTE EN LA UNION DE LAS 2 LINEAS (y = 256)
# Rejilla base: 320 x 128 (escala 4x -> 1280 x 512)
# ------------------------------------------------------------------------------
gw, gh = 320, 128
grid = np.zeros((gh, gw, 4), dtype=np.uint8)

def set_px(x, y, rgba):
    if 0 <= x < gw and 0 <= y < gh:
        grid[y, x] = rgba

notches = [(76, 88), (156, 166), (232, 244)]
def in_notch(x):
    return any(a <= x <= b for a, b in notches)
def notch_edge(x):
    return any(x == a - 1 or x == b + 1 for a, b in notches)

# Hacemos que la placa ocupe casi el 100% del alto y ancho (y = 4..124 de 128 -> y = 16..496 de 512px)
# y x = 1..318 de 320 (x = 4..1272 de 1280px)
top_base = 5
front_bot = 107
ext_bot = 124

for y in range(top_base, ext_bot + 1):
    if y <= front_bot:
        t = (y - top_base) / float(front_bot - top_base)
        inset = int(round(9 * (1.0 - t)))
        left = 1 + inset
        right = (gw - 2) - inset
    else:
        dy = y - front_bot
        left = 1 + int(round(dy * 1.3))
        right = (gw - 2) - int(round(dy * 1.3))

    for x in range(left, right + 1):
        # Escalones inferiores 3D
        if y >= 122 and (60 <= x <= 195 or x < 34 or x > 285):
            continue
        if y >= 119 and (80 <= x <= 178 or x < 24 or x > 295):
            continue
        if y >= 123 and (196 <= x <= 232):
            continue

        top_y = (top_base + 3) if in_notch(x) else top_base
        if y < top_y:
            continue

        is_left_border = (x == left) or (x == left + 1)
        is_right_border = (x == right) or (x == right - 1)
        is_bottom_border = (
            y == ext_bot
            or (y == 121 and (60 <= x <= 195 or x < 34 or x > 285))
            or (y == 118 and (80 <= x <= 178 or x < 24 or x > 295))
            or (y == 122 and (196 <= x <= 232))
        )

        if is_left_border or is_right_border or is_bottom_border or y in (top_y, top_y + 1):
            set_px(x, y, (24, 7, 3, 255))
            continue

        # Borde dorado superior (top_y+2..top_y+5)
        if top_y + 2 <= y <= top_y + 5:
            if y in (top_y + 2, top_y + 3):
                set_px(x, y, (246, 236, 102, 255))
            else:
                set_px(x, y, (196, 180, 66, 255))
            continue

        # Bisel dorado lateral
        if y < 68 and (x in (left + 2, left + 3, left + 4, right - 2, right - 3, right - 4)):
            fade = max(0.0, 1.0 - (y - (top_base + 5)) / 56.0)
            r = int(232 * fade + 162 * (1 - fade))
            g = int(214 * fade + 68 * (1 - fade))
            b = int(86 * fade + 36 * (1 - fade))
            set_px(x, y, (r, g, b, 255))
            continue

        # Separador oscuro bajo el borde dorado
        if y in (top_y + 6, top_y + 7) or (y in range(top_base + 2, top_base + 9) and notch_edge(x)):
            set_px(x, y, (28, 6, 2, 255))
            continue

        # Cara frontal de piedra/terracota (y = top_y+8 .. front_bot)
        # El centro de las dos líneas está en y = 64 (256px)
        if y <= front_bot:
            fy = (y - (top_base + 8)) / float(front_bot - (top_base + 8))
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
            # Base 3D inferior en sombra profunda
            if y in (front_bot + 1, front_bot + 2):
                set_px(x, y, (74, 22, 15, 255))
            else:
                fy2 = (y - (front_bot + 3)) / float(ext_bot - (front_bot + 3))
                r = int(52 * (1 - fy2) + 30 * fy2)
                g = int(12 * (1 - fy2) + 6 * fy2)
                b = int(5 * (1 - fy2) + 2 * fy2)
                set_px(x, y, (r, g, b, 255))

# Líneas de ladrillos pixel-art arriba y abajo del texto
brick_H = [
    (18, 18, 76), (20, 118, 204), (18, 236, 302),
    (25, 44, 144), (25, 184, 282),
    (95, 14, 108), (97, 124, 212), (95, 228, 306),
    (102, 38, 154), (102, 180, 286),
]
for by, x1, x2 in brick_H:
    for x in range(x1, x2 + 1):
        if grid[by, x, 3] > 0 and by <= front_bot:
            grid[by, x] = (88, 30, 22, 255)
            if by + 1 <= front_bot and grid[by + 1, x, 3] > 0:
                c = grid[by + 1, x]
                grid[by + 1, x] = (min(255, int(c[0] * 1.15)), min(255, int(c[1] * 1.15)), min(255, int(c[2] * 1.15)), 255)

brick_V = [
    (44, 13, 25), (96, 13, 26), (144, 13, 25), (204, 13, 26), (262, 13, 25),
    (54, 90, 107), (108, 92, 107), (158, 92, 107), (212, 90, 107), (264, 92, 107),
]
for bx, y1, y2 in brick_V:
    for y in range(y1, y2 + 1):
        if grid[y, bx, 3] > 0 and y <= front_bot:
            grid[y, bx] = (84, 28, 20, 255)

for cx in [52, 96, 188, 264]:
    for dy in range(3):
        for dx in range(3 - dy):
            set_px(cx + dx, top_base + 8 + dy, (28, 6, 2, 255))

# Chispas en los bordes para aprovechar hasta el último píxel de los 10 bloques
sparks = [
    (22, 1, 3), (58, 0, 2), (105, 1, 3), (142, 0, 2), (188, 1, 3), (222, 0, 2), (268, 1, 3), (302, 2, 2),
    (18, 118, 3), (48, 124, 2), (92, 123, 3), (144, 122, 3), (185, 125, 2), (242, 124, 3), (298, 118, 3),
]
for sx, sy, sz in sparks:
    for dy in range(sz):
        for dx in range(sz):
            is_core = (dx < sz - 1 and dy < sz - 1) if sz > 1 else True
            color = (242, 130, 28, 255) if is_core else (175, 82, 22, 215)
            set_px(sx + dx, sy + dy, color)

plate_5x2 = Image.fromarray(grid).resize((W, H), Image.Resampling.NEAREST)

# Colocar el logo THUNDER GIGANTE (1180 x 286 px) CENTRADO EXACTAMENTE EN LA LINEA DIVISORIA y = 256!
# Así la mitad superior (y = 113..256, 143px) está en los 5 emojis de arriba
# y la mitad inferior (y = 256..399, 143px) está en los 5 emojis de abajo!
logo_w_placa = 1180
logo_h_placa = 286
logo_for_placa = logo_clean.resize((logo_w_placa, logo_h_placa), Image.Resampling.LANCZOS)

lx = (W - logo_w_placa) // 2
ly = (H - logo_h_placa) // 2  # y = 113 (Centro exacto en y = 256!)

alpha_mask = logo_for_placa.split()[3]
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dark_silhouette = Image.new("RGBA", (logo_w_placa, logo_h_placa), (24, 5, 2, 255))

for sdx in [-5, 0, 5]:
    for sdy in [-5, 0, 5, 10, 14]:
        shadow_layer.paste(dark_silhouette, (lx + sdx, ly + sdy), alpha_mask)

combined_5x2_placa = Image.alpha_composite(plate_5x2, shadow_layer)
combined_5x2_placa.paste(logo_for_placa, (lx, ly), logo_for_placa)

combined_5x2_placa.save(os.path.join(out_dir, "thunder_5x2_placa_full.png"))
idx = 1
for row in range(2):
    for col in range(5):
        tile = combined_5x2_placa.crop((col * 256, row * 256, (col + 1) * 256, (row + 1) * 256))
        tile.save(os.path.join(out_dir, f"thunder_5x2_placa_{idx}.png"))
        idx += 1


# ------------------------------------------------------------------------------
# OPCION B: LOGO LIMPIO EN 5x2 OCUPANDO EL MAXIMO BLOQUE Y CENTRADO EN y = 256
# Ancho máximo = 1272 px (de 1280 px), Alto = 360 px (centrado en y = 256: y = 76..436)
# ------------------------------------------------------------------------------
canvas_5x2_limpio = Image.new("RGBA", (W, H), (0, 0, 0, 0))
logo_w_limpio = 1272
logo_h_limpio = 360
logo_for_limpio = logo_clean.resize((logo_w_limpio, logo_h_limpio), Image.Resampling.LANCZOS)
canvas_5x2_limpio.paste(logo_for_limpio, ((W - logo_w_limpio) // 2, (H - logo_h_limpio) // 2), logo_for_limpio)

canvas_5x2_limpio.save(os.path.join(out_dir, "thunder_5x2_limpio_full.png"))
idx = 1
for row in range(2):
    for col in range(5):
        tile = canvas_5x2_limpio.crop((col * 256, row * 256, (col + 1) * 256, (row + 1) * 256))
        tile.save(os.path.join(out_dir, f"thunder_5x2_limpio_{idx}.png"))
        idx += 1


# ==============================================================================
# PREVIEW SHEET (ESCALA REAL DISCORD JUMBO 5x2 = 240x96 px + ESCALA COMPLETA 1280x512)
# ==============================================================================
def alpha_paste(dst, src, pos):
    tmp = Image.new("RGBA", dst.size, (0, 0, 0, 0))
    tmp.paste(src, pos)
    return Image.alpha_composite(dst, tmp)

preview = Image.new("RGBA", (1360, 1220), (49, 51, 56, 255))

# Arriba: Escala real en Discord (5 emojis de 48x48 arriba + 5 de 48x48 abajo = 240 x 96 px)
sm_placa = combined_5x2_placa.resize((240, 96), Image.Resampling.LANCZOS)
sm_limpio = canvas_5x2_limpio.resize((240, 96), Image.Resampling.LANCZOS)
preview = alpha_paste(preview, sm_placa, (220, 24))
preview = alpha_paste(preview, sm_limpio, (820, 24))

# Debajo: Lienzos completos 1280 x 512 con la cuadrícula 5x2 marcada
y_p1 = 145
preview = alpha_paste(preview, combined_5x2_placa, (40, y_p1))

y_p2 = 685
preview = alpha_paste(preview, canvas_5x2_limpio, (40, y_p2))

draw = ImageDraw.Draw(preview)
for base_y in [y_p1, y_p2]:
    # Borde exterior del bloque completo 5x2
    draw.rectangle([40, base_y, 40 + 1280, base_y + 512], outline=(255, 255, 255, 50), width=1)
    # 4 cortes verticales (dividiendo en 5 columnas de 256px)
    for col in range(1, 5):
        cx = 40 + col * 256
        for yd in range(base_y, base_y + 512, 8):
            draw.line([(cx, yd), (cx, yd + 4)], fill=(255, 255, 255, 100), width=2)
    # 1 corte horizontal central (dividiendo Fila 1 y Fila 2 exactamente en y=256)
    cy = base_y + 256
    for xd in range(40, 40 + 1280, 8):
        draw.line([(xd, cy), (xd + 4, cy)], fill=(255, 200, 80, 130), width=2)

preview.save(os.path.join(out_dir, "preview_10_partes_5x2.png"))
print("Generated 10-part (5x2) full-block centered emoji sets successfully!")
