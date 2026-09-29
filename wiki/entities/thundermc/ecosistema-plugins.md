# 🌐 Ecosistema de Plugins — ThunderMC Survival (1.21.11)

Documento maestro con el mapeo técnico, responsabilidades e integración de los plugins del servidor Survival.

- **Servidor**: [[wiki/entities/thundermc|ThunderMC]]
- **Arquitectura Maestra**: [[wiki/synthesis/thundermc-master-synthesis|Síntesis Maestra ThunderMC]]
- **Hardware y Entorno**: [[wiki/entities/thundermc/infraestructura-hardware|Infraestructura Hardware]]
- **Documentación Externa**: [[wiki/entities/thundermc/enlaces-wikis-oficiales|Enlaces a Wikis Oficiales]]
- **Estándares de Interfaz**: [[wiki/entities/thundermc/estilo-menus-ui|Estilo Menús UI]] | [[wiki/entities/thundermc/iconos-compatibles-ui|Iconos Compatibles UI]] | [[wiki/concepts/deluxemenus_standards|Estándares DeluxeMenus]]

---

## 🏛️ 1. Infraestructura Core & Red
- **[[wiki/entities/thundermc/core-infrastructure/luckperms|LuckPerms]] (5.5.42)**: Motor de permisos jerárquico y cálculo de grupos/pesos.
- **[[wiki/entities/thundermc/core-infrastructure/vault|Vault]]**: API unificadora para economía y permisos.
- **[[wiki/entities/thundermc/core-infrastructure/placeholderapi|PlaceholderAPI]] (2.12.2)**: Puente de reemplazo de variables en tiempo de ejecución.
- **[[wiki/entities/thundermc/core-infrastructure/fawe|FastAsyncWorldEdit (FAWE)]] (2.15.0)**: Edición de terreno asíncrona optimizada para Paper 1.21.
- **[[wiki/entities/thundermc/core-infrastructure/multiverse-core|Multiverse-Core]] (5.5.2)**: Gestión multi-mundo y control de generadores.
- **[[wiki/entities/thundermc/core-infrastructure/viaversion|ViaVersion]] (5.11.0)**: Compatibilidad multi-versión cliente-servidor.
- **[[wiki/entities/thundermc/core-infrastructure/floodgate|Floodgate]]**: Autenticación y acceso crossplay para jugadores de Minecraft Bedrock.
- **[[wiki/entities/thundermc/core-infrastructure/voicechat|Simple Voice Chat]] (2.6.21)**: Chat de voz posicional/proximidad UDP.
- **[[wiki/entities/thundermc/core-infrastructure/tab|TAB]] (5.5.0)**: Nametags, Tablist y Scoreboard optimizado vía packets.
- **[[wiki/entities/thundermc/core-infrastructure/plan|Plan (Player Analytics)]] (5.8-b3579)**: Analítica de rendimiento, retención y actividad de jugadores.
- **[[wiki/entities/thundermc/core-infrastructure/fancyholograms|FancyHolograms]]**: Displays flotantes optimizados con TextDisplays.
- **[[wiki/entities/thundermc/core-infrastructure/fancynpcs|FancyNpcs]]**: NPCs estáticos y de interacción basados en paquetes.

---

## 💰 2. Economía, Tiendas y Comercio
- **[[wiki/entities/thundermc/economy-progression/shopguiplus|ShopGUIPlus]] (1.113.0) + `SellGUI` (1.1.8)**: Tienda oficial del servidor (admin shop) y venta masiva.
- **[[wiki/entities/thundermc/economy-progression/quickshop-hikari|QuickShop-Hikari]] (6.2.0.11)**: Tiendas físicas en cofres creadas por usuarios.
- **[[wiki/entities/thundermc/economy-progression/zelauction|ZelAuction]] (1.4-rc.1)**: Casa de subastas global (`/ah`).
- **[[wiki/entities/thundermc/economy-progression/jobs-reborn|Jobs Reborn]] (5.2.6.6)**: Motor de profesiones e inyección de dinero orgánico.
- **[[wiki/entities/thundermc/economy-progression/playerpoints|PlayerPoints]] (3.3.4)**: Economía secundaria / Moneda premium.
- **[[wiki/entities/thundermc/economy-progression/excellentcrates|ExcellentCrates]] (6.6.1)**: Cajas de recompensas animadas con llaves virtuales.
- **[[wiki/entities/thundermc/economy-progression/minigames-afk-gambling|AxAFKZone & Gambling]]**: Zona AFK y minijuegos de apuestas (DeluxeCoinflip / GambleBarPro).

---

## ⚔️ 3. Jugabilidad, RPG y Mazmorras
- **[[wiki/entities/thundermc/gameplay-mechanics/mythicmobs|MythicMobs]] (5.11.2)**: Creación de jefes, habilidades personalizadas y mobs de mazmorras.
- **[[wiki/entities/thundermc/gameplay-mechanics/executableitems|ExecutableItems]] (7.26.5.17)**: Armas, armaduras y herramientas legendarias con habilidades activas/pasivas.
- **[[wiki/entities/thundermc/gameplay-mechanics/itemedit|ItemEdit]] (3.7.8)**: Ajuste directo de NBT, nombres y lore.
- **[[wiki/entities/thundermc/gameplay-mechanics/excellentenchants|ExcellentEnchants]] (5.4.1)**: Encantamientos adicionales para enriquecer el meta de combate.
- **[[wiki/entities/thundermc/gameplay-mechanics/catamines|CataMines]] (2.5.11)**: Minas progresivas por rangos y zona PvP.
- **[[wiki/entities/thundermc/gameplay-mechanics/betterrtp|BetterRTP]] (3.6.13)**: Teletransporte aleatorio eficiente en mundos Survival/Recursos.
- **[[wiki/entities/thundermc/gameplay-mechanics/ultimatekoth|UltimateKoth]] (2.25.2)**: Eventos de captura de zona PvP (King of the Hill).
- **[[wiki/entities/thundermc/gameplay-mechanics/gsit|GSit]] (3.4.2)**: Animaciones de descanso (sentarse/tumbarse).
- **[[wiki/entities/thundermc/composicion-minas|Composición de Minas]]**: Distribución porcentual y balance de bloques por rango.
- **[[wiki/entities/thundermc/mobs-mazmorras|Mobs y Jefes de Mazmorras]]**: Especificaciones de bosses (Araña Reina, Cérbero, etc.).

---

## 🛡️ 4. Protección, Seguridad y Moderación
- **[[wiki/entities/thundermc/world-protection/worldguard|WorldGuard]] (7.0.15) + `WorldGuardExtraFlags`**: Protección de spawn, minas y zonas seguras.
- **[[wiki/entities/thundermc/world-protection/protectionstones|ProtectionStones]] (2.10.6)**: Sistema de protección de parcelas para jugadores.
- **[[wiki/entities/thundermc/world-protection/pvpmanager|PvPManager]] (4.1.68)**: Control de estado PvP y anti-desconexión en combate.
- **[[wiki/entities/thundermc/world-protection/coreprotect|CoreProtect]] (CE 24.0)**: Registro forense de transacciones, cofres y bloques.
- **[[wiki/entities/thundermc/world-protection/inventoryrollbackplus|InventoryRollbackPlus]] (1.8.3)**: Restauración de inventarios por muertes o bugs.
- **[[wiki/entities/thundermc/world-protection/litebans|LiteBans]]**: Sistema centralizado de sanciones y moderación.

---

## 👥 5. Chat, Clanes y Social
- **[[wiki/entities/thundermc/chat-social/zelchat|ZelChat]] (2.0.0-pre-18)**: Canales de chat, prefijos y menciones interactivas.
- **[[wiki/entities/thundermc/chat-social/zelteams|ZelTeams]] (3.3.4)**: Sistema de clanes, alianzas y banco de equipo.
- **[[wiki/entities/thundermc/chat-social/playerwarps|PlayerWarps]] (7.10.0)**: Warps públicos creados por la comunidad.
- **[[wiki/entities/thundermc/chat-social/alonsotags|AlonsoTagsPro]] (2.3-BETA)**: Cosméticos de tags y colores de mensaje.

---

## ⚙️ 6. Plugins Custom Propios
- **[[wiki/entities/thundermc/custom-plugins/plugins-custom|Plugins Custom ThunderMC]]**: Especificación de EnderChestPlus, RankUp y ValyrTutorial.
