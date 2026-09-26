# Desglose de Fuente: Documentación Oficial de ShopGUIPlus

**Fuente**: `https://docs.brcdev.net/#/shopgui/shops-items-setup` (brcdev documentation)  
**Tipo**: Documentación Técnica / Especificación de Plugin Spigot  
**Materia**: Configuración de tiendas, metadatos de ítems, sistemas de precios y hooks de comandos.

---

## 1. Arquitectura y Estructura de Tiendas (`shops/*.yml`)

Cada tienda se almacena en un archivo `.yml` dentro de `/plugins/ShopGUIPlus/shops/`.

### 1.1 Encabezado y Propiedades Principales
```yaml
<shop_id>:
  name: "&0&l|&r &0Tienda ▶ &8Nombre"   # Título del inventario (soporta %page%)
  size: 45                               # 9, 18, 27, 36, 45, 54
  fillItem:                              # Relleno de slots vacíos
    material: AIR
    name: " "
  economy: VAULT                         # Opcional: VAULT, EXP_LEVELS, CUSTOM
  buttons:                               # Posicionamiento de botones de navegación nativos
    goBack:
      slot: 40
    previousPage:
      slot: 39
    nextPage:
      slot: 41
  items:
    # Definición de productos
```

---

## 2. Tipos de Ítems Soportados (`type:`)

ShopGUIPlus soporta 5 tipos de elementos en la sección `items`:

| Tipo | Descripción | Campos Clave |
|---|---|---|
| `item` | Producto físico estándar de Minecraft | `item:`, `buyPrice:`, `sellPrice:`, `slot:` |
| `command` | Ejecuta comandos de servidor al comprar | `item:`, `commands:`, `buyPrice:`, `slot:` |
| `enchantment` | Aplica un encantamiento al ítem que sostiene el jugador | `item:`, `enchantment:`, `level:`, `buyPrice:` |
| `permission` | Otorga un permiso (LuckPerms/Vault) | `item:`, `permission:`, `buyPrice:` |
| `dummy` | Elemento visual o botón de navegación | `item:`, `commandsOnClick:`, `slot:` |

---

## 3. Jerarquía y Sintaxis Estricta de Propiedades de Ítem

> [!WARNING]
> Las propiedades `buyPrice`, `sellPrice`, `slot` y `commandsOnClick` deben ubicarse estrictamente al nivel del identificador del ítem (`items.<id>`), **NUNCA** dentro del sub-bloque `item:`.

### Ejemplo Correcto:
```yaml
items:
  1:
    type: item
    item:
      material: DIAMOND
      quantity: 1
      name: "&bDiamante Puro"
      lore:
        - "&7Mineral precioso"
      flags:
        - HIDE_ATTRIBUTES
      unbreakable: false
    buyPrice: 100
    sellPrice: 25
    slot: 9
```

---

## 4. Ítems Dummy y Botones de Interfaz (`type: dummy`)

Los ítems dummy permiten crear botones interactivos dentro de la tienda:
```yaml
items:
  308:
    type: dummy
    item:
      material: COMPARATOR
      quantity: 1
      name: "&eFiltrar Categoria"
      lore:
        - "&8Elige categoria"
    commandsOnClick:
      - "shop farmeo"
    slot: 36
```

---

## 5. Metadatos Avanzados de Ítems (`item-meta`)

- **Colores Hex / RGB**: Soportados nativamente en Spigot 1.16+ mediante sintaxis de color o códigos estándar.
- **Pociones (1.20.2+)**: Se declaran con `potion: type: <TIPO>` (ej. `STRONG_STRENGTH`, `LONG_INVISIBILITY`).
- **Plantillas y Diseños de Armadura (Trims)**: Soportados mediante materiales directos en 1.20+ (`SILENCE_ARMOR_TRIM_SMITHING_TEMPLATE`).
- **Flags de Ítem**: `HIDE_ENCHANTS`, `HIDE_ATTRIBUTES`, `HIDE_UNBREAKABLE`, `HIDE_DESTROYS`, `HIDE_PLACED_ON`, `HIDE_POTION_EFFECTS`.

---

## 6. Formato Global de Precios y Lores (`config.yml -> shopItemLoreFormat`)

- `item`: Lore aplicado en la cuadrícula de catálogo.
- `itemBuyGUI`: Lore aplicado en la ventana modal de selección de cantidad (`amountSelectionGUI`).
- `itemSellGUI`: Lore aplicado en la ventana de venta.
- Placeholders nativos: `%buy%`, `%sell%`, `%amount%`, `%page%`, `%pages%`.
