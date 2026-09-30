# Guía de Estilo: Logotipo / Icono Vectorial Mascota (THUNDER_ICON)

Ingeniería inversa de estilo y prompt maestro para generar variantes, iconos de rangos o avatares bajo el estilo canónico de **ThunderStudios (THUNDER_ICON_LOGO)**.

---

## 1. Prompt Maestro Extendido (Inglés de Alta Precisión)

```text
A premium 2.5D vector gaming mascot logo icon of an angry Minecraft pig head wearing a golden castle-crenellated crown, official esports app icon aesthetic. Dynamic three-quarter isometric perspective, tilted dynamically 15 degrees counterclockwise on an isolated pure white background.

SUBJECT & GEOMETRY:
Cubic blocky Minecraft pig head with an extruded rectangular 3D snout and sharp rectangular nostrils. Fierce, aggressive, determined expression with sharp angled trapezoidal dark eyes. Atop the cubic head sits a fortress battlements crown (castle crenellations with four stepped merlons) seamlessly integrated into the cubic geometry.

ART STYLE & LINEWORK:
Modern mobile game app icon and esports sticker illustration style. Enclosed by a thick, bold, clean dark burgundy-brown outer contour outline (#4a1010) with sharp, precise edges. Cel-shaded vector art finish with perfectly smooth, clean surfaces and crisp geometric plane separations.

COLOR PALETTE & GRADIENTS:
- Golden Crown: Radiant warm yellow to deep golden amber gradient (#FFE033 to #FF8C00) with bright specular triangle highlights on top-right facets and warm orange shadows on left/bottom facets.
- Pig Skin (Front Face): Vibrant soft salmon-pink (#FF9E9E) with a smooth clean ambient gradient.
- Pig Skin (Shadow/Side Face): Rich coral crimson (#FF5252 to #D63031) creating bold geometric 3D volume.
- Snout: Extruded box with pale pink front and deeper shaded underside.
- Eyes, Nostrils & Outlines: Deep dark chocolate burgundy-brown (#3D0C0C).

LIGHTING & RENDERING:
Bright directional key light coming from the upper right, casting sharp planar shadows across facets with clean airbrushed interior gradients. Ultra-clean graphic design finish, vector illustration, high saturation, high contrast.

NEGATIVE PROMPTS:
photorealistic, 3D CGI realism, pixel art, noisy textures, micro-voxels, realistic pig anatomy, rounded organic shapes, soft blurry airbrush, messy lines, text, typography, watermark, complex background, photographic skin texture.
```

---

## 2. Desglose Anatómico y Parámetros Técnicos

### A. Geometría y Composición
- **Rotación y Dinamismo**: El cubo no se presenta plano de frente ni isométrico estático; cuenta con un giro de ~15° a 20° antihorario que confiere agresividad y dinamismo de logotipo de videojuego.
- **Corona de Fortaleza (*Crenellated Crown*)**: 4 almenas escalonadas de castillo que sustituyen a la típica corona de puntas triangulares, reforzando la temática de facciones/reinos de Minecraft.
- **Mirada Hostil (*Angry Mascot*)**: En lugar de la mirada neutra/vacía del cerdo de Minecraft (ojos cuadrados separados), los ojos se han rediseñado como trapezoides inclinados hacia el centro, dotándolo de actitud competitiva.

### B. Sistema de Delineado (*Sticker Contour*)
- **Trazo Exterior (*Stroke*)**: Borde uniforme de grosor medio-alto en tono marrón chocolate/burdeos muy oscuro (`#3D0C0C` / `#4A1010`), nunca negro puro (el negro puro ensucia el contraste con el rosa y el dorado).
- **Separación de Facetas**: Las aristas entre la cara frontal, la cara lateral y la corona están perfectamente definidas por el salto cromático de los degradados, sin requerir líneas internas negras.

### C. Paleta Cromática Exacta
| Elemento | Código Hex Base | Función Visual |
| :--- | :--- | :--- |
| **Borde / Ojos / Fosas** | `#3D0C0C` - `#4A1010` | Contorno de pegatina y rasgos faciales oscuros |
| **Corona (Luz)** | `#FFF159` - `#FFD000` | Reflejo especular y plano superior |
| **Corona (Sombra)** | `#FF8A00` - `#D96B00` | Plano lateral de las almenas |
| **Cara Frontal** | `#FFA399` - `#FF8A80` | Iluminación directa de la cabeza |
| **Cara Lateral (Sombra)**| `#FF4A40` - `#E03030` | Profundidad tridimensional de bloque |
| **Hocico** | `#FFB8B0` / `#FF6B60` | Volumen extruido frontal |

---

## 3. Plantilla Modular para Derivar Nuevos Iconos

Para generar variantes (por ejemplo: con casco de hierro, con bandana pirata o con gemas), se conserva la base de estilo y se reemplaza el sujeto:

```text
A premium 2.5D vector gaming mascot logo icon of [SUJETO EN ESTILO MINECRAFT], official esports app icon aesthetic. Dynamic three-quarter isometric perspective, tilted 15 degrees counterclockwise on pure white background. Thick bold dark burgundy-brown outer contour outline, smooth cel-shaded vector gradients, high saturation, sharp planar shadows, clean graphic finish. Strictly no realistic textures, no pixel art, no noise.
```
