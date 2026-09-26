# 🌐 Ecosistema de Plugins — ThunderMC Survival (1.21.11)

Documento maestro con el mapeo técnico, responsabilidades e integración de los plugins del servidor Survival.

---

## 🏛️ 1. Infraestructura Core & Red
- **`LuckPerms` (5.5.42)**: Motor de permisos jerárquico.
- **`Vault`**: API unificadora para economía y permisos.
- **`PlaceholderAPI` (2.12.2)**: Puente de reemplazo de variables.
- **`FastAsyncWorldEdit` (2.15.0)**: Edición de terreno asíncrona optimizada para Paper 1.21.
- **`Multiverse-Core` (5.5.2)**: Gestión multi-mundo.
- **`ViaVersion` (5.11.0)**: Compatibilidad multi-versión.
- **`Floodgate`**: Acceso crossplay para jugadores de Minecraft Bedrock.
- **`Simple Voice Chat` (2.6.21)**: Chat de voz posicional/proximidad.
- **`TAB` (5.5.0)**: Nametags, Tablist y Scoreboard optimizado vía packets.
- **`Plan` (5.8-b3579)**: Analítica de rendimiento, retención y actividad de jugadores.

---

## 💰 2. Economía, Tiendas y Comercio
- **`ShopGUIPlus` (1.113.0) + `SellGUI` (1.1.8)**: Tienda oficial del servidor (admin shop) y venta masiva.
- **`QuickShop-Hikari` (6.2.0.11)**: Tiendas físicas en cofres creadas por usuarios.
- **`ZelAuction` (1.4-rc.1)**: Casa de subastas global (`/ah`).
- **`Jobs Reborn` (5.2.6.6)**: Motor de profesiones e inyección de dinero orgánico.
- **`AxAFKZone` (1.10.1)**: Recompensas automáticas en zona AFK.
- **`PlayerPoints` (3.3.4)**: Economía secundaria / Moneda premium.
- **`DeluxeCoinflip` (2.11.2) / `GambleBarPro` (2.2.0)**: Minijuegos de apuestas y bar de efectos.

---

## ⚔️ 3. Jugabilidad, RPG y Mazmorras
- **`MythicMobs` (5.11.2)**: Creación de jefes, habilidades personalizadas y mobs de mazmorras.
- **`ExecutableItems` (7.26.5.17)**: Armas, armaduras y herramientas legendarias con habilidades activas y pasivas.
- **`ItemEdit` (3.7.8)**: Ajuste directo de NBT, nombres y lore.
- **`ExcellentEnchants` (5.4.1)**: Encantamientos adicionales para enriquecer el meta de combate.
- **`ExcellentCrates` (6.6.1)**: Cajas de recompensas animadas.
- **`CataMines` (2.5.11)**: Minas progresivas por rangos.
- **`SilkSpawners_v2`**: Recogida e intercambio de generadores de monstruos.
- **`BetterRTP` (3.6.13)**: Teletransporte aleatorio eficiente en los mundos Survival/Recursos.
- **`UltimateKoth` (2.25.2)**: Eventos de captura de zona PvP (King of the Hill).

---

## 🛡️ 4. Protección, Seguridad y Moderación
- **`WorldGuard` (7.0.15) + `WorldGuardExtraFlags`**: Protección de spawn, minas y zonas seguras.
- **`ProtectionStones` (2.10.6) + `ProtectionMenu` (1.0)**: Sistema de protección de parcelas para jugadores.
- **`PvPManager` (4.1.68)**: Control de estado PvP y anti-desconexión en combate.
- **`CoreProtect` (CE 24.0)**: Registro forense de transacciones, cofres y bloques.
- **`InventoryRollbackPlus` (1.8.3)**: Restauración de inventarios por muertes o bugs.
- **`LiteBans`**: Sistema centralizado de sanciones y moderación.
- **`EasyCommandBlocker` (1.18.1)**: Ocultación de plugins y bloqueo de comandos sensibles.
- **`Insights` (6.20.2)**: Límites de tiles, tolvas y redstone por chunk para proteger el MSPT.

---

## 👥 5. Chat, Clanes y Social
- **`ZelChat` (2.0.0-pre-18)**: Canales de chat, prefijos y menciones.
- **`ZelTeams` (3.3.4)**: Sistema de clanes, alianzas y banco de equipo.
- **`ChatGames` (1.2.1)**: Eventos automáticos de preguntas/respuestas en el chat.
- **`AlonsoTagsPro` (2.3-BETA) / `ChatColor2` (1.15.1)**: Cosméticos de tags y colores de mensaje.
- **`PlayerWarps` (7.10.0)**: Warps públicos creados por la comunidad.
- **`GSit` (3.4.2)**: Animaciones de descanso (sentarse/tumbarse).
