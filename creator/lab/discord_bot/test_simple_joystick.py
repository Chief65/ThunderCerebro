import os
from PIL import Image, ImageDraw

script_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\lab\discord_bot"
icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"

SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

# Diseño simplificado y limpio del joystick:
# - Bola superior redonda, grande y limpia (sin cortes de brillo recargados)
# - Barra / eje vertical robusto
# - Fuelle cónico sutil
# - Base redondeada limpia y estilizada (sin botones pequeños que ensucien la silueta)
def draw_simple_joystick(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base inferior sólida con esquinas redondeadas
    # x entre 116 y 396 (ancho 280 en 512px -> ~140px en 256px, muy equilibrado)
    draw.rounded_rectangle((116, 360, 396, 444), radius=38, fill=color)

    # 2. Cono / fuelle de soporte de la palanca
    collar_pts = [(188, 360), (324, 360), (292, 290), (220, 290)]
    draw.polygon(collar_pts, fill=color)

    # 3. Eje / palanca vertical robusta
    draw.rounded_rectangle((232, 160, 280, 300), radius=18, fill=color)

    # 4. Bola superior grande, limpia y centrada en (256, 134)
    bx, by, br = 256, 134, 76
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    # 5. Detalle minimalista: un único botón redondo limpio en la base a la derecha
    # y una pequeña ranura o indicador limpio a la izquierda
    draw.ellipse((326, 384, 362, 420), fill=trans)
    draw.rounded_rectangle((150, 394, 210, 410), radius=8, fill=trans)

    return img

test = draw_simple_joystick(YELLOW, TRANSPARENT_YELLOW)
test.resize((256, 256), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "test_simple_joystick.png"))
print("Generated test simple joystick!")
