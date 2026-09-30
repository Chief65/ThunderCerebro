# RND-001: Baby Pig Pirate Captain (Armada Banner)

- **ID**: `RND-001`
- **Nombre de archivo**: `pig_pirate_captain.jpg`
- **Ubicación de Salida**: `creator/output/renders/pig_pirate_captain.jpg`
- **Formato**: 16:9 (Cinematic Banner / Web Hero)
- **Caso de Uso**: Banner principal de servidor / Tienda Web Tebex / Campaña temática de Piratas

---

## 1. Prompt Completo Utilizado

```text
A highly polished cinematic 3D Minecraft CGI illustration for a premium Minecraft server promotional banner. Wide 16:9 cinematic landscape composition, low-angle heroic camera near water level looking upward. In the foreground, a small cute Minecraft baby pig stands heroically at the bow of a gigantic wooden Minecraft pirate flagship, commanding an armada. The baby pig has unmistakable Minecraft cubic proportions, wearing a dark black pirate captain hat with gold trim and emblem, and an elegant small dark red captain coat with gold accents. On the deck behind him is a lively crew of Minecraft blocky pigs in pirate attire. Across a glossy, vibrant turquoise and deep blue ocean with stylized waves and white foam, an immense fleet of Minecraft pirate ships stretches toward the horizon under atmospheric perspective. Sunny sky with warm golden volumetric sunlight, bright cyan water reflections, strong rim lighting, and soft stylized Minecraft clouds. Clean macro-level Minecraft block geometry with smooth cinematic shading, broad readable surfaces, and AAA game promotional key-art finish. Not micro-voxelized, no dense noisy cube textures, no pixel art, no realistic animal anatomy.
```

---

## 2. Parámetros Técnicos

- **Aspect Ratio**: 16:9
- **Tipo de Cámara**: Gran angular moderado, ángulo contrapicado a nivel del agua (*low-angle heroic shot*).
- **Esquema de Color**:
  - Luces: Oro cálido (sol poniente/mediodía dramático) y reflejos cian/turquesa del mar.
  - Sombras y Tonos Medios: Marrón madera oscura, negro carbón (velas), azul marino profundo.
  - Acentos: Rosa canónico Minecraft (cerdos), rojo carmesí oscuro y dorado (atuendos piratas).

---

## 3. Red Teaming y Análisis de Calidad

### Fortalezas Técnicas:
1. **Separación de Planos**: El contraste entre el barco insignia en primer plano y la armada difuminada en el fondo genera una escala épica sin empastar la imagen.
2. **Geometría Cúbica Controlada**: El cerdo protagonista conserva la cabeza cúbica, hocico cuadrado y patas cortas características de Minecraft, evitando el error común de la IA de suavizar los bordes hacia un cerdo realista.
3. **Calidad de Materiales**: El agua exhibe refracción y reflejos cinemáticos sin perder el estilo estilizado del juego.

### Riesgos y Desviaciones Observadas (Modos de Fallo a Vigilar):
1. **Generación Involuntaria de Texto**: El modelo introdujo la placa `"THE HOG'S REVENGE"` en el casco del navío. Aunque aquí aporta sabor narrativo pirata, en renders futuros donde se requiera espacio limpio para logos o tipografías de Tebex, debe forzarse el negativo estricto contra texto incrustado.
2. **Complejidad de Aparejos de Barcos**: La jarcia y cuerdas tienden a generar micro-líneas complejas que pueden desentonar si el servidor busca un estilo minimalista puro.
