---
title: "Plan Maestro de Monetización — ThunderMC"
type: synthesis
created: 2026-08-28
updated: 2026-08-28
tags:
  - monetizacion
  - tienda
  - tebex
  - rangos
  - zafiros
  - pase-de-batalla
  - game-design
  - negocio
sources:
  - "Estrategia_Monetizacion_Servidor_Minecraft.md (raw)"
  - "wiki/entities/thundermc/core-infrastructure/luckperms.md"
  - "wiki/entities/thundermc/economy-progression/excellentcrates.md"
  - "wiki/entities/thundermc/economy-progression/playerpoints.md"
  - "wiki/concepts/economia-servidor-minecraft.md"
  - "wiki/synthesis/thundermc-master-synthesis.md"
---

# Plan Maestro de Monetizacion — ThunderMC

## 0. Contexto del Servidor (Base Técnica Real)

| Variable | Estado Actual |
|---|---|
| **Version** | Paper 1.21.11 |
| **Modo de Juego** | Survival (20kx20k), Nether (10kx10k), End (10kx10k con reset programado) |
| **Sistema de Rangos** | LuckPerms 5.5.42 — Tracks configurados, herencia DAG, metadata/prefijos |
| **Economia In-Game** | Vault + QuickShop-Hikari / SellGUI / ZelAuction |
| **Progresion** | CataMines (mineria progresiva), Jobs-Reborn (multiempleo), RankUp (ascenso por minas) |
| **Loot Boxes** | ExcellentCrates (sistema de llaves y cajas) |
| **Moneda Premium (candidata)** | PlayerPoints — ya instalado, integrado con PAPI y Vault |
| **RPG / Contenido** | MythicMobs (10 mazmorras + bosses), ExecutableItems, ItemEdit, ExcellentEnchants |
| **Tienda Web** | Tebex Headless API — cuenta 1171683 (ThunderMC) — plantilla personalizada lista en Instalacion Tebex/ |
| **Chat / Prefijos** | TAB + ZelChat + AlonsoTags (prefijos visuales de rangos en tablist y chat) |

---

## 1. Resumen Ejecutivo del Modelo

El modelo elegido combina 4 pilares que se refuerzan entre si en un embudo completo de monetizacion:

```
F2P entra -> Retencion (pase/misiones/CataMines) -> FOMO
  -> Primera compra +50% bienvenida -> Currency Overhang
    -> Compras progresivas -> Rango (compromiso)
      -> Comprador recurrente cada temporada -> LTV alto
```

| Pilar | Rol en el Embudo | Ingresos |
|---|---|---|
| **3 Rangos VIP permanentes** | Producto ancla / conversion inicial | Ingreso base estable |
| **Zafiros (moneda premium)** | Gasto recurrente e impulsivo | Ingresos continuos |
| **Pase de Batalla (4-6 semanas)** | Retencion diaria + FOMO | Ingresos por temporada |
| **Packs de Ofertas / Bundles** | Maximizar ticket medio | Picos por evento/lanzamiento |

---

## 2. Pilar 1 — Rangos VIP Permanentes

### 2.1 Arquitectura de Rangos

| Rango | Precio Sugerido | Posicionamiento | Rol en la Estrategia |
|---|---|---|---|
| **LITE** (VIP) | 4,99 EUR | Acceso basico | Baja barrera de entrada, primer "si" |
| **STAR** (VIP+) [MAS POPULAR] | 14,99 EUR | Rango medio señuelo | El que mas debe venderse — efecto ancla |
| **MEGA** (MVP) | 29,99 EUR | Premium exclusivo | Aspiracional, percepcion de estatus |

Precio no lineal deliberado (4.99 / 14.99 / 29.99): el jugador indeciso siempre convergera a STAR (efecto señuelo clasico de precios).

### 2.2 Estructura de Beneficios por Rango (Acumulativos)

**LITE — 4,99 EUR**
- Prefijo [LITE] en chat y tablist (TAB + ZelChat + AlonsoTags)
- 1 /home adicional (total: 4)
- Acceso a /nick (personalizacion de nombre)
- Particulas basicas (cosmético)
- Regalo cruzado: 200 Zafiros al comprar

**STAR — 14,99 EUR**
- Prefijo [STAR] en chat y tablist
- 3 /home adicionales (total: 6)
- Comando /fly en zonas no PvP (comodidad clave, no P2W)
- Alas/particulas de nivel medio (cosmeticos)
- Acceso prioritario a eventos y mazmorras (5 min antes)
- Regalo cruzado: 500 Zafiros al comprar

**MEGA — 29,99 EUR**
- Prefijo animado [MEGA] en chat y tablist
- /home ilimitados (o max configurado, ej. 15)
- Fly en todos los mundos no-PvP
- Tag exclusivo [MEGA] en el tag system de AlonsoTags
- NPC personalizado en el Spawn (FancyNPCs) con el nombre del jugador durante 1 mes
- Acceso a canal VIP en Discord (via integracion Tebex->Discord)
- Regalo cruzado: 1.200 Zafiros al comprar

### 2.3 Integracion Tecnica (LuckPerms)

Track en LuckPerms:
```
Track "vip": default -> LITE -> STAR -> MEGA
```

Comandos en Tebex para activacion automatica:
```
lp user {username} parent set LITE
lp user {username} parent set STAR
lp user {username} parent set MEGA
```

RIESGO FATAL: NUNCA usar comodines amplios (essentials.*, worldedit.*) en grupos VIP.
Asignar permisos explicitos uno a uno. Revisar seccion 7 de wiki/entities/thundermc/core-infrastructure/luckperms.md

---

## 3. Pilar 2 — Zafiros (Moneda Premium)

### 3.1 Por que Zafiros y no euros directos

- Desconecta el valor real -> menor friccion psicologica al gastar
- Permite currency overhang (sobras que empujan a la siguiente compra)
- Capa de separacion legal entre dinero real y loot boxes
- La infraestructura tecnica de Zafiros se definira con la economia custom (PENDIENTE — no tocar hasta que este lista)

### 3.2 Tabla de Paquetes

| Paquete | Precio | Zafiros base | Bonus | Total | Zaf/EUR | Rol |
|---|---|---|---|---|---|---|
| Bolsa Pequeña | 2,99 EUR | 250 | 0% | 250 | 84 | Impulso / Prueba |
| Bolsa Mediana | 4,99 EUR | 500 | +10% | 550 | 110 | Compra recurrente |
| **Bolsa Popular** | 9,99 EUR | 1.100 | +15% | 1.265 | 127 | Foco de conversion |
| Bolsa Grande | 19,99 EUR | 2.300 | +20% | 2.760 | 138 | Jugadores dedicados |
| Bolsa XL | 39,99 EUR | 4.800 | +25% | 6.000 | 150 | Whales |
| **Caja del Tesoro (Ancla)** | 79,99 EUR | 10.000 | +30% | 13.000 | 162 | Hace razonables los otros |

### 3.3 Reglas de Diseño

- Precios terminados en .99 siempre
- Precios de items nunca coinciden exactamente con paquetes -> garantiza sobras
- +50% bonus en la primera compra de cualquier paquete
- Oferta flash semanal o de evento con tasa mejorada temporal

### 3.4 Integracion Tecnica (PENDIENTE)

La entrega de Zafiros via Tebex se definira cuando este lista la economia custom que los implementa de forma nativa.
No se usara PlayerPoints — sera sustituido por el plugin de economia custom con Zafiros integrados.

---

## 4. Pilar 3 — Pase de Batalla de Temporada

| Variable | Valor Recomendado | Razon |
|---|---|---|
| **Duracion** | 5 semanas (35 dias) | Punto dulce: suficiente sin aburrir |
| **Precio** | 7,99 EUR (premium) | Accesible, no compite con rango STAR |
| **Version F2P** | Si — recompensas basicas | FOMO -> compra a mitad de temporada |
| **Niveles totales** | 50 niveles | Suficiente contenido |
| **Recompensas F2P** | 5-10 Zafiros/nivel, cosmeticos menores | Mantiene F2P enganchado |
| **Recompensas Premium** | Cosmeticos exclusivos, 50-100 Zaf/nivel | El diferencial debe ser VISIBLE y ENVIDIABLE |

### 4.1 Economia Interna

- Zafiros totales en 50 niveles premium: ~2.500 (el pase "paga" ~25% de su valor en Zafiros)
- Cosmético exclusivo de temporada (no repetido): 1 tag + 1 particula o mascota

### 4.2 Monetizacion Extra

- Compra de niveles con Zafiros (ej. 150 Zafiros/nivel) para quien no tiene tiempo
- Bundle de lanzamiento: Pase Premium + 500 Zafiros + Cosmético exclusivo a 11,99 EUR (ahorro vs. 12,98 EUR por separado)

### 4.3 Nota Tecnica de Implementacion

Opciones de plugin para 1.21.11:
1. BattlePass by Plajer (SpigotMC) — integra con PAPI, Jobs, MythicMobs y PlayerPoints
2. QuestCreator + PlayerPoints + recompensas escalonadas por misiones
3. Solucion Custom con ThunderMines (mayor control y marca propia)
RECOMENDACION: BattlePass plugin + PlayerPoints como moneda de Zafiros

---

## 5. Pilar 4 — Packs de Ofertas y Bundles

**Pack Starter (Bienvenida) — 6,99 EUR**
- Rango LITE + 400 Zafiros + Kit de Inicio exclusivo
- Target: nuevos jugadores en sus primeras 48h (ventana de mayor intencion de compra)
- Disponible solo durante X dias desde el primer login

**Bundle Temporada — 11,99 EUR**
- Pase de Batalla Premium + 500 Zafiros + Cosmético exclusivo de temporada
- Alta conversion por percepcion de ahorro
- Disponible solo los primeros 7 dias de la temporada

**Pack Invasion (evento tematico mazmorras) — 9,99 EUR**
- 5 Llaves de Mazmorra + 300 Zafiros + Kit de Mazmorra
- Alineado con los 10 dungeons de MythicMobs del servidor
- Halloween, aniversario del servidor

**Pack Ascenso — 19,99 EUR**
- Upgrade de LITE a STAR (descuento del precio completo) + 500 Zafiros
- Target: jugadores que ya tienen VIP y quieren subir — reduce friccion del upsell

Reglas de packs:
- Mostrar siempre el valor real (suma de componentes) y el ahorro
- Packs de eventos: tiempo limitado y NUNCA exactamente repetidos
- Maximo 2-3 packs activos simultaneamente

---

## 6. Tacticas In-Game de Conversion

| Tactico | Plugin | Implementacion |
|---|---|---|
| Anuncio en chat de compras | ZelChat | Mensaje global formateado via Tebex webhook |
| Holograma Top Donadores | FancyHolograms | PAPI %vault_top_balance_X% |
| NPC Tienda en Spawn | FancyNPCs | Rotacion de ofertas, TP a /tienda |
| Cosmeticos visibles | GSit + particulas de rangos | Prefijos y particulas en TAB/LuckPerms |

Momentos de conversion clave:
- Primer login: mensaje bienvenida + oferta +50% primera compra
- Nivel de mina alto: "Los VIP desbloquean [beneficio extra]"
- Intento de /fly sin rango: "El comando /fly es exclusivo de STAR+ — consiguelo en /tienda!"
- 3 dias antes fin de temporada: boss bar countdown + Discord @everyone
- Login en evento: mensaje especial con pack de evento

---

## 7. Jerarquia Visual de la Tienda Web

Orden de categorias en Instalacion Tebex/index.html:
1. Rangos VIP (arriba del todo — producto ancla)
2. Pase de Batalla (banner grande + countdown si activo)
3. Packs y Bundles ("Ofertas")
4. Zafiros (pestaña separada o seccion inferior)
5. Llaves y Cajas (seccion inferior)

STAR debe estar marcado como "Mas Popular" / "Recomendado"

---

## 8. Compliance Legal (España / UE)

| Obligacion | Estado | Accion |
|---|---|---|
| Transparencia de probabilidades en cajas | PENDIENTE | Publicar tabla por caja (ExcellentCrates las tiene) |
| Moneda premium como intermediario de loot boxes | CORRECTO (Zafiros->Llaves) | Mantener: nunca llaves directas con euros |
| Terminos y condiciones + No reembolso | PENDIENTE | Anadir pagina /terms en cmspage.html |
| No marketing dirigido a menores | PENDIENTE | Revisar tono en Discord/redes |

---

## 9. Metricas Clave Post-Lanzamiento

| Metrica | Que mide | Umbral de Alerta |
|---|---|---|
| % F2P -> Payer | Salud del embudo de entrada | < 2% = redisenar primera oferta/bienvenida |
| ARPPU (ticket medio pagador) | Efectividad de packs/señuelo | Si < 8 EUR -> optimizar upsell y bundles |
| ARPU (gasto medio por jugador total) | Salud economica global | Ref: top servers ~0.5-2 EUR/jugador activo/mes |
| Retencion D1 / D7 / D30 | Sin retencion no hay ventas futuras | D7 < 20% = problema de gameplay, no de monetizacion |
| % completado del pase | Ajustar duracion/dificultad | > 80% = pase demasiado facil, subir niveles |
| Tasa de recompra | Funciona el currency overhang? | < 15% en 30 dias = ajustar precios de items |
| LTV | Metrica maestra | Objetivo año 1: > 15 EUR por jugador pagador |

---

## 10. Riesgos Fatales y Modos de Fallo

| Riesgo | Probabilidad | Impacto | Mitigacion |
|---|---|---|---|
| Pay-to-Win agresivo en PvP/economia | Media | Alto — fuga de F2P | Limitar kits a cosmeticos + comodidades; sin equipo P2W que domine PvP |
| Currency overhang excesivo sin gastar | Media | Medio — devalua la moneda | Flash sales semanales + nuevos cosmeticos cada temporada |
| Pase de batalla demasiado largo | Media | Alto — baja retencion | 5 semanas max; misiones diarias de 15-30 min |
| Chargebacks / Fraudes de pago | Baja | Alto — cuenta Tebex suspendida | T&C claros, politica de no reembolso, Tebex antifraude nativo |
| Exploit de entrega de rangos doble | Baja | Medio | Usar {uuid} en comandos Tebex, no {username} |
| Queja legal por cajas | Baja | Muy Alto | Probabilidades publicas + solo compra con Zafiros + T&C claro |
| Inflacion in-game por kits de rangos | Media | Alto | Auditoria de items de kits antes del lanzamiento |

---

## 11. Checklist de Lanzamiento

### Tienda y Productos
- [ ] 3 rangos (LITE / STAR / MEGA) con beneficios escalonados y precios no lineales
- [ ] Paquetes de Zafiros configurados en Tebex con bonus creciente y precios .99
- [ ] Bonus +50% primera compra configurado (cupon automatico de bienvenida)
- [ ] Packs de Ofertas (Starter, Bundle Temporada, Pack Invasion) creados en Tebex
- [ ] Llaves/cajas configuradas en ExcellentCrates con probabilidades definidas
- [ ] Pase de Batalla configurado (plugin + integracion PlayerPoints/Zafiros)
- [ ] Pagina /terms con T&C y probabilidades de cajas publicadas

### Infraestructura Tecnica
- [ ] Comandos de entrega en Tebex para rangos (LuckPerms) — Zafiros: pendiente economia custom
- [ ] Webhook de Tebex -> chat de ThunderMC para anuncio de compras
- [ ] Comando /tienda configurado y accesible desde cualquier mundo
- [ ] GUI in-game del pase de batalla accesible desde inventario
- [ ] Boss bar / scoreboard con countdown activo de temporada
- [ ] Mensaje de bienvenida con oferta de primera compra activado en join

### Tienda Web
- [ ] Jerarquia visual correcta (Rangos -> Pase -> Packs -> Zafiros)
- [ ] Rango STAR marcado como "Mas Popular" / "Recomendado"
- [ ] Hero Slider con banner de temporada activa y countdown
- [ ] Ticker de compras recientes activo
- [ ] Top Donadores visible en homepage

### In-Game Conversion
- [ ] Holograma Top Donadores en spawn (FancyHolograms)
- [ ] NPC de tienda en spawn (FancyNPCs)
- [ ] Mensajes contextuales de conversion
- [ ] Sistema de votacion con recompensa en Zafiros

### Legal
- [ ] Probabilidades de cajas publicadas en Tebex (por caja, visible antes de comprar)
- [ ] Plan de contenido Discord para lanzamiento
- [ ] Showcase de cosmeticos en video corto (TikTok/Shorts/Reels)

---

## 12. Proximos Pasos Inmediatos (Orden de Prioridad)

1. Definir los beneficios exactos de los 3 rangos LITE / STAR / MEGA (permisos/comandos por rango) — kits para mas adelante
2. Configurar los grupos en LuckPerms (lite, star, mega) con Track "vip"
3. Crear los productos en Tebex con comandos de entrega correctos (LuckPerms)
4. Finalizar jerarquia visual de la tienda en Instalacion Tebex/index.html (STAR marcado "Mas Popular")
5. Esperar a que la economia custom con Zafiros este lista antes de configurar los paquetes de moneda premium
6. Decidir el plugin de Pase de Batalla (BattlePass vs. custom ThunderMines)
7. Redactar T&C y probabilidades de cajas para cumplimiento legal UE

---

## Referencias Cruzadas
- Índice General: [[index|Índice Maestro ThunderCerebro]]
- Concepto Base: [[wiki/concepts/monetizacion-modelo-negocio|Modelo de Negocio & Monetización]]
- Macro-Arquitectura: [[wiki/synthesis/thundermc-master-synthesis|Síntesis Maestra ThunderMC]]
- Estudio Económico: [[wiki/synthesis/estudio_mercado_minecraft_multijugador|Estudio de Mercado Multijugador]]
- Ecosistema Completo: [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema de Plugins]]
- Gestión de Rangos: [[wiki/entities/thundermc/core-infrastructure/luckperms|LuckPerms]]
- Moneda Premium: [[wiki/entities/thundermc/economy-progression/playerpoints|PlayerPoints]]
- Cajas de Recompensas: [[wiki/entities/thundermc/economy-progression/excellentcrates|ExcellentCrates]]

