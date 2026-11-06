import os
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

# JOYSTICK ARCADE PROFESIONAL Y NORMAL
# Geometría clásica de máquina arcade: base rectangular sólida, fuelle de goma escalonado,
# eje recto metálico, bola superior esférica, y botones arcade redondos.
def draw_normal_arcade_joystick(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base arcade sólida (panel de control de recreativa)
    # Dimensiones: ancho 320px (x=96..416), alto 124px (y=320..444)
    # Proporción perfecta con esquinas redondeadas normales (radio 24)
    draw.rounded_rectangle((96, 320, 416, 444), radius=24, fill=color)

    # Bisel / línea horizontal limpia que separa la superficie de los botones de la cara frontal
    draw.line([(102, 396), (410, 396)], fill=trans, width=10)

    # 3 botones arcade circulares en la superficie superior derecha (alineados con estilo arcade clásico)
    # Botón 1, 2 y 3
    draw.ellipse((296, 342, 332, 378), fill=trans)
    draw.ellipse((338, 334, 374, 370), fill=trans)
    draw.ellipse((380, 342, 416, 378), fill=trans)

    # 2. Fuelle de goma circular en la base de la palanca (2 anillos concéntricos)
    # Anillo inferior
    draw.ellipse((192, 302, 320, 342), fill=color)
    draw.line([(198, 324), (314, 324)], fill=trans, width=6)
    # Anillo superior
    draw.ellipse((214, 276, 298, 312), fill=color)
    draw.line([(220, 294), (292, 294)], fill=trans, width=6)

    # 3. Eje / palanca vertical metálica recta (ancho 40px, alto 140px)
    draw.rounded_rectangle((236, 142, 276, 282), radius=14, fill=color)

    # 4. Bola de control grande perfectamente redonda (radio 86px -> diámetro 172px)
    bx, by, br = 256, 120, 86
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

test = draw_normal_arcade_joystick(YELLOW, TRANSPARENT_YELLOW)
test.resize((256, 256)).save(os.path.join(icons_dir, "test_normal_arcade_final.png"))
print("Saved normal arcade final!")
