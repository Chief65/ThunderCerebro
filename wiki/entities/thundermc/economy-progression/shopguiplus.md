# 📖 ShopGUIPlus & SellGUI

- **Categoría**: Tienda Administrativa Global & Menús GUI de Venta
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Documentación Oficial**: [BRCDev ShopGUIPlus Wiki](https://docs.brcdev.net/#/shopgui/shops-items-setup)
- **Dependencias Clave**: Vault, PlaceholderAPI, SilkSpawners / WildStacker / MMOItems / ItemsAdder (hooks opcionales).

---

## 🎯 Propósito & Funcionalidad
**ShopGUI+** es el estándar de la industria para tiendas GUI del servidor (economía centralizada), permitiendo a los usuarios comprar y vender recursos directamente a través de menús dinámicos con paginación, precios dinámicos, soporte multi-economía (Vault, PlayerPoints, tokens) y control de permisos por secciones.

**SellGUI** (módulo/addon integrado o complementario) facilita la venta masiva de inventarios completos mediante cofres GUI virtuales donde los jugadores depositan sus recursos y reciben el importe total liquidado al instante según las tablas de precios de ShopGUI+.

---

## 🏗️ Arquitectura & Funcionamiento Interno
1. **Estructura Modular por Secciones (`shops/*.yml`)**:
   - Cada categoría de la tienda se define en un archivo YAML individual (`blocks.yml`, `farming.yml`, `ores.yml`, `spawners.yml`). La clave raíz dentro del archivo debe coincidir exactamente con el nombre del archivo.
2. **Multi-Currency Engine**:
   - Soporta definir proveedores económicos diferentes por ítem o por sección (`VAULT`, `EXP`, `PLAYER_POINTS`, etc.).
3. **Dynamic Pricing & Price Modifiers**:
   - Permite aplicar modificadores globales, por permiso o basados en oferta/demanda que alteran los precios de compra y venta dinámicamente según volumen de transacciones.

---

## ⚙️ Configuración & Estructura de Tiendas

### Estructura de Tienda por Categoría (`plugins/ShopGUIPlus/shops/farming.yml`)
```yaml
farming:
  name: "&8&lCultivos & Agricultura (Pág. %page%)"
  size: 45
  fillItem:
    material: GRAY_STAINED_GLASS_PANE
    name: " "
  buttons:
    goBack:
      slot: 36
    previousPage:
      slot: 39
    nextPage:
      slot: 41
  items:
    1:
      type: item
      item:
        material: WHEAT
        quantity: 1
      buyPrice: 12.0
      sellPrice: 3.5
      slot: 10
    2:
      type: item
      item:
        material: SUGAR_CANE
        quantity: 1
      buyPrice: 15.0
      sellPrice: 4.0
      slot: 11
    3:
      type: item
      item:
        material: NETHER_WART
        quantity: 1
      buyPrice: 50.0
      sellPrice: 14.0
      slot: 12
      permission: "shopguiplus.shops.farming.netherwart" # Requisito de desbloqueo
```

### Configuración de SellGUI e Integración (`config.yml`)
```yaml
# Control Económico y Prevención de Exploits
economyType: "VAULT"
sellAllSound: "ENTITY_PLAYER_LEVELUP"

# Optimización de Cálculos
enableSellGUI: true
sellGuiRows: 6
dropUnsoldItems: true # Devolver al inventario ítems no vendibles o sin precio configurado

# Modificadores de Precios por Rangos (Boosters)
priceModifiers:
  - permission: "shopguiplus.booster.vip"
    buyMultiplier: 0.95 # 5% de descuento al comprar
    sellMultiplier: 1.10 # 10% de ganancia extra al vender
  - permission: "shopguiplus.booster.thunder"
    buyMultiplier: 0.85
    sellMultiplier: 1.25
```

---

## 💻 Comandos & Permisos

### Comandos Principales
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/shop` | Abre el menú principal de categorías de la tienda. | `shopguiplus.shop` |
| `/shop <sección>` | Abre directamente una categoría específica (ej. `/shop farming`). | `shopguiplus.shop.<sección>` |
| `/sellgui` o `/sell` | Abre la GUI de venta masiva de ítems. | `shopguiplus.sellgui` |
| `/sellall [mano/inventario]` | Vende rápidamente los ítems comerciables del inventario. | `shopguiplus.sellall` |
| `/shop check` | Analiza el ítem en mano y muestra sus datos y precios configurados. | `shopguiplus.check` |
| `/editshop addhanditem <sección> <buy> <sell>` | Agrega automáticamente el ítem de la mano al archivo de tienda. | `shopguiplus.editshop` |
| `/shop reload` | Recarga todas las configuraciones, tiendas e integraciones NBT. | `shopguiplus.reload` |

---

## 🧩 Placeholders PlaceholderAPI (PAPI)
* `%shopguiplus_total_earned%`: Total de ingresos generados por el jugador en la tienda.
* `%shopguiplus_total_spent%`: Total de dinero gastado por el jugador.
* `%shopguiplus_sell_modifier%`: Multiplicador actual de venta del jugador (ej. `1.15`).
* `%shopguiplus_buy_modifier%`: Multiplicador actual de compra del jugador (ej. `0.90`).

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Exploit de Ciclos Infinitos de Dinero (Buy Low / Sell High)**:
   - **Vulnerabilidad**: Configurar por error un `sellPrice` superior al `buyPrice` o permitir que multiplicadores de rango eleven el precio de venta por encima del coste de compra.
   - **Solución**: Auditar las tablas de precios asegurando siempre que `sellPrice <= buyPrice * 0.40`. Validar que el multiplicador máximo de venta (ej. `1.25x`) nunca supere el precio base de compra.
2. **Dupe por Cierre Forzado en `/sellgui`**:
   - **Vulnerabilidad**: Dropear ítems o desconectarse mientras el servidor calcula la venta masiva.
   - **Solución**: ShopGUI+ bloquea la interacción del jugador durante el tick de procesamiento y devuelve de forma segura al inventario o al suelo (`dropUnsoldItems: true`) cualquier objeto con componentes no registrados.
3. **Exploit de Ítems Dañados / Sin Durabilidad**:
   - Configurar `damageMatch: true` o habilitar cálculo proporcional de durabilidad en herramientas/armaduras para evitar que jugadores reparen ítems gastados vendiéndolos al 100% de valor.
4. **Desync con Ítems NBT / MMOItems / Slimefun**:
   - Utilizar el validador de NBT estricto en lugar de sólo `material`, evitando que variantes básicas se vendan como ítems legendarios o viceversa.

---

## ⚡ Optimización & Mejores Prácticas
- **Separación de Archivos**: Mantener las categorías divididas en archivos YAML pequeños de no más de 100 ítems para reducir el tiempo de parseo en memoria durante `/shop reload`.
- **Caché de Materiales**: ShopGUI+ cachea las estructuras de inventario pre-renderizadas; evitar activar debuggers innecesarios en producción para no saturar los logs de consola.
