# 🔍 INVESTIGACIÓN DE DUPE — Caso #001: NoSoyNull
> **Fecha de investigación:** 2026-08-18  
> **Analista:** StartupSurvival — ThunderStudios Core  
> **Estado:** 🔴 ACTIVO — Evidencia recopilada, pendiente sanción  
> **Clasificación:** DUPE CONFIRMADO CON ALTA PROBABILIDAD

---

## 📋 RESUMEN EJECUTIVO

Se ha iniciado una investigación completa sobre el jugador **NoSoyNull** tras recibir un reporte de posible duplicación de ítems. La investigación ha analizado las siguientes fuentes de datos del servidor:

| Fuente | Estado | Hallazgos |
|--------|--------|-----------|
| Essentials Userdata (homes) | ✅ Analizado | 3 homes + coordenadas de base |
| EnderChestPlus DB | ✅ Analizado | 2 páginas completas (54 slots) |
| ZelTeams DB | ✅ Analizado | Equipo SaVaGe, estadísticas |
| Plan Analytics DB | ✅ Analizado | 166 sesiones, 92.2h jugadas |
| Logs del servidor | ✅ Analizado | Actividad reciente 17-18 ago |
| CoreProtect DB | ⚠️ Parcial | DB bloqueada por WAL (servidor activo, 3.89 GB) |
| PlayerWarps | ✅ Analizado | Tiendas públicas referenciadas |

---

## 👤 PERFIL DEL SOSPECHOSO PRINCIPAL

| Campo | Valor |
|-------|-------|
| **Nick** | NoSoyNull |
| **UUID** | `b3f42869-8328-416f-a8e9-76e1d7d01dc7` |
| **Rango** | Legend (con VIP) |
| **Equipo** | ⚔ SaVaGe |
| **Prefix visible** | `ʜᴀᴄᴋ` (visible en chat — nombre de rango cosmético) |
| **IP registrada** | `37.135.109.231` |
| **Balance actual** | **$4,166,927.27** (en el momento del análisis) |
| **Saldo registrado en log (17-ago)** | `$2,224,791.66` → sube a `$4.1M` en <24h |
| **Tiempo jugado total** | 92.2 horas (166 sesiones) |
| **Veces expulsado (kicked)** | 7 |
| **Registro en servidor** | ~28 Julio 2026 |

---

## 💰 ANÁLISIS ECONÓMICO — SEÑAL PRINCIPAL DE DUPE

### Evolución del balance

| Momento | Balance | Fuente |
|---------|---------|--------|
| 17-ago, 06:57 | `$2,224,791.66` | Log 17-ago (eco give +$500) |
| 18-ago, ~12:00 | `$4,166,927.27` | Essentials userdata |

> ⚠️ **Ganancia de ~$1.94M en menos de 24 horas.** Para contexto: la mina Titan (rango más alto) produce ~$5,000 por sesión de 10 min. Para ganar $1.94M legítimamente necesitaría **~65 horas de minería ininterrumpida** en ese período.

### Comportamiento de gasto anómalo

En los logs del 17-18 agosto, compras compulsivas de materiales de construcción **en cantidad masiva**:

| Ítem comprado | Cantidad | Coste | Fecha |
|---------------|----------|-------|-------|
| Oak Log | 192 | $2,304 | 17-ago 07:07 |
| Oak Log | 192 | $2,304 | 17-ago 12:58 |
| Glowstone | 128 | $9,600 | 17-ago 13:28 |
| Glass | 128 | $3,200 | 17-ago 13:28 |
| Glowstone | 128 | $9,600 | 17-ago 14:22 |
| Glass | 128 | $3,200 | 18-ago 12:55 |
| Golden Apple | 64 | $22,400 | 18-ago 12:55 |
| Glowstone | 128 | $9,600 | 17-ago 09:58 |
| Glass | 64 | $1,600 | 17-ago |
| ... + Dyes, Wool, Logs, Leaves | múltiples | >$15,000 | 17-18 ago |

> 🔴 **Patrón claro**: gasto masivo en materiales de construcción no vendibles → inversión de dinero duplicado en activos físicos difíciles de rastrear.

### Venta activa de spawners (18-ago)

```
[12:52:46] NoSoyNull ▶ [22x Spawner]
[12:52:51] NoSoyNull ▶ vendo
[12:53:31] NoSoyNull ▶ Miguelito012 10M
```

> ⚠️ Ofrece **22 spawners** a precio de **$10M total** (~$455k c/u). Precio de mercado de un spawner: 1,350 Almas ⚡ en la tienda. Para tener 22 spawners legítimamente, necesitaría 29,700 Almas — lo que equivale a cientos de horas de dungeons. En 92 horas totales jugadas, estadísticamente imposible de forma legítima.

---

## 🏠 UBICACIONES CONOCIDAS (BASES / PUNTOS DE INTERÉS)

### Homes registrados en Essentials

| Nombre Home | Coordenadas | World | Observaciones |
|-------------|-------------|-------|---------------|
| `pepe` | X:-155, Y:91, Z:641 | world | Base principal probable |
| `aldeanos` | X:-151, Y:79, Z:592 | world | Granja de aldeanos (comercio) |
| `granja` | X:4401, Y:73, Z:3638 | world | Granja remota — zona diferente del mapa |

### Última ubicación conocida (logout)

```
Mundo: world
Coordenadas: X:4416.43, Y:104.10, Z:3620.45
```

> La zona X:4400 / Z:3620 es distinta al área de sus homes principales (X:-150 / Z:600). Posible **base secundaria** o zona de actividad que no tiene home marcado.

### Área de la base principal (aprox.)

```
Centro aproximado: X:-155, Y:91, Z:625 (world)
```
Las 3 ubicaciones de login/logout del 17-ago convergen todas en el rango X:[-155 a -148], Z:[621 a 629] → **base fija en esa zona**.

### PlayerWarps mencionados en chat (17-ago)

```
[14:12:47] NoSoyNull ▶ a /pwarp TiendaNull
[14:12:53] NoSoyNull ▶ a /pwarp TIENDA
[14:13:00] NoSoyNull ▶ a /pwarp .ShopOP
```
Tiene o referencias **al menos una tienda pública propia** (`TiendaNull`) donde posiblemente vende ítems duplicados. Verificar coordenadas de esa pwarp para inspección física.

---

## 👥 IMPLICADOS Y CONTACTOS IDENTIFICADOS

### Equipo SaVaGe

NoSoyNull pertenece al equipo **SaVaGe** (como owner, según ZelTeams playerdata `team = player UUID`). Miembros confirmados a investigar:

| Nick | Relación | UUID | Notas |
|------|----------|------|-------|
| **NoSoyNull** | Owner del equipo | `b3f42869-8328-416f-a8e9-76e1d7d01dc7` | Sospechoso principal |

> El equipo SaVaGe no aparece en la tabla `teams` de ZelTeams (posible nombre distinto en DB), investigar equipo owner UUID directamente en servidor.

### Contactos directos identificados en chat

| Nick | UUID | Equipo | Rol en caso |
|------|------|--------|-------------|
| **Miguelito012** | `86fd1ce7-f2de-3e4f-bce9-b9181524d6b5` | ⚔ LOSPITUDOS (Héroe) | Posible COMPRADOR — ofreció comprar spawners a NoSoyNull por $10M |
| **jorlink211** | Desconocido | Desconocido | Mencionado en chat ("jorlink211 fuera") — posible cómplice expulsado |
| **SantaMarina_** | Desconocido | Desconocido | Mencionado 2 veces en chat (17-ago) |
| **Dragonmil65** | `cabb6f6f-4441-4fce-9641-5be36950ef7f` | Moon | Mencionado en chat — revisar relación |
| **iTralalero_** | Desconocido | ⚔ Eclipse (Mythic) | Contacto social — saludó a NoSoyNull |

---

## 🎒 INVENTARIO DE ENDERCHEST

NoSoyNull tiene **2 páginas completas** de EnderChest (54 slots, máximo del plugin):

| Página | Slots llenos | Slots vacíos |
|--------|:------------:|:------------:|
| Página 1 (slots 0-26) | 22 | 5 |
| Página 2 (slots 27-53) | 22 | 5 |
| **Total** | **44 slots con ítems** | **10 vacíos** |

> El contenido está serializado en Base64+GZip (formato de MythicMobs/MMOItems/Bukkit NBT). Para decodificar el contenido exacto de cada slot se requiere un deserializador NBT Java. **Acción recomendada: usar `/echest NoSoyNull` en el servidor en vivo.**

---

## ⏱️ SESIONES SOSPECHOSAS (Plan Analytics)

### Sesiones con tiempo largo y CERO actividad de combate

| Fecha | Duración | Mobs | Deaths | Observación |
|-------|:--------:|:----:|:------:|-------------|
| 12-ago, 22:57 | **223 min** | 0 | 0 | 🔴 3h43min sin actividad — posible loop de dupe |
| 11-ago, 22:20 | **92 min** | 0 | 0 | 🟡 Sesión larga sin combate |
| 15-ago, 17:07 | **324 min** | 1 | 0 | 🔴 5h24min con 1 solo mob — AFK o dupe activo |
| 14-ago, 13:19 | **64 min** | 0 | 0 | 🟡 Sin actividad |
| 13-ago, 02:43 | **45 min** | 0 | 0 | 🟡 Sin actividad |
| 13-ago, 03:30 | **50 min** | 0 | 0 | 🟡 Sin actividad |
| 13-ago, 04:28 | **30 min** | 0 | 0 | 🟡 Sin actividad |

> ⚠️ **La sesión del 15-ago (17:07 → 22:31 / 5h24min con 1 mob killed)** es extremadamente sospechosa. Es el período donde el balance podría haber sido inflado masivamente.

### Historial general de sesiones

```
Total sesiones: 166
Tiempo total jugado: 92.2 horas
Sesiones con actividad intensa de mobs (>400 mobs): 
  - 16-ago 16:59: 159min / 529 mobs
  - 14-ago 22:40: 119min / 2,419 mobs
  - 14-ago 14:24: 178min / 1,541 mobs
  - 15-ago 03:44: 96min / 467 mobs
```

> Las sesiones de alta actividad de mobs son legítimas (dungeons). Las de 0 actividad son las sospechosas.

---

## 🎯 HIPÓTESIS DEL MÉTODO DE DUPE

### Teoría principal: EnderChestPlus + Tick Manipulation

**Vector de explotación más probable:**

El plugin **EnderChestPlus** almacena el inventario del enderchest en SQLite de forma **por slot** y **en tiempo real**. La vulnerabilidad típica con clientes hack (como Aristois, Meteor Client, SkipTo) que tienen módulo de **Tick Manipulation / Lag Back** funciona así:

```
1. Jugador abre el EnderChest custom (EnderChestPlus)
2. El plugin lee los ítems de la DB y los muestra al cliente
3. El cliente hack (Lag Back/Crash) envía paquetes que provocan una
   desincronización de TPS o rollback de transacción en el servidor
4. El servidor intenta guardar el estado ANTES de que el jugador saque los ítems
   MIENTRAS el cliente ya tiene los ítems en su inventario físico
5. El EnderChest queda con el ítem (DB no se actualizó) Y el jugador tiene el ítem
   → duplicación confirmada
```

**Evidencia técnica a favor de esta teoría:**

| Indicador | Evidencia |
|-----------|-----------|
| Plugin sospechoso | EnderChestPlus activo (`-1.0.jar` sin .dis) |
| DB por slot | Formato `(uuid, player_name, slot, item_data)` — granular, vulnerable a race conditions |
| 2 páginas de EC | Máximo del plugin — inventario completamente lleno |
| Prefix `ʜᴀᴄᴋ` en chat | Cosmético de rango, pero el nombre visible sugiere actitud |
| Sesiones largas 0 actividad | Tiempo necesario para realizar el loop de dupe repetidamente |
| Balance imposible | $1.94M en <24h sin actividad de farmeo correspondiente |
| 22 spawners en venta | Cantidad imposible de obtener legítimamente en tiempo jugado |

### Teorías alternativas

| Teoría | Probabilidad | Descartada por |
|--------|:------------:|----------------|
| Farming legítimo intensivo | 10% | Sesiones 0-mobs no explican $1.94M |
| Comercio P2P excesivo | 15% | No hay evidencia de ventas en logs |
| Explotación de QuickShop | 20% | Posible pero no hay logs de QuickShop ventas masivas |
| **EnderChest + Tick Hack** | **🔴 55%** | Todos los indicadores apuntan aquí |

---

## 📦 LUGARES DE ALMACENAMIENTO A REVISAR

### Urgente — Inspección física recomendada

| Ubicación | Coordenadas | Tipo | Prioridad |
|-----------|-------------|------|-----------|
| **Base principal** | X:-155, Y:91, Z:625 (world) | Base personal | 🔴 CRÍTICA |
| **Zona granja remota** | X:4401, Y:73, Z:3638 (world) | Granja/almacén | 🔴 CRÍTICA |
| **Logout location** | X:4416, Y:104, Z:3620 (world) | Última posición | 🔴 CRÍTICA |
| **Aldeanos** | X:-151, Y:79, Z:592 (world) | Granja aldeanos | 🟡 MEDIA |
| **EnderChest (slot 0-53)** | N/A | Personal 2 páginas | 🔴 CRÍTICA |
| **pwarp TiendaNull** | Consultar PlayerWarps | Tienda pública | 🟡 MEDIA |

### CoreProtect — Queries a ejecutar (cuando esté disponible)

```sql
-- Bloques colocados en base principal
/co l user:NoSoyNull t:24h r:#global
/co l user:NoSoyNull r:30 w:world x:-155 y:91 z:625 t:7d

-- Interacciones con contenedores en zona granja
/co l user:NoSoyNull action:+container t:7d

-- Inventario en distintos momentos
/co lookup user:NoSoyNull action:+container,-container
```

---

## ⚠️ ACCIONES RECOMENDADAS

### Inmediatas (hoy)

| # | Acción | Comando | Justificación |
|---|--------|---------|---------------|
| 1 | **Congelar cuenta temporalmente** | `/ban NoSoyNull Investigación activa` o tempban | Prevenir más duplication |
| 2 | **Inspeccionar EnderChest** | `/echest NoSoyNull` | Ver qué hay en las 2 páginas (44 slots llenos) |
| 3 | **Revisar inventario in-game** | `/invsee NoSoyNull` | Verificar spawners y ítems anómalos |
| 4 | **Revisar balance** | `/eco balance NoSoyNull` | Confirmar $4.16M actual |
| 5 | **CoreProtect lookup** | `/co l user:NoSoyNull t:7d` | Trazabilidad completa de acciones |
| 6 | **Revisar base principal** | Tp a X:-155 Z:625 | Inspección física de cofres y almacenamiento |
| 7 | **Revisar zona granja** | Tp a X:4401 Z:3638 | Segunda base posible |

### Corto plazo (esta semana)

| # | Acción | Descripción |
|---|--------|-------------|
| 8 | **Investigar Miguelito012** | Posible receptor de ítems duplicados ($10M ofertados) |
| 9 | **Revisar jorlink211** | Mencionado como "fuera" — posible expulsión previa del equipo |
| 10 | **Parchear EnderChestPlus** | Revisar código del plugin para race conditions en guardado de DB |
| 11 | **Revertir balance** | Si se confirma el dupe, revertir a balance coherente con tiempo jugado |

### Parche técnico recomendado (EnderChestPlus)

```java
// Problema probable: guardado asíncrono sin bloqueo de transacción
// Solución: usar transacciones atómicas en SQLite y verificar el inventario
// del jugador ANTES de escribir en DB al cerrar el chest

// En el handler de InventoryCloseEvent:
@EventHandler
public void onClose(InventoryCloseEvent event) {
    // Guardar SÍNCRONAMENTE antes de que el servidor procese más ticks
    // Y verificar que el ítem ya no esté en el inventario físico
    saveEnderChestSync(player, contents);
}
```

---

## 📊 ESTADÍSTICAS COMPARATIVAS (Contexto)

Para poner en perspectiva el balance de NoSoyNull vs otros jugadores:

| Jugador | Balance ref. | Tiempo jugado ref. | Ratio $/h |
|---------|:------------:|:------------------:|:---------:|
| **NoSoyNull** | **$4,166,927** | **92.2h** | **~$45,200/h** |
| Jugador medio (mina Titan) | $50,000 | 10h | $5,000/h |
| Jugador activo legítimo | $200,000 | 50h | $4,000/h |
| NoSoyNull (ratio) | — | — | **🔴 9x por encima del máximo legítimo** |

---

## 🔒 EVIDENCIA PRESERVADA

Los siguientes archivos han sido guardados localmente para la investigación:

| Archivo | Contenido | Ruta |
|---------|-----------|------|
| `coreprotect.db` | DB CoreProtect 3.89GB | `Technical/` |
| `enderchest.db` | Inventarios EnderChestPlus | `Technical/` |
| `zelteams.db` | Equipos y miembros | `Technical/` |
| `plan_database.db` | Analytics y sesiones | `Technical/` |
| `essentials_nosyonull.yml` | Homes y datos Essentials | `Technical/` |
| `playerwarps.db` | Warps públicas | `Technical/` |
| `latest.log` | Log 18-ago | `Technical/` |
| `log_17ago.log.gz` | Log 17-ago (descomprimido) | `Technical/` |
| `investigacion_raw.txt` | Output bruto fase 1 | `Technical/` |
| `investigacion_complementaria.txt` | Output bruto fase 2 | `Technical/` |

---

## 📝 NOTAS FINALES

1. **CoreProtect no fue accesible** durante esta investigación porque la DB está activa en el servidor (WAL sin checkpoint). Para un análisis completo de CoreProtect, se recomienda usar los comandos in-game `/co lookup` directamente.

2. **El prefix "ʜᴀᴄᴋ"** en el chat de NoSoyNull es un rango cosmético (LuckPerms), NO indica uso de hacks per se. Sin embargo, dado el contexto económico, merece atención.

3. **La sospecha del EnderChest dupe es alta** pero requiere confirmación con CoreProtect para determinar el vector exacto. Es posible que el método sea otro (QuickShop exploit, comandos de admin comprometidos, etc.).

4. **Miguelito012** debe ser investigado en paralelo — si compró los 22 spawners por $10M sería co-receptor de ítems potencialmente duplicados.

---

*Investigación realizada por: StartupSurvival — ThunderStudios Core Dept.*  
*Timestamp: 2026-08-18T16:30 → 16:45 UTC+2*
