# Estándar Oficial de Embeds de Discord — ThunderMC (Estilo Sr Ramos)

Este documento define la especificación técnica y de diseño visual para todos los mensajes interactivos y embeds de Discord en **ThunderMC** (ThunderStudios).

---

## 1. Fundamentos Arquitectónicos

1. **Formato Estructural**: **Embed Tradicional (`embeds: [...]`)** con barra cromática lateral, **NUNCA** contenedor fluido `type: 17` para mensajes informativos principales. Esto garantiza un ancho contenido y consistente (~432 px) sin desbordamiento horizontal.
2. **Colorimetría Oficial**:
   - `color`: `16706304` (Hexadecimal `#FEEB00` / Amarillo Ámbar oficial de ThunderMC).
3. **Relación de Aspecto de Imagen**:
   - Proporción: **16:9 exacta**.
   - Dimensiones de referencia: **1138 × 640 px** (o 1920×1080 / 3840×2160 reescalado a esa base).
   - Renderizado: Integrado en el slot `"image": { "url": "..." }`, respetando las esquinas redondeadas nativas de Discord.

---

## 2. Jerarquía Tipográfica y Patrones de Markdown

| Elemento | Sintaxis | Ejemplo / Propósito |
| :--- | :--- | :--- |
| **Título** | Emoji simple + saludo/nombre | `👋 ¡Bienvenid@ a ThunderMC!` o `🔔 Roles de Notificaciones` |
| **Subtítulo Narrativo** | Subtexto bajo contraste (`-#`) con Small Caps | `-# ᴇᴍᴘɪᴇᴢᴀ ᴛᴜ ᴀᴠᴇɴᴛᴜʀᴀ ᴜɴɪᴇɴᴅᴏᴛᴇ ᴀʟ ꜱᴇʀᴠɪᴅᴏʀ` |
| **Listas de Atributos** | Título en negrita + emojis en backticks individuales | `**Encontraras:**\n`🏰` Dungeons Unicas\n`🐉` Jefes Custom` |
| **Llamada a la Acción (Copiar)** | Flecha direccional + aclaración entre paréntesis | `↓ IP del Servidor (Copia directa con 1 clic) ↓` |
| **Bloque 1-Clic Copy** | Bloque de código puro en lenguaje `text` | ```` ```text\nthundermc.es\n``` ```` (Garantiza portapapeles limpio) |
| **Datos Secundarios** | Subtexto con emojis en backticks | `-# 📱 Puerto Bedrock: `19132` \| 🎮 Java: Puerto por defecto` |
| **Enlaces de Navegación** | Negrita + subtexto con interpunct (`•`) | `**Links Interesantes:**\n-# [Tienda](url) • [Tiktok](url)` |
| **Encabezado Interactivo** | H2 (`##`) con subtítulo aclaratorio | `## Dashboard (Menu Interactivo)\nSelecciona una categoría...` |

---

## 3. Componentes Interactivos (UI Kit)

1. **Ubicación**: En el array raíz `components` (`type: 1` Action Row) justo debajo de los embeds.
2. **String Select Menu (`type: 3`)**:
   - `custom_id`: Identificador funcional snake_case (ej. `menu_principal`, `select_notificaciones`).
   - `placeholder`: Verbo en imperativo claro ("Elige una categoría...", "Selecciona tus alertas...").
   - `options`:
     - `label`: Nombre limpio de 2-4 palabras.
     - `value`: Clave técnica para backend/bot.
     - `description`: Resumen funcional conciso (máx. 50 caracteres).
     - `emoji`: Emoji visual que represente la opción.
   - `min_values` / `max_values`: 
     - Para menús de navegación: `min_values: 1`, `max_values: 1`.
     - Para selección de roles múltiples: `min_values: 0`, `max_values: N`.
3. **Botones de Enlace Web (`type: 2`, `style: 5`)**:
   - Para redirigir directamente a la web/tienda sin interacción intermedia del bot.
   - Restricción Discord: Solo `style: 5` admite campo `url` nativo (renderiza gris con icono de enlace externo).
   - Atributos requeridos: `label`, `url`, `emoji` (ej. `🪙` o `🛒`).
4. **Avatar Dinámico en Miniatura (`thumbnail`)**:
   - Ubicación: `"thumbnail": { "url": "https://minotar.net/bust/{player}/100" }`
   - Renderiza el busto 3D isométrico (cabeza y torso) en la esquina superior derecha del embed a partir del nickname. Tolera jugadores offline y Bedrock degradando limpiamente a Steve/Alex (HTTP 200). Alternativa para solo cabeza 2D: `https://mc-heads.net/avatar/{player}/100`.

---

## 4. Prompt Maestro Reutilizable (System Directive)

```text
Actúa como Diseñador Técnico de UI para Discord bajo el estándar estricto de ThunderMC (Estilo Sr Ramos). 
Al crear cualquier mensaje o embed de Discord, debes seguir obligatoriamente estas reglas:

1. Estructura: Usa exclusivamente la estructura de Embeds Tradicionales ("embeds": [...]) con "components": [...] en la raíz. No uses contenedores fluidos type: 17 a menos que se te ordene expresamente.
2. Color: El color del embed debe ser siempre 16706304 (#FEEB00 dorado ámbar oficial).
3. Título: Inicia siempre con un emoji representativo y texto conciso.
4. Tipografía y Estilo:
   - Usa un subtítulo narrativo en low-contrast (-#) con tipografía Small Caps (ᴀ ʙ ᴄ...).
   - Listas de contenido con viñetas usando emojis envueltos en backticks individuales (`🏰` Texto).
   - Bloques de copia directa de datos críticos (como IPs) en bloques de código puro (```text\nvalor\n```) sin prefijos contaminantes para permitir el copiado nativo de 1 clic.
   - Aclaraciones técnicas y enlaces en formato (-#) separados por interpuncts ( • ).
   - Encabezados de acción usando Markdown ## para indicar el uso de menús o botones inferiores.
5. Multimedia: Si incluye imagen, debe usar la relación 16:9 con resolución base 1138x640 px colocada en el campo "image".
6. Componentes Interactivos: Diseña siempre una Action Row (type: 1) con Select Menus (type: 3) o Botones (type: 2), proporcionando custom_id, placeholder claro, y opciones con emoji, label y description informativa.
Entrega siempre el payload JSON completo, sintácticamente impecable y listo para producción.
```
