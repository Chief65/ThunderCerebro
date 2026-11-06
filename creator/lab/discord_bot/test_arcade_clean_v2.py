import os
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

def draw_arcade_stick_clean(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base rectangular sólida de consola arcade con esquinas redondeadas
    # x=96..416 (ancho 320), y=316..432 (alto 116)
    draw.rounded_rectangle((96, 316, 416, 432), radius=28, fill=color)

    # Bisel / línea horizontal de separación de perspectiva
    draw.line([(104, 394), (408, 394)], fill=trans, width=8)

    # 2 botones de acción redondos en la superficie arcade a la derecha (cómodamente dentro)
    draw.ellipse((312, 342, 348, 378), fill=trans)
    draw.ellipse((360, 342, 396, 378), fill=trans)

    # 2. Cono / fuelle de soporte de la palanca (trapezoide sólido limpio)
    collar_pts = [(196, 316), (316, 316), (284, 256), (228, 256)]
    draw.polygon(collar_pts, fill=color)
    draw.line([(206, 316), (306, 316)], fill=trans, width=6)

    # 3. Varilla / eje vertical de la palanca (ancho 42px, alto 124px)
    draw.rounded_rectangle((235, 142, 277, 266), radius=14, fill=color)

    # 4. Bola superior esférica grande perfectamente centrada en (256, 120)
    bx, by, br = 256, 120, 84
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

test = draw_arcade_stick_clean(YELLOW, TRANSPARENT_YELLOW)
test.resize((256, 256)).save(os.path.join(icons_dir, "test_arcade_clean_v2.png"))
print("Saved test arcade clean v2!")
