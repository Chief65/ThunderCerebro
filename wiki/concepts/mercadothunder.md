# Especificación y Arquitectura del Sistema: Mercado Thunder (Lonja Bursátil Diaria)

**Módulo**: Economía y Especulación de Recursos — Servidor Minecraft 1.21.11  
**Inspiración**: Modelo Bursátil de LaLiga Fantasy DAZN (Mercado de Ciclos con Flotación Regulada)  
**Objetivo**: Convertir la venta de materias primas en una mecánica de inversión y especulación viva, eliminando granjas monopolísticas y protegiendo el TPS/MSPT del servidor.

---

## 1. Filosofía y Pilares del Sistema

1. **Separación Estricta de Funciones**:
   - **Tienda Común de Suministros (`/shop`)**: Abastecimiento estable para constructores y aventureros. Precios fijos o con variaciones mínimas. Solo compras.
   - **Lonja de Exportación / Bolsa (`/lonja`, `/bolsaventa`)**: El único punto de venta oficial para la economía productiva (cultivos, minerales, drops de mobs). Los precios fluctúan según el balance oferta/demanda del servidor.

2. **Rendimiento Cero Impacto (Ciclos Diarios vs. Tiempo Real)**:
   - Los precios **NO** se recalculan por cada transacción individual en tiempo real (evita sobrecarga de base de datos y saturación de ticks/MSPT).
   - El mercado funciona por **Jornadas Diarias** (revaluación automática a las 00:00 hora servidor o cada ciclo de 12 horas).

3. **Incentivo a la Especulación y Fin de Monopolios**:
   - Si un clan abusa de una macro-granja de caña o hierro, inundará el mercado. Al día siguiente ese recurso sufrirá un desplome y obligará a rotar a otros métodos de producción.
   - Los jugadores almacenan recursos en cofres/shulkers esperando el ciclo alcista para vender en máximos.

---

## 2. Parámetros Matemáticos y Bandas de Fluctuación

### 2.1 Bandas de Variación Diaria
- **Tasa Máxima de Subida Diaria**: $+15\%$ a $+20\%$ por ciclo.
- **Tasa Máxima de Bajada Diaria**: $-15\%$ a $-20\%$ por ciclo.
- Ningún activo puede multiplicar su valor ni destruirse en una sola jornada.

### 2.2 Techos y Suelos Absolutos (Hard Caps & Hard Floors)
Para evitar inflación destructiva y exploits de duplicación económica:
- **Techo Absoluto (*Hard Cap*)**: $+100\%$ a $+150\%$ respecto al Precio Base ($P_{base}$).
  - *Regla de Oro*: El precio máximo de venta en la lonja debe ser **estrictamente menor** al precio de compra de cualquier suministro en la tienda general para imposibilitar el arbitraje.
- **Suelo Absoluto (*Hard Floor*)**: $-50\%$ a $-60\%$ respecto al Precio Base ($P_{base}$).
  - Ningún recurso baja de su suelo garantizado, asegurando que los jugadores novatos siempre obtengan una compensación mínima.

### 2.3 Deslizamiento de Precio por Venta Masiva (*Slippage Anti-Dump*)
- Para evitar que un clan acumule 100 cofres dobles y los liquide en el segundo 1 del nuevo ciclo vaciando la economía:
  - Primeras 5 shulkers: $100\%$ del valor de mercado del día.
  - Siguientes 10 shulkers: Descuento del $3\%$ progresivo por volumen masivo.
  - Venta extrema (+20 shulkers): Se liquida al precio suelo provisional del día.

---

## 3. Estados de Mercado y Clasificación Visual

| Estado de Mercado | Indicador Visual | Variación Diaria | Comportamiento Sugerido |
| :--- | :--- | :--- | :--- |
| **En Auge Extremo** | `&#59E91F▲ +15% a +20%` (Glow) | Máximo alcista del ciclo | **Momento ideal de venta / vaciar almacenes** |
| **En Auge Moderado** | `&#59E91F▲ +5% a +14%` | Demanda superior a la oferta | Venta recomendada |
| **Estable / Neutro** | `&7= 0%` | Oferta y demanda en equilibrio | Mantener o comerciar al día |
| **A la Baja** | `#FF4D4D▼ -5% a -14%` | Aumento progresivo de stock | Almacenar y esperar recuperación |
| **Desplome / Suelo** | `#FF4D4D▼ -15% a -20%` | Saturación extrema de granjas | **Momento ideal para acumular y no vender** |

---

## 4. Estructura de Datos en Menú y Lore Bursátil

Cada ítem en la interfaz GUI de DeluxeMenus (`lonja_venta.yml`, título `Venta del Día (Temporizador)`) exhibe la siguiente ficha técnica:

```yaml
display_name: '&#FFF275Cactus &8[&#59E91F▲ +18%&8]'
lore:
  - '&8ʙᴏʟꜱᴀ ᴅᴇ ᴠᴀʟᴏʀᴇꜱ'
  - ''
  - ' &8| &fUnidad: &#59E91F&l$&r&#59E91F14.50'
  - ' &8| &fStack x64: &#59E91F&l$&r&#59E91F928.00'
  - ' &8| &fRango: &7$5.00 &8- &7$15.00'
  - ''
  - ' &8| &fHistorial: &#59E91F↗ ↗ ↗ ↗ ↗'
  - '   &7ꜰᴜᴇʀᴛᴇ ᴀʟᴢᴀ'
  - ''
  - ' &8| &fConsejo: &#59E91FVender'
  - '   &7ᴘʀᴇᴄɪᴏ ᴍᴀxɪᴍᴏ'
  - ''
  - ' &8| &fActualización: &e03h 42m'
  - ''
  - '&7▶ Click Izquierdo para vender inventario'
  - '&7▶ Click Derecho para vender 1 stack'
```

---

## 5. Modelo de 5 Cupos Diarios y Pity System

Para evitar monocultivos y canalizar la liquidez del servidor:
1. **5 Cupos Diarios**: Solo 5 ítems cotizan activamente cada jornada.
2. **Pity System Acumulativo**:
   - Cada día que un recurso no sale seleccionado, gana entre un `+5%` y `+8%` de probabilidad adicional acumulada.
   - Al llegar a 7 jornadas sin aparecer en la lonja, el ítem obtiene **Pity Garantizado (100% de probabilidad)** de entrar en el siguiente ciclo diario.
3. **Pronóstico Visible**: Un botón con el catalejo (`SPYGLASS`) muestra el pronóstico del mercado y el top de ítems con mayor probabilidad para el día siguiente.

---

## 6. Hoja de Ruta Técnica para el Plugin / Script

1. **Persistencia de Datos**: Almacenamiento en SQLite (`mercadothunder.db`) del historial de los últimos 7 días por ítem, los contadores de días sin salir (pity) y el volumen diario vendido.
2. **Cron Diaria / Tarea Asíncrona**: Ejecución a las 00:00 para calcular $\Delta P$ (tope ±20%), actualizar historial de flechas, calcular probabilidades con pity y seleccionar los 5 cupos.
3. **Temporizador Dinámico**: PlaceholderAPI `%mercadothunder_cierre%` inyectado en el lore de cada ítem.
