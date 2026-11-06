import os
import math
from PIL import Image, ImageDraw

out_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)
SIZE = 512
FINAL_SINGLE = 128

def clean_rgba(img, target_size=FINAL_SINGLE):
    resized = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
    alpha = resized.split()[3]
    clean = Image.new("RGBA", (target_size, target_size), TRANSPARENT_WHITE)
    solid = Image.new("RGBA", (target_size, target_size), WHITE)
    clean.paste(solid, mask=alpha)
    # 4 esquinas ancladas
    px = clean.load()
    w, h = clean.size
    for x, y in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        if px[x, y][3] == 0:
            px[x, y] = (255, 255, 255, 1)
    return clean

# Espadas cruzadas simétricas perfectas (Minecraft Style)
def make_swords():
    # Creamos una sola espada vertical centrada y luego la rotamos +45 y -45 grados
    blade = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(blade)
    cx = 256
    # Hoja
    d.polygon([(cx, 50), (cx + 26, 85), (cx + 26, 330), (cx - 26, 330), (cx - 26, 85)], fill=WHITE)
    # Guarda horizontal
    d.rounded_rectangle((cx - 65, 330, cx + 65, 362), radius=10, fill=WHITE)
    # Empuñadura
    d.rounded_rectangle((cx - 15, 362, cx + 15, 435), radius=6, fill=WHITE)
    # Pomo
    d.ellipse((cx - 28, 425, cx + 28, 475), fill=WHITE)

    # Rotamos ambas espadas 45 grados en sentidos opuestos
    s1 = blade.rotate(45, resample=Image.Resampling.BICUBIC)
    s2 = blade.rotate(-45, resample=Image.Resampling.BICUBIC)

    combined = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    combined.alpha_composite(s1)
    combined.alpha_composite(s2)

    res = clean_rgba(combined)
    path = os.path.join(out_dir, "icon_reglas_gen_w.png")
    res.save(path, "PNG")
    print(f"Saved {path}")
    return path

# Logo de Discord canónico estilizado
def make_discord_logo():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Silueta poligonal suave del mando/cabeza de Discord
    pts = [
        (130, 150), (200, 110), (256, 130), (312, 110), (382, 150),
        (430, 290), (370, 395), (320, 360), (288, 385), (256, 390), (224, 385), (192, 360), (142, 395),
        (82, 290)
    ]
    d.polygon(pts, fill=WHITE)
    # Redondeado exterior
    r = 24
    for x, y in pts:
        d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE)
    for i in range(len(pts)):
        d.line([pts[i], pts[(i + 1) % len(pts)]], fill=WHITE, width=r * 2)

    # Arqueo superior
    d.ellipse((200, 50, 312, 140), fill=(0, 0, 0, 0))
    # Recorte inferior entre patitas
    d.polygon([(200, 420), (256, 350), (312, 420)], fill=(0, 0, 0, 0))
    d.ellipse((215, 335, 297, 395), fill=(0, 0, 0, 0))

    # Ojos ovalados
    d.ellipse((165, 215, 215, 280), fill=(0, 0, 0, 0))
    d.ellipse((297, 215, 347, 280), fill=(0, 0, 0, 0))

    res = clean_rgba(img)
    path = os.path.join(out_dir, "icon_reglas_dc_w.png")
    res.save(path, "PNG")
    print(f"Saved {path}")
    return path

make_swords()
make_discord_logo()
