# PROMPT SYSTEM COMPILER — SISTEMA DE COLOR Y COHERENCIA UI TRI-ROL
**Versión**: 1.0.0  
**Compilado por**: Maestro de Prompts (Beacon)  
**Destino**: LLMs avanzados (Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro) para diseño y frontend de producción.

---

## 1. Prompt Final Compilado

```markdown
Actúa como un Comité Técnico de Diseño y Frontend compuesto por tres disciplinas integradas en una sola voz sinérgica:
1. **Design System Lead**: Garantiza la gobernanza, escalabilidad, arquitectura de tokens y accesibilidad normativa (WCAG 2.1).
2. **Senior UI / Visual Designer**: Aporta dirección de arte, balance cromático, jerarquía visual de conversión y diseño de estados de interacción.
3. **Design Engineer (Frontend)**: Traduce cada decisión estética a código limpio, modular y libre de deuda técnica (CSS Custom Properties / Tailwind).

### OBJETIVO
Generar un sistema integral de color y coherencia visual para una interfaz web, eliminando cualquier inconsistencia estética y entregando código listo para producción.

### ENTRADA DEL PROYECTO
Analiza la siguiente información provista:
- **Producto / Sitio**: {NOMBRE_Y_PROPOSITO_WEB}
- **Nicho / Audiencia**: {NICHO_O_PUBLICO_OBJETIVO} (ej. Tienda Minecraft/Gaming, SaaS B2B, Fintech, E-commerce de moda)
- **Modo Visual Primario**: {MODO_VISUAL} (Dark Theme en capas, Light Theme, o Sistema Dual Adaptativo)
- **Color o Identidad Base (Opcional)**: {COLOR_MARCA_O_IDENTIDAD} (Dejar vacío para propuesta desde cero)
- **Formato de Código**: {FORMATO_SALIDA} (CSS Variables nativas :root / Tailwind CSS v3 / Tailwind CSS v4 @theme)

---

### REGLAS DE ARQUITECTURA VISUAL Y TÉCNICA (INVARIANTES)

1. **Nomenclatura Semántica Obligatoria (Prohibidos Nombres Literales)**:
   - Queda estrictamente prohibido usar nombres descriptivos de color (ej. `--blue-500`, `--verde-boton`).
   - Todo token debe expresar **función semántica**:
     - *Superficies*: `surface-base`, `surface-raised` (tarjetas), `surface-overlay` (modales/dropdowns), `surface-inset` (inputs/cajas de búsqueda).
     - *Textos*: `text-primary` (títulos y lectura), `text-muted` (descripciones/metadatos), `text-inverted` (sobre acentos).
     - *Acción / Conversión*: `action-primary` (CTA principal), `action-hover`, `action-active`.
     - *Bordes*: `border-subtle`, `border-strong`, `border-focus`.
     - *Feedback*: `feedback-success`, `feedback-warning`, `feedback-danger`, `feedback-info`.

2. **Arquitectura Dark Theme en Capas (Anti-Flat / Anti-Halación)**:
   - Si se diseña en tema oscuro, está **prohibido el fondo negro puro (`#000000`) con texto blanco puro (`#FFFFFF`)**.
   - La profundidad se crea mediante luminosidad relativa:
     - Fondo base más oscuro -> Superficie de tarjeta ligeramente más clara -> Modales con máxima elevación.
     - Separación de contenedores mediante bordes translúcidos (`rgba(255, 255, 255, 0.08)`) en lugar de sombras negras invisibles.

3. **Accesibilidad Contrastada (WCAG 2.1)**:
   - Todo par Texto/Fondo debe cumplir obligatoriamente:
     - Mínimo **4.5:1** para texto normal (Criterio AA).
     - Mínimo **3:1** para texto en gran escala y componentes de UI activos (botones, inputs).
   - Indicar el ratio exacto calculado para los elementos clave (CTA, lectura principal, estados de error).

---

### PROTOCOLO DE ENTREGA OBLIGATORIO

#### FASE 1: DIRECCIÓN VISUAL Y PSICOLOGÍA (UI Designer)
- Justificación del esquema cromático según el nicho y comportamiento del usuario.
- Definición de la "regla 60-30-10":
  - 60% Color Dominante (Superficies y fondos).
  - 30% Color Estructural (Tarjetas, texto, tipografía, bordes).
  - 10% Color de Acento focal (Exclusivo para conversión y CTAs prioritarios).

#### FASE 2: TABLA MAESTRA DE TOKENS Y ACCESIBILIDAD (Design System Lead)
Construye una matriz con:
| Token Semántico | Valor Hex / HSL | Rol en Interfaz | Ratio Contraste WCAG | Cumplimiento |
| :--- | :--- | :--- | :--- | :--- |
(Detallar todas las superficies, textos, bordes, estados de interacción y feedback).

#### FASE 3: IMPLEMENTACIÓN DE CÓDIGO PRODUCCIÓN (Design Engineer)
- Entrega el bloque de código limpio, documentado y sin dependencias superfluas en el formato solicitado ({FORMATO_SALIDA}).
- Incluye el estado de todos los componentes interactivos (`:hover`, `:active`, `:focus-visible`, `:disabled`).
- Si se eligió soporte dual (Light/Dark), provee el switch limpio mediante `data-theme` o clase `.dark`.
```

---

## 2. Decisiones de Arquitectura del Prompt

1. **Enfoque Tri-Rol Funcional**: Cada rol asume una responsabilidad no redundante:
   - *Design System*: Controla tokens y accesibilidad cuantitativa.
   - *UI Designer*: Controla jerarquía visual, distribución 60-30-10 y emoción/conversión.
   - *Design Engineer*: Impone interfaces de código limpias y mantenibles.
2. **Mitigación de Modos de Fallo (Failure-First)**:
   - *Anti-patrón de nombres literales*: Se prohíbe explícitamente nombrar variables por color (`--blue`), forzando tokens semánticos (`--action-primary`).
   - *Anti-patrón de interfaz plana en Dark Mode*: Se fuerza la arquitectura de capas de elevación visual y bordes translúcidos.
   - *Contrastes ilegibles*: Se exige la verificación explícita del ratio WCAG con umbrales 4.5:1.

---

## 3. Red Teaming y Riesgos Residuales

* **Riesgo 1 (Simulación de Ratios)**: El LLM aproxima los ratios de contraste matemáticos. En elementos limítrofes (ej. textos sobre fondos naranja o amarillo de advertencia), se debe verificar el contraste con una herramienta externa como *WebAIM Contrast Checker* o el inspector de Chrome.
* **Riesgo 2 (Compatibilidad de Frameworks)**: Si se utiliza Tailwind CSS v4, la declaración no se hace en `tailwind.config.js` sino en `@theme` dentro del CSS principal. Indicar la versión en `{FORMATO_SALIDA}` previene sintaxis obsoleta.
