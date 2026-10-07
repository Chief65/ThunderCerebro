# Estándar de Expresiones Faciales y Rigs para Renders Minecraft (3D Expressive Rig)

Documento normativo para la generación y dirección de arte de personajes en renders 3D de **ThunderStudios** con expresividad facial avanzada, preservando la estética canónica cúbica de Minecraft.

---

## 1. Fundamentos del Estilo Visual (Rig Tipo Blender / Enderframes)

El estilo no utiliza caras hiperrealistas, redondeadas ni anime. Mantiene la esencia geométrica de Minecraft mientras introduce un sistema de rigging facial tridimensional:

1. **Malla Base Cúbica & Resolución Vanilla**: La cabeza mantiene la estructura ortogonal pura (cubo) y la cuadrícula de texturas tipo pixel-art (16x16 / 32x32) con sombreado PBR limpio y biselado sutil.
2. **Cejas Articuladas 3D (Extrusión Geométrica)**: No son píxeles planos pintados. Son prismas rectangulares en relieve que pueden rotar, arquearse y fruncirse asimétricamente para comunicar emoción.
3. **Ojos con Párpados y Mirada Direccional (*Glance*)**: Ojos cúbicos/rectangulares con esclera blanca nítida, pupila desplazada y párpados móviles cortados en línea recta o diagonal leve.
4. **Boca Geométrica Estilizada**: Ranura sutilmente curvada o rectangular con remate limpio (opcional: destello o bloque de diente blanco único). Evita bocas orgánicas de masa blanda tipo Disney/Pixar.

---

## 2. Estructura del Prompt Modular para Rostros

```text
Close-up of a Minecraft character face, 3D Minecraft render style, Blender Minecraft rig, voxel cubic head retaining crisp pixel texture grid. Expressive 3D facial rig: [CEJAS], [OJOS_Y_MIRADA], [BOCA] showing [EMOCION], subtle bevelled edges, warm studio key lighting on the cubic face, no uncanny valley, clean blocky aesthetic.
```

---

## 3. Catálogo de Expresiones Estandarizadas

### A. Desafiante / Seguro de Sí Mismo (Defiant / Cocky / Smirking)
* **Cejas**: `asymmetrical extruded blocky eyebrows, one brow raised confidently and one slightly furrowed`.
* **Ojos/Mirada**: `sharp rectangular eyes with subtle hooded upper eyelids, pupils glancing sideways with intense focused determination`.
* **Boca**: `subtle corner-turned smirk slit mouth with a tiny white tooth glint`.
* **Emoción**: `confident defiant smirk, daring challenger attitude`.

### B. Felicidad / Serenidad Confiada (Friendly / Content)
* **Cejas**: `relaxed slightly elevated blocky eyebrows in a gentle arch`.
* **Ojos/Mirada**: `warm rectangular eyes with soft lower-eyelid curve, glancing pleasantly sideways`.
* **Boca**: `subtle upturned curved mouth slit showing calm warmth and friendly satisfaction`.
* **Emoción**: `friendly contentment, gentle relaxed confidence`.

### C. Misterio / Suspicacia (Mysterious / Suspicious)
* **Cejas**: `tense asymmetric blocky eyebrows, one sharply raised high and one lowered in doubt`.
* **Ojos/Mirada**: `narrowed hooded rectangular eyes with tiny focused pupils peering sideways`.
* **Boca**: `tight horizontal slit mouth, sealed shut with subtle skeptical tension`.
* **Emoción**: `quiet suspicion, enigmatic intrigue and calculation`.

### D. Asombro / Tensión Alerta (Shocked / Alert)
* **Cejas**: `high arched blocky eyebrows pulled straight up in alert surprise`.
* **Ojos/Mirada**: `wide square dilated eyes staring intensely forward`.
* **Boca**: `small open rectangular mouth dropped slightly open showing tense shock`.
* **Emoción**: `alert astonishment, breathless realization`.

### E. Furia / Combate Decidido (Fierce / Battle Focus)
* **Cejas**: `heavily furrowed and angled downward blocky eyebrows meeting over the brow ridge`.
* **Ojos/Mirada**: `clenched narrow rectangular eyes locked into an aggressive direct stare`.
* **Boca**: `taut grimace slit mouth showing gritted cubic teeth`.
* **Emoción**: `fierce battle intensity, unyielding aggression`.

---

## 4. Tokens Negativos Obligatorios

Para evitar deformaciones orgánicas o rupturas con el canon:
* `smooth skin, round anime face, hyperrealistic human eyes, photorealistic skin pores, disney pixar rounded mouth, realistic mammal snout, spherical eyes, messy micro-voxels, noisy textures`.

---

## 5. Historial de Pruebas y Estado en Memoria

* **Prueba 1 (2026-10-06 - Cerdo Caballero Desafiante)**:
  - Archivo: `creator/output/renders/cerdo_caballero_desafiante/cerdo_caballero_desafiante_1.jpg`
  - Veredicto Sr Ramos: Correcto en ejecución técnica pero no convence estéticamente.
  - Estado: **En reserva / Latente**. No utilizar por defecto para personajes principales a menos que el Sr Ramos solicite explorar o recuperar este estilo específico.

