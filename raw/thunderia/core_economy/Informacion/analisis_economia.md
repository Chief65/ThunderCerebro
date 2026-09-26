# 📊 Análisis de Economía — ThunderStudios Survival
> Última actualización: 2026-08-18 | Fuente: Core/Economia_Actual (minas + dungeons + shop)

---

## 🗺️ Visión General del Ecosistema Económico

El servidor opera con **dos monedas paralelas** y **tres fuentes principales de ingreso**. Entender cómo se relacionan es clave para saber dónde pone el tiempo un jugador.

| Moneda | Símbolo | Fuente principal | Gasto principal |
|--------|---------|------------------|-----------------|
| Dinero | $ (Vault) | Minas, Dungeons, Shop venta | Shop compra, comercio jugador |
| Almas | ⚡ (PlayerPoints) | Dungeons (mobs/jefes) | Spawners, Llaves, Protecciones |

> Las Almas **no se generan en minas** — son exclusivas del sistema de Dungeons. Esto crea una dependencia directa entre ambos sistemas.

---

## ⛏️ SISTEMA 1 — Minas (CataMines)

**Naturaleza:** Farmeo pasivo, AFK-friendly, escalado por rango.

### Mecánica económica
- Cada bloque de **Amatista** garantiza **1 Cristal Estelar → $10** vía `/sellgui`
- Drops secundarios: Bolsas de Dinero ($500–$2,000) y Piezas de Llave (rarísimas)
- El bloque de Piedra es relleno — no produce valor

### Ingreso base por 100 bloques minados

| Mina | % Amatista | $$ garantizado | Rango requerido |
|------|:----------:|:--------------:|:---------------:|
| Inicial | 20.25% | ~$202 | Inicial |
| Knight | 30.25% | ~$302 | Knight |
| Héroe | 40.25% | ~$402 | Héroe |
| Legend | 50.25% | ~$502 | Legend |
| Mythic | 60.25% | ~$602 | Mythic |
| Titan | 70.25% | ~$702 | Titan |
| PvP | 80.00% | ~$800 | Titan + riesgo PvP |

### Ingresos esperados por sesión (estimado)
> Asumiendo ~500 bloques minados en una sesión activa de ~10 minutos (reset: 3-4 min, varios ciclos):

| Mina | $$ base (500 bloques) | Total estimado con Bolsas |
|------|:---------------------:|:--------------------------:|
| Inicial | ~$1,010 | ~$1,000–$1,500 |
| Knight | ~$1,512 | ~$1,500–$2,000 |
| Héroe | ~$2,012 | ~$2,000–$2,500 |
| Legend | ~$2,512 | ~$2,500–$3,500 |
| Mythic | ~$3,012 | ~$3,000–$4,500 |
| Titan | ~$3,512 | ~$3,500–$5,500 |
| PvP | ~$4,000 | ~$4,000–$6,000 ⚠️ PvP |

### Fuente de Piezas de Llave en Minas
- Minas altas (Titan/PvP) son fuente de Piezas Mítica y Pieza Limited (PvP exclusivo en minas)
- Estas piezas tienen valor de mercado entre jugadores al estar ligadas a cofres de recompensa

---

## ⚔️ SISTEMA 2 — Dungeons (MythicMobs)

**Naturaleza:** Combate activo, requiere equipo, riesgo/recompensa alto.

### Mecánica económica
- Cada kill genera **$ Dinero + ⚡ Almas** de forma garantizada
- Drops secundarios: Fragmentos de Llave (2% Super/Rara/Gadget, 0.3% Mítica, 0.1% Limited)
- Mobs élite (Portero M8, Espíritu Helado M7) dan el **doble** de recompensa base
- Jefes: máxima concentración de valor por enfrentamiento (requieren skill)

### Ingreso por mazmorra — Estimado por sesión activa (~10 min)
> Asumiendo limpieza de sala completa, ciclos de respawn incluidos:

| Mazmorra | $/kill prom. | ⚡/kill prom. | $$ sesión | ⚡ sesión | Drop Notable |
|----------|:------------:|:------------:|:---------:|:---------:|:-------------|
| M1 — Establos | $12 | +1.3 | ~$480 | ~52 | — |
| M2 — Galerías | $26 | +2.7 | ~$910 | ~95 | Gadget 2% |
| M3 — Ruinas | $38 | +3.7 | ~$1,140 | ~111 | Mítica 0.3% |
| M4 — Santuario | $63 | +5.3 | ~$1,575 | ~133 | Limited 0.1% |
| M6 — Arañas | $45 | +4 | ~$1,350 | ~120 | Limited 0.1% |
| M7 — Helada | $65 | +6 | ~$1,625 | ~150 | Diamond drop |
| M8 — Forja | $65 | +6 | ~$1,625 | ~150 | Blaze Rod exclusivo |

### Ingresos de Jefes (por kill)

| Jefe | HP | $ Kill | ⚡ Kill | Drop destacado | Frag. Mítica | Frag. Limited |
|------|----|:------:|:-------:|----------------|:------------:|:-------------:|
| Aracne (M6) | 2,000 | $1,000 | +30 | String + XP | 0.3% | 0.1% |
| Frostal (M7) | 1,500 | $1,200 | +40 | Diamond 10% | 0.3% | 0.1% |
| Hefesto (M8) | 2,500 | $1,200 | +40 | Diamond 10% | 0.3% | 0.1% |
| Cerbero (Especial) | 2,000 | $600 | +25 | 4-7 Diamantes + Llave Super garantizada | **2.5%** | 0.1% |

> 💡 **Cerbero es el jefe más eficiente en drops:** su recompensa incluye llave garantizada + 4-7 diamantes + 15% fragmentos (vs 2% del resto). Aunque da menos $, el valor total por kill supera a Hefesto y Frostal.

---

## 🛒 SISTEMA 3 — Shop (ShopGUI+)

**Naturaleza:** Convertidor económico. No genera dinero por sí solo — transforma recursos en $ o consume $ en mejoras.

### Rol del Shop en la economía

El Shop actúa como **regulador y sumidero** del dinero del servidor. Sus funciones son:

1. **Venta de recursos** farmados (mobs, bloques, comida) → entrada de $ al jugador
2. **Compra de mejoras** (encantamientos $50k, spawners ⚡, protecciones ⚡) → salida de $ y ⚡
3. **Precio de referencia** para el mercado jugador-jugador (QuickShop)

### Fuentes de ingreso vía Shop (los más relevantes para vender)

| Item | Precio venta | Origen | Ruta de obtención |
|------|:------------:|--------|-------------------|
| NETHERITE_BLOCK | $4,000 | Exploración/farmeo | End + Netherite scraps |
| DIAMOND_BLOCK | $600 | Minas/Dungeons | Drop M7/M8/Cerbero |
| EMERALD_BLOCK | $400 | Farmeo/villagers | Aldeas + trading |
| STRING | $15/ud | Dungeons M6 | Araña Mutante/Venenosa |
| COCOA_BEANS | $30/ud | Farmeo | Jungla + granja |
| Cristal Estelar | $10/ud | Minas (exclusivo) | Bloque Amatista roto |
| IRON_BLOCK | $40 | Dungeons/farmeo | Spawner Golem + drop M2+ |
| MAGMA_CREAM | $20/ud | Dungeons M8 | Drop Espíritu Fuego |
| SHULKER_SHELL | $45/ud | End | Shulkers del End |

### El Shop como sumidero de Almas ⚡

| Item | Coste ⚡ | Valor estratégico |
|------|:-------:|-------------------|
| Spawner Golem Hierro | 1,350 | ROI alto — genera iron pasivo → $40/bloque en shop |
| Spawner Blaze | 900 | ROI medio — blaze rods para encantamientos |
| Llave Mítica | 3,000 | Acceso a cofres de alta rareza |
| Llave Limited | 10,000 | Cofre más exclusivo del servidor |
| Protección 128x128 | 1,000 | Seguridad de base a largo plazo |

---

## 🔗 CO-RELACIÓN ENTRE LOS TRES SISTEMAS

```
MINAS ─────────────────────────────────────────────────────────────────┐
│  Genera: $ (Cristal Estelar → $10 c/u via /sellgui)                 │
│  Genera: Piezas de Llave (Super → Limited según tier de mina)        │
│  NO genera: Almas ⚡                                                  │
│                         ↓                                             │
│         $ entra al bolsillo del jugador                               │
│         Piezas van a /llaves → Cofres con loot vendible               │
│                                                                       │
DUNGEONS ───────────────────────────────────────────────────────────────┤
│  Genera: $ (kills de mobs + jefes)                                   │
│  Genera: Almas ⚡ — ÚNICA fuente del servidor                         │
│  Genera: Fragmentos de Llave (misma pool que minas)                   │
│  Genera: Drops vendibles en Shop (String $15, Magma $20, Diamond)     │
│                         ↓                                             │
│         $ + ⚡ + materiales vendibles                                 │
│                                                                       │
SHOP ───────────────────────────────────────────────────────────────────┤
│  Convierte: materiales de Minas/Dungeons en $                        │
│  Gasta: ⚡ en mejoras de largo plazo (spawners, llaves)               │
│  Gasta: $ en encantamientos, equipamiento                             │
│  Actúa como: referencia de precio para el QuickShop P2P              │
└───────────────────────────────────────────────────────────────────────┘
```

### Flujo económico tipo de un jugador avanzado

```
1. MINAS (rango Titan)
   → Farmear Cristales Estelares → /sellgui → $$$ garantizados
   → Drop eventual: Pieza Mítica/Limited → /llaves o venta a otros jugadores

2. DUNGEONS (M7/M8 o Cerbero)
   → Kills → $ + ⚡ Almas acumuladas
   → Drops (Diamond, String, Magma) → Shop → $$ extra por encima del kill
   → Fragmentos → /llaves → Cofres (contenido vendible en QuickShop)

3. SHOP
   → Gastar ⚡ acumuladas en Spawner Golem de Hierro (1,350 ⚡)
   → Spawner genera Iron pasivo → Iron Block → Shop → $40/bloque
   → Ciclo autosostenido de ingreso pasivo que amplifica las otras fuentes
```

### Dependencias clave entre sistemas

| Relación | Descripción | Importancia |
|----------|-------------|:-----------:|
| Minas → Shop | Cristal Estelar solo vendible vía /sellgui (no entra al shop normal) | 🔴 Crítica |
| Dungeons → Almas ⚡ | Única fuente de Almas — sin dungeons no hay spawners ni llaves | 🔴 Crítica |
| Dungeons → Shop | Drops de mobs (String $15, Magma $20, Diamond) se venden en Shop | 🟡 Media |
| Minas + Dungeons → Llaves | Ambos generan Piezas de Llave — se combinan en /llaves | 🟡 Media |
| Shop → Spawners → $ | Gasto de ⚡ → recursos pasivos → más $ en Shop (ciclo virtuoso) | 🟢 Sinérgica |
| Mina PvP → Limited | Única fuente de Pieza Limited en minas (riesgo PvP requerido) | 🟡 Media |

---

## 🏆 RANKING DE RENTABILIDAD

### Por ingreso en $ (Vault) — sesión de 10 minutos

| # | Actividad | $$/sesión estimado | Dificultad | Riesgo |
|:-:|-----------|:-----------------:|:----------:|:------:|
| 🥇 | **Mina PvP (rango Titan)** | $4,000–$6,000 | Baja | ⚠️ PvP activo |
| 🥈 | **Mina Titan** | $3,500–$5,500 | Baja | Ninguno |
| 🥉 | **Dungeon M8 + Jefe Hefesto** | $2,800–$4,500 | Alta | Medio-alto |
| 4 | Dungeon M7 + Jefe Frostal | $2,600–$4,000 | Alta | Medio |
| 5 | Mina Mythic | $3,000–$4,500 | Baja | Ninguno |
| 6 | Dungeon M4 Santuario Piglin | $2,000–$3,000 | Media | Medio |
| 7 | Cerbero (jefe especial) | $1,500–$2,500 + loot | Muy alta | Alto |
| 8 | Mina Legend | $2,500–$3,500 | Baja | Ninguno |

### Por ingreso en ⚡ Almas — sesión de 10 minutos

| # | Actividad | ⚡/sesión estimado | Notas |
|:-:|-----------|:-----------------:|-------|
| 🥇 | **Dungeon M8 — Forja Ardiente** | ~150–200 ⚡ | Portero da +10 ⚡ (doble) |
| 🥈 | **Dungeon M7 — Prisión Helada** | ~150–200 ⚡ | Espíritu da +10 ⚡ (doble) |
| 🥉 | **Jefe Hefesto / Frostal (por kill)** | +40 ⚡ | Solo por kill de jefe |
| 4 | Dungeon M4 Santuario Piglin | ~100–130 ⚡ | +4-8 por mob |
| 5 | Mina X (cualquiera) | **0 ⚡** | Las minas NO generan Almas |

### Por valor total combinado ($ + ⚡ convertidas + drops vendibles)

| # | Actividad | Valor total estimado | Por qué |
|:-:|-----------|:--------------------:|---------|
| 🥇 | **Mina Titan + Dungeon M8 alternando** | $5,000–$8,000/h equiv. | Complemento perfecto: minas = $ pasivo, dungeons = ⚡ + drops |
| 🥈 | **Mina PvP (con equipo full)** | $4,500–$7,000/h equiv. | Máximo $ bruto pero riesgo PvP |
| 🥉 | **Dungeon M8 con farm de Portero** | $3,500–$5,000/h + ⚡ | Portero 100HP da doble recompensa |
| 4 | **Cerbero farm repetido** | $2,000–$4,000/h + loot | Llave garantizada por kill = valor extra en cofres |

---

## 💡 CONCLUSIONES ESTRATÉGICAS

### ¿Cuál es la actividad más rentable?

> **En $ puro: Mina Titan o Mina PvP.**
> Son las más rentables en $ bruto porque la mecánica de minería es AFK-friendly, sin riesgo de muerte y el reset es automático. Un jugador con rango Titan puede acumular **$3,500–$5,500 por sesión de 10 minutos** sin ningún peligro.

> **En economía completa ($ + ⚡ + items): Dungeon M8.**
> Es el único sistema que genera Almas ⚡ (moneda escasa e infarmeable en minas), drops vendibles exclusivos (Blaze Rod, Magma Cream) y fragmentos de llave a buen ritmo. La combinación $ + ⚡ lo hace insustituible para la progresión.

> **Actividad más eficiente por sinergia: Minas (Titan) + Dungeons (M7/M8).**
> El jugador optimizado alterna ambas: farmea cristales en minas para acumular $ rápido, y hace runs de dungeon para acumular ⚡ que luego invierte en spawners → generando un ciclo de ingreso pasivo que amplifica ambas fuentes.

### Puntos de atención económicos

| Observación | Impacto |
|-------------|---------|
| 🔴 Las Almas son escasas y solo vienen de dungeons | Jugadores que solo minan no pueden comprar spawners ni llaves top |
| 🔴 El Cristal Estelar no existe en el shop de compra | No hay forma de inflar el valor artificialmente — precio fijo y estable |
| 🟡 Los drops de dungeon (String, Magma) tienen precio bajo en shop | El shop subutiliza el valor de los drops de combate |
| 🟡 Cerbero da la llave más valiosa pero poco $ directo | Su verdadero valor está en el loot de cofre, no en el kill |
| 🟢 El ciclo Dungeon → ⚡ → Spawner → Iron → Shop → $ es sostenible | Crea progresión autónoma sin depender únicamente de las minas |
| 🟢 La Mina PvP da Pieza Limited exclusiva | Único modo de obtenerla en minas — incentivo real para el riesgo PvP |
