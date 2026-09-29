# 🎨 Guía de Estilo & Patrones Visuales de Menús — ThunderMC (DeluxeMenus & CommandPanels)

Documento maestro de diseño UI/UX para la creación de menús en la red ThunderMC.

---

## 🏛️ 1. Estructura y Títulos de Menús (menu_title / title)
El estándar visual de títulos utiliza separadores sobrios en negro/gris oscuro con mayúsculas y sub-secciones claras:
- **Patrón Principal**: `&0&l|&r &0<Categoría> » &8<Subtítulo/Acción>`
  - Ejemplo: `&0&l|&r &0Casas » &8Eliminar hogar`
  - Ejemplo: `&0&l|&r &0Dash » &8Inicio`
  - Ejemplo: `&0&l|&r &0Dash » &8Novato 2/20`
- **Títulos con Temporizador / Eventos**: `&8» Temporada 1 | &830d 12h 5min &8«`

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## 💎 2. Paleta de Colores y Formato
- **Títulos de Ítem / Encabezados**:
  - Acentos de Color Principal: `&#FEEB00` (Amarillo Thunder), `&#59E91F` (Verde Esmeralda/Dinero), `&#34B0F3` (Azul Zafiro/Almas), `&#FF0000` o `&#EB1717` (Rojo Alerta/Cancelar), `&#00FC00` (Verde Confirmar).
  - Íconos y Viñetas: `»`, `▶`, `•`, `✦`, `⚔`, `⛏`, `💎`, `👑`, `⌚`, `👤`.
- **Estructura del Lore**:
  1. **Separador Superior Decorativo**: `&8» <Título Sección en Small Caps o MiniMessage>`
  2. **Línea en Blanco**: `''`
  3. **Cuerpo Informativo**:
     - `&8 • &fCampo: &7%variable%`
     - `&8 • &fMundo: &7%world%`
  4. **Línea en Blanco**: `''`
  5. **Call to Action (Acción al Clic)**:
     - Aceptar/Acción: `&7▶ Click para seleccionar` / `&7▶ Click para eliminar` / `&7▶ Click para abrir`
     - Volver/Atrás: `&7▶ Click para volver`

---

## 🖼️ 3. Distribución de Slots y Relleno (Layout UI)
- **Tamaño Estándar**: `size: 27` (3 filas) para confirmaciones y submenús; `size: 54` (6 filas) para Dashboards, Trabajos y Niveles.
- **Panel Lateral de Navegación (Dashboard 6 Filas)**:
  - Columna 0 (Slots 0, 9, 18, 27, 36, 45): Ítems de navegación fija (Rachas, Ubicaciones, Temporada, Trabajos, Recetas, Perfil).
  - Columna 1 (Slots 1, 10, 19, 28, 37, 46): Separador vertical de cristal negro/gris (`GRAY_STAINED_GLASS_PANE` / `BLACK_STAINED_GLASS_PANE`).
  - Columnas 2 a 8: Contenido interactivo dinámico.
- **Diálogos de Confirmación (3 Filas / 27 Slots)**:
  - Slot 11: Cancelar (`RED_STAINED_GLASS_PANE`, `&#FF0000Cancelar`, `&7▶ Click para cancelar`).
  - Slot 13: Ítem Objetivo / Preview (`LIME_BED`, etc.).
  - Slot 15: Aceptar / Confirmar (`LIME_STAINED_GLASS_PANE`, `&#00FC00Aceptar`, `&7▶ Click para eliminar/comprar`).

---

## 🔊 4. Acciones y Sonidos Estándar
- **Clic en Botón**: `[sound] UI_BUTTON_CLICK` o `[sound] ENTITY_EXPERIENCE_ORB_PICKUP`
- **Error / Cancelar**: `[sound] BLOCK_NOTE_BLOCK_BASS`
- **Éxito / Compra**: `[sound] ENTITY_PLAYER_LEVELUP` o `[sound] BLOCK_NOTE_BLOCK_PLING`
- **Transición de Menú**: `[openguimenu] <NombreMenu>`

---

## Referencias Cruzadas
- [[wiki/concepts/deluxemenus_standards|EstÃ¡ndares DeluxeMenus]]
- [[wiki/entities/thundermc/iconos-compatibles-ui|Iconos Compatibles UI]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
