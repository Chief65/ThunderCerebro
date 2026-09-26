---
title: "Monetizacion ThunderMC — Modelo de Negocio"
type: concept
created: 2026-08-28
updated: 2026-08-28
tags:
  - monetizacion
  - tienda
  - tebex
  - rangos
  - zafiros
  - pase-de-batalla
  - LTV
  - game-design
sources:
  - "Plan de Monetizacion/plan-monetizacion-thundermc.md"
  - "wiki/concepts/economia-servidor-minecraft.md"
  - "wiki/synthesis/thundermc-master-synthesis.md"
---

# Monetizacion ThunderMC — Modelo de Negocio

Modelo de monetizacion de 4 pilares disenado para maximizar el LTV (Lifetime Value) de los jugadores del servidor ThunderMC (Survival 1.21.11).

---

## Los 4 Pilares

### 1. Rangos VIP Permanentes (Producto Ancla)
- **Trueno** (4,99 EUR) — barrera de entrada baja, primer "si"
- **Tormenta** (14,99 EUR) — señuelo de precio medio, el que mas se vende
- **Relampago** (29,99 EUR) — aspiracional, percepcion de estatus
- Implementacion tecnica: LuckPerms Tracks (trueno -> tormenta -> relampago)
- Beneficios: cosmeticos + comodidades (fly, homes) — SIN ventajas P2W en PvP/economia

### 2. Zafiros (Moneda Premium)
- Infraestructura: PlayerPoints (ya instalado) — integracion via Tebex API
- 6 paquetes con bonus creciente (2,99 EUR a 79,99 EUR — el de 79 EUR es "ancla")
- Paquete Popular: 9,99 EUR -> 1.265 Zafiros (foco de conversion)
- Regla clave: precios de items nunca coinciden exactamente con paquetes -> currency overhang
- +50% en primera compra de cualquier paquete (romper barrera psicologica)

### 3. Pase de Batalla de Temporada
- Duracion: 5 semanas (35 dias)
- Precio: 7,99 EUR (version premium)
- Version F2P obligatoria (genera FOMO)
- 50 niveles; recompensas premium: cosmeticos exclusivos + ~2.500 Zafiros totales
- Bundle de lanzamiento: Pase + 500 Zafiros + Cosmético a 11,99 EUR

### 4. Packs de Ofertas y Bundles
- Pack Starter (bienvenida, primeras 48h): Trueno + 400 Zafiros a 6,99 EUR
- Bundle Temporada: Pase + 500 Zafiros + exclusivo a 11,99 EUR
- Pack Invasion (eventos mazmorras): 5 Llaves + 300 Zafiros a 9,99 EUR
- Pack Ascenso (upsell VIP->VIP+): Upgrade + 500 Zafiros a 19,99 EUR

---

## Embudo de Conversion

```
F2P entra -> Retencion (CataMines/pase/misiones) -> FOMO
  -> Primera compra +50% bienvenida -> Currency Overhang (sobras de Zafiros)
    -> Compras progresivas -> Rango (compromiso) -> LTV alto
```

---

## Metricas Clave

| Metrica | Umbral de Alerta |
|---|---|
| % F2P -> Payer | < 2% = redisenar bienvenida |
| ARPPU (ticket medio) | < 8 EUR = optimizar upsell |
| Retencion D7 | < 20% = problema de gameplay |
| LTV objetivo año 1 | > 15 EUR por jugador pagador |

---

## Riesgos Criticos

- **Pay-to-Win agresivo**: kits de rangos deben ser cosmeticos + comodidades, NO generadores de ventaja economica o PvP
- **Inflacion in-game**: auditar items de kits antes del lanzamiento
- **Legal UE**: probabilidades de cajas publicas + solo compra de llaves con Zafiros (no euros directos) + T&C claros

---

## Enlaces Relacionados

- Plan completo: Plan de Monetizacion/plan-monetizacion-thundermc.md
- Economia base: wiki/concepts/economia-servidor-minecraft.md
- Sintesis maestra: wiki/synthesis/thundermc-master-synthesis.md
- LuckPerms (rangos): wiki/entities/thundermc/core-infrastructure/luckperms.md
- PlayerPoints (Zafiros): wiki/entities/thundermc/economy-progression/playerpoints.md
- ExcellentCrates (llaves): wiki/entities/thundermc/economy-progression/excellentcrates.md
- Tienda web: Instalacion Tebex/
