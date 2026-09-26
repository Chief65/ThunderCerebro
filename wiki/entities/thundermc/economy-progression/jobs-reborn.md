# 📖 Jobs Reborn & Progresión Económica

- **Categoría**: Profesiones, Economía de Actividades & Retención de Jugadores
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Documentación Oficial**: [Jobs Reborn Wiki (SpigotMC/GitHub)](https://github.com/Zrips/Jobs)
- **Dependencias Clave**: Vault, PlaceholderAPI, CMI / EssentialsX, WorldGuard, CoreProtect (anti-exploit de bloques colocados).

---

## 🎯 Propósito & Funcionalidad
**Jobs Reborn** es el motor principal de progresión y generación pasiva/activa de dinero, experiencia y puntos de trabajo para los jugadores mediante profesiones (Miner, Woodcutter, Hunter, Farmer, Builder, Fisher, Crafter, Enchanter, Digger, Explorer). Ofrece misiones diarias (Daily Quests), límites de ganancia por tiempo (Money Limits), bonificaciones por rangos (Boosters) y control estricto anti-trampas mediante seguimiento de bloques colocados por jugadores.

---

## 🏗️ Arquitectura & Funcionamiento Interno
1. **Block Ownership Tracking & CoreProtect/Internal Metadata**:
   - Para evitar que los jugadores coloquen y rompan repetidamente el mismo mineral o madera, el plugin registra metadatos en memoria y base de datos sobre los bloques colocados por usuarios, anulando el pago de dinero/XP para bloques no generados naturalmente por el mapa.
2. **Dynamic Payout Curve & Formulas**:
   - Las ganancias de dinero y experiencia escalan con el nivel de cada trabajo mediante fórmulas matemáticas configurables: `base-payout * (level ^ exponent)`.
3. **Database Caching & Batch Updates**:
   - Mantiene los datos de progreso de trabajos de los jugadores en memoria RAM y realiza guardados periódicos en lote (Batch Saving) a MariaDB/MySQL para no sobrecargar las conexiones SQL.

---

## ⚙️ Configuración Crítica (`generalConfig.yml` & `jobs/*.yml`)

### Configuración General Optimizada (`generalConfig.yml`)
```yaml
# Control Anti-Exploit y Límites Económicos
Economy:
  PaymentMethod: "Vault"
  # Límite de dinero ganado por trabajo cada 60 minutos para frenar granjas AFK
  MoneyLimit:
    Enable: true
    MoneyLimit: 25000.0
    TimeLimit: 3600
    StopPayment: true # Deja de pagar al llegar al límite

AntiCheat:
  BlockBreak:
    # Ignorar pago en bloques colocados por jugadores (requiere NBT/Metadata)
    IgnorePlacedBlocks: true
    # Duración de la marca de bloque colocado en segundos (ej. 24 horas)
    Timer: 86400
  SpawnerMobs:
    # Deshabilitar o reducir pago por matar mobs nacidos de Spawners/granjas
    IgnoreSpawnerMobs: true
  Riding:
    # Evitar pagos de Explorer si el jugador viaja en botes/vagonetas AFK
    IgnoreRiding: true

Storage:
  Database: "MYSQL"
  Mysql:
    Host: "127.0.0.1"
    Port: 3306
    Database: "thundermc_jobs"
    Username: "thundermc_user"
    Password: "YOUR_SECURE_PASSWORD"
    PoolSize: 10
```

### Configuración de Ejemplo de Trabajo (`jobs/miner.yml`)
```yaml
Miner:
  fullname: "&b&lMinero"
  shortname: "M"
  description: "Gana dinero y experiencia extrayendo minerales y piedras preciosas."
  ChatColour: "AQUA"
  max-level: 100
  leveling-progression:
    experience: "100*(level^1.5)"
    money: "1.0*(level^0.8)"
  Break:
    STONE:
      income: 0.05
      experience: 0.05
    DEEPSLATE:
      income: 0.06
      experience: 0.06
    COAL_ORE:
      income: 1.50
      experience: 1.00
    IRON_ORE:
      income: 3.00
      experience: 2.50
    DIAMOND_ORE:
      income: 25.00
      experience: 20.00
    ANCIENT_DEBRIS:
      income: 150.00
      experience: 100.00
```

---

## 💻 Comandos & Permisos

### Comandos de Jugador
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/jobs` o `/jobs browse` | Abre la interfaz gráfica para explorar y unirse a trabajos. | `jobs.command.browse` |
| `/jobs join <trabajo>` | Se une a una profesión específica. | `jobs.command.join` |
| `/jobs leave <trabajo>` | Abandona una profesión. | `jobs.command.leave` |
| `/jobs stats` | Muestra el nivel actual, experiencia y límite restante. | `jobs.command.stats` |
| `/jobs quests` | Abre el menú de misiones diarias del trabajo. | `jobs.command.quests` |
| `/jobs top <trabajo>` | Muestra la tabla de clasificación de niveles. | `jobs.command.top` |

### Comandos de Administración
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/jobs glog <jugador>` | Inspecciona el registro de ganancias detalladas de un usuario. | `jobs.command.admin.glog` |
| `/jobs editjobs <jugador> <trabajo> setlevel <nivel>` | Establece el nivel de un jugador en un trabajo. | `jobs.command.admin.editjobs` |
| `/jobs boost <trabajo/all> <multiplicador>` | Aplica un evento global de doble dinero/XP en la network. | `jobs.command.admin.boost` |
| `/jobs reload` | Recarga las fórmulas, archivos de trabajos y traducciones. | `jobs.command.admin.reload` |

---

## 🧩 Placeholders PlaceholderAPI (PAPI)
* `%jobsr_user_jobs%`: Lista de trabajos actuales en los que está inscrito el jugador.
* `%jobsr_user_job_<num>_level%`: Nivel alcanzado en el trabajo número X.
* `%jobsr_user_job_<num>_exp%`: Experiencia actual en el trabajo número X.
* `%jobsr_user_job_<num>_maxexp%`: Experiencia requerida para subir al siguiente nivel.
* `%jobsr_user_limit_money%`: Dinero restante que el jugador puede ganar antes del límite horario.

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Place & Break Exploit (Miner / Builder / Woodcutter)**:
   - **Vulnerabilidad**: Jugadores colocando bloques de diamante o madera para luego romperlos infinitamente con picos/hachas de fortuna.
   - **Solución**: Activar `IgnorePlacedBlocks: true` y enlazar con `CoreProtect` para descartar bloques alterados por jugadores.
2. **Granjas AFK de Spawners & Mob Farms**:
   - **Vulnerabilidad**: Dejar cuentas AFK con macros matando esqueletos/zombis de spawners para farmear miles de monedas sin jugar.
   - **Solución**: Habilitar `IgnoreSpawnerMobs: true` en `generalConfig.yml`.
3. **Exploit de Movimiento AFK (Explorer Job)**:
   - Bloquear pagos por desplazamientos en botes automáticos sobre hielo o vagonetas continuas (`IgnoreRiding: true` e `IgnorePistonMoves: true`).
4. **Inflación Desmedida de la Economía**:
   - Implementar techos de pago (`MoneyLimit`) por hora para que las cuentas de granjas o bots no desestabilicen el balance macroeconómico de ThunderMC.
