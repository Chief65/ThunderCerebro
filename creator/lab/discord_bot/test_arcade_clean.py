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
    # Altura y anchura robustas y perfectamente centradas
    draw.rounded_rectangle((92, 316, 420, 432), radius=34, fill=color)

    # 2 botones de acción redondos en la base arcade a la derecha
    draw.ellipse((304, 350, 348, 394), fill=trans)
    draw.ellipse((358, 350, 402, 394), fill=trans)

    # 2. Cono / fuelle de goma en la base de la palanca
    collar_pts = [(198, 316), (314, 316), (288, 256), (224, 256)]
    draw.polygon(collar_pts, fill=color)

    # Ranura sutil separando el cono de la base
    draw.line([(206, 316), (306, 316)], fill=trans, width=6)

    # 3. Varilla / eje vertical de la palanca
    draw.rounded_rectangle((236, 144, 276, 260), radius=14, fill=color)

    # 4. Bola de control grande y perfectamente circular arriba
    bx, by, br = 256, 122, 84
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

test = draw_arcade_stick_clean(YELLOW, TRANSPARENT_YELLOW)
test.resize((256, 256)).save(os.path.join(icons_dir, "test_arcade_clean.png"))
print("Saved test arcade clean!")
