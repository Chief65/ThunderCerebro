# 📖 FancyAnimations (v1.0.0)

- **Categoría**: NPC Kinematics & Procedural Animation Engine
- **Servidor**: ThunderMC Network (Paper 1.21.11 / Geyser)
- **Desarrollador**: ThunderStudios (Desarrollo Propio Open-Source)
- **Dependencias**: FancyNpcs 2.9+, Java 21, PacketEvents 2.13+
- **Ubicación en Servidor**: `plugins/FancyAnimations-1.0.0.jar`
- **Código Fuente**: `creator/lab/FancyAnimations/`

---

## 🎯 1. Propósito & Visión General
**FancyAnimations** es un addon oficial desarrollado a medida para dotar a los NPCs de FancyNpcs de comportamiento orgánico, sensación de vida ("gestos de ambiente"), feedback interactivo (cursor glow verde per-player, display names bicapa reactivos, action bar continuo) y paisajes sonoros sin requerir mods de cliente, modelos pesados de Blockbench ni resource packs.

Es **100% visible tanto en clientes Java como en Bedrock (Geyser)** mediante el uso de cinemática procedural vanilla e interpolación nativa de entidades Display.

---

## 🏗️ 2. Módulos Cinemáticos & Interactivos

1. **Breathing (Respiración)**: Oscilación vertical senoidal suave en el eje Y ($Y + \sin(t \cdot 0.08) \cdot 0.05$).
2. **Swaying (Balanceo de Torso / Hombros)**: Oscilación angular continua en Yaw ($\text{Yaw} + \sin(t \cdot 0.04) \cdot 3.5^\circ$).
3. **Head Tilt (Ladeo de Cabeza)**: Modulación angular armónica en Pitch ($\text{Pitch} + \cos(t \cdot 0.05 + \phi) \cdot 5.0^\circ$).
4. **Nodding (Asentimiento / Cabeceo)**: Disparos periódicos suaves con curva senoidal de media onda de 20 ticks ($12.0^\circ$).
5. **Micro-Rotation (Mirada Viva)**: Desplazamientos aleatorios de la orientación ($-20^\circ$ a $+20^\circ$) con interpolación exponencial (Lerp) cada 100-260 ticks cuando no hay jugadores cerca.
6. **Custom Look-At Player (Seguimiento Desacoplado)**: Motor propio de seguimiento angular suave en Yaw y Pitch con interpolación Lerp sin saltos. Desactiva forzosamente el `turnToPlayer` interno de FancyNpcs para erradicar cualquier conflicto de paquetes.
7. **Cursor Hover vía BoundingBox RayTrace**:
   - Hitbox tridimensional precisa ($X \pm 0.55, Y \text{ de } -0.1 \text{ a } +2.65, Z \pm 0.55$) evaluada con `BoundingBox.rayTrace()`. Detecta la mira del jugador sin importar si apunta a los pies, pecho, cabeza o a los textos flotantes superiores.
   - Dispara Glowing verde per-player (`0x40`) en el Scoreboard Team verde asignado en FancyNpcs.
8. **Arquitectura Bicapa de Display Names (Dual Virtual TextDisplays)**:
   - **Capa 1: Título / Nombre ($Y + 2.32$)**:
     - Background: `0x40000000` (**recubierto con la caja negra translúcida** tanto en reposo como en selección).
     - Escala: `1.40` en reposo (tamaño visiblemente más grande), ampliándose fluidamente a `1.65` al apuntar con la mira (`interpolation-ticks: 3`).
     - Formato Reposo: `&f%name%` (blanco limpio).
     - Formato Selección (Hover): `&a&l%name%` (verde negrita limpio, sin flechas).
   - **Capa 2: Subtítulo ($Y + 2.02$)**:
     - Background: `0` (**100% transparente en ambas situaciones**, sin caja negra).
     - Escala: `1.0` constante (tamaño estándar en reposo y en selección).
     - Texto: `&7ᴄʟɪᴄᴋ ᴘᴀʀᴀ ᴠᴇʀ` (fijo tanto en reposo como en selección).
   - Ambas capas se sincronizan milimétricamente con el desplazamiento vertical ($dy$) de la respiración senoidal mediante `teleport_duration: 1`.
   - **Sincronización Estricta de Visibilidad**: Ambas capas virtuales se vinculan directamente al estado de renderizado nativo de FancyNpcs (`npc.isShownFor(player)`) y a la distancia de visibilidad (`visibility_distance: 20` de FancyNpcs). En cuanto el jugador sale del rango o el NPC se oculta/despawnea, el motor emite paquetes `destroyTextDisplay` destruyendo inmediatamente ambos hologramas sin dejar texto fantasma en el aire.
9. **Sincronización en Tiempo Real de Comandos FancyNpcs**:
   - Escucha reactiva en `NpcModifyEvent` e inspección por tick en `ensureNpcConfigured`.
   - Cualquier cambio realizado vía `/npc displayname <nuevo_nombre>` o `/npc displayname @none` se captura al instante, actualizando los paquetes de las entidades virtuales de todos los clientes en tiempo real.
10. **Hover Action Bar Dinámico con Descripciones de NPCs**:
    - Al apuntar al NPC con la mira, el Action Bar despliega dinámicamente la **descripción personalizada** asignada al NPC.
    - Si el NPC no tiene descripción personalizada, recurre automáticamente a la descripción por defecto: `&fNpc clickeable`.
    - Procesado mediante `LegacyComponentSerializer.legacySection()` y sanitización de MiniMessage para garantizar renderizado cromático nativo exacto.
    - Se refresca continuamente cada 10 ticks (`Bukkit.getCurrentTick()`) mientras se mantiene la mira sobre el NPC y se limpia instantáneamente al apartar el cursor.
    - Gestión en tiempo real con detección contextual por RayTrace: `/npcs desc add [npc] <texto...>`, `/npcs desc remove [npc]`, `/npcs desc list` y `/npcs desc default <texto...>`.
11. **Paisaje Sonoro Inmersivo**:
    - **Sonido Ambiental Periódico**: Disparo aleatorio cada 10-25 segundos de `entity.villager.ambient` a volumen moderado (`0.5`) con modulación aleatoria de tono ($0.9 - 1.15$).
    - **Sonido de Clic**: Al interactuar (`NpcInteractEvent`), reproduce instantáneamente el sonido de confirmación `entity.villager.yes` en el canal de voces.
12. **Módulo de Adaptación y Paridad para Bedrock (Floodgate Integration)**:
    - **Detección Dinámica**: Mediante `FloodgateApi.getInstance().isFloodgatePlayer()` y fallback por prefijo `.`, el motor detecta la plataforma en cada paquete de red.
    - **Preservación Estética de Formato**:
      - En reposo: Mantiene el formato blanco limpio `&f%name%` y subtítulo `&7ᴄʟɪᴄᴋ ᴘᴀʀᴀ ᴠᴇʀ`.
      - En selección (Hover): Sustituye la falta de escala 3D de Bedrock aplicando el formato destacado `&a▶ &a&l%name% &a◀` (`bedrock-title-hover-format`), permitiendo al jugador de consola/móvil distinguir inmediatamente la selección sin romper la estética.
    - **Aura de Partículas de Selección**: Al no existir el shader de Glowing en Bedrock, emite pulsos de micro-partículas verdes (`HAPPY_VILLAGER`) orbitando el torso del NPC únicamente visibles para el jugador de Bedrock que apunta.
    - **Micro-feedback Háptico/Auditivo**: Dispara un clic sutil (`UI_BUTTON_CLICK` a volumen 0.25 y tono alto) al colocar la mira sobre el NPC.

---

## ⚙️ 3. Configuración (`config.yml`)

```yaml
display-names:
  enabled: true
  title-normal-format: "&f%name%"
  title-hover-format: "&a&l%name%"
  bedrock-title-hover-format: "&a▶ &a&l%name% &a◀"
  title-height-offset: 2.32
  title-normal-scale: 1.40
  title-hover-scale: 1.65
  title-interpolation-ticks: 3
  subtitle-format: "&7ᴄʟɪᴄᴋ ᴘᴀʀᴀ ᴠᴇʀ"
  subtitle-height-offset: 2.02
  subtitle-scale: 1.0

  bedrock-adaptation:
    enabled: true
    particles: false
    hover-sound: true

hover-action-bar:
  enabled: true
  default-description: "&fNpc clickeable"
  text: "&fNpc clickeable"

sounds:
  ambient:
    enabled: true
    sound: "ENTITY_VILLAGER_AMBIENT"
    volume: 0.5
    min-interval-ticks: 200
    max-interval-ticks: 500
  click:
    enabled: true
    sound: "ENTITY_VILLAGER_YES"
    volume: 1.0
    pitch: 1.0

npcs:
  pruebas:
    description: "&fGana dinero con oficios"
```

---

## ⌨️ 4. Comandos & Permisos

| Comando | Alias | Descripción |
|---|---|---|
| `/npcs desc add [npc] <texto...>` | `/npc desc add`, `/fanim desc add` | Asigna descripción al Action Bar (detecta automáticamente el NPC al que miras o por nombre) |
| `/npcs desc remove [npc]` | `/npc desc remove`, `/fanim desc remove` | Elimina la descripción personalizada (vuelve al valor por defecto) |
| `/npcs desc list` | `/fanim desc list` | Lista los NPCs con descripción personalizada asignada y el texto por defecto |
| `/npcs desc info [npc]` | `/fanim desc info` | Muestra la descripción actual del NPC objetivo |
| `/npcs desc default <texto...>` | `/fanim desc default` | Cambia el texto de descripción por defecto (`Npc clickeable`) |
| `/fanim ambient <npc> <on\|off>` | `/ambient` | Activa o desactiva el conjunto ambiental completo en un NPC |
| `/fanim animate <npc> <tipo> <on\|off>` | - | Control individual (`breathing`, `swaying`, `headtilt`, `nodding`, `microrotation`, `lookat`, `cursorglow`, `randomgestures`) |
| `/fanim play <npc> <wave\|nod\|offhand>` | - | Fuerza un gesto puntual inmediato |
| `/fanim preset <npc> <ambient\|none>` | - | Aplica plantilla rápida |
| `/fanim default <ambient\|none>` | - | Cambia la política por defecto para NPCs nuevos |
| `/fanim list` | - | Muestra todos los NPCs y su estado cinemático |
| `/fanim info <npc>` | - | Detalle de las animaciones activas en un NPC |
| `/fanim reload` | - | Recarga `config.yml` |

- **Permiso**: `fancyanimations.admin` (por defecto `op`).
