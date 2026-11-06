import os
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons"
SIZE = 512
YELLOW = (255, 200, 0, 255)  # #FFC800 Amarillo-anaranjado oficial
TRANSPARENT_YELLOW = (255, 200, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

# Diseño 1: Cubo Isométrico de Minecraft (Grass Block icónico de Minecraft)
def draw_minecraft_cube(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Coordenadas isométricas 3D centradas en (256, 256)
    # Cara superior (rombo)
    top_face = [(256, 80), (416, 172), (256, 264), (96, 172)]
    draw.polygon(top_face, fill=color)

    # Cara izquierda
    left_face = [(96, 172), (256, 264), (256, 432), (96, 340)]
    draw.polygon(left_face, fill=color)

    # Cara derecha
    right_face = [(256, 264), (416, 172), (416, 340), (256, 432)]
    draw.polygon(right_face, fill=color)

    # Líneas de aristas en recorte transparente para separar las 3 caras del cubo limpiamente
    draw.line([(256, 80), (256, 264)], fill=trans, width=16)
    draw.line([(96, 172), (256, 264)], fill=trans, width=16)
    draw.line([(416, 172), (256, 264)], fill=trans, width=16)
    draw.line([(256, 264), (256, 432)], fill=trans, width=16)

    # Franja escalonada de césped (estilo Minecraft) en ambas caras laterales
    # Capa de césped izquierda (recortes decorativos de tierra/bloque)
    draw.polygon([(136, 250), (176, 250), (176, 280), (136, 280)], fill=trans)
    draw.polygon([(186, 310), (226, 310), (226, 340), (186, 340)], fill=trans)

    # Capa de césped derecha
    draw.polygon([(286, 310), (326, 310), (326, 340), (286, 340)], fill=trans)
    draw.polygon([(336, 250), (376, 250), (376, 280), (336, 280)], fill=trans)

    # Esquinas redondeadas sutiles en los 6 vértices exteriores
    return img

# Diseño 2: Espada de Minecraft (Minecraft Sword en diagonal a 45°)
def draw_minecraft_sword(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Hoja de la espada en diagonal limpia (de esquina inferior izquierda a superior derecha)
    # Punta afilada en (392, 120)
    blade_pts = [(392, 120), (412, 140), (260, 292), (220, 252)]
    draw.polygon(blade_pts, fill=color)
    draw.line([(392, 120), (412, 140)], fill=color, width=24)

    # Guardia / cruceta protectora transversal
    guard_pts = [(180, 260), (230, 210), (300, 280), (250, 330)]
    draw.polygon(guard_pts, fill=color)

    # Empuñadura / mango
    hilt_pts = [(186, 324), (214, 296), (154, 356), (126, 384)]
    draw.polygon(hilt_pts, fill=color)
    draw.line([(190, 316), (130, 376)], fill=color, width=32)

    # Pomo inferior de la espada
    draw.rounded_rectangle((94, 386, 154, 446), radius=16, fill=color)

    # Ranura central en la hoja (canal de sangre / filo)
    draw.line([(244, 268), (380, 132)], fill=trans, width=14)

    # Recortes en la guarda para detalle
    draw.ellipse((220, 260, 250, 290), fill=trans)

    return img

img_cube = draw_minecraft_cube(YELLOW, TRANSPARENT_YELLOW)
img_sword = draw_minecraft_sword(YELLOW, TRANSPARENT_YELLOW)

img_cube.resize((256, 256), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "test_cube_jugar.png"))
img_sword.resize((256, 256), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, "test_sword_jugar.png"))
print("Generated test cube and sword!")
