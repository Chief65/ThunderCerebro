import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_erosion, binary_fill_holes

out_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\emojis_thunder"
os.makedirs(out_dir, exist_ok=True)

# 1. Load clean THUNDER logo, remove stray x=0 pixels, and decontaminate ONLY outer perimeter
raw_logo = Image.open(r"C:\Users\PC\Desktop\ThunderCerebro\raw\assets\thunder_full_logo.png").convert("RGBA")
arr = np.array(raw_logo)
arr[:, :7, :] = 0  # clear the 2 stray pixels at x=0
clean_bbox = Image.fromarray(arr).getbbox()  # (9, 24, 500, 131)
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
                    logo_crop[y, x, :3] = [62, 11, 4]   # dark maroon outline of N
                else:
                    logo_crop[y, x, :3] = [10, 18, 34]  # dark navy outline of THU / DER
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

# 2. Build pure Minecraft Nametag IP box:
# Pure black (0, 0, 0) with lowered opacity (alpha = 155, ~61% opacity, zero yellow!)
# And pure white (255, 255, 255) pixel-art text "thundermc.es" with zero yellow/brown fringe!
ref_ip_img = Image.open(
    r"C:\Users\PC\.gemini\antigravity-cli\brain\1815398b-7a02-4d40-82dc-73531c9ec3ae\.user_uploaded\uploaded_media_1793950102462.png"
).convert("RGBA")
ref_ip_arr = np.array(ref_ip_img)

# Original IP box in reference is y=293..352 (59px tall), x=139..825 (686px wide)
ip_box_raw = ref_ip_arr[293:352, 139:825].copy()
box_alpha = 155  # 61% black opacity like Minecraft nametag

ip_nametag_arr = np.zeros_like(ip_box_raw)
for y in range(ip_box_raw.shape[0]):
    for x in range(ip_box_raw.shape[1]):
        r, g, b, _ = ip_box_raw[y, x]
        if b > 170:
            # Pure white crisp pixel of "thundermc.es" (100% opaque white, zero yellow)
            ip_nametag_arr[y, x] = [255, 255, 255, 255]
        elif b > 80:
            # Edge pixel of text: blend pure white (255,255,255) over pure black nametag (0,0,0, box_alpha)
            # No yellow/orange channel used at all!
            t_white = float(b - 30) / (239.0 - 30.0)
            t_white = max(0.0, min(1.0, t_white))
            # Composite white with alpha=t_white over black with alpha=(box_alpha/255)
            bg_a = box_alpha / 255.0
            out_a = t_white + bg_a * (1.0 - t_white)
            out_rgb = int(round((255.0 * t_white) / out_a))
            ip_nametag_arr[y, x] = [out_rgb, out_rgb, out_rgb, int(round(out_a * 255))]
        else:
            # Pure black nametag background with lowered opacity
            ip_nametag_arr[y, x] = [0, 0, 0, box_alpha]

ip_nametag_img = Image.fromarray(ip_nametag_arr)


W, H = 768, 256

# ==============================================================================
# 1. RECUADRO IP NAMETAG PARA EL LOGO LIMPIO (Ancho = 756 px, x = 6..762)
# ==============================================================================
target_w = 756
ip_h = int(round(ip_nametag_img.height * (target_w / ip_nametag_img.width)))  # 65 px
ip_resized_limpio = ip_nametag_img.resize((target_w, ip_h), Image.Resampling.NEAREST)

canvas_ip_limpio = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ox = (W - target_w) // 2  # x = 6
canvas_ip_limpio.paste(ip_resized_limpio, (ox, 8), ip_resized_limpio)

canvas_ip_limpio.save(os.path.join(out_dir, "ip_original_full.png"))
canvas_ip_limpio.save(os.path.join(out_dir, "ip_nametag_full.png"))
for i in range(3):
    tile = canvas_ip_limpio.crop((i * 256, 0, (i + 1) * 256, 256))
    tile.save(os.path.join(out_dir, f"ip_original_{i+1}.png"))
    tile.save(os.path.join(out_dir, f"ip_nametag_{i+1}.png"))

# Logo limpio alineado abajo para que quede a solo 4px del nametag de la fila 2
logo_h_clean = int(round(logo_clean.height * (target_w / logo_clean.width)))  # 164 px
logo_resized_clean = logo_clean.resize((target_w, logo_h_clean), Image.Resampling.LANCZOS)

canvas_clean_bottom = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas_clean_bottom.paste(logo_resized_clean, (ox, H - logo_h_clean - 4), logo_resized_clean)
canvas_clean_bottom.save(os.path.join(out_dir, "thunder_limpio_bajo_full.png"))
for i in range(3):
    tile = canvas_clean_bottom.crop((i * 256, 0, (i + 1) * 256, 256))
    tile.save(os.path.join(out_dir, f"thunder_limpio_bajo_{i+1}.png"))


# ==============================================================================
# 2. RECUADRO IP NAMETAG AJUSTADO AL ANCHO DE LA PLACA (Ancho = 688 px, x = 40..728)
# Mismo estilo Nametag negro semitransparente sin restos amarillos
# ==============================================================================
placa_w = 688
ip_h_placa = int(round(ip_nametag_img.height * (placa_w / ip_nametag_img.width)))  # 59 px
ip_resized_placa = ip_nametag_img.resize((placa_w, ip_h_placa), Image.Resampling.NEAREST)

canvas_ip_placa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ox_placa = (W - placa_w) // 2  # x = 40
canvas_ip_placa.paste(ip_resized_placa, (ox_placa, 8), ip_resized_placa)

canvas_ip_placa.save(os.path.join(out_dir, "ip_placa_full.png"))
for i in range(3):
    tile = canvas_ip_placa.crop((i * 256, 0, (i + 1) * 256, 256))
    tile.save(os.path.join(out_dir, f"ip_placa_{i+1}.png"))


# ==============================================================================
# 3. COMBO EN 1 FILA (LOGO + NAMETAG IP EN LOS MISMOS 3 EMOJIS)
# ==============================================================================
canvas_combo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
top_y_combo = (H - (logo_h_clean + 6 + ip_h)) // 2  # y = 10
canvas_combo.paste(logo_resized_clean, (ox, top_y_combo), logo_resized_clean)
canvas_combo.paste(ip_resized_limpio, (ox, top_y_combo + logo_h_clean + 6), ip_resized_limpio)

canvas_combo.save(os.path.join(out_dir, "thunder_combo_ip_full.png"))
for i in range(3):
    tile = canvas_combo.crop((i * 256, 0, (i + 1) * 256, 256))
    tile.save(os.path.join(out_dir, f"thunder_combo_ip_{i+1}.png"))


# ==============================================================================
# PREVIEW SHEET ON DISCORD DARK BACKGROUND (#313338) + LIGHTER TEST PATCH
# ==============================================================================
combined_plate = Image.open(os.path.join(out_dir, "thunder_placa_full.png")).convert("RGBA")

def alpha_paste(dst, src, pos):
    tmp = Image.new("RGBA", dst.size, (0, 0, 0, 0))
    tmp.paste(src, pos)
    return Image.alpha_composite(dst, tmp)

preview = Image.new("RGBA", (880, 920), (49, 51, 56, 255))

# Top bar: Real Discord Jumbo size (144x48 per row) comparison
p_placa_sm = combined_plate.resize((144, 48), Image.Resampling.LANCZOS)
p_ip_placa_sm = canvas_ip_placa.resize((144, 48), Image.Resampling.NEAREST)
preview = alpha_paste(preview, p_placa_sm, (60, 20))
preview = alpha_paste(preview, p_ip_placa_sm, (60, 68))

p_limpio_sm = canvas_clean_bottom.resize((144, 48), Image.Resampling.LANCZOS)
p_ip_orig_sm = canvas_ip_limpio.resize((144, 48), Image.Resampling.NEAREST)
preview = alpha_paste(preview, p_limpio_sm, (260, 20))
preview = alpha_paste(preview, p_ip_orig_sm, (260, 68))

p_combo_sm = canvas_combo.resize((144, 48), Image.Resampling.LANCZOS)
preview = alpha_paste(preview, p_combo_sm, (460, 28))

# Full size Stack 1: Logo Limpio (Row 1) + Nametag IP (Row 2)
y1 = 110
preview = alpha_paste(preview, canvas_clean_bottom, (56, y1))
preview = alpha_paste(preview, canvas_ip_limpio, (56, y1 + 256))

# Full size Stack 2: Logo Placa (Row 1) + Nametag IP (Row 2)
y2 = 490
preview = alpha_paste(preview, combined_plate, (56, y2))
preview = alpha_paste(preview, canvas_ip_placa, (56, y2 + 256))

draw = ImageDraw.Draw(preview)
for cut_x in [56 + 256, 56 + 512]:
    for yd in range(y1 + 80, y1 + 256 + 90, 8):
        draw.line([(cut_x, yd), (cut_x, yd + 4)], fill=(255, 255, 255, 95), width=1)
for xd in range(56, 56 + 768, 8):
    draw.line([(xd, y1 + 256), (xd + 4, y1 + 256)], fill=(255, 255, 255, 80), width=1)

for cut_x in [56 + 256, 56 + 512]:
    for yd in range(y2 + 30, y2 + 256 + 90, 8):
        draw.line([(cut_x, yd), (cut_x, yd + 4)], fill=(255, 255, 255, 95), width=1)
for xd in range(56, 56 + 768, 8):
    draw.line([(xd, y2 + 256), (xd + 4, y2 + 256)], fill=(255, 255, 255, 80), width=1)

preview.save(os.path.join(out_dir, "preview_con_ip.png"))
print("Generated pure black semi-transparent nametag IP sets successfully!")
