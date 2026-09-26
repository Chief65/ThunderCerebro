---
name: analisisdelmes
description: >-
  Análisis mensual exhaustivo del servidor Minecraft usando la base de datos del plugin Plan (Player Analytics).
  Se activa con "análisis del mes", "informe mensual", "reporte mensual", "estadísticas del mes",
  "recuento del mes", "analisisdelmes", "métricas mensuales", "cómo va el servidor",
  "progresión del servidor", "crecimiento mensual".
  Genera un informe completo con progresión semana a semana, retención, engagement, rendimiento,
  posicionamiento de mercado y proyecciones.
---

# 📊 AnalisisDelMes — Informe Mensual del Servidor

Al activar este skill, ejecutas un pipeline completo de análisis de datos del servidor Minecraft usando la base de datos SQLite del plugin **Plan (Player Analytics)**. El resultado es un informe ejecutivo con métricas de crecimiento, retención, rendimiento y proyecciones.

---

## 🔧 Requisitos Previos

1. **Base de datos Plan**: Archivo `database.db` del plugin Plan (SQLite). Ubicación típica en el servidor: `plugins/Plan/database.db`
2. **Archivos WAL** (opcionales pero recomendados): `database.db-shm` y `database.db-wal` para datos completos
3. **Node.js**: Disponible en el sistema
4. **better-sqlite3**: Módulo de Node.js (se instala automáticamente si no existe)

---

## 📋 Pipeline de Ejecución

### Paso 1: Obtener la Base de Datos

Preguntar al Sr Ramos dónde está la base de datos. Opciones habituales:
- **Local**: Si ya la descargó manualmente (ej: `C:\Users\tecno\Desktop\TrabajoSucio\database.db`)
- **Remota via SFTP**: Descargar desde el servidor Survival usando el skill `startupsurvival`

```powershell
# Descarga via SFTP (si aplica)
sftp -i "$env:USERPROFILE\.ssh\id_rsa" -P 2022 -o BatchMode=yes ymykh9qy.575c7473@MIA-251006.bloom.host:"plugins/Plan/database.db" "C:\Users\tecno\Desktop\TrabajoSucio\database.db"
```

### Paso 2: Copiar a directorio de trabajo

Copiar los 3 archivos de la DB (`.db`, `.db-shm`, `.db-wal`) al directorio scratch de la conversación actual:

```powershell
$scratch = "<ARTIFACT_DIR>\scratch"
Copy-Item "<RUTA_DB>\database.db" -Destination "$scratch\database.db" -Force
Copy-Item "<RUTA_DB>\database.db-shm" -Destination "$scratch\database.db-shm" -Force -ErrorAction SilentlyContinue
Copy-Item "<RUTA_DB>\database.db-wal" -Destination "$scratch\database.db-wal" -Force -ErrorAction SilentlyContinue
```

### Paso 3: Asegurar dependencias

```powershell
# Verificar/instalar better-sqlite3 en el directorio scratch
cd $scratch
node -e "try { require('better-sqlite3'); } catch(e) { require('child_process').execSync('npm install better-sqlite3', {stdio:'inherit'}); }"
```

### Paso 4: Ejecutar el script de análisis

Ejecutar el script `scripts/full_analysis.js` que está en este skill:

```powershell
node "<SKILL_DIR>\scripts\full_analysis.js" "$scratch\database.db"
```

Si el script no está accesible, **crearlo inline** usando el contenido del archivo `scripts/full_analysis.js` de este skill.

### Paso 5: Generar el informe

Con los datos del output del script, generar un **artefacto Markdown** siguiendo la plantilla en `references/plantilla-informe.md`.

---

## 📐 Esquema de la Base de Datos Plan

Tablas clave y sus columnas relevantes:

### `plan_users` — Registro de jugadores
| Columna | Tipo | Descripción |
|---|---|---|
| id | INTEGER | ID interno |
| uuid | varchar(36) | UUID del jugador |
| registered | bigint | Timestamp de registro (epoch ms) |
| name | varchar(36) | Nombre del jugador |
| times_kicked | INTEGER | Veces kickeado |

### `plan_sessions` — Sesiones de juego
| Columna | Tipo | Descripción |
|---|---|---|
| id | INTEGER | ID de sesión |
| user_id | INTEGER | FK a plan_users.id |
| server_id | INTEGER | FK al servidor |
| session_start | bigint | Inicio de sesión (epoch ms) |
| session_end | bigint | Fin de sesión (epoch ms) |
| mob_kills | INTEGER | Mobs matados en la sesión |
| deaths | INTEGER | Muertes en la sesión |
| afk_time | bigint | Tiempo AFK (ms) |
| join_address_id | INTEGER | FK a dirección de conexión |

### `plan_tps` — Rendimiento del servidor
| Columna | Tipo | Descripción |
|---|---|---|
| server_id | INTEGER | FK al servidor |
| date | bigint | Timestamp (epoch ms) |
| tps | double | Ticks por segundo |
| players_online | INTEGER | Jugadores online |
| cpu_usage | double | Uso de CPU % |
| ram_usage | bigint | RAM en MB |
| entities | INTEGER | Entidades cargadas |
| chunks_loaded | INTEGER | Chunks cargados |
| mspt_average | double | MSPT medio |
| mspt_95th_percentile | double | MSPT percentil 95 |

### `plan_user_info` — Info adicional por jugador
| Columna | Tipo | Descripción |
|---|---|---|
| user_id | INTEGER | FK a plan_users.id |
| join_address | varchar(191) | Dirección usada para conectar |
| registered | bigint | Timestamp de registro |
| banned | boolean | Si está baneado |

### `plan_kills` — PvP kills
| Columna | Tipo | Descripción |
|---|---|---|
| date | bigint | Timestamp del kill |

### `plan_ping` — Latencia
| Columna | Tipo | Descripción |
|---|---|---|
| user_id | INTEGER | FK a plan_users.id |
| min_ping | INTEGER | Ping mínimo |
| max_ping | INTEGER | Ping máximo |

### `plan_world_times` — Tiempo por mundo
| Columna | Tipo | Descripción |
|---|---|---|
| user_id | INTEGER | FK |
| world_id | INTEGER | FK a plan_worlds |
| survival_time | bigint | Tiempo en survival (ms) |
| creative_time | bigint | Tiempo en creative (ms) |

### `plan_worlds` — Mundos
| Columna | Tipo | Descripción |
|---|---|---|
| id | INTEGER | ID del mundo |
| world_name | varchar(100) | Nombre del mundo |

### `plan_version_protocol` — Versiones de los clientes
| Columna | Tipo | Descripción |
|---|---|---|
| uuid | varchar(36) | UUID del jugador |
| protocol_version | INT | Versión del protocolo MC |

---

## 📊 Métricas que se Calculan

### Por Semana
1. **Adquisición**: Jugadores nuevos (registrados esa semana)
2. **Actividad**: Jugadores activos (al menos 1 sesión), jugadores recurrentes
3. **Retención**: % de jugadores de la semana anterior que volvieron
4. **Engagement**: Total sesiones, playtime total, sesión promedio, sesión máxima
5. **AFK**: Tiempo AFK total y % del playtime
6. **Combate**: Mob kills, deaths, PvP kills
7. **Concurrencia**: Pico y media de jugadores simultáneos
8. **Rendimiento**: TPS medio/mínimo, MSPT medio/P95, CPU, RAM, entidades, chunks
9. **Horas pico**: Top 3 horas con más sesiones

### Globales
10. **Bounce rate**: % jugadores con 1 sola sesión
11. **Distribución de sesiones**: Buckets (1, 2-5, 6-10, 11-25, 26-50, 51-100, 100+)
12. **Distribución de playtime**: Buckets (<1h, 1-5h, 5-10h, 10-20h, 20-50h, 50h+)
13. **Top 15 jugadores** por playtime
14. **Stickiness (DAU/WAU)**: Ratio de actividad diaria vs semanal
15. **Churn**: Activos 7d, riesgo churn 7-14d, churned >14d
16. **Concurrencia por día de la semana**
17. **Jugadores únicos diarios** (tendencia)
18. **Registros diarios** (tendencia)
19. **Ping medio** y distribución
20. **Mundos**: Tiempo por mundo y distribución
21. **Versiones de cliente**: Distribución de protocol versions
22. **Direcciones de conexión**: Por qué dominio/IP entraron

### Proyecciones
23. **Tendencia 1ª mitad vs 2ª mitad**: Crecimiento o declive
24. **Estimación próximo mes**: 3 escenarios (conservador, base, optimista)
25. **Posicionamiento de mercado**: Comparativa con competidores hispanohablantes

---

## 🎯 Competidores de Referencia (Mercado MC Hispano)

Actualizar estos datos con búsqueda web cada vez que se genere el informe:

| Tier | Servidores | CCU Referencia |
|---|---|---|
| Tier 1 (Consolidados) | UniversoCraft | 500-2,000+ |
| Tier 2 (Competitivos) | DeathZone, MagmaMC, Volatik | 70-200 |
| Tier 3 (Emergentes) | ThunderMC, SurvivalDub | 30-120 |

---

## ⚠️ Puntos de Control Obligatorios

Al generar el informe, **siempre** verificar y alertar sobre:

1. **MSPT > 20ms**: Zona de riesgo de rendimiento
2. **TPS < 18**: Lag perceptible por jugadores
3. **AFK > 30%**: Inflación de métricas de playtime
4. **Retención semanal < 30%**: Problema de contenido o onboarding
5. **Bounce rate > 40%**: Problema severo de primera experiencia
6. **Entidades > 3,000**: Revisar granjas y limits
7. **Mob kills anómalos** (>1M por jugador/mes): Posible granja masiva o exploit
8. **Stickiness < 25%**: Falta de contenido recurrente

---

## 📁 Archivos del Skill

```
analisisdelmes/
├── SKILL.md                      ← Este archivo (instrucciones)
├── scripts/
│   ├── schema_discovery.js       ← Descubrimiento del esquema de la DB
│   └── full_analysis.js          ← Script principal de análisis completo
└── references/
    └── plantilla-informe.md      ← Plantilla del informe mensual en Markdown
```
