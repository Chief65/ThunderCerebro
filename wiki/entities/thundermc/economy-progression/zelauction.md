# 📖 ZelAuction

- **Categoría**: Casa de Subastas / Mercado Global P2P
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Documentación Oficial**: [ZelAuction Docs (PikzStudio)](https://zelauction.pikzstudio.xyz/zelauction)
- **Dependencias Clave**: Vault, PlaceholderAPI, MySQL / MariaDB (Recomendado para multi-instancia o red).

---

## 🎯 Propósito & Funcionalidad
**ZelAuction** es un sistema moderno de Casa de Subastas (`/ah`, `/auctionhouse`) diseñado para entornos de alto tráfico en Minecraft 1.20+ y 1.21+. Proporciona una interfaz gráfica fluida, compras directas (Buy Now), subastas con pujas en tiempo real, caducidad de ítems en buzón de reclamo (Expired Storage) e historial de transacciones seguro.

---

## 🏗️ Arquitectura & Funcionamiento Interno
1. **Asynchronous Auction Indexer**:
   - Mantiene un índice en memoria RAM de todos los ítems subastados activos para renderizar GUIs a 60+ FPS sin bloquear el hilo principal de Paper.
2. **Atomic Transaction Lock**:
   - Cuando un jugador hace clic en comprar, el plugin reserva el ítem mediante un cerrojo atómico (Atomic Lock). Si dos jugadores compran el mismo milisegundo, solo la primera transacción pasa a Vault; la segunda es rechazada limpiamente sin duplicaciones de saldo ni de ítems.
3. **Módulo de Ítems Caducados / Unsold Queue**:
   - Los ítems no vendidos se transfieren a un almacén persistente (`/ah expired`) serializado en base de datos, evitando pérdidas por reinicios o limpiezas de entidades.

---

## ⚙️ Configuración Crítica (`config.yml`)

```yaml
# ==========================================
# Configuración Optimizada ZelAuction
# ==========================================

settings:
  currency: "VAULT" # Opciones: VAULT, PLAYER_POINTS, CUSTOM
  listing-duration: 86400 # 24 horas en segundos
  expired-item-storage-duration: 604800 # 7 días antes de purge
  max-listings-per-player: 5
  min-price: 1.0
  max-price: 100000000.0
  
  # Impuestos de Subasta
  tax:
    listing-tax-percent: 2.0 # 2% por poner a la venta (evita spam en el AH)
    sale-tax-percent: 5.0 # 5% descontado de la ganancia final
    
  # Sonidos y Feedback
  sound-effects: true
  discord-webhook:
    enabled: true
    url: "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    notify-rare-sales-above: 1000000.0

# Base de Datos
storage:
  type: "MYSQL"
  host: "127.0.0.1"
  port: 3306
  database: "thundermc_zelauction"
  username: "thundermc_user"
  password: "YOUR_SECURE_PASSWORD"
  pool:
    maximum-pool-size: 8
    minimum-idle: 2
    connection-timeout: 30000
```

---

## 💻 Comandos & Permisos

### Comandos de Jugador
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/ah` o `/auction` | Abre el menú principal de la casa de subastas. | `zelauction.use` |
| `/ah sell <precio>` | Pone en venta el ítem sostenido en mano. | `zelauction.sell` |
| `/ah bid <precio-inicial>` | Abre una subasta con sistema de pujas. | `zelauction.bid` |
| `/ah expired` | Abre la bóveda de ítems caducados o cancelados. | `zelauction.expired` |
| `/ah search <término>` | Filtra las subastas activas por nombre de ítem o vendedor. | `zelauction.search` |
| `/ah history` | Muestra el historial reciente de ventas y compras del jugador. | `zelauction.history` |

### Comandos de Administración
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/ah admin reload` | Recarga ficheros de configuración y mensajes. | `zelauction.admin.reload` |
| `/ah admin remove <id>` | Retira una subasta de manera forzosa y la devuelve al dueño. | `zelauction.admin.remove` |
| `/ah admin purge <días>` | Purga ítems del almacén expirado con más de X días. | `zelauction.admin.purge` |

---

## 🧩 Placeholders PlaceholderAPI (PAPI)
* `%zelauction_active_listings%`: Total de subastas activas de la network.
* `%zelauction_player_listings%`: Cantidad de subastas activas creadas por el jugador.
* `%zelauction_player_max_listings%`: Límite máximo de subastas permitidas al jugador.
* `%zelauction_expired_count%`: Cantidad de ítems pendientes de recoger en `/ah expired`.

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Packet Delay / Multi-Buy Race Condition**:
   - **Vulnerabilidad**: Dos clientes enviando paquetes de compra concurrentes para clonar un ítem único con NBT valioso.
   - **Solución**: ZelAuction serializa las compras en un pipeline single-thread con locks a nivel de ID único de subasta antes de contactar a Vault.
2. **Ítems Shulker / Mochilas Anidadas con Contrabando**:
   - Bloquear la subasta de contenedores con items prohibidos o limitar el tamaño del payload de NBT para prevenir que paquetes gigantes crasheen a clientes al abrir la GUI (`max-nbt-size-bytes: 65536`).
3. **Lavado de Dinero y Evasión de Impuestos**:
   - La tasa de publicación (`listing-tax-percent: 2.0`) disuade a los usuarios de usar `/ah` como almacenamiento infinito temporal.
4. **Pérdida de Ítems por Inventario Lleno**:
   - Si el jugador compra un ítem o recoge un expirado con el inventario lleno, el plugin no lo arroja al suelo (donde un clearlag podría borrarlo); lo mantiene seguro en `/ah expired`.
