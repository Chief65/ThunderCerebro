# 📦 InventoryRollbackPlus - Documentación Técnica

- **Categoría**: Recuperación de Datos de Jugador / Backups de Inventarios
- **Versión Core Soportada**: Minecraft 1.13.x - 1.21.x (Paper / Purpur)
- **Desarrollador**: TechnicallyCoded
- **Dependencias**: MySQL / SQLite, PlaceholderAPI
- **Ruta de Configuración**: `plugins/InventoryRollbackPlus/`

---

## 🏛️ 1. Arquitectura y Funcionamiento Interno

InventoryRollbackPlus captura instantáneas completas (Snapshots) de los inventarios, armaduras, efectos de pociones, nivel de experiencia, hambre y ubicación del jugador en momentos críticos de la sesión de juego.

```mermaid
flowchart TD
    A[Disparador de Evento: Muerte / Desconexión / Cambio de Mundo / Forzado] --> B[Clonar Estado de ItemStack[] & Player Data]
    B --> C[Serializar Datos NBT a Formato Base64 / JSON / Binario]
    C --> D[Enviar Tarea Asíncrona al Pool de Guardado]
    D --> E[(Base de Datos SQLite / MySQL)]
    E --> F[Rutina de Purga Periódica según max-days-retention]
```

### Eventos de Captura (Snapshots):
1. **Death Snapshot**: Captura el inventario exacto antes de que los ítems caigan al suelo por muerte del jugador.
2. **Quit Snapshot**: Registrado inmediatamente antes de desconectarse de la sesión.
3. **World Change**: Instantánea al cambiar de dimensión (Overworld -> Nether -> End).
4. **Periodic / Force Backup**: Guardados automáticos por intervalos o invocados mediante comando.

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## ⚙️ 2. Configuración Crítica (`config.yml`)

```yaml
database:
  type: SQLITE # O MYSQL para clusters
  mysql:
    host: "127.0.0.1"
    port: 3306
    database: "inventory_backups"
    username: "root"
    password: "password"

retention:
  # Eliminar automáticamente backups con más de 14 días
  max-retention-days: 14
  # Límite máximo de backups por jugador
  max-saves-per-player: 50

events:
  save-on-death: true
  save-on-join: true
  save-on-quit: true
  save-on-world-change: true

sounds:
  enabled: true
  restore-sound: "ENTITY_PLAYER_LEVELUP"
```

---

## 💻 3. Comandos y Jerarquía de Permisos

### Comandos de Operación:
| Comando | Descripción | Permiso |
| :--- | :--- | :--- |
| `/irp restore <jugador>` | Abre la interfaz gráfica con el historial cronológico de backups. | `inventoryrollbackplus.restore` |
| `/irp forcebackup <jugador>` | Fuerza la creación inmediata de una instantánea. | `inventoryrollbackplus.forcebackup` |
| `/irp purge <días>` | Purga manualmente registros antiguos de la base de datos. | `inventoryrollbackplus.purge` |
| `/irp reload` | Recarga la configuración del plugin. | `inventoryrollbackplus.reload` |

### Jerarquía de Permisos:
- `inventoryrollbackplus.admin`: Acceso completo a restauraciones, purgas y configuraciones.
- `inventoryrollbackplus.restore.self`: Permite al usuario ver o restaurar sus propios backups (si se habilita).

---

## 🧩 4. Integración con PlaceholderAPI (PAPI)

| Placeholder | Descripción |
| :--- | :--- |
| `%irp_total_backups%` | Cantidad total de copias de seguridad almacenadas para el jugador. |
| `%irp_last_death_time%` | Fecha y hora del último evento de muerte registrado. |

---

## 🛡️ 5. Modos de Fallo, Exploits y Prevención

> [!CAUTION]
> **Riesgo de Duplicación por Restauraciones Maliciosas**:
> Si un moderador restaura el inventario a un jugador cuyos ítems no se perdieron realmente (por ejemplo, ya los había guardado en un cofre antes de morir), los ítems se duplicarán en el servidor.
> **Mitigación**: Siempre verificar los registros de `CoreProtect` (`/co l u:<jugador>`) antes de autorizar un `/irp restore`.

> [!TIP]
> **Crecimiento de la Base de Datos SQLite**:
> En servidores con cientos de muertes diarias, el archivo `.db` puede alcanzar gigabytes rápidamente.
> **Optimización**: Configurar `max-retention-days: 7` o migrar a MySQL con particionado mensual.

---

## Referencias Cruzadas
- [[wiki/entities/thundermc/world-protection/coreprotect|CoreProtect]]
- [[wiki/entities/thundermc/world-protection/pvpmanager|PvPManager]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
