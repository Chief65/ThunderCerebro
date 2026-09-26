# 📖 QuickShop-Hikari

- **Categoría**: Tiendas de Jugadores / Economía Descentralizada
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Documentación Oficial**: [QuickShop-Hikari Documents](https://quickshop-community.github.io/QuickShop-Hikari-Documents/)
- **Dependencias Clave**: Vault, ProtocolLib / PacketEvents (opcional según renderer), PlaceholderAPI, WorldGuard / ProtectionStones.

---

## 🎯 Propósito & Funcionalidad
**QuickShop-Hikari** es un plugin de tiendas basado en cofres y contenedores (Chests, Trapped Chests, Barrels, Shulker Boxes) optimizado para alto rendimiento y control estricto de transacciones en economías descentralizadas. Permite a los usuarios crear tiendas físicas de compra y venta (`/qs buy`, `/qs sell`) simplemente interactuando con un contenedor sosteniendo el ítem en la mano.

Incorpora soporte para componentes de Minecraft 1.20.5+ / 1.21.11, NBT avanzado, displays flotantes virtuales (ItemDisplay/TextDisplay entities vía paquetes), registro de auditoría de transacciones y persistencia en bases de datos SQL (MySQL / MariaDB / H2).

---

## 🏗️ Arquitectura & Funcionamiento Interno
1. **Virtual Display Engine**:
   - Utiliza Minecraft 1.19.4+ `ItemDisplay` y `TextDisplay` entities gestionadas por paquetes hacia el cliente sin instanciar entidades pesadas en los chunks del servidor, reduciendo a cero la degradación de guardado de mundos y TPS.
2. **Transaction Threading**:
   - La validación del inventario del contenedor y la verificación de fondos en Vault se ejecutan en sincronía con el hilo principal para prevenir condiciones de carrera (Race Conditions), mientras que los logs y auditorías se delegan a un pool HikariCP asíncrono.
3. **Control de Contenedores y Protecciones**:
   - Dispara eventos simulados y chequeos de protección (`BlockBreakEvent` / `PlayerInteractEvent`) verificando hooks con WorldGuard, ProtectionStones y GriefPrevention.

---

## ⚙️ Configuración Crítica (`config.yml`)

```yaml
# ==========================================
# Configuración Optimizada QuickShop-Hikari
# ==========================================

# Motor de Base de Datos
database:
  type: "MySQL" # Opciones: H2, SQLite, MySQL, MariaDB
  host: "127.0.0.1"
  port: 3306
  database: "thundermc_quickshop"
  user: "thundermc_user"
  password: "YOUR_SECURE_PASSWORD"
  prefix: "qs_"
  use-ssl: false
  # HikariCP Pool Tuning
  maximum-pool-size: 10
  minimum-idle: 2
  connection-timeout: 30000
  idle-timeout: 600000
  max-lifetime: 1800000

# Configuración de Displays Visuales
display:
  engine: "PACKET" # O "NATIVE_ENTITY" (Se recomienda PACKET o DISPLAY_ENTITY en 1.21.11)
  entity-type: "ITEM_DISPLAY" # Requiere Paper 1.19.4+
  show-item: true
  show-text: true
  text-format:
    - "&e&l{0}" # Nombre del ítem
    - "&aCompra: &f${1} &8| &cVenta: &f${2}"
    - "&7Stock: &b{3}"
  view-distance: 16 # Chunks/bloques de visualización para ahorrar ancho de banda
  update-ticks: 20 # Frecuencia de actualización de texto

# Protección y Seguridad Económica
shop:
  lock-chest: true # Impide abrir el cofre a usuarios sin permisos
  prevent-despawn: true
  allow-stacks: true # Soporte para venta por paquetes/stacks
  maximum-price: 100000000.0 # Límite para evitar overflow de double
  minimum-price: 0.01
  tax:
    enable: true
    rate: 0.05 # 5% de impuesto por transacción hacia la bóveda del servidor
    receiver: "ServerTaxAccount"
  blacklist-items:
    - "BEDROCK"
    - "BARRIER"
    - "STRUCTURE_BLOCK"
    - "DEBUG_STICK"
    - "*_SPAWN_EGG"

# Control de Dupes y Concurrencia
interaction:
  cooldown-ms: 500 # Cooldown entre clics de compra/venta para evitar spam de paquetes
  enable-click-confirm: true # Confirmación previa para compras de alto valor
```

---

## 💻 Comandos & Permisos

### Comandos de Jugador
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/qs` o `/quickshop` | Muestra la interfaz interactiva de ayuda. | `quickshop.use` |
| `/qs buy` | Cambia el modo a compra (la tienda compra ítems de clientes). | `quickshop.create.buy` |
| `/qs sell` | Cambia el modo a venta (la tienda vende ítems a clientes). | `quickshop.create.sell` |
| `/qs price <precio>` | Modifica el precio unitario del ítem de la tienda seleccionada. | `quickshop.create.changeprice` |
| `/qs stack <cantidad>` | Establece la cantidad vendida/comprada en lote por clic. | `quickshop.create.stacks` |
| `/qs staff <add/remove/list>`| Gestiona miembros autorizados para reponer stock. | `quickshop.staff` |
| `/qs transfer <jugador>` | Transfiere la titularidad de la tienda a otro jugador. | `quickshop.transfer` |
| `/qs remove` | Elimina la tienda seleccionada y remueve displays. | `quickshop.create.remove` |

### Comandos de Administración
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/qs unlimited` | Transforma una tienda en infinita (tipo Admin Shop). | `quickshop.unlimited` |
| `/qs setowner <jugador>` | Modifica administrativamente el dueño de la tienda. | `quickshop.admin` |
| `/qs clean` | Remueve tiendas huérfanas o con cofres rotos. | `quickshop.admin` |
| `/qs purge <días>` | Purga de la base de datos tiendas inactivas por X días. | `quickshop.admin` |
| `/qs reload` | Recarga las configuraciones y ficheros de idioma. | `quickshop.reload` |

---

## 🧩 Placeholders PlaceholderAPI (PAPI)
* `%quickshop_total_shops%`: Cantidad total de tiendas activas en el servidor.
* `%quickshop_player_shops%`: Cantidad de tiendas creadas por el jugador.
* `%quickshop_total_earned%`: Monedas totales obtenidas por ventas del jugador.
* `%quickshop_total_spent%`: Monedas totales gastadas por compras del jugador.
* `%quickshop_is_shop_owner%`: Retorna `true`/`false` si el bloque observado es tienda propia.

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Doble Clic / Packet Spam Dupe**:
   - **Riesgo**: Clientes enviando múltiples paquetes `USE_ITEM_ON` en el mismo tick para duplicar transferencias de Vault antes de actualizar el inventario.
   - **Mitigación**: QuickShop-Hikari implementa un semáforo de exclusión mutua en memoria y un `interaction.cooldown-ms` de 500 ms.
2. **Extracción mediante Tolvas / Hoppers**:
   - Bloquear el vaciado automático de cofres-tienda habilitando el chequeo de eventos de inventario y protecciones de tolva en `config.yml`.
3. **Exploit de Renombrado / Modificación de NBT**:
   - Hikari valida el ítem mediante serialización estricta y comparación de componentes NBT. Si un usuario introduce ítems con componentes alterados pretendiendo cobrar por el original, la compra/venta se bloquea automáticamente.
4. **Desconexión Forzada Durante Transacción**:
   - Si un jugador cierra sesión en mitad del procesamiento, la transacción se aborta atómicamente antes de registrar movimientos de saldo en Vault.

---

## ⚡ Optimización de Base de Datos & Rendimiento
- **HikariCP Pool**: Ajustar `maximum-pool-size: 10` y `minimum-idle: 2` para mitigar tiempos de espera en redes con alta concurrencia.
- **Display Engine**: Utilizar `ITEM_DISPLAY` nativo de Minecraft 1.21+ en lugar de entidades `ARMOR_STAND` para evitar sobrecarga en el pipeline de render del servidor y del cliente.
- **Mantenimiento**: Programar purgas automáticas con `/qs purge 60` para limpiar tiendas abandonadas de jugadores inactivos.
