import os
import math
from PIL import Image, ImageDraw

icons_dir = r"C:\Users\PC\Desktop\ThunderCerebro\creator\output\renders\discord_icons\joystick_tests"
os.makedirs(icons_dir, exist_ok=True)

SIZE = 512
YELLOW = (255, 200, 0, 255)
TRANSPARENT_YELLOW = (255, 200, 0, 0)

# ==============================================================================
# CONCEPTO 1: DYNAMIC ANGLED JOYSTICK (Estilo Emoji 🕹️ de Discord/Apple)
# Palanca inclinada con energía dinámica, base arcade en perspectiva limpia
# ==============================================================================
def draw_dynamic_angled(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base en perspectiva isométrica suave
    # Cara superior trapezoidal
    draw.polygon([(110, 328), (402, 328), (430, 424), (82, 424)], fill=color)
    # Suavizar esquinas exteriores de la base
    for pt in [(110, 328), (402, 328), (430, 424), (82, 424)]:
        draw.ellipse((pt[0]-16, pt[1]-16, pt[0]+16, pt[1]+16), fill=color)

    # Dos botones circulares en relieve a la derecha
    draw.ellipse((326, 350, 366, 390), fill=trans)
    draw.ellipse((374, 360, 414, 400), fill=trans)

    # Fuelle ovalado en la base de la palanca (en el lado izquierdo)
    draw.ellipse((168, 340, 276, 396), fill=color)
    draw.line([(180, 368), (264, 368)], fill=trans, width=6)

    # Palanca / eje inclinado dinámicamente hacia la derecha (de (222, 360) a (304, 142))
    # Inclinación natural de ~20° como en 🕹️
    draw.line([(222, 360), (304, 142)], fill=color, width=44)
    r = 22
    draw.ellipse((222-r, 360-r, 222+r, 360+r), fill=color)
    draw.ellipse((304-r, 142-r, 304+r, 142+r), fill=color)

    # Bola esférica grande en el extremo superior derecho
    bx, by, br = 304, 138, 86
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

# ==============================================================================
# CONCEPTO 2: ATARI 2600 RETRO ICON (El clásico icono de joystick cuadrado)
# Base cuadrada robusta, fuelle de goma estriado concéntrico y palanca recta
# ==============================================================================
def draw_atari_retro(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base casi cuadrada / rectangular compacta (estilo caja Atari)
    draw.rounded_rectangle((108, 290, 404, 436), radius=32, fill=color)

    # Botón rojo/disparo redondo icónico en la esquina superior izquierda
    draw.ellipse((136, 318, 186, 368), fill=trans)

    # Anillos estriados del fuelle de goma central
    # Anillo 1 (base)
    draw.ellipse((204, 280, 308, 320), fill=color)
    draw.line([(212, 300), (300, 300)], fill=trans, width=6)
    # Anillo 2 (medio)
    draw.ellipse((220, 250, 292, 286), fill=color)
    draw.line([(226, 268), (286, 268)], fill=trans, width=6)

    # Eje cilíndrico robusto con empuñadura ergonómica
    draw.rounded_rectangle((234, 126, 278, 258), radius=16, fill=color)

    # Extremo superior: stick con botón o bola achatada tipo joystick vintage
    bx, by, br = 256, 116, 74
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)
    # Tapa superior del stick
    draw.ellipse((256 - 36, 116 - 54, 256 + 36, 116 - 22), fill=trans)

    return img

# ==============================================================================
# CONCEPTO 3: FLIGHTSTICK / PALANCA DE SIMULADOR (Ergonómica con gatillo)
# Silueta moderna de palanca de vuelo con empuñadura contorneada
# ==============================================================================
def draw_flight_stick(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base circular / elíptica robusta de soporte
    draw.ellipse((96, 344, 416, 440), fill=color)
    draw.ellipse((140, 360, 372, 424), fill=trans)
    draw.ellipse((184, 372, 328, 412), fill=color)

    # Fuelle cónico de acordeón
    draw.polygon([(194, 380), (318, 380), (288, 300), (224, 300)], fill=color)
    draw.line([(206, 350), (306, 350)], fill=trans, width=8)

    # Empuñadura ergonómica (cuerpo de la palanca)
    draw.rounded_rectangle((226, 120, 286, 310), radius=22, fill=color)

    # Gatillo frontal (a la izquierda)
    trigger = [(226, 190), (180, 210), (180, 240), (226, 250)]
    draw.polygon(trigger, fill=color)
    draw.ellipse((170, 210, 194, 240), fill=color)

    # Cabezal superior de la palanca con botón de pulgar
    head_pts = [(210, 150), (320, 110), (304, 76), (220, 96)]
    draw.polygon(head_pts, fill=color)
    for pt in head_pts:
        draw.ellipse((pt[0]-16, pt[1]-16, pt[0]+16, pt[1]+16), fill=color)
    # Botón de pulgar en el cabezal
    draw.ellipse((270, 84, 302, 116), fill=trans)

    return img

# ==============================================================================
# CONCEPTO 4: ARCADE MINIMALISTA SIMÉTRICO (Súper equilibrado en 2x2)
# Diseñado con proporciones áureas: base elíptica limpia, dos botones simétricos
# ==============================================================================
def draw_arcade_symmetrical(color, trans):
    img = Image.new("RGBA", (SIZE, SIZE), trans)
    draw = ImageDraw.Draw(img)

    # Base arcade estilizada (cápsula redondeada de diseño moderno)
    # x=96..416 (ancho 320), y=320..424 (alto 104)
    draw.rounded_rectangle((96, 320, 416, 424), radius=52, fill=color)

    # Dos botones simétricos a la izquierda y derecha para equilibrio total en el split 2x2
    # Lado izquierdo (TL/BL)
    draw.ellipse((136, 350, 178, 392), fill=trans)
    # Lado derecho (TR/BR)
    draw.ellipse((334, 350, 376, 392), fill=trans)

    # Fuelle cónico limpio en el centro
    collar = [(208, 324), (304, 324), (280, 252), (232, 252)]
    draw.polygon(collar, fill=color)

    # Eje vertical metálico centrado y limpio
    draw.rounded_rectangle((236, 146, 276, 260), radius=14, fill=color)

    # Bola superior esférica grande perfectamente centrada
    bx, by, br = 256, 122, 84
    draw.ellipse((bx - br, by - br, bx + br, by + br), fill=color)

    return img

c1 = draw_dynamic_angled(YELLOW, TRANSPARENT_YELLOW)
c2 = draw_atari_retro(YELLOW, TRANSPARENT_YELLOW)
c3 = draw_flight_stick(YELLOW, TRANSPARENT_YELLOW)
c4 = draw_arcade_symmetrical(YELLOW, TRANSPARENT_YELLOW)

c1.resize((256, 256)).save(os.path.join(icons_dir, "opt1_dynamic_angled.png"))
c2.resize((256, 256)).save(os.path.join(icons_dir, "opt2_atari_retro.png"))
c3.resize((256, 256)).save(os.path.join(icons_dir, "opt3_flight_stick.png"))
c4.resize((256, 256)).save(os.path.join(icons_dir, "opt4_arcade_symmetrical.png"))

# Generar una hoja de comparación 2x2 en fondo oscuro de Discord (#313338)
sheet = Image.new("RGBA", (580, 580), (49, 51, 56, 255))
sheet.paste(c1.resize((240, 240)), (30, 30), c1.resize((240, 240)))
sheet.paste(c2.resize((240, 240)), (310, 30), c2.resize((240, 240)))
sheet.paste(c3.resize((240, 240)), (30, 310), c3.resize((240, 240)))
sheet.paste(c4.resize((240, 240)), (310, 310), c4.resize((240, 240)))

# Dibujar etiquetas numéricas
draw_s = ImageDraw.Draw(sheet)
draw_s.text((36, 36), "1. DINAMICO 🕹️", fill=(255, 255, 255, 220))
draw_s.text((316, 36), "2. ATARI RETRO", fill=(255, 255, 255, 220))
draw_s.text((36, 316), "3. FLIGHT STICK", fill=(255, 255, 255, 220))
draw_s.text((316, 316), "4. SIMETRICO", fill=(255, 255, 255, 220))

sheet.save(os.path.join(icons_dir, "comparativa_joysticks.png"))
print("Generated all 4 joystick concepts and comparison sheet!")
