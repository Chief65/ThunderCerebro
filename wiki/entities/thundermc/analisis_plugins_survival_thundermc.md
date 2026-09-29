# 🛡️ Auditoría Exhaustiva de Plugins — Servidor Survival ThunderMC (1.21.11)

**Fecha de Ejecución**: 27 de Agosto de 2026  
**Auditor**: Hanush (Cerebro Digital & Analista Técnico de ThunderStudios)  
**Servidor**: Survival ThunderMC (Host: `MIA-251006.bloom.host:2022`, Paper 1.21.11 build 126)  
**Entorno de Documentación**: `ThunderCerebro/wiki/entities/thundermc/`

---

## 📊 1. Resumen Ejecutivo del Ecosistema

- **Total de JARs Activos**: 74
- **Total de JARs Desactivados (`.dis`)**: 16
- **Total de Carpetas de Configuración en `plugins/`**: 89
- **Plugins Custom / Exclusivos Detectados**: 4 (`EnderChestPlus`, `RankUp`, `ValyrTutorial`, `ThunderMines`)
- **Bibliotecas / Bridge Cores**: 8 (`Vault`, `PlaceholderAPI`, `SCore`, `MythicLib`, `CMILib`, `nightcore`, `AxAPI`, `item-nbt-api`)

---

- **Parte de**: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]] | [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra]]
## 📦 2. Inventario Completo de Plugins Activos y Versiones

| # | Archivo JAR | Plugin / Sistema | Versión Detectada | Categoría | Estado / Propósito |
|---|---|---|---|---|---|
| 1 | `Advanced-Portals-Spigot-2.7.1.jar` | AdvancedPortals | 2.7.1 | Infraestructura / Navegación | Portales custom sin coste de redstone |
| 2 | `AlonsoTagsPro-v2.3-BETA-PRO (1).jar` | AlonsoTagsPro | 2.3-BETA-PRO | Cosméticos | Tags sobre la cabeza y chat |
| 3 | `AxAFKZone-1.10.1.jar` | AxAFKZone | 1.10.1 | Economía / Retención | Zona AFK con recompensas temporizadas |
| 4 | `BetterRTP-3.6.13.jar` | BetterRTP | 3.6.13 | Jugabilidad / Teletransporte | Teletransporte aleatorio seguro |
| 5 | `CMILib1.5.9.9 (1).jar` | CMILib | 1.5.9.9 | Dependencia / Core | Biblioteca requerida por Jobs Reborn |
| 6 | `CataMines-2.5.11 (1).jar` | CataMines | 2.5.11 | Minas / Progresión | Minas progresivas y regeneración de bloques |
| 7 | `ChatColor2-1.15.1.jar` | ChatColor2 | 1.15.1 | Chat / Cosmético | Selector de color en chat por menú |
| 8 | `ChatGames-v1.2.1.jar` | ChatGames | 1.2.1 | Social / Eventos | Trivias y desafíos matemáticos en chat |
| 9 | `CommandPanels.jar` | CommandPanels | N/A | GUI / Menús | Motor de menús interactivos secundario |
| 10 | `ConditionalEvents-4.77.1.jar` | ConditionalEvents | 4.77.1 | Automatización | Motor de triggers y scripts por eventos |
| 11 | `CoreProtect-CE-24.0.jar` | CoreProtect | 24.0 (Community) | Seguridad / Rollback | Logger de bloques, cofres y transacciones |
| 12 | `DailyRewardsPlus-1.4.8.jar` | DailyRewardsPlus | 1.4.8 | Retención | Recompensas diarias acumulativas |
| 13 | `DeluxeCoinflip-2.11.2.jar` | DeluxeCoinflip | 2.11.2 | Economía / Minijuegos | Apuestas 1v1 cara o cruz |
| 14 | `DeluxeMenus-1.14.1-Release (1).jar` | DeluxeMenus | 1.14.1-Release | GUI / Menús | Motor principal de menús y paneles |
| 15 | `EasyCommandBlocker-1.18.1.jar` | EasyCommandBlocker | 1.18.1 | Seguridad | Bloqueo de comandos `/pl`, `/ver`, etc. |
| 16 | `Elevator.jar` | Elevator | N/A | Mecánica | Elevadores instantáneos en saltos/agacharse |
| 17 | `EnderChestPlus-1.0.jar` | EnderChestPlus | 1.0 (Custom) | Almacenamiento | Enderchests ampliados / páginas múltiples |
| 18 | `EssentialsX-2.21.2.jar` | EssentialsX | 2.21.2 | Core Base | Economía básica, warps, homes, moderación |
| 19 | `EssentialsXSpawn-2.21.2.jar` | EssentialsXSpawn | 2.21.2 | Core Base | Manejo del spawn de jugadores |
| 20 | `ExcellentCrates-6.6.1.jar` | ExcellentCrates | 6.6.1 | Economía / Cajas | Cajas de recompensas animadas con llaves |
| 21 | `ExcellentEnchants-5.4.1.jar` | ExcellentEnchants | 5.4.1 | Combate / RPG | Encantamientos vanilla-plus custom |
| 22 | `ExecutableItems_Prem-7.26.5.17.jar` | ExecutableItems Premium | 7.26.5.17 | RPG / Ítems | Ítems con habilidades y cooldowns |
| 23 | `FancyGlow-2.10.3.jar` | FancyGlow | 2.10.3 | Cosméticos | Resplandor/Glow de colores en jugadores |
| 24 | `FancyHolograms-2.9.1.jar` | FancyHolograms | 2.9.1 | Display / Entidades | Hologramas basados en display entities |
| 25 | `FancyNpcs-2.9.2.349.jar` | FancyNpcs | 2.9.2.349 | NPCs / Interactivos | NPCs ligeros vía display entities y packets |
| 26 | `FastAsyncWorldEdit-Paper-2.15.0.jar` | FAWE (WorldEdit) | 2.15.0 | Administración / Build | Edición masiva asíncrona de bloques |
| 27 | `GSit-3.4.2.jar` | GSit | 3.4.2 | Mecánica / Inmersión | Sentarse, tumbarse, crawl y pose |
| 28 | `GambleBarPro-2.2.0.jar` | GambleBarPro | 2.2.0 | Economía / Casino | Bar de bebidas y ruleta de pociones/efectos |
| 29 | `Insights-6.20.2.jar` | Insights | 6.20.2 | Rendimiento / Control | Límites de tiles, redstone y entidades por chunk |
| 30 | `InventoryRollbackPlus-1.8.3.jar` | InventoryRollbackPlus | 1.8.3 | Seguridad | Guardado histórico de inventarios y muertes |
| 31 | `ItemEdit-3.7.8.jar` | ItemEdit | 3.7.8 | Creación / Ítems | Editor in-game de NBT, lore y atributos |
| 32 | `Jobs5.2.6.6.jar` | Jobs Reborn | 5.2.6.6 | Economía / Trabajos | Sistema de profesiones y recompensas por acción |
| 33 | `LiteBans.jar` | LiteBans | N/A (Premium) | Moderación | Sistema global de sanciones y baneos |
| 34 | `LootChests-1.11.jar` | LootChests | 1.11 | Mazmorras / Eventos | Cofres de botín reabastecibles en mundo |
| 35 | `LuckPerms-Bukkit-5.5.42.jar` | LuckPerms | 5.5.42 | Permisos / Seguridad | Sistema de permisos centralizado |
| 36 | `MythicLib-dist-1.7.1-20260312.111127-87.jar` | MythicLib | 1.7.1 (Snapshot) | Dependencia RPG | Motor de stats de MMO/Mythic |
| 37 | `MythicMobs-5.11.2.jar` | MythicMobs | 5.11.2 | Jefes / Mazmorras | Mobs customizados, bosses y habilidades |
| 38 | `PetNameFix-1.0.5.jar` | PetNameFix | 1.0.5 | Bugfix | Corrección de nombres largos de mascotas |
| 39 | `PlaceholderAPI-2.12.2.jar` | PlaceholderAPI (PAPI) | 2.12.2 | Core Bridge | Motor universal de variables `%papi%` |
| 40 | `Plan-5.8-build-3579.jar` | Plan Analytics | 5.8-b3579 | Analítica | Métricas de retención, MSPT y jugadores |
| 41 | `PlayerKits2-1.22.2.jar` | PlayerKits2 | 1.22.2 | Kits / Progresión | Kits con cooldown e interfaz visual |
| 42 | `PlayerPoints-3.3.4.jar` | PlayerPoints | 3.3.4 | Moneda Secundaria | Puntos premium / tokens de tienda |
| 43 | `PlayerWarps 7.10.0.jar` | PlayerWarps | 7.10.0 | Social / Economía | Warps creados y valorados por usuarios |
| 44 | `ProtectionMenu-1.0.jar` | ProtectionMenu | 1.0 | Menús Protecciones | GUI wrapper para ProtectionStones |
| 45 | `ProtectionStones-2.10.6.jar` | ProtectionStones | 2.10.6 | Reclamaciones | Bloques de protección basados en WorldGuard |
| 46 | `PvPManager-4.1.68.jar` | PvPManager | 4.1.68 | Combate | Anti-combat log, tagger y toggle pvp |
| 47 | `QuickShop-Hikari-6.2.0.11.jar` | QuickShop Hikari | 6.2.0.11 | Economía / Tiendas | Tiendas de cofres para jugadores (Hikari) |
| 48 | `RankUp-1.0.jar` | RankUp (Ranks) | 1.0 (Custom) | Progresión | Subida de rangos por requisitos de dinero/stats |
| 49 | `SCore-5.26.5.17.jar` | SCore (Ssomar Core) | 5.26.5.17 | Dependencia | Motor común de la suite Ssomar |
| 50 | `ShopGUIPlus-1.113.0.jar` | ShopGUIPlus | 1.113.0 | Economía / Admin Shop | Tienda virtual del servidor `/shop` |
| 51 | `ShopGUIPlus-SellGUI-1.1.8-all.jar` | ShopGUIPlus SellGUI | 1.1.8 | Economía | Menú de venta rápida en bloque `/sellgui` |
| 52 | `Shopkeepers-2.26.1 (1).jar` | Shopkeepers | 2.26.1 | Economía / Aldeanos | Aldeanos comerciantes fijos |
| 53 | `SilkSpawners_v2.jar` | SilkSpawners v2 | N/A | Economía / Grinding | Minado y recogida de spawners con toque de seda |
| 54 | `SkinsRestorer.jar` | SkinsRestorer | N/A | Cosmético / No-Premium | Carga de skins para usuarios Bedrock y Java |
| 55 | `TAB v5.5.0 (1).jar` | TAB (NEZNAMY) | 5.5.0 | Interfaz / Scoreboard | Tablist, Nametags, Scoreboard y BossBar |
| 56 | `UltimateKoth-2.25.2.jar` | UltimateKoth | 2.25.2 | PvP / Eventos | Rey de la Colina automatizado |
| 57 | `ValyrTutorial-3.0.jar` | ValyrTutorial | 3.0 (Custom) | Onboarding | Guía/tutorial interactivo de bienvenida |
| 58 | `Vault.jar` | Vault | 1.7.3+ | API Economía/Perms | Puente universal entre plugins de economía |
| 59 | `ViaVersion-5.11.0.jar` | ViaVersion | 5.11.0 | Compatibilidad | Permite conectar a clientes de versiones superiores |
| 60 | `VoidGen-2.3.4.jar` | VoidGen | 2.3.4 | Generación | Generador de mundos vacíos |
| 61 | `VoidSpawn.jar` | VoidSpawn | N/A | Jugabilidad | Teletransporte al caer al vacío del spawn |
| 62 | `WorldGuardExtraFlags.jar` | WorldGuardExtraFlags | N/A | Protección | Flags adicionales para regiones WorldGuard |
| 63 | `ZelAuction-1.4-rc.1.jar` | ZelAuction | 1.4-rc.1 | Economía / Subastas | Casa de subastas `/ah` para jugadores |
| 64 | `ZelTeams-3.3.4.jar` | ZelTeams | 3.3.4 | Clanes / Equipos | Creación de clanes, chat de team y banco |
| 65 | `floodgate-spigot (6).jar` | Floodgate | 2.2.3+ | Crossplay | Autenticación de jugadores Bedrock vía Geyser |
| 66 | `item-nbt-api-plugin-2.15.7 (1).jar` | NBTAPI | 2.15.7 | Dependencia | Manipulación directa de tags NBT de items |
| 67 | `multiverse-core-5.5.2.jar` | Multiverse-Core | 5.5.2 | Gestión de Mundos | Carga, descarga y gestión de múltiples dimensiones |
| 68 | `nightcore-2.14.0.jar` | nightcore | 2.14.0 | Dependencia | Framework base de NightExpress (Crates/Enchants) |
| 69 | `packetevents-spigot-2.13.0.jar` | packetevents | 2.13.0 | Dependencia Red | API de inyección de paquetes de red |
| 70 | `tebex-bukkit-2.4.2-19b0f2a.jar` | Tebex (Buycraft) | 2.4.2 | Monetización | Conexión con tienda web de pagos reales |
| 71 | `topper-spigot-plugin-4.7.0-shaded.jar` | Topper | 4.7.0 | Leaderboards | Cálculos de rankings y tops de variables |
| 72 | `voicechat-bukkit-2.6.21.jar` | Simple Voice Chat | 2.6.21 | Inmersión / Voz | Chat de proximidad por voz |
| 73 | `worldguard-bukkit-7.0.15.jar` | WorldGuard | 7.0.15 | Protección Base | Protección de regiones, spawn y reglas de mundo |
| 74 | `zelchat-2.0.0-pre-18.jar` | ZelChat | 2.0.0-pre-18 | Chat / Formato | Formateador de rangos en chat y canales |

---

## 🛑 3. Lista de Plugins Desactivados (`.dis`) y Diagnóstico de Archivo

1. **`CataMines-2.5.11.dis`**: Duplicado del activo `CataMines-2.5.11 (1).jar`. *(Eliminable)*.
2. **`Citizens (1).dis`**: Desactivado a favor de `FancyNpcs` (decisión correcta para ahorrar TPS de entidades físicas).
3. **`CommandWhitelist-Bukkit-2.12.0.dis`**: Reemplazado por `EasyCommandBlocker`.
4. **`EnderChestPlus-1.0.dis`**: Compilación antigua del custom `EnderChestPlus`.
5. **`ItemTag-3.7.6.dis`**: Desactivado (conflictivo con sistema NBT de ItemEdit).
6. **`LibsDisguises-11.0.16-Premium.dis` & `11.0.18-Premium (1).dis`**: Desactivados por consumo y dependencia de ProtocolLib.
7. **`MMOItems-6.10.1-20260312.111212-50.dis`**: Desactivado; el servidor migró a `ExecutableItems` + `ItemEdit`. *(Nota: `MythicLib` sigue activo sin él)*.
8. **`ProtectionMenu-1.0.dis`**: Compilación anterior de `ProtectionMenu-1.0.jar`.
9. **`Shopkeepers-2.26.1.dis`**: Duplicado del JAR activo con índice (1).
10. **`ThunderMines-1.9.dis`**: Plugin custom de minas reemplazado por `CataMines`.
11. **`ValyrTutorial-1.0.dis`**: Versión 1.0 superseded por `ValyrTutorial-3.0.jar`.
12. **`cAFKZone.dis`**: Sustituido por `AxAFKZone-1.10.1.jar`.
13. **`grimac-bukkit-2.3.73.dis`**: Anticheat desactivado temporalmente.
14. **`justRTP-3.5.4.dis`**: Sustituido por `BetterRTP-3.6.13.jar`.
15. **`zSchedulers-1.0.9.dis`**: Desactivado; sustituido por tareas en `ConditionalEvents`.

---

## 🛠️ 4. Análisis Específico de Plugins Custom

1. **`EnderChestPlus-1.0.jar`**:
   - **Función**: Gestor de baúl del fin expandido con páginas y permisos (`enderchestplus.page.X`).
   - **Riesgo Operativo**: Verificar persistencia de NBT complejo (items de ExecutableItems) al guardar en disco para evitar reseteos de NBT o dupes en desconexión.
2. **`RankUp-1.0.jar` (Ranks)**:
   - **Función**: Sistema de progresión escalonada de rangos con cobro Vault y asignación de grupos LuckPerms (`lp user %player% parent set/add`).
   - **Riesgo Operativo**: Bloquear spam de clic en GUI para impedir ejecución concurrente de subida de rango múltiple.
3. **`ValyrTutorial-3.0.jar`**:
   - **Función**: Sistema de onboarding inmersivo paso a paso para usuarios novatos.
   - **Riesgo Operativo**: Comprobar compatibilidad con Floodgate (clientes Bedrock en móviles) para evitar bloqueos de pantalla o cinemáticas rotas.
4. **`ThunderMines-1.9.dis` (Obsoleto)**:
   - Plugin custom anterior para regeneración de menas; totalmente absorbido y superseded por `CataMines`.

---

## ⚖️ 5. Análisis de Armonía, Redundancias y Rendimiento

### 🔴 Redundancias y Cargas Innecesarias Detectadas:
1. **Doble Motor de Menús (`DeluxeMenus` vs. `CommandPanels`)**:
   - Posees ambos activos. Mantener dos parsers de GUI consume memoria adicional y confunde la administración. **Recomendación**: Centralizar todo en `DeluxeMenus 1.14.1`.
2. **Dependencia Huérfana (`MythicLib` sin `MMOItems`)**:
   - `MMOItems` está desactivado (`.dis`), pero `MythicLib-dist-1.7.1.jar` sigue activo. Si solo usas `MythicMobs`, este último no requiere MythicLib (a menos que uses mecánicas de daño específicas de MythicCraft). Evaluar si genera sobrecarga de stats en memoria.
3. **Residuos de Archivos en `plugins/`**:
   - El archivo `CoreProtect-2026-08-04T081318Z.tar.gz` pesa **2.51 GB** y reside dentro de la carpeta `plugins/`. Debe moverse fuera de la raíz del servidor para evitar lentitud en lecturas de directorio y backups automáticos.

### 🟢 Aspectos Positivos de Rendimiento y Arquitectura:
- **`FancyNpcs` + `FancyHolograms`**: La migración de HolographicDisplays/Citizens a Display Entities de 1.21 evita ticks de IA de entidades, manteniendo el MSPT del servidor bajo control.
- **`AxAFKZone` + `BetterRTP`**: Excelente elección frente a alternativas antiguas; usan caching de chunks y colas asíncronas para no congelar el hilo principal.
- **`QuickShop-Hikari`**: Utiliza base de datos optimizada y transacciones asíncronas, protegiendo contra dupes habituales de QuickShop Clásico.

---

## 🗂️ 6. Organización en el Cerebro Digital (`ThunderCerebro`)

Se ha estructurado la carpeta centralizada:
`ThunderCerebro/wiki/entities/thundermc/` con las siguientes subcarpetas y notas detalladas:
- `core-infrastructure/`: Vault, LuckPerms, ViaVersion, Multiverse, FAWE, TAB, etc.
- `economy-progression/`: QuickShop-Hikari, ShopGUIPlus, Jobs Reborn, ExcellentCrates, PlayerPoints.
- `gameplay-mechanics/`: MythicMobs, ExecutableItems, ExcellentEnchants, BetterRTP, GSit.
- `chat-social/`: ZelChat, ZelTeams, ChatGames, AlonsoTagsPro.
- `world-protection/`: WorldGuard, ProtectionStones, CoreProtect, PvPManager.
- `custom-plugins/`: EnderChestPlus, RankUp, ValyrTutorial.
- `disabled-orphans/`: Registro de plugins `.dis` y plan de limpieza.

---

## Referencias Cruzadas
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
- [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra ThunderMC]]
