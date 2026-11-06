import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_erosion, binary_fill_holes

out_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\emojis_thunder\6_partes"
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
# MODALIDAD 1: 6 EMOJIS EN FILA HORIZONTAL (6x1 -> 1536 x 256 px, 6 de 256x256)
# ==============================================================================
W6, H6 = 1536, 256

# 1A. Logo Limpio 6x1 (Ocupando los 6 bloques de ancho y casi todo el alto 244px)
canvas_6x1_limpio = Image.new("RGBA", (W6, H6), (0, 0, 0, 0))
tw_6x1 = 1512
th_6x1 = 244
logo_6x1 = logo_clean.resize((tw_6x1, th_6x1), Image.Resampling.LANCZOS)
canvas_6x1_limpio.paste(logo_6x1, ((W6 - tw_6x1) // 2, (H6 - th_6x1) // 2), logo_6x1)

canvas_6x1_limpio.save(os.path.join(out_dir, "thunder_6x1_limpio_full.png"))
for i in range(6):
    tile = canvas_6x1_limpio.crop((i * 256, 0, (i + 1) * 256, 256))
    tile.save(os.path.join(out_dir, f"thunder_6x1_limpio_{i+1}.png"))

# 1B. Logo con Placa Pixel-Art 6x1 (1536 x 256 px)
gw, gh = 384, 64
grid6 = np.zeros((gh, gw, 4), dtype=np.uint8)

def set_px6(x, y, rgba):
    if 0 <= x < gw and 0 <= y < gh:
        grid6[y, x] = rgba

notches6 = [(85, 96), (168, 178), (242, 252), (310, 322)]
def in_notch6(x):
    return any(a <= x <= b for a, b in notches6)
def notch_edge6(x):
    return any(x == a - 1 or x == b + 1 for a, b in notches6)

for y in range(7, 58):
    if y <= 47:
        t = (y - 7) / 40.0
        inset = int(round(9 * (1.0 - t)))
        left = 10 + inset
        right = (gw - 11) - inset
    else:
        dy = y - 47
        left = 10 + int(round(dy * 1.4))
        right = (gw - 11) - int(round(dy * 1.4))

    for x in range(left, right + 1):
        if y >= 56 and (70 <= x <= 230 or x < 42 or x > 342):
            continue
        if y >= 54 and (92 <= x <= 210 or x < 30 or x > 354):
            continue
        if y == 57 and (231 <= x <= 275):
            continue

        top_y = 9 if in_notch6(x) else 7
        if y < top_y:
            continue

        is_left_border = (x == left)
        is_right_border = (x == right)
        is_bottom_border = (
            y == 57
            or (y == 55 and (70 <= x <= 230 or x < 42 or x > 342))
            or (y == 53 and (92 <= x <= 210 or x < 30 or x > 354))
            or (y == 56 and (231 <= x <= 275))
        )

        if is_left_border or is_right_border or is_bottom_border or y == top_y:
            set_px6(x, y, (26, 8, 3, 255))
            continue

        if y == top_y + 1 or y == top_y + 2:
            set_px6(x, y, (242, 232, 96, 255) if y == top_y + 1 else (196, 182, 68, 255))
            continue

        if y < 35 and (x in (left + 1, left + 2, right - 1, right - 2)):
            fade = max(0.0, 1.0 - (y - 9) / 26.0)
            r = int(230 * fade + 158 * (1 - fade))
            g = int(214 * fade + 66 * (1 - fade))
            b = int(86 * fade + 36 * (1 - fade))
            set_px6(x, y, (r, g, b, 255))
            continue

        if y == top_y + 3 or (y in (9, 10, 11) and notch_edge6(x)):
            set_px6(x, y, (28, 6, 2, 255))
            continue

        if y <= 47:
            fy = (y - 11) / 36.0
            if fy < 0.52:
                t2 = fy / 0.52
                r = int(194 * (1 - t2) + 170 * t2)
                g = int(96 * (1 - t2) + 72 * t2)
                b = int(50 * (1 - t2) + 38 * t2)
            else:
                t2 = (fy - 0.52) / 0.48
                r = int(170 * (1 - t2) + 110 * t2)
                g = int(72 * (1 - t2) + 39 * t2)
                b = int(38 * (1 - t2) + 31 * t2)
            set_px6(x, y, (r, g, b, 255))
        else:
            if y == 48:
                set_px6(x, y, (72, 20, 14, 255))
            else:
                fy2 = (y - 49) / 8.0
                r = int(52 * (1 - fy2) + 30 * fy2)
                g = int(12 * (1 - fy2) + 6 * fy2)
                b = int(5 * (1 - fy2) + 2 * fy2)
                set_px6(x, y, (r, g, b, 255))

brick_H6 = [
    (14, 24, 82), (15, 130, 220), (14, 260, 350),
    (41, 20, 110), (42, 135, 245), (41, 265, 360),
    (45, 45, 175), (45, 205, 335),
]
for by, x1, x2 in brick_H6:
    for x in range(x1, x2 + 1):
        if grid6[by, x, 3] > 0 and by <= 47:
            grid6[by, x] = (88, 30, 22, 255)
            if by + 1 <= 47 and grid6[by + 1, x, 3] > 0:
                c = grid6[by + 1, x]
                grid6[by + 1, x] = (min(255, int(c[0] * 1.15)), min(255, int(c[1] * 1.15)), min(255, int(c[2] * 1.15)), 255)

for bx, y1, y2 in [(52, 11, 18), (112, 12, 18), (165, 11, 18), (235, 11, 18), (305, 11, 18), (68, 38, 47), (125, 39, 47), (188, 39, 47), (255, 38, 47), (315, 39, 47)]:
    for y in range(y1, y2 + 1):
        if grid6[y, bx, 3] > 0 and y <= 47:
            grid6[y, bx] = (84, 28, 20, 255)

sparks6 = [
    (22, 5, 2), (48, 2, 1), (92, 1, 2), (132, 4, 2), (175, 2, 2), (225, 3, 2), (285, 4, 2), (332, 2, 1), (368, 9, 2),
    (32, 50, 2), (102, 58, 1), (185, 56, 2), (275, 59, 1), (358, 50, 2),
]
for sx, sy, sz in sparks6:
    if sz == 1:
        set_px6(sx, sy, (225, 110, 24, 235))
    else:
        for dy in range(2):
            for dx in range(2):
                set_px6(sx + dx, sy + dy, (240, 128, 28, 255) if (dx == 0 and dy == 0) else (175, 82, 22, 215))

plate_6x1 = Image.fromarray(grid6).resize((W6, H6), Image.Resampling.NEAREST)

logo_w6 = 1220
logo_h6 = 122  # Wait: keep natural bold height inside the 256px tall plate (118px)
logo_for_p6 = logo_clean.resize((logo_w6, logo_h6), Image.Resampling.LANCZOS)
lx6 = (W6 - logo_w6) // 2
ly6 = 52

alpha_m6 = logo_for_p6.split()[3]
shadow_6 = Image.new("RGBA", (W6, H6), (0, 0, 0, 0))
dark_sil6 = Image.new("RGBA", (logo_w6, logo_h6), (24, 5, 2, 255))
for sdx in [-4, 0, 4]:
    for sdy in [-3, 0, 3, 6, 9]:
        shadow_6.paste(dark_sil6, (lx6 + sdx, ly6 + sdy), alpha_m6)

combined_6x1_placa = Image.alpha_composite(plate_6x1, shadow_6)
combined_6x1_placa.paste(logo_for_p6, (lx6, ly6), logo_for_p6)

combined_6x1_placa.save(os.path.join(out_dir, "thunder_6x1_placa_full.png"))
for i in range(6):
    tile = combined_6x1_placa.crop((i * 256, 0, (i + 1) * 256, 256))
    tile.save(os.path.join(out_dir, f"thunder_6x1_placa_{i+1}.png"))


# ==============================================================================
# MODALIDAD 2: 6 EMOJIS EN BLOQUE 3x2 (3 arriba + 3 abajo -> 768 x 512 px)
# Ideal si quieres poner 3 emojis en la línea 1 y 3 emojis en la línea 2
# ==============================================================================
W32, H32 = 768, 512

# 2A. Logo con Placa en 3x2 (768 x 512)
# Escalado para centrarse en la unión de las dos filas (y = 256)
placa_base = Image.open(r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\emojis_thunder\thunder_placa_full.png").convert("RGBA")
# En 768x512 podemos darle más altura (340px de alto) para que luzca imponente en las 2 filas
placa_3x2_scaled = placa_base.resize((768, 340), Image.Resampling.NEAREST)
canvas_3x2_placa = Image.new("RGBA", (W32, H32), (0, 0, 0, 0))
canvas_3x2_placa.paste(placa_3x2_scaled, (0, (H32 - 340) // 2), placa_3x2_scaled)

canvas_3x2_placa.save(os.path.join(out_dir, "thunder_3x2_placa_full.png"))
idx = 1
for row in range(2):
    for col in range(3):
        tile = canvas_3x2_placa.crop((col * 256, row * 256, (col + 1) * 256, (row + 1) * 256))
        tile.save(os.path.join(out_dir, f"thunder_3x2_placa_{idx}.png"))
        idx += 1

# 2B. Logo Limpio en 3x2 (768 x 512)
canvas_3x2_limpio = Image.new("RGBA", (W32, H32), (0, 0, 0, 0))
logo_3x2_scaled = logo_clean.resize((756, 240), Image.Resampling.LANCZOS)
canvas_3x2_limpio.paste(logo_3x2_scaled, ((W32 - 756) // 2, (H32 - 240) // 2), logo_3x2_scaled)

canvas_3x2_limpio.save(os.path.join(out_dir, "thunder_3x2_limpio_full.png"))
idx = 1
for row in range(2):
    for col in range(3):
        tile = canvas_3x2_limpio.crop((col * 256, row * 256, (col + 1) * 256, (row + 1) * 256))
        tile.save(os.path.join(out_dir, f"thunder_3x2_limpio_{idx}.png"))
        idx += 1


# ==============================================================================
# PREVIEW SHEET
# ==============================================================================
def alpha_paste(dst, src, pos):
    tmp = Image.new("RGBA", dst.size, (0, 0, 0, 0))
    tmp.paste(src, pos)
    return Image.alpha_composite(dst, tmp)

preview = Image.new("RGBA", (1600, 1080), (49, 51, 56, 255))

# 1. 6x1 Placa (1536 x 256)
preview = alpha_paste(preview, combined_6x1_placa, (32, 30))
# 2. 6x1 Limpio (1536 x 256)
preview = alpha_paste(preview, canvas_6x1_limpio, (32, 310))
# 3. 3x2 Placa (768 x 512) left bottom
preview = alpha_paste(preview, canvas_3x2_placa, (32, 560))
# 4. 3x2 Limpio (768 x 512) right bottom
preview = alpha_paste(preview, canvas_3x2_limpio, (810, 560))

draw = ImageDraw.Draw(preview)
# Draw cut lines for 6x1 (every 256px)
for i in range(1, 6):
    cx = 32 + i * 256
    for yd in range(30, 30 + 256, 8):
        draw.line([(cx, yd), (cx, yd + 4)], fill=(255, 255, 255, 95), width=2)
    for yd in range(310, 310 + 256, 8):
        draw.line([(cx, yd), (cx, yd + 4)], fill=(255, 255, 255, 95), width=2)

# Draw cut lines for 3x2 (3 cols x 2 rows)
for base_x in [32, 810]:
    for i in range(1, 3):
        cx = base_x + i * 256
        for yd in range(580, 560 + 490, 8):
            draw.line([(cx, yd), (cx, yd + 4)], fill=(255, 255, 255, 95), width=2)
    for xd in range(base_x, base_x + 768, 8):
        draw.line([(xd, 560 + 256), (xd + 4, 560 + 256)], fill=(255, 200, 80, 110), width=2)

preview.save(os.path.join(out_dir, "preview_6_partes.png"))
print("Generated all 6-part emoji sets successfully!")
