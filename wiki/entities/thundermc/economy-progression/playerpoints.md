# 📖 PlayerPoints

- **Categoría**: Moneda Secundaria Premium / Tokens
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Documentación Oficial**: [PlayerPoints Wiki (GitHub)](https://github.com/Blackixx/PlayerPoints/wiki)
- **Dependencias Clave**: Vault (opcional vía Hook), PlaceholderAPI, MySQL / MariaDB / SQLite.

---

## 🎯 Propósito & Funcionalidad
**PlayerPoints** es el sistema de moneda secundaria y créditos premium más ligero, estable y extendido para redes de Minecraft. Permite gestionar una economía paralela al dinero tradicional de Vault (Tokens de Donación, Puntos de Eventos, ThunderPoints, BattlePass points), con soporte completo para transacciones instantáneas, transferencias entre jugadores, tiendas de puntos y sincronización en tiempo real a través de bases de datos relacionales.

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## 🏗️ Arquitectura & Funcionamiento Interno
1. **Thread-Safe Point Transactions**:
   - Todas las operaciones de depósito, retiro y consulta de puntos utilizan llamadas concurrentes con semáforos en memoria y actualizaciones asíncronas en base de datos.
2. **Multi-Server Database Sync**:
   - Al usar MySQL/MariaDB, sincroniza el saldo de puntos de forma transparente entre múltiples modalidades de la network mediante transacciones atómicas `UPDATE ... SET points = points + ? WHERE uuid = ?`.
3. **PAPI & GUI Integrations**:
   - Integración nativa con ShopGUI+, DeluxeMenus, ExcellentCrates, UltraCosmetics y BattlePass para el cobro de ítems y rangos cosméticos o temporales.

---

## ⚙️ Configuración Crítica (`config.yml`)

```yaml
# ==========================================
# Configuración Optimizada PlayerPoints
# ==========================================

storage:
  # Opciones: SQLITE, MYSQL, MARIADB
  type: "MYSQL"
  host: "127.0.0.1"
  port: 3306
  database: "thundermc_points"
  username: "thundermc_user"
  password: "YOUR_SECURE_PASSWORD"
  table: "playerpoints_data"
  import:
    use: false
    source: "SQLITE"

points:
  # Nombre y formato de la moneda
  name: "ThunderPoints"
  symbol: "⛃"
  decimals: false # Moneda entera (sin decimales) para prevenir errores de coma flotante
  minimum: 0
  maximum: 2000000000 # Limitar a Integer.MAX_VALUE para evitar overflow

transaction:
  allow-pay: true # Permitir que los jugadores se envíen puntos con /points pay
  pay-tax-percentage: 0.0 # Impuesto de transferencia
  log-to-console: true
  log-to-file: true # Registro estricto de auditoría para auditorías de tienda Tebex / donaciones
```

---

## 💻 Comandos & Permisos

### Comandos de Jugador
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/points me` o `/points` | Consulta el saldo actual de puntos del jugador. | `playerpoints.points` |
| `/points pay <jugador> <cantidad>` | Transfiere puntos a otro usuario conectado. | `playerpoints.pay` |
| `/points top [página]` | Muestra el ranking de jugadores con más puntos. | `playerpoints.lead` |
| `/points help` | Muestra la lista de comandos disponibles. | `playerpoints.points` |

### Comandos de Administración
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/points give <jugador> <cantidad>` | Entrega puntos a un usuario (compatible con Tebex/Buycraft). | `playerpoints.give` |
| `/points giveall <cantidad>` | Otorga puntos a todos los jugadores conectados. | `playerpoints.giveall` |
| `/points take <jugador> <cantidad>` | Deduce puntos del balance de un usuario. | `playerpoints.take` |
| `/points set <jugador> <cantidad>` | Establece el saldo exacto de puntos de un usuario. | `playerpoints.set` |
| `/points reset <jugador>` | Reinicia a 0 los puntos de un jugador. | `playerpoints.reset` |
| `/points look <jugador>` | Consulta el saldo de puntos de cualquier jugador offline/online. | `playerpoints.look` |
| `/points reload` | Recarga las configuraciones y mensajes. | `playerpoints.reload` |

---

## 🧩 Placeholders PlaceholderAPI (PAPI)
* `%playerpoints_points%`: Saldo actual de puntos del jugador sin formato (ej. `1500`).
* `%playerpoints_points_formatted%`: Saldo formateado con separadores de miles (ej. `1,500`).
* `%playerpoints_points_compact%`: Formato compacto abreviado (ej. `1.5k`, `2.4M`).
* `%playerpoints_top_player_<1-10>%`: Nombre del jugador en la posición X del top.
* `%playerpoints_top_points_<1-10>%`: Puntos del jugador en la posición X del top.

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Packet Delay / Pay Spam Glitch**:
   - **Vulnerabilidad**: Jugadores enviando múltiples comandos `/points pay` en paralelo en milisegundos para transferir más puntos de los que poseen antes de registrar la deducción.
   - **Solución**: PlayerPoints ejecuta un bloqueo sincronizado por UUID. Si el saldo actual es menor que el monto a debitar, la transacción se cancela instantáneamente.
2. **Integer Overflow Vulnerability**:
   - **Vulnerabilidad**: Si un comando de entrega concede más de `2,147,483,647` puntos, el valor de 32-bit se vuelve negativo (`-2147483648`).
   - **Solución**: Mantener `decimals: false` y configurar `maximum: 2000000000` en `config.yml` para rechazar cualquier suma fuera de rango.
3. **Desconexión Forzada y Rollbacks de Servidor**:
   - Al estar conectado a MariaDB/MySQL, las operaciones ejecutan `COMMIT` inmediato. Los reinicios repentinos o crashes de Paper no revierten las transacciones de puntos ni compras web de la tienda.

---

## Referencias Cruzadas
- [[wiki/concepts/monetizacion-modelo-negocio|Modelo MonetizaciÃ³n]]
- [[wiki/entities/thundermc/economy-progression/excellentcrates|ExcellentCrates]]
- [[wiki/entities/thundermc/core-infrastructure/vault|Vault]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
