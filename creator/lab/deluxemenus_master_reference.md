# Manual Técnico Maestro: DeluxeMenus

Guía y especificación exhaustiva de arquitectura, sintaxis, requisitos y patrones de diseño para el plugin **DeluxeMenus** (Spigot/Paper 1.20 - 1.21+).

---

## 1. Arquitectura de Archivos y Registro

### 1.1 config.yml (Gestor Maestro)
Los menús deben modularizarse siempre en archivos externos dentro de gui_menus/:

`yaml
# plugins/DeluxeMenus/config.yml
check_updates: false
gui_menus:
  nombre_menu:
    file: nombre_menu.yml
  menu_con_carpeta:
    file: tiendas/armaduras.yml
`

Comandos de consola / admin:
* /dm reload: Recarga configuraciones y menús.
* /dm open <menu> [jugador]: Abre un menú a un jugador específico.
* /dm list: Lista todos los menús registrados.

---

## 2. Estructura Raíz de un Menú Externo (gui_menus/*.yml)

`yaml
menu_title: '&#55ff99&lTÍTULO DEL MENÚ' # Soporta MiniMessage, Hex y PAPI
open_command:
  - comando_principal
  - alias_comando
register_command: true # Registra el comando nativamente en el servidor (requiere reinicio si usa args)
inventory_type: 'CHEST' # CHEST, HOPPER, DISPENSER, DROPPER, ANVIL, BARREL, etc.
size: 54 # 9, 18, 27, 36, 45, 54 (Solo aplica a tipo CHEST)
update_interval: 1 # Intervalo en segundos para refrescar placeholders (en items con update: true)

# Argumentos en comando (Ej: /menu <objetivo> <tipo>)
args:
  - objetivo
  - tipo
args_usage_message: '&cUso correcto: /menu <jugador> <categoria>'
parse_placeholders_after_arguments: true

# Requisitos para poder abrir el menú completo
open_requirement:
  requirements:
    permiso_staff:
      type: has permission
      permission: network.staff
      deny_commands:
        - '[message] &cNo tienes acceso a este panel.'

# Acciones al abrir / cerrar
open_commands:
  - '[sound] BLOCK_CHEST_OPEN 1.0 1.0'
close_commands:
  - '[sound] BLOCK_CHEST_CLOSE 1.0 1.0'

items:
  # Declaración de ítems...
`

---

## 3. Especificación de Ítems (items:)

### 3.1 Materiales Compatibles
* **Vanilla**: STONE, NETHERITE_SWORD, BARRIER, AIR (para slots invisibles clickeables).
* **Cabezas**:
  * head-%player_name%
  * head-{argumento}
  * asehead-<Base64_String>
  * 	exture-<Texture_ID> (ID tras 	extures.minecraft.net/textures/)
  * hdb-<ID> (HeadDatabase)
* **Custom Models / Plugins**:
  * itemsadder-namespace:item_id
  * oraxen-item_id
  * 
exo-item_id
  * mmoitems-type:id
  * executableitems-item_id
* **Dinámicos**:
  * main_hand, off_hand
  * rmor_helmet, rmor_chestplate, rmor_leggings, rmor_boots
  * placeholder-%placeholder_material%

### 3.2 Opciones de Renderizado de Ítems
`yaml
items:
  item_ejemplo:
    material: DIAMOND_SWORD
    slot: 13 # O slots: [10, 11, 12] o slots: ['0-8', '45-53']
    priority: 1 # Prioridad más alta = 0. Menor número = se evalúa primero
    amount: 1
    dynamic_amount: '%player_level%'
    display_name: '&#00e5ffEspada Astral'
    lore:
      - '&7Nivel: &f%player_level%'
      - '&7Daño: &c+25'
      - ''
      - '&e¡Click izquierdo para comprar!'
    
    # 1.20.5+ / 1.21+ Opciones Modernas
    enchantment_glint_override: true # Brillo de encantamiento sin encantar
    hide_tooltip: false
    rarity: EPIC # COMMON, UNCOMMON, RARE, EPIC
    
    # Custom Model Data moderno (1.21.4+)
    model_data_component:
      strings: [ custom_sword]
      floats: [1.0]
      flags: [true]
    # Model data clásico (<1.21.4)
    # model_data: 10025
    
    # Item Flags
    item_flags:
      - HIDE_ATTRIBUTES
      - HIDE_ENCHANTS
      - HIDE_UNBREAKABLE
      - HIDE_ADDITIONAL_TOOLTIP
      
    # Actualización en vivo
    update: true
`

---

## 4. Tipos de Acciones ([ACTIONTYPE])

| Acción | Sintaxis | Descripción |
| :--- | :--- | :--- |
| [player] | [player] spawn | Ejecuta comando como jugador |
| [console] | [console] give %player_name% diamond 1 | Ejecuta comando desde consola |
| [message] | [message] &a¡Compra completada! | Envía mensaje al jugador (PAPI + Legacy) |
| [minimessage] | [minimessage] <gradient:green:blue>Éxito</gradient> | Envía mensaje MiniMessage Kyori |
| [broadcast] | [broadcast] &e%player_name% subió de rango | Transmite mensaje a todo el servidor |
| [minibroadcast]| [minibroadcast] <rainbow>%player_name% es VIP</rainbow> | Transmite MiniMessage al servidor |
| [openguimenu] | [openguimenu] perfil_usuario {target} | Abre otro menú de DeluxeMenus |
| [close] | [close] | Cierra el inventario actual |
| [refresh] | [refresh] | Refresca los ítems del menú en pantalla |
| [sound] | [sound] ENTITY_PLAYER_LEVELUP 1.0 1.2 | Reproduce sonido al jugador |
| [broadcastsound] | [broadcastsound] UI_TOAST_CHALLENGE_COMPLETE 1 1 | Sonido global |
| [takemoney] | [takemoney] 500 | Descuenta dinero (Requiere Vault) |
| [givemoney] | [givemoney] 100 | Otorga dinero (Requiere Vault) |
| [takeexp] | [takeexp] 5L (o 100 sin L para puntos) | Descuenta niveles o experiencia |
| [giveexp] | [giveexp] 2L | Otorga experiencia o niveles |
| [meta] | [meta] set claim_daily BOOLEAN true | Modifica metadatos PDC del jugador |
| [connect] | [connect] survival | Envía al jugador a otro servidor Bungee/Velocity |

### Tags de Acción:
* <delay=20>: Retraso en ticks (20 ticks = 1s). Ej: -[message] Hola<delay=40>
* <chance=50>: Probabilidad de ejecución (0-100%). Ej: -[givemoney] 1000<chance=25>

---

## 5. Motor de Requisitos (equirements)

### 5.1 Estructura Estándar y Operadores Lógicos

`yaml
click_requirement:
  minimum_requirements: 1 # Opcional: basta con cumplir X requisitos marcados como opcionales
  stop_at_success: true # Detiene la evaluación al cumplir el mínimo
  requirements:
    tiene_dinero:
      type: has money
      amount: 1000
      deny_commands:
        - '[message] &cNo tienes suficiente dinero (,000).'
        - '[sound] ENTITY_VILLAGER_NO 1.0 1.0'
    tiene_nivel:
      type: '>='
      input: '%player_level%'
      output: 10
      deny_commands:
        - '[message] &cDebes ser mínimo nivel 10.'
  deny_commands:
    - '[sound] BLOCK_NOTE_BLOCK_BASS 1.0 0.5'

click_commands:
  - '[takemoney] 1000'
  - '[console] kit premio %player_name%'
  - '[message] &a¡Recompensa reclamada con éxito!'
  - '[refresh]'
`

### 5.2 Catálogo de Tipos de Requisitos
1. **Permisos**:
   * has permission (permission: string)
   * !has permission (Invertido)
   * has permissions (permissions: [...], minimum: #)
2. **Economía & Exp**:
   * has money (mount: # o placeholder: '%coste%')
   * has exp (mount: #, level: true/false)
3. **Inventario & Objetos**:
   * has item (material: STONE, mount: 10, modeldata: 5, 
ame: ..., 
ame_contains: true, strict: true, offhand: true, rmor: true)
4. **Comparadores Matemáticos**:
   * ==, !=, >=, <=, >, < (input: #, output: #)
5. **Cadenas de Texto & Regex**:
   * string equals / string equals ignorecase
   * string contains
   * string length (min: #, max: #)
   * egex matches (egex: '^[0-9]+$')
6. **Objetos y Tipado**:
   * is object (object: INT | DOUBLE | PLAYER | UUID)
7. **Metadatos & Posición**:
   * has meta (key: ..., meta_type: STRING|BOOLEAN|INTEGER|DOUBLE, value: ...)
   * is near (location: world,100,64,200, distance: 15)
8. **Evaluador Lógico Avanzado**:
   * javascript (expression: '%vault_eco_balance% >= 500 && %player_has_permission_vip% == yes')

---

## 6. Patrón Maestro: Ítems Dinámicos por Prioridades

Para mostrar estados (Ej: **Bloqueado** vs **Disponible para comprar** vs **Ya Comprado**):

`yaml
items:
  # Prioridad 0: Ya comprado / Reclamado
  recompensa_comprada:
    material: LIME_STAINED_GLASS_PANE
    slot: 20
    priority: 0
    view_requirement:
      requirements:
        ya_reclamado:
          type: has meta
          key: kit_reclamado
          meta_type: BOOLEAN
          value: true
    display_name: '&a&lRecompensa: Reclamada'
    lore:
      - '&7Ya has recogido esta recompensa.'

  # Prioridad 1: Puede comprarlo
  recompensa_disponible:
    material: CHEST
    slot: 20
    priority: 1
    view_requirement:
      requirements:
        tiene_saldo:
          type: has money
          amount: 500
    display_name: '&e&lRecompensa: Disponible'
    lore:
      - '&7Coste: &a'
      - ''
      - '&a[Click para Comprar]'
    click_commands:
      - '[takemoney] 500'
      - '[meta] set kit_reclamado BOOLEAN true'
      - '[message] &a¡Has comprado el cofre!'
      - '[sound] UI_TOAST_CHALLENGE_COMPLETE 1.0 1.0'
      - '[refresh]'

  # Prioridad 2: Bloqueado (Fallback por defecto)
  recompensa_bloqueada:
    material: GRAY_STAINED_GLASS_PANE
    slot: 20
    priority: 2
    display_name: '&c&lRecompensa: Bloqueada'
    lore:
      - '&7Necesitas  para desbloquear esto.'
    click_commands:
      - '[sound] ENTITY_VILLAGER_NO 1.0 1.0'
      - '[message] &cNo tienes suficiente dinero.'
`
