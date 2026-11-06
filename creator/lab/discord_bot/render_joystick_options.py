import os
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
os.makedirs(icons_dir, exist_ok=True)

SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)

# DISEÑO 1: Joystick Arcade Clásico Estándar (Estilo 🕹️ estándar)
# Proporciones equilibradas, palanca recta, base de consola con 2 botones redondos clásicos
def draw_joystick_classic_v1(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base rectangular limpia con esquinas redondeadas (tipo panel arcade)
    # x=96..416 (ancho 320), y=330..440 (alto 110)
    draw.rounded_rectangle((96, 330, 416, 440), radius=28, fill=color)

    # Bisel frontal inferior de la base (línea transparente que separa la superficie del frontal)
    draw.line([(100, 396), (412, 396)], fill=trans, width=12)

    # 2 Botones circulares arcade a la derecha en la superficie
    draw.ellipse((320, 346, 356, 382), fill=trans)
    draw.ellipse((368, 346, 404, 382), fill=trans)

    # Fuelle de goma circular en la base de la palanca (anillo cónico)
    draw.ellipse((208, 310, 304, 350), fill=color)
    draw.line([(220, 330), (292, 330)], fill=trans, width=8)

    # 2. Eje vertical metálico / palanca recta
    draw.rounded_rectangle((238, 140, 274, 320), radius=14, fill=color)

    # 3. Bola superior grande perfectamente esférica
    bx, by, br = 256, 116, 76
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

# DISEÑO 2: Joystick Ultra-Minimalista Simétrico
# Silueta súper limpia, perfecta para iconos de interfaz (sin detalles asimétricos)
def draw_joystick_minimal_v2(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # 1. Base trapezoidal / consola limpia
    base_pts = [(120, 340), (392, 340), (428, 440), (84, 440)]
    draw.polygon(base_pts, fill=color)
    # Esquinas redondeadas
    for p in base_pts:
        draw.ellipse((p[0]-16, p[1]-16, p[0]+16, p[1]+16), fill=color)

    # Dos botones simétricos a ambos lados
    draw.ellipse((140, 374, 184, 418), fill=trans)
    draw.ellipse((328, 374, 372, 418), fill=trans)

    # 2. Fuelle cónico en el centro
    collar = [(212, 340), (300, 340), (280, 280), (232, 280)]
    draw.polygon(collar, fill=color)

    # 3. Eje vertical robusto
    draw.rounded_rectangle((238, 140, 274, 290), radius=16, fill=color)

    # 4. Bola superior
    bx, by, br = 256, 116, 76
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

# DISEÑO 3: Joystick Tipo Atari / Retro Clásico Sólido
# La silueta más normal y universalmente reconocida en diseño gráfico
def draw_joystick_retro_v3(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base sólida rectangular con esquinas suaves
    draw.rounded_rectangle((104, 310, 408, 440), radius=36, fill=color)

    # Un botón grande a la izquierda o centro-derecha
    draw.ellipse((330, 344, 384, 398), fill=trans)

    # Cono escalonado en la base de la palanca (2 escalones)
    draw.rounded_rectangle((196, 290, 316, 320), radius=10, fill=color)
    draw.line([(198, 316), (314, 316)], fill=trans, width=8)

    draw.rounded_rectangle((216, 260, 296, 292), radius=10, fill=color)
    draw.line([(218, 288), (294, 288)], fill=trans, width=8)

    # Eje cilíndrico
    draw.rounded_rectangle((238, 136, 274, 266), radius=14, fill=color)

    # Bola superior
    bx, by, br = 256, 114, 78
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

draw_joystick_classic_v1(YELLOW, TRANSPARENT_YELLOW).resize((256, 256)).save(os.path.join(icons_dir, "test_joy_v1.png"))
draw_joystick_minimal_v2(YELLOW, TRANSPARENT_YELLOW).resize((256, 256)).save(os.path.join(icons_dir, "test_joy_v2.png"))
draw_joystick_retro_v3(YELLOW, TRANSPARENT_YELLOW).resize((256, 256)).save(os.path.join(icons_dir, "test_joy_v3.png"))
print("Generated v1, v2, v3 test joysticks!")
