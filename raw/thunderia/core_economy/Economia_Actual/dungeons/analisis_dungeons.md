# ⚔️ Análisis de Mazmorras — ThunderStudios Survival
> Última actualización: 2026-08-17 | Plugin: MythicMobs | Fuente: plugins/MythicMobs/mobs/

---

## 📌 Sistema de Recompensas Universal

Todos los mobs de mazmorra comparten el mismo sistema base de recompensas al morir:

| Tipo | Descripción | Probabilidad |
|------|-------------|:------------:|
| 💰 Dinero ($) | Vault — varía por mazmorra | 100% |
| ⚡ Almas | PlayerPoints — varía por mob | 100% |
| 🟩 Fragmento Super | Pieza de llave SUPER | 2% |
| 🔵 Fragmento Rara | Pieza de llave RARA | 2% |
| 🟡 Fragmento Gadget | Pieza de llave ÉPICA | 2% |
| 🔴 Fragmento Mítica | Pieza de llave MÍTICA | 0.3% |
| 🌈 Fragmento Limited | Pieza de llave DIVINA | 0.1% *(M4+)* |

> ⚡ = PlayerPoints (Almas) | $ = Vault (dinero en juego)
> Los fragmentos de llave se combinan via /llaves para obtener llaves de cofre completas.

---

## 🗺️ MAZMORRA 1 — Los Establos

> **Tema:** Granja corrupta | **Nivel recomendado:** 1 | **Dificultad:** ⭐☆☆☆☆☆☆

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Jabalí | jabali1 | PIG | **12** | **7** | 0.23 | Ninguna |
| Oveja Furiosa | OvejaDash | SHEEP | **10** | **7** | 0.35 | 💨 Dash cada 2s |
| Vaca Bruta | VacaBruta | COW | **18** | **14** | 0.22 | Escala 1.2x |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla |
|-----|:--------:|:--------:|--------------|
| Jabalí | $10 | +1 | PORKCHOP 1-2 |
| Oveja Furiosa | $10 | +1 | MUTTON 1-2 |
| Vaca Bruta | $18 | +2 | BEEF 1-3 |

### Resumen M1
- Mob más peligroso: **Vaca Bruta** (18 HP / 14 dmg)
- Sin mecánicas de élite ni umbrales de fase
- Drops básicos de granja, sin fragmentos de alta rareza disponibles
- Ideal para jugadores nuevos — sin equipamiento especial requerido

---

## 🗺️ MAZMORRA 2 — Las Galerías

> **Tema:** Mina subterránea | **Nivel recomendado:** 2 | **Dificultad:** ⭐⭐☆☆☆☆☆

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Explorador de Galerías | ExploradorGalerias | ZOMBIE | **14** | **9** | 0.33 | Salto al jugador (leap) cada 6s |
| Minero Corrupto | MineroCorrupto | HUSK | **16** | **11** | 0.24 | Escala 1.2x, aplica Hambre |
| Capataz de la Mina | CapatazMina | IRON_GOLEM | **28** | **15** | 0.20 | Speed propio al <50% HP |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla |
|-----|:--------:|:--------:|--------------|
| Explorador | $18 | +2 | COAL 30%, ROTTEN_FLESH |
| Minero Corrupto | $22 | +2 | COAL 1-2, IRON_INGOT 30% |
| Capataz | $40 | +4 | IRON_INGOT 1-5, ROTTEN_FLESH |

### Resumen M2
- Mob más peligroso: **Capataz** (28 HP / 15 dmg — casi el doble de HP que los comunes)
- El Explorador usa Leap para sorprender — mantener distancia
- Primera mazmorra con drops de hierro garantizados
- El Capataz desbloquea Fragmento Gadget (2% también)

---

## 🗺️ MAZMORRA 3 — Las Ruinas de la Forja

> **Tema:** Ruinas medievales / forja | **Nivel recomendado:** 3-4 | **Dificultad:** ⭐⭐⭐☆☆☆☆

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Explorador Ígneo | ExploradorIgneo | SKELETON | **18** | **12** | 0.30 | Ranged (arco) + Leap cada 5s + Speed al recibir daño |
| Soldado Errante | SoldadoRuinas | ZOMBIE | **22** | **15** | 0.25 | Speed propio al <30% HP |
| Guardián de la Forja | GuardianForja | ZOMBIE | **35** | **20** | 0.22 | ⚠️ Fase 1 (60% HP): Lentitud al jugador + Partículas de lava |

### Mecánicas de fase — Guardián de la Forja

| Umbral HP | Efecto |
|:---------:|--------|
| < 60% (21 HP) | Aplica Lentitud I al jugador + partículas de lava |
| < 30% (10 HP) | Se auto-aplica Fuerza I durante 5s |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla | Frag. Mítica |
|-----|:--------:|:--------:|--------------|:------------:|
| Explorador Ígneo | $25 | +3 | ARROW 2-5, COAL 60% | 0.3% |
| Soldado Errante | $30 | +3 | IRON_NUGGET 2-4, GRAVEL 50% | 0.3% |
| Guardián de la Forja | $60 | +5 | IRON_INGOT 1-3, GOLD_NUGGET 50% | 0.3% |

### Resumen M3
- Primera mazmorra con enemigos **a distancia** (Explorador Ígneo con arco)
- El Guardián tiene 2 **fases de combate** — mecánica de jefe en mob común
- Primera mazmorra con drop de **Fragmento Mítica (0.3%)**
- Requiere armadura de hierro mínimo para sobrevivir al Guardián

---

## 🗺️ MAZMORRA 4 — El Santuario Piglin

> **Tema:** Nether / Piglin | **Nivel recomendado:** 4-5 | **Dificultad:** ⭐⭐⭐⭐☆☆☆

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Guardia Piglin | AcolitoSantuario | PIGLIN | **24** | **22** | 0.24 | Debilidad I al jugador al <50% HP |
| Bestia Hoglin | BestiaPiglin | HOGLIN | **24** | **22** | 0.30 | Inmune a zombificación, escala 0.8x |
| Gladiador Piglin | CentinelaEterno | PIGLIN_BRUTE | **45** | **30** | 0.21 | ⚠️ 2 fases + invoca refuerzo |

### Mecánicas de fase — Gladiador Piglin (CentinelaEterno)

| Umbral HP | Efecto |
|:---------:|--------|
| < 70% (32 HP) | Lentitud II al jugador + partículas Netherrack |
| < 40% (18 HP) | **Invoca un AcolitoSantuario de refuerzo** + Fuerza II + partículas de llama |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla | Frag. Limited |
|-----|:--------:|:--------:|--------------|:-------------:|
| Guardia Piglin | $45 | +4 | GOLD_NUGGET 3-8, GOLD_INGOT 30%, XP_BOTTLE 70% | 0.1% |
| Bestia Hoglin | $45 | +4 | GOLD_NUGGET 3-8, GOLD_INGOT 30%, XP_BOTTLE 70% | 0.1% |
| Gladiador Piglin | $100 | +8 | IRON_INGOT 2-4, GOLD_INGOT 50%, WITHER_SKULL 5% | 0.1% |

### Resumen M4
- El Gladiador da **Daño 30** — el más alto hasta ahora en mobs comunes
- El sistema de **invocación de refuerzo** puede abrumar si no se gestiona bien
- Primer mob que puede dropear **Cráneo Wither (5%)**
- Los 3 mobs tienen drop de **Fragmento Limited (0.1%)**
- Requiere armadura de diamante o muy buen hierro con encantamientos

---

## 🗺️ MAZMORRA 6 — La Guarida de las Arañas

> **Tema:** Cueva de arácnidos | **Nivel recomendado:** 6 | **Dificultad:** ⭐⭐⭐⭐⭐☆☆

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Araña Mutante | ArañaMutante | SPIDER | **35** | **25** | 0.30 | Escala 1.5x, Knockback resist. 30% |
| Araña Venenosa | ArañaVenenosa | CAVE_SPIDER | **20** | **15** | 0.30 | Aplica **Veneno I** (5s) en cada ataque |
| Arañita | Arañita | SPIDER | **20** | **16** | 0.30 | Escala 0.5x (miniatura), Knockback resist. 30% |
| Esqueleto Guardián | EsqueletoGuardian | BOGGED | **30** | **25** | 0.24 | Debilidad I al jugador al <50% HP |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla | Frag. Limited |
|-----|:--------:|:--------:|--------------|:-------------:|
| Araña Mutante | $45 | +4 | STRING 1-3, SPIDER_EYE 50%, XP_BOTTLE 70% | 0.1% |
| Araña Venenosa | $45 | +4 | STRING 1-3, SPIDER_EYE 50%, XP_BOTTLE 70% | 0.1% |
| Arañita | $45 | +4 | STRING 1-3, SPIDER_EYE 50%, XP_BOTTLE 70% | 0.1% |
| Esqueleto Guardián | $45 | +4 | IRON_NUGGET 3-8, IRON_INGOT 30%, XP_BOTTLE 70% | 0.1% |

### Resumen M6
- El **Veneno** de la Araña Venenosa es el peligro principal — llevar leche o pociones de curación
- La **Arañita** (escala 0.5x) es pequeña pero con daño 16 — difícil de ver
- El **Esqueleto Guardián** (BOGGED) aplica Debilidad — reduce el daño del jugador
- Todas las arañas tienen resistencia al knockback — no se pueden alejar fácilmente

---

## 🗺️ MAZMORRA 7 — La Prisión Helada

> **Tema:** Dungeon de hielo / congelamiento | **Nivel recomendado:** 7 | **Dificultad:** ⭐⭐⭐⭐⭐⭐☆

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Carcelero | Carcelero1 | PILLAGER | **40** | **30** | 0.30 | **Debilidad I** en cada ataque, Knockback resist. 50% |
| Guardián Gélido | GuardianGelido | PILLAGER | **40** | **30** | 0.30 | Escala 1.3x, Knockback resist. 50%, lleva **Escudo** |
| Cucaracha Helada | CucharachaHelada | SILVERFISH | **40** | **30** | 0.30 | Escala **2x** (gigante), Knockback resist. 50% |
| Esqueleto Gélido | EsqueletoGelido | SKELETON | **40** | **30** | 0.30 | Armadura de diamante + hacha, Knockback resist. 50% |
| Espíritu Helado | EspirituHelado | BREEZE | **40** | **30** | 0.30 | **+10 Almas / $100** (doble recompensa) |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla | Frag. Limited |
|-----|:--------:|:--------:|--------------|:-------------:|
| Carcelero | $50 | +5 | PACKED_ICE 1-2 50%, DIAMOND 1-2, XP_BOTTLE 1-2 | 0.1% |
| Guardián Gélido | $50 | +5 | EMERALD 1-2 50%, DIAMOND 1-2, XP_BOTTLE 1-2 | 0.1% |
| Cucaracha Helada | $50 | +5 | EMERALD 1-2 50%, DIAMOND 1-2, XP_BOTTLE 1-2 | 0.1% |
| Esqueleto Gélido | $50 | +5 | EMERALD 1-2 50%, DIAMOND 1-2, XP_BOTTLE 1-2 | 0.1% |
| Espíritu Helado | **$100** | **+10** | EMERALD 1-2 50%, DIAMOND 1-2, XP_BOTTLE 1-2 | 0.1% |

### Resumen M7
- **Todos los mobs tienen HP y daño unificado** (40 HP / 30 dmg) — diseño de tier uniforme
- El **Carcelero** aplica Debilidad en cada golpe — muy peligroso en grupos
- El **Guardián Gélido** lleva escudo — puede bloquear ataques del jugador
- La **Cucaracha Helada** es escala 2x — visualmente imponente e inesperada
- El **Espíritu Helado** (BREEZE) da **doble recompensa** ($100 / +10 Almas)
- **Primera mazmorra con drops de Diamante garantizados** en todos los mobs
- El jefe de esta mazmorra es **Frostal (JineteEsqueletoJefe)**

---

## 🗺️ MAZMORRA 8 — La Forja Ardiente

> **Tema:** Nether / Piglin de fuego | **Nivel recomendado:** 8 | **Dificultad:** ⭐⭐⭐⭐⭐⭐⭐

### Mobs

| Mob | ID | Tipo | HP | Daño | Velocidad | Mecánica especial |
|-----|----|------|:--:|:----:|:---------:|-------------------|
| Minero de la Forja | MineroForja | ZOMBIFIED_PIGLIN | **45** | **30** | 0.30 | Knockback resist. 50%, partículas de llama |
| Espíritu de Fuego | EspirituFuego | BLAZE | **45** | **30** | 0.30 | Aura de fuego activa (AuraFuego) |
| Guardia de la Forja | GuardiaForja | PIGLIN | **45** | **30** | 0.30 | Armadura completa dorada + escudo |
| Esqueleto Calcinado | EsqueletoCalcinado | WITHER_SKELETON | **45** | **30** | 0.30 | Spada dorada, aplica Wither |
| Portero de la Forja | PorteroForja | PIGLIN | **100** | **30** | 0.30 | Armadura NETHERITA completa, **+10 Almas / $100** |

### Recompensas por kill

| Mob | $ Dinero | ⚡ Almas | Drop vanilla | Frag. Limited |
|-----|:--------:|:--------:|--------------|:-------------:|
| Minero Forja | $50 | +5 | MAGMA_CREAM 50%, GOLD 1-2, XP_BOTTLE 1-2 | 0.1% |
| Espíritu Fuego | $50 | +5 | MAGMA_CREAM 50%, GOLD 1-2, XP_BOTTLE 1-2, **BLAZE_ROD** | 0.1% |
| Guardia Forja | $50 | +5 | MAGMA_CREAM 50%, GOLD 1-2, XP_BOTTLE 1-2 | 0.1% |
| Esqueleto Calcinado | $50 | +5 | MAGMA_CREAM 50%, GOLD 1-2, XP_BOTTLE 1-2 | 0.1% |
| Portero Forja | **$100** | **+10** | MAGMA_CREAM 50%, GOLD 1-2, XP_BOTTLE 1-2 | 0.1% |

### Resumen M8
- El **Espíritu de Fuego** usa `AuraFuego` activa — daño de área pasivo
- El **Portero** tiene **100 HP** (el doble) y armadura completa de Netherita — mini-jefe de sala
- El **Esqueleto Calcinado** (Wither Skeleton) aplica el efecto Wither — daño continuo
- Todos los mobs son resistentes al knockback (50%)
- El jefe de esta mazmorra es **Hefesto (ReyForja)**
- Drop exclusivo: **BLAZE_ROD** del Espíritu de Fuego (único en todo el servidor)

---

## 👑 JEFES — Análisis Completo

### 🕷️ Aracne — La Araña Reina
> **ID:** ArañaReina | **Mazmorra:** 6 | **Tipo:** CAVE_SPIDER

| Stat | Valor |
|------|:-----:|
| HP | **2,000** |
| Daño | **30** |
| Escala | 4x (gigante) |
| Velocidad | 0.40 |
| Knockback | 30% resistencia |
| Bossbar | ✅ Rojo — "Aracne \| La Araña Reina" |

**Habilidades activas:**
| Skill | Trigger | Efecto |
|-------|---------|--------|
| Veneno II | ~onAttack | Veneno nivel 2 al jugador (7.5s) |
| InvocarArañas75 | ~onTimer | Invoca arañas al 75% HP |
| InvocarArañas50 | ~onTimer | Invoca arañas al 50% HP |
| InvocarArañas25 | ~onTimer | Invoca arañas al 25% HP |
| Guardian_Beam | ~onTimer:150 | Rayo de jefe cada 7.5s |

**Recompensas al morir:**

| Tipo | Cantidad |
|------|:--------:|
| $ Dinero | **$1,000** |
| ⚡ Almas | **+30** |
| Fragmentos (Super/Rara/Gadget) | 2% c/u |
| Fragmento Mítica | 0.3% |
| Fragmento Limited | 0.1% |
| STRING | 1-3 (100%) |
| SPIDER_EYE | 1 (50%) |
| XP_BOTTLE | 1-3 (70%) |

---

### ❄️ Frostal — El Ghoul Helado
> **ID:** JineteEsqueletoJefe | **Mazmorra:** 7 | **Tipo:** STRAY (montado en caballo esqueleto)

| Stat | Valor |
|------|:-----:|
| HP | **1,200** (+ Corcel: 300 HP separado) |
| Daño | **25** |
| Escala | 1.5x |
| Velocidad | 0.30 (caballo 0.40) |
| Knockback | 80% resistencia |
| Bossbar | ✅ Blanco — "Frostal \| El Ghoul Helado" |
| Inmunidad | Proyectiles (0 daño) |

**Habilidades activas:**
| Skill | Trigger | Efecto |
|-------|---------|--------|
| freeze | ~onAttack | **Congela al jugador** (5 ticks) |
| disengage | ~onAttack | Se aleja tras atacar |
| PrisionHielo | ~onTimer:1 | Prisión de hielo periódica |
| InvocarCarceleros25 | ~onTimer:1 | Invoca Carceleros al 25% HP |
| EscudoHielo | ~onDamaged | Escudo de hielo al recibir daño |
| Partículas hielo | ~onTimer:10 | Visual SNOWFLAKE continuo |

**Recompensas al morir:**

| Tipo | Cantidad |
|------|:--------:|
| $ Dinero | **$1,200** |
| ⚡ Almas | **+40** |
| Fragmentos (Super/Rara/Gadget) | 2% c/u |
| Fragmento Mítica | 0.3% |
| Fragmento Limited | 0.1% |
| BONE | 2-4 (100%) |
| DIAMOND | 1 (10%) |

---

### 🔥 Hefesto — El Señor de la Forja
> **ID:** ReyForja | **Mazmorra:** 8 | **Tipo:** PIGLIN_BRUTE

| Stat | Valor |
|------|:-----:|
| HP | **2,500** |
| Daño | **35** |
| Escala | 2x (gigante) |
| Velocidad | 0.40 |
| Knockback | 80% resistencia |
| Bossbar | ✅ Blanco — "Hefesto \| El Señor de la Forja" |
| Inmunidades | Proyectiles, caída, explosiones |

**Habilidades activas:**
| Skill | Trigger | Efecto |
|-------|---------|--------|
| disengage | ~onAttack | Se aleja tras atacar |
| SaltoMinero | ~onDamaged | Salto de ataque al recibir daño |
| AuraFuego | ~onTimer:10 | Aura de fuego continua (cada 0.5s) |
| fireball_barrage | ~onTimer:400 | **Lluvia de bolas de fuego** cada 20s |
| hurricane_wave | ~onTimer:200 | **Ola de huracán** cada 10s |
| BlockMask magma | ~onTimer:5 | Convierte bloques cercanos en magma |
| Partículas llama | ~onTimer:5 | Visual FLAME continuo |

**Recompensas al morir:**

| Tipo | Cantidad |
|------|:--------:|
| $ Dinero | **$1,200** |
| ⚡ Almas | **+40** |
| Fragmentos (Super/Rara/Gadget) | 2% c/u |
| Fragmento Mítica | 0.3% |
| Fragmento Limited | 0.1% |
| BONE | 2-4 (100%) |
| DIAMOND | 1 (10%) |

---

### 🐺 Cerbero — El Guardián
> **ID:** Cerbero | **Mazmorra:** Zona especial | **Tipo:** HOGLIN

| Stat | Valor |
|------|:-----:|
| HP | **2,000** |
| Daño | **25** |
| Escala | **3.0x** (enorme) |
| Velocidad | 0.30 |
| Knockback | ThreatTable activo |
| Bossbar | ✅ Rojo — "Cerbero \| El Guardian" |

**Sistema de 3 fases:**
| Fase | HP Umbral | Habilidades activas |
|:----:|:---------:|---------------------|
| Fase 1 | 100% → 66% (>800 HP) | LanzarArriba (c/16s) + Embestida (c/14s) |
| Transición → F2 | ~66% | Activa aura `fase2` |
| Fase 2 | 66% → 33% (800-400 HP) | Mismas skills con cooldown reducido |
| Transición → F3 | ~33% | Activa aura `fase3` |
| Fase 3 | 33% → 0% (<400 HP) | Cooldowns mínimos (10s/9s) |

**Recompensas al morir (las más generosas de todos los jefes):**

| Tipo | Cantidad |
|------|:--------:|
| $ Dinero | **$600** |
| ⚡ Almas | **+25** |
| 🔑 Llave Super | **1 garantizada** |
| Fragmentos (Super/Rara/Gadget) | **15%** c/u |
| Fragmento Mítica | **2.5%** |
| Fragmento Limited | 0.1% |
| DIAMOND | 4-7 (100%) |
| GOLDEN_APPLE | 1-2 (70%) |

> ⚠️ El Cerbero tiene las probabilidades de fragmentos **más altas de todos los jefes** (15% vs 2% del resto).

---

## 📊 Tabla Comparativa General

### Mobs comunes por mazmorra

| Mazmorra | HP Rango | Daño Rango | $ por kill | ⚡ Almas/kill | Frag. Limited |
|----------|:--------:|:----------:|:----------:|:-------------:|:-------------:|
| M1 — Los Establos | 10-18 | 7-14 | $10-18 | +1-2 | ❌ |
| M2 — Las Galerías | 14-28 | 9-15 | $18-40 | +2-4 | ❌ |
| M3 — Ruinas Forja | 18-35 | 12-20 | $25-60 | +3-5 | ❌ |
| M4 — Santuario Piglin | 24-45 | 22-30 | $45-100 | +4-8 | ✅ 0.1% |
| M6 — Guarida Arañas | 20-35 | 15-25 | $45 | +4 | ✅ 0.1% |
| M7 — Prisión Helada | 40 (todos) | 30 (todos) | $50-100 | +5-10 | ✅ 0.1% |
| M8 — Forja Ardiente | 45-100 | 30 (todos) | $50-100 | +5-10 | ✅ 0.1% |

### Jefes comparativa

| Jefe | HP | Daño | Fases | $ Reward | ⚡ Almas | 💎 Drop destacado |
|------|:--:|:----:|:-----:|:--------:|:--------:|-------------------|
| Aracne (M6) | 2,000 | 30 | Invocaciones | $1,000 | +30 | STRING + XP |
| Frostal (M7) | 1,200 (+300) | 25 | 1 + invocaciones | $1,200 | +40 | DIAMOND 10% |
| Hefesto (M8) | 2,500 | 35 | 1 continua | $1,200 | +40 | DIAMOND 10% |
| Cerbero (Especial) | 2,000 | 25 | **3 fases** | $600 | +25 | 💎×4-7 + 🍎×1-2 + 🔑Llave |

---

## 🔍 Observaciones y Puntos de Atención

| Observación | Detalle |
|-------------|---------|
| ⚠️ Mazmorra 5 ausente | No existe MAZMORRA5 en el sistema — posiblemente eliminada o no implementada |
| ⚠️ Frostal menor HP que Hefesto | JineteHelado tiene 1,200 HP pero está en M7 — Hefesto (M8) tiene 2,500 HP |
| ✅ Escalado consistente | HP de mobs sube ~10 por mazmorra. Daño sube ~5 por tier |
| ✅ Cerbero = mejor loot | 15% fragmentos, llave garantizada, 4-7 diamantes — claramente el boss más recompensado |
| 🔵 M7 y M8 unificados | Todos los mobs tienen exactamente las mismas stats base (HP/daño) — diseño de tier plano |
| 🔵 Portero M8 | 100 HP (el doble) — actúa como mini-jefe de sala antes de Hefesto |
| 💡 EspirituHelado (M7) y EspirituFuego (M8) | Dan el doble de almas ($100 / +10) — recompensan agresividad |

---

## 📝 Notas Técnicas

- **Plugin:** MythicMobs 5.11.2
- **Todos los mobs:** `PreventOtherDrops: true` + `Despawn: false` (no desaparecen)
- **Sistema ThreatTable:** Activado en M7 y M8 — targeting dinámico por daño
- **Sistema de Almas:** Cada mob guarda su valor en variable interna (`almas`) para el `BoostAlmas`
- **Fragmentos de llave:** Se combinan en /llaves para obtener llaves completas de cofre
- **DropOptions de jefes:** PerPlayerDrops=true — cada jugador recibe sus propios drops
- **RequiredDamagePercent:** 0.1 en jefes — necesitas infligir al menos 10% del daño para recibir recompensa
