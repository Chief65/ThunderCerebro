# 📖 PlaceholderAPI (2.12.2+)

- **Categoría**: Core Bridge / Universal String & Variable Interpolation Engine
- **Servidor**: ThunderMC Survival 1.21.11 (Paper build 126+)
- **Desarrollador**: HelpChat (ExtendedClip / Glare)
- **Dependencias**: Ninguna (Bridge Core Universal)
- **Integraciones Clave**: TAB, DeluxeMenus, ConditionalEvents, FancyHolograms, ZelChat, ShopGUI+, BetterRTP, Topper

---

## 🎯 1. Propósito & Visión General
**PlaceholderAPI (PAPI)** es la columna vertebral de interoperabilidad e intercambio de datos dinámicos entre plugins en el ecosistema Bukkit/Paper. Proporciona una API centralizada donde cualquier plugin puede registrar "Expansiones" que transforman identificadores estructurados `%identificador_parametro%` en valores calculados en tiempo real (estadísticas de juego, balances, ping, rangos, coordenadas, datos de clanes, etc.).

---

## 🏗️ 2. Arquitectura Interna & Ciclo de Parseo

```mermaid
graph TD
    ClientCaller[Plugins Consumidores: TAB, DeluxeMenus, Hologramas] -->|PlaceholderAPI.setPlaceholders(player, string)| PAPIEngine[PlaceholderAPI Core Parser]
    PAPIEngine -->|Regex Match: %([a-zA-Z0-9_]+)%| TokenExtractor[Token & Identifier Extractor]
    TokenExtractor -->|Consulta Mapa de Expansiones| ExpansionRegistry[Registered Expansions Map en RAM]
    ExpansionRegistry -->|Invocación de onPlaceholderRequest| CustomExpansion[Expansión: Vault / LuckPerms / Server / Math]
    CustomExpansion -->|Retorna String / Null| TokenExtractor
    TokenExtractor -->|Sustitución en Cadena| FinalString[Texto Final Renderizado]
```

### 2.1 Componentes Principales
1. **`PlaceholderExpansion` Class**:
   - Clase base que todo desarrollador o plugin extiende implementando `onPlaceholderRequest(Player player, String params)`.
   - Propiedades obligatorias: `getIdentifier()`, `getAuthor()`, `getVersion()`, `persist()` (mantiene la expansión cargada al ejecutar `/papi reload`).
2. **eCloud (Expansion Cloud)**:
   - Repositorio remoto centralizado (`api.extendedclip.com`) que permite descargar, actualizar e instalar módulos de soporte para plugins externos en caliente mediante comandos in-game sin necesidad de reiniciar el servidor.
3. **Mecanismo de Parseo Recursivo y Relacional**:
   - **Placeholders Simples**: `%player_name%`, `%vault_eco_balance%`.
   - **Placeholders Anidados**: `%javascript_is_vip_{player_name}%`.
   - **Placeholders Relacionales (`%rel_...%`)**: Permite comparar dos jugadores (e.g. `%rel_factionsuuid_relation%` para calcular si dos usuarios son aliados, enemigos o neutrales para colorear nametags).

---

## ⌨️ 3. Comandos Completos y Sintaxis

| Comando | Alias | Argumentos | Descripción | Nivel de Acceso |
|---|---|---|---|---|
| `/papi ecloud download` | `/papi download` | `<expansión>` | Descarga e instala una expansión desde el repositorio oficial eCloud. | Admin |
| `/papi ecloud list` | `/papi list` | `all [página]` | Lista todas las expansiones disponibles en la nube. | Admin |
| `/papi ecloud update` | `/papi update` | `<expansión\|all>` | Actualiza las expansiones instaladas a su última versión. | Admin |
| `/papi reload` | Ninguno | Ninguno | Recarga la configuración de PAPI y refresca todas las expansiones registradas. | Admin |
| `/papi parse` | Ninguno | `[jugador] <texto>` | Evalúa y muestra el resultado de parsear una cadena con placeholders en el chat. | Staff / Admin |
| `/papi dump` | Ninguno | Ninguno | Genera un reporte técnico de diagnóstico en Pastebin con el estado del motor. | Admin |
| `/papi info` | Ninguno | `<expansión>` | Muestra información de versión, autor y estado de una expansión específica. | Staff / Admin |

---

## 🔑 4. Árbol de Permisos

| Permiso | Descripción | Por Defecto |
|---|---|---|
| `placeholderapi.admin` | Permite gestionar eCloud, descargas, parseos de test y recargas `/papi`. | `op` / `luckperms.group.admin` |
| `placeholderapi.ecloud` | Permiso para descargar o actualizar expansiones desde eCloud. | `op` |
| `placeholderapi.parse` | Permiso para testear cadenas con `/papi parse`. | `luckperms.group.staff` |
| `placeholderapi.reload` | Permiso para ejecutar `/papi reload`. | `op` |

---

## 🧩 5. Expansiones eCloud Fundamentales en ThunderMC

| Expansión | Comando de Instalación | Variables de Ejemplo |
|---|---|---|
| **Player** | `/papi ecloud download Player` | `%player_name%`, `%player_ping%`, `%player_uuid%`, `%player_gamemode%` |
| **Server** | `/papi ecloud download Server` | `%server_online%`, `%server_ram_used%`, `%server_tps_1%`, `%server_time%` |
| **Vault** | `/papi ecloud download Vault` | `%vault_eco_balance%`, `%vault_prefix%`, `%vault_rank%` |
| **LuckPerms** | `/papi ecloud download LuckPerms` | `%luckperms_primary_group_name%`, `%luckperms_highest_group_by_weight%` |
| **Math** | `/papi ecloud download Math` | `%math_({vault_eco_balance}*0.1)%`, `%math_round_{player_x}%` |
| **Javascript** | `/papi ecloud download Javascript` | Permite crear lógica condicional avanzada en `javascript_placeholders.yml`. |
| **CheckItem** | `/papi ecloud download CheckItem` | `%checkitem_amount_mat:DIAMOND%` (comprueba cantidad de ítems). |

---

## ⚡ 6. Optimización de Rendimiento & Cuellos de Botella

1. **Evitar Parseo Masivo en el Hilo Principal**:
   - Plugins como TAB o Scoreboards no deben consultar placeholders pesados (que hagan queries SQL o iteraciones de inventarios) en intervalos menores a 1 segundo (20 ticks).
2. **Caché en JavaScript Placeholders**:
   - Si se utiliza la expansión JavaScript, evitar bucles `while` o llamadas a APIs pesadas. Limitar las expresiones a evaluaciones lógicas booleanas directas.
3. **Limpieza de Expansiones Huérfanas**:
   - Eliminar carpetas y expansiones de plugins que ya no estén instalados en el servidor para evitar que el regex parser pierda tiempo buscando proveedores inexistentes.

---

## ⚠️ 7. Modos de Fallo, Vulnerabilidades & Exploits en 1.21.11

> [!CAUTION]
> **Exploit de Congelación de Servidor por Placeholders Recursivos**
> Si un placeholder se referencia a sí mismo o genera una llamada cíclica infinita (e.g. `%javascript_test%` que contiene `%javascript_test%`), el hilo principal entrará en `StackOverflowError`, provocando la congelación inmediata del servidor (Paper Watchdog crash).

### Mitigaciones Críticas:
- **Límite de Recursión**: Mantener configurado el parámetro de protección contra bucles infinitos en `config.yml`.
- **Sanitización de Entrada de Usuario**: Nunca permitir que los jugadores envíen texto sin sanitizar que luego sea evaluado por `PlaceholderAPI.setPlaceholders()` en anuncios globales de chat o carteles, para evitar inyección de variables privadas del sistema.
