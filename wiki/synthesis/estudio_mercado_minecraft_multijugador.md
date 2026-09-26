# Síntesis Maestra: Estudio de Mercado de Minecraft y Ecosistema Multijugador

**Destinatario**: Sr Ramos  
**Fecha de Publicación**: Septiembre 2026  
**Alcance**: Global, España & Latinoamérica (Mercado Hispanohablante)  
**Herramientas Asociadas**: `thunder-dashboard` (Web Local en puerto 3838) y Skill `analisisdelmes`.

---

## 1. Dimensionamiento Macro y Demanda (TAM / SAM / SOM)

* **TAM Global**:
  * >300 Millones de copias vendidas (videojuego de pago más vendido de la historia).
  * 140M - 170M de Usuarios Activos Mensuales (MAU) en versiones de pago (Java y Bedrock).
  * >600M de usuarios registrados en la versión F2P de NetEase (China).
  * Concurrencia global simultánea: 2,5M a 4,2M CCU.
* **SAM Hispanohablante (Servidores Públicos)**:
  * Universo hispano activo: ~22M - 28M MAU.
  * Jugadores en servidores públicos dedicados: ~7M - 9.5M MAU (~30-35% del total).
  * Concurrencia simultánea en hora pico hispana: 75.000 - 110.000 CCU.
* **SOM (Cuotas de Captura para Red Propia)**:
  * Nivel Inicial: 30 – 80 CCU (~3.500 – 9.000 jugadores únicos/mes). Facturación est.: 150€ – 600€/mes.
  * Nivel Consolidado: 150 – 400 CCU (~18.000 – 45.000 únicos/mes). Facturación est.: 1.200€ – 4.500€/mes.
  * Nivel Referente: 600 – 1.800 CCU (~70.000 – 200.000 únicos/mes). Facturación est.: 6.000€ – 20.000€/mes.

---

## 2. Ecosistema No-Premium y Plataformas

* **Composición en Servidores Hispanos**:
  * España: ~70% Premium oficial, ~30% No-Premium.
  * Latinoamérica: ~78-82% No-Premium (TLauncher, SKLauncher, etc.) y APKs Bedrock gratuitas, ~18-22% Premium.
* **Distribución de Dispositivos**:
  * Bedrock Móvil (Android): ~46.5%.
  * Java PC No-Premium: ~32.0%.
  * Java PC Premium: ~15.5%.
  * Bedrock Consolas (PS/Xbox/Switch): ~6.0%.
* **Directriz Obligatoria**: Soportar modo híbrido (Java + Bedrock vía Geyser/Floodgate con autenticación dual FastLogin/AuthMe). Operar solo en `online-mode=true` reduce el alcance en un ~80%.

---

## 3. Matriz de Benchmarks de Salud (Semáforo Operativo)

| Cuadrante | Métrica Clave | 🟢 Óptimo | 🟡 Alerta | 🔴 Modo de Fallo |
| :--- | :--- | :--- | :--- | :--- |
| **Adquisición** | Nuevos Jugadores / Día | >100 nuevos | 30 – 100 | <30 nuevos |
| **Retención** | Retención D1 (24h) | >25% | 15% – 25% | <15% |
| **Retención** | Retención D7 (7 días) | >10% | 5% – 10% | <5% |
| **Engagement** | Duración Media Sesión | >60 minutos | 30 – 60 min | <20 minutos |
| **Técnico** | MSPT / TPS en Pico | <35 ms (20 TPS) | 35 – 45 ms (19.5 TPS) | >50 ms (<18.5 TPS) |
| **Monetización** | Conversión Tienda | >2.0% | 1.0% – 2.0% | <0.8% |
| **Monetización** | Ticket Medio (ARPPU) | >4,00 € | 2,00 € – 4,00 € | <1,50 € |

---

## 4. Monetización y Pasarelas de Pago en LATAM

* El 67.5% de la facturación en LATAM depende de métodos en efectivo y billeteras locales (**Mercado Pago** y **OXXO**).
* Limitar la tienda a PayPal y tarjeta de crédito internacional reduce la facturación en un 70-80%.
* El modelo óptimo combina micro-transacciones cosméticas y pases de temporada de bajo coste (1€ a 5€).

---

## 5. Escalado al Mercado Anglosajón (US/UK)

* **Multiplicador de ARPU**: Entre 4x y 5x superior al mercado hispanohablante (ticket promedio de 12$ a 30$, conversión del 3.5% al 6.0%).
* **Condición de entrada**: Cero ventajas Pay-to-Win para evitar denuncias al EULA de Mojang; enfoque 90% cosmético.
* **Arquitectura recomendada**: Red unificada multilenguaje (i18n) sobre el proxy Velocity con servidores y lobbies adaptados al locale del jugador.
