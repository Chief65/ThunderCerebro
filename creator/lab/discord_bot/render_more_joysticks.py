import os
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons\joystick_tests"
SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)

# CONCEPTO 5: ARCADE SANWA PROPORCIONADO (Heavyweight Arcade Stick)
# Proporciones estándar: palanca corta y sólida, bola grande, base de recreativa con 2 botones
def draw_arcade_sanwa(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base robusta de recreativa (ancho 330px, alto 130px)
    # x=91..421, y=294..424
    draw.rounded_rectangle((91, 294, 421, 424), radius=30, fill=color)

    # Bisel horizontal que da perspectiva al panel de control
    draw.line([(99, 376), (413, 376)], fill=trans, width=8)

    # 2 botones de acción arcade circulares a la derecha
    draw.ellipse((314, 322, 354, 362), fill=trans)
    draw.ellipse((364, 322, 404, 362), fill=trans)

    # Fuelle de goma escalonado en la base de la palanca (2 capas concéntricas)
    draw.rounded_rectangle((188, 280, 324, 312), radius=12, fill=color)
    draw.line([(194, 298), (318, 298)], fill=trans, width=6)

    # 2. Varilla metálica CORTA y ROBUSTA (ancho 44px, alto 86px: de y=170 a y=256)
    # ¡Al ser corta, la proporción es 100% natural de máquina recreativa!
    draw.rounded_rectangle((234, 168, 278, 284), radius=16, fill=color)

    # 3. Bola esférica grande perfectamente redonda (diámetro 180px, centrada en (256, 126))
    bx, by, br = 256, 126, 90
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

# CONCEPTO 6: ATARI CLEAN FLAT (Inspirado en el icono de joystick oficial de Google Fonts / Material Design)
def draw_material_joystick(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base trapezoidal suave
    base = [(120, 310), (392, 310), (426, 420), (86, 420)]
    draw.polygon(base, fill=color)
    for p in base:
        draw.ellipse((p[0]-24, p[1]-24, p[0]+24, p[1]+24), fill=color)

    # Ranura decorativa o botón frontal
    draw.rounded_rectangle((130, 386, 210, 406), radius=8, fill=trans)
    draw.ellipse((340, 356, 380, 396), fill=trans)

    # Collar cónico en la base
    collar = [(200, 310), (312, 310), (280, 240), (232, 240)]
    draw.polygon(collar, fill=color)

    # Palanca corta y fuerte
    draw.rounded_rectangle((234, 150, 278, 250), radius=14, fill=color)

    # Bola superior
    bx, by, br = 256, 116, 88
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

c5 = draw_arcade_sanwa(YELLOW, TRANSPARENT_YELLOW)
c6 = draw_material_joystick(YELLOW, TRANSPARENT_YELLOW)

c5.resize((256, 256)).save(os.path.join(icons_dir, "opt5_arcade_sanwa.png"))
c6.resize((256, 256)).save(os.path.join(icons_dir, "opt6_material_joystick.png"))

sheet2 = Image.new("RGBA", (580, 300), (49, 51, 56, 255))
sheet2.paste(c5.resize((240, 240)), (30, 30), c5.resize((240, 240)))
sheet2.paste(c6.resize((240, 240)), (310, 30), c6.resize((240, 240)))

draw_s2 = ImageDraw.Draw(sheet2)
draw_s2.text((36, 36), "5. ARCADE SANWA (RECOMENDADO)", fill=(255, 255, 255, 220))
draw_s2.text((316, 36), "6. MATERIAL FLAT", fill=(255, 255, 255, 220))

sheet2.save(os.path.join(icons_dir, "comparativa_nuevos.png"))
print("Generated concepts 5 and 6!")
