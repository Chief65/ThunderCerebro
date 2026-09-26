# Estándares y Sintaxis de DeluxeMenus (1.14.x+)

**Ámbito**: Servidor de Pruebas y Survival — Servidores Minecraft 1.21.11  
**Objetivo**: Evitar advertencias (*deprecation warnings*) y garantizar compatibilidad futura.

---

## 1. Reglas de Item Flags (Prohibido Sintaxis Legacy)

Queda estrictamente prohibido el uso de claves booleanas obsoletas directas en items. Siempre debe utilizarse la lista `item_flags`.

| Directiva Obsoleta (LEGACY - PROHIBIDO) | Directiva Moderna Obligatoria (ACTUAL) |
|---|---|
| `hide_attributes: true` | `item_flags:`<br>&nbsp;&nbsp;`- HIDE_ATTRIBUTES` |
| `hide_enchantments: true` | `item_flags:`<br>&nbsp;&nbsp;`- HIDE_ENCHANTS` |
| `hide_effects: true` | `item_flags:`<br>&nbsp;&nbsp;`- HIDE_POTION_EFFECTS` |
| `hide_unbreakable: true` | `item_flags:`<br>&nbsp;&nbsp;`- HIDE_UNBREAKABLE` |
| `hide_dye: true` | `item_flags:`<br>&nbsp;&nbsp;`- HIDE_DYE` |

---

## 2. Estructura Estándar de Item con Flags

```yaml
  'Ejemplo_Boton':
    material: FIREWORK_STAR
    slot: 53
    display_name: '&#FEEB00Botón Ejemplo'
    item_flags:
      - HIDE_ATTRIBUTES
      - HIDE_ENCHANTS
    enchantments:
      - UNBREAKING;1
    lore:
      - '&7Texto descriptivo'
    left_click_commands:
      - '[sound] UI_BUTTON_CLICK'
      - '[close]'
```

---

## 3. Lecciones Aprendidas del Feedback del Sr Ramos

### [2026-09-07] Leccion 1: El filtrador de categorias debe tener coherencia entre menus
- **Contexto**: Menu de banners en ShopGUIPlus mostraba categorias incorrectas (Trims, Encantamientos) en su filtrador.
- **Error previo**: El comparador de banners tenia en el lore las mismas categorias que los menus de XP.
- **Correccion aplicada**: Cada menu muestra solo sus propias categorias en el filtrador. El comparador de banners muestra solo "Colores" y "Custom". El de almas solo "Spawners", "Llaves", "Protecciones". El de XP solo "Trims" y "Encantamientos".
- **Regla derivada**: El lore del boton COMPARATOR de filtrado SIEMPRE debe listar unicamente las categorias propias del contexto del menu actual. Nunca copiar/pegar el lore de otro menu sin adaptar las categorias.

### [2026-09-07] Leccion 2: Los balances en items dummy de ShopGUIPlus NO parsean PlaceholderAPI
- **Contexto**: Se intentaba mostrar %thundercurrencys_almas% en un item dummy de ShopGUIPlus.
- **Error previo**: Usar type: dummy con placeholder PAPI en lore -> el texto se muestra como texto literal.
- **Correccion aplicada**: Migrar a type: special con special: balance en las tiendas de ShopGUIPlus. En DeluxeMenus si funcionan los placeholders PAPI.
- **Regla derivada**: En ShopGUIPlus -> type: special / special: balance. En DeluxeMenus -> placeholder PAPI directo en lore. Nunca cruzar.

### [2026-09-07] Leccion 3: Las 3 filas de productos deben estar completas (sin huecos)
- **Contexto**: Tienda de banners con slots vacios en filas de contenido.
- **Error previo**: Paginas con menos de 27 productos dejaban slots vacios visibles.
- **Correccion aplicada**: Rellenar todas las 3 filas de contenido (slots 9 a 35 en un menu de 45 slots) con productos. Si no hay suficientes productos, generar mas o usar variantes.
- **Regla derivada**: Los 27 slots de contenido (fila 2, 3 y 4 de la zona de items) deben estar siempre ocupados en menus de ShopGUIPlus paginados.

### [2026-09-07] Leccion 4: El boton de Catalogo de Precios es EXCLUSIVO del menu principal
- **Contexto**: El boton SPYGLASS de catalogo aparecia en menus secundarios.
- **Error previo**: Copiar la navbar del menu principal a submenus sin filtrar el boton de catalogo.
- **Correccion aplicada**: Eliminar SPYGLASS de todos los menus excepto tienda_principal.yml.
- **Regla derivada**: El boton de Catalogo de Precios (SPYGLASS) solo existe en tienda_principal.yml slot 27. Ningun otro menu lo tiene.

### [2026-09-07] Leccion 5: Cristales en posiciones de flechas de navegacion generan bugs visuales
- **Contexto**: Cristales decorativos en slots 33, 34, 35 de un menu de ShopGUIPlus bloqueaban los items de venta.
- **Error previo**: Poner cristales decorativos en slots que pertenecen a la zona de contenido o a las flechas nativas.
- **Correccion aplicada**: En menus de ShopGUIPlus el slot 39 es flecha anterior, 40 es volver, 41 es flecha siguiente, 44 es balance. Los slots 33-35 son slots de VENTA, no de decoracion.
- **Regla derivada**: En ShopGUIPlus (size 45), slots 9-35 son zona de productos. Slots 36-44 son navbar. No poner cristales en zona de productos.


### [2026-09-07] Leccion 6: Espaciado vertical y aislamiento de prototipos
- **Contexto**: Creación de prototipos nuevos de menús (ej. mercado_comercio.yml).
- **Error previo**: Crear menús compactos de 3 filas donde la barra de navbar queda inmediatamente pegada a la fila de botones funcionales, y asumir enlaces con menús existentes (como tienda_vender) sin instrucción explícita.
- **Correccion aplicada**: Cambiar a 4 filas (size: 36) para dejar la fila 3 (slots 18-26) completamente libre como respirador visual antes del navbar (slots 27-35), y dejar los clicks sin redirecciones a menús viejos salvo orden directa.
- **Regla derivada**: Los menús principales o intermediarios nuevos deben tener un mínimo de 4 filas (size: 36) para asegurar aire visual entre el contenido (fila 2) y la barra de navegación (fila 4). No enlazar sistemas existentes a un prototipo nuevo sin petición explícita.


### [2026-09-10] Lección 8: Disposición de Lonja Diaria y Limpieza de Relleno (6 filas, size 54)
- **Contexto**: Diseño de la Lonja de Venta bursátil con 5 cupos rotativos.
- **Error previo**: Usar paneles de cristal de relleno alrededor de los ítems en menús de venta bursátil (ensucia la interfaz), colocar los cristales indicadores arriba en vez de abajo de cada ítem, y usar descripciones de lore demasiado anchas horizontalmente.
- **Corrección aplicada**: 
  - Expandir el menú a 6 filas (`size: 54`).
  - Eliminar todos los cristales de marco/relleno decorativo, dejando respirar el cofre.
  - Colocar los 5 ítems de venta en la Fila 3 (slots 20 a 24).
  - Colocar los cristales indicadores de tendencia exactamente debajo de cada producto en la Fila 4 (slots 29 a 33).
  - Reubicar la Navbar en la Fila 6 (slots 45 a 53): Pronóstico/Pity en slot 45 (izquierda extrema), Volver en slot 49 (centro), Venta Rápida en slot 52 (al lado del balance), y Tu Economía en slot 53 (derecha extrema).
  - Compactar el ancho horizontal del lore a sintaxis ultra-concisa (`U:`, `x64:`, `Trend:`, `Acción:`, `Uso hoy:`).
- **Regla derivada**: En menús de venta bursátil/mercados tipo lonja, prescindir de marcos de cristal de relleno para máxima limpieza visual. Los indicadores de estado se posicionan directamente bajo cada ítem y los lores deben priorizar la brevedad horizontal.
  - **Límite de caracteres en títulos con temporizador**: Al combinar el prefijo estándar `&0&l|&r &0Sección ▶ &#FFF275` con contadores como `&8(03h 42m)`, el nombre de la sección debe ser de una sola palabra (ej. `&#FFF275Venta`) para evitar que el texto se trunque o se desborde fuera del marco GUI del cliente de Minecraft.

### [2026-09-10] Lección 9: Universalización del Ícono de Economía Multimoneda
- **Contexto**: Diversidad de íconos de balance (`KELP`, `SOUL_CAMPFIRE`, `EXPERIENCE_BOTTLE`) en subtiendas y menús intermediarios.
- **Error previo**: Usar materiales aislados según la moneda de la subtienda en lugar de una interfaz consistente para el jugador.
- **Corrección aplicada**: Homogeneizar todos los menús (principales, categorías de compra, intermediarios, lonja y pity) con el ícono unificado de la cabeza del jugador (`head-%player_name%`) y el lore multimoneda canónico completo (Dinero, Almas, Zafiros, XP), enlazado a `[openguimenu] info_economia`.
- **Regla derivada**: En todos los menús del sistema de economía de ThunderMC, el botón `Info_Balance` SIEMPRE debe ser `head-%player_name%` con el bloque multimoneda completo, permitiendo consultar el balance global y acceder a `info_economia` desde cualquier pantalla.


