# 📖 ExcellentCrates

- **Categoría**: Cajas de Recompensas (Crates) & Gacha
- **Servidor**: ThunderMC Survival (Paper/Purpur 1.21.11)
- **Documentación Oficial**: [NightExpress ExcellentCrates Docs](https://nightexpressdev.com/excellentcrates/)
- **Dependencias Clave**: NightCore (Core Engine), Vault, PlaceholderAPI, DecentHolograms / HolographicDisplays (o Displays nativos).

---

## 🎯 Propósito & Funcionalidad
**ExcellentCrates** es un motor avanzado y visualmente optimizado de cajas de recompensas (Crates). Ofrece soporte para llaves físicas y virtuales, aperturas con animaciones configurables (CS:GO Roulette, Wheel, Instant, Mystery Box), hologramas interactivos por encima del bloque de la caja, editor GUI en tiempo real (`/crates editor`) y tablas de recompensas con porcentajes probabilísticos exactos.

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## 🏗️ Arquitectura & Funcionamiento Interno
1. **Core Integration (NightCore Engine)**:
   - Basado en el framework modular `NightCore`, que centraliza el manejo de menús GUI, parsing de componentes de texto moderno (MiniMessage/Adventure) y llamadas asíncronas seguras.
2. **Key Verification System (Physical vs Virtual)**:
   - **Llaves Físicas**: Identificadas mediante PDC (PersistentDataContainer) y NBT tags únicos a prueba de falsificación por renombrado en yunques.
   - **Llaves Virtuales**: Almacenadas en la base de datos del jugador (SQLite / MySQL) accesibles remotamente o al hacer clic directo en el cofre.
3. **Roll Engine & Probability Logic**:
   - Cálculo de probabilidad ponderada (Weight-based drops) garantizando un porcentaje determinista en la distribución de premios raros, épicos y legendarios.

---

## ⚙️ Configuración & Estructura de Cajas

### Configuración de Caja Ejemplo (`plugins/ExcellentCrates/crates/legendary.yml`)
```yaml
id: "legendary"
name: "&6&lCaja Legendaria"
block:
  type: "ENDER_CHEST"
  hologram:
    enabled: true
    offset-y: 1.8
    lines:
      - "&6&l⚡ CAJA LEGENDARIA ⚡"
      - "&7¡Haz clic derecho con tu llave!"
      - "&eLlaves virtuales: &a%excellentcrates_keys_legendary%"

key:
  id: "legendary_key"
  name: "&6&lLlave Legendaria"
  material: "TRIPWIRE_HOOK"
  glow: true
  lore:
    - "&7Úsala en el Spawn para"
    - "&7reclamar premios exclusivos."

opening:
  animation: "ROULETTE" # Opciones: INSTANT, CSGO, ROULETTE, WHEEL
  duration: 7 # Segundos
  sound: "BLOCK_NOTE_BLOCK_BELL"

rewards:
  1:
    name: "&6Espada del Trueno"
    chance: 5.0 # 5%
    broadcast: true
    item:
      material: "NETHERITE_SWORD"
      name: "&6&lEspada del Trueno"
      enchantments:
        SHARPNESS: 6
        UNBREAKING: 4
  2:
    name: "&a$50,000 Dinero"
    chance: 25.0
    commands:
      - "eco give %player% 50000"
  3:
    name: "&b500 Puntos Thunder"
    chance: 35.0
    commands:
      - "p give %player% 500"
```

---

## 💻 Comandos & Permisos

### Comandos Principales
| Comando | Descripción | Permiso Requerido |
| :--- | :--- | :--- |
| `/crates` | Abre el menú de cajas disponibles o llaves virtuales. | `excellentcrates.user` |
| `/crates key give <jugador> <caja> <cantidad>` | Entrega llaves físicas a un usuario. | `excellentcrates.admin.key.give` |
| `/crates key giveall <caja> <cantidad>` | Entrega llaves a todos los jugadores conectados. | `excellentcrates.admin.key.giveall` |
| `/crates key take <jugador> <caja> <cantidad>` | Retira llaves físicas/virtuales a un usuario. | `excellentcrates.admin.key.take` |
| `/crates editor` | Abre el editor gráfico in-game de cajas y premios. | `excellentcrates.admin.editor` |
| `/crates reload` | Recarga todas las configuraciones y cajas de la carpeta. | `excellentcrates.admin.reload` |

---

## 🧩 Placeholders PlaceholderAPI (PAPI)
* `%excellentcrates_keys_<crate_id>%`: Cantidad de llaves que posee el jugador para la caja indicada.
* `%excellentcrates_crates_opened_total%`: Total de cajas abiertas históricamente por el usuario.
* `%excellentcrates_crate_name_<crate_id>%`: Nombre con formato de la caja especificada.

---

## 🛡️ Prevención de Dupes, Exploits & Modos de Fallo
1. **Falsificación de Llaves Físicas (Anvil Renaming Dupe)**:
   - **Vulnerabilidad**: Jugadores renombrando ganchos de hilo (`TRIPWIRE_HOOK`) para engañar al detector de llaves.
   - **Solución**: ExcellentCrates comprueba las llaves mediante `PersistentDataContainer` (clave de namespace interna criptográficamente única) y no únicamente por el nombre visible.
2. **Apertura Doble en Bloque por Spam de Clics**:
   - Bloqueo de interacción inmediata: una vez consumida la llave y comenzada la animación, el cofre entra en estado `LOCKED` para ese jugador impidiendo que se consuma más de una llave a la vez o se glitchee la entrega de recompensas.
3. **Crash / Desconexión en Mitad de la Animación**:
   - Si un jugador sufre un desync o desconexión durante la ruleta, el plugin procesa y entrega el premio directamente al inventario persistente o al buzón de recompensas sin perder la llave.
4. **Comandos de Recompensa con Caracteres Peligrosos**:
   - Excelente sanitización de `%player%` en la ejecución de comandos de consola evitando inyecciones de comandos maliciosos.

---

## Referencias Cruzadas
- [[wiki/entities/thundermc/economy-progression/playerpoints|PlayerPoints]]
- [[wiki/concepts/monetizacion-modelo-negocio|Modelo MonetizaciÃ³n]]
- [[wiki/entities/thundermc/gameplay-mechanics/executableitems|ExecutableItems]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
