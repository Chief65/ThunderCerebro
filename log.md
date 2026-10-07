# Registro de Auditoría y Crónica (log.md)

Registro cronológico e incremental de todas las operaciones realizadas en **ThunderCerebro**.

## [2026-10-06] creator & discord | Integración de Bolsa Morada (Purple Bundle) en Embed de Sorteos
- **Archivos Modificados y Guardados**:
  - [`creator/output/discord/sorteo_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/sorteo_embed.json)
  - [`creator/lab/discord_bot/sorteo_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/sorteo_embed.json)
  - [`creator/lab/discord_bot/sorteo_manager.js`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/sorteo_manager.js)
- **Activos Locales Guardados**:
  - [`raw/assets/purple_bundle_closed.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/raw/assets/purple_bundle_closed.png) (Sprite oficial con canal alfa)
  - [`raw/assets/purple_bundle_open.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/raw/assets/purple_bundle_open.png) (Variante abierta)
- **Especificaciones Implementadas**:
  1. Adopción del sprite oficial de Minecraft 1.21 de Bolsa Morada Cerrada en el slot `thumbnail` del embed de sorteos.
  2. Thumbnail alojado y validado en CDN Discord con fondo transparente.
  3. Despacho verificado al canal oficial de Discord (`1552723526996336724`) con Message ID `1557219346407759953`.
  4. Guardado consolidado en `lab/` y `output/` para producción.

## [2026-10-06] creator & discord | Actualización de Avatar del Bot (Valyr sin Libro - Peto Limpio)
- **Archivos Creados**:
  - [`creator/output/renders/discord_avatar/valyr_bot_pfp_nobook_transparent.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/discord_avatar/valyr_bot_pfp_nobook_transparent.png)
  - [`creator/output/renders/discord_avatar/valyr_bot_pfp_nobook.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/discord_avatar/valyr_bot_pfp_nobook.jpg)
- **Especificaciones Implementadas**:
  1. Supresión total del libro o elementos sostenidos a petición del Sr Ramos.
  2. Retención del encuadre ampliado (zoom cerrado del 80%) y giro 3/4 hacia la derecha.
  3. Expresión canónica 100% neutra de mob vanilla de Minecraft (ojos de 2 píxeles, cero boca).
  4. Peto de hierro pulido limpio y hombreras dobles dominando el torso.
  5. Extracción con anti-aliasing a PNG transparente RGBA 32-bit.
  6. Despacho directo a la API de Discord (`PATCH /users/@me`) para `ValyrPruebas#2861` (Nuevo Hash CDN: `4e90c292e2951f646761282115ecee31`).

## [2026-10-06] creator & discord | Actualización de Foto de Perfil del Bot de Discord (Valyr Zoom & Expresión Neutra)
- **Archivos Creados/Actualizados**:
  - [`creator/output/renders/discord_avatar/valyr_bot_pfp_zoom_neutral_transparent.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/discord_avatar/valyr_bot_pfp_zoom_neutral_transparent.png)
  - [`creator/output/renders/discord_avatar/valyr_bot_pfp_zoom_neutral.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/discord_avatar/valyr_bot_pfp_zoom_neutral.jpg)
- **Especificaciones Implementadas**:
  1. Encuadre ampliado (zoom cerrado del 80% del plano vertical) para legibilidad en círculos pequeños de Discord.
  2. Expresión canónica 100% neutra de mob vanilla de Minecraft (ojos de 2 píxeles sin inclinación ni expresiones humanizadas).
  3. Perfil girado en 3/4 mirando hacia la derecha con libro "ADVENTURER" abierto.
  4. Extracción de canal alfa a PNG transparente RGBA 32-bit con anti-aliasing de bordes limpio.
  5. Despacho directo a la API de Discord (`PATCH /users/@me`) para el bot `ValyrPruebas#2861` (Nuevo Hash CDN: `182f876723f8252c25d611fc5bcefe1b`).

## [2026-10-06] creator & discord | Adopción de Busto 3D (Cara y Torso) en Embed de Compras Tebex
- **Archivos Modificados**: [`creator/output/discord/tebex_purchase_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/tebex_purchase_embed.json), [`creator/lab/discord_bot/tebex_purchase_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/tebex_purchase_embed.json), [`creator/lab/discord_bot/tebex_listener.js`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/tebex_listener.js), [`wiki/concepts/estandar_embeds_discord.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/wiki/concepts/estandar_embeds_discord.md).
- **Especificaciones Implementadas**:
  1. Sustitución del render de cabeza (`mc-heads.net/avatar/{player}/100`) por el busto 3D isométrico (`https://minotar.net/bust/{player}/100`), integrando cabeza y torso en la miniatura.
  2. Tolerancia garantizada para jugadores offline y Bedrock (fallback automático a skins estándar Steve/Alex con código HTTP 200).
  3. Prueba de despacho validada y aprobada por el Sr Ramos en el canal `1552723526996336724` (Message ID: `1557190333413064706`).

## [2026-10-06] creator & discord | Refinamiento y Simplificación del Embed de Sorteos
- **Archivos Modificados**: [`creator/output/discord/sorteo_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/sorteo_embed.json), [`creator/lab/discord_bot/sorteo_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/sorteo_embed.json), [`creator/lab/discord_bot/sorteo_manager.js`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/sorteo_manager.js), [`creator/lab/discord_bot/send.ps1`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/send.ps1).
- **Especificaciones Implementadas**:
  1. Premio unificado en formato H1 (`# 🏆 Rango Titán [Permanente]`), eliminando tiers por puestos.
  2. Temporizador dinámico de Discord destacado en formato H1 (`# ⏳ <t:TIMESTAMP:R>`).
  3. Eliminación de requisitos y supresión del bloque de IP/puerto del cuerpo.
  4. Retiro del banner inferior y del footer a solicitud del Sr Ramos para máxima compacidad visual.
  5. Interfaz interactiva depurada a un único botón de participación (`sorteo_participar`), retirando botones secundarios de estado y tienda.
  6. Despacho verificado al canal `1552723526996336724` (Message ID: `1557173834527023145`).

## [2026-10-06] creator & discord | Módulo y Embed Interactivo de Sorteos (Giveaways)
- **Archivos Creados**: [`creator/output/discord/sorteo_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/sorteo_embed.json), [`creator/lab/discord_bot/sorteo_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/sorteo_embed.json), [`creator/lab/discord_bot/sorteo_manager.js`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/sorteo_manager.js).
- **Especificaciones Implementadas**:
  1. Contador de entradas en tiempo real reflejado directamente en el cuerpo del embed (`🎟️ Entradas registradas: X participantes`).
  2. Temporizador relativo nativo de Discord con cuenta atrás sincronizada (`<t:TIMESTAMP:R>`) y fecha completa (`<t:TIMESTAMP:F>`).
  3. Sistema de 3 tiers de premios (1er Lugar: Titán Permanente, 2do Lugar: Héroe, 3er Lugar: Llaves y monedas).
  4. Fila de componentes con botón verde de participación instantánea (`sorteo_participar`), botón de consulta de estado efímero (`sorteo_ver_estado`) y botón de tienda oficial.
  5. Módulo backend (`sorteo_manager.js`) con almacenamiento persistente de entries, control de duplicados y refresco dinámico del mensaje (`type: 7 UPDATE_MESSAGE`).
  6. Despacho en vivo verificado al canal `1552723526996336724` (Message ID: `1557144593517121696`).

## [2026-10-06] creator & discord | Embed de Instrucciones de Simple Voice Chat
- **Archivos Creados**: [`creator/output/discord/voicechat_setup_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/voicechat_setup_embed.json), [`creator/lab/discord_bot/voicechat_setup_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/voicechat_setup_embed.json).
- **Activo Local Respaldado**: [`creator/output/renders/voicechat_thumbnail.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/voicechat_thumbnail.png).
- **Especificaciones Implementadas**:
  1. Título y subtítulo en Small Caps bajo el estándar oficial de ThunderMC (`16706304`).
  2. Pasos de setup en 3 puntos (`1️⃣`, `2️⃣`, `3️⃣`) para Java 1.21+.
  3. Aclaración de Bedrock con derivación a canales de voz de Discord y cita blockquote con enlace a tutorial de YouTube.
  4. Thumbnail temático personalizado de micrófono y banner 16:9 (`campamento_dia_1138x640.jpg`).
  5. Botón interactivo de enlace (`type: 2`, `style: 5`) directo a la descarga en Modrinth con icono `📥`.
  6. Despacho verificado al canal `1552723526996336724` (Message ID: `1557143738583744552`).

## [2026-10-06] creator & discord | Roles de Notificaciones con Thumbnail de Campana
- **Archivos Modificados**: [`creator/output/discord/roles_notificaciones.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/roles_notificaciones.json), [`creator/lab/discord_bot/roles_notificaciones.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/roles_notificaciones.json).
- **Activo Local Respaldado**: [`creator/output/renders/roles_bell_thumbnail.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/roles_bell_thumbnail.png).
- **Especificaciones Implementadas**:
  1. Integración de propiedad `thumbnail` apuntando al PNG de campana transparente para el panel de roles.
  2. Imagen 16:9 inferior (`campamento_dia_1138x640.jpg`) preservada.
  3. Despacho verificado al canal `1552723526996336724` (Message ID: `1557138620748398612`).

## [2026-10-06] creator & discord | Menú Principal con Thumbnail de Brújula Transparente
- **Archivos Modificados**: [`creator/output/discord/menu_discord_thundermc.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/menu_discord_thundermc.json), [`creator/lab/discord_bot/menu_discord_thundermc.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/menu_discord_thundermc.json).
- **Activo Local Descargado**: [`creator/output/renders/minecraft_compass_transparent.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/minecraft_compass_transparent.png).
- **Especificaciones Implementadas**:
  1. Incorporación del campo `thumbnail` en el embed apuntando al render de brújula transparente.
  2. Imagen principal 16:9 preservada (`campamento_dia_1138x640.jpg`).
  3. Despacho en vivo verificado al canal `1552723526996336724` (Message ID: `1557138229407522918`).

## [2026-10-06] creator & discord | Embed de Compras Tebex con Botón de Enlace a Tienda Oficial
- **Archivo de Configuración**: [`creator/output/discord/tebex_purchase_embed.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/tebex_purchase_embed.json).
- **Servicio Receptor de Webhooks**: [`creator/lab/discord_bot/tebex_listener.js`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/tebex_listener.js).
- **Especificaciones Implementadas**:
  1. **Título Personalizado**: `🛒 ¡Nueva Compra de {player}!`.
  2. **Avatar Dinámico del Jugador (`thumbnail`)**: Integrado en la esquina superior derecha mediante CDN de cabezas de Minecraft (`https://mc-heads.net/avatar/{player}/100`), extrayendo automáticamente el render 2D con capas de la skin a partir del nickname.
  3. **Cuerpo del Embed**: Agradecimiento conciso (`¡Agradecemos enormemente el apoyo!` / `-# ɢʀᴀᴄɪᴀꜱ ᴘᴏʀ ʜᴀᴄᴇʀ ᴄʀᴇᴄᴇʀ ᴛʜᴜɴᴅᴇʀ`), detalles (`Comprador` y `Paquete`), IP en bloque de código limpio y pseudo-footer con enlaces.
  4. **Botón Interactivo (`type: 2`, `style: 5`)**: Botón URL en fila de componentes (`type: 1`) con etiqueta `"Click para ver la tienda oficial de ThunderMc"`, emoji `🪙` y destino `https://tienda.thundermc.es/`.
  5. **Imagen 16:9 Adjunta**: [`creator/output/renders/campamento_dia/campamento_dia_1138x640.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_1138x640.jpg).
  6. **Despacho Verificado**: Mensajes enviados al canal `1552723526996336724` (Simulación SrRamos: `1557133459129106494`, Plantilla Literal: `1557133485595033623`).

## [2026-10-06] wiki & discord | Estándar Oficial de Embeds Discord (Estilo Sr Ramos) + Selector de Roles
- **Documento Maestro de Estilo**: [`wiki/concepts/estandar_embeds_discord.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/wiki/concepts/estandar_embeds_discord.md).
- **Nuevo Entregable de Producción**: [`creator/output/discord/roles_notificaciones.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/roles_notificaciones.json).
- **Entorno de Laboratorio**: [`creator/lab/discord_bot/roles_notificaciones.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/roles_notificaciones.json).
- **Especificaciones Implementadas**:
  1. **Análisis Estilístico**: Compilación exhaustiva de reglas de diseño (Embeds tradicionales vs V2, paleta `16706304`, Small Caps en `-#`, viñetas con emojis en backticks, bloque de 1-click copy y menús `type: 3`).
  2. **Selector de Roles de Notificaciones**: Embed temático con 5 categorías de alertas (`Anuncios`, `Sorteos`, `Eventos/Keyalls`, `Actualizaciones`, `Estado`) con soporte multiselección (`min_values: 0`, `max_values: 5`).
  3. **Despacho Verificado**: Probado y validado en el canal `1552723526996336724` (Message ID: `1557117766572708013`).

## [2026-10-06] creator & discord | Menú Discord ThunderMC Definitivo (Embed Compacto + Desplegable + 1-Click Copy)
- **Entregable Oficial**: [`creator/output/discord/menu_discord_thundermc.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/discord/menu_discord_thundermc.json).
- **Entorno de Laboratorio**: [`creator/lab/discord_bot/menu_discord_thundermc.json`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/discord_bot/menu_discord_thundermc.json).
- **Activo Multimedia Integrado**: [`creator/output/renders/campamento_dia/campamento_dia_1138x640.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_1138x640.jpg) (1138×640 px, relación 16:9 optimizada para contenedor de imagen de embed de Discord).
- **Especificaciones Implementadas**:
  1. **Embed Estándar Bounded**: Ancho bloqueado a ~432 px, evitando el desbordamiento horizontal fluido de Components V2. Borde ámbar oficial (`16706304`).
  2. **Bloque de Copiado Directo 1-Clic**: IP del servidor formateada como bloque de código limpio (```` ```text \n thundermc.es \n ``` ````) con soporte para el botón flotante nativo de Discord (*Copy code*). Puerto Bedrock `19132` desacoplado en subtítulo para no ensuciar el portapapeles. Etiqueta de versión fijada a `(Version 1.21.1+  )`.
  3. **Dashboard Interactivo**: Fila de componentes con selector de cadenas (`string_select`, `menu_principal`) con 4 opciones (`Anuncios`, `Normativa`, `Soporte`, `Tienda`).
  4. **Barra de Enlaces Oficiales**: Subtítulos de acceso rápido a Tienda Web, TikTok y YouTube reubicados al pie del Dashboard.
  5. **Despacho Verificado**: Validado y enviado al canal de pruebas `1552723526996336724` (Message ID: `1557126084984836126`).

- **Módulo**: [`creator/lab/renders/menu_principal_taberna/menu_principal_taberna_4.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/menu_principal_taberna/menu_principal_taberna_4.md).
- **Referencia Extraída**: [`creator/lab/renders/menu_principal_taberna/crop_valyr_campamento.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/menu_principal_taberna/crop_valyr_campamento.jpg).
- **Especificaciones Compiladas**:
  1. **Alineación Visual del Casco**: Extracción técnica de la máscara del yelmo de `campamento_dia_final.jpg` (barra nasal vertical entre los ojos, visera horizontal frontal y ranuras de ventilación rectangulares).
  2. **Inclinación de Cabeza**: Valyr con la mirada y la cabeza dirigidas en ángulo descendente hacia el mapa de campaña sobre la mesa.
  3. **Estado Operativo**: Prompt maestro afinado y registrado en espera del restablecimiento de la ventana de cuota del motor de render (`gemini-3.1-flash-image` ~20:28 UTC).


## [2026-10-06] creator & renders | Render Cinemático AAA: Menú Principal — Valyr Frontal en Primer Plano (4K UHD)
- **Módulo**: [`creator/lab/renders/menu_principal_taberna/menu_principal_taberna_3.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/menu_principal_taberna/menu_principal_taberna_3.md), [`creator/output/renders/menu_principal_taberna/menu_principal_taberna_final.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/menu_principal_taberna/menu_principal_taberna_final.jpg).
- **Resolución**: **3840 × 2160 (4K UHD)** a calidad 100%.
- **Propósito**: Encabezado visual definitivo para el Menú Principal de la comunidad en Discord (`discord_bot/menu_principal_v2.json`) y portales oficiales.
- **Ajustes Críticos de la Iteración**:
  1. **Encuadre Cercano (Zoom)**: Cámara en plano medio corto; mesa de planificación con mapa y brújula dominando el primer plano sin espacio residual vacío en el suelo.
  2. **Valyr en Posición Rigurosamente Frontal**: Centrado exacto, mirando de frente a cámara mientras apunta al centro del mapa con su dedo.
  3. **Corrección de Casco y Armadura Canónica**: Casco de hierro canónico abierto de Minecraft (enmarcando el rostro rosado sin bloquearlo ni deformarlo), peto de acero limpio sin tabardo ni rayo en el pecho, y capa de Thunder en la espalda.
  4. **Compañeros y Fondo**: Arquera a la izquierda y guerrero a la derecha estrechamente integrados en la mesa; chimenea crepitante y estandarte oficial de Thunder alineado en el eje central.





## [2026-10-06] creator & renders | Render Cinemático AAA: Campamento Diurno (Iluminación Cálida Dark Fantasy 4K)
- **Módulo**: [`creator/lab/renders/campamento_dia/campamento_dia_dark_fantasy_1.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/campamento_dia/campamento_dia_dark_fantasy_1.md), [`creator/output/renders/campamento_dia/campamento_dia_dark_fantasy_1.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_dark_fantasy_1.jpg).
- **Resolución**: **3840 × 2160 (4K UHD)** a calidad 100%.
- **Transformación Lumínica Ejecutada**:
  1. **Supresión de Luz Plana**: Reemplazada la iluminación blanca difusa por un esquema direccional rasante cálido (*golden-amber god rays*) que corta la bruma forestal.
  2. **Atmósfera Dark Fantasy**: Bosque de abetos profundo y sombrío con fuerte claroscuro. La fogata y farolillos cobran fuerza con brasas flotantes y resplandor anaranjado acogedor.
  3. **Identidad y Composición Preservadas**: Estandarte oficial de Thunder con rayo dorado, cerdo caballero con casco liso y capa discreta comiendo zanahoria, arquero, cocinero y líder con mapa intactos.


## [2026-10-06] creator & renders | Render Cinemático AAA: Campamento Diurno Final (Resolución 4K UHD — 3840×2160)
- **Módulo**: [`creator/lab/renders/campamento_dia/campamento_dia_final.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/campamento_dia/campamento_dia_final.md), [`creator/output/renders/campamento_dia/campamento_dia_final.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_final.jpg).
- **Resolución**: **3840 × 2160 (4K UHD Nativo Remasterizado)** a calidad JPEG 100%.
- **Optimización Crítica de Nitidez**:
  1. **Eliminación de Degradación Iterativa**: Generación pura desde cero en un único pase para recuperar la textura microscópica de maderas, agujas de pino y metal PBR sin artefactos acumulados.
  2. **Pipeline 4K**: Escalado de alta precisión en .NET/GDI+ con remuestreo bicúbico fino.
  3. **Identidad**: Cerdo caballero con yelmo de hierro pulido (sin penacho), capa discreta de Thunder y estandarte del rayo dorado en el campamento.


## [2026-10-06] creator & renders | Render Cinemático AAA: Campamento Diurno v4 & Final (Capa Discreta y Pulido Definitivo)
- **Módulo**: [`creator/lab/renders/campamento_dia/campamento_dia_4.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/campamento_dia/campamento_dia_4.md), [`creator/output/renders/campamento_dia/campamento_dia_final.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_final.jpg).
- **Ajustes Críticos**:
  1. **Capa Discreta**: Sustituida la capa voluminosa por una capa clásica delgada y rectangular de Minecraft en azul marino oscuro, cayendo recta ceñida a la espalda de la armadura.
  2. **Activo Final Generado**: Consolidado como `campamento_dia_final.jpg` (9.9/10).


## [2026-10-06] creator & renders | Render Cinemático AAA: Campamento Diurno v3 (Capa Thunder + Encuadre Limpio)
- **Módulo**: [`creator/lab/renders/campamento_dia/campamento_dia_3.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/campamento_dia/campamento_dia_3.md), [`creator/output/renders/campamento_dia/campamento_dia_3.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_3.jpg).
- **Estándar Creado**: [`creator/lab/renders/estandar_marca_insignia_thunder.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/estandar_marca_insignia_thunder.md) y actualizado en [`creator/lab/renders/README.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/README.md).
- **Ajustes Críticos**:
  1. **Encuadre**: Suprimido el bloque elevado en la esquina inferior izquierda; primer plano abierto y limpio sobre césped plano natural.
  2. **Diseño de Mascota**: Eliminado el penacho del yelmo (ahora hierro sobrio pulido) e incorporada la capa azul marino de Thunder con ribete dorado.
  3. **Insignia Diegética**: Estandarte oficial de Thunder (`minecraft:banner`) con rayo dorado sobre fondo azul marino ondeando en el campamento.
- **Evaluación**: Puntuación 9.8/10. Activo definitivo pulido y normalizado.


## [2026-10-06] creator & renders | Render Cinemático AAA: Campamento Diurno v2 (Corrección Bug de Cofre + Insignia Thunder)
- **Módulo**: [`creator/lab/renders/campamento_dia/campamento_dia_2.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/campamento_dia/campamento_dia_2.md), [`creator/output/renders/campamento_dia/campamento_dia_2.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_2.jpg).
- **Correcciones Críticas Realizadas**:
  1. **Bug Resuelto**: Eliminado el cofre doble alargado y roto del primer plano inferior izquierdo; sustituido por césped natural con flores silvestres y cofre regular con farolillo.
  2. **Insignia Oficial de Marca Thunder**: Introducido el estandarte canónico de Minecraft con el rayo dorado sobre fondo azul marino oscuro en el campamento, y el penacho dorado en el yelmo del cerdo caballero.
- **Evaluación**: Puntuación 9.6/10. Activo depurado y representativo de la identidad oficial de ThunderMC.


## [2026-10-06] creator & renders | Prueba de Render Aislado: Cerdo Caballero Desafiante & Estándar Facial
- **Módulos**:
  - Estándar: [`wiki/concepts/estandar_expresiones_faciales_renders.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/wiki/concepts/estandar_expresiones_faciales_renders.md)
  - Lab: [`creator/lab/renders/cerdo_caballero_desafiante/cerdo_caballero_desafiante_1.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/cerdo_caballero_desafiante/cerdo_caballero_desafiante_1.md)
  - Activo: [`creator/output/renders/cerdo_caballero_desafiante/cerdo_caballero_desafiante_1.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/cerdo_caballero_desafiante/cerdo_caballero_desafiante_1.jpg)
- **Especificaciones**:
  1. **Rig Facial**: Implementación del estándar basado en `@enderframes` (cejas extruidas asimétricas, párpados con corte diagonal, mirada lateral y hendidura de sonrisa/smirk en el hocico).
  2. **Composición**: Render puro de personaje sobre ciclorama neutro de estudio (sin escenario de fondo), con espada al hombro y postura a 3/4.
  3. **Evaluación y Feedback Sr Ramos**: Veredicto: No convence estéticamente. Se archiva como prueba latente en memoria para consulta bajo demanda sin aplicarlo por defecto.

## [2026-10-06] creator & renders | Render Cinemático AAA: Campamento Diurno de Expedición (4 Personajes)
- **Módulo**: [`creator/lab/renders/campamento_dia/campamento_dia_1.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/campamento_dia/campamento_dia_1.md), [`creator/output/renders/campamento_dia/campamento_dia_1.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/campamento_dia/campamento_dia_1.jpg).
- **Referencia Base**: Ingestada desde `C:\Users\PC\Downloads\52f679758f750330ba547c3d54a7265d.jpg` a [`creator/raw/references/referencia_campamento.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/raw/references/referencia_campamento.jpg).
- **Especificaciones**:
  1. **Composición y Entorno**: Campamento de expedición con 3 tiendas de campaña medievales, fogata central con caldero, cofres, farolillos y bosque de abetos bañado por rayos de sol volumétricos (*god rays*).
  2. **Delimitación de 4 Personajes en Acción**: Cerdo caballero comiendo zanahoria en tronco, arquero con capucha ajustando arco, cocinero en fogata con cuchara y guerrero leyendo mapa en barril.
  3. **Puntaje Estimado**: 9.2/10. Composición equilibrada, iluminación diurna cálida y limpia, sin ruido ni micro-voxels.


## [2026-10-06] creator & renders | Render Cinemático AAA: Cerdo Caballero en Barca (Cueva Dark Fantasy)
- **Módulo**: [`creator/lab/renders/cerdo_barca_cueva/cerdo_barca_cueva_1.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/cerdo_barca_cueva/cerdo_barca_cueva_1.md), [`creator/output/renders/cerdo_barca_cueva/cerdo_barca_cueva_1.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/cerdo_barca_cueva/cerdo_barca_cueva_1.jpg).
- **Referencia Base**: Ingestada desde `C:\Users\PC\Downloads\171c8ee0fa3d8631324c5441b33f1795.jpg` a [`creator/raw/references/referencia_barca_cueva.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/raw/references/referencia_barca_cueva.jpg).
- **Especificaciones**:
  1. **Composición 16:9**: Adaptación del plano de navegación subterránea a cueva Dark Fantasy.
  2. **Personaje**: Bebé cerdo caballero con proporciones canónicas (cabeza cúbica grande, orejas caídas), armadura de hierro cúbica a medida y espada en el interior de la barca de roble.
  3. **Iluminación**: Esquema de claroscuro donde la antorcha sostenida en alto actúa como key-light principal, proyectando reflejos cálidos ámbar en el agua y sombras profundas en el abismo de la caverna.
- **Evaluación**: Puntuación preliminar 8.8/10. Activo generado sin artefactos, listo para revisión del Sr Ramos.


## [2026-10-05] dev & packet-anim | HeadAnimator v1.2.1 — Normalización Forzada a Fotograma Base (Frame 0) en Inventario y Desequipamiento (Sandbox)
- **Módulo**: `creator/lab/head_animator/`, `creator/output/plugins/HeadAnimator-1.0.0.jar`, Servidor Sandbox (`ymykh9qy.274758bd`).
- **Diagnóstico de Causa Raíz**:
  1. Al despachar `sendEquipmentChange` al propio jugador (render F5), el cliente Minecraft local actualiza su array de armadura (`inventory.armor.set(3, frame)`).
  2. Cuando el jugador retira el casco de la ranura (mediante clic, arrastre o shift-click en Survival o Creative), el cliente enviaba el fotograma que estuviese renderizando en ese instante (Frame 1 o Frame 2), corrompiendo la textura estática en el inventario.
  3. No existía ninguna rutina de saneamiento que forzara la restitución del ítem base al salir de la ranura de casco.
- **Solución Técnica Implementada**:
  1. **Método `normalizeToBase(ItemStack)` ([`HeadAnimation.java`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/head_animator/src/com/thunderstudios/headanimator/HeadAnimation.java))**: Compara el UUID del perfil NBT con el UUID determinista de Frame 0. Si difiere, reescribe el `PlayerProfile` y metadatos con el fotograma base precalculado en memoria sin costo de red ni recreación de objetos.
  2. **Invariante en Tick Loop ([`AnimationManager.java`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/head_animator/src/com/thunderstudios/headanimator/AnimationManager.java))**: El ítem real almacenado en el inventario del jugador en la ranura de casco se normaliza a Frame 0 en cada ciclo; la animación es 100% virtual vía paquetes. Al desequipar, se invoca `normalizePlayerInventory`.
  3. **Suite de Listeners Reactivos ([`HeadListener.java`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/head_animator/src/com/thunderstudios/headanimator/HeadListener.java))**:
     - `InventoryClickEvent` & `InventoryCreativeEvent`: Sanean en tiempo real el cursor y el ítem clickeado, programando un pase diferido y forzando `player.updateInventory()`.
     - `PlayerArmorChangeEvent` & `InventoryCloseEvent`: Detección instantánea de retirada del casco para normalizar todo el inventario.
     - `PlayerDropItemEvent`, `EntityPickupItemEvent` & `PlayerDeathEvent`: Blindaje total para que las cabezas en el suelo o tras morir siempre tengan textura Frame 0.
     - `BlockPlaceEvent`: Cancela la colocación en suelo para evitar la destrucción del PDC NBT.
     - `PlayerInteractEntityEvent`: Bloquea colocación en Armor Stands o Item Frames.
- **Despliegue Remoto**:
  - Compilado nativamente en Java 21 contra Paper 1.21.11 API.
  - Empaquetado y subido `HeadAnimator-1.0.0.jar` vía SFTP al directorio `/plugins/` del Sandbox.


## [2026-10-05] events & architecture | Compilación y Persistencia del Modelo de Evento de Temporada (Síntesis Wiki)
- **Módulo**: [`wiki/synthesis/modelo-evento-temporada-thundermc.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/wiki/synthesis/modelo-evento-temporada-thundermc.md), [`index.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/index.md).
- **Contenido Persistido**:
  1. **Core Loop**: Mapeo visual y funcional del ciclo de retención (Pase de Batalla + Bosses 1h/24h + KOTH $\rightarrow$ Tokens $\rightarrow$ Cajas, Runa y Altar).
  2. **Prompts Especializados de Agentes**: 4 directivas maestras para *Systems & Economy Designer*, *Combat & Encounter Designer*, *Minecraft Technical Lead* y *LiveOps & Monetization Lead*.
  3. **Matriz de Red Teaming (8 Fallas Fatales)**: Diagnóstico y mitigaciones técnicas obligatorias (Soft-Cap diario de tokens, límites semanales anti-arbitraje, sustitución de adds por pilares para proteger el MSPT a < 40 ms, loot instanciado por tiers de daño, validación atómica NBT en ExecutableItems, ventanas Prime Time en KOTH, balance dual PvE/PvP y persistencia SQL).
  4. **Blueprint del Hito Comunitario (El Altar de la Falla)**: Dinámica de donaciones con incentivo dual (recompensas personales Top 1-10 + desbloqueo progresivo en 4 fases globales).
  5. **Modelo de Monetización Ética (Rating 8.5/10)**: Estructura de BattlePass freemium, skips de nivel, boosters globales solidarios y Pity System garantizado a 20 aperturas.

## [2026-10-03] dev & packet-anim | HeadAnimator v1.2.0 — Arquitectura Híbrida PacketEvents + Interceptor de Movimiento (Sandbox)
- **Módulo**: `creator/lab/head_animator/`, `creator/output/plugins/HeadAnimator-1.0.0.jar`, Servidor Sandbox (`ymykh9qy.274758bd`).
- **Diagnóstico y Corrección de Causa Raíz**:
  1. **Enfoque Exclusivo en Ranura de Casco (`HELMET`)**: Según la especificación directa del Sr Ramos, el sistema se enfoca al 100% en la cabeza equipada como casco (vista externa y F5), eliminando la sobrecarga y mutaciones innecesarias del inventario local.
  2. **Interceptor de Salida PacketEvents (`PacketListenerAbstract`)**: En Paper 1.21, cada movimiento, salto o giro del jugador fuerza al `EntityTrackerEntry` del servidor a despachar un paquete `ENTITY_EQUIPMENT` con el ítem real del inventario. El listener intercepta en tiempo real estos paquetes y sobreescribe de forma transparente el slot `HELMET` con el fotograma animado activo (`SpigotConversionUtil.fromBukkitItemStack`). Esto elimina por completo el bug de congelación o desincronización al caminar.
  3. **Caché Determinista en OpenGL**: Cada fotograma precalcula un `PlayerProfile` con UUID y nombre fijos (`Bukkit.createProfile(uuid, name)`). El cliente de Minecraft descarga la textura una sola vez y conmuta los fotogramas en memoria GPU instantáneamente sin saturar la caché ni invocar Mojang CDN.
  4. **Emisión Periódica Dual (F5 y Espectadores)**: Tarea programada a **10 ticks** (0.5s / 2 FPS) con ciclo Ping-Pong suave (`0 ➔ 1 ➔ 2 ➔ 1 ➔ 0`). Despacha `sendEquipmentChange` tanto al propio jugador (render en F5) como a todos los observadores en un radio de 48 bloques.
  5. **Comando `/ha debug`**: Telemetría in-game mejorada que muestra el estado en vivo del casco, el registro en `activeWearers` y el fotograma actual que se está emitiendo.
- **Despliegue Remoto**:
  - Compilado nativamente en Java 21 contra Paper 1.21.11 y PacketEvents 2.13.0.
  - Subido JAR y `config.yml` vía SFTP a Sandbox.


## [2026-10-03] dev & packet-anim | Creación, Compilación y Despliegue de HeadAnimator v1.0.0 (Sandbox)
- **Módulo**: `creator/lab/head_animator/`, `creator/output/plugins/HeadAnimator-1.0.0.jar`, Servidor Sandbox (`ymykh9qy.274758bd`).
- **Arquitectura Técnica Implementada (Hypixel Stop-Motion Pattern)**:
  - **Zero Database / Zero Heap Alloc**: Las texturas Base64 se pre-generan en memoria al arrancar; el bucle de ticks no asigna objetos nuevos.
  - **Zero Cursor Glitch**: El inventario real del jugador no se modifica jamás. El cambio de textura se despacha virtualmente vía `player.sendEquipmentChange(EquipmentSlot.HEAD)` a observadores en un radio configurable de 24 bloques y al propio jugador (render F5 en tercera persona).
  - **Cráneo de Slimer Animado (`slimer`)**: 4 fotogramas Base64 secuenciales a 5 ticks (4 FPS) con lore y estética oficial de la temporada Ecto-Alien.
- **Despliegue Remoto**:
  - Compilado nativamente en Java 21 contra Paper 1.21.11 API.
  - Subido `HeadAnimator-1.0.0.jar` a `/plugins` en el servidor Sandbox vía SFTP. Servidor Survival mantenido en solo lectura intacto.

## [2026-10-03] crates & effects | Configuración Cromática y Escala de Partículas Espirales (Tiers Super a Divina) (Sandbox)
- **Módulo**: `plugins/ExcellentCrates/crates/` (`vote.yml`, `rara.yml`, `consumibles.yml`, `mitica.yml`, `limitada.yml`), Servidor Sandbox (`ymykh9qy.274758bd`).
- **Implementación Técnica Directa (NightCore UniParticle / DUST)**:
  - **Caja Super (`vote.yml`)**: `Model: spiral`, `Particle: DUST`, `Color: 75, 253, 0` (Verde lima fino, `Size: 0.6`, `Enabled: true`).
  - **Caja Rara (`rara.yml`)**: `Model: spiral`, `Particle: DUST`, `Color: 0, 141, 255` (Azul fino, `Size: 0.6`, `Enabled: true`).
  - **Caja Épica (`consumibles.yml`)**: `Model: spiral`, `Particle: DUST`, `Color: 168, 78, 222` (Morado fino, `Size: 0.6`, `Enabled: true`).
  - **Caja Mítica (`mitica.yml`)**: `Model: spiral`, `Particle: DUST`, `Color: 208, 38, 38` (Rojo medio, `Size: 1.0`, `Enabled: true`).
  - **Caja Divina (`limitada.yml`)**: `Model: spiral`, `Particle: DUST`, `Color: 255, 230, 0` (Amarillo oro grueso, `Size: 1.5`, `Enabled: true`).
- **Despliegue Remoto**:
  - Actualizados localmente y subidos vía SFTP al servidor Sandbox. Servidor Survival mantenido en solo lectura intacto.

## [2026-10-02] crates & ui | Unificación de Previews para Todas las Calidades de ExcellentCrates (Estándar Mítico)
- **Archivos Diseñados y Desplegados**:
  1. [`creator/output/previews/super.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/super.yml) / [`vote.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/vote.yml) ▶ Tier Super / Vote (`minecraft:lime_stained_glass_pane`, `&0&l|&r &0Preview &0▶ &8Super &e⭐&7⭐⭐⭐⭐`).
  2. [`creator/output/previews/rara.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/rara.yml) ▶ Tier Rara (`minecraft:light_blue_stained_glass_pane`, `&0&l|&r &0Preview &0▶ &8Rara &e⭐⭐&7⭐⭐⭐`).
  3. [`creator/output/previews/epica.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/epica.yml) / [`consumibles.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/consumibles.yml) ▶ Tier Épica / Consumibles (`minecraft:purple_stained_glass_pane`, `&0&l|&r &0Preview &0▶ &8Epica &e⭐⭐⭐&7⭐⭐`).
  4. [`creator/output/previews/mitica.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/mitica.yml) ▶ Tier Mítica (`minecraft:red_stained_glass_pane`, `&0&l|&r &0Preview &0▶ &8Mitica &e⭐⭐⭐⭐&7⭐`).
  5. [`creator/output/previews/divina.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/divina.yml) / [`limitada.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/limitada.yml) ▶ Tier Divina / Limitada (`minecraft:yellow_stained_glass_pane`, `&0&l|&r &0Preview &0▶ &8Divina &e⭐⭐⭐⭐⭐`).
  6. [`creator/output/previews/slime.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/previews/slime.yml) ▶ Crate Temática Slime (`minecraft:green_stained_glass_pane`, `&0&l|&r &0Preview &0▶ &8Slime`).
- **Implementación Técnica**:
  - Propagada la arquitectura gráfica de 54 slots (9x6) tomada de la preview mítica diseñada por el Sr Ramos: 20 slots centrales para recompensas, 8 cristales teñidos de calidad flanqueando los premios en slots `10,16,19,25,28,34,37,43`, marco perimetral gris exterior y controles de navegación en fila 6.
  - Actualizados los archivos de caja en Sandbox (`rara.yml`, `vote.yml`, `consumibles.yml`, `limitada.yml`, `slime.yml`) para vincular sus respectivos `Preview.Id`.
- **Despliegue Remoto**:
  - Sincronizados todos los archivos YAML en `plugins/ExcellentCrates/previews/` y `plugins/ExcellentCrates/crates/` del servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP. Servidor Survival mantenido intacto.

## [2026-10-02] items & mechanics | Bolsita Súper v5.1 — Fix Definitivo con Condición Nativa ifSneaking (Bukkit API)
- **Diagnóstico Comparativo con Cajitas Existentes (`cajitacomun.yml`)**:
  - Se auditó la configuración de las cajitas del servidor (`cajitacomun`, `cajitaepica`, `cajitalegendaria`) y se constató que la detección de agachado en ExecutableItems se implementa nativamente en `playerConditions:` mediante `ifSneaking: false` e `ifSneaking: true`.
  - El uso de `placeholdersConditions:` con `%player_sneaking%` fallaba al comparar cadenas o al evaluar condiciones de tipo asíncrono en Folia/Paper, provocando que el evento de clic no disparara ningún activador.
- **Implementación Aplicada en [`bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml)**:
  - `activator1` (Apertura ordinaria): `playerConditions.ifSneaking: false`. Ejecuta sin intermediarios la animación de 5s y el MEGA-RANDOM de exclusividad mutua.
  - `activator2` (Preview DeluxeMenus): `playerConditions.ifSneaking: true`. Ejecuta `dm open preview_bolsa_super %player%` con `usageModification: 0`.
  - Eliminado por completo el bloque `placeholdersConditions: {}`.
- **Sincronización Remota**: Subido y verificado en Sandbox (`ymykh9qy.274758bd`).

## [2026-10-02] items & deluxemenus | Bolsita Súper v5.0 — Restauración de Apertura Robusta + Preview en DeluxeMenus GUI
- **Causa Raíz de Bloqueo Previo**:
  - Las condiciones de piedad matemática en `activator_pity` y `activator_normal` fallaban cuando la variable no estaba instanciada en memoria con un número válido, bloqueando simultáneamente ambos activadores y dejando el ítem inoperativo.
- **Solución y Mejoras Aplicadas**:
  1. **Apertura Robusta Restablecida (`activator1`)**:
     - Eliminada la bifurcación condicional frágil.
     - Se mantiene el sistema **MEGA-RANDOM de exclusividad mutua** (98 pesos para Mejoras de calidad + 902 pesos para Aperturas ordinarias + 2% Jackpot independiente).
     - Comando de llave corregido a `/crates key give %player% super 1`.
  2. **Preview vía DeluxeMenus (`activator2` — Shift + Clic)**:
     - Creado menú GUI: [`creator/lab/preview_bolsa_super.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/preview_bolsa_super.yml) desplegado en `plugins/DeluxeMenus/gui_menus/menusIA/preview_bolsa_super.yml`.
     - Registrado en `plugins/DeluxeMenus/config.yml` bajo la clave `preview_bolsa_super`.
     - Diseño limpio de 27 slots: Nether Star (Mejoras de calidad con % exactos), Girasol (Fase I Efectivo), Cofre (Fase II Consumibles), Gancho brillante (Jackpot Crate Súper) y Barrera para cerrar con sonido de clic.
     - Cero spam en el chat; el ítem ejecuta directamente `dm open preview_bolsa_super %player%` con `usageModification: 0`.
- **Sincronización Remota**: Subidos y verificados vía SFTP los 3 archivos en el Sandbox (`ymykh9qy.274758bd`).

## [2026-10-02] items & mechanics | Bolsita Súper v4.1 — Pity System 100% Silencioso e Interno (Bugfixes de Sintaxis)
- **Diagnóstico en Logs (`logs/latest.log`)**:
  1. *Fallo de Comparadores*: `GREATER_OR_EQUALS` no es un comparador válido en ExecutableItems (requiere `SUPERIOR_OR_EQUALS` / `INFERIOR`) y faltaba `type: PLAYER_NUMBER` / `type: PLAYER_STRING`. Esto provocaba que `activator_pity` se ejecutase siempre.
  2. *Fallo de Comando SCore*: El comando `/score variable-modification` no existe en esta versión de SCore; el comando soportado es `/score variables-define <variable> <player> <value>`.
  3. *Fallo de Sintaxis en Crates*: `crates key give crate_super %player% 1` intentaba otorgar a un jugador inexistente; la sintaxis de ExcellentCrates es `/crates key give %player% super 1`.
- **Modificaciones Aplicadas en [`bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml)**:
  - **100% Invisible**: Eliminadas todas las menciones a piedad en títulos, subtítulos, chat y visor de loot (`Shift+Clic`). La piedad se camufla como un Jackpot ordinario al 100%.
  - **Reinicio Garantizado**: `/score variables-define pity_bundle_super %player% 0` al saltar Jackpot (natural o por piedad).
  - **Incremento Matemático PAPI**: `/score variables-define pity_bundle_super %player% %math_0_{score_variables_pity_bundle_super}+1%` en cada apertura sin Jackpot.
- **Sincronización Remota**: Subido y verificado en Sandbox (`ymykh9qy.274758bd`).

## [2026-10-02] items & mechanics | Bolsita Súper v4.0 — Implementación del Sistema de Piedad (Pity System 25x)
- **Módulos y Variables Creados/Desplegados**:
  - Variable SCore: [`creator/lab/pity_bundle_super.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/pity_bundle_super.yml) desplegada en `plugins/SCore/variables/pity_bundle_super.yml`.
  - Módulo EI: [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml) desplegado en `plugins/ExecutableItems/items/ThunderMC/`.
- **Mecánica del Pity System (25 aperturas)**:
  1. **Contador Persistente**: `%score_variables_pity_bundle_super%` almacena los intentos fallidos sin Jackpot por jugador.
  2. **Activador Condicional de Piedad (`activator_pity`)**: Se dispara si el contador alcanza `>= 24`. Otorga animación completa, dinero garantizado (\$1.200), consumible garantizado (`vialdealmas`), **Llave Crate Súper garantizada (100%)** y resetea el contador a `0`.
  3. **Activador Estándar (`activator_normal`)**: Opera si el contador es `< 24`. Si toca el 2% de Jackpot natural, entrega la llave y resetea a `0`. Si falla (98%), suma `+1` a la variable del jugador.
  4. **Visor de Loot Dinámico (`activator_loot`)**: Muestra en tiempo real el progreso exacto del jugador (`%score_variables_pity_bundle_super%/25`).
  5. **Corrección de ID Real**: `vial_de_almas` actualizado a `vialdealmas` tras auditar los ítems reales del servidor.
- **Sincronización Remota**: Ambos archivos subidos y validados vía SFTP en el Sandbox (`ymykh9qy.274758bd`). Verificación exitosa.

## [2026-10-02] items & mechanics | Propagación Suite Completa: MEGA-RANDOM, 2 Fases, Jackpot y Visor de Loot
- **Módulos Actualizados**:
  - [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml)
  - [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml)
  - [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml)
  - [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml)
- **Implementación Arquitectural en los 4 Tiers**:
  1. **Mutua Exclusión (Mejora vs Recompensas)**: La mejora de calidad opera como outcome exclusivo antes de abrir, resolviendo en entrega de bolsa superior sin quemar fases de recompensa.
  2. **Secuencia de Subtítulos de Apertura**:
     - `t=0s`: Sonido `entity.zombie.break_wooden_door` + Título "¡Bolsita Abierta!" + Subtítulo "ᴘʀᴇᴍɪᴏꜱ ʀᴇᴄɪʙɪᴅᴏꜱ".
     - `t=1s`: Subtítulo se actualiza con monto en efectivo + sonido `experience_orb.pickup`.
     - `t=2.2s`: Subtítulo se actualiza con consumible en small-caps + sonido `block.chest.open`.
     - `t=2.7s`: Bloque `SEND_MESSAGE` con resumen integral de botín impreso al final en el chat.
  3. **Jackpot Independiente**: Ejecución posterior con porcentajes escalados: Rara (3%), Épica (4%), Mítica (5%), Divina (7%).
  4. **Visor de Loot In-Game (Activador 2)**: Shift + Clic derecho (`%player_sneaking% = true`), `usageModification: 0` y tabla descriptiva completa en chat.
- **Sincronización Remota**: Los 4 archivos fueron transferidos vía SFTP al Sandbox (`ymykh9qy.274758bd`) bajo `plugins/ExecutableItems/items/ThunderMC/`. Verificación exitosa.

## [2026-10-02] items & mechanics | Bolsita Súper v3.0 — Arquitectura 2 Fases + Jackpot + Visor de Loot
- **Módulo Actualizado**: [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml)
- **Nueva Arquitectura (3 bloques RANDOM RUN secuenciales)**:
  1. **Fase I — Dinero** (garantizado): `$800` (50%) / `$1.200` (35%) / `$1.500` (15%)
  2. **Fase II — Consumible** (garantizado): `Vial de Almas` (40%) / `Kit Súper` (35%) / `4x Manzana de Oro` (25%)
  3. **Jackpot** (2%): `Llave Crate Súper` — bloque independiente 2/98
  4. **Mejora de Calidad** (preservado): Rara/Épica/Mítica/Divina según pesos originales (50/28/15/5/902)
- **Visor de Loot (Activador 2 — Shift+Clic)**:
  - Condición: `%player_sneaking% = true` vía PAPI
  - `usageModification: 0` — no consume el ítem
  - Muestra tabla completa en chat con todas las fases, porcentajes y nota informativa
  - Cooldown de 1s para evitar spam
- **Lore Actualizado**: Añadida línea `&8▶ ꜱʜɪꜰᴛ+ᴄʟɪᴄᴋ - ᴠᴇʀ ʟᴏᴏᴛ`
- **IDs de Ejemplo** (reemplazar con IDs reales): `vial_de_almas`, `kit_super`, `crate_super`
- **Sincronización Remota**: Desplegado en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_super_test.yml` en Sandbox (`ymykh9qy.274758bd`). Verificación exitosa.



## [2026-10-01] items & balance | Eliminación de Bolsa Limited y Adaptación Cromática de '¡Bolsita Abierta!' por Calidad
- **Eliminación Canónica de Tier Limited**:
  - Eliminado localmente y en servidor Sandbox: `bundle_recompensas_limited_test.yml`.
  - Purgadas todas las referencias de mejora y lores a Limited (`&#5489FF➠ &fLimited (2%)`) en los 5 módulos restantes.
  - Purgados los triggers de jackpot correspondientes (`2:LOOP START: ... ei give %player% bundle_recompensas_limited_test 1 ...`).
  - **Bolsa Divina** formalizada como la cúspide de progresión: encabezado de lore actualizado a `&8★ ¡ᴄᴀʟɪᴅᴀᴅ ᴍÁxɪᴍᴀ! ★` con lista completa de calidades superadas en tachado.
- **Adaptación Cromática de Títulos al Abrir (Códigos Vanilla Legacy)**:
  - El comando `/title` de Minecraft vanilla no procesa colores en formato HEX (`&#HEX`), por lo que se ajustaron a códigos de color legacy correspondientes a cada tier:
    - Súper: `&a¡Bolsita Abierta!`
    - Rara: `&b¡Bolsita Abierta!`
    - Épica: `&d¡Bolsita Abierta!`
    - Mítica: `&4¡Bolsita Abierta!`
    - Divina: `&e¡Bolsita Abierta!`
- **Sincronización Remota**: Archivo limited eliminado vía SFTP y los 5 módulos actualizados (`super`, `rara`, `epica`, `mitica`, `legend`) desplegados en `plugins/ExecutableItems/items/ThunderMC/` en Sandbox (`ymykh9qy.274758bd`). Verificación exitosa.

## [2026-10-01] items & ui | Estandarización de Subtítulo de Título 'ᴘʀᴇᴍɪᴏꜱ ʀᴇᴄɪʙɪᴅᴏꜱ' y Partículas de Tótem al Abrir
- **Módulos YAML Actualizados (Suite de 6 Bolsitas)**:
  1. [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml)
  2. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml)
  3. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml)
  4. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml)
  5. [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml)
  6. [`creator/lab/bundle_recompensas_limited_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_limited_test.yml)
- **Modificaciones de Feedback Visual**:
  - Subtítulo unificado al momento de apertura: `title %player% subtitle "&fᴘʀᴇᴍɪᴏꜱ ʀᴇᴄɪʙɪᴅᴏꜱ"` propagado a todos los outcomes estándar (reemplaza la lista redundante en el subtitle).
  - Partículas de apertura: agregado `PARTICLE TOTEM 25 0.4 0.4` sincronizado con las partículas existentes al revelar el botín.
- **Sincronización Remota**: Subidos los 6 archivos a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox (`ymykh9qy.274758bd`). Verificación exitosa.

## [2026-10-01] mythicmobs & eventos | Mob de Evento Halloween: Fantasma Viscoso (Slimer) con Vuelo Allay
- **Módulos Creados y Promocionados a Producción**:
  - Mob definitivo: [`creator/output/configs/MythicMobs/fantasma_halloween.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/configs/MythicMobs/fantasma_halloween.yml)
  - Ítems definitivos: [`creator/output/configs/MythicMobs/fantasma_items_halloween.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/configs/MythicMobs/fantasma_items_halloween.yml)
  - Desplegado en Sandbox: `plugins/MythicMobs/mobs/fantasma.yml` y `plugins/MythicMobs/items/fantasma_items.yml`.
- **Documentación Wiki y Memoria**:
  - Creada documentación oficial: [`wiki/entities/thundermc/evento-halloween-mobs.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/wiki/entities/thundermc/evento-halloween-mobs.md).
  - Vinculación permanente de término operativo: la expresión *"evento de halloween mobs"* queda indexada formalmente para referirse a este mob y su arquitectura técnica.
  - Actualizado [`index.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/index.md).
- **Especificaciones Técnicas Validadas**:
  - Arquitectura bi-entidad: Bebé Zombie jinete con invisibilidad en cuerpo montado sobre un Allay invisible/invulnerable (`Fantasma_Vuelo`).
  - Vuelo tridimensional nativo a altura de ojos/cabeza del jugador (~1.8 - 2.2 bloques) sin rozar el suelo ni atascar pathfinding.
  - Equipamiento: Cabeza de Slime oficial (#105231) + Peto de cuero verde lima ectoplasma (`RGB: 120, 205, 35`), sin pantalones ni botas (`AIR`) para crear efecto de torso flotante.
  - Sincronización de muerte: Destrucción instantánea del Allay al morir el fantasma mediante `@Children` y comando console `execute at <caster.uuid> run kill @e[type=allay,distance=..3,limit=1]`.


## [2026-10-01] items & essentials | Desvinculación de Negrita en Estrella y Silenciamiento de Notificación de Saldo EssentialsX
- **Módulos YAML Actualizados (Suite de 6 Bolsas)**:
  - Eliminado el formato `&l` de la estrella en los títulos de chat, pasando de `&#HEX&l⭐ BOLSA...` a `&#HEX⭐ &lBOLSA...` en los 6 tiers:
    1. [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml) ▶ `&#3CDB10⭐ &lBOLSA SUPER`
    2. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml) ▶ `&#1DC8FF⭐ &lBOLSA RARA`
    3. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml) ▶ `&#732AE2⭐ &lBOLSA EPICA`
    4. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml) ▶ `&#D02626⭐ &lBOLSA MITICA`
    5. [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml) ▶ `&#EFFF00⭐ &lBOLSA DIVINA`
    6. [`creator/lab/bundle_recompensas_limited_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_limited_test.yml) ▶ `&#5489FF⭐ &lBOLSA &#FF4B4B&lL...`
- **Configuración de EssentialsX Modificada**:
  - Silenciada la clave `addedToAccount=` (dejada en blanco) tanto en `plugins/Essentials/messages/messages_es.properties` como en `plugins/Essentials/messages/messages.properties`.
  - Evita la notificación redundante `THUNDERMC ✔ Se añadieron X a tu cuenta` al abrir bolsitas o recibir ingresos vía `/eco give`.
- **Sincronización Remota**: Subidos los 6 archivos de ExecutableItems y los 2 archivos de propiedades de Essentials al Sandbox (`ymykh9qy.274758bd`). Verificación completada.

## [2026-10-01] items & ui | Propagación de Formato de Mensaje de Chat en Apertura a Toda la Suite (Tiers I a VI)
- **Módulos Actualizados y Desplegados**:
  1. [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml) ▶ Cabecera: `&r  &#3CDB10&l⭐ BOLSA SUPER`
  2. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml) ▶ Cabecera: `&r  &#1DC8FF&l⭐ BOLSA RARA`
  3. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml) ▶ Cabecera: `&r  &#732AE2&l⭐ BOLSA EPICA`
  4. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml) ▶ Cabecera: `&r  &#D02626&l⭐ BOLSA MITICA`
  5. [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml) ▶ Cabecera: `&r  &#EFFF00&l⭐ BOLSA DIVINA`
  6. [`creator/lab/bundle_recompensas_limited_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_limited_test.yml) ▶ Cabecera: `&r  &#5489FF&l⭐ BOLSA &#FF4B4B&lL&#FF8B2D&lI&#FFD031&lM&#DCFF39&lI&#6DFF45&lT&#3BFFC7&lE&#5489FF&lD`
- **Diseño Unificado en los 6 Tiers**:
  - Margen superior e inferior vacío (`SEND_MESSAGE &r`).
  - Margen izquierdo de 2 espacios (`&r  `) en todas las líneas.
  - Subtítulo uniforme: `&r  &7ʀᴇᴄᴏᴍᴘᴇɴꜱᴀꜱ`.
  - Recompensas individuales con viñeta oscura `&8•` y texto en color blanco vanilla `&f`.
- **Sincronización Remota**: Subidos los 5 archivos restantes vía SFTP por lote a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox (`ymykh9qy.274758bd`). Verificación exitosa.

## [2026-10-01] items & ui | Ajuste de Mensaje de Chat en Apertura de Bolsa Épica (Indentación, Negrita, Mayúsculas y Premios en Blanco)
- **Módulo Actualizado**: [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml)
- **Cambios de Formato Implementados**:
  1. **Margen Izquierdo**: Agregada indentación de 2 espacios (`&r  `) al inicio de cada línea del bloque informativo.
  2. **Cabecera**: Texto en negrita y mayúsculas completas: `&r  &#732AE2&l⭐ BOLSA EPICA`.
  3. **Recompensas**: Texto de los premios entregados en blanco vanilla (`&f$5.000`, `&f12x Diamantes`, `&f$6.500`, `&f4x Bloques de Hierro`, `&f$8.000`, `&f4x Bloques de Oro`) manteniendo viñetas oscuras `&8•`.
- **Sincronización**: Desplegado en Sandbox (`plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_epica_test.yml`).

## [2026-10-01] items & mechanics | Migración de Calidad a DIVINA y Propagación de Animación de Apertura 5s con Cuenta Regresiva
- **Módulos Actualizados y Desplegados (Suite de 6 Bolsitas)**:
  1. [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml) ▶ Tier I: Súper (`&#3CDB10⭐ &fBolsita &8▶ &#3CDB10Super`)
  2. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml) ▶ Tier II: Rara (`&#1DC8FF⭐ &fBolsita &8▶ &#1DC8FFRara`)
  3. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml) ▶ Tier III: Épica (`&#732AE2⭐ &fBolsita &8▶ &#732AE2Epica`)
  4. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml) ▶ Tier IV: Mítica (`&#D02626⭐ &fBolsita &8▶ &#D02626Mitica`)
  5. [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml) ▶ Tier V: Divina (`&#EFFF00⭐ &fBolsita &8▶ &#EFFF00Divina`, tag `&8⁂ &#FD9A00&lD&#FAAE00&lI&#F7C200&lV&#F5D700&lI&#F2EB00&lN&#EFFF00&lA &e⭐⭐⭐⭐⭐`)
  6. [`creator/lab/bundle_recompensas_limited_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_limited_test.yml) ▶ Tier VI: Limited (`&#5489FF⭐ &fBolsita &8▶ &#FF4B4BL&#FF8B2Di&#FFD031m&#DCFF39i&#6DFF45t&#3BFFC7e&#5489FFd`)
- **Implementaciones Clave**:
  1. **Transición Canónica Legend $\to$ Divina**: Reemplazada la denominación Legend por **Divina** en toda la jerarquía de lore (`➠ &fDivina (75%)` / `➠ &7&mDivina (5%)`), tag formal `&8⁂ DIVINA &e⭐⭐⭐⭐⭐`, broadcasts y comandos de upgrade. Actualizado el estándar canónico en [`wiki/concepts/estandar-calidades-items.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/wiki/concepts/estandar-calidades-items.md).
  2. **Propagación del Motor de Animación Diseñado por el Sr Ramos**:
     - Estructura limpia de 5 segundos con fotogramas de 10 ticks:
       - `title %player% title "<Color>Bolsita <Tier>"`
       - `title %player% subtitle "&8▪ &fᴀʙʀɪᴇɴᴅᴏ &8[&a&m ... &r&8] &7Xs"` (cuenta regresiva 5s $\to$ 1s con barra segmentada).
       - Efectos acústicos sincrónicos: `playsound minecraft:item.bundle.drop_contents` + `minecraft:block.note_block.hat`.
       - Resolución con títulos estandarizados: `&a¡Bolsita Abierta!` para recompensas base y títulos con formato canónico en mejoras de tier.
- **Sincronización Remota**:
  - Subidos los 6 módulos YAML vía SFTP a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox (`ymykh9qy.274758bd`). Verificación de integridad completada.

## [2026-10-01] items & ui | Propagación de Diseño Oficial de Nombre y Lore en Suite de Bolsitas de Premios (Tiers I a VI)
- **Módulos Actualizados y Desplegados**:
  1. [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml) ▶ Tier I: Súper (`&#3CDB10⭐ &fBolsita &8▶ &#3CDB10Super`)
  2. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml) ▶ Tier II: Rara (`&#1DC8FF⭐ &fBolsita &8▶ &#1DC8FFRara`)
  3. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml) ▶ Tier III: Épica (`&#732AE2⭐ &fBolsita &8▶ &#732AE2Epica`)
  4. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml) ▶ Tier IV: Mítica (`&#D02626⭐ &fBolsita &8▶ &#D02626Mitica`)
  5. [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml) ▶ Tier V: Legend (`&#EFFF00⭐ &fBolsita &8▶ &#EFFF00Legend`)
  6. [`creator/lab/bundle_recompensas_limited_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_limited_test.yml) ▶ Tier VI: Limited (`&#5489FF⭐ &fBolsita &8▶ &#FF4B4BL&#FF8B2Di&#FFD031m&#DCFF39i&#6DFF45t&#3BFFC7e&#5489FFd`)
- **Alineación Visual implementada**:
  - Propagado el patrón de nomenclatura canónico del Sr Ramos: `&#<HEX>⭐ &fBolsita &8▶ &#<HEX><Calidad>` (con degradado Rainbow completo para Limited).
  - Unificado el encabezado de progresión a `&8ᴘʀᴏʙ ᴅᴇ ᴍᴇᴊᴏʀᴀʀ:` en small-caps para Tiers I-V y `&8★ ¡ᴄᴀʟɪᴅᴀᴅ ᴍÁxɪᴍᴀ! ★` para Tier VI.
- **Sincronización Remota**:
  - Sincronizados los 6 archivos vía SFTP en `plugins/ExecutableItems/items/ThunderMC/` del servidor Sandbox (`ymykh9qy.274758bd`). Verificación exitosa.

## [2026-09-30] brand & renders | Iconos Discord con Fondo Flat Amarillo Corporativo (#FEEB00)
- **Entregables creados**:
  - **Variante Cerdo Rey con Corona**:
    - PNG Oficial Discord 512x512: [`creator/output/renders/logo_rey/logo_rey_flat_yellow_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/logo_rey_flat_yellow_discord.png)
    - Simulación de Tamaños Discord: [`creator/output/renders/logo_rey/preview_rey_flat_yellow_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/preview_rey_flat_yellow_discord.png)
  - **Variante Caballero Medieval**:
    - PNG Oficial Discord 512x512: [`creator/output/renders/logo_caballero/logo_caballero_flat_yellow_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_flat_yellow_discord.png)
    - Simulación de Tamaños Discord: [`creator/output/renders/logo_caballero/preview_caballero_flat_yellow_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/preview_caballero_flat_yellow_discord.png)
- **Aspectos técnicos**:
  1. Extracción exacta del color corporativo del embed provisto: `accent_color: 16706304` = `#FEEB00` (RGB: 254, 235, 0).
  2. Sustitución de fondos escénicos por un color plano *flat* puro sin texturas ni degradados.
  3. Contraste de alto impacto en Discord: el trazo perimetral burdeos `#4A1010` delimita con máxima nitidez la silueta contra el fondo amarillo eléctrico, garantizando 100% de reconocimiento visual en la barra lateral reducida a 32x32 y 48x48 px.

## [2026-09-30] brand & renders | Cerdo Rey con Corona + Fondo Dungeon Cinemático (Estilo Shaders/Chimenea)
- **Entregables creados**:
  - PNG Oficial Discord 512x512: [`creator/output/renders/logo_rey/logo_rey_cinematic_dungeon_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/logo_rey_cinematic_dungeon_discord.png)
  - Simulación de Tamaños Discord: [`creator/output/renders/logo_rey/preview_rey_cinematic_dungeon_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/preview_rey_cinematic_dungeon_discord.png)
  - Fondo Base Dungeon Cinemático 1024x1024: [`creator/output/renders/logo_rey/dungeon_cinematic_bg.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/dungeon_cinematic_bg.jpg)
  - Imagen de Referencia de Usuario Persistida: [`creator/raw/references/render_estilo_referencia_chimenea.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/raw/references/render_estilo_referencia_chimenea.jpg)
- **Aspectos técnicos**:
  1. Alineación estética con la referencia provista: iluminación volumétrica global, fuego cúbico resplandeciente en el hogar central, velas en repisas de piedra y sombras en azul pizarra/carbón.
  2. Arquitectura de mazmorra simétrica: chimenea/hoguera monumental de ladrillos de piedra con arco gótico y textura de bloques nítida sin ruido visual.
  3. Integración con el cerdo rey canónico de `THUNDER_ICON_LOGO.png` al 82% de cobertura, logrando un balance cromático entre el resplandor ámbar cálido de las llamas y la corona dorada.

## [2026-09-30] brand & renders | Cerdo Rey con Corona Oficial + Fondo Mazmorra Minecraft Vanilla
- **Entregables creados**:
  - PNG Oficial Discord 512x512: [`creator/output/renders/logo_rey/logo_rey_mc_vanilla_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/logo_rey_mc_vanilla_discord.png)
  - Simulación de Tamaños Discord: [`creator/output/renders/logo_rey/preview_rey_mc_vanilla_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/preview_rey_mc_vanilla_discord.png)
  - Render Base Mazmorra Vanilla 1024x1024: [`creator/output/renders/logo_rey/mc_vanilla_dungeon_bg.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/mc_vanilla_dungeon_bg.jpg)
- **Aspectos técnicos**:
  1. Fidelidad estricta a texturas oficiales de Minecraft Vanilla: bloques reconocibles de adoquín (*cobblestone*), adoquín musgoso (*mossy cobblestone*), ladrillos de piedra (*stone bricks*) y antorcha vanilla con textura pixel-art de fuego/humo.
  2. Atmósfera de mazmorra clásica: iluminación natural de antorcha en nivel de luz 7-8 sobre bloques cúbicos 3D, barrotes de hierro y cofre de madera en penumbra.
  3. Contraste de identidad: el cerdo rey con corona original de `THUNDER_ICON_LOGO.png` domina el 82% del círculo en primer plano, integrándose orgánicamente en el entorno de juego real sin generar ruido visual.

## [2026-09-30] brand & renders | Cerdo Rey con Corona Oficial + Fondo Dungeon Tenue
- **Entregables creados**:
  - PNG Oficial Discord 512x512: [`creator/output/renders/logo_rey/logo_rey_dungeon_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/logo_rey_dungeon_discord.png)
  - Simulación de Tamaños Discord: [`creator/output/renders/logo_rey/preview_rey_dungeon_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/preview_rey_dungeon_discord.png)
  - Fondo Base Dungeon Tenue: [`creator/output/renders/logo_rey/dungeon_tenue_bg.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/dungeon_tenue_bg.jpg)
- **Aspectos técnicos**:
  1. Supresión total del ruido visual: sustitución del castillo complejo por una cámara de mazmorra oscura con bloques geométricos de piedra cúbica en planos vectoriales planos (*cel-shading* estricto).
  2. Atmósfera tenue y minimalista: reja de calabozo al fondo, pilares limpios de pizarra y una única antorcha tenue con resplandor ámbar suave.
  3. Contraste óptimo del personaje: el cerdo rey con corona original de `THUNDER_ICON_LOGO.png` se sitúa en primer plano absoluto sin interferencias ni competencia gráfica.

## [2026-09-30] brand & renders | Cerdo Rey con Corona Oficial + Fondo Medieval de Castillo
- **Entregables creados**:
  - PNG Oficial Discord 512x512: [`creator/output/renders/logo_rey/logo_rey_castillo_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/logo_rey_castillo_discord.png)
  - Simulación de Tamaños Discord: [`creator/output/renders/logo_rey/preview_rey_castillo_discord.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/preview_rey_castillo_discord.png)
  - Render Base 1024x1024: [`creator/output/renders/logo_rey/logo_rey_castillo_raw.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_rey/logo_rey_castillo_raw.jpg)
  - Ficha técnica: [`creator/lab/renders/logo_rey/logo_rey_castillo.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/logo_rey/logo_rey_castillo.md)
- **Aspectos técnicos**:
  1. Integración del cerdo rey con corona de oro de `THUNDER_ICON_LOGO.png` en un entorno de fortaleza medieval con el mismo estándar `estilo_logo`.
  2. Elementos arquitectónicos vivos: torres de sillar con almenas, estandartes heráldicos, portal ojival con rastrillo, antorchas encendidas y cielo nocturno con luna.
  3. Formateado en medallón circular de 512x512 px con esquinas transparentes, optimizado para máxima micro-lectura en la barra lateral de Discord (32x32 y 48x48 px).

## [2026-09-30] brand & renders | Logo Caballero Prueba 6: Alta Definición, Matting Alfa y Defringing
- **Entregables creados**:
  - Ficha técnica: [`creator/lab/renders/logo_caballero/logo_caballero_6.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/logo_caballero/logo_caballero_6.md)
  - Render estándar: [`creator/output/renders/logo_caballero/logo_caballero_6.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_6.jpg)
  - Versión transparente ARGB refinada: [`creator/output/renders/logo_caballero/logo_caballero_6.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_6.png)
  - Validación fondo oscuro (#18191C): [`creator/output/renders/logo_caballero/logo_caballero_6_test_dark.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_6_test_dark.png)
  - **Pack Optimizado Discord (512x512)**:
    - Transparente con encuadre circular estricto (0 px recortados): [`creator/output/renders/logo_caballero/logo_caballero_discord_transparente.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_discord_transparente.png)
    - Emblema con disco Thunder y aro dorado: [`creator/output/renders/logo_caballero/logo_caballero_discord_emblema.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_discord_emblema.png)
    - **Fondo Castillo V2 Iluminado (Torres, Almenas, Antorchas y Luna)**: [`creator/output/renders/logo_caballero/logo_caballero_discord_castillo_v2.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_discord_castillo_v2.png) (Simulación: [`creator/output/renders/logo_caballero/preview_discord_castillo_v2.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/preview_discord_castillo_v2.png))
- **Refinamiento técnico**:
  1. Depuración perimetral profunda: eliminación total del halo residual claro mediante penetración directa hasta el trazo oscuro `#4A1010`.
  2. Auditoría perimetral certificada: 2.765 píxeles perimetrales oscuros vs. 0 píxeles residuales claros en la frontera con la transparencia.
  3. Suavizado subpixel continuo y libre de halos sobre cualquier fondo (blanco, oscuro o transparente).
  4. Mayor definición en degradados del penacho amarillo y facetas de acero con biseles nítidos.

## [2026-09-30] brand & renders | Logo Caballero Prueba 5: Coleta Amarilla Corporativa y Desgaste Sutil
- **Entregables creados**:
  - Ficha técnica: [`creator/lab/renders/logo_caballero/logo_caballero_5.md`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/renders/logo_caballero/logo_caballero_5.md)
  - Render estándar: [`creator/output/renders/logo_caballero/logo_caballero_5.jpg`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_5.jpg)
  - Versión transparente ARGB: [`creator/output/renders/logo_caballero/logo_caballero_5.png`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/renders/logo_caballero/logo_caballero_5.png)
- **Modificaciones aplicadas sobre Modelo 3**:
  1. Penacho/coleta superior transformado a amarillo oro corporativo Thunder (`#FFD700`), unificando la identidad cromática de la corona original.
  2. Moderación de magulladuras y eliminación de abolladuras invasivas; incorporación de desgaste sutil y pulido en biseles de acero manteniendo cel-shading estricto.
  3. Conversión de fondo a canal alfa transparente para uso directo en plataformas web y Tebex.


## [2026-09-29] gamedev-roles-app | App de Roles de Estudio Indie con Prompts Profesionales
- **Entregable creado**: [`creator/lab/gamedev_roles_app/index.html`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/gamedev_roles_app/index.html) — SPA HTML/CSS/JS sin dependencias externas.
- **Funcionalidad**: Navbar lateral con 7 departamentos (EXECUTIVE, MARKETING, PROGRAMACION, DISENO, ARTE, AUDIO, PRODUCCION) + vista "Todos". Cada rol muestra: descripción, ¿Por qué se debe tener?, Riesgo si falta, y Prompt de Liderazgo colapsable.
- **Prompts profesionales**: 21 prompts individuales por rol — cada uno con contexto operativo, marco metodológico, herramientas específicas, referencias reales (GDC, libros de industria) y output esperado accionable.
- **Bugs resueltos**: función `renderCards` mal declarada (código fuera de función), botón de prompt duplicado por lógica redundante de dept-level, caracteres corruptos por doble codificación Latin-1252/UTF-8 en heredoc PowerShell (solucionado con ensamblado de bytes crudos), fuente monospace y overflow del bloque `<pre>` (CSS `white-space: pre-wrap` + font stack del sistema).
- **Renders ThunderStudios**: series caballero_portal (4), caballero_fogata (1+final), barco_pirata (4), logo_caballero (4) + THUNDER_ICON_LOGO — persistidos en `creator/output/renders/` con fichas técnicas en `creator/lab/renders/`.
- **Commit**: `b8aec13` — 44 files changed, 2163 insertions, 280 deletions.

## [2026-09-29] items & standards | Estandarización Final: Nomenclatura 'Bolsita de Premios', Progresión Tachada y Despliegue SFTP

- **Módulos Optimizados y Desplegados (Suite de 6 Bolsitas de Premios)**:
  1. [`creator/lab/bundle_recompensas_super_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_super_test.yml) (`bundle_recompensas_super_test`) ▶ Tier I: Súper (`&#3CDB10Bolsita de Premios`, `LIME_BUNDLE`)
  2. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml) (`bundle_recompensas_rara_test`) ▶ Tier II: Rara (`&#1DC8FFBolsita de Premios`, `LIGHT_BLUE_BUNDLE`)
  3. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml) (`bundle_recompensas_epica_test`) ▶ Tier III: Épica (`&#732AE2Bolsita de Premios`, `PURPLE_BUNDLE`)
  4. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml) (`bundle_recompensas_mitica_test`) ▶ Tier IV: Mítica (`&#D02626Bolsita de Premios`, `RED_BUNDLE`)
  5. [`creator/lab/bundle_recompensas_legend_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legend_test.yml) (`bundle_recompensas_legend_test`) ▶ Tier V: Legend (`&#EFFF00Bolsita de Premios`, `YELLOW_BUNDLE`)
  6. [`creator/lab/bundle_recompensas_limited_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_limited_test.yml) (`bundle_recompensas_limited_test`) ▶ Tier VI: Limited (`WHITE_BUNDLE`, degradado Rainbow completo en display name y tag)
- **Alineación con Estándar Canónico de ThunderMC**:
  - Nombre oficial establecido: **`Bolsita de Premios`** con el color de su respectiva calidad (o espectro Rainbow para Limited).
  - Conservación de calidades superadas tachadas (`&7&m<Calidad> (XX%)`): visible en el lore para reflejar visualmente la escala de progresión alcanzada, manteniendo al mismo tiempo un ancho horizontal compacto (< 20 caracteres por línea).
  - En Tier VI Limited se exponen todos los tiers previos tachados bajo la cabecera `★ ¡ᴄᴀʟɪᴅᴀᴅ ᴍÁxɪᴍᴀ! ★`.
  - Reubicación de la etiqueta formal de rareza (`&8⁂ <GRADIENTE> <ESTRELLAS>`) inmediatamente previa a la interacción de apertura `&7▶ ᴄʟɪᴄᴋ ᴅᴇʀ - ᴀʙʀɪʀ`.
  - Ocultación sistemática de tooltips vanilla (`Can hold mixed items` / `Fullness`) en las 6 bolsitas (`hideAdditionalTooltip: true`).
- **Despliegue y Sincronización Remota**:
  - Sincronizados los 6 archivos YAML vía SFTP en `plugins/ExecutableItems/items/ThunderMC/` del servidor Sandbox (`ymykh9qy.274758bd`). Verificación de integridad completada.

---

## [2026-09-28] items & mechanics | Suite Completa de Bundles de Recompensas de Prueba (Tiers I al VI)
- **Módulos Creados y Desplegados**:
  1. [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml) (`bundle_recompensas_test`) ▶ Tier I: Común (`&#CECECE`, `BUNDLE`)
  2. [`creator/lab/bundle_recompensas_especial_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_especial_test.yml) (`bundle_recompensas_especial_test`) ▶ Tier II: Especial (`#63e80c`, `LIME_BUNDLE`)
  3. [`creator/lab/bundle_recompensas_rara_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_rara_test.yml) (`bundle_recompensas_rara_test`) ▶ Tier III: Rara (`#0ccee8`, `LIGHT_BLUE_BUNDLE`)
  4. [`creator/lab/bundle_recompensas_epica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_epica_test.yml) (`bundle_recompensas_epica_test`) ▶ Tier IV: Épica (`#ba0ffa`, `PURPLE_BUNDLE`)
  5. [`creator/lab/bundle_recompensas_mitica_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_mitica_test.yml) (`bundle_recompensas_mitica_test`) ▶ Tier V: Mítica (`#BC1013`, `RED_BUNDLE`)
  6. [`creator/lab/bundle_recompensas_legendaria_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_legendaria_test.yml) (`bundle_recompensas_legendaria_test`) ▶ Tier VI: Legendaria (`#fab60f`, `YELLOW_BUNDLE`)
- **Acciones Implementadas**:
  - **Identidad de Materiales en 1.21.11**: Implementación de los nuevos sacos teñidos de Minecraft 1.21 (`LIME_BUNDLE`, `LIGHT_BLUE_BUNDLE`, `PURPLE_BUNDLE`, `RED_BUNDLE`, `YELLOW_BUNDLE`) para reconocimiento visual inmediato en el inventario.
  - **Experiencia de Apertura Unificada**: Los 6 sacos incorporan la secuencia cinemática de descifrado cinético con `darkness 4 0 true`, escala de notas `pling` (1.0 a 2.0), partículas temáticas y la barra de progreso tachada en `subtitle`.
  - **Cadena de Upgrades Interconectada**: La probabilidad de mejora en cada tier entrega directamente el bundle de nivel superior correspondiente (`ei give %player% bundle_recompensas_<tier>_test 1`), con el lore tachando dinámicamente los rangos ya superados.
  - **Calibración de Economía Escalonada**:
    - *Común*: $750 - $1.200 + carbón, hierro, oro.
    - *Especial*: $2.000 - $3.000 + redstone, lapislázuli, esmeraldas.
    - *Rara*: $5.000 - $8.000 + diamantes, bloques de hierro/oro.
    - *Épica*: $12.000 - $20.000 + fragmentos/lingotes de netherite, bloques de diamante, manzanas doradas.
    - *Mítica*: $30.000 - $50.000 + lingotes/bloques de netherite, manzanas notch, tótem.
    - *Legendaria (Jackpot)*: $75.000 - $150.000 + bloques masivos de netherite, múltiples tótems y manzanas notch.
- **Despliegue Remoto**:
  - Los 6 archivos fueron transferidos y sincronizados con éxito en `plugins/ExecutableItems/items/ThunderMC/` del servidor Sandbox (`ymykh9qy.274758bd`).

---

## [2026-09-28] items & mechanics | Animación Cinética de Descifrado y Sobrecarga Energética
- **Módulo**: [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml)
- **Requerimiento del Sr Ramos**:
  - Eliminar los nombres de calidades en el `title` para evitar predisposición/spoiler.
  - Centrar el texto en `ᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ`, dotándolo de movimiento cinético y sensación de sobrecarga progresiva ("algo bueno va a salir").
- **Acciones Implementadas**:
  1. **Secuencia de Movimiento y Sobrecarga Energética**:
     - **Paso 1 (0 ticks)**: `&8[&7&k??&8] &7ᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ &8[&7&k??&8]` + Subtitle `&a&m &8&m    &r`. Sonido metálico/amatista + partículas de runas tenues.
     - **Paso 2 (10 ticks)**: `&#0ccee8✦ &fᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ &8[&b.&8  ] &#0ccee8✦` + Subtitle `&a&m  &8&m   &r`. Despertar eléctrico cyan, pling 1.1 + crítico blanco.
     - **Paso 3 (20 ticks)**: `#63e80c▲ &a&lᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ &8[&a..&8 ] #63e80c▲` + Subtitle `&a&m   &8&m  &r`. Resonancia esmeralda en negrita, pling 1.3 + XP pickup + estrellas verdes.
     - **Paso 4 (30 ticks)**: `#ba0ffa★ &d&lᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ &8[&d...&8] #ba0ffa★` + Subtitle `&a&m    &8&m &r`. Salto a amatista violeta, pling 1.55 + XP pickup + remolino de runas.
     - **Paso 5 (40 ticks)**: `#fab60f★ &e&l¡ꜱᴏʙʀᴇᴄᴀʀɢᴀ! &8[&e&k!!&8] #fab60f★` + Subtitle `&a&m     &r`. Alerta dorada de sobrecarga con glifos inestables, pling 1.8 + campana de amatista + aura violeta.
     - **Paso 6 (50 ticks)**: `#fab60f★ &f&l¡ꜱᴇʟʟᴏ ʀᴏᴛᴏ! #fab60f★` + Subtitle `&a&l✔ ᴅᴇꜱᴄɪꜰʀᴀᴅᴏ ✔`. Clímax armónico pling 2.0 + fanfarria + tótem dorado.
  2. **Compatibilidad Estricta**:
     - Cada comando encapsulado en comillas simples `'...'` para mantener compatibilidad con SnakeYAML en Folia.
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`.

---

## [2026-09-28] fix & items | Corrección de Carga SnakeYAML en Bundle de Recompensas
- **Módulo**: [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml)
- **Diagnóstico de Causa Raíz**:
  - Al revisar los registros en vivo del servidor Folia (`creator/lab/latest.log`), se identificó la excepción:
    `[ExecutableItems] Error when loading bundle_recompensas_test.yml, your config is not made correctly !`
  - Causa: En la lista `playerCommands`, los comandos con títulos (`title %player% title "..."`) y comandos con tildes de coordenadas de Minecraft (`~ ~ ~`) no poseían comillas envolventes al inicio de la línea. SnakeYAML interpreta las comillas a mitad de un escalar no entrecomillado (`unquoted scalar, found a quote`) como un error fatal de parseo, abortando la carga del ítem.
- **Acciones Implementadas**:
  - Encapsulación estricta de cada línea de comando dentro de comillas simples (`'title %player% title "..."'`), protegiendo operadores especiales de YAML (`#`, `|`, `~`, `""`).
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`.

---

## [2026-09-28] items & mechanics | Descifrado Rúnico y Escalado Dopamínico de Calidad en Bundle
- **Módulo**: [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml)
- **Requerimiento del Sr Ramos**:
  - Transformar la animación del `title` para que simule un descifrado activo de su calidad.
  - Generar un impacto visual y auditivo de alta dopamina que haga sentir la emoción de mejora de tier (*upgrade*).
- **Acciones Implementadas**:
  1. **Arquitectura Multisensorial de Descifrado**:
     - **Paso 1 (0 ticks)**: `&8[&7&k??&8] &7ᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ &8[&7&k??&8]` + Subtitle `&a&m &8&m    &r`. Efecto `darkness 4 0 true`, partículas de encantamiento rúnico y sonido de percusión metálica/amatista (`amethyst_block.hit` + `note_block.hat`).
     - **Paso 2 (10 ticks)**: Detección base `&#CECECE&k| &fᴄᴀʟɪᴅᴀᴅ: &#CECECEᴄᴏᴍÚɴ &#CECECE&k|` + Subtitle `&a&m  &8&m   &r`. Primer destello con `note_block.pling` (pitch 1.0) y chispas críticas (`crit`).
     - **Paso 3 (20 ticks)**: Primer salto `#63e80c▲ &l¡ᴜᴘɢʀᴀᴅᴇ! &r#63e80cᴇꜱᴘᴇᴄɪᴀʟ ▲` + Subtitle `&a&m   &8&m  &r`. Subida armónica `pling` (1.25) + `experience_orb.pickup` y estrellas esmeralda (`happy_villager`).
     - **Paso 4 (30 ticks)**: Segundo salto `#0ccee8▲▲ &l¡ᴜᴘɢʀᴀᴅᴇ! &r#0ccee8ʀᴀʀᴀ ▲▲` + Subtitle `&a&m    &8&m &r`. Tono `pling` (1.5) + `experience_orb.pickup` y remolino de runas (`enchant`).
     - **Paso 5 (40 ticks)**: Sobrecarga mística `#ba0ffa★ &l¡ꜱᴏʙʀᴇᴄᴀʀɢᴀ! &r#ba0ffaÉᴘɪᴄᴀ ★` + Subtitle `&a&m     &r`. Tono `pling` (1.75) + resonancia de amatista (`amethyst_block.chime`) y aura morada (`witch`).
     - **Paso 6 (50 ticks)**: Clímax dorado `#fab60f★ &l¿ʟᴇɢᴇɴᴅᴀʀɪᴀ? &r#fab60f&k|||` + Subtitle `&a&l✔ ᴅᴇꜱᴄɪꜰʀᴀᴅᴏ ✔`. Clímax armónico `pling` (2.0) + fanfarria (`challenge_complete`) y explosión de tótem dorado (`totem_of_undying`).
  2. **Contraste y Resolución**:
     - Retraso de 20 ticks tras el fotograma de tensión para disipación natural del `darkness` antes de disparar el `RANDOM RUN` con la entrega del botín y la confirmación final.
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`.

---

## [2026-09-28] items & mechanics | Ruleta de Calidades de Tiers en Title Sincronizada con Subtitle
- **Módulo**: [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml)
- **Requerimiento del Sr Ramos**:
  - Implementar en el `title` una animación de mejora/ruleta de calidades sincronizada con la progresión de la barra tachada en `subtitle`.
- **Acciones Implementadas**:
  1. **Secuencia de Ruleta de Calidades de Tiers en Title**:
     - Paso 1 (0 ticks): `title %player% title "&#CECECE★ ᴄᴏᴍÚɴ ★"` + Subtitle `&a&m &8&m    &r` (Pitch 0.9).
     - Paso 2 (10 ticks): `title %player% title "#63e80c★ ᴇꜱᴘᴇᴄɪᴀʟ ★"` + Subtitle `&a&m  &8&m   &r` (Pitch 1.1).
     - Paso 3 (20 ticks): `title %player% title "#0ccee8★ ʀᴀʀᴀ ★"` + Subtitle `&a&m   &8&m  &r` (Pitch 1.3).
     - Paso 4 (30 ticks): `title %player% title "#ba0ffa★ Éᴘɪᴄᴀ ★"` + Subtitle `&a&m    &8&m &r` (Pitch 1.5).
     - Paso 5 (40 ticks): `title %player% title "#BC1013★ ᴍÍᴛɪᴄᴀ ★"` + Subtitle `&a&m     &r` (Pitch 1.8).
     - Paso 6 (50 ticks): `title %player% title "#fab60f★ ʟᴇɢᴇɴᴅᴀʀɪᴀ ★"` + Subtitle `&aᴄᴏᴍᴘʟᴇᴛᴀᴅᴏ` (Pitch 2.0).
  2. **Atmósfera y Dinámica**:
     - Preservado el efecto `darkness 4 0 true` de inicio que se aclara justo al terminar el fotograma legendario e iniciar el botín final.
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`.

---

## [2026-09-28] items & mechanics | Apertura en Solo Subtítulo y Efecto Darkness en Bundle de Recompensas
- **Módulo**: [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml)
- **Requerimiento del Sr Ramos**:
  - Restringir la animación de apertura exclusivamente al componente `subtitle` (sin texto en `title`).
  - Aplicar el efecto `minecraft:darkness` al jugador durante el transcurso de la apertura.
- **Acciones Implementadas**:
  1. **Aislamiento Visual de Subtitle**:
     - Eliminado el string `&fᴀʙʀɪᴇɴᴅᴏ` de `title %player% title`.
     - Establecido `title %player% title ""` (cadena vacía) en cada iteración para disparar el paquete de refresco del cliente sin pintar caracteres en la línea principal de título, dejando el foco 100% sobre la barra de progreso tachada en `subtitle`.
  2. **Efecto de Inmersión Atmosférica (`Darkness`)**:
     - Inyectado `effect give %player% minecraft:darkness 4 0 true` al inicio de la apertura.
     - Duración calibrada en 4 segundos (80 ticks) con partículas ocultas (`true`), cubriendo los 3.5 segundos de la secuencia de apertura y desvaneciéndose justo en la entrega del botín y títulos de recompensa.
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`.

---

## [2026-09-28] items & mechanics | Implementación de Barra de Progreso Tachada (&a&m &8&m &r) en Bundle de Recompensas
- **Módulo**: [`creator/lab/bundle_recompensas_test.yml`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/bundle_recompensas_test.yml)
- **Requerimiento del Sr Ramos**:
  - Reemplazar los caracteres de bloque sólido (`■`) en el subtítulo por la barra de progresión basada en espacios con formato tachado (`&a&m   &8&m   &r`) empleada en las bolsas de dinero.
- **Acciones Implementadas**:
  1. **Secuencia de Subtítulos Calibrada**:
     - Paso 1: `title %player% subtitle "&a&m &8&m    &r"`
     - Paso 2: `title %player% subtitle "&a&m  &8&m   &r"`
     - Paso 3: `title %player% subtitle "&a&m   &8&m  &r"`
     - Paso 4: `title %player% subtitle "&a&m    &8&m &r"`
     - Paso 5: `title %player% subtitle "&a&m     &r"`
     - Paso 6: `title %player% subtitle "&aᴄᴏᴍᴘʟᴇᴛᴀᴅᴏ"`
  2. **Preservación Visual y de Rendimiento**:
     - Mantenido el título fijo `&fᴀʙʀɪᴇɴᴅᴏ` con timings `0 20 5` para evitar parpadeos.
     - Preservada la cadencia sonora ascendente de `minecraft:item.bundle.drop_contents` (pitch 0.9 a 1.8).
- **Despliegue Remoto**:
  - Subido y reemplazado con éxito en el servidor Sandbox (`ymykh9qy.274758bd`) vía SFTP en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`.

---

## [2026-09-28] items & mechanics | Migración de Animación Actionbar a Title y Subtitle en Bundle de Recompensas
- **Módulo**: `creator/lab/bundle_recompensas_test.yml`
- **Requerimiento del Sr Ramos**:
  - Trasladar la secuencia de apertura de Actionbar a Title y Subtitle.
  - Title: Fijar texto "Abriendo" con la custom font (`ᴀʙʀɪᴇɴᴅᴏ`).
  - Subtitle: Proyección de la barra progresiva de apertura.
  - Optimizar la experiencia visual para que sea lo más limpia posible.
- **Acciones Implementadas**:
  1. **Configuración de Tiempos (`title times 0 20 5`)**:
     - Previene el parpadeo (flickering) entre fotogramas de 10 ticks al eliminar el `fadeIn` inicial y mantener una ventana de persistencia suave.
  2. **Estructura Visual Atómica en Fase de Apertura**:
     - Title persistente: `&fᴀʙʀɪᴇɴᴅᴏ`.
     - Subtitle progresivo: Escalado de 5 bloques sólidos `■` (`&e■&8■■■■` $\to$ `&e■■■■■` $\to$ `&a■■■■■` $\to$ `&aᴄᴏᴍᴘʟᴇᴛᴀᴅᴏ`).
  3. **Limpieza Integral de Entrega de Premios (Post-Animación)**:
     - Erradicado el spam de bucles redundantes y delays en Actionbar (`+++ DELAY_TICK 20 +++ title actionbar...`).
     - Migrada la recompensa directamente al canal central: Title (`¡ʙᴜɴᴅʟᴇ ᴀʙɪᴇʀᴛᴏ!` o `¡ʙᴜɴᴅʟᴇ ᴍᴇᴊᴏʀᴀᴅᴏ!`) y Subtitle con el desglose del premio (`+$750 | 64x Carbón` o `Calidad Especial Tier II`) calibrado con `times 2 40 10`.
     - Mantenida la confirmación en Chat (`SEND_MESSAGE`) y acústica ceremonial (`levelup`, `challenge_complete`, almas/totem).
  4. **Preservación Acústica**:
     - Mantenida la secuencia de pitch incremental (`0.9` a `1.8`) en `minecraft:item.bundle.drop_contents`.
- **Despliegue Remoto**:
  - Autenticación SSH actualizada con la nueva clave moderna `id_ed25519`.
  - Subido con éxito al servidor Sandbox (`ymykh9qy.274758bd`) en `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml` (9.639 bytes confirmados).

---

## [2026-09-28] fix & runtime | Corrección de Bloqueo de Arranque en Lanzadores por Falso Positivo de Socket y Timeout
- **Módulo**: `INICIAR_PANEL_BEACON.bat`, `INICIAR_PANEL_HANUSH.bat`, `thunder-ai-control/`
- **Diagnóstico de Causa Raíz**:
  1. **Falso Positivo en Detección de Puerto (`netstat -ano | findstr :4848`)**:
     - Tras cerrar el navegador o reiniciar, Windows mantiene conexiones TCP efímeras en estado `TIME_WAIT` hasta por 120 segundos. El comando detectaba el socket en `TIME_WAIT` como si el servidor estuviese activo, omitiendo el arranque de PowerShell (`server.ps1`). El navegador se abría de inmediato encontrando el puerto cerrado (`ERR_CONNECTION_REFUSED`).
  2. **Colapso de Comando `timeout` con Redirección**:
     - La instrucción `timeout /t 2 /nobreak > nul` abortaba con `ERROR: Input redirection is not supported, exiting the process immediately.` en consolas desasociadas de stdin estándar.
  3. **Incompatibilidad de Saltos de Línea Unix (LF)**:
     - El archivo batch poseía saltos de línea LF (`\n`), provocando desalineamiento de buffers en el intérprete `cmd.exe` al procesar caracteres multibyte UTF-8 (`⚡`), ejecutando fragmentos de palabras como comandos erróneos (`'r'`, `'o'`).
- **Acciones Ejecutadas**:
  1. **Reescritura Robusta de `INICIAR_PANEL_BEACON.bat`**:
     - Filtro estricto de socket activo mediante regex de estado de escucha: `netstat -ano | findstr /R /C:":4848 .*LISTENING" > nul`.
     - Reemplazo de `timeout` por bucle de polling no bloqueante con `ping 127.0.0.1 -n 2 > nul` que verifica activamente hasta que el servidor responde antes de disparar el navegador.
     - Conversión estricta a formato Windows CRLF (`\r\n`).
  2. **Auditoría Integral del Frontend**:
     - Verificada la ejecución limpia y libre de errores de todos los módulos (`app.js`, `latency-estimator.js`, `index.html`) mediante emulación headless en Edge.

---

## [2026-09-28] engine & ui | Herramienta BeaconLatencyEstimator y Barra de Progreso Minimalista con Auto-completado
- **Módulo**: `thunder-ai-control/` (`public/latency-estimator.js`, `public/index.html`, `public/styles.css`, `public/app.js`, `server.ps1`)
- **Requerimiento del Sr Ramos**:
  - Visualización aproximada y precisa del tiempo de espera de la respuesta.
  - Barra de progresión sencilla, minimalista y fluida que se autocomplete en tiempo real.
  - Desarrollo de una herramienta propia para calcular el tiempo aproximado con la máxima exactitud posible.
- **Acciones Implementadas**:
  1. **Herramienta Propia `BeaconLatencyEstimator` ([`latency-estimator.js`](file:///C:/Users/PC/Desktop/ThunderCerebro/thunder-ai-control/public/latency-estimator.js))**:
     - Motor analítico basado en 5 dimensiones: Time-To-First-Token (TTFT) por arquitectura de modelo, ratio tokens/segundo, análisis semántico de complejidad del prompt (detección de código, análisis o consultas breves), overhead de razonamiento interno (`--effort high`) y probabilidad de invocación de herramientas del sistema.
     - Sistema de auto-calibración adaptativa continua: almacena en `localStorage` la razón entre el tiempo estimado y el tiempo real devuelto, calculando un factor multiplicador ($C_{factor}$) que aprende y se ajusta automáticamente según la potencia de cómputo y latencia de red del usuario.
  2. **Controlador de Física y Progresión Asintótica**:
     - Avance suave de 0% a 90% mediante curva cuadrática de desaceleración durante el tiempo estimado inicial.
     - Curva asintótica de seguridad ($90\% \to 98\%$) en caso de que el modelo requiera tiempo extra, evitando estancamiento visual o desbordamiento antes de recibir la respuesta.
     - Al completar la petición, la barra transiciona instantáneamente al 100% (*snap*) con feedback visual (`Listo en X.Xs`) y auto-registra la métrica en el estimador.
  3. **Interfaz Minimalista y Píldora de Tiempo ([`index.html`](file:///C:/Users/PC/Desktop/ThunderCerebro/thunder-ai-control/public/index.html#L183-L208), [`styles.css`](file:///C:/Users/PC/Desktop/ThunderCerebro/thunder-ai-control/public/styles.css#L865-L935))**:
     - Burbuja de pensamiento compacta con micro-barra de 3.5px en gradiente ámbar Beacon (`#f59e0b` a `#d97706`), texto de fase dinámica (*"Conectando y analizando..."* $\to$ *"Razonando y sintetizando..."* $\to$ *"Estructurando respuesta final..."*) y píldora con contador dinámico `⏱️ elapsed / ~est`.
     - Inclusión permanente de badge de tiempo de respuesta (`⏱️ X.Xs`) en la barra de herramientas de cada mensaje generado.
  4. **Precisión en Backend ([`server.ps1`](file:///C:/Users/PC/Desktop/ThunderCerebro/thunder-ai-control/server.ps1#L481-L540))**:
     - Cronometrado exacto de llamadas mediante `[System.Diagnostics.Stopwatch]` y retorno del atributo `executionSeconds` en la respuesta JSON.

---

## [2026-09-28] security & ui | Sistema de Confirmación de Acciones Delicadas y Modal Guardián en Beacon
- **Módulo**: `thunder-ai-control/` (`public/index.html`, `public/styles.css`, `public/app.js`)
- **Requerimiento del Sr Ramos**:
  - Incorporar un mecanismo de confirmación interactiva con botón y mensaje explicativo para prevenir ejecuciones destructivas o involuntarias al operar con auto-aprobación de permisos (`--dangerously-skip-permissions`).
- **Acciones Implementadas**:
  1. **Modal Guardián Reutilizable (`#confirmActionModal`)**:
     - Diálogo emergente con diseño de alta visibilidad (badge ámbar `⚠️`, título, descripción del riesgo, caja de previsualización monospaciada de la orden y botones `[Confirmar y Proceder]` / `[Cancelar]`).
     - Soporta atajos de teclado (`Enter` para confirmar, `Escape` para cancelar) y clic fuera del modal.
  2. **Intercepción Proactiva en Chat Web (`submitChatMessage`)**:
     - Algoritmo de detección heurística de patrones delicados (`borrar`, `eliminar`, `modificar`, `sobrescribir`, `ejecutar`, `powershell`, `rm`, `del`, `git reset`, `survival`, `production`, etc.).
     - Toggle visual integrado en la base del dock de entrada: `[x] 🛡️ Confirmar cambios delicados antes de ejecutar` (activo por defecto).
     - Si la orden contiene operaciones críticas y el toggle está activo, el envío se suspende hasta que el usuario pulse explícitamente el botón de confirmación.
  3. **Confirmación en Lanzador de Consola (`triggerLaunch`)**:
     - Al pulsar `Iniciar Antigravity` (`#btnLaunchHero` o botón superior), se despliega el modal solicitando confirmación explícita para abrir la terminal con permisos elevados.

---

## [2026-09-28] security & execution | Integración de --dangerously-skip-permissions en Beacon para Ejecución Headless
- **Módulo**: `thunder-ai-control/` (`server.ps1`, `public/app.js`, `public/index.html`)
- **Causa Raíz Diagnosticada**:
  - Al invocar `agy` en modo headless (`-p` / `--print`) desde el backend web de Beacon (`server.ps1`), la IA intentaba ejecutar herramientas del sistema (comandos de terminal o filesystem) que requerían confirmación interactiva.
  - Al no haber una terminal interactiva (TTY) conectada para responder afirmativamente al prompt de permisos, el motor `jetski` abortaba con el error: `agy.exe : jetski: no output produced — a tool required the "command" permission that headless mode cannot prompt`.
- **Acciones Ejecutadas**:
  1. **Backend (`server.ps1`)**:
     - En `Invoke-BeaconChat`, añadido el flag `--dangerously-skip-permissions` a las llamadas de ejecución directa de `agy -p`.
     - En `Launch-AntigravitySession`, preconfigurado `$agyCmd` con `--dangerously-skip-permissions` para que las sesiones interactivas y comandos lanzados arranquen con auto-aprobación de permisos.
  2. **Frontend (`public/app.js` & `public/index.html`)**:
     - Actualizado el generador dinámico de previsualización `updateCmdPreview` y la caja de preview estática con `--dangerously-skip-permissions`.
- **Validación**:
  - Comprobada sintaxis de `server.ps1` y verificado que `agy --dangerously-skip-permissions -p "..."` responde limpiamente sin bloqueos de permisos.

---

## [2026-09-28] ui & telemetry | Implementación de Chat Beacon (Estilo ChatGPT) y Panel de Rendimiento de Tokens
- **Módulo**: `thunder-ai-control/` (`server.ps1`, `public/index.html`, `public/styles.css`, `public/app.js`)
- **Requerimiento del Sr Ramos**:
  1. Chat con estética y ergonomía inspirada en ChatGPT para interactuar y desarrollar directamente en el navegador.
  2. Selector de modelo en cabecera con porcentaje de consumo de la ventana de contexto actualizado a tiempo real.
  3. Módulo analítico "Rendimiento" enfocado en telemetría de tokens, detección de procesos consumidores, auditoría de archivos pesados del repositorio y recomendaciones de optimización.
- **Acciones Ejecutadas**:
  1. **Chat Beacon (ChatGPT Clean Style)**:
     - Contenedor centrado (máx. 820px) en modo claro con streaming de mensajes, avatar de Beacon (`⚡`) y badges de turno.
     - Barra de entrada flotante redondeada (`border-radius: 26px`) con auto-expansión dinámica de altura, envío rápido con `Enter` (salto de línea con `Shift+Enter`) y botón de envío animado.
     - Pantalla de bienvenida con 4 tarjetas de atajo (Auditoría de Economía 1.21.11, Generador DeluxeMenus, Plugins Custom Obsidian y Diagnóstico de Rendimiento).
     - Renderizador Markdown completo con sintaxis para bloques de código, cabeceras de lenguaje y botón de copiado de un clic con feedback visual.
     - Indicador de pensamiento animado con 3 puntos pulsantes.
  2. **Selector de Modelo & Telemetría en Tiempo Real**:
     - Selector dropdown en cabecera: `Gemini 3.8 Flash (1.0M)`, `Gemini 3.8 Pro (2.0M)`, `Gemini Flash-Lite (1.0M)` y `Claude 3.7 Sonnet (200k)`.
     - Píldora de estado en tiempo real (`X.XX% uso | Y.Yk / Z.ZM tok`) con semáforo cromático dinámico (Verde `<30%`, Ámbar `30%-60%`, Rojo `>60%`).
  3. **Panel "Rendimiento" & Optimización de Tokens**:
     - 4 Tarjetas KPI: Tokens Totales de Sesión, Ventana de Contexto Ocupada, Ratio Entrada/Salida y Estado de Salud del Contexto.
     - Desglose porcentual por proceso: Lectura de Archivos Extensos (`view_file`), Historial Acumulado, Salidas de Consola (`run_command`), Generación de Código y Reglas del Sistema (`AGENTS.md`).
     - Auditoría en vivo de los 10 archivos más pesados del repositorio (`.sparkprofile`, `.log`, `.yml`, `.json`, `.md`), con cálculo de tokens potenciales (`~Length/4`), nivel de riesgo y directiva operativa.
     - Protocolos de Red Teaming para mitigación de saturación de ventana (lecturas por rango, exclusión de volcados binarios, segmentación atómica en Obsidian).
  4. **Backend Robusto en PowerShell**:
     - Lector de buffer exacto mediante `ContentLength64` evitando bloqueos por HTTP Keep-Alive.
     - Integración directa con `agy -p` con manejo estricto de banderas (`--model <modelo> --effort high`).
     - Endpoints REST operativos: `POST /api/chat`, `GET /api/chat/history`, `POST /api/chat/clear`, `GET /api/performance`, `POST /api/model`.

---

## [2026-09-28] agent & ui | Transición de Identidad a Beacon y Rediseño Visual en Blanco (Light Mode)
- **Módulo**: `thunder-ai-control/`, `INICIAR_PANEL_BEACON.bat`, `CLAUDE.md`, `AGENTS.md`
- **Requerimiento del Sr Ramos**: Cambio de identidad del agente a **Beacon** y migración integral del diseño gráfico a una interfaz en blanco de alta legibilidad.
- **Acciones Ejecutadas**:
  1. **Rediseño UI Modo Claro (White Theme)**:
     - Paleta de colores migrada a fondo blanco puro (`#ffffff`) con estructura en `Slate 50` (`#f8fafc`), bordes sutiles (`#e2e8f0`) y tipografía de alto contraste (`#0f172a` / `#334155`).
     - Adaptación del motor Canvas del Grafo: enlaces renderizados en gris claro pizarra (`#cbd5e1`), realce ámbar (`#d97706`) y etiquetas oscuras nítidas.
  2. **Transición de Identidad a Beacon**:
     - Actualizado protocolo maestro en `CLAUDE.md` y `AGENTS.md` a **Beacon**.
     - Interfaz web y backend `server.ps1` renombrados a **Beacon // ThunderCerebro Control Center**.
     - Generado lanzador principal `INICIAR_PANEL_BEACON.bat` manteniendo compatibilidad de redirección.

---

## [2026-09-28] wiki & obsidian | Reestructuración Topológica del Grafo, Malla de Referencias Cruzadas y Erradicación de Hojas Muertas
- **Módulo**: `wiki/` (75 archivos), `Plan de Monetizacion/`, `index.md`, `.obsidian/`
- **Diagnóstico Integral (Fase 2)**:
  - 47 archivos en `wiki/` actuaban como "hojas muertas" (Out=0, solo recibían 1 enlace entrante sin proyectar conexiones).
  - 121 archivos Markdown operativos (`skills/`, `.agents/`, `raw/`, `creator/`) aparecían como puntos aislados en Obsidian debido a que `userIgnoreFilters` tenía sintaxis con globs incompatibles (`**`) y `graph.json` no tenía filtro de búsqueda activo.
- **Acciones Ejecutadas**:
  1. **Malla Completa de Referencias Cruzadas en Wiki**: Interconectados los 47 archivos restantes (Core, Economía, RPG, Mazmorras, Protección, Chat, UI, Hardware y Fuentes) añadiendo enlaces bidireccionales, vínculos a hubs (`ecosistema-plugins.md`, `thundermc-master-synthesis.md`) y secciones `## Referencias Cruzadas`.
  2. **Enlazado del Plan de Monetización**: Interconectado `plan-monetizacion-thundermc.md` con el índice maestro, el concepto de monetización y los plugins del stack económico.
  3. **Corrección de Configuración Obsidian**:
     - `.obsidian/app.json`: Sintaxis de `userIgnoreFilters` normalizada a nombres de carpeta canónicos (`skills`, `.agents`, `raw`, `creator`, `thunder-dashboard`).
     - `.obsidian/graph.json`: Filtro predeterminado configurado con `-path:skills -path:.agents -path:raw -path:creator -path:thunder-dashboard` y visualización de flechas de flujo direccional (`showArrow: true`).
- **Métricas Finales**:
  - Archivos aislados en `wiki/` (0 In, 0 Out): **0**
  - Raíces sin entrantes en `wiki/` (In=0): **0**
  - Hojas muertas sin salientes en `wiki/` (Out=0): **0** (Reducido de 47 a 0)
  - Enlaces rotos / no resueltos: **0**
  - Red de conocimiento 100% articulada como malla compleja y navegable.

---

## [2026-09-21] items & mechanics | Creación de Bundle de Recompensas con Animación Actionbar y Probabilidad de Mejora (Sandbox)
- **Módulo**: `creator/lab/bundle_recompensas_test.yml` -> `plugins/ExecutableItems/items/ThunderMC/bundle_recompensas_test.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Arquitectura y Características**:
  1. **Material Base**: `BUNDLE` vanilla 1.21 con glow y protección (`cancel-item-place: true`, `cancel-anvil: true`, `cancelEvent: true`, `detailedSlots: [-1]`).
  2. **Animación Actionbar**: Secuencia de 5 segundos con el sonido bundle (`item.bundle.drop_contents`) con pitch progresivo y barra segmentada `ᴀʙʀɪᴇɴᴅᴏ &e&m &8&m ...` hasta `ᴀʙʀɪᴇɴᴅᴏ ᴄᴏᴍᴘʟᴇᴛᴀᴅᴏ`.
  3. **Sistema Dual: Recompensas vs Probabilidad de Mejora**:
     - Tiradas base (recompensas ordinarias con minerales + economía + sonido `item.bundle.remove_one`):
       - $750 + 64x Carbón
       - $1.000 + 32x Hierro
       - $1.200 + 16x Oro
     - Tiradas de Mejora (Upgrade de calidad entregando la siguiente caja de tier superior con fanfarria sonora, partículas y aviso especial en Actionbar y chat):
       - 50%: Mejora a `cajitaespecial`
       - 28%: Mejora a `cajitarara`
       - 15%: Mejora a `cajitaepica`
       - 5%: Mejora a `cajitamitica`
       - 2%: Mejora a `cajitalegendaria`
  4. **Persistencia Actionbar**: Visualización persistente de 3 segundos con los colores HEX de cada tier sin comillas internas.
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox vía SFTP.

---

## [2026-09-21] economy & items | Reversión a Recompensas Definidas Calibradas y Corrección de Color Hex en Actionbar (Sandbox)
- **Módulo**: `creator/lab/bolsadedinero_test.yml` -> `plugins/ExecutableItems/items/ThunderMC/bolsadedinero_test.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Ajustes Implementados**:
  1. **Migración a Recompensas Definidas Fijas**:
     - Descartado el uso de `%rand%` y variables de ítem por preferencia del Sr Ramos.
     - Implementada la tabla de 12 premios definidos y balanceados ($500, $500, $600, $650, $750, $850, $1.000, $1.200, $1.400, $1.600, $1.800 y Jackpot de $2.000).
     - Cada tirada ejecuta de forma atómica y sincronizada el `eco give`, el sonido correspondiente, las partículas, el mensaje de chat y el Actionbar persistente durante 3 segundos.
  2. **Corrección de Color Hexadecimal**:
     - Retiradas las comillas dobles literales `"..."` que rompían el renderizado de `&#59E91F` en los actionbars concatenados con `+++`.
  3. **Prevención de Ejecución Triple**:
     - `cancelEvent: true` y `detailedSlots: [-1]` mantenidos para bloquear cualquier disparo repetido por interacción de bloques o mano secundaria (offhand).
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox vía SFTP.

---

## [2026-09-21] economy & items | Corrección de Triple Ejecución, Persistencia con Variable y Limpieza Hex en Actionbar (Sandbox)
- **Módulo**: `creator/lab/bolsadedinero_test.yml` -> `plugins/ExecutableItems/items/ThunderMC/bolsadedinero_test.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Correcciones Implementadas**:
  1. **Bloqueo de Ejecución Triple**:
     - Activado `cancelEvent: true` en el activador.
     - Restringido `detailedSlots` estrictamente a `[-1]` (mano principal), eliminando el slot `40` (offhand) que disparaba el evento duplicado.
  2. **Persistencia y Sincronización de Recompensa Aleatoria**:
     - Definida la variable de ítem `premio` (tipo `NUMBER`, default `500.0`).
     - Añadido bloque `variablesModification` en el activador con `SET` a `%rand:500|1800%`.
     - `eco give`, el mensaje de chat y el Actionbar (durante sus 3 segundos de refresco) ahora leen unánimemente `%var:premio%`, garantizando que el dinero pagado coincida al 100% con lo mostrado en pantalla.
  3. **Corrección de Color Hexadecimal en Actionbar**:
     - Retiradas las comillas dobles internas literales `"..."` que rompían la interpretación de `&#59E91F`.
- **Despliegue Remoto**:
  - Subido con éxito al servidor Sandbox vía SFTP.

---

## [2026-09-21] economy & items | Optimización y Simplificación de Recompensas con %rand% y Jackpot Ponderado (Sandbox)
- **Módulo**: `creator/lab/bolsadedinero_test.yml` -> `plugins/ExecutableItems/items/ThunderMC/bolsadedinero_test.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Ajustes Realizados por el Sr Ramos**:
  - Calibración de la secuencia de actionbar con bloques bundle (`item.bundle.drop_contents`), transición de color `#59E91F`/`&e`/`&a` y texto `ᴀʙʀɪᴇɴᴅᴏ ᴄᴏᴍᴘʟᴇᴛᴀᴅᴏ`.
- **Trabajo del Agente**:
  1. **Simplificación Drástica del Código de Recompensa**:
     - Eliminadas las 12 líneas redundantes de probabilidades manuales individuales.
     - Implementado el placeholder de rango nativo de ExecutableItems `%rand:min|max%` (`%rand:500|1800%`).
  2. **Jackpot Independiente de Baja Probabilidad**:
     - Estructurado mediante ponderación nativa en `RANDOM RUN: 1`:
       - `95:` -> Tirada ordinaria dinámica: `eco give %player% %rand:500|1800%` (95% probabilidad).
       - `5:` -> Jackpot extraordinario: `$2.000` con fuegos/totem y fanfarre (5% probabilidad).
- **Despliegue Remoto**:
  - Subido vía SFTP al servidor Sandbox.

---

## [2026-09-21] economy & items | Corrección de Barra de Progreso a Bloques (■) y Color Hex Directo (#59E91F) en Bolsa de Dinero (Sandbox)
- **Módulo**: `creator/lab/bolsadedinero_test.yml` -> `plugins/ExecutableItems/items/ThunderMC/bolsadedinero_test.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Causas Raíz Diagnosticadas y Corregidas**:
  1. **Bug en Barra de Espacios Strikethrough**:
     - El cliente vanilla colapsaba los espacios consecutivos o no mostraba el relleno tachado (`&m &r`), truncando visualmente a 3 caracteres y no evidenciando la progresión de apertura.
     - **Solución**: Sustituido por 5 caracteres de bloque visual `■` con color `#59E91F` (activo) y `&8` (pendiente):
       - Paso 1 (0s): `&fᴀʙʀɪᴇɴᴅᴏ #59E91F■&8■■■■`
       - Paso 2 (1s): `&fᴀʙʀɪᴇɴᴅᴏ #59E91F■■&8■■■`
       - Paso 3 (2s): `&fᴀʙʀɪᴇɴᴅᴏ #59E91F■■■&8■■`
       - Paso 4 (3s): `&fᴀʙʀɪᴇɴᴅᴏ #59E91F■■■■&8■`
       - Paso 5 (4s): `&fᴀʙʀɪᴇɴᴅᴏ #59E91F■■■■■`
  2. **Formato Hexadecimal en Comandos Actionbar y Chat**:
     - Los comandos vanilla `title %player% actionbar` ejecutados desde consola no procesan la sintaxis Bungee `&#RRGGBB`.
     - **Solución**: Migrado a la sintaxis `#RRGGBB` directa (`#59E91F`), garantizando que la recompensa se pinte con el color canónico oficial tanto en el Actionbar (`&fʙᴏʟꜱᴀ ᴀʙɪᴇʀᴛᴀ: #59E91F+$X`) como en el chat (`SEND_MESSAGE #59E91F&l$ &8| &fHas conseguido #59E91F$X &fen tu bolsa de dinero.`).
  3. **Persistencia**: Se mantienen los refrescos de 3 segundos exactos (`DELAY_TICK 20`) para la recompensa final y el cooldown de seguridad de 6s.
- **Despliegue Remoto**:
  - Subido vía SFTP al servidor Sandbox.

---

## [2026-09-21] economy & items | Acústica de Apertura (entity.horse.saddle al Abrir/Finalizar) y Subtítulos Blancos en Bolsas de Dinero (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/bolsadedinero*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Acústica de Apertura de Cuero / Saco**:
     - Trasladado el sonido de montura/silla de montar de caballo al momento exacto de la **finalización y entrega de la recompensa**:
       - `execute at %player% run playsound minecraft:entity.horse.saddle master %player% ~ ~ ~ 0.9 1.1`
     - Se ejecuta simultáneamente con la entrega del dinero, el sonido de levelup y las partículas de aldeano/totem, simulando la apertura física del saco al vaciar las monedas.
  2. **Subtítulos con Custom Font en Blanco (`&f`)**:
     - Fase de animación:
       - `title %player% subtitle "&f&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ..."`
       - `title %player% subtitle "&f&o¡ᴅᴇꜱᴄɪꜰʀᴀᴅᴏ!"`
     - Fase de recompensa:
       - Tiradas estándar: `title %player% subtitle "&f¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!"`
       - Premio máximo: `title %player% subtitle "&f¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!"`
       - Premio supremo (Tier V): `title %player% subtitle "&f¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!"`
- **Despliegue Remoto**:
  - Subidos los 5 archivos actualizados vía SFTP a Sandbox.

---

## [2026-09-21] economy & items | Unificación de Color Temático de Dinero (&#59E91F) en Bolsas de Dinero (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/bolsadedinero*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Color Canónico de Dinero (`&#59E91F`) en Nombre y Premio**:
     - Desvinculado el color de la calidad en el nombre del ítem y en la línea de premio del lore (siguiendo el mismo criterio unificado que los Viales de Almas con `&#00A896`).
     - Fijado el color oficial del dinero del servidor (`&#59E91F` de TAB/Scoreboard) en todas las fases (Tiers I a V):
       - Nombre: `name: '&#59E91FBolsa de Dinero &8[&#59E91F<ROMAN>&8]'`.
       - Lore premio: ` ' &#59E91F• &fPremio: &#59E91F<rango> '`.
     - La línea de calidad (`&8⁂ ...`) preserva su degradado oficial y estrellas según el estándar.
  2. **Estandarización de Mensajes de Chat**:
     - Prefijo `&#59E91F&l$` y `&#59E91F&l★` unificados en las notificaciones de chat de los 5 tiers.
  3. **Preservación de Texturas**:
     - Se mantiene la textura de cabeza personalizada (`material: PLAYER_HEAD` con `headValue`).
- **Despliegue Remoto**:
  - Subidos los 5 archivos actualizados vía SFTP a Sandbox.

---

## [2026-09-21] economy & items | Acústica Combinada de Liberación (Puerta + Cristal + Vex) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  - Se combinó en la fase final de liberación el sonido de ruptura física con el efecto espectral de almas:
    1. `minecraft:entity.zombie.break_wooden_door` (volumen: `0.9`, pitch: `1.1`): Ruptura contundente de la puerta/sello.
    2. `minecraft:block.amethyst_cluster.hit` (volumen: `1.1`, pitch: `2.0`): Resonancia brillante de cristal.
    3. `minecraft:entity.vex.death` (volumen: `0.85`, pitch: `1.25`): Gemido/chillido espectral característico de las almas liberadas.
  - En tiradas de Premio Máximo y Premio Supremo se añade simultáneamente el fanfarre de logro (`ui.toast.challenge_complete`).
- **Despliegue Remoto**:
  - Subidos los 5 archivos actualizados vía SFTP a Sandbox.

---

## [2026-09-21] economy & items | Restauración de Lore en Viales de Almas (Tier I a V) desactivando hideTooltip (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Causa Raíz Diagnosticada**:
  - En Minecraft 1.20.5+/1.21, el componente `minecraft:hide_tooltip` oculta por completo toda la caja flotante de información del ítem (incluyendo el lore personalizado configurado en el plugin).
  - Al haberse activado `hideTooltip: true` en la sección `hiders:`, el cliente de Minecraft suprimía por diseño el lore entero del vial.
- **Corrección Aplicada**:
  - Se configuró `hideTooltip: false` y `hideToolTip: false` manteniendo `hideAdditionalTooltip: true` y `hidePotionEffects: true` en los 5 tiers (`vialdealmas.yml` a `vialdealmas_5.yml`).
  - Esto suprime las estadísticas vanilla del efecto Bad Omen (`OMINOUS_BOTTLE`) sin afectar la visibilidad del lore corporativo.
- **Despliegue Remoto**:
  - Subidos los 5 archivos corregidos a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Corrección de Casing y Activación de hideTooltip (1.20.5+/1.21) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Auditoría de Bytecode en SCore (`Hiders.class`)**:
     - Se auditó la clase interna `com.ssomar.score.features.custom.hiders.Hiders` del JAR `SCore-5.26.5.17.jar`.
     - Hallazgo crítico:
       - En versiones de Minecraft 1.20.5 y superiores (como la 1.21.11 en uso), los componentes vanilla de pociones y Bad Omen no se controlan únicamente por `HIDE_POTION_EFFECTS`, sino por la nueva flag de componentes de item `HIDE_ADDITIONAL_TOOLTIP` y la bandera `hideTooltip`.
       - La clave de configuración en SCore tiene distinción de mayúsculas/minúsculas: `hideTooltip` (con `tip` en minúsculas) y estaba fijada erróneamente en `hideToolTip: false`.
  2. **Corrección Aplicada**:
     - Activadas simultáneamente en los 5 tiers:
       ```yaml
       hiders:
         hideEnchantments: true
         hideUnbreakable: true
         hideAttributes: true
         hidePotionEffects: true
         hideAdditionalTooltip: true
         hideTooltip: true
         hideToolTip: true
       ```
  3. **Despliegue Remoto**:
     - Subidos los 5 archivos corregidos a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Nuevo Sonido de Liberación (entity.zombie.break_wooden_door) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Acústica de Ruptura de Puerta**:
     - Sustituido el sonido de vex por el sonido contundente de ruptura de madera:
       - `minecraft:entity.zombie.break_wooden_door` (volumen: `0.9`, pitch: `1.1`): Ruptura de sello/puerta de almas.
       - Combinado con `minecraft:block.amethyst_cluster.hit` (volumen: `1.1`, pitch: `2.0`): Resonancia de cristal.
  2. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Subtítulos de Animación ("ʟɪʙᴇʀᴀɴᴅᴏ..." y "¡ʟɪʙᴇʀᴀᴅᴏ!") en Blanco (&f) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Subtítulos de Fase de Animación en Blanco (`&f`)**:
     - Modificados los subtítulos de la fase previa de descifrado/liberación a color blanco:
       - `title %player% subtitle "&f&oʟɪʙᴇʀᴀɴᴅᴏ..."`
       - `title %player% subtitle "&f&o¡ʟɪʙᴇʀᴀᴅᴏ!"`
     - Los títulos ofuscados se mantienen exclusivamente en `&3` (`&3&k||||`, `&3&l&k||||||`, etc.).
  2. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Animación y Títulos 100% Monocolor &3 (Dark Aqua) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de Colores Intercalados en Animación**:
     - Eliminado cualquier color intercalado (`&b`, etc.) en la secuencia de animación y subtítulos.
     - Fijado exclusivamente el color `&3` de principio a fin:
       - Subtítulos: `&3&oʟɪʙᴇʀᴀɴᴅᴏ...` y `&3&o¡ʟɪʙᴇʀᴀᴅᴏ!`.
       - Títulos ofuscados: `&3&k||||`, `&3&l&k||||||`, `&3&k||||||` y `&3&l&k||||`.
  2. **Títulos de Recompensa 100% en &3**:
     - Tiradas regulares: `title %player% title "&3+<cantidad> Almas"`.
     - Premio máximo / supremo: `title %player% title "&3★ &3+<cantidad> Almas &3★"`.
     - Subtítulo de entrega permanece en blanco limpio (`&f¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!`).
  3. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Color Temático &3 (Dark Aqua) en Animación y Títulos de Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Animación Matricial con `&3`**:
     - Adaptada la secuencia de 19 ticks al tono `&3` (Dark Aqua) intercalado con `&b` (Aqua claro):
       - `title %player% subtitle "&3&oʟɪʙᴇʀᴀɴᴅᴏ..."`
       - `title %player% title "&3&k||||"`
       - `title %player% title "&3&l&k||||||"`
       - `title %player% subtitle "&b&oʟɪʙᴇʀᴀɴᴅᴏ..."`
       - `title %player% title "&3&k||||&b&k||"`
       - `title %player% subtitle "&b&o¡ʟɪʙᴇʀᴀᴅᴏ!"`
  2. **Títulos de Recompensa con `&3`**:
     - Tiradas regulares: `title %player% title "&3+<cantidad> Almas"` (ej. `&3+10 Almas`, `&3+50 Almas`, `&3+200 Almas`, `&3+600 Almas`, `&3+2.000 Almas`).
     - Premio máximo / supremo: `title %player% title "&b★ &3+<cantidad> Almas &b★"`.
     - Subtítulo en blanco: `title %player% subtitle "&f¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!"`.
     - Mensajes de chat sincronizados con prefijo `&3&l✧`.
  3. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Reincorporación de "Almas" en Títulos de Recompensa de Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Títulos con Cantidad + "Almas"**:
     - Modificado el título de entrega de recompensa para que acompañe el nombre de la moneda:
       - Tiradas estándar: `title %player% title "&b+<cantidad> &9Almas"` (ej. `&b+10 &9Almas`, `&b+50 &9Almas`, `&b+2.000 &9Almas`).
       - Premio máximo / supremo: `title %player% title "&9★ &b+<cantidad> &9Almas &9★"` (ej. `&9★ &b+40 &9Almas &9★`, `&9★ &b+5.000 &9Almas &9★`).
     - El lore de premio se mantiene con el rango numérico limpio (` ' &#00A896• &fPremio: &#00A896<rango> '`).
  2. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Subtítulos de Recompensa en Blanco (&f) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Subtítulos en Blanco (`&f`)**:
     - Actualizados los subtítulos de recompensa final a color blanco limpio:
       - Tiradas estándar: `title %player% subtitle "&f¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!"`.
       - Premio máximo: `title %player% subtitle "&f¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!"`.
       - Premio supremo (Tier V): `title %player% subtitle "&f¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!"`.
  2. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Acústica Espectral de Liberación (entity.vex.death + block.amethyst_cluster.hit) en Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Diseño Acústico Espectral Multicapa**:
     - Sustituido el sonido genérico de subida de nivel (`entity.player.levelup`) por la combinación de sonidos requerida:
       - `minecraft:entity.vex.death` (volumen: `0.85`, pitch: `1.25`): Efecto chillido/gemido espectral de alma liberada.
       - `minecraft:block.amethyst_cluster.hit` (volumen: `1.1`, pitch: `2.0`): Efecto resonante de cristal/vidrio roto.
     - En tiradas de Premio Máximo y Premio Supremo se superpone la combinación espectral junto con el fanfarre de logro (`ui.toast.challenge_complete`).
  2. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Actualización al Color Actual de Almas de la Scoreboard (&#00A896) en Viales y Menús (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas*.yml`, `plugins/ShopGUIPlus/shops/almas.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Auditoría de Color en TAB (Scoreboard)**:
     - Verificada la configuración en `plugins/TAB/config.yml` en la línea de Almas de la scoreboard: `&#00A896| &fAlmas: &#00A896%thundercurrencys_almas%`.
     - Color canónico oficial actual: `&#00A896` (turquesa/esmeralda abisal).
  2. **Actualización Completa en Viales de Almas (Tier I a V)**:
     - Reemplazado el color previo (`&#34B0F3`) por el color actual de la scoreboard (`&#00A896`):
       - Nombre: `name: '&#00A896Vial de Almas &8[&#00A896<ROMAN>&8]'`.
       - Lore premio: ` ' &#00A896• &fPremio: &#00A896<rango> '`.
  3. **Migración en Configuraciones Previas**:
     - Actualizado `plugins/ShopGUIPlus/shops/almas.yml`: cabecera cambiada a `&8Almas &8(#00A896🔥&8)`.
     - Actualizado `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`: slot 53 sincronizado a `&#00A896`.
  4. **Despliegue Remoto**:
     - Subidos los 7 archivos actualizados al servidor Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Unificación de Color Temático de Almas (&#34B0F3) en Nombre y Lore de Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas.yml`, `vialdealmas_2.yml`, `vialdealmas_3.yml`, `vialdealmas_4.yml`, `vialdealmas_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Color Canónico de Almas (`&#34B0F3`) en Nombre y Premio**:
     - Desvinculado el color de la categoría/calidad en el nombre del ítem y en la línea de premio del lore.
     - Fijado el color oficial de las almas del servidor (`&#34B0F3`) en todas las fases (Tiers I a V):
       - Nombre: `name: '&#34B0F3Vial de Almas &8[&#34B0F3<ROMAN>&8]'`.
       - Lore premio: ` ' &#34B0F3• &fPremio: &#34B0F3<rango> '`.
     - La línea de calidad (`&8⁂ ...`) preserva su degradado oficial intacto según el estándar.
  2. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Eliminación del Sufijo "Almas" en Lore y Títulos de Viales de Almas (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas.yml`, `vialdealmas_2.yml`, `vialdealmas_3.yml`, `vialdealmas_4.yml`, `vialdealmas_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de "Almas" en Lore**:
     - Eliminada la palabra "Almas" al final de la línea de premio, quedando estrictamente el rango numérico formateado: `' <hex>• &fPremio: <hex><rango> '` (ej. ` ' &#3CDB10• &fPremio: &#3CDB1010-40 '`).
  2. **Purga de "Almas" en Títulos de Recompensa**:
     - Títulos regulares: `title %player% title "&b+<cantidad>"` (ej. `&b+10`, `&b+50`, `&b+200`, `&b+600`, `&b+2.000`).
     - Títulos de premio máximo / supremo: `title %player% title "&9★ &b+<cantidad> &9★"` (ej. `&9★ &b+40 &9★`, `&9★ &b+5.000 &9★`).
  3. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados a `plugins/ExecutableItems/items/ThunderMC/` en Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Ajustes en Viales de Almas: Ocultación de Bad Omen, Color Temático Azul/Cian y Purga de Ícono en Lore (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas.yml`, `vialdealmas_2.yml`, `vialdealmas_3.yml`, `vialdealmas_4.yml`, `vialdealmas_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ocultación de Atributo de Efecto de Poción (Bad Omen)**:
     - Activadas las banderas en `hiders`: `hidePotionEffects: true` y `hideAdditionalTooltip: true` para suprimir la información de efecto Bad Omen que Minecraft muestra por defecto en `OMINOUS_BOTTLE`.
  2. **Purga del Ícono en Lore**:
     - Eliminado el símbolo (`✧`) al final de la línea de premio en el lore, quedando limpio: `' <hex>• &fPremio: <hex><rango> Almas '`.
  3. **Paleta Temática de Almas en Títulos y Notificaciones**:
     - Modificados los títulos y subtítulos de recompensa hacia la paleta espiritual (`&b` cian / `&9` azul oscuro):
       - Título regular: `title %player% title "&b+<cantidad> &9Almas"`.
       - Título premio máximo / supremo: `title %player% title "&9★ &b+<cantidad> &9Almas &9★"`.
       - Subtítulos: `&b¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!`, `&b¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!`, `&b¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!`.
       - Mensaje de chat: `&b&l✧ &8| &fHas liberado &b<cantidad> &9Almas &fen tu vial.`
  4. **Despliegue Remoto**:
     - Subidos los 5 archivos actualizados vía SFTP al Sandbox.

---

## [2026-09-17] economy & items | Creación y Despliegue de Viales de Almas (Tier I a V) en ExecutableItems (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/vialdealmas.yml`, `vialdealmas_2.yml`, `vialdealmas_3.yml`, `vialdealmas_4.yml`, `vialdealmas_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Material OMINOUS_BOTTLE & Estándar Visual**:
     - Creados los 5 tiers utilizando `material: OMINOUS_BOTTLE` de Minecraft 1.21.
     - Lore estilizado y uniforme idéntico a las Bolsas de Dinero, sin tildes:
       - Header: `&8ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ`
       - Descripción: `' &7Vial con almas '` / `' &7para el mercado.'`
       - Premio: `' <hex>• &fPremio: <hex><rango> ✧ '`
       - Calidad: Escala canónica oficial (SUPER, RARA, EPICA, MITICA, DIVINA) con sangría inicial.
       - Footer: `&7▶ ᴄʟɪᴄᴋ ᴅᴇʀ - ʟɪʙᴇʀᴀʀ`.
  2. **Curva de Economía de Almas (ThunderCurrencys / Mercado)**:
     - **Tier I (SUPER)**: 10 a 40 Almas (`playerpoints:p give %player% ...`).
     - **Tier II (RARA)**: 50 a 150 Almas.
     - **Tier III (EPICA)**: 200 a 500 Almas.
     - **Tier IV (MITICA)**: 600 a 1.500 Almas (`disableStack: true`).
     - **Tier V (DIVINA)**: 2.000 a 5.000 Almas (`disableStack: true`, cooldown 3s).
  3. **Animación Matricial & Títulos Sanitizados (Sin Negrita, Verde &a, Sin Tildes)**:
     - Títulos en `&a+<cantidad> Almas` y Premio Máximo `&2★ &a+<cantidad> Almas &2★`.
     - Subtítulos en Small Caps: `&2&oʟɪʙᴇʀᴀɴᴅᴏ...`, `&a&oʟɪʙᴇʀᴀɴᴅᴏ...`, `&a&o¡ʟɪʙᴇʀᴀᴅᴏ!`, `&a¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!`, `&a¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!` y `&a¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!`.
     - Sonidos y partículas nativas de alta inmersión (`amethyst_block.hit`, `note_block.pling`, `entity.player.levelup`, `totem`, `villager_happy`).
  4. **Despliegue Remoto**:
     - Subidos los 5 archivos vía SFTP a Sandbox (`ymykh9qy.274758bd`).

---

## [2026-09-17] economy & items | Purga de Tildes en Textos Visibles de Bolsas de Dinero (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/bolsadedinero.yml`, `bolsadedinero_2.yml`, `bolsadedinero_3.yml`, `bolsadedinero_4.yml`, `bolsadedinero_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga Completa de Caracteres con Tilde**:
     - Eliminadas todas las tildes ortográficas en textos visibles al jugador para evitar fallos de renderizado y detección de glifos en Minecraft:
       - Subtítulos: `&a¡ᴘʀᴇᴍɪᴏ ᴍᴀ́xɪᴍᴏ!` -> `&a¡ᴘʀᴇᴍɪᴏ ᴍᴀxɪᴍᴏ!` (reemplazada la letra pequeña combinada `ᴀ́` con acento agudo por la forma limpia `ᴀ`).
       - Lore: `' &7para tu economía.'` -> `' &7para tu economia.'`.
       - Mensajes de chat: `¡Premio máximo de...` -> `¡Premio maximo de...`.
  2. **Despliegue Remoto**:
     - Actualizados y subidos los 5 archivos al servidor Sandbox vía SFTP.

---

## [2026-09-17] economy & items | Corrección de Títulos (Verde &a sin Negrita) y Subtítulos en Small Caps en Bolsas de Dinero (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/bolsadedinero.yml`, `bolsadedinero_2.yml`, `bolsadedinero_3.yml`, `bolsadedinero_4.yml`, `bolsadedinero_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Títulos de Recompensa Estandarizados**:
     - Eliminados todos los códigos hexadecimales en los títulos finales (`/title %player% title ...`).
     - Fijado el color verde canónico `&a` de forma estricta para la cantidad ganada en todas las tiradas de todos los tiers (ej. `&a+$500`, `&a+$2.500`, `&a+$10.000`, `&a+$40.000`, `&a+$120.000`).
     - Eliminado el formato negrita (`&l`) de las cantidades ganadas.
     - Títulos de premio máximo / supremo unificados a formato sin negrita: `&2★ &a+$... &2★`.
  2. **Subtítulos con Tipografía Small Caps (Custom Font)**:
     - Secuencia de animación de descifrado:
       - `&2&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ...`
       - `&a&oᴅᴇꜱᴄɪꜰʀᴀɴᴅᴏ...`
       - `&a&o¡ᴅᴇꜱᴄɪꜰʀᴀᴅᴏ!`
     - Subtítulos de entrega de recompensa:
       - Tiradas estándar: `&a¡ʀᴇᴄᴏᴍᴘᴇɴꜱᴀ ᴏʙᴛᴇɴɪᴅᴀ!`
       - Premio máximo: `&a¡ᴘʀᴇᴍɪᴏ ᴍᴀ́xɪᴍᴏ!`
       - Premio supremo (Tier V): `&a¡ᴘʀᴇᴍɪᴏ ꜱᴜᴘʀᴇᴍᴏ!`
  3. **Despliegue Remoto**:
     - Actualizados y subidos los 5 archivos vía SFTP a `plugins/ExecutableItems/items/ThunderMC/` en el servidor Sandbox (`ymykh9qy.274758bd`).

---

## [2026-09-17] economy & items | Homogeneización, Textura Unificada y Calidades Predefinidas en Bolsas de Dinero (Tier I a V) (Sandbox)
- **Módulo**: `plugins/ExecutableItems/items/ThunderMC/bolsadedinero.yml`, `bolsadedinero_2.yml`, `bolsadedinero_3.yml`, `bolsadedinero_4.yml`, `bolsadedinero_5.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Textura de Cabeza Unificada**:
     - Asignada a todos los Tiers (I al V) la textura oficial de bolsa de monedas (`headValue: eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvMWMzYjRkMWVjMjk4NDc3NDQwYjJjMDA1N2QzYTUzOTNiOWQzZjBiODBkZGE4MTg0YmU1MTQ2M2E5OWFiOWMyZSJ9fX0=`).
  2. **Calidades y Línea de Premio en Lore (Estándar Canónico Oficial)**:
     - Integrada la escala exacta con sangría/margen de espacio inicial (` ' &8⁂ ...'`).
     - Color de nombre de ítem y de la línea de premio unificados con el **último código hexadecimal** de cada calidad, incorporando espacio final derecho de margen en el premio (`' <hex>• &fPremio: <hex><rango> '`):
       - **Tier I** (`&#3CDB10`): ` ' &#3CDB10• &fPremio: &#3CDB10$500-$2K '`
       - **Tier II** (`&#1DC8FF`): ` ' &#1DC8FF• &fPremio: &#1DC8FF$2.5K-$8K '`
       - **Tier III** (`&#732AE2`): ` ' &#732AE2• &fPremio: &#732AE2$10K-$30K '`
       - **Tier IV** (`&#D02626`): ` ' &#D02626• &fPremio: &#D02626$40K-$100K '`
       - **Tier V** (`&#EFFF00`): ` ' &#EFFF00• &fPremio: &#EFFF00$120K-$300K '`
     - Corregido el lore descriptivo cambiando la referencia a "monedas" por "dinero" (`' &7Bolsa con dinero '` / `' &7Saco con dinero '`) conforme a la economía oficial del servidor.
     - Documentado formalmente en `wiki/concepts/estandar-calidades-items.md` e indexado en `index.md`.
  3. **Animación Matricial & Feedback**:
     - 19 ticks de descifrado verde ofuscado (`&a&k||||`), curva de amatista progresiva (pitch 1.0 a 1.7) con remate `pling` (pitch 2.0).
     - Feedback unificado: `&a¡Recompensa obtenida!` y pantalla estelar para Premio Máximo.
  4. **Despliegue**: Subidos los 5 archivos al servidor Sandbox vía SFTP y validados.

---

## [2026-09-15] economy & items | Migración de ExecutableItems, Ecosistema de Bolsas de Dinero (Tier I a V) y Animación Matricial (Sandbox)
- **Módulo**: `plugins/ExecutableItems/`, `plugins/SCore/`, Servidor Survival (`ymykh9qy.575c7473`) -> Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Migración Completa de Plugins**:
     - Transferidos desde Survival a Sandbox los binarios `ExecutableItems_Prem-7.26.5.17.jar`, `SCore-5.26.5.17.jar` y las carpetas completas `ExecutableItems/` y `SCore/`.
  2. **Rediseño Visual de Bolsa de Dinero (Tier I)**:
     - Actualizado `bolsadedinero.yml` a formato compacto horizontal (máximo 19 caracteres visibles por línea).
     - Activadas banderas de ocultación (`hideAttributes`, `hideEnchantments`, `hideUnbreakable`).
  3. **Jerarquización de Tiers II a V**:
     - Auditada la escala de costes de RankUp (de Knight a Titan).
     - Diseñados, generados y desplegados 4 nuevos tiers en Sandbox: `bolsadedinero_2.yml` (Heroe, $2.5K-$8K), `bolsadedinero_3.yml` (Legend, $10K-$30K), `bolsadedinero_4.yml` (Mythic, $40K-$100K) y `bolsadedinero_5.yml` (Titan, $120K-$300K).
     - Configuradas texturas de cabeza distintivas, `disableStack: true` para mitigar exploits/alts en Tiers IV-V, y sincronización atómica con `RANDOM RUN: 1`.
  4. **Animación de Descifrado Verde (`&a&k||||`)**:
     - Reestructurada la apertura de `bolsadedinero.yml` eliminando códigos hexadecimales incompatibles con `/title`.
     - Implementada secuencia de 19 ticks de descifrado con ofuscación matricial (`&a&k||||`) y sonido progresivo (`amethyst_block.hit` -> `pling` -> `levelup`/`toast`), manteniéndose 100% en paleta verde (`&a` y `&2`).
  5. **Despliegue**: Todos los archivos validados y subidos vía SFTP al Sandbox con éxito.

---

## [2026-09-14] ui & gui | Reinstalación de Cristales Grises en Navbars Superior e Inferior (Sandbox)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta_2.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa_2.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Marco Superior (`slots: 0-3, 5-8`)**: Reinstalados los cristales grises (`GRAY_STAINED_GLASS_PANE`) flanqueando la cabecera central del menú.
  2. **Marco Inferior (`slots: 46, 47, 48, 50, 51`)**: Reinstalados los cristales grises entre el botón de alternar (slot 45), volver (slot 49), venta rápida (slot 52) y tu economía (slot 53).
  3. **Zona Central Abierta**: Filas 2 y 3 se mantienen totalmente transparentes sin relleno gris invasivo, con los cristales de tendencia coloreados colocados directamente bajo cada ítem.
  4. **Despliegue**: Subidos los 4 archivos vía SFTP a Sandbox con éxito.

---

## [2026-09-14] ui & gui | Purga de Cristales en Navbars Superior e Inferior (Sandbox)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta_2.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa_2.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga Completa de Cristales de Relleno en Navbars**:
     - Eliminados todos los cristales grises del marco superior (slots 0-3 y 5-8).
     - Eliminados todos los cristales grises de la barra inferior (slots 46, 47, 48, 50, 51).
     - Eliminados los marcos laterales. Toda la interfaz queda 100% limpia, transparente y minimalista.
  2. **Preservación Exclusiva de los Cristales de Tendencia**:
     - Se conservan únicamente los cristales coloreados colocados inmediatamente debajo de cada ítem de venta (fila 4) para marcar su tendencia de mercado (verde lima para alza, amarillo/gris para estable, rojo para baja).
  3. **Disposición Final de la Barra Inferior (Limpia y Funcional)**:
     - **Slot 45 (Abajo Izquierda)**: Botón para alternar categoría (`SPAWNER` en Pág. 1 / `WHEAT` en Pág. 2).
     - **Slot 49 (Centro)**: Botón de volver atrás (`DARK_OAK_DOOR`).
     - **Slot 52 (Penúltimo Derecha)**: Venta Rápida (`HOPPER`).
     - **Slot 53 (Derecha del Todo)**: Tu Economía (`head-%player_name%`).
  4. **Despliegue**: Subidos los 4 menús actualizados vía SFTP a Sandbox con éxito.

---

## [2026-09-14] ui & gui | Cristales de Tendencia Inferiores y Reorganización de Navbar (Sandbox)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta_2.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa_2.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de Cristales Grises de Fondo**:
     - Eliminado el relleno gris invasivo en las filas centrales. Los ítems quedan limpios y flotantes con marcos únicamente laterales (slots 9, 17, 18, 26, 27, 35, 36, 44).
  2. **Cristal de Tendencia Bajo Cada Ítem**:
     - Colocado inmediatamente debajo de cada producto (fila 4: slots 28 a 34 o 29 a 34) el cristal teñido del color de su tendencia:
       - Verde (`LIME_STAINED_GLASS_PANE`): `&#59E91F▲ En Auge (+15% / +12% / +8%)`.
       - Amarillo (`YELLOW_STAINED_GLASS_PANE`): `&#FFF275= Estable (+4% / +2%)`.
       - Gris (`GRAY_STAINED_GLASS_PANE`): `&7= Regular (0%)`.
       - Rojo (`RED_STAINED_GLASS_PANE`): `&#FF4D4D▼ A la Baja (-4% / -8%)`.
  3. **Purga de la Sección de Tendencia en el Lore**:
     - Eliminadas las líneas de historial/tendencia del lore de cada ítem, dejando únicamente la categoría, el precio por unidad y el precio por stack x64.
  4. **Reorganización Completa de la Barra Inferior (Navbar)**:
     - **Slot 45 (Abajo Izquierda)**: Botón interactivo para alternar entre categorías (`SPAWNER` en Pág. 1 para ir a Mobs; `WHEAT` en Pág. 2 para ir a Cultivos).
     - **Slot 49 (Centro)**: Botón de volver atrás (`DARK_OAK_DOOR`).
     - **Slot 52 (Penúltimo Derecha)**: Botón de Venta Rápida (`HOPPER` con comando `/sellgui`).
     - **Slot 53 (Derecha del Todo)**: Botón de Tu Economía (`head-%player_name%` con dinero, almas, zafiros y nivel).
  5. **Despliegue**: Subidos los 4 menús actualizados vía SFTP a Sandbox con éxito.

---

## [2026-09-14] economy & balance | Purga Estricta: 7 Cultivos Oficiales y 6 Spawners con Curva por Dificultad
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta_2.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa_2.yml`, `plugins/SmartSpawner/item_prices.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga Total de Ítems Relleno**:
     - Eliminados todos los cultivos secundarios y mob drops genéricos.
     - Reducido estrictamente a los **7 Cultivos Oficiales** (Pág. 1) y los **6 Mob Drops Oficiales de Spawners** (Pág. 2).
  2. **Calibración de la Curva de Dificultad (Cultivos)**:
     - **Dificultad Alta (Manual / Nether / Jungla)**: Verruga ($18.00/u - $1,152/stack), Cacao ($16.00/u - $1,024/stack).
     - **Dificultad Media (Manual Clásica)**: Trigo ($10.00/u - $640/stack).
     - **Dificultad Baja (Masiva con Fortuna)**: Zanahoria ($5.50/u - $352/stack), Patata ($5.00/u - $320/stack).
     - **Automatizable (Pistones / Redstone)**: Calabaza ($4.00/u - $256/stack), Caña de Azúcar ($2.50/u - $160/stack).
  3. **Curva Equilibrada de Mob Drops (Precios 1:1 con Lonja)**:
     - Super (Zombie): $1.50 | Rara (Slime): $6.50 | Épica (Enderman): $14.00 | Legend (Blaze): $22.00 | Mítica (Magma Cube): $32.00 | Limited (Breeze): $45.00.
     - El diferencial con los cultivos es un **+25% a +35%**, lo bastante significativo para motivar a cultivar activamente sin dejar obsoletos a los spawners.
  4. **Diseño Visual Compacto en 2 Páginas**:
     - Textos horizontales breves (2-3 palabras por línea), sin relleno.
     - Ambas interfaces (`/lonja` y `/objetosdeventa`) presentan el mismo catálogo limpio.
  5. **Despliegue**: Subidos los 5 archivos vía SFTP a Sandbox con éxito.

---

## [2026-09-14] economy & balance | Unificación de Precios 1:1 y Separación en 2 Páginas (Cultivos vs Mobs)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta_2.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa_2.yml`, `plugins/SmartSpawner/item_prices.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Unificación de Precios 1:1 (Spawner vs Lonja)**:
     - Eliminado el diferencial del 35%: vender un drop de mob en el spawner o en la Lonja paga exactamente la misma cantidad.
     - `item_prices.yml` sincronizado al 100% con los valores oficiales de la Lonja.
  2. **Diferenciación Económica Radical (Cultivos Óptimos vs Mob Drops Moderados)**:
     - **Cultivos (Motor Activo)**: Precios muy generosos (hasta $45.00/u y $2,880/stack en Cacao/Verruga; Trigo a $35.60 y $2,278/stack).
     - **Mob Drops (Renta Pasiva)**: Precios moderados/bajos (Zombies a $1.00, Huesos a $5.50, Slime a $11.00, Blaze a $26.00).
  3. **Estructura en 2 Páginas en la Lonja (`/lonja`) y en `/objetosdeventa`**:
     - **Página 1**: Exclusiva de **Cultivos de Macrogranjas** (21 ítems agrícolas con lore compacto y cabecera verde de "Venta Más Óptima").
     - **Página 2**: Exclusiva de **Drops de Mobs y Spawners** (19 mob drops con cabecera naranja de "Renta Pasiva" y precios unificados).
     - Botones de navegación bidireccionales con sonido y flechas en slots 48/50.
  4. **Despliegue**: Subidos los 6 archivos vía SFTP a Sandbox con éxito.

---

## [2026-09-14] economy & progression | Calibración de 6 Calidades Lineales con Almas en SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/config.yml`, `plugins/SmartSpawner/item_prices.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Configuración de Tiers en SmartSpawner (`config.yml`)**:
     - **Super (Zombie)**: Delay 60s, 1 pág (45 slots), 150 Almas.
     - **Rara (Slime)**: Delay 50s, 1 pág (45 slots), 350 Almas.
     - **Épica (Enderman)**: Delay 40s, 2 págs (90 slots), 800 Almas.
     - **Legend (Blaze)**: Delay 30s, 2 págs (90 slots), 1,800 Almas.
     - **Mítica (Magma Cube)**: Delay 20s, 3 págs (135 slots), 4,000 Almas.
     - **Limited (Breeze)**: Delay 15s, 4 págs (180 slots), 10,000 Almas.
  2. **Ajuste de Precios en `item_prices.yml`**:
     - Agregado `BREEZE_ROD: 35.00` (Lonja: $52.00) para el spawner Limited.
  3. **Reestructuración Completa del Menú `/objetosdeventa`**:
     - Fila 2: Cabezas con textura custom de los 6 spawners con lore ultra-compacto horizontalmente, desglose de precio en Almas, delay, páginas de almacén, y rendimiento exacto tanto base (x1) como máximo (x32).
     - Fila 3: Los 6 drops representativos de cada calidad con precio unitario y por stack x64.
     - Fila 4: 3 paneles informativos de auditoría: Adquisición con Almas, Escalamiento Lineal de velocidad/almacén y Protección Anti-Colapso por saturación de inventario.
  4. **Despliegue**: Subidos los 3 archivos vía SFTP a Sandbox con éxito.

---

## [2026-09-14] economy & balance | Menú de Pruebas ObjetosDeVenta y Expansión de Spawners x32 (Sandbox)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/objetosdeventa.yml`, `plugins/DeluxeMenus/config.yml`, `plugins/SmartSpawner/config.yml`, `plugins/SmartSpawner/item_prices.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Expansión de Apilado a 32 Spawners (`config.yml`)**:
     - Configurado `max_stack_size: 32` en las propiedades por defecto de SmartSpawner para brindar un techo de progresión amplio a granjas AFK.
  2. **Calibración y Despliegue de `item_prices.yml`**:
     - Precios de venta directa sincronizados con la Lonja con un diferencial protector del ~30-35% (Zombie: $1.00, Esqueleto: $5.50 / $1.40, Araña: $20.00 / $1.20, Slime: $11.00, Magma: $30.00, Blaze: $26.00, Enderman: $18.00).
  3. **Creación del Menú `/objetosdeventa` (DeluxeMenus)**:
     - Estructurado en 54 slots con diseño corporativo ThunderMC:
       - Fila 2 (Verde): Los 7 cultivos clave para macrogranjas (Verruga, Trigo, Zanahoria, Patata, Calabaza, Sandía, Caña) con sus precios unidad y stack x64 en Lonja.
       - Fila 3 (Naranja): Los 7 drops de spawners oficiales con comparativa explícita de precio Lonja vs. venta directa en Spawner.
       - Fila 4: Paneles informativos de reglas de spawners (apilado x32, delay 60s, 0% no apilables), reglas de macrogranjas (0 lag, 100% Lonja) y explicación del margen del 35%.
  4. **Registro en `DeluxeMenus/config.yml`**:
     - Registrado el menú bajo la clave `objetosdeventa` y comandos `/objetosdeventa`, `/objetosventa`, `/testventa`.
  5. **Despliegue**: Todos los archivos subidos vía SFTP al servidor de Pruebas con éxito.

---

## [2026-09-14] ui & gui | Compactación de Lores y Depuración de Placeholder en Almacén (Sandbox)
- **Módulo**: `plugins/SmartSpawner/language/en_US/gui.yml`, `creator/lab/smartspawner_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de Placeholder Roto en Almacén (`sell_button`)**:
     - El botón del almacén (`sell_button`) no parsea `{total_sell_price}` en tiempo real en la vista de almacenamiento (el motor de SmartSpawner solo lo evalúa en el menú de confirmación `gui_title_sell_confirm` / `button_sell_info`).
     - Eliminada la línea de ganancia no parseada para evitar mostrar texto roto o placeholders literales.
  2. **Compactación Horizontal de Lores**:
     - Acortadas todas las líneas de lore de `sell_button`, `drop_page_button`, `button_sell_cancel`, `button_sell_confirm` y `button_sell_info`.
     - Textos ajustados a 2-3 palabras por línea con saltos visuales limpios, evitando cuadros de diálogo ensanchados en pantalla.
  3. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] ui & gui | Estandarización Visual del Menú de Confirmación de Venta (Sandbox)
- **Módulo**: `plugins/SmartSpawner/language/en_US/gui.yml`, `creator/lab/smartspawner_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Título del Menú (`gui_title_sell_confirm`)**: Actualizado a `&0&l|&r &0Spawner ▶ &8Confirmar Venta`.
  2. **Botón Cancelar (`button_sell_cancel`)**: Estilizado con color de error corporativo `&#FF4D4D✘ Cancelar` y lore de acción `&7▶ Clic para cancelar`.
  3. **Botón Confirmar (`button_sell_confirm`)**: Estilizado con color de éxito corporativo `&#59E91F✔ Confirmar Venta`, subcabecera `&8ᴠᴇɴᴛᴀ ᴅɪʀᴇᴄᴛᴀ`, ganancia `&#59E91F&l$&r&#59E91F{total_sell_price}` y call to action `&7▶ Clic para confirmar`.
  4. **Botón Resumen Central (`button_sell_info`)**: Estilizado con amarillo corporativo `&#FFF275Resumen de Venta`, desglose de entidad, cantidad de ítems y ganancia total estimada.
  5. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] mechanics | Reactivación de Recolección de Spawners Colocados (Sandbox)
- **Módulo**: `plugins/SmartSpawner/config.yml`, `creator/lab/smartspawner_config_sandbox.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Habilitación de Romper Spawners (`spawner_break.enabled: true`)**:
     - Reactivado para que los jugadores puedan picar y recuperar los spawners que hayan colocado.
     - Requiere pico de hierro o superior con encantamiento Toque de Seda (*Silk Touch* nivel 1).
     - Se mantiene `direct_to_inventory: true` para entrega segura directa al inventario.
     - Se mantiene `natural_spawner.breakable: false`: los spawners naturales del mapa siguen protegidos para evitar farmeo masivo del mundo.
  2. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] ui & gui | Actualización de Iconos en Almacén SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/gui_layouts/default/storage_gui.yml`, `creator/lab/smartspawner_storage_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Cambio de Icono de Ordenar (`slot_3`)**: Actualizado a `COMPARATOR`.
  2. **Cambio de Icono de Vender Botín (`slot_5`)**: Actualizado a `HOPPER_MINECART`.
  3. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] ui & gui | Inclusión del Conteo de Spawners Apilados en Título de Menús SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/language/en_US/gui.yml`, `creator/lab/smartspawner_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste de Títulos (`gui_title_main`)**:
     - Spawner individual: `&0&l|&r &0Spawner x1 ▶ &8{ᴇɴᴛɪᴛʏ}`
     - Spawners apilados: `&0&l|&r &0Spawner x{amount} ▶ &8{ᴇɴᴛɪᴛʏ}`
  2. **Ajuste de Título de Almacén (`gui_title_storage`)**:
     - `&0&l|&r &0Spawner x{amount} ▶ &8Almacén &7[{current_page}/{total_pages}]`
  3. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] ui & gui | Depuración de Botones de Filtro y Retirar Todo en SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/gui_layouts/default/storage_gui.yml`, `creator/lab/smartspawner_storage_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de Funciones Secundarias**:
     - Desactivado el botón de filtro de botín (`slot_4: enabled: false`).
     - Desactivado el botón de retirar todo el botín (`slot_6: enabled: false`).
  2. **Simetría Espacial Alterna**:
     - La barra de navegación queda perfectamente espaciada en ranuras alternas: Slot 1 (Anterior), Slot 3 (Ordenar), Slot 5 (Venta Directa), Slot 7 (Soltar) y Slot 9 (Siguiente).
  3. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] economy & gui | Integración del Botón de Venta Directa en Almacén SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/gui_layouts/default/storage_gui.yml`, `plugins/SmartSpawner/config.yml`, `plugins/SmartSpawner/language/en_US/gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Configuración de Venta Directa (`slot_5`)**:
     - Asignado el lingote de oro (`GOLD_INGOT`) en la posición central (Slot 5) de la fila inferior del almacén de botín.
     - Acción vinculada: `sell_all` para liquidar automáticamente todos los ítems almacenados por dinero de Vault ($).
  2. **Habilitación de Economía (`config.yml`)**:
     - Activado `custom_economy.enabled: true` con integración a Vault y ShopGUI+ / `item_prices.yml`.
  3. **Estilización Visual (`gui.yml`)**:
     - Botón rotulado: `&#59E91FVender Todo el Botín` con cálculo en vivo de `&#59E91F&l$&r&#59E91F{total_sell_price}`.
  4. **Despliegue**: Subidos los 3 archivos vía SFTP a Sandbox con éxito.

---

## [2026-09-14] ui & gui | Eliminación del Botón Salir en Almacén SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/gui_layouts/default/storage_gui.yml`, `creator/lab/smartspawner_storage_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de Salir (`slot_5`)**:
     - Desactivado el botón de salir (`enabled: false`, cristal rojo) en el menú de almacenamiento.
     - La fila inferior queda limpia y simétrica exclusivamente con las herramientas operativas: *Página Anterior*, *Ordenar Almacén*, *Filtro de Botín*, *Retirar Todo*, *Soltar al Suelo* y *Página Siguiente*.
  2. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] loot & economy | Purga de Ítems No Apilables y Bloqueo de Recolección de Spawners (Sandbox)
- **Módulo**: `plugins/SmartSpawner/config.yml`, `plugins/SmartSpawner/spawners_settings.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga Completa de Ítems No Apilables (`spawners_settings.yml`)**:
     - Eliminados todos los drops no apilables (`BOW`, `CROSSBOW`, `GOLDEN_AXE`, `GOLDEN_SWORD`, `IRON_AXE`, `SADDLE`, `STONE_SWORD`, `TOTEM_OF_UNDYING`, `TRIDENT`) de todas las tablas de loot.
     - Garantizado que el 100% de los drops generados en el almacén virtual sean apilables (stacks x64 o x16), evitando que el inventario de 45 slots colapse con armas gastadas de durabilidad aleatoria.
  2. **Bloqueo de Recolección de Spawners (`config.yml`)**:
     - Configurado `spawner_break.enabled: false`: los spawners colocados ya no pueden picarse ni recolectarse con herramientas ni Toque de Seda.
     - Verificado `natural_spawner.breakable: false`: los spawners naturales de mazmorras no se pueden obtener.
     - Canalizado el acceso a spawners exclusivamente a la venta oficial (tienda de Almas / crates / tienda).
  3. **Despliegue**: Subidos ambos archivos vía SFTP a Sandbox con éxito.

---

## [2026-09-14] balance & core | Freno de Producción y Balance de SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/config.yml`, `creator/lab/smartspawner_config_current.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Freno de Producción**:
     - `max_stack_size`: reducido de 16 a **8** spawners máximos por bloque.
     - `delay`: ampliado de 25s a **60s** (1 ciclo por minuto).
     - `max_mobs`: ajustado a **2** (de 1 a 2 mobs por ciclo en vez de 4).
  2. **QoL y Optimización**:
     - `direct_to_inventory: true` para evitar pérdida física de spawners al picar con Toque de Seda.
     - `particle.spawner_generate_loot: false` para eliminar saturación de partículas en bases.
  3. **Despliegue**: Subido a Sandbox vía SFTP con éxito.

---

## [2026-09-14] ui & localization | Estandarización Cromática Semántica en SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/language/en_US/messages.yml`, `creator/lab/smartspawner_messages_es.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Código Semántico de Colores (Chat & Action Bar)**:
     - **Éxito / Afirmativo**: Glifo verde `&#59E91F✔`, variable en blanco `&f` y fuente custom en verde `&#59E91F` (`&8[&eSpawners&8] &#59E91F✔ &f{Variable} &#59E91Fᴛᴇxᴛᴏ`).
     - **Error / Bloqueo**: Glifo rojo `&#FF4D4D✘`, variable en blanco `&f` y fuente custom en rojo `&#FF4D4D` (`&8[&eSpawners&8] &#FF4D4D✘ &f{Variable} &#FF4D4Dᴛᴇxᴛᴏ`).
     - **Neutro / Información**: Glifo gris `&7⚙`, variable en blanco `&f` y fuente custom en gris `&7` (`&8[&eSpawners&8] &7⚙ &f{Variable} &7ᴛᴇxᴛᴏ`).
  2. **Depuración Funcional**:
     - Purgadas todas las menciones a comandos inexistentes.
     - Action Bar sincronizada con la misma lógica cromática minimalista.
  3. **Despliegue**: Subido a Sandbox vía SFTP y verificado con éxito.

---

## [2026-09-14] optimization & core | Despliegue de UniverseSpigot Optimizado en Producción (Survival)
- **Módulo**: `universespigot.yml`, `creator/lab/survival_universespigot.yml`, `creator/output/universespigot.yml`, Servidor Survival (`ymykh9qy.575c7473`)
- **Trabajo Realizado**:
  1. **Protección de Dungeons y Combate RPG (`combat.mace`)**:
     - Configurado `limit-fall-distance: 15.0` para acotar el escalado de daño de la maza a un máximo de 15 bloques de caída (mitiga one-shots a bosses de dungeons).
  2. **Optimizaciones de Motor y Red**:
     - Activado `behavior.alternativeKeepAlive: true` para estabilidad de conexiones Bedrock/Floodgate.
     - Reducida la comprobación de fluidos en entidades: `ticksBetweenWaterChecks: 4` (alivio del 75% en corrientes de granjas).
     - Habilitado `reducePlayerChunkSourceUpdates: true`, `cacheWorldConfigurations: true` y `optimiseRails: true`.
  3. **Seguridad y Parches Anti-Lag**:
     - Habilitados `fixOffHandGhostBlocks: true` y `fixPluginPlaceholderExploits: true`.
     - Configurado `remove-excess` con límite estricto de 8 para colisiones de minecarts y boats.
  4. **Corrección de UX Survival**:
     - Restauradas partículas al romper bloques (`disableBlockBreakParticles: false`) y sonidos de pasos (`disableFootStepSounds: false`).
  5. **Despliegue**: Subido vía SFTP al servidor de producción tras autorización explícita del Sr Ramos.

---

## [2026-09-13] spawner & ui | Configuración Directa al Botín y Desactivación de Experiencia (Sandbox)
- **Módulo**: `plugins/SmartSpawner/`, `creator/lab/smartspawner_config.yml`, `creator/lab/smartspawner_main_gui.yml`, `creator/lab/smartspawner_storage_gui.yml`, `creator/lab/smartspawner_gui.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Salto Directo al Almacén (`skip_main_gui: true`)**:
     - Configurado en `gui_layouts/default/main_gui.yml`. Al hacer clic derecho a cualquier spawner en el mundo, el jugador entra directamente a la interfaz de botín (almacén de 6 filas).
  2. **Desactivación Integral de Experiencia**:
     - `max_stored_exp: 0` y `allow_exp_mending: false` en `config.yml`.
     - Botón de experiencia desactivado (`enabled: false`) en `main_gui.yml`.
     - Botón de experiencia en almacén rotulado como `Desactivada`.
  3. **Estilización Completa del Almacén (`gui.yml`)**:
     - Título estandarizado: `&0&l|&r &0Spawner ▶ &8Almacén &7[{current_page}/{total_pages}]`.
     - Botón de Retirar Todo (`take_all_button`): `&#59E91FRetirar Todo el Botín` con lore de recolección en small caps.
     - Botón de Filtro (`item_filter_button`): `&#FFF275Filtro de Botín`.
     - Botón de Ordenar (`sort_items_button`): `&#FFF275Ordenar Almacén`.
     - Botón de Soltar (`drop_page_button`): `&#FF4D4DSoltar al Suelo`.
     - Botón de Salir (`return_button`): `&cSalir`.
  4. Subidos los 4 archivos modificados vía SFTP al Sandbox con código de salida 0.

---

## [2026-09-13] ui & demo | Maquetas Interactivas de SmartSpawner en DeluxeMenus (Sandbox)
- **Módulo**: `creator/lab/maqueta_spawner.yml`, `creator/lab/maqueta_spawner_almacen.yml`, `creator/lab/maqueta_spawner_apilar.yml`, `creator/lab/deluxemenus_config.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Maqueta 1: Panel Principal del Spawner (`/maqueta_spawner`)**:
     - 3 filas (size: 27) con marco simétrico de cristales grises.
     - Slot 11: Almacén de Botín (`CHEST`), muestra ranuras ocupadas y resumen de botín acumulado con enlace a la vista de almacén.
     - Slot 13: Información y Gestión (`ZOMBIE_HEAD`), estadísticas de apilado (4/16), rango, estado activo y atajos de clic izquierdo/derecho.
     - Slot 15: Experiencia (`EXPERIENCE_BOTTLE`), muestra 640/1.000 XP acumulada y estado de Mending.
     - Slot 22: Botón de Salir (`DARK_OAK_DOOR`).
  2. **Maqueta 2: Almacén de Botín (`/maqueta_spawner_almacen`)**:
     - 6 filas (size: 54) con drops simulados (Carne podrida, Zanahoria, Hierro).
     - Fila inferior de control (Navbar): Paginación (slots 45/53), Ordenar (slot 47), Filtro (slot 48), Volver Atrás (slot 49), Retirar Todo (slot 50, `BUNDLE`) y Tirar al Suelo (slot 51, `DROPPER`).
  3. **Maqueta 3: Gestión de Apilado (`/maqueta_spawner_apilar`)**:
     - 3 filas (size: 27) con botones simétricos: -1 Spawner (slot 11), Desapilar Todo (slot 12), Estado central (slot 13), Agregar Todo (slot 14), +1 Spawner (slot 15) y Volver (slot 22).
  4. Registradas las 3 maquetas en `plugins/DeluxeMenus/config.yml` y desplegadas vía SFTP al servidor de pruebas con código de salida 0.

---

## [2026-09-13] spawner & balance | Despliegue de Configuración Optimizada de SmartSpawner (Sandbox)
- **Módulo**: `plugins/SmartSpawner/config.yml`, `creator/lab/smartspawner_config.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Ajustes de Balance y Red Teaming Aplicados**:
  1. **Cap de Apilado**: `max_stack_size` reducido de 10.000 a **16** unidades para prevenir hiperinflación y picos de memoria por bloque.
  2. **Protección de la Lonja de Exportación**: `custom_economy.enabled` cambiado a **`false`**, impidiendo que los usuarios vendan de forma pasiva dentro del GUI del spawner y preservando el tráfico hacia `/lonja`.
  3. **Seguridad en Rotura**: `auto_sell_and_claim_exp_on_break` cambiado a **`false`** para evitar transacciones fantasmas; preservado requisito de Silk Touch I con pico de hierro/diamante/netherite.
  4. **Persistencia Robusta**: `database.mode` migrado de YAML a **`SQLITE`** (`spawners.db`) para evitar corrupción de archivos en caídas y reducir el lag de I/O en disco.
  5. Desplegado vía SFTP en el Sandbox con código de salida 0.

---

## [2026-09-13] wiki & spawner | Ingesta de SmartSpawner v1.6.6 y Auditoría de Configuración
- **Módulo**: `plugins/SmartSpawner/`, `raw/thunderia/SmartSpawner/`, `wiki/sources/smartspawner/desglose_smartspawner_v1_6_6.md`
- **Trabajo Realizado**:
  1. Ingerida la documentación oficial de SmartSpawner (`https://docs.smartspawner.site/docs/`).
  2. Descargados desde el servidor Sandbox los ficheros de configuración activos: `config.yml`, `spawners_settings.yml`, `item_spawners_settings.yml`, `item_prices.yml`.
  3. Creado el desglose técnico en la wiki con arquitectura de virtual spawner, prevención de entity lag, apilado de hasta 10.000 unidades y tablas de precios.
  4. Identificados 5 parámetros críticos de desbalance y rendimiento por defecto (`max_stack_size`, `price_source_mode`, `hopper.enabled`, `auto_sell_and_claim_exp_on_break`, persistencia YAML).
  5. Actualizado `index.md`.

---

## [2026-09-13] crates & fx | Configuración de Partícula ITEM_SLIME en Slime Crate
- **Módulo**: `plugins/ExcellentCrates/crates/slime.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. Localizada la nueva caja `slime.yml` recién creada en el servidor de pruebas.
  2. Sustituida la partícula `HAPPY_VILLAGER` por la partícula oficial de baba **`ITEM_SLIME`** bajo el modelo `spiral`.
  3. Desplegado el archivo vía SFTP con código de salida 0.

---

## [2026-09-13] crates & fix | Inyección de Plantillas de Preview y UI de ExcellentCrates (Sandbox)
- **Módulo**: `plugins/ExcellentCrates/previews/`, `plugins/ExcellentCrates/ui/`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Diagnóstico del Fallo**:
  - Las cajas (`limitada.yml`, `mitica.yml`, `rara.yml`) tenían asignado `Preview.Id: prueba`.
  - El servidor de pruebas carecía del archivo `previews/prueba.yml` (así como de `limited.yml` y los menús de `ui/`), provocando que la apertura de la previsualización in-game fuera nula.
- **Acciones Realizadas**:
  1. Descargadas desde el servidor Survival (modo lectura):
     - `previews/prueba.yml`, `previews/limited.yml`, `previews/default.yml`.
     - `ui/crate_open_amount.yml`, `ui/crate_open_costs.yml`.
  2. Subidos todos los archivos vía SFTP al servidor Sandbox de pruebas.
  3. Comprobada integridad de las plantillas (layout 9x6 con slots de recompensas 0-44, milestones en slot 47, puerta de salida en slot 49 y flechas de paginación).

---

## [2026-09-13] ui & deluxemenus | Creación del Submenú Intermedio de Zafiros (Mercado Zafiros)
- **Módulo**: `creator/lab/mercado_zafiros.yml`, `creator/lab/tienda_principal_sandbox.yml`, `creator/lab/deluxemenus_config.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación de `mercado_zafiros.yml` (4 filas, size: 36)**:
     - Título estandarizado: `&0&l|&r &0Mercado ▶ &8Zafiros &8(&#1E6BFF💎&8)`.
     - **Fila 2 centrada simétrica**:
       - Slot 12 (Izquierda): `&#1E6BFFTienda de Zafiros` (`DIAMOND`), enlace directo a `[player] shop zafiros` (o futuro catálogo interno).
       - Slot 14 (Derecha): `&#FFF275Comprar Zafiros` (`NETHER_STAR`), acceso a la tienda web `[player] buy`.
     - **Fila 4 (Navbar)**:
       - Slot 31: Botón volver (`DARK_OAK_DOOR`) apuntando a `tienda_principal`.
       - Slot 35: Cabeza de balance `head-%player_name%` homologada con las 4 monedas.
       - Filtro de cristales grises en el resto de la fila de navegación.
  2. **Actualización de Navegación en `tienda_principal`**:
     - Botón `Boton_Zafiros` (slot 10) reorientado para abrir `[openguimenu] mercado_zafiros`.
  3. **Registro y Despliegue en Sandbox**:
     - Registrado `mercado_zafiros` en `plugins/DeluxeMenus/config.yml`.
     - Subidos los 3 archivos vía SFTP al servidor de pruebas con código de salida 0.

---

## [2026-09-13] market & telemetry | Estudio de Mercado Minecraft y Construcción de Thunder-Dashboard
- **Módulo**: `wiki/synthesis/estudio_mercado_minecraft_multijugador.md`, `thunder-dashboard/`
- **Trabajo Realizado**:
  1. **Estudio de Mercado Multijugador**:
     - Dimensionamiento macro (TAM de >300M copias y 150M MAU) y micro-segmentación hispanohablante (SAM de ~8M MAU en servidores públicos, 75k-110k CCU pico).
     - Cuantificación del ecosistema No-Premium (TLauncher, APKs de Android Bedrock en LATAM) y cuotas reales (78-82% no-premium en LATAM vs 70% premium en España).
     - Análisis de viabilidad de negocio, estructura OPEX/ingresos (>80% margen neto) y red teaming de modos de fallo.
     - Evaluación de escalabilidad al mercado anglosajón (multiplicador de ARPU 4x-5x).
  2. **Creación de Cuadro de Mando Local (`thunder-dashboard`)**:
     - Creada aplicación web local en `C:\Users\tecno\Desktop\ThunderCerebro\thunder-dashboard\` sobre Node.js nativo (puerto 3838).
     - Implementado semáforo de 5 cuadrantes (Adquisición, Retención D1/D7, Engagement, MSPT/TPS, Monetización Tebex).
     - Implementada calculadora financiera reactiva con conmutador Hispano vs Anglosajón.
     - Creado script de arranque automático en un clic: `iniciar_dashboard.bat`.
     - Integración con síntesis wiki en `wiki/synthesis/estudio_mercado_minecraft_multijugador.md`.

---

## [2026-09-12] crates & migration | Traspaso de Configuración Completa de ExcellentCrates (Survival ➔ Pruebas)
- **Módulo**: `plugins/ExcellentCrates/`, Servidor Survival (`ymykh9qy.575c7473`) ➔ Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Descarga desde Servidor Survival**:
     - Respaldados en local bajo [`raw/thunderia/ExcellentCrates_Survival/`](file:///C:/Users/tecno/Desktop/ThunderCerebro/raw/thunderia/ExcellentCrates_Survival/):
       - Core: `config.yml`, `engine.yml`, `milestones.yml`.
       - Cajas (`crates/`): `consumibles.yml`, `limitada.yml`, `mitica.yml`, `rara.yml`, `vote.yml`.
       - Llaves (`keys/`): `gadgets.yml`, `limited.yml`, `mitica.yml`, `rara.yml`, `vote.yml`.
  2. **Despliegue e Inyección en Servidor de Pruebas**:
     - Subidos los 13 archivos a `plugins/ExcellentCrates/` en el servidor Sandbox vía SFTP.
     - Preservada la integridad de los pesos porcentuales, animaciones y recompensas oficiales.
  3. **Verificación Remota**: Confirmados todos los ficheros persistidos en el directorio remoto de pruebas con código de salida 0.

---

## [2026-09-12] database & itemedit | Migración de Server Database Completa al Servidor de Pruebas
- **Módulo**: `plugins/ItemEdit/database/server-database.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Auditoría Previa**: Verificado el estado de `plugins/ItemEdit/database/server-database.yml` en el servidor de pruebas (estaba vacío en 0 bytes).
  2. **Transferencia SFTP**:
     - Subido el archivo maestro [`raw/thunderia/core_economy/Informacion/server-database.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/raw/thunderia/core_economy/Informacion/server-database.yml) (381.142 bytes, 2.628 líneas) al directorio de destino del servidor Sandbox.
     - Contiene los 140 objetos oficiales con su serialización completa de Bukkit/Paper (sets Divinos, Míticos, Raros, fragmentos de llaves, auras y armas custom).
  3. **Verificación**: Confirmada la persistencia del archivo en el servidor remoto con código de salida 0.

---

## [2026-09-10] ui & deluxemenus | Pronóstico/Pity con Objetos en Venta y Ajuste Devaluación Max
- **Módulo**: `creator/lab/lonja_venta.yml`, `creator/lab/lonja_probabilidades.yml`, `plugins/DeluxeMenus/config.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste en `lonja_venta.yml`**:
     - Sustituido el texto de devaluación por ` ' &8&o(ᴅᴇᴠᴀʟᴜᴀᴄɪᴏɴ: ᴍᴀx -15%)'` en los 5 cupos activos.
  2. **Recreación Integral de `lonja_probabilidades.yml` (6 filas, size: 54)**:
     - Título sincronizado con temporizador y reloj de arena: `&0&l|&r &0Mercado ▶ &8Pronóstico y Pity &7⏳ 03h 42m`.
     - **Fila 2 (Slots 11-15)**: Top 5 recursos con mayor probabilidad acumulada (Zanahoria 38.5% con 5d de sequía/pity inminente, Trigo 32.0%, Cuero 26.5%, Bambú 22.0%, Hueso 18.5%).
     - **Fila 4 (Slots 29-33)**: Los 5 objetos activos hoy en venta (Cactus, Pólvora, Patata, Caña de Azúcar, Vara de Blaze) con pity reiniciado a 0 días, probabilidad residual de repetición y precio del día.
     - **Navbar (Fila 6)**: Botón Volver Atrás en Slot 49 (`DARK_OAK_DOOR`) hacia `lonja_venta` y balance en Slot 53 (`head-%player_name%`).
  3. **Registro y Despliegue en Sandbox**:
     - Registrado `lonja_probabilidades` en `plugins/DeluxeMenus/config.yml` con comandos `/lonjaprobabilidades`, `/lonja_probabilidades`, `/lonjapity`.
     - Subidos los 3 ficheros actualizados por SFTP al servidor de pruebas.

---

## [2026-09-10] ui & deluxemenus | Limpieza y Formateo de Lore en Lonja de Venta
- **Módulo**: `creator/lab/lonja_venta.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste de Lore en los 5 Cupos Activos (`lonja_venta.yml`)**:
     - `U:` sustituido formalmente por `Unidad:` en los 5 ítems (Cactus, Pólvora, Patata, Caña de Azúcar, Vara de Blaze).
     - Purgadas las líneas analíticas de `Trend:` y `Accion:` para aligerar la lectura visual.
     - Ajustado el aviso de devaluación (`(ᴅᴇᴠᴀʟᴜᴀᴄɪᴏɴ: ʜᴀꜱᴛᴀ -15%)`) pegado a la izquierda con margen único de 1 espacio (` ' &8&o...'`).
     - Unificada la llamada a la acción inferior en `&7▶ Click para vender`.
  2. **Despliegue**: Subido archivo actualizado vía SFTP al Sandbox de pruebas.

---

## [2026-09-10] ui & deluxemenus | Ajuste de Formato de Título en Lonja de Venta
- **Módulo**: `creator/lab/lonja_venta.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste de `menu_title` en `lonja_venta.yml`**:
     - Modificado a `&0&l|&r &0Mercado ▶ &8Venta &7⏳ 03h 42m`.
     - Texto `Venta` en color gris oscuro (`&8`), temporizador en gris claro (`&7`), eliminado el encapsulado entre paréntesis y añadido el símbolo del reloj de arena (`⏳`).
  2. **Despliegue**: Subido archivo actualizado vía SFTP al Sandbox de pruebas.

---

## [2026-09-10] ui & deluxemenus | Menú Intermedio de Experiencia: Tienda de XP vs Encantamientos Custom
- **Módulo**: `creator/lab/mercado_xp.yml`, `creator/lab/tienda_xp_fija.yml`, `creator/lab/xp_trims.yml`, `creator/lab/xp_encantamientos.yml`, `plugins/DeluxeMenus/config.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Reestructuración de `mercado_xp.yml` (4 filas, size: 36)**:
     - Título: `&0&l|&r &0Mercado ▶ &8Experiencia &8(&#D48BFF✦&8)`.
     - Fila central simétrica con 2 opciones principales:
       - **Slot 12**: `&#D48BFFTienda de XP` (`EXPERIENCE_BOTTLE`), abre `[openguimenu] tienda_xp_fija` (catálogo de Trims y Encantamientos vanilla).
       - **Slot 14**: `&#FFF275Encantamientos Custom` (`ENCHANTED_BOOK`), ejecuta `[player] enchants` (ExcellentEnchants).
     - Botón de volver (slot 31) hacia `tienda_principal` y balance homologado en slot 35 (`head-%player_name%`).
  2. **Creación de `tienda_xp_fija.yml` (4 filas, size: 36)**:
     - Alberga el catálogo fijo: Trims (slot 12) y Encantamientos (slot 14).
     - Botón de volver (slot 31) retorna ordenadamente a `mercado_xp`.
  3. **Ajuste de Navegación en Subtiendas**:
     - `xp_trims.yml` y `xp_encantamientos.yml` actualizados para volver a `tienda_xp_fija`.
  4. **Registro y Despliegue en Sandbox**:
     - Registrado `tienda_xp_fija` en `plugins/DeluxeMenus/config.yml`.
     - Desplegados todos los archivos actualizados vía SFTP al servidor de pruebas.

---

## [2026-09-10] ui & deluxemenus | Recreación de Subtiendas de Almas/XP y Homologación de Tu Economía
- **Módulo**: `creator/lab/almas_spawners.yml`, `creator/lab/almas_llaves.yml`, `creator/lab/almas_protecciones.yml`, `creator/lab/mercado_xp.yml`, `creator/lab/xp_trims.yml`, `creator/lab/xp_encantamientos.yml`, `creator/lab/tienda_almas_fija.yml`, Servidor Sandbox (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Recreación de Subtiendas de Almas**:
     - `almas_spawners.yml` (Spawners de Mobs pasivos y hostiles pagados con Almas).
     - `almas_llaves.yml` (Llaves de cajas de recompensa con costes escalonados).
     - `almas_protecciones.yml` (Piedras de protección por bloques de área).
     - Conectadas bidireccionalmente con `tienda_almas_fija.yml`.
  2. **Recreación de Subtiendas de Experiencia**:
     - `xp_trims.yml` (18 plantillas de herrería / Armor Trims adquiribles con niveles de XP).
     - `xp_encantamientos.yml` (9 libros de encantamientos balanceados pagados con XP).
     - Conectadas con rotación y retorno a `mercado_xp.yml`.
  3. **Estandarización y Homologación del Icono `Tu Economía`**:
     - Actualizado en todos los menús del árbol de Almas y Experiencia (`mercado_almas`, `tienda_almas_fija`, `almas_*`, `mercado_xp`, `xp_*`) a `head-%player_name%`.
     - Lore homologado con formato multimoneda completo (Dinero, Almas, Zafiros, Niveles de XP) y acción `[openguimenu] info_economia`.
  4. **Despliegue**: Subidos todos los ficheros actualizados al Sandbox de pruebas mediante SFTP.

---

## [2026-09-10] fix & deluxemenus | Corrección de Encoding (0x8D), Flags Inválidas y Comandos Duplicados
- **Módulo**: `creator/lab/night_market.yml`, `creator/lab/tienda_almas_fija.yml`, `creator/output/MenusIA/mercado_xp.yml`, `creator/lab/mercado_comercio.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Causa Raíz del Error Fatal en `night_market.yml` (`0x8D unacceptable code point`)**:
     - Localizados caracteres especiales invisibles generados durante el reemplazo en Windows PowerShell.
     - Regenerado el archivo completo en codificación UTF-8 pura sin BOM, garantizando compatibilidad absoluta con SnakeYAML 2.2.
  2. **Depuración de Item Flags Inválidas**:
     - Retiradas banderas no soportadas por la versión de DeluxeMenus (`HIDE_ITEM_SPECIFICS`, `HIDE_ADDITIONAL_TOOLTIP`, `HIDE_POTION_EFFECTS`) en `tienda_almas_fija.yml` y `mercado_xp.yml`.
     - Purgadas directivas booleanas legacy residuales (`hide_attributes`, `hide_enchantments`, `hide_all_flags`).
  3. **Resolución de Conflicto de Comandos**:
     - Eliminado el alias redundante `mercadodinero` en `mercado_comercio.yml` para evitar el conflicto con `mercado_dinero.yml`.
  4. **Despliegue**: Subidos los 4 archivos corregidos vía SFTP al Sandbox de pruebas.

---

## [2026-09-10] ui & deluxemenus | Menú Selector de Almas: Tienda Fija vs Night Market
- **Módulo**: `creator/lab/mercado_almas.yml`, `creator/lab/tienda_almas_fija.yml`, `creator/lab/night_market.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Reestructuración de `mercado_almas.yml` a Menú Selector (4 filas, size: 36)**:
     - Título estandarizado: `&0&l|&r &0Mercado ▶ &8Almas &8(&#34B0F3🔥&8)`.
     - Fila central simétrica con 2 opciones principales:
       - **Slot 12**: `&#34B0F3Tienda de Almas` (`SOUL_CAMPFIRE`), abre `[openguimenu] tienda_almas_fija` (catálogo permanente de Spawners, Llaves y Protecciones).
       - **Slot 14**: `&#FFF275Night Market` (`SOUL_LANTERN`), abre `[openguimenu] night_market` (altar sombrío con ofertas rotativas, rarezas y pity).
     - Navbar inferior estándar en Fila 4 con retorno en slot 31 (`DARK_OAK_DOOR` hacia `tienda_principal`) y balance multimoneda en slot 35 (`head-%player_name%`).
  2. **Creación de `tienda_almas_fija.yml` (4 filas, size: 36)**:
     - Preserva el catálogo fijo de 3 categorías de Almas (Spawners en slot 11, Llaves en slot 13, Protecciones en slot 15).
     - Botón de volver en slot 31 retorna a `mercado_almas`.
  3. **Ajuste de Flujo en `night_market.yml`**:
     - Botón de volver (slot 49) redirige limpiamente a `mercado_almas` manteniendo el árbol jerárquico.
  4. **Registro y Despliegue en Sandbox**:
     - Registrado `tienda_almas_fija` en `plugins/DeluxeMenus/config.yml`.
     - Subidos todos los archivos actualizados vía SFTP al servidor de pruebas (`ymykh9qy.274758bd`).

---

## [2026-09-10] economy & deluxemenus | Night Market de Almas con Pity System, Descuento Global y Re-roll de Zafiros
- **Módulo**: `creator/lab/night_market.yml`, `creator/lab/nightmarket_premios.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación y Pulido del Night Market (`night_market.yml`, size: 54)**:
     - Título: `&0&l|&r &0Mercado ▶ &#34B0F3Altar Sombrío &8(Nocturno)`.
     - 5 cartas clasificadas estrictamente por rarezas: `Súper` (Slot 20), `Rara` (Slot 21), `Épica` (Slot 22), `Legend` (Slot 23), `Limited` (Slot 24).
     - Descuento único y global aplicado en todas las cartas (-35% OFF), con stock máximo de 1 compra por ciclo.
     - Cristales de rareza alineados en la fila 4 (slots 29 a 33).
     - Botón de re-roll de descuento en Slot 48 (`DIAMOND`) pagando 150 Zafiros, con límite máximo de -50% OFF.
     - Botón de Catálogo de Premios y Pity en Slot 45 (`SPYGLASS`), botón de retorno en Slot 49 (`DARK_OAK_DOOR`) y balance multimoneda universal en Slot 53 (`head-%player_name%`).
  2. **Creación del Menú de Probabilidades y Pity (`nightmarket_premios.yml`, size: 54)**:
     - Cabecera explicativa del Pity System en Slot 4 (`SPYGLASS`): incremento diario de probabilidades acumulativo con garantía del 100% de calidad Limited al 7º día consecutivo de sequía.
     - Fila central detallando las 6 rarezas (Súper, Rara, Épica, Legend, Mítica, Limited) con sus rangos de Almas, probabilidades base y pity escalonado.
  3. **Registro y Despliegue en Sandbox**:
     - Registrados ambos menús en `plugins/DeluxeMenus/config.yml` con comandos `/nightmarket`, `/mercadonocturno`, `/almasmarket`, `/nightmarketpremios` y `/nmpremios`.
     - Archivos subidos vía SFTP al servidor de pruebas (`ymykh9qy.274758bd`).

---

## [2026-09-10] economy & deluxemenus | Rediseño de la Lonja Bursátil a 5 Cupos Diarios + Menú de Pronósticos Pity
- **Módulo**: `creator/lab/lonja_venta.yml`, `creator/lab/lonja_probabilidades.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Rediseño y Pulido de `lonja_venta.yml` (size: 54)**:
     - Actualizado `menu_title` a `&0&l|&r &0Mercado ▶ &#FFF275Venta &8(03h 42m)` (simplificado a una palabra para evitar que el texto se salga de los márgenes del cofre).
     - Añadidos cristales grises superiores (`GRAY_STAINED_GLASS_PANE`) en slots 0-3 y 5-8, manteniendo el libro central en Slot 4.
     - Eliminados los símbolos `&` sobrantes en los precios (ahora `&#59E91F$14.50` en vez de `&#59E91F&$14.50`).
     - Aplicada font custom Thunder (small-caps `ᴅᴇᴠᴀʟᴜᴀᴄɪᴏɴ: ʜᴀꜱᴛᴀ -15%`) en los avisos de caída de precio por volumen, reduciendo el ancho horizontal.
     - Posicionados los cristales de tendencia en la Fila 4 (slots 29-33) directamente debajo de cada producto.
     - Navbar reorganizada en Fila 6 (slots 45-53): Slot 45 Pronósticos/Pity, Slot 49 Volver, Slot 52 Venta Rápida, Slot 53 Tu Economía.
  2. **Creación del Menú de Probabilidades Pity (`lonja_probabilidades.yml`, size: 54)**:
     - Cabecera explicativa en Slot 4 (`SPYGLASS`) con fórmula de días acumulados y garantía 100% a los 7 días.
     - 14 ítems en orden de probabilidad decreciente:
       - Zanahoria (38.5%, 5 días sin salir), Trigo (32.0%), Cuero (26.5%), Bambú (22.0%), etc.
       - Ítems activos hoy marcados al final como improbables (2.0% - 2.5%) por reinicio de pity.
     - Botón de volver a la lonja en Slot 45 y balance en Slot 53.
  3. **Despliegue y Registro**:
     - Registrado `lonja_probabilidades` en `DeluxeMenus/config.yml` (comandos `/lonjaprobabilidades`, `/lonjapity`).
     - Subidos vía SFTP al Sandbox `lonja_venta.yml`, `lonja_probabilidades.yml` y `config.yml`.
  4. **Interconexión y Renombramiento (`tienda_principal.yml` -> `mercado_comercio.yml`)**:
     - Conectado el botón de Dinero (`slot 12` de `tienda_principal.yml`) para que abra directamente `[openguimenu] mercado_comercio` en lugar de la tienda nativa de ShopGUIPlus.
     - Renombrado el título de `mercado_comercio.yml` a `&0&l|&r &0Mercado ▶ &8Dinero &8(&#59E91F$&8)`.
     - Ajustado el botón Volver (`slot 31`) de `mercado_comercio.yml` para regresar a `tienda_principal.yml`.
     - Subidos ambos archivos actualizados al Sandbox vía SFTP.
  5. **Reorganización de Navbar en Menú Principal (`tienda_principal.yml`)**:
     - Eliminado el botón Catálogo de Precios (`slot 27`).
     - Reubicado el botón Mercado de Subastas (`BELL`) del `slot 28` al `slot 27`.
     - Eliminado el botón Venta Rápida (`slot 34`).
     - Rellenados los huecos liberados (`slots 28, 34`) con paneles de cristal gris (`GRAY_STAINED_GLASS_PANE`).
     - Subido al Sandbox vía SFTP.
  6. **Ajuste de Título en Mercado Almas (`mercado_almas.yml`)**:
     - Cambiado el título a `&0&l|&r &0Mercado ▶ &8Almas &8(&#34B0F3🔥&8)` homogeneizando la palabra "Almas" en gris `&8` con el símbolo entre paréntesis.
     - Subido al Sandbox vía SFTP.
  7. **Ajuste de Título en Mercado Experiencia (`mercado_xp.yml`)**:
     - Cambiado el título a `&0&l|&r &0Mercado ▶ &8Experiencia &8(&#D48BFF✦&8)` homogeneizando la palabra "Experiencia" en gris `&8` con el símbolo entre paréntesis.
     - Subido al Sandbox vía SFTP.
  8. **Centrado de Íconos en Mercado Dinero (`mercado_comercio.yml`)**:
     - Reubicada la opción Tienda de Compra del slot 11 al slot 12, y la Tienda de Venta del slot 15 al slot 14, juntándolos más al centro de la Fila 2.
     - Subido al Sandbox vía SFTP.
  9. **Universalización del Ícono "Tu Economía" en Todos los Menús de Categorías (28 menús)**:
     - Sustituidos los ítems de economía variables (`KELP`, `SOUL_CAMPFIRE`, `EXPERIENCE_BOTTLE`) por la cabeza del jugador (`head-%player_name%`) con la ficha multimoneda completa del menú principal (Dinero, Almas, Zafiros, XP) y acceso a `[openguimenu] info_economia`.
     - Aplicado en `mercado_dinero.yml`, `mercado_comercio.yml`, `mercado_almas.yml`, `mercado_xp.yml`, todas las 20 páginas de subtiendas de compra (`compra_bloques_*`, `compra_comida`, etc.), `lonja_venta.yml` y `lonja_probabilidades.yml`.
     - Desplegados todos los archivos vía SFTP al Sandbox.
  10. **Diseño y Despliegue del Night Market de Almas (`night_market.yml`, size: 54)**:
     - Creado el menú temático "Altar de las Sombras" con 5 cupos rotativos con descuentos (20% a 50%):
       - Slot 20: Pociones exóticas de mazmorras (precios accesibles, ej. 600 Almas).
       - Slot 21: Cosméticos exclusivos (Tags / Glows / ChatColors con 30% OFF).
       - Slot 22: Llaves abisales / fragmentos supremos con 40% OFF.
       - Slot 23: Equipo custom RPG (armas y herramientas con pasivas).
       - Slot 24: Jackpot Mítico con 50% de descuento (Spawner de Warden Ancestral).
     - Stock limitado a 1 compra por ciclo nocturno en cada oferta.
     - Cristales indicadores de rareza de carta (Común, Rara, Épica, Legendaria, Mítica) en slots 29 a 33.
     - Navbar con acceso a la tienda estable de Almas (`Slot 45`), volver (`Slot 49`) y balance multimoneda (`Slot 53`).
     - Registrado en `DeluxeMenus/config.yml` (comandos `/nightmarket`, `/mercadonocturno`, `/almasmarket`).
     - Subidos vía SFTP al Sandbox `night_market.yml` y `config.yml`.

---

## [2026-09-10] ui & deluxemenus | Estandarización de Info_Balance en Subtiendas de Almas (head-%player_name%)
- **Módulo**: `almas_spawners.yml`, `almas_llaves.yml`, `almas_protecciones.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Homologación con el Menú Principal**:
     - Reemplazado el icono de `SOUL_CAMPFIRE` en el slot 44 de las 3 subtiendas de Almas (`almas_spawners.yml`, `almas_llaves.yml`, `almas_protecciones.yml`) por el botón estándar del menú principal:
       - Material: `head-%player_name%`
       - Título: `&#FFF275Tu Economía`
       - Lore completo con las 4 economías: Dinero, Almas, Zafiros y XP.
       - Clic para abrir el desglose informativo en `[openguimenu] info_economia`.
  2. **Despliegue**: Subidos los 3 archivos vía SFTP al servidor Sandbox.

---

## [2026-09-10] ui & deluxemenus | Recreación Integral del Mercado de Experiencia (Trims y Encantamientos)
- **Módulo**: `xp_trims.yml`, `xp_encantamientos.yml`, `mercado_xp.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación de Subtiendas de Experiencia en DeluxeMenus (`size: 45`)**:
     - **`xp_trims.yml` (18 Trims Smithing Templates)**: Sentry, Vex, Wild, Coast, Dune, Wayfinder, Raiser, Shaper, Host, Ward, Silence, Tide, Snout, Rib, Eye, Spire, Flow, Bolt a 10 Niveles de XP c/u.
     - **`xp_encantamientos.yml` (9 Libros de Encantamiento)**: Mending, Infinity, Irrompibilidad III, Protección IV, Filo V, Fortuna III, Botín III, Eficiencia V, Toque de Seda a 50 Niveles de XP c/u.
  2. **Estructura Estándar y Filtrador**:
     - Fila 1 con paneles grises decorativos.
     - Botón **Filtrar Categoría (`COMPARATOR`)** en slot 36 con rotación bidireccional continua: `Trims ➔ Encantamientos ➔ Trims` y viñetas dinámicas (`&#FFF275● Activa`, `&7● Inactiva`).
     - Botón `Volver Atrás` en slot 40 (`DARK_OAK_DOOR`, regresa a `mercado_xp`).
     - Balance de Experiencia en slot 44 (`EXPERIENCE_BOTTLE` con `%player_level% LVL DE XP`).
  3. **Conexión de Flujo y Despliegue**:
     - Actualizado `mercado_xp.yml` para abrir directamente `[openguimenu] xp_trims` y `[openguimenu] xp_encantamientos`.
     - Registrados `xp_trims` y `xp_encantamientos` en `plugins/DeluxeMenus/config.yml`.
     - Subidos vía SFTP al servidor Sandbox.

---

## [2026-09-10] ui & deluxemenus | Recreación Integral de las 3 Categorías de Almas en DeluxeMenus
- **Módulo**: `almas_spawners.yml`, `almas_llaves.yml`, `almas_protecciones.yml`, `tienda_almas_fija.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación de Submenús en DeluxeMenus (5 Filas, `size: 45`)**:
     - **`almas_spawners.yml`**: Los 8 generadores oficiales (Cerdo, Vaca, Zombie, Araña, Esqueleto, Blaze, Slime, Magma Cube) con precios desde 150 a 2,000 Almas.
     - **`almas_llaves.yml`**: Las 5 llaves oficiales (Super 100🔥, Rara 400🔥, Gadgets 600🔥, Mítica 3,000🔥, Limited 10,000🔥).
     - **`almas_protecciones.yml`**: Los 6 bloques de protección PS (Carbón 8x8 10🔥, Hierro 16x16 100🔥, Oro 32x32 200🔥, Esmeralda 64x64 500🔥, Diamante 128x128 1,000🔥, Netherite 256x256 15,000🔥).
  2. **Estructura Estándar y Navegación**:
     - Fila 1 con paneles grises decorativos.
     - Botón de **Filtrar Categoría (`COMPARATOR`)** en slot 36 con ciclo continuo exclusivo de Almas: `Spawners ➔ Llaves ➔ Protecciones ➔ Spawners`.
     - Botón `Volver Atrás` en slot 40 (`DARK_OAK_DOOR`, regresa a `tienda_almas_fija`).
     - Balance de Almas en slot 44 (`SOUL_CAMPFIRE` con `%thundercurrencys_almas%`).
  3. **Conexión de Flujo y Despliegue**:
     - Actualizado `tienda_almas_fija.yml` para abrir directamente los menús creados en DeluxeMenus (`[openguimenu] almas_spawners`, `[openguimenu] almas_llaves`, `[openguimenu] almas_protecciones`).
     - Registrados los 3 menús en `plugins/DeluxeMenus/config.yml`.
     - Desplegados todos los archivos vía SFTP al servidor Sandbox.

---

## [2026-09-10] fix & deluxemenus | Registro de Menús Faltantes en DeluxeMenus: Tienda de Almas y Night Market
- **Módulo**: `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Diagnóstico**:
  - Los archivos físicos `tienda_almas_fija.yml`, `night_market.yml` y `nightmarket_premios.yml` existían en `plugins/DeluxeMenus/gui_menus/menusIA/`, y el menú intermediario `mercado_almas.yml` los ejecutaba con `[openguimenu] tienda_almas_fija` y `[openguimenu] night_market`.
  - Sin embargo, no estaban declarados dentro de la sección `gui_menus:` de `plugins/DeluxeMenus/config.yml`, provocando que DeluxeMenus no los reconociera y bloqueara su apertura.
- **Trabajo Realizado**:
  1. **Registro en Config**: Añadidas las 3 definiciones en `DeluxeMenus/config.yml`:
     - `tienda_almas_fija` ➔ `menusIA/tienda_almas_fija.yml`
     - `night_market` ➔ `menusIA/night_market.yml`
     - `nightmarket_premios` ➔ `menusIA/nightmarket_premios.yml`
  2. **Despliegue**: Subido el `config.yml` actualizado al servidor Sandbox vía SFTP.

---

## [2026-09-10] fix & deluxemenus | Depuración de Advertencias: Migración a item_flags y Supresión de Colisión de Comandos
- **Módulo**: `warps.yml`, `warps_minas.yml`, `warps_dungeons.yml`, `warps_rtp.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Corrección de Directivas Deprecadas (*hide_attributes* y *hide_enchantments*)**:
     - Migradas todas las directivas booleanas obsoletas a la sintaxis moderna estándar `item_flags: [HIDE_ATTRIBUTES, HIDE_ENCHANTS]` en los 4 menús de teletransporte (`warps.yml`, `warps_minas.yml`, `warps_dungeons.yml`, `warps_rtp.yml`), erradicando las 38 advertencias de consola durante el `/dm reload`.
  2. **Resolución de Conflicto de Comandos (*Command already exists*)**:
     - Eliminada la entrada duplicada `tienda_vender` en `plugins/DeluxeMenus/config.yml` (que cargaba el mismo archivo `precios_todos.yml`), suprimiendo los avisos de omisión de comandos (`shopvender`, `preciosvender`, `precios_todos`).
  3. **Despliegue**: Archivos corregidos y subidos vía SFTP al servidor Sandbox.

---

## [2026-09-10] ui & deluxemenus | Menú de Compra por Lotes/Stacks (`compra_stacks.yml`) e Integración
- **Módulo**: `creator/lab/compra_stacks.yml`, `creator/lab/compra_cantidad.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación de `compra_stacks.yml` (4 Filas, `size: 36`)**:
     - `Fila 2 (Slots 9 a 17)`: Selección continua de 1 a 9 stacks con iconos de cofres (`CHEST` con `amount: 1..9`), títulos claros (`1 Stack (x64)` a `9 Stacks (x576)`) y cálculo de unidades y precios escalonados.
     - `Fila 4 (Navbar)`: Botón `Volver Atrás` en slot 31 (`DARK_OAK_DOOR`, regresa a `compra_cantidad`) con cristales grises decorativos en los slots restantes.
  2. **Enlace Bidireccional**:
     - Conectado el botón `Comprar Stacks` (`slot 27` en `compra_cantidad.yml`) con la acción `[openguimenu] compra_stacks`.
  3. **Registro y Despliegue**:
     - Registrado en `DeluxeMenus/config.yml` (comandos `/comprastacks`, `/maquetastacks`).
     - Subido al servidor Sandbox vía SFTP.

---

## [2026-09-10] ui & deluxemenus | Navbar con Paneles Grises y Comprar Stacks en Slot 27 (`compra_cantidad.yml`)
- **Módulo**: `creator/lab/compra_cantidad.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/compra_cantidad.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste de Navbar (Fila 4, Slots 27 a 35)**:
     - `Slot 27` (Izquierda del todo): Posicionado el botón `Comprar Stacks` (`CHEST_MINECART`).
     - `Slot 31` (Centro): Botón `Volver Atrás` (`DARK_OAK_DOOR`, regresa al menú de compra).
     - `Slots 28, 29, 30, 32, 33, 34, 35`: Rellenados con paneles de cristal gris decorativo (`GRAY_STAINED_GLASS_PANE`).
     - `Fila 1`: Despejada con aire limpio (`AIR`) para mantener la simetría y foco sobre el ítem central.
  2. **Despliegue**: Subido directamente al servidor Sandbox vía SFTP.

---

## [2026-09-10] ui & deluxemenus | Rediseño de compra_cantidad.yml: 4 Filas, Botones Invertidos y BuyMore Superior
- **Módulo**: `creator/lab/compra_cantidad.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/compra_cantidad.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Expansión a 4 Filas (`size: 36`)**:
     - `Fila 1 (Slot 4)`: Reubicado el botón `Comprar Stacks` (`CHEST_MINECART`) **justo encima** del objeto central para una jerarquía visual vertical limpia.
     - `Fila 2 (Slots 9 a 17)`: Controles de cantidad invertidos de izquierda a derecha:
       - **Izquierda (Suma / Confirmación)**: `Slot 9` (Establecer 64), `Slot 10` (Agregar 10), `Slot 11` (Agregar 1), `Slot 12` (Confirmar Compra / `LIME_SHULKER_BOX`).
       - **Centro (Slot 13)**: Ítem seleccionado (`GOLDEN_CARROT`).
       - **Derecha (Cancelación / Resta)**: `Slot 14` (Cancelar / `RED_SHULKER_BOX`), `Slot 15` (Quitar 1), `Slot 16` (Quitar 10), `Slot 17` (Establecer 1).
     - `Fila 4 (Slot 31)`: Botón de retorno estándar (`DARK_OAK_DOOR`, regresa a la tienda).
  2. **Despliegue**: Subido directamente al servidor Sandbox vía SFTP.

---

## [2026-09-10] ui & deluxemenus | Maqueta de Selección de Cantidad (`compra_cantidad.yml`) e Integración
- **Módulo**: `creator/lab/compra_cantidad.yml`, `creator/lab/compra_*.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación de la Maqueta de Cantidad (`compra_cantidad.yml`, 3 filas, `size: 27`)**:
     - Fila central (slots 9 a 17) replicando exactamente el layout oficial de ShopGUIPlus:
       - `Slot 9`: `&cEstablecer 1` (`RED_STAINED_GLASS_PANE`)
       - `Slot 10`: `&cQuitar 10` (`RED_STAINED_GLASS_PANE` x10)
       - `Slot 11`: `&cQuitar 1` (`RED_STAINED_GLASS_PANE` x1)
       - `Slot 12`: `&cCancelar` (`RED_SHULKER_BOX`, retorna al menú de la tienda)
       - `Slot 13`: Ítem de muestra central (`GOLDEN_CARROT`, lore con cantidad y total dinámico)
       - `Slot 14`: `&aConfirmar Compra` (`LIME_SHULKER_BOX`, simulación de compra con sonido)
       - `Slot 15`: `&aAgregar 1` (`LIME_STAINED_GLASS_PANE` x1)
       - `Slot 16`: `&aAgregar 10` (`LIME_STAINED_GLASS_PANE` x10)
       - `Slot 17`: `&aEstablecer 64` (`LIME_STAINED_GLASS_PANE` x64)
     - Fila 3:
       - `Slot 22`: Botón `&#FFF275Comprar Stacks` (`CHEST_MINECART`) alineado justo debajo del ítem central.
  2. **Interconexión Universal**:
     - Actualizados los 21 submenús de compra para que al hacer clic en cualquier producto abran `compra_cantidad`.
  3. **Registro y Despliegue**:
     - Registrado `compra_cantidad` en `DeluxeMenus/config.yml` (comandos `/compracantidad`, `/maquetacantidad`).
     - Subidos vía SFTP todos los menús actualizados al servidor Sandbox.

---

## [2026-09-10] ui & deluxemenus | Recreación Integral de Subtiendas de Compra (21 Menús en DeluxeMenus)
- **Módulo**: `creator/lab/compra_*.yml`, `creator/lab/mercado_dinero.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Recreación Fiel de Catálogos de Compra en DeluxeMenus**:
     - Generados 21 menús correspondientes a las 7 categorías exclusivas de compra de dinero:
       - **Bloques** (12 páginas, 307 ítems): `compra_bloques.yml` a `compra_bloques_12.yml`.
       - **Comida** (1 página, 17 ítems): `compra_comida.yml`.
       - **Equipo** (1 página, 17 ítems): `compra_equipo.yml`.
       - **Redstone** (1 página, 10 ítems): `compra_redstone.yml`.
       - **Misceláneo** (1 página, 20 ítems): `compra_misc.yml`.
       - **Tintes** (1 página, 16 ítems): `compra_tintes.yml`.
       - **Banners** (4 páginas, 108 ítems): `compra_banners.yml` a `compra_banners_4.yml`.
  2. **Estructura Visual y Lores Estándar**:
     - Fila 1 con paneles grises decorativos.
     - Filas 2 a 4 con catálogo de ítems, precio por unidad y stack x64 (`&8ᴘʀᴇᴄɪᴏ ᴅᴇ ᴄᴏᴍᴘʀᴀ`, `&#59E91F&l$&r&#59E91F...`).
     - Botón de **Filtrar Categoría (`COMPARATOR`)** en slot 36 con ciclo continuo activo (`Bloques ➔ Comida ➔ Equipo ➔ Redstone ➔ Misceláneo ➔ Tintes ➔ Banners ➔ Bloques`) y lore reactivo con viñetas coloreadas.
     - Paginación estandarizada en slots 39 y 41 (con cristales de bloqueo en páginas límite), retorno en slot 40 (`DARK_OAK_DOOR` hacia `mercado_dinero`) y balance del jugador en slot 44 (`KELP`).
  3. **Interconexión y Despliegue**:
     - Conectados los 7 botones de `mercado_dinero.yml` para abrir sus respectivas subtiendas.
     - Registrados todos los 21 menús en `plugins/DeluxeMenus/config.yml`.
     - Desplegados todos los archivos vía SFTP en el servidor Sandbox de pruebas.

---

## [2026-09-10] ui & deluxemenus | Lonja Paginada (40 Ítems Oficiales) y Purga de Venta en Mercado de Compra
- **Módulo**: `creator/lab/mercado_dinero.yml`, `creator/lab/lonja_venta.yml`, `creator/lab/lonja_venta_2.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de Categorías Vendibles en Tienda de Compra (`mercado_dinero.yml`)**:
     - Retiradas las categorías de *Farmeo* y *Mobs* al ser de producción y venta.
     - Centradas las 7 categorías exclusivas de compra en los slots 10 al 16 (Bloques, Comida, Equipo, Redstone, Misceláneo, Tintes, Banners).
     - Corregido el prefijo hex en el título a `&#59E91F`.
  2. **Expansión y Paginación de la Lonja de Venta (`lonja_venta.yml` y `lonja_venta_2.yml`)**:
     - **Página 1 (27 slots, 9 a 35)**: Los 21 ítems oficiales de Farmeo + Top 6 de Drops de Mobs (Vara de Blaze, Pólvora, Perla de Ender, Cuero, Hueso, Semillas de Trigo).
     - **Página 2 (27 slots)**: Los 14 drops de Mobs restantes (Slime, Breeze, Crema Magma, Hilo, Polvo Blaze, Membrana, Panal, Prismarina, Flecha, Pluma, Ojo Araña, Piel Conejo, Pata Conejo, Carne Podrida) con relleno gris neutro en slots vacíos.
     - **Navegación Paginada Completa**: Flecha anterior (slot 48), retorno a `mercado_comercio` (slot 49) y flecha siguiente (slot 50).
  3. **Registro y Despliegue**:
     - Registrado `lonja_venta_2` en `plugins/DeluxeMenus/config.yml`.
     - Subidos todos los archivos vía SFTP al servidor Sandbox.

---

## [2026-09-10] ui & deluxemenus | Recreación de Categorías de Dinero (mercado_dinero.yml)
- **Módulo**: `creator/lab/mercado_dinero.yml`, `creator/lab/mercado_comercio.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Recreación de Categorías en DeluxeMenus (`mercado_dinero.yml`)**:
     - Creado menú idéntico a la selección de categorías de ShopGUIPlus pero en DeluxeMenus (`size: 36`).
     - Título estandarizado: `&0&l|&r &0Mercado ▶ &8Dinero &8(#59E91F$&8)`.
     - Fila 2 (slots 9 a 17) con las 9 categorías: Bloques, Farmeo, Comida, Mobs, Equipo, Redstone, Misceláneo, Tintes y Banners.
     - Fila 4 con navbar estándar: Retorno a `mercado_comercio` en slot 31 (`DARK_OAK_DOOR`) y balance en slot 35 (`KELP` con `%vault_eco_balance_formatted%`).
  2. **Enlace de Flujo**:
     - `mercado_comercio.yml` actualizado en Slot 11 (`Opcion_Comprar`) con acción `[openguimenu] mercado_dinero`.
  3. **Registro y Despliegue**:
     - Registrado `mercado_dinero` en `DeluxeMenus/config.yml` (comandos `/mercadodinero`, `/dinerocategorias`).
     - Desplegados todos los archivos al servidor Sandbox vía SFTP.

---

## [2026-09-10] ui & deluxemenus | Ajuste de Color en Título de Comercio a Gris (&8)
- **Módulo**: `creator/lab/mercado_comercio.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/mercado_comercio.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste de Título**: Actualizado `menu_title` de `&0&l|&r &0Mercado ▶ &#59E91FComercio` a `&0&l|&r &0Mercado ▶ &8Comercio`.
  2. **Despliegue**: Subido directamente al servidor Sandbox vía SFTP.

---

## [2026-09-07] ui & deluxemenus | Reducción Horizontal Extrema: Textos Sintéticos de 10-15 Caracteres
- **Módulo**: `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `wiki/concepts/mercadothunder.md`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Acortamiento Horizontal Estricto**:
     - Separado el precio unitario y el stack x64 en dos líneas para evitar líneas que sobrepasen los 25-28 caracteres de ancho.
     - Textos en small caps reducidos a expresiones ultra sintéticas de 2 palabras (máximo 12-15 caracteres):
       - `ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ` / `ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ`
       - `ᴇɴ ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ` / `ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ`
       - `ᴍᴇʀᴄᴀᴅᴏ ᴇꜱᴛᴀʙʟᴇ` / `ᴘʀᴇᴄɪᴏ ʀᴇɢᴜʟᴀʀ`
       - `ʙᴀᴊᴀᴅᴀ ʟᴇᴠᴇ` / `ʀɪᴇꜱɢᴏ ᴅᴇ ᴄᴀɪᴅᴀ`
       - `ᴄᴀɪᴅᴀ ᴄᴏɴᴛɪɴᴜᴀ` / `ᴇꜱᴘᴇʀᴀʀ ʀᴇʙᴏᴛᴇ`
       - `ꜱᴜᴇʟᴏ ᴀʟᴄᴀɴᴢᴀᴅᴏ` / `ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ`
     - Título de actualización abreviado a `&8| &fActualización: &e03h 42m`.
  2. **Despliegue**: Subido a Sandbox vía SFTP y actualizado en `wiki/concepts/mercadothunder.md`.

---

## [2026-09-07] ui & deluxemenus | Homogenización Bursátil: Rangos en Gris, Textos Genéricos y Supresión de Viñetas
- **Módulo**: `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `wiki/concepts/mercadothunder.md`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Rangos Neutros**: Los valores numéricos de suelo y techo se formatearon uniformemente en gris (`&7$X.XX &8- &7$X.XX`).
  2. **Textos Genéricos Estandarizados (Sin contextos específicos)**:
     - Reemplazadas las menciones a granjas de golems, nether o minería por descripciones financieras genéricas asignadas a 6 tiers de mercado:
       - `ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ ᴇɴ ᴜʟᴛɪᴍᴀꜱ ᴊᴏʀɴᴀᴅᴀꜱ` / `ᴄᴇʀᴄᴀ ᴅᴇʟ ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ`
       - `ʀᴇᴄᴜᴘᴇʀᴀᴄɪᴏɴ ᴘʀᴏɢʀᴇꜱɪᴠᴀ ᴅᴇ ᴠᴀʟᴏʀ` / `ᴄᴏᴛɪᴢᴀᴄɪᴏɴ ꜱᴏʙʀᴇ ʟᴀ ᴍᴇᴅɪᴀ`
       - `ᴛᴇɴᴅᴇɴᴄɪᴀ ᴇꜱᴛᴀʙʟᴇ ꜱɪɴ ᴠᴀʀɪᴀᴄɪᴏɴ` / `ᴘʀᴇᴄɪᴏ ʀᴇɢᴜʟᴀʀ ᴅᴇ ᴍᴇʀᴄᴀᴅᴏ`
       - `ᴍᴇʀᴄᴀᴅᴏ ᴄᴏɴ ʟɪɢᴇʀᴀ ᴛᴇɴᴅᴇɴᴄɪᴀ ᴀ ʟᴀ ʙᴀᴊᴀ` / `ᴘᴏꜱɪʙʟᴇ ᴘᴇʀᴅɪᴅᴀ ᴅᴇ ᴠᴀʟᴏʀ`
       - `ᴄᴀɪᴅᴀ ᴄᴏɴᴛɪɴᴜᴀ ᴅᴇ ᴄᴏᴛɪᴢᴀᴄɪᴏɴ` / `ᴇꜱᴘᴇʀᴀʀ ʀᴇʙᴏᴛᴇ ᴅᴇ ᴘʀᴇᴄɪᴏ`
       - `ᴍᴀxɪᴍᴀ ᴘᴇʀᴅɪᴅᴀ ᴅɪᴀʀɪᴀ ᴀʟᴄᴀɴᴢᴀᴅᴀ` / `ᴘʀᴇᴄɪᴏ ᴍɪɴɪᴍᴏ ɢᴀʀᴀɴᴛɪᴢᴀᴅᴏ`
  3. **Limpieza Tipográfica**: Suprimida la viñeta (`•`) inicial de las descripciones, manteniendo sangría limpia de 3 espacios.
  4. **Despliegue**: Subido a Sandbox vía SFTP y reflejado en `wiki/concepts/mercadothunder.md`.

---

## [2026-09-07] ui & deluxemenus | Ajuste Visual Definitivo de Lonja: Subtítulo Restaurado, Márgenes con Sangría y Espaciado Vertical Limpio
- **Módulo**: `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `wiki/concepts/mercadothunder.md`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Restauración de Identidad y Márgenes**:
     - Restaurado el subtítulo principal en small caps `&8ʙᴏʟꜱᴀ ᴅᴇ ᴠᴀʟᴏʀᴇꜱ` al inicio del lore.
     - Preservados los márgenes horizontales con sangría de un espacio (` ' &8| &f...'`) en todas las líneas funcionales.
     - Sangría anidada de 3 espacios (` '   &8• &7...'`) para las explicaciones en small caps (`ꜱᴜʙɪᴅᴀ ᴄᴏɴᴛɪɴᴜᴀ`, `ᴄᴇʀᴄᴀ ᴅᴇʟ ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ`).
  2. **Espaciado Vertical por Bloques**:
     - Líneas en blanco (`''`) separando:
       - Subtítulo inicial.
       - Bloque 1: Precio unitario + Stack x64 y Rango suelo/techo.
       - Bloque 2: Historial sparkline 5d y su explicación.
       - Bloque 3: Consejo bursátil y su explicación.
       - Bloque 4: Actualización de Precios con temporizador.
       - Hint de click para vender.
  3. **Despliegue**: Subido al servidor Sandbox vía SFTP y sincronizado en `wiki/concepts/mercadothunder.md`.

---

## [2026-09-07] ui & deluxemenus | Reestructuración de Lores Bursátiles en 5 Secciones Divididas
- **Módulo**: `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `wiki/concepts/mercadothunder.md`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **División Estructural del Lore en 5 Bloques**:
     - **`&8ᴠᴀʟᴏʀ ᴅᴇ ᴍᴇʀᴄᴀᴅᴏ`**: Precio por Unidad y Stack x64 divididos en líneas independientes.
     - **`&8ʀᴀɴɢᴏ ᴅᴇ ᴘʀᴇᴄɪᴏ`**: Suelo mínimo garantizado y Techo máximo en la misma línea.
     - **`&8ʜɪꜱᴛᴏʀɪᴀʟ ᴅᴇ ᴛᴇɴᴅᴇɴᴄɪᴀ`**: Gráfica sparkline de 5 días con subtítulo explicativo de la causa del movimiento.
     - **`&8ᴄᴏɴꜱᴇᴊᴏ ᴅᴇ ʙᴏʟꜱᴀ`**: Recomendación de acción inmediata con explicación técnica del porqué.
     - **`&8ᴀᴄᴛᴜᴀʟɪᴢᴀᴄɪᴏɴ ᴅᴇ ᴘʀᴇᴄɪᴏꜱ`**: Temporizador de cuenta atrás (`⏳ Tiempo restante: 03h 42m`).
  2. **Documentación**: Reflejado en `wiki/concepts/mercadothunder.md`.
  3. **Despliegue**: Subido a Sandbox vía SFTP.

---

## [2026-09-07] ui & deluxemenus | Optimización de Interfaz: Título Compacto, Timer en Lore e Historial Gráfico (Sparklines)
- **Módulo**: `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `wiki/concepts/mercadothunder.md`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Ajuste de Título de Menú**:
     - Reducido a `&0&l|&r &0Mercado ▶ &#FFF275Lonja de Venta` para evitar desbordamientos visuales fuera del marco del inventario del cliente.
  2. **Compactación Horizontal de Lores**:
     - Retiradas las cadenas excesivamente anchas.
     - Formato condensado:
       - `Precio: $X.XX (x64: $XXX)`
       - `Rango: $X.XX - $XX.XX`
       - `Historial: ↗ ↗ ↗ ↗ ↗` (*Sparkline condensado de 5 días*)
       - `Consejo: Vender ahora / Acumular / Cerca del suelo`
       - `⏳ Cierre: 03h 42m` (Temporizador trasladado al interior del lore de cada ítem y balance).
  3. **Documentación de Especulación**:
     - Actualizado `wiki/concepts/mercadothunder.md` formalizando los 4 pilares de especulación informada para el usuario.
  4. **Despliegue**: Subido a Sandbox vía SFTP.

---

## [2026-09-07] ui & deluxemenus | Corrección de Formato Hex: Añadido Prefijo '&' a Colores Rojos
- **Módulo**: `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Corrección de Sintaxis Hex**:
     - Localizadas y corregidas las 36 instancias de `#FF4D4D` que carecían del prefijo `&`.
     - Actualizadas a `&#FF4D4D` en todos los `display_name` y líneas de `lore` de los ítems en bajada/suelo.
  2. **Autoaprendizaje**:
     - Registrada la **Lección 7** en `wiki/concepts/deluxemenus_standards.md` formalizando la obligatoriedad de la sintaxis `&#RRGGBB` para evitar texto plano literal en el renderizado del cliente.
  3. **Despliegue**: Subido al servidor Sandbox vía SFTP.

---

## [2026-09-07] game-design & core | Adaptación del Mercado a Jornadas Bursátiles (Modelo Fantasy DAZN)
- **Módulo**: `wiki/concepts/mercadothunder.md`, `creator/lab/lonja_venta.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Documento Maestro de Arquitectura (`mercadothunder.md`)**:
     - Creado en `creator/lab/mercadothunder.md` e integrado en la base de conocimiento en `wiki/concepts/mercadothunder.md`.
     - Indexado en `index.md`.
     - Detalla: filosofía de tienda común vs lonja, ciclos de revaluación diaria (cero lag en MSPT), bandas de variación ($\pm 15\%$ a $\pm 20\%$ max/día), techos absolutos ($+150\%$ max) y suelos absolutos ($-50\%$ min), además del mecanismo *anti-dump* con deslizamiento de precio (*slippage*).
  2. **Adaptación de `lonja_venta.yml`**:
     - **Título con Contador**: `&0&l|&r &0Bolsa de Valores &8(Cierre: &e03h 42m&8)`.
     - **Lore adaptado a Jornada Diaria**: Sustituidas las referencias por `&8ᴊᴏʀɴᴀᴅᴀ ᴅɪᴀʀɪᴀ`, techos/suelos claros por ítem y recomendaciones de especulación (*Vender ahora* vs *Acumular en cofres*).
     - **Bandas de Variación Diarias**: Reajustadas al rango real de ciclo diario (Top alcista Cactus `+18.5%`, Suelo diario `-20.0%`).
  3. **Despliegue**: Subido al servidor Sandbox vía SFTP.

---

## [2026-09-07] ui & deluxemenus | Enlace de Navegación: mercado_comercio.yml ➔ lonja_venta.yml
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/mercado_comercio.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Conexión de Flujo**:
     - Configurado el **Slot 15** (`Opcion_Vender` / `HOPPER_MINECART`) en `mercado_comercio.yml` para ejecutar `[openguimenu] lonja_venta`.
     - Actualizado el hint de acción a `&7▶ Click para abrir lonja`.
     - Preservado el retorno bidireccional: el slot 49 de `lonja_venta.yml` regresa con `[openguimenu] mercado_comercio`.
  2. **Despliegue**: Subido a Sandbox vía SFTP.

---

## [2026-09-07] ui & deluxemenus | Prototipo de Lonja de Venta Dinámica (Bolsa de Valores)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/lonja_venta.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Creación de `lonja_venta.yml` (6 filas, size: 54)**:
     - Basado en la referencia estética de `precios_todos.yml` y adaptado al modelo de mercado bursátil de oferta y demanda.
     - **Filas 2 a 4 (slots 9 a 35 = 27 ítems ordenados por tendencia)**:
       - **Top 1 a 4 (En Auge / Alcista Extremo)**: Cactus (`+45%`, glow), Caña (`+38%`, glow), Varas de Blaze (`+32%`, glow), Sandía (`+28%`, glow).
       - **Top 5 a 8 (Alcista Moderado)**: Pólvora (`+22%`), Cuero (`+18%`), Trigo (`+12%`), Hueso (`+8%`).
       - **Neutrales (0%)**: Patata, Zanahoria, Calabaza, Hilo.
       - **A la Baja (-5% a -22%)**: Ojo de araña, Cobre, Carbón, Bayas, Oro bruto, Remolacha.
       - **Desplome / Saturación (-28% a -50%)**: Bambú (`-28%`), Hierro bruto (`-32%`), Carne podrida (`-35%`), Cobblestone (`-40%`), Algas (`-45%`), Semillas (`-48%` a `-50%`).
     - **Estructura de Lore Financiero en cada ítem**:
       - `Tendencia`: indicador porcentual y estado visual (`▲ En Auge` vs `▼ Desplome`).
       - `Precio Actual`: unitario y stack x64 con formato canónico verde `#59E91F`.
       - `Rango Permitido`: límite suelo (*mínimo*) y límite techo (*máximo*) para evitar dupes de arbitraje.
       - `Demanda`: nivel cualitativo de presión compradora/vendedora.
     - **Fila 5 (slots 36-44)**: Respirador visual con paneles grises.
     - **Fila 6 (slots 45-53)**: Navbar con comparador de ordenación (slot 45), volver a `mercado_comercio` (slot 49), Venta Rápida (slot 52) y balance (slot 53).
  2. **Registro y Despliegue**:
     - Registrado en `DeluxeMenus/config.yml` con comandos `/lonja`, `/mercadoventa` y `/bolsaventa`.
     - Subido al servidor Sandbox vía SFTP.

---

## [2026-09-07] ui & deluxemenus | Reestructuración de mercado_comercio.yml a 4 Filas Aislado
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/mercado_comercio.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Rediseño a 4 Filas (`size: 36`)**:
     - Fila 1 (slots 0-8): Aire limpio.
     - Fila 2 (slots 9-17): **Slot 11 (Tienda de Compra)** con `CHEST_MINECART` y **Slot 15 (Tienda de Venta)** con `HOPPER_MINECART`.
     - Fila 3 (slots 18-26): Separador de aire visual para evitar que el contenido esté pegado al navbar.
     - Fila 4 (slots 27-35): Navbar inferior con paneles grises, botón salir en slot 31 (`DARK_OAK_DOOR` con `[close]`) y balance en slot 35 (`head-%player_name%`).
  2. **Aislamiento Total**: Desconectados los clicks de redirecciones a menús preexistentes.
  3. **Autoaprendizaje**: Registrada la Lección 6 en `wiki/concepts/deluxemenus_standards.md`.
  4. **Despliegue**: Subido a Sandbox por SFTP.

---

## [2026-09-07] infra & skills | Creación del Skill deluxemenus-builder y Consolidación de Lecciones Aprendidas
- **Módulo**: `.agents/skills/deluxemenus-builder/SKILL.md`, `wiki/concepts/deluxemenus_standards.md`
- **Trabajo Realizado**:
  1. **Skill Creado**: `.agents/skills/deluxemenus-builder/SKILL.md` con base de conocimiento completa:
     - Paleta canónica de colores y símbolos de las 4 divisas (Dinero, Almas, Zafiros, XP).
     - Patrones de diseño canonizados: botones de categoría, balance, volver, navbar.
     - Layouts por tipo de menú (principal, intermediario, informativo).
     - Árbol de navegación completo del servidor.
     - Sintaxis obligatoria y prohibiciones (legacy vs. moderno).
     - Protocolo de feedback y autoaprendizaje con formato estándar de lección.
  2. **Lecciones Consolidadas en Wiki**: `wiki/concepts/deluxemenus_standards.md` ampliado con 5 lecciones derivadas del feedback real del Sr Ramos en esta sesión de trabajo.
  3. **Contexto**: Subagente listo para invocarse cuando el Sr Ramos pida crear o modificar un menú de DeluxeMenus. Lee las lecciones acumuladas antes de cada producción y guarda nuevas lecciones tras cada feedback.

---

## [2026-09-07] shopgui & core | Solución de Balance Dinámico Nativo en ShopGUIPlus para Almas y Experiencia
- **Módulo**: `plugins/ShopGUIPlus/shops/spawners_almas.yml`, `llaves_almas.yml`, `protecciones_almas.yml`, `trims.yml`, `encantamientos.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Diagnóstico del Motor de Balances**:
     - Constatado que ShopGUIPlus no ejecuta el parser de PlaceholderAPI en ítems decorativos estáticos (`type: dummy`).
     - Descompilado `ThunderCurrencys-1.0.jar` (`ShopGuiHook.class` y `ThunderEconomyProvider.class`), confirmando que el plugin implementa la API de economías custom de ShopGUIPlus bajo el identificador `almas`.
  2. **Migración a Botones Nativos (`type: special`)**:
     - Actualizado el slot 44 de las 3 tiendas de Almas (`spawners_almas.yml`, `llaves_almas.yml`, `protecciones_almas.yml`) reemplazando los ítems `dummy` por `type: special` con `special: balance`.
     - Actualizado el slot 44 de las 2 tiendas de Experiencia (`trims.yml`, `encantamientos.yml`) para emplear `type: special` con `special: balance` en su economía nativa `EXP_LEVELS`.
  3. **Despliegue**:
     - Subidos los 5 archivos modificados vía SFTP al servidor Sandbox de pruebas.

---

## [2026-09-07] shopgui & ui | Eliminación del Catálogo de Precios en Menús Secundarios (Exclusividad en Menú Principal)
- **Módulo**: `plugins/ShopGUIPlus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Purga de `Catálogo de Precios` (`SPYGLASS`) en Menús Secundarios**:
     - Retirado el ítem de `SPYGLASS` (slot 27) del menú principal de categorías de dinero en ShopGUIPlus (`plugins/ShopGUIPlus/config.yml`).
     - Detectado y purgado el `SPYGLASS` residual en el slot 36 de las subtiendas de Experiencia (`trims.yml` y `encantamientos.yml`).
     - Reemplazado el slot 36 en `trims.yml` y `encantamientos.yml` por el **Filtrador de Categoría (`COMPARATOR`)** con lore exclusivo de las 2 categorías de XP (rotación cíclica `Trims ➔ Encantamientos ➔ Trims`).
     - Añadido el botón de retorno (`DARK_OAK_DOOR`) en el slot 40 que regresa ordenadamente a `mercado_xp`.
     - Confirmada la total ausencia de botones de catálogo en todas las subtiendas y menús intermediarios.
  2. **Exclusividad Preservada**:
     - El botón de `Catálogo de Precios` (`SPYGLASS`) permanece exclusivamente en el menú principal (`tienda_principal.yml`, slot 27).
  3. **Despliegue**:
     - Subidos `ShopGUIPlus/config.yml`, `trims.yml` y `encantamientos.yml` vía SFTP al Sandbox (`ymykh9qy.274758bd`).

---

## [2026-09-07] shopgui & ui | Menú Intermediario de Almas y División en 3 Categorías con Filtrador Cíclico
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/mercado_almas.yml`, `tienda_principal.yml`, `config.yml`, `plugins/ShopGUIPlus/shops/spawners_almas.yml`, `llaves_almas.yml`, `protecciones_almas.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Nuevo Menú Intermediario de Categorías (`mercado_almas.yml`)**:
     - Creado en DeluxeMenus con tamaño de 4 filas (`size: 36`) y registrado bajo comandos `/shop almas` y `/mercado almas`.
     - Fila central simétrica con las 3 categorías principales:
       - **Slot 11 (Spawners)**: Icono `SPAWNER` (8 artículos a cambio de almas). Abre `shop spawners_almas`.
       - **Slot 13 (Llaves)**: Icono `TRIPWIRE_HOOK` con glow (5 artículos). Abre `shop llaves_almas`.
       - **Slot 15 (Protecciones)**: Icono `DIAMOND_ORE` con glow (6 artículos). Abre `shop protecciones_almas`.
     - Barra inferior (slots 27-35) con paneles grises, botón de retorno en slot 31 (`DARK_OAK_DOOR` hacia `tienda_principal`) y balance de almas en slot 35 (`SOUL_CAMPFIRE` con placeholder `%thundercurrencys_almas%`).
  2. **División de la Tienda de Almas en 3 Subtiendas ShopGUIPlus**:
     - Creadas `spawners_almas.yml`, `llaves_almas.yml` y `protecciones_almas.yml` preservando exactamente comandos originales, precios y economía (`almas`).
     - Navbar inferior estándar (slots 36 a 44) en cada tienda:
       - Slot 36: **Filtrador de Categoría (`COMPARATOR`)** con glow y lore reactivo (`#FFF275●` en la activa y `&7●` en las inactivas), enlazando un ciclo continuo: `Spawners ➔ Llaves ➔ Protecciones ➔ Spawners`.
       - Slot 40: Botón de retorno (`DARK_OAK_DOOR`) que regresa a `mercado_almas`.
       - Slot 44: Balance visual de almas (`SOUL_CAMPFIRE`).
  3. **Integración Global y Despliegue**:
     - Actualizado `tienda_principal.yml` (slot 14 `Boton_Almas`) para abrir el menú intermediario `[openguimenu] mercado_almas`.
     - Registrado `mercado_almas` en `DeluxeMenus/config.yml`.
     - Subidos todos los archivos vía SFTP al Sandbox de pruebas (`ymykh9qy.274758bd`).

---

## [2026-09-07] shopgui & ui | Expansión de Tienda de Banners a 4 Páginas con Figuras y Diseños Custom de Minecraft Tools
- **Módulo**: `plugins/ShopGUIPlus/shops/banners.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Expansión Multilista a 4 Páginas Completas en ShopGUIPlus**:
     - Las 3 filas centrales (slots 9 a 35 = 27 slots de tienda) han quedado 100% llenas en todas las páginas sin huecos ni cristales invasivos:
       - **Página 1 (27 ítems)**: 16 Banners clásicos monocromáticos (slots 9 a 24) + 11 Banners custom (slots 25 a 35, incluyendo Fox, Ominous, Ender Dragon, Sunshine, Angel, etc.).
       - **Página 2 (27 ítems)**: 27 Banners custom con figuras de criaturas, fauna y monstruos (slots 9 a 35).
       - **Página 3 (27 ítems)**: 27 Banners custom de cosmos, elementos, paisajes y emblemas (slots 9 a 35).
       - **Página 4 (27 ítems)**: 27 Banners custom de cultura pop, símbolos, armas y banderas (slots 9 a 35).
     - Total: 16 banners base + 92 banners custom únicos curados directamente desde la galería de Minecraft Tools.
  2. **Corrección de Navbar y Flechas de Navegación**:
     - Eliminados los cristales espurios que ocupaban las posiciones 33, 34 y 35 (ahora son slots de compra activos).
     - En **Página 1**, donde no existe página anterior, se añade un cristal de relleno gris en el **Slot 39** para evitar el hueco vacío.
     - En **Página 4**, donde no existe página siguiente, se añade un cristal de relleno gris en el **Slot 41**.
     - En páginas intermedias (2 y 3), ShopGUIPlus renderiza de forma limpia las flechas nativas en slots 39 y 41 con retorno en slot 40, comparador en 36 y balance en 44.
  3. **Despliegue y Validación**:
     - Generado y verificado sin errores sintácticos.
     - Subido vía SFTP al servidor Sandbox de pruebas (`ymykh9qy.274758bd`).

---

## [2026-09-07] shopgui & ui | Menú de Dinero a 4 Filas, Categorías en Línea Única y Creación de Tienda de Banners
- **Módulo**: `plugins/ShopGUIPlus/config.yml`, `plugins/ShopGUIPlus/shops/banners.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Reestructuración a 4 Filas (`shopMenuSize: 36`)**:
     - Fila 1 (slots 0-8): Fondo limpio.
     - Fila 2 (slots 9-17): Las 9 categorías del mercado de dinero alineadas de forma horizontal continua:
       - Slot 9: `Bloques` (GRASS_BLOCK)
       - Slot 10: `Farmeo` (WHEAT)
       - Slot 11: `Comida` (COOKED_BEEF)
       - Slot 12: `Mobs` (GUNPOWDER)
       - Slot 13: `Equipo` (TOTEM_OF_UNDYING)
       - Slot 14: `Redstone` (REDSTONE)
       - Slot 15: `Misceláneo` (SADDLE)
       - Slot 16: `Tintes` (RED_DYE)
       - Slot 17: `Banners` (CYAN_BANNER)
     - Fila 3 (slots 18-26): Fondo limpio.
     - Fila 4 (slots 27-35): Barra de navegación homogénea:
       - Slot 27: `Catálogo de Precios` (SPYGLASS)
       - Slot 31: `Volver Atrás` (DARK_OAK_DOOR)
       - Slot 35: `Tu Economía` (KELP)
       - Slots restantes con paneles grises decorativos.
  2. **Creación y Perfeccionamiento de la Tienda `banners.yml`**:
     - Título estandarizado: `&0&l|&r &0Mercado ▶ &8Banners &8(#59E91F$&8)`.
     - Fila superior decorativa (slots 0-8) y slots 33-35 con paneles de cristal gris (`GRAY_STAINED_GLASS_PANE`).
     - Eliminados los patrones de telar (`BANNER_PATTERN`).
     - 16 Banners clásicos base (todos los colores) a $50 c/u.
     - 8 Banners con diseños pre-ensamblados complejos ($150 - $200):
       - **Fox Banner** (Diseño de Minecraft Tools suministrado por el Sr Ramos, adaptado a la sintaxis nativa de ShopGUIPlus `patterns: <id>: color: ... type: ...`).
       - **Ominous Banner**, **Ender Dragon Banner**, **Solar Phoenix Banner**, **Pirate Skull Banner**, **Thunder Storm Banner**, **Arcane Portal Banner** y **Royal Shield Banner**.
     - Barra de navegación inferior completa (slots 36-44) con botón de retorno en slot 40 y balance en slot 44.
  3. **Estandarización Total del Filtrador de Categorías (`COMPARATOR`)**:
     - Se depuraron las 8 tiendas existentes (`bloques`, `farmeo`, `comida`, `mobs`, `equipo`, `redstone`, `miscellaneo`, `tintes`) junto con `banners`:
       - Removidas categorías ajenas al dinero (`Trims` y `Encantamientos`, las cuales pertenecen a la divisa XP).
       - Añadido `Banners` en todas las listas.
       - Ciclo continuo cerrado enlazado por `commandsOnClick`: Bloques ➔ Farmeo ➔ Comida ➔ Mobs ➔ Equipo ➔ Redstone ➔ Misceláneo ➔ Tintes ➔ Banners ➔ Bloques.
  4. **Despliegue**:
     - Subidos `config.yml` y las 9 tiendas al servidor de pruebas vía SFTP.

---

## [2026-09-07] shopgui & ui | Creación del Submenú Informativo de Economías (`info_economia.yml`)
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/info_economia.yml`, `tienda_principal.yml`, `plugins/DeluxeMenus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Nuevo Submenú de 4 Filas (`info_economia.yml`)**:
     - Registrado en DeluxeMenus bajo comandos `/economia` e `/infoeconomia`.
     - Fila central estructurada:
       - **Slot 10**: Cabeza del jugador (`head-%player_name%`) con resumen conceptual del ecosistema económico múltiple de ThunderMC.
       - **Slot 11**: Espaciado neutro.
       - **Slots 12 a 15**: Los 4 iconos económicos con efecto brillante (`glow: true` vía `DURABILITY;1` + `HIDE_ENCHANTS`), desglosando utilidades, balances en tiempo real y métodos de obtención calificados con estrellas (⭐⭐⭐⭐⭐):
         - **Slot 12 (Zafiros - DIAMOND)**: Economía premium, obtención exclusiva en tienda web (ejecuta `/tienda` al hacer click) y cajas especiales.
         - **Slot 13 (Dinero - EMERALD)**: Utilidad universal (`/rankup`, `/shop`, `/ah`). Métodos desglosados (Granjas de Spawners ⭐⭐⭐⭐⭐, Comercio `/ah` ⭐⭐⭐⭐, Venta al Shop ⭐⭐⭐, Trabajos `/jobs` ⭐⭐⭐, Crates ⭐⭐⭐, Dungeons ⭐).
         - **Slot 14 (Almas - SOUL_CAMPFIRE)**: Materiales y llaves de mazmorra (`/almas`). Métodos (Jefes ⭐⭐⭐⭐⭐, Mobs ⭐⭐⭐⭐, scaling por nivel de mazmorra, sin aparición en crates comunes).
         - **Slot 15 (Experiencia - EXPERIENCE_BOTTLE)**: Trims (`/shop xp`), encantamientos custom y yunques. Métodos (Granjas ⭐⭐⭐⭐⭐, Vanilla natural ⭐⭐⭐⭐, Botellas en crates ⭐⭐⭐).
     - Fila 4: Barra inferior limpia con botón de retorno al menú principal en slot 31 (`DARK_OAK_DOOR`).
  2. **Estilización y Formateo Visual de Lores (`info_economia.yml`)**:
     - Margen izquierdo de 1 espacio en encabezados de sección (` ¿Para qué sirve? ` y ` ¿Cómo se consigue? `) con el color hex de cada divisa.
     - Tipografía custom **Thunder Small Caps** aplicada a todas las descripciones secundarias de los métodos en gris (`&7`): ej. `ᴜɴɪᴄᴀ ᴇɴ ᴛɪᴇɴᴅᴀ ᴡᴇʙ`, `ᴘʀᴏᴅᴜᴄᴄɪᴏɴ ᴍᴀꜱɪᴠᴀ`, `ᴠᴇɴᴛᴀ ᴀ ᴊᴜɢᴀᴅᴏʀᴇꜱ`, `ᴅᴇʀʀᴏᴛᴀʀ ʙᴏꜱꜱᴇꜱ`, `ꜰᴀʀᴍᴇᴏ ᴍᴀꜱɪᴠᴏ`.
     - Eliminado el separador `&8| ` al inicio de los métodos numerados, mostrando directamente el círculo numérico (` &#1E6BFF① `, ` &#59E91F① `, etc.).
     - Títulos de métodos en blanco nítido (`&f`) y estrellas en amarillo (`&e⭐⭐⭐⭐⭐`).
     - Reducción horizontal de líneas para evitar desbordes en pantalla.
  3. **Interconexión y Catálogo de Precios en `tienda_principal.yml`**:
     - Al hacer click en el botón de balance `Tu Economía` (slot 35), ejecuta `[openguimenu] info_economia`.
     - Actualizado el botón del Catálogo de Precios (slot 27):
       - Título: `&#59E91FCatálogo de Precios` con subtítulo `&8ᴍᴇʀᴄᴀᴅᴏ ᴅᴇ ᴅɪɴᴇʀᴏ`.
       - Lore explicativo: `Consulta los objetos con mayor o menor precio del mercado de dinero`.
  4. **Despliegue**:
     - Subidos `info_economia.yml`, `tienda_principal.yml` y `config.yml` al servidor de pruebas vía SFTP.

---

## [2026-09-07] shopgui & ui | Reordenamiento, Coloreado y Embellecimiento del Menú Principal
- **Módulo**: `plugins/DeluxeMenus/gui_menus/menusIA/tienda_principal.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Reordenamiento de Mercados (Fila Central)**:
     - Slot 10: **Mercado Zafiros** (Diamante).
     - Slot 12: **Mercado Dinero** (Esmeralda).
     - Slot 14: **Mercado Almas** (Soul Campfire).
     - Slot 16: **Mercado Experiencia** (Botella de XP).
  2. **Colores Temáticos por Moneda en Títulos**:
     - Mercado Zafiros: `&#1E6BFFMercado Zafiros`
     - Mercado Dinero: `&#59E91FMercado Dinero`
     - Mercado Almas: `&#34B0F3Mercado Almas`
     - Mercado Experiencia: `&#D48BFFMercado Experiencia`
  3. **Embellecimiento Lore Zafiros**:
     - Adaptado al estatus de economía premium: `Adquiere cosméticos, beneficios y artículos de élite con tus gemas de zafiro`.
  4. **Despliegue**:
     - Sincronizado vía SFTP al servidor de pruebas.

---

## [2026-09-07] shopgui & ui | Estandarización de Títulos de Mercados y Tiendas por Moneda
- **Módulo**: `plugins/ShopGUIPlus/config.yml`, `shops/*.yml`, `plugins/DeluxeMenus/gui_menus/menusIA/mercado_xp.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Títulos de Menús de Selección de Categoría**:
     - Mercado Dinero (`shopMenuName` en ShopGUIPlus): `&0&l|&r &0Mercado ▶ #59E91FDinero &8(#59E91F$&8)` (sin `&` para ShopGUIPlus).
     - Mercado Experiencia (`mercado_xp.yml` en DeluxeMenus): `&0&l|&r &0Mercado ▶ &#D48BFFExperiencia &8(&#D48BFF✦&8)` (con `&#` requerido por el parser de DeluxeMenus).
  2. **Títulos de Subtiendas / Categorías Específicas**:
     - Se formateó el nombre de la categoría en `&8<Nombre>` seguido del indicador de divisa `&8(<SimboloColor>&8)`:
       - Dinero (`$` en `#59E91F`): `Bloques`, `Comida`, `Equipo`, `Farmeo`, `Misceláneo`, `Mobs`, `Redstone`, `Tintes` ➔ `&0&l|&r &0Mercado ▶ &8<Cat> &8(#59E91F$&8)`
       - Almas (`🔥` en `#34B0F3`): `almas.yml` ➔ `&0&l|&r &0Mercado ▶ &8Almas &8(#34B0F3🔥&8)`
  3. **Ajustes en Menús DeluxeMenus (`mercado_xp.yml` y `tienda_principal.yml`)**:
     - Corregidos todos los colores hexadecimales en los lores (`#D48BFF` ➔ `&#D48BFF`) para que el parser de DeluxeMenus interprete el morado.
     - Simplificada la nomenclatura de la divisa de XP a `&#D48BFFXP (Lvl)` en los lores de `mercado_xp.yml` y `tienda_principal.yml`.
     - Añadidas directivas exhaustivas de ocultación (`hide_attributes: true`, `hide_enchantments: true`, `hide_all_flags: true` y lista completa de `item_flags` Spigot 1.21 como `HIDE_ADDITIONAL_TOOLTIP`, `HIDE_ITEM_SPECIFICS`, `HIDE_ARMOR_TRIM`) en el icono `Categoria_Trims`.
  4. **Despliegue**:
     - Todos los ficheros fueron actualizados y subidos al servidor de pruebas vía SFTP.

---

## [2026-09-07] shopgui & ui | Corrección de Formato Hexadecimal en Títulos de ShopGUIPlus
- **Módulo**: `plugins/ShopGUIPlus/config.yml`, `shops/*.yml` (`almas`, `bloques`, `comida`, `equipo`, `farmeo`, `miscellaneo`, `mobs`, `redstone`, `tintes`), Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Auditoría de Formatos Hexadecimales**:
     - Localizadas las definiciones de títulos (`name:` en tiendas y `shopMenuName:` en config principal) que contenían el prefijo `&#RRGGBB` en vez del formato estándar `#RRGGBB` que utiliza ShopGUIPlus en Spigot/Paper para los títulos de inventarios.
  2. **Corrección Aplicada**:
     - Modificado `shopMenuName` en `config.yml` a `&0&l|&r &0Mercado ▶ #59E91FDinero`.
     - Modificados los `name:` en las 9 tiendas afectadas reemplazando `&#` por `#`.
  3. **Despliegue**:
     - Archivos sincronizados al servidor de pruebas vía SFTP.

---

## [2026-09-07] shopgui & ui | Retiro de Tolva de Venta Rápida de Subtiendas y Menús Secundarios
- **Módulo**: `plugins/ShopGUIPlus/config.yml`, `shops/almas.yml`, `shops/encantamientos.yml`, `shops/trims.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Retiro del Botón Venta Rápida (Tolva)**:
     - Removido el ítem tolva (`HOPPER`) del slot 43 en la navbar global de categorías (`config.yml` de ShopGUIPlus).
     - Removido el botón tolva de las tiendas que sobrescribían la navbar: `almas.yml`, `encantamientos.yml` y `trims.yml`.
     - Reemplazado el slot 43 por panel decorativo neutro (`GRAY_STAINED_GLASS_PANE`) para mantener la simetría y limpieza visual en la fila inferior.
  2. **Preservación Exclusiva**:
     - Mantenido exclusivamente en:
       - **Menú de Venta**: `tienda_vender.yml` (DeluxeMenus) y `venta.yml` (ShopGUIPlus).
       - **Menú Principal**: `tienda_principal.yml` (DeluxeMenus).
  3. **Despliegue**:
     - Subidos los archivos actualizados al servidor de pruebas vía SFTP.

---

## [2026-09-07] shopgui & ui | Diagnóstico de Tolva Venta Rápida en Menú de Almas y Reestructuración de Mercados
- **Módulo**: `plugins/ShopGUIPlus/shops/almas.yml`, `creator/output/MenusIA/tienda_principal.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Realizado**:
  1. **Diagnóstico Venta Rápida (Tolva)**:
     - Identificado que en ShopGUIPlus 1.113.0 los ítems `type: dummy` ignoran directivas de click como `commandsOnClick`.
     - Determinada la causa raíz de la falta de respuesta de la tolva en `/shop almas`.
  2. **Reestructuración de Categorías**:
     - Documentadas las directrices para reorganización de mercados en la tienda principal (Dinero, Almas, Zafiros, Experiencia).

---

## [2026-09-06] shopgui & ui | Configuración de Iconos Económicos por Tienda (XP y Almas)
- **Módulo**: `plugins/ShopGUIPlus/shops/encantamientos.yml`, `plugins/ShopGUIPlus/shops/trims.yml`, `plugins/ShopGUIPlus/shops/almas.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Completado**:
  1. **Tiendas de Experiencia (`encantamientos.yml` y `trims.yml`)**:
     - Motor económico: `economy: EXP_LEVELS`.
     - Botón de economía contextual en slot 44 configurado como `type: special` + `special: balance` (para que el motor nativo procese la llamada `replacePlaceholder` de `%balance%` en tiempo real):
       - Material: `EXPERIENCE_BOTTLE`.
       - Efecto: `glow: true`.
       - Color mágico: Morado claro legible `#D48BFF` (`#D48BFFTu Economía`).
       - Formato de lore: `&8| &fNivel de XP: #D48BFF%balance% LVL DE XP`.
     - Barra de navegación estandarizada en ambas tiendas (Slot 36: `SPYGLASS`, Slot 40: `DARK_OAK_DOOR`, Slot 43: `HOPPER`).
  2. **Tienda de Almas**:
     - Homogeneizada la navbar inferior para incluir el botón de Catálogo de Precios en el slot 36 (`SPYGLASS`) y Venta Rápida en el slot 43 (`HOPPER`), manteniendo el botón de almas en el slot 44 (`SOUL_CAMPFIRE`).
  3. **Despliegue**:
     - Archivos subidos al servidor de pruebas vía SFTP.

---

## [2026-09-06] shopgui & ui | Ajustes en amountSelectionGUI, BuyMore (CHEST_MINECART) y BulkBuy
- **Módulo**: `plugins/ShopGUIPlus/config.yml`, Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Trabajo Completado**:
  1. **amountSelectionGUI (Reducción a 3 Filas y Nuevo Layout)**:
     - Tamaño minimizado a `size: 27` (3 filas).
     - Intercambiados de lugar los shulkers:
       - Cancelar: `RED_SHULKER_BOX` en slot `12` (izquierda del ítem).
       - Confirmar: `LIME_SHULKER_BOX` en slot `14` (derecha del ítem).
     - Slot central del ítem fijado en `13`.
     - Fondo limpio (`AIR`).
  2. **Botón Comprar Stacks (`buyMore`) Reubicado y Simplificado**:
     - Posicionado en el slot `22` (**justo debajo** del ítem que se compra en el slot 13).
     - Icono: `CHEST_MINECART`.
     - Textos simplificados para evitar ancho horizontal excesivo (`&8Varios stacks` / `&7▶ Elegir cantidad`).
  3. **Formatos de Precios, Lores y Márgenes de Espaciado**:
     - Añadido salto de línea entre la línea de cantidad y la de precio total en `itemBuyGUI` y `itemSellGUI`.
     - Añadido margen inferior de 1 espacio entre el precio y el final del tooltip.
     - Añadido símbolo `$` en negrita (`#59E91F&l$&r#59E91F%balance%`) en el elemento especial `balance` de ShopGUIPlus y en el botón `Info_Balance` del menú principal DeluxeMenus (`&#59E91F&l$&r&#59E91F%vault_eco_balance_formatted%`).
     - Estandarización de iconos de economía: `KELP` para dinero ($), `EXPERIENCE_BOTTLE` para experiencia y `SOUL_CAMPFIRE` para almas.
     - Corrección y estandarización del símbolo `$` y formato negrita en textos de compra y venta.
  4. **Navbar del Menú de Categorías (`shopMenuItems`) Homogeneizada**:
     - Integrados los botones del menú principal en la barra inferior (fila 5, slots 36-44):
       - **Slot 36**: `Catálogo de Precios` (`SPYGLASS`, ejecuta `dm open precios_todos`).
       - **Slots 37, 38, 39**: Paneles de cristal gris decorativo (`GRAY_STAINED_GLASS_PANE`).
       - **Slot 40**: `Volver Atrás` (`DARK_OAK_DOOR`, ejecuta `dm open tienda_principal`).
       - **Slots 41, 42**: Paneles de cristal gris decorativo (`GRAY_STAINED_GLASS_PANE`).
       - **Slot 43**: `Venta Rápida` (`HOPPER`, ejecuta comando `sellgui`).
       - **Slot 44**: `Tu Economía` (`special: balance`, `SUNFLOWER` con `$`).
  5. **Despliegue**:
     - Sincronizado vía SFTP en el servidor Sandbox (`plugins/ShopGUIPlus/config.yml`).



---

## [2026-09-05] docs & ingesta | Ingesta Técnica de ShopGUIPlus y Validación Estructural de Tiendas
- **Módulo**: `wiki/sources/shopguiplus-official-docs.md`, `plugins/ShopGUIPlus/`
- **Trabajo Completado**:
  1. **Ingesta Integral de la Documentación Oficial**:
     - Lectura y síntesis técnica de `shops-items-setup`, `item-meta`, `commands-permissions`, `hidden-options` y `price-modifiers`.
     - Creación de [`wiki/sources/shopguiplus-official-docs.md`](file:///C:/Users/tecno/Desktop/ThunderCerebro/wiki/sources/shopguiplus-official-docs.md) y catalogación en `index.md`.
  2. **Auditoría de Configuraciones Existentes**:
     - Verificación de la jerarquía estricta de propiedades (`buyPrice`, `sellPrice`, `slot` y `commandsOnClick` fuera de `item:`).
     - Validación de compatibilidad con UTF-8 y eliminación de caracteres small caps conflictivos en clientes de Minecraft.
     - Confirmación del pipeline de compra nativo `amountSelectionGUI` y desacoplamiento de DeluxeMenus.

---

## [2026-09-05] menus & ui | Rediseño de Filtro por Comparador y Paginación en Catálogo de Precios
- **Módulo**: `creator/output/MenusIA/`, `plugins/DeluxeMenus/` (Servidor de Pruebas)
- **Trabajo Completado**:
  1. **Nuevo Sistema de Filtro Secuencial (`COMPARATOR`)**:
     - Botón brillante (`COMPARATOR` con glow) ubicado en el slot 36 (abajo a la izquierda).
     - Ciclo continuo por clic: `TODOS` (41 ítems) → `CULTIVOS` (21 ítems) → `DROPS DE MOBS` (19 ítems) → `ESPECIALES` (1 ítem) → `TODOS`.
  2. **Paginación Dinámica para el Modo TODOS**:
     - Estructura de 5 filas mantenida intacta.
     - Paginación automática en la barra inferior a los lados del botón Volver (`Slot 39: Anterior`, `Slot 40: Volver`, `Slot 41: Siguiente`).
     - Creación de [`precios_todos.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/creator/output/MenusIA/precios_todos.yml) (Pág 1) y [`precios_todos_2.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/creator/output/MenusIA/precios_todos_2.yml) (Pág 2).
  3. **Refinamiento de Layout y Lores**:
     - Primera fila rellenada completamente con paneles de cristal gris decorativo (`Filtro_Top` slots 0-8).
     - Margen inferior (`- ''`) añadido en el lore de precio de todos los ítems.
     - Títulos contextuales en la barra superior según la categoría activa.
  4. **Despliegue y Registro**:
     - Sincronizados todos los archivos en `plugins/DeluxeMenus/gui_menus/menusIA/` del servidor de Pruebas.
     - Registrados `precios_todos` y `precios_todos_2` en `plugins/DeluxeMenus/config.yml`.
     - Actualizado [`tienda_principal.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/creator/output/MenusIA/tienda_principal.yml) para abrir el catálogo global por defecto.

---

## [2026-09-02] analytics & ops | Análisis Mensual Agosto 2026 y Diagnóstico de Rendimiento / Granjas
- **Módulo**: `wiki/synthesis/`, `.agents/skills/analisisdelmes/`
- **Trabajo Completado**:
  1. **Informe Mensual Agosto 2026**:
     - Procesamiento de base de datos SQLite de Plan (`database.db`, 28.8k sesiones, 2.5k usuarios).
     - Progresión semana a semana, retención, stickiness DAU/WAU, análisis de churn, rendimiento MSPT/TPS y posicionamiento de mercado Tier 2 emergente.
     - Documentos generados en [`informe-agosto-2026.md`](file:///C:/Users/tecno/Desktop/TrabajoSucio/informe-agosto-2026.md).
  2. **Skill `analisisdelmes` Creado**:
     - Pipeline automatizado con `SKILL.md`, `scripts/full_analysis.js`, `scripts/schema_discovery.js` y `references/plantilla-informe.md`.
  3. **Diagnóstico y Plan de Optimización de Granjas Survival**:
     - Conexión SFTP a Survival (`MIA-251006.bloom.host:2022`) e inspección de `paper-world-defaults.yml`, `spigot.yml`, `server.properties`, `SilkSpawners_v2` y `ProtectionStones`.
     - Identificado cuello de botella de MSPT (33ms) por ausencia de stacking de mobs/spawners, granjas en bordes de 4 chunks y falta de AFK kick.
     - Documentado plan de acción y configuraciones exactas en [`wiki/synthesis/optimizacion-granjas-survival.md`](file:///C:/Users/tecno/Desktop/ThunderCerebro/wiki/synthesis/optimizacion-granjas-survival.md).

---

## [2026-08-28] ui & polish | Refinamiento Maestro de la Tienda Tebex (Botones, HUD Timer y Pase Alien)
- **Módulo**: `Instalacion Tebex/` (`index.html`), `creator/lab/tienda-tebex/`
- **Cambios Completados**:
  1. **Estructura de Acciones Unificada**:
     - Botón principal de compra directa: `AGREGAR AL CARRITO` (`tz-btn-add-cart`) con diseño consistente dorado `#facc15` sin glows en todos los paquetes.
     - Botón secundario de información `[i]` posicionado a la izquierda (`tz-btn-info`) con disparo modal AJAX (`triplezone__toogle--modal`).
     - Eliminación de botones flotantes antiguos de carrito rápido en cabecera de cards.
  2. **Rangos VIP (LITE, STAR, MEGA)**:
     - Personajes sobresalen verticalmente (`overflow: visible`).
     - Fondos vívidos flat con textura sutil geométrica: Lima (`#84cc16`), Amarillo potente (`#facc15`) y Morado rosado (`#c084fc`).
     - Títulos exteriores coloreados en sintonía con su zona temática.
  3. **Banner del Pase de Temporada (Temática Alienígena / Slime)**:
     - Fondo bioluminiscente verde alienígena con textura orgánica celular y libre de rebordeados agresivos.
     - Tipografía de alto contraste con subtítulo en verde menta claro `#bbf7d0`.
     - **HUD Modular de Temporizador**: Bloques segmentados en vivo (`[Días] : [Horas] : [Min] : [Seg]`) con cuenta regresiva dinámica a 60 días en JavaScript.
  4. **Persistencia & Entregables**:
     - Sincronizado en [`Instalacion Tebex/index.html`](file:///C:/Users/tecno/Desktop/ThunderCerebro/Instalacion%20Tebex/index.html) y en el entorno de pruebas local `creator/lab/tienda-tebex/`.

---

## [2026-08-28] asset & ui | Replicación Exacta de Rangos VIP 1:1 (ejemplss.PNG)
- **Módulo**: `Instalacion Tebex/` (`index.html`, `Assets/`)
- **Implementación Idéntica a Referencia Visual**:
  1. **Títulos y Badges Superiores**: Barra externa `.tz-vip-top-title-bar` alineada por encima de cada tarjeta (`Rango LITE`, `Rango STAR`, `Rango MEGA` en `26px`).
  2. **Fondos y Auras Circulares Fijas (Exactas a la captura)**:
     - **LITE**: Fondo `#091712`, borde sólido `#10b981` y resplandor circular interior centrado en `rgba(16, 185, 129, 0.22)`.
     - **STAR**: Fondo `#191408`, borde sólido `#facc15` y resplandor circular interior centrado en `rgba(250, 204, 21, 0.26)`.
     - **MEGA**: Fondo `#170d24`, borde sólido `#a855f7` y resplandor circular interior centrado en `rgba(168, 85, 247, 0.25)`.
  3. **Cero Distorsiones o Animaciones Invasivas**: Fondos estáticos, sombras limpias superiores y sin cortes en la base.
- **Sincronización**: Reflejado en `Instalacion Tebex/index.html` y `creator/lab/tienda-tebex/index.html`.

---

## [2026-08-28] feature | Reestructuración Comercial y Estratégica del Catálogo Tebex
- **Módulo**: `Instalacion Tebex/` (`index.html`, `Assets/layout.header.twig`)
- **Implementación de Estrategia de Marketing & Monetización**:
  1. **Bloque 1 — 3 Rangos VIP Permanentes (Grid 3 Columnas)**:
     - **LITE** (4,99 €): Acceso inicial, 4 homes, /nick, partículas y 200 Zafiros de regalo.
     - **STAR** (14,99 €) [SEÑUELO / MÁS POPULAR]: Destacado con gradiente y badge ámbar, /fly en zonas seguras, 6 homes, prioridad y 500 Zafiros.
     - **MEGA** (29,99 €) [ANCLA / EXCLUSIVO]: Homes ilimitados, prefijo animado, tag [MEGA], NPC en Spawn, canal VIP Discord y 1.200 Zafiros.
  2. **Bloque 2 — Banner Horizontal del Pase de Temporada**:
     - Formato horizontal envolvente para la Temporada 1 (*Invasión Mítica*), 50 niveles y precio de 7,99 €.
  3. **Bloque 3 — 2 Filas de Paquetes de Zafiros (3 por fila, 6 paquetes en total)**:
     - Fila 1: Pequeño (250 zaf / 2,99 €), Mediano (+10% / 550 zaf / 4,99 €) y Popular ⭐ (+15% / 1.265 zaf / 9,99 € — resaltado).
     - Fila 2: Grande (+20% / 2.760 zaf / 19,99 €), XL (+25% / 6.000 zaf / 39,99 €) y Caja del Tesoro (+30% / 13.000 zaf / 79,99 € — ancla de valor).
     - Badge superior con mensaje de conversión: *+50% Bonus Extra en tu 1ª Compra*.
  4. **Bloque 4 — Otros Servicios (Desbaneo)**:
     - Apartado minimalista con la tarjeta de Pase de Desbaneo (15,00 €).
  5. **Navegación Sincronizada**: Menú de categorías, dropdown de navbar y drawer móvil enlazados con scroll suave hacia `#cat-rangos`, `#cat-pase`, `#cat-zafiros` y `#cat-otros`.

---

## [2026-08-28] ingest | Plan Maestro de Monetización ThunderMC
- **Módulo**: `Plan de Monetizacion/`, `wiki/concepts/`
- **Fuente Ingestada**: `C:\Users\tecno\Downloads\Estrategia_Monetizacion_Servidor_Minecraft.md` + conversación raw de ideación con Sr Ramos
- **Archivos Creados**:
  1. `Plan de Monetizacion/plan-monetizacion-thundermc.md`: Documento maestro de 12 secciones con análisis profundo, conectado al ecosistema real del servidor (LuckPerms, PlayerPoints, ExcellentCrates, MythicMobs, Tebex API).
  2. `wiki/concepts/monetizacion-modelo-negocio.md`: Entrada de wiki concisa para consulta rápida.
- **4 Pilares del Modelo**:
  1. **3 Rangos VIP Permanentes** (Trueno 4,99€ / Tormenta 14,99€ señuelo / Relámpago 29,99€): escalonados, acumulativos, precios no lineales. LuckPerms Track configurado.
  2. **Zafiros (PlayerPoints)**: 6 paquetes (2,99€-79,99€), +50% primera compra, currency overhang deliberado.
  3. **Pase de Batalla** (5 semanas, 7,99€ premium, F2P obligatorio, 50 niveles, ~2.500 Zafiros totales).
  4. **Packs de Ofertas** (Starter 6,99€ / Bundle Temporada 11,99€ / Pack Invasión 9,99€ / Pack Ascenso 19,99€).
- **Riesgos Fatales Documentados**: Pay-to-Win en PvP, inflación por kits, currency overhang excesivo, compliance legal UE (probabilidades de cajas, menores, T&C).
- **Metricas Clave**: % F2P→Payer, ARPPU, Retención D7, LTV objetivo >15€/jugador pagador año 1.
- **Proximos Pasos**: Definir permisos exactos por rango → Configurar LuckPerms → Crear productos en Tebex → Activar PlayerPoints como Zafiros → Decidir plugin Pase de Batalla.

---

## [2026-08-27] checkpoint | Punto de Guardado 5: Rediseño Maestro de Menús DeluxeMenus & Arquitectura de Servidores
- **Módulo**: `creator/output/menusIA/`, `wiki/entities/thundermc/`
- **Servidores Sincronizados**: Servidor de Pruebas (`ymykh9qy.274758bd`)
- **Archivos Clave en Producción/Pruebas**:
  1. `warps.yml`: Menú Principal de Ubicaciones con estructura compacta, Warden Egg para Mazmorras, Honey Bottle para La Taberna, Campfire para PWarps, y NavBar limpia.
  2. `warps_minas.yml`: Submenú del Sector Minero con los 6 corales oficiales de `/ranks`, porcentajes reales extraídos de `CataMines`, bolsa de dinero Tier 1 fija y disposición de drops vertical.
  3. `warps_rtp.yml`: Selector de Mundos (Survival 20kx20k, Nether 10kx10k, End 10kx10k con reset programado), mecánicas de protección y protips compactos.
  4. `warps_dungeons.yml`: Matriz de 10 Mazmorras con mobs y jefes reales de MythicMobs, indicadores de dificultad en columna 0, enlaces en amarillo subrayado y botón condicional de Tienda VIP.
- **Documentación y Wiki Actualizada**:
  1. `wiki/entities/thundermc/composicion-minas.md`: Ficha técnica de densidades y tablas de loot de CataMines.
  2. `wiki/entities/thundermc/iconos-compatibles-ui.md`: Catálogo maestro de símbolos e iconos Unicode seguros para Java/Bedrock.
  3. `wiki/entities/thundermc/mobs-mazmorras.md`: Catálogo de bosses de MythicMobs.
  4. `CLAUDE.md` / `AGENTS.md`: Blindaje de seguridad remota (Survival = Solo Lectura; Pruebas = Sandbox libre).

---

## [2026-08-25] checkpoint | Punto de Guardado 4: Tienda Tebex Producción (Catálogo Dinámico, Carrito Asíncrono, Drawer Interactiva y Checkout)
- **Módulo**: `creator/lab/tienda-tebex/`
- **Ubicación de Copia de Seguridad**: `creator/lab/tienda-tebex/backups/punto_guardado_4/`
- **Archivos Clave en Producción**: `Instalacion Tebex/` (`index.html`, `category.html`, `package.html`, `checkout.html`, `layout.html`, `Assets/layout.basket.twig`, `Assets/function.productModal.js`, `Assets/layout.header.twig`)
- **Avances y Características Consolidadas**:
  1. **Catálogo Dinámico & Scraping Compatible**: Eliminado el error de `categoryImageItem` / plural y estructurado el DOM de `category.html` para parseo directo desde `index.html`.
  2. **Modal de Detalle del Paquete (`package.html`)**:
     - Botón superior *"Comprar Ya"* plano y directo a checkout.
     - Botón inferior *"Añadir al Carrito"* en tono gris tenue con procesamiento AJAX en segundo plano.
     - Desplegable de regalo reubicado debajo de ambos botones.
     - Solucionado el scroll interno (`overflow-y: auto`), eliminación de outline blanco y cierre inmediato con botón X.
  3. **Toast Popup de Confirmación**: Notificación flotante al agregar productos con miniatura, nombre y precio.
  4. **Barra Lateral del Carrito (`layout.basket.twig`)**:
     - Despliegue automático al añadir productos desde el modal o mediante el botón flotante rápido de las tarjetas.
     - Miniatura real del producto (`package.image.url`) en el drawer.
     - Controles de cantidad interactivos (`+` y `−`) con límite de 99 unidades.
     - Stackeo automático de paquetes iguales en lugar de duplicar tarjetas.
     - Recálculo en tiempo real del *Total a Pagar* y actualización del contador en el navbar (incluso al reducir a 0 items).
     - Botón *"Ir a Pagar"* con diseño limpio y márgenes simétricos.

---

## [2026-08-25] checkpoint | Punto de Guardado 3: Tienda Tebex Conectada & Smart Features
- **Módulo**: `creator/lab/tienda-tebex/`
- **Ubicación de Copia de Seguridad**: `creator/lab/tienda-tebex/backups/punto_guardado_3/`
- **Nuevo Entorno Producción en Vivo**: `tienda-tiempo-real/`
- **Avances Consolidados**:
  1. **Header Smart Sticky & Autohide**: Ocultamiento en scroll down y descenso suave en scroll up con compensador `.tz-header-spacer`.
  2. **Menú Desplegable Hover en 'Ver Catalogo'**: Despliegue flotante con iconos oficiales de las 7 categorías y scroll suave con compensación de altura.
  3. **Tarjetas 100% Clickables**: Superficie total interactiva con apertura directa de modales y hover dorado.
  4. **Carrusel de Compras Limpio**: Supresión de cajas y recuadros para flujo visual integrado de compradores.
  5. **Páginas Secundarias (`cmspage.html`)**: Vistas `/about` y `/help` con acordeones FAQ, copiado de IP y enlace a Discord.
  6. **Conexión Exitosa con Tebex Headless API**: Sincronización oficial con cuenta `1171683` (ThunderMC).

---

## [2026-08-24] checkpoint | Punto de Guardado 2: Tienda Tebex ThunderMC (Modal Detalle, Checkout Split 2-Col, Login 3D y Navbar)
- **Módulo**: `creator/lab/tienda-tebex/`
- **Ubicación de Copia de Seguridad**: `creator/lab/tienda-tebex/backups/punto_guardado_2/`
- **Avances y Características Clave Consolidadas**:
  1. **Modal de Detalle del Producto (`package.html`)**:
     - Estructura split en 2 columnas: perks RPG con checks verdes a la izquierda, busto 3D del destinatario, switch para regalar a amigos (`Gifting`), botón amarillo sólido `#facc15` sin brillo y sellos de seguridad a la derecha.
  2. **Página de Checkout / Cesta de Compra (`/checkout/basket`)**:
     - Diseño a 2 columnas con selector interactivo de cantidad (`+`/`-`), botón de eliminar artículo, bloque de términos con validación de checkboxes, tarjeta de jugador con busto 3D (`minotar.net/bust/`), cajetín de cupones y botón de pago SSL de 256 bits.
  3. **Tarjetas del Catálogo Pulidas (`index.html`)**:
     - Fondo unificado `#0d121f`, bordes redondeados `18px`, badges de descuento `-35% OFF`, precios en `Plus Jakarta Sans` y botón directo *"Agregar al Carrito"*.
  4. **Hero Slider & Viewport**:
     - Temporizador exacto a `6000ms` (6 segundos) sin retrasos acumulados.
     - Fondo de imágenes extendido continuamente a lo ancho hacia la izquierda con `linear-gradient(90deg, ...)` sin recortes.
  5. **Sistema de Inicio de Sesión & Carrito Unificado**:
     - Widget en el navbar con busto 3D interactivo (`Steve` para invitados, busto personalizado para usuarios logueados).
     - Modal de login con render 3D en vivo al tipear el nickname, pestañas estilizadas Java Edition / Bedrock (añade prefijo `.` automático), cierre con `✕`/`Escape`/overlay y soporte para añadir al carrito como invitado y solicitar login antes de pagar.
     - Discord posicionado junto al widget en la derecha y enlaces de navegación centrados.

---

## [2026-08-24] checkpoint | Punto de Guardado 1: Tienda Tebex ThunderMC
- **Módulo**: `creator/lab/tienda-tebex/`
- **Ubicación de Copia de Seguridad**: `creator/lab/tienda-tebex/backups/punto_guardado_1/`
- **Estado y Características Clave Guardadas**:
  1. **Hero Slider & Viewport**:
     - Pantalla inicial exclusiva (`Hero Slider 500px` con fondos de alta visibilidad + `Compras Recientes` dinámicas con bustos 48px).
     - Botones CTA con animación de reflejo reluciente (`@keyframes tzButtonShine`).
     - Transición lateral suave en slider y vertical descendente en Announcement Bar.
  2. **Catálogo & Envolvente Unificado**:
     - Recuadro contenedor oscuro prémium con bordes redondeados (`24px`), borde fino (`rgba(255,255,255,0.07)`) y padding amplio (`36px 40px`).
     - Barra de navegación unificada: Título "Catálogo" en blanco con icono de cuadrícula (`mdi-view-grid-outline`), acompañado de accesos directos a las 7 categorías.
     - Iconos oficiales webp asignados a cada categoría (`cat_rangos.webp`, `cat_club_vip.webp`, `cat_icon_bag.png`, `cat_llaves.webp`, `cat_packs.webp`, `cat_otros.webp`).
  3. **Banners Promocionales Horizontales**:
     - 2 banners destacados en grid debajo de la botonera del catálogo: **Temporada Invasión** (evento mazmorras/fuego) y **Packs** (ahorro y bundles dorados).
  4. **Pasarelas de Pago Oficiales en Footer**:
     - Logos vectoriales limpios (Visa, Mastercard, PayPal, Apple Pay, Google Pay, Paysafecard) con texto sutil *"y muchos más métodos disponibles"*.

---

## [2026-08-24] fix | Solución Permanente de Recarga en Vivo y Scroll de Tienda Tebex
- **Módulo**: `creator/lab/tienda-tebex/`
- **Diagnóstico del Fallo**:
  1. El servidor Express entregaba respuestas con caché HTTP implícito y Nunjucks no tenía activado `watch: true` ni `noCache: true` en el loader de archivos.
  2. Había bloques CSS duplicados en `index.html` que interferían con el cálculo del scroll del navegador, provocando que la página se quedara bloqueada en la vista.
- **Solución Implementada**:
  1. `server.js`: Añadido middleware global con cabeceras obligatorias `Cache-Control: no-store, no-cache, must-revalidate`, `Pragma: no-cache` y `Expires: 0`.
  2. `server.js`: Configurado Nunjucks con `{ noCache: true, watch: true }` en el `FileSystemLoader`.
  3. `index.html`: Eliminado el CSS corrupto, activado `scroll-behavior: smooth` nativo con `scroll-margin-top: 100px` y barra de categorías 100% centrada, sin recuadros ni cajas pesadas, con icono `cat_icon_bag.png` integrado.
- **Resultado**: Los cambios en plantillas y estilos se reflejan instantáneamente al refrescar el navegador sin necesidad de reiniciar el servidor ni limpiar caché manual.

---

## [2026-08-23] feature | Desarrollo, Pulido y Arte de Tienda Tebex ThunderMC
- **Módulo**: `creator/lab/tienda-tebex/`
- **Trabajo Realizado**:
  - **Header & Navbar**: Barra superior con widget minimalista de IP (`thundermc.es`), widget de carrito limpio sin recuadros pesados, Announcement Bar interactivo con transición entre oferta y temporizador regresivo (`02d 14h 28m 45s`).
  - **Hero Landing Principal**: Emblema frontal centralizado (estilo ref1.PNG) con animación de flotación y flechas sutiles de scroll descendente.
  - **Social Proof / Ticker de Pagos (Estilo PhoenixPlugins)**: Integración de pasarela deslizante continua con métodos reales de Tebex (`Visa`, `Mastercard`, `PayPal`, `Apple Pay`, `Google Pay`, `Paysafecard`, `Klarna`, etc.) e información persuasiva de seguridad (+100M€ procesados, activación <60s).
  - **Sidebar de Categorías**: Cabecera con textura de spawn difuminada, iconos de categorías ampliados a 58px y selector dinámico por pestaña que muestra únicamente la categoría activa.
  - **Catálogo & Botones**: Rediseño táctil de botones de compra con gradiente dorado, relieve de 2.5px y microinteracción de clic.
  - **Footer & Cumplimiento Tebex**: Reincorporación de la barra oficial obligatoria de Tebex Checkout (`we-accept` y powered by Tebex) junto con botón destacado de Discord (+10k miembros).
  - **Generación de Arte**: Iteraciones de diseño de emblemas y logos con Rey Esqueleto, Zombie, Creeper y cofre frontal.

---

## [2026-08-23] feature | Instalación de Skills Web y UI/UX (`web/`)
- **Fuentes**: `taste-skill.zip` y `emil-design-eng.zip` extraídos desde `C:\Users\tecno\Desktop\TrabajoSucio\`.
- **Destino**: `skills/web/` y replicado a `.agents/skills/web/`.
- **Skills Instaladas**:
  - `skills/web/emil-design-eng/`: Filosofía de ingeniería de diseño, microinteracciones, timing de animaciones y pulido de interfaces (Emil Kowalski).
  - `skills/web/taste-skill/`: Framework *anti-slop* para landing pages, portafolios y rediseños web con criterio de diseño real.
- **Catálogo Actualizado**: Añadida la categoría *Desarrollo Web, UI/UX & Frontend* a `skills/README.md`.

---

## [2026-08-23] feature | Módulo Creator e Infraestructura de Creación/I+D
- **Objetivo**: Crear un entorno aislado de experimentación y diseño técnico (`creator/`) que use la memoria existente sin modificarla.
- **Estructura Creada**:
  - `creator/README.md`: Manifiesto y reglas de aislamiento estricto.
  - `creator/raw/`: Subdirectorios `prompts/` y `references/` para ingesta de ideas/ejemplos.
  - `creator/lab/`: Subdirectorios `items/`, `mechanics/` y `storylines/` para borradores e iteraciones.
  - `creator/output/`: Subdirectorios `items/`, `configs/` y `blueprints/` para resultados finales de producción.
- **Archivos de Control Actualizados**: `CLAUDE.md`, `AGENTS.md`, `index.md`, `log.md`.
- **Regla Operativa**: Lectura libre de `wiki/` y `raw/`, pero cero escrituras en memoria salvo instrucción explícita del Sr Ramos.

---

## [2026-08-23] config | Protocolo de Hanush y Enfoque en Network Minecraft 1.21.11
- **Actualización**: Establecido el marco de identidad y reglas operativas directas en `CLAUDE.md` y `AGENTS.md`.
- **Identidad**: Hanush.
- **Usuario**: Sr Ramos.
- **Foco Primario**: Network de Minecraft 1.21.11 (economía, plugins, rendimiento, Catamines, dungeons, balance RPG) y THUNDERVERSE.
- **Reglas Fijas**: Cero validación inicial, red teaming forzado, tono clínico/técnico, honestidad radical ("sé vs. asumo") y comunicación en español.

---

## [2026-08-23] ingest | Ecosistema ThunderIA Completo y Sistema de Skills
- **Fuentes**: `C:\Users\tecno\Desktop\ThunderIA` (Technical, Core, Ramos, AGENTS.md, README.md, _setup, skills).
- **Capa Raw Creada**:
  - `raw/thunderia/narrative_and_agents/`
  - `raw/thunderia/ramos/`
  - `raw/thunderia/core_economy/`
  - `raw/thunderia/technical/`
- **Sistema de Skills Implementado**:
  - Carpeta raíz `skills/` y `.agents/skills/` con catálogo maestro `skills/README.md`.
  - 18 skills cognitivas y de productividad (Hanush/Ramos).
  - 17 skills de producción narrativa y departamentos (ThunderStudios en `skills/studio/`).
- **Páginas Wiki Creadas**:
  - **Fuentes**: `[[wiki/sources/thunderia-overview|Resumen Maestro ThunderIA]]`, `[[wiki/sources/thundermc-economia-minas-dungeons|Economía Minas y Dungeons]]`, `[[wiki/sources/hanush-marco-cognitivo-jordan|Marco Cognitivo y Perfil de Jordan]]`
  - **Entidades**: `[[wiki/entities/thunderstudios|ThunderStudios]]`, `[[wiki/entities/thundermc|ThunderMC]]`, `[[wiki/entities/jordan|Jordan]]`, `[[wiki/entities/hanush|Hanush]]`, `[[wiki/entities/catamines|Catamines]]`
  - **Conceptos**: `[[wiki/concepts/thunderverse-canon-levels|Niveles de Canon THUNDERVERSE]]`, `[[wiki/concepts/economia-servidor-minecraft|Economía Servidor Minecraft]]`, `[[wiki/concepts/calidades-y-lore-items|Calidades y Lore de Ítems]]`, `[[wiki/concepts/dungeons-y-jefes|Dungeons y Jefes]]`, `[[wiki/concepts/framework-cognitivo-operativo|Framework Cognitivo Operativo]]`
  - **Síntesis**: `[[wiki/synthesis/thundermc-master-synthesis|Síntesis Maestra ThunderMC]]`, `[[wiki/synthesis/sistema-habilidades-y-skills|Sistema de Habilidades y Skills]]`
  - **Comparaciones**: `[[wiki/comparisons/minas-vs-dungeons-balance|Balance Minas vs. Dungeons]]`
- **Archivos de Control Actualizados**: `CLAUDE.md`, `index.md`, `log.md`.
- **Resultado**: Segundo cerebro completamente estructurado, interconectado y listo para operaciones en español.

---

- **Key Takeaway**: Inicialización de la base ThunderCerebro.

---

## [2026-08-27] audit & ingest | Auditoría Completa de Plugins ThunderMC (1.21.11)
- **Origen**: Servidor Survival `MIA-251006.bloom.host:2022` vía SFTP + Wikis oficiales proporcionadas por el Sr Ramos.
- **Entidades y Wikis Creadas (41 archivos)**:
  - **Directorio Raíz**: `[[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins ThunderMC]]`, `[[wiki/entities/thundermc/enlaces-wikis-oficiales|Directorio de Wikis Oficiales]]`, `[[wiki/entities/thundermc/analisis_plugins_survival_thundermc|Informe Técnico de Auditoría]]`.
  - **Infraestructura Core (12 guías)**: `VaultUnlocked`, `Multiverse-Core`, `VoiceChat`, `FancyHolograms`, `FancyNpcs`, `LuckPerms`, `PlaceholderAPI`, `FAWE`, `ViaVersion`, `Floodgate`, `TAB`, `Plan`.
  - **Economía y Progresión (7 guías)**: `QuickShop-Hikari`, `ShopGUIPlus/SellGUI`, `ZelAuction`, `ExcellentCrates`, `PlayerPoints`, `Jobs-Reborn`, `Minigames/AFK/Gambling`.
  - **Jugabilidad y RPG (8 guías)**: `ExecutableItems`, `ItemEdit`, `ExcellentEnchants`, `CataMines`, `BetterRTP`, `UltimateKoth`, `MythicMobs`, `GSit`.
  - **Protección y Seguridad (6 guías)**: `ProtectionStones`, `LiteBans`, `InventoryRollbackPlus`, `WorldGuard`, `CoreProtect`, `PvPManager`.
  - **Chat y Social (4 guías)**: `ZelChat`, `ZelTeams`, `PlayerWarps`, `AlonsoTags`.
  - **Plugins Custom (1 guía)**: `EnderChestPlus`, `RankUp`, `ValyrTutorial`, `ThunderMines`.
- **Actualizados**: `index.md`, `log.md`.
- **Métricas Clave**: 74 JARs activos analizados, 16 `.dis` auditados, 41 documentos técnicos compilados con diagramas Mermaid, sintaxis de comandos, permisos, variables PAPI, optimizaciones Paper 1.21.11 y mitigación de vulnerabilidades/exploits.

