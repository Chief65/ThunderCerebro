# Estándar Oficial: estilo_logo (ThunderStudios)

Protocolo y prompt maestro exclusivo para logotipos, iconos de tienda Tebex, avatares y marcas de identidad vectorial 2.5D de **ThunderStudios**.

---

## 1. Definición y Caso de Uso Estricto

- **Destino Exclusivo**: Logotipos, isotipos, avatares de Discord/redes, iconos de categorías de Tebex y sellos de marca.
- **Diferenciación Operativa**: No debe confundirse con la rama de *Renders Cinemáticos 3D CGI* (utilizada para banners y paisajes). `estilo_logo` es una ilustración vectorial 2.5D con estética de pegatina (*sticker*) y cel-shading pulido.
- **Referencia Base Inmutable**: `creator/raw/references/THUNDER_ICON_LOGO.png`.

---

## 2. Los 5 Pilares Gráficos de `estilo_logo`

1. **Perspectiva y Rotación**:
   - Perspectiva isométrica a tres cuartos sobre fondo blanco puro aislado.
   - Inclinación dinámica de **15° a 20° en sentido antihorario**, aportando agresividad y movimiento.
2. **Contorno de Pegatina (*Sticker Stroke*)**:
   - Trazo exterior grueso, uniforme y de cantos afilados.
   - Color obligatorio: **Marrón chocolate / Burdeos muy oscuro (`#3D0C0C` / `#4A1010`)**. PROHIBIDO el negro puro `#000000`.
3. **Expresión "Angry Mascot"**:
   - Ojos trapezoidales oscuros fuertemente inclinados hacia el centro (mirada feroz y competitiva de esports).
   - Hocico extruido en 3D con dos fosas nasales rectangulares oscuras.
4. **Sombreado Cel-Shading Vectorial**:
   - Iluminación directa desde la esquina superior derecha.
   - Transiciones internas mediante aerografiado suave (*smooth ambient gradients*) contenidas dentro de facetas geométricas estrictamente delimitadas.
   - Destellos triangulares especulares blancos en los vértices superiores iluminados.
5. **Paleta de Color Canónica**:
   - *Piel de Cerdo (Frente)*: Salmón rosado vibrante (`#FFA399`).
   - *Piel de Cerdo (Sombra)*: Coral carmesí profundo (`#FF4A40` / `#D63031`).
   - *Líneas y Rasgos*: Marrón burdeos oscuro (`#3D0C0C`).

---

## 3. Plantilla Maestra de Prompting para `estilo_logo`

```text
A premium 2.5D vector gaming mascot logo icon in the exact same art style, linework, and shading as the reference image, registered as estilo_logo. Featuring an angry Minecraft pig head wearing [ELEMENTO DE CABEZA / CASCO / CORONA]. Dynamic three-quarter isometric perspective, tilted dynamically 15 degrees counterclockwise on an isolated pure white background. Cubic blocky Minecraft pig head with extruded rectangular 3D snout, sharp rectangular nostrils, and fierce aggressive dark trapezoidal eyes. [DESCRIPCIÓN DEL ACCESORIO CON DETALLES DE PLANOS Y REMACHES]. Enclosed by a thick, bold, clean dark burgundy-brown outer contour outline (#4a1010) with sharp precise edges. Cel-shaded vector art finish with perfectly smooth, clean surfaces and crisp geometric plane separations. [ESQUEMA DE COLOR ESPECÍFICO DEL ACCESORIO]. Pig skin shaded with salmon-pink front and rich coral crimson shadow side. Bright directional key light from upper right, casting sharp planar shadows. Vector illustration, sticker style, strictly no photorealistic 3D realism, no pixel art, no micro-voxels, no complex background, no text.
```
