# Pipeline y Estándar de Renders Cinemáticos Minecraft — ThunderStudios

Guía técnica, framework de prompting y control de calidad visual para renders promocionales AAA de Minecraft (ThunderVerse / Network 1.21.11).

---

## 1. Resumen de Aprendizajes de la Sesión (RND-001 a RND-004)

| Iteración | Puntos Críticos Corregidos | Lección Operativa |
| :--- | :--- | :--- |
| **RND-001** | Prompt masivo (galeón + armada + tripulación numerosa). Generó texto accidental (*"The Hog's Revenge"*), sobrecarga visual y pérdida de foco. | **Sobrecarga de contexto**: Los prompts kilométricos dispersan la atención de la IA y generan alucinaciones no deseadas. |
| **RND-002** | Simplificación a barca de roble vainilla y 2 cerdos en composición centrada. Iluminación de atardecer. | **Composición funcional**: Centrar el sujeto en 16:9 garantiza espacio negativo en los tercios laterales para interfaces web/Tebex. |
| **RND-003** | Transición a día pleno brillante y postura de remado activa del tripulante. | **Cinética obligatoria**: Si hay una herramienta o vehículo (remos), el personaje debe interactuar físicamente, no solo posar cerca. |
| **RND-004** | Caracterización pirata completa (capitán con parche, loro en hombro y espada al frente; remero con ropa de marinero a rayas y pañuelo). | **Micro-accesorios compatibles con Minecraft**: Los elementos temáticos deben traducirse a volúmenes cúbicos limpios, no a detalles microscópicos. |

---

## 2. Diagnóstico Clínico del "7/10" (Brecha hacia el 10/10 AAA)

Para elevar los resultados de un 7/10 a un 9-10/10 (nivel trailer oficial de Mojang / Minecraft Dungeons / key-art cinematográfico), se deben solucionar 4 deficiencias técnicas detectadas en RND-004:

1. **Texturas Híbridas vs. Materiales PBR Reales**:
   - *Fallo actual (7/10)*: La madera y la piel presentan un aspecto a veces ceroso o plástico semi-difuso.
   - *Objetivo (10/10)*: Requerir acabado de sombreado PBR con sutiles mapas de rugosidad (*roughness*), biseles sutiles en los bordes de los cubos (*bevelled edges / soft chamfers*) para que la luz capture el contorno del bloque de forma natural sin verse afilado como render barato ni redondeado como plastilina.
2. **Discordancia en la Física del Agua**:
   - *Fallo actual (7/10)*: La espuma mezcla cubos flotantes con salpicaduras líquidas realistas, generando una colisión de estilos.
   - *Objetivo (10/10)*: Homogeneizar el estilo: agua volumétrica estilizada con refracción y cáusticas limpias, pero con espuma geométrica coherente.
3. **Rigging Facial y Expresividad**:
   - *Fallo actual (7/10)*: Los ojos y expresiones son calcomanías planas estándar de Minecraft sin profundidad.
   - *Objetivo (10/10)*: Incorporar sutil profundidad en los párpados o cuencas (estilo cinemáticas oficiales de Minecraft) para dotar de intención y personalidad al personaje.
4. **Gradación de Color y Oclusión de Contacto**:
   - *Fallo actual (7/10)*: La barca flota ligeramente sin una sombra de contacto (*ambient occlusion / contact shadow*) lo suficientemente pesada en la línea de flotación.
   - *Objetivo (10/10)*: Forzar sombras de contacto nítidas y gradientes de color (*color grading*) cinematográfico cinematográfico.

---

## 3. Las 5 Reglas Maestras para Futuros Prompts

### Regla 1: Delimitación Estricta de Entidades
- **Nunca** solicitar "una multitud" o "un ejército" sin un primer plano ultra definido.
- Declarar el número exacto de entidades en primer plano: `"Strictly two characters: [Personaje A en pose X], [Personaje B en pose Y]"`.

### Regla 2: Geometría Macro Cúbica + Sombreado PBR
- Mantener la forma de bloque a nivel de silueta, pero exigir materiales avanzados:
  `"Macro Minecraft cubic geometry, subtle bevelled block edges, stylized PBR materials, soft specular highlights, clean ambient occlusion"`.
- Prohibir terminantemente la micro-voxelización: `"No tiny voxels, no dense cube noise, no LEGO-like fragmented surfaces"`.

### Regla 3: Composición Orientada a Producción (UI-Ready)
- Definir siempre el caso de uso y el encuadre:
  - **Banner Web / Hero (16:9)**: Sujeto centrado o en regla de tercios con amplio espacio negativo lateral para títulos y botones.
  - **Icono Tebex / Item / Rango (1:1)**: Encuadre centrado cerrado (*close-up* / plano medio) con fondo limpio o gradiente de desenfoque.

### Regla 4: Dinamismo de Objetos y Cinemática
- Si un personaje porta un objeto (espada, remo, pico, arco), describir el vector de movimiento y la postura muscular:
  `"[Personaje] actively holding [Objeto] pointing straight towards the viewer with heroic dynamic intent"`.

### Regla 5: Bloque de Negativos Blindado
Incluir siempre en el generador el bloque de exclusiones técnicas:
```text
Negative: text, typography, watermark, logo, UI elements, low-res textures, micro voxels, LEGO brick studs, realistic human anatomy, photorealistic animal anatomy, deformed hands, broken blocks, oversaturated neon, flat 2D shading.
```

---

## 4. Plantilla Maestra de Prompting para ThunderStudios

```text
[ENCABEZADO DE ESTILO]:
A masterclass 3D cinematic Minecraft CGI illustration, official Mojang cinematic trailer quality, [16:9 banner / 1:1 icon].

[SUJETO Y POSE]:
[Cantidad exacta y descripción de personajes con roles, ropa y objetos específicos en posturas dinámicas activas].

[COMPOSICIÓN Y CÁMARA]:
[Posición en el encuadre: centrado / regla de tercios], [ángulo de cámara: contrapicado heroico / plano medio], ample negative space on [sides / top] for web typography.

[GEOMETRÍA Y MATERIALES]:
Iconic macro-level Minecraft block geometry, canonical vanilla textures enhanced with subtle bevelled edges, stylized PBR shaders, clean surfaces without noisy micro-cubes.

[ILUMINACIÓN Y AMBIENTE]:
[Tipo de luz: diurna cristalina / nocturna con antorchas], strong directional key light, golden rim lighting, soft ambient occlusion contact shadows, [cielo y partículas atmosféricas controladas].

[RESTRICCIONES]:
Strictly no text, no logos, no watermarks, no photorealistic flesh, no LEGO studs, no chaotic voxel clusters.
```
