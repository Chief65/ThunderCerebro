from PIL import Image, ImageDraw

SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)
WHITE = (255, 255, 255, 255)
TRANSPARENT_WHITE = (255, 255, 255, 0)

def draw_minecraft_grass_block(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Coordenadas isométricas precisas
    # Cara superior (rombo)
    top_face = [(256, 76), (426, 174), (256, 272), (86, 174)]
    draw.polygon(top_face, fill=color)

    # Cara izquierda (polígono)
    left_face = [(86, 174), (256, 272), (256, 436), (86, 338)]
    draw.polygon(left_face, fill=color)

    # Cara derecha (polígono)
    right_face = [(256, 272), (426, 174), (426, 338), (256, 436)]
    draw.polygon(right_face, fill=color)

    # Separación limpia de aristas en transparente (14px)
    draw.line([(256, 76), (256, 272)], fill=trans, width=14)
    draw.line([(86, 174), (256, 272)], fill=trans, width=14)
    draw.line([(426, 174), (256, 272)], fill=trans, width=14)
    draw.line([(256, 272), (256, 436)], fill=trans, width=14)

    # Capa de hierba escalonada (Minecraft Grass Drip) en las caras laterales
    # Cara izquierda: franja de corte escalonada separando césped de tierra
    # Puntos de césped colgante:
    draw.polygon([(114, 258), (146, 276), (146, 306), (114, 288)], fill=trans)
    draw.polygon([(168, 288), (200, 306), (200, 336), (168, 318)], fill=trans)
    draw.polygon([(220, 318), (248, 334), (248, 364), (220, 348)], fill=trans)

    # Cara derecha: franja de césped colgante simétrica
    draw.polygon([(264, 334), (292, 318), (292, 348), (264, 364)], fill=trans)
    draw.polygon([(312, 306), (344, 288), (344, 318), (312, 336)], fill=trans)
    draw.polygon([(366, 276), (398, 258), (398, 288), (366, 306)], fill=trans)

    # Partículas/bloquecitos de tierra en la zona inferior
    # Cara izquierda
    draw.polygon([(136, 330), (164, 346), (164, 370), (136, 354)], fill=trans)
    # Cara derecha
    draw.polygon([(348, 346), (376, 330), (376, 354), (348, 370)], fill=trans)

    # Textura sutil en la cara superior (2 cuadrados recortados)
    draw.polygon([(236, 142), (256, 130), (276, 142), (256, 154)], fill=trans)
    draw.polygon([(176, 196), (196, 184), (216, 196), (196, 208)], fill=trans)
    draw.polygon([(296, 216), (316, 204), (336, 216), (316, 228)], fill=trans)

    return img

test = draw_minecraft_grass_block(YELLOW, TRANSPARENT_YELLOW)
test.resize((256, 256), Image.Resampling.LANCZOS).save(r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons\test_grass_block.png")
print("Saved test grass block!")
