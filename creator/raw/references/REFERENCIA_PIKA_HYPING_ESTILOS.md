# Análisis de Referencias de Diseño: PlayHyping y PikaNetwork Store

Documento de extracción técnica y guía de patrones visuales para tiendas de Minecraft Network (ThunderMC).

---

## 1. Referencias Analizadas

### A. PlayHyping (`https://playhyping.com/fr-fr`)
* **Vibe**: Gaming moderno, alegre, enérgico, alta conversión.
* **Tipografía**: `Bakbak One` (títulos en mayúsculas contundentes) + `Poppins` (textos limpios y legibles).
* **Header / Navbar**:
  * Logo temático con glow.
  * Cápsula de conexión verde brillante (*Play Button*) con contador de jugadores en vivo y botón rápido para copiar la IP.
  * Selector de modos de juego en Hero con tarjetas interactivas e iconos 3D rotatorios.

### B. PikaNetwork Store (`https://store.pika-network.net/`)
* **Vibe**: E-commerce gaming de alto volumen, cuadrícula de paquetes con badges y botones de compra directos.
* **Paleta & Tokens**:
  * Fondos: Slate / Dark Pine / Charcoal con bordes suaves (`border-radius: 14px` a `18px`).
  * Botones de Acción: Amarillo/Dorado vibrante (`#ffc845` / `#facc15`) con hover en relieve y sombras difusas.
* **Arquitectura de Tarjetas de Paquetes**:
  * **Badges de Éxito**: `POPULAR` (rosa/magenta `#c650a7`), `BEST VALUE` (oro brillante `#fceb38`), `XX% EXTRA`.
  * **Precios tachados con ángulo**: Efecto visual de descuento llamativo (`strike-through` dinámico).
  * **Botón doble**: Botón cuadrado de `Info [i]` + Botón ancho `Add to Cart` con efecto `card-promo-glow`.

---

## 2. Pautas para el Rediseño de ThunderMC

1. **Cero Formalismo**: Evitar aspectos corporativos o minimalistas aburridos. Usar estética de servidor top de Minecraft.
2. **Jerarquía Visual**:
   * Hero impactante con badges y modos de juego.
   * Sección "Most Popular" / "Mejor Valor" con tarjetas de rangos y paquetes visualmente ricas.
   * Microinteracciones en tarjetas (hover con elevación `-6px`, glow dorado y botones elásticos).
