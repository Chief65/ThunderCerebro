import os
import math
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)

# OPCIÓN A: Arcade Clásico Proporcional (Sturdy stick, bola grande, base proporcionada)
def draw_normal_arcade(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base arcade sólida (x=100..412, y=310..430)
    draw.rounded_rectangle((100, 310, 412, 430), radius=32, fill=color)

    # Dos botones arcade redondos a la derecha
    draw.ellipse((310, 344, 350, 384), fill=trans)
    draw.ellipse((358, 344, 398, 384), fill=trans)

    # Fuelle de goma escalonado en el centro (ancho 120, alto 48)
    draw.rounded_rectangle((196, 296, 316, 326), radius=12, fill=color)
    draw.line([(200, 312), (312, 312)], fill=trans, width=6)
    draw.rounded_rectangle((216, 270, 296, 298), radius=10, fill=color)
    draw.line([(220, 284), (292, 284)], fill=trans, width=6)

    # 2. Varilla / eje vertical robusto (ancho 44px, alto 120px) - NO largo y fino
    draw.rounded_rectangle((234, 150, 278, 272), radius=16, fill=color)

    # 3. Bola superior grande (radio 86px -> diámetro 172px, centrada en X=256, Y=126)
    bx, by, br = 256, 126, 86
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

# OPCIÓN B: Estilo Emoji 🕹️ (Palanca inclinada dinámica, base 3D limpia)
def draw_emoji_joystick(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base trapezoidal limpia en 3D
    # Cara superior de la base
    top_base = [(110, 340), (402, 340), (370, 390), (142, 390)]
    draw.polygon(top_base, fill=color)
    # Cara frontal de la base
    draw.rounded_rectangle((90, 380, 422, 436), radius=22, fill=color)
    draw.line([(96, 386), (416, 386)], fill=trans, width=10)

    # Botón rojo clásico en la base
    draw.ellipse((330, 348, 370, 382), fill=trans)

    # Fuelle circular en la base
    draw.ellipse((200, 344, 280, 384), fill=color)

    # Palanca inclinada hacia la derecha a ~15 grados
    # Centro base: (240, 350) -> Centro bola: (286, 136)
    draw.line([(240, 350), (286, 136)], fill=color, width=42)
    # Redondear extremos del trazo
    r = 21
    draw.ellipse((240-r, 350-r, 240+r, 350+r), fill=color)
    draw.ellipse((286-r, 136-r, 286+r, 136+r), fill=color)

    # Bola superior
    bx, by, br = 286, 136, 84
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

# OPCIÓN C: Minimalista Clásico "Gamer" (Base suave, palanca perfectamente centrada y proporcionada)
def draw_clean_classic(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base ovalada/redondeada compacta y sólida (tipo stand)
    draw.rounded_rectangle((112, 330, 400, 430), radius=48, fill=color)

    # 1 botón circular a la izquierda, 1 botón a la derecha
    draw.ellipse((146, 362, 186, 402), fill=trans)
    draw.ellipse((326, 362, 366, 402), fill=trans)

    # Fuelle cónico suave
    collar = [(202, 332), (310, 332), (284, 260), (228, 260)]
    draw.polygon(collar, fill=color)

    # Eje vertical corto y grueso
    draw.rounded_rectangle((234, 150, 278, 268), radius=16, fill=color)

    # Bola superior grande perfectamente proporcionada
    bx, by, br = 256, 128, 88
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

draw_normal_arcade(YELLOW, TRANSPARENT_YELLOW).resize((256, 256)).save(os.path.join(icons_dir, "test_normal_a.png"))
draw_emoji_joystick(YELLOW, TRANSPARENT_YELLOW).resize((256, 256)).save(os.path.join(icons_dir, "test_normal_b.png"))
draw_clean_classic(YELLOW, TRANSPARENT_YELLOW).resize((256, 256)).save(os.path.join(icons_dir, "test_normal_c.png"))
print("Generated Normal A, B, C!")
