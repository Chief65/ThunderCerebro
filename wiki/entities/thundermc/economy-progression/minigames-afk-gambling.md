# 📖 Plugins de Minijuegos y Recompensas de Retención

- **Categoría**: Retención AFK, Apuestas y Minijuegos Económicos
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Plugins Cubiertos**: AxAFKZone, DeluxeCoinflip, GambleBarPro
- **Dependencias Clave**: Vault, PlayerPoints, PlaceholderAPI, WorldGuard.

---

## 1. ⏳ AxAFKZone (Zona de Recompensas AFK)

### 🎯 Propósito & Arquitectura
**AxAFKZone** permite delimitar regiones físicas (generalmente en la Sala AFK del Spawn) donde los jugadores ausentes reciben recompensas progresivas y periódicas (dinero, llaves de cajas, ítems o puntos) sin desconectarse del servidor.

### ⚙️ Configuración & Recompensas (`plugins/AxAFKZone/config.yml`)
```yaml
# Región WorldGuard asignada a la zona AFK
region: "afk_zone"
check-interval: 20 # Chequeo cada segundo (20 ticks)

rewards:
  tier1:
    chance: 100.0
    interval-seconds: 300 # Cada 5 minutos
    commands:
      - "eco give %player% 250"
      - "p give %player% 5"
  tier2:
    chance: 15.0 # 15% de probabilidad
    interval-seconds: 900 # Cada 15 minutos
    permission: "axafkzone.booster.vip" # Recompensa VIP
    commands:
      - "crates key give %player% voting 1"
```

### 💻 Comandos & Permisos
- `/afkzone reload`: Recarga la configuración del plugin (`axafkzone.admin`).
- Permisos de multiplicador: `axafkzone.multiplier.<valor>`.

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## 2. 🪙 DeluxeCoinflip (Lanzamiento de Monedas PvP)

### 🎯 Propósito & Arquitectura
**DeluxeCoinflip** es un sistema de apuestas 1v1 entre jugadores donde ambos arriesgan la misma cantidad de dinero o PlayerPoints con un 50% de probabilidad de ganar el pozo total, aplicando un porcentaje de impuesto (Tax) que actúa como sumidero económico (Money Sink).

### ⚙️ Configuración Optimizada (`plugins/DeluxeCoinflip/config.yml`)
```yaml
currency: "VAULT" # O PLAYER_POINTS
min-bet: 1000.0
max-bet: 50000000.0 # Techo de apuesta para prevenir quiebras o lavado de dinero
tax:
  enabled: true
  percentage: 5.0 # El servidor quema el 5% del pozo para combatir la inflación

animation:
  enabled: true
  duration: 5 # Segundos de ruleta GUI

anti-dupe:
  deduct-instantly: true # Deduce el balance de inmediato al publicar la apuesta
```

### 💻 Comandos & Permisos
- `/coinflip` o `/cf`: Abre el menú de apuestas activas (`deluxecoinflip.use`).
- `/cf create <monto> <cara/cruz>`: Crea una apuesta pública (`deluxecoinflip.create`).
- `/cf cancel`: Cancela la apuesta propia y devuelve los fondos al jugador (`deluxecoinflip.cancel`).
- `/cf reload`: Recarga configuraciones (`deluxecoinflip.admin`).

---

## 3. 🍸 GambleBarPro (Bar de Apuestas con NPCs/GUI)

### 🎯 Propósito & Arquitectura
**GambleBarPro** introduce una taberna/bar interactivo donde los usuarios compran bebidas alcohólicas o pociones mágicas que tienen un porcentaje de ganancia o pérdida económica y efectos visuales de pociones al consumirlas.

### ⚙️ Configuración de Bebidas (`plugins/GambleBarPro/drinks.yml`)
```yaml
drinks:
  cerveza_trueno:
    name: "&e&lCerveza del Trueno"
    price: 5000.0
    win-chance: 45.0 # 45% probabilidad de éxito (ventaja para la casa)
    win-multiplier: 2.0 # Si gana, recibe $10,000
    effects:
      - "NAUSEA:100:1"
      - "CONFUSION:80:1"
  whisky_dragon:
    name: "&c&lWhisky del Dragón"
    price: 25000.0
    win-chance: 30.0
    win-multiplier: 3.2 # Si gana, recibe $80,000
```

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Coinflip Double-Bet Dupe**:
   - **Vulnerabilidad**: Crear una apuesta y transferir dinero antes de que otro jugador acepte, generando fondos de la nada.
   - **Solución**: El plugin retira los fondos del saldo del jugador en el instante exacto en que la apuesta se registra en el menú (`deduct-instantly: true`). Si se cancela, se reembolsa.
2. **AFK Spoofing en AxAFKZone**:
   - Para evitar que los jugadores ejecuten scripts de movimiento fuera de la zona para saltarse el detector AFK vanilla, la zona se delimita rígidamente con WorldGuard y flags de entrada.
3. **Inflación por Minijuegos de Apuestas**:
   - Las apuestas del servidor (GambleBarPro) deben tener un RTP (Return to Player) del 80%-90% (ventaja matemática para la casa) para actuar como filtros de absorción y destrucción de moneda circulante.

---

## Referencias Cruzadas
- [[wiki/entities/thundermc/core-infrastructure/vault|Vault]]
- [[wiki/entities/thundermc/economy-progression/playerpoints|PlayerPoints]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
