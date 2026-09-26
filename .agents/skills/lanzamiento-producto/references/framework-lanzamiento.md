# FRAMEWORK DE LANZAMIENTO DE PRODUCTO

**De la intuición al dato: proceso estructurado para Garza**

Alejandro Campos | Imprex & Garza | Febrero 2026 | v1.0

---

## Contexto y problema

Este framework nace de una necesidad real: sustituir la práctica heredada de decidir qué producto lanzar en función del coste del proveedor y el precio de los bestsellers. Esa heurística, aunque funcional cuando no hay datos, condena a Garza a competir siempre en precio y en modo reactivo.

El objetivo es construir un proceso repetible que parta del mercado y el consumidor para llegar al producto, no al revés. No se trata de un modelo académico ideal, sino de un framework adaptado a la realidad operativa de Garza: datos B2B mayoritarios, incipiente captura B2C vía Shopify, acceso limitado a GFK (coste) y uso de Helium10 para Amazon.

**Principio clave:** cada fase produce un entregable concreto que alimenta la siguiente. Si una fase no puede completarse por falta de datos, se documenta la hipótesis utilizada y se marca para validación posterior.

---

## Visión general del proceso

El framework consta de 7 fases. Las fases 1 y 2 son iterativas entre sí (no estrictamente secuenciales). La fase 3 (análisis competitivo) actúa como bisagra que conecta la comprensión del mercado con las decisiones de producto.

| # | Fase | Pregunta clave | Output principal |
|---|------|---------------|-----------------|
| 1 | Exploración de mercado | ¿Qué hay ahí fuera? ¿Cuánto se vende, dónde y quién lidera? | Mapa de mercado: tamaño, canales, players, tendencias |
| 2 | Buyer persona | ¿Quién compra, por qué, qué valora y qué le frustra? | Perfil(es) de buyer persona con drivers de decisión |
| 3 | Análisis competitivo | ¿Qué propuesta de valor ofrece cada competidor y dónde hay huecos? | Mapa competitivo + oportunidades de diferenciación |
| 4 | Definición de producto | ¿Qué producto fabricar con qué características y a qué precio? | Brief de producto + pricing + requisitos de calidad |
| 5 | Dimensionamiento | ¿Cuántas unidades fabricar para la primera tirada? | Plan de producción con escenarios (conservador, base, optimista) |
| 6 | Posicionamiento y comunicación | ¿Qué mensaje, a quién y por qué canal? | Brief creativo + assets de venta + plan de medios |
| 7 | Go-to-market y seguimiento | ¿Cómo lanzamos y cómo medimos? | Plan de lanzamiento + KPIs + ciclo de feedback |

---

## Fase 1: Exploración de mercado

**Objetivo:** entender el terreno antes de decidir nada. Aquí respondemos al «qué hay» y al «cuánto», no al «por qué» (eso viene en la Fase 2).

### Qué necesitas saber

**Tamaño total del mercado** en la categoría (ej: cámaras de seguridad domésticas en España). Desglosado por canal (gran superficie, online, especializado, bricolaje) y por rango de precio. También necesitas entender la evolución de la categoría: ¿crece, decrece, está madura? Y las cuotas de mercado por marca.

### Herramientas y fuentes de datos

| Herramienta | Qué te da | Limitación | Coste / Acceso |
|-------------|-----------|------------|----------------|
| **GFK** | Sell-out por producto, marca, canal, precio. Cuotas de mercado reales. | Caro. No siempre disponible para todas las categorías de Garza. | De pago (variable). Pedir presupuesto por categoría. |
| **Helium10** | Volumen de venta estimado por marca/producto en Amazon. Keywords y tendencias de búsqueda. | Solo canal Amazon. Estimaciones, no sell-out real. Sesgo hacia consumidor digital. | Suscripción activa. |
| **Google Trends** | Tendencia de interés de búsqueda por categoría/producto. Comparativa entre términos. Estacionalidad. | No da volúmenes absolutos, solo índice relativo. No distingue intención de compra. | Gratuito. |
| **Statista** | Informes de mercado con tamaño, previsiones y segmentación por país/región. | Datos agregados (macro). No siempre granular a nivel producto. | Versión básica gratuita. Premium de pago. |
| **Euromonitor** | Análisis profundos de categoría con sizing, tendencias, perfiles de consumidor. | Muy caro. Más orientado a FMCG que a electrónica de consumo. | De pago (caro). Verificar acceso UNIR. |
| **ProQuest One Business** | Artículos académicos, informes sectoriales, análisis de industria. Bueno para contexto y tendencias macro. | Más académico que operativo. No da sell-out. | Acceso vía UNIR (Student Pack). |
| **SEMrush / SimilarWeb** | Tráfico web de competidores, keywords por las que posicionan, share of voice digital. | Solo canal digital. No refleja venta offline. | Freemium. Planes de pago. |

### Entregable de Fase 1

**Mapa de mercado:** documento que responda a: ¿cuánto vale esta categoría? ¿Quién vende cuánto y dónde? ¿La categoría crece o decrece? ¿Hay estacionalidad? ¿Qué rango de precios domina? Este documento no tiene que ser perfecto — tiene que ser honesto con lo que sabes vs. lo que asumes.

---

## Fase 2: Buyer persona (iterativa con Fase 1)

**Objetivo:** pasar del «cuánta gente compra» al «quién es, qué valora, qué le frustra y cómo decide». Esta fase es iterativa con la Fase 1: los datos de mercado te ayudan a segmentar, y la segmentación te hace buscar datos de mercado más específicos.

### Dos capas de análisis

**Capa cuantitativa (el QUÉ):** datos demográficos, volumen por segmento, comportamiento de compra medible. Fuentes: datos B2B internos, Shopify (B2C incipiente), GFK, Helium10.

**Capa cualitativa (el POR QUÉ):** motivaciones, miedos, frustraciones, criterios de decisión. Esta es la capa que hoy Garza no tiene y que es crítica para diferenciarse. Sin el «por qué», solo puedes competir en precio.

### Cómo construir el «por qué» sin presupuesto de investigación

| Método | Cómo aplicarlo en Garza | Qué te da |
|--------|------------------------|-----------|
| **Minería de reseñas** | Scraping de reseñas de Amazon (tu categoría y competidores). Analizar con Python/NLP qué palabras se repiten en reseñas de 5 estrellas vs. 1 estrella. | Drivers de satisfacción e insatisfacción reales del consumidor final. |
| **Análisis de keywords** | Helium10 + Google Keyword Planner. Buscar cómo busca la gente el producto (ej: «cámara seguridad fácil instalar» vs «cámara vigilancia profesional»). | Intención de búsqueda = proxy de lo que valoran. Los modificadores de búsqueda revelan el segmento. |
| **Entrevistas a comerciales** | Entrevistas estructuradas al equipo comercial de Garza. Ellos hablan con los clientes B2B que a su vez conocen al consumidor final. | Conocimiento tácito del mercado que hoy no se captura. Insights de canal sobre qué se vende y qué no. |
| **Datos Shopify** | Analizar el funnel: qué productos se ven más, cuáles convierten, dónde se abandona. Cruzar con datos demográficos del comprador. | Comportamiento real del consumidor Garza (aunque muestra pequeña aún). |
| **Encuestas rápidas** | Google Forms o Typeform enviadas a base de clientes Shopify o post-compra. Máximo 5 preguntas. Preguntar: ¿por qué eligió este producto? ¿Qué valoró más? ¿Qué mejoraría? | Datos primarios propios. Pequeña muestra pero de alto valor por ser clientes reales. |

### Entregable de Fase 2

**Ficha(s) de buyer persona:** para cada segmento prioritario, un documento que incluya: perfil demográfico, contexto de uso, drivers de decisión (qué valora), pain points (qué le frustra), mensaje clave (qué quiere oír), y canal de compra preferido. Distinguir siempre entre lo que SABES (dato) y lo que ASUMES (hipótesis a validar).

---

## Fase 3: Análisis competitivo

**Objetivo:** entender no solo quién compite, sino cómo compite y dónde hay espacio para Garza. Esta fase actúa como bisagra entre entender el mercado y tomar decisiones de producto.

**Importante:** el análisis competitivo no es un paso único. Se aplica en dos momentos: aquí (nivel estratégico, para encontrar oportunidades de diferenciación) y dentro de la Fase 4 (nivel táctico, para definir features específicas del producto).

### Dimensiones del análisis

| Dimensión | Qué analizar | Herramientas |
|-----------|-------------|--------------|
| **Propuesta de valor** | ¿Qué promete cada competidor? ¿A qué segmento apunta? ¿Cuál es su mensaje principal? | Análisis manual de webs, packaging y comunicación de competidores. |
| **Posicionamiento precio** | Rangos de precio por competidor y canal. Relación precio-features. | GFK (si disponible), Helium10, scraping manual de precios en retail. |
| **Percepción del consumidor** | ¿Qué dicen los consumidores de cada marca? ¿Qué les gusta y qué odian? | Minería de reseñas (Amazon, Google). Análisis de sentimiento. |
| **Presencia digital** | Share of voice online, posicionamiento SEO, inversión publicitaria estimada. | SEMrush, SimilarWeb, Google Ads Transparency Center. |
| **Gaps y oportunidades** | Cruzar los pain points del buyer persona (Fase 2) con las propuestas de valor de la competencia. Donde hay frustración no resuelta, hay oportunidad. | Síntesis propia. No hay herramienta para esto — es análisis estratégico puro. |

### Entregable de Fase 3

**Mapa competitivo:** matriz de competidores por propuesta de valor, precio, segmento objetivo y fortalezas/debilidades percibidas. Más importante aún: un documento de oportunidades de diferenciación que identifique dónde Garza puede ofrecer algo que el mercado no resuelve bien.

---

## Fase 4: Definición de producto

**Objetivo:** traducir todo lo anterior en un producto concreto con características, precio objetivo y requisitos de calidad.

**Cambio de paradigma:** en el proceso actual de Garza, el producto se define por el coste del proveedor. En este framework, el producto se define por la intersección de tres cosas: lo que el buyer persona valora, lo que la competencia no resuelve bien, y lo que Garza puede ejecutar (capacidad operativa y margen).

### Inputs que necesitas de fases anteriores

**De Fase 1:** tamaño de la oportunidad y rangos de precio que el mercado acepta.

**De Fase 2:** características que el buyer persona valora y sus pain points.

**De Fase 3:** huecos competitivos donde Garza puede diferenciarse.

### Componentes del brief de producto

**Features priorizadas:** lista de características clasificadas en must-have, nice-to-have y diferenciador. Las must-have vienen del análisis de reseñas negativas de competidores (lo que el mercado exige como mínimo). Los diferenciadores vienen de los gaps de la Fase 3.

**Precio objetivo:** definido desde el mercado hacia dentro (target costing), no desde el coste hacia fuera (cost-plus). El precio de venta se determina por el posicionamiento elegido, y el margen es la restricción que negocias con el proveedor.

**Requisitos de calidad:** criterios de testing derivados de los pain points del consumidor. Si las reseñas negativas de la competencia mencionan «falsos positivos» en cámaras, eso se convierte en un test obligatorio pre-lanzamiento.

### Entregable de Fase 4

**Brief de producto:** documento que el equipo de compras / producto puede llevar al proveedor con: features requeridas, precio objetivo PVP y margen mínimo, criterios de calidad no negociables, y posicionamiento de referencia (contra qué compite este producto y por qué es diferente).

---

## Fase 5: Dimensionamiento

**Objetivo:** determinar cuántas unidades fabricar en la primera tirada con un modelo basado en datos, no en intuición.

### Variables del modelo

| Variable | Fuente | Consideración |
|----------|--------|---------------|
| **TAM de la categoría** | Fase 1 (GFK, Statista, Helium10) | Tamaño total del mercado accesible. |
| **Cuota objetivo realista** | Benchmark de cuota de nuevos entrantes en la categoría (GFK histórico si disponible). | No asumir más del 1-3% en el primer año salvo que haya evidencia. |
| **Capacidad de distribución** | Datos internos: número de puntos de venta, velocidad de listado, sell-in histórico de productos nuevos. | La restricción real suele ser ésta, no la demanda. |
| **Lead time del proveedor** | Datos del proveedor. | Determina si puedes hacer reposición rápida o necesitas acertar a la primera. |
| **Estacionalidad** | Google Trends + datos de venta internos. | Planificar la tirada para llegar antes del pico estacional. |
| **Coste de oportunidad del stock** | Finanzas internas. | Cuánto cuesta tener producto sin vender (almacén, capital inmovilizado, obsolescencia). |

### Modelo de escenarios

Calcular tres escenarios: conservador (percentil 25 de las estimaciones), base (percentil 50) y optimista (percentil 75). La primera tirada debería dimensionarse entre el escenario conservador y el base, nunca sobre el optimista. Si el lead time del proveedor permite reposición en menos de 8 semanas, puedes permitirte una primera tirada más ajustada.

### Entregable de Fase 5

**Plan de producción:** cantidad de primera tirada con justificación (modelo de escenarios), calendario de producción alineado con estacionalidad, y trigger de reposición (a qué nivel de stock se lanza el siguiente pedido).

---

## Fase 6: Posicionamiento y comunicación

**Nota crítica:** aunque aparece como Fase 6, el posicionamiento (mensaje central) debería empezar a definirse en paralelo con la Fase 4. El packaging y los assets de venta son la ejecución, pero el mensaje es una decisión estratégica que influye en el producto mismo.

### Componentes del brief creativo

**Mensaje central:** una frase que conecte el driver principal del buyer persona con la ventaja diferencial de Garza. Ejemplo del caso cámaras: «Tranquilidad real: la cámara que avisa solo cuando importa» (conecta «tranquilidad» como driver del senior con «cero falsos positivos» como diferenciador).

**Tono y estilo:** derivado del buyer persona. No es lo mismo comunicar para un perfil tech-savvy de 30 años que para un senior de 65.

**Assets necesarios:** packaging, ficha de producto para canal B2B, landing page, vídeo de producto, materiales para punto de venta (si aplica), contenido para marketplace (A+ content en Amazon).

**Plan de medios:** dónde llegar al buyer persona. Las keywords de Fase 2 te dicen qué busca; SEMrush te dice dónde busca.

---

## Fase 7: Go-to-market y seguimiento

**Objetivo:** lanzar con un plan medible y establecer un ciclo de feedback que alimente futuros lanzamientos.

### KPIs por fase de lanzamiento

| Fase de lanzamiento | KPIs | Fuente de datos |
|--------------------|------|-----------------|
| **Pre-lanzamiento (semanas -4 a 0)** | Número de puntos de venta listados, pedidos B2B en cartera, cobertura de distribución vs. objetivo. | CRM / ERP interno. |
| **Lanzamiento (semanas 1-4)** | Velocidad de sell-out (unidades/semana), conversión en Shopify/Amazon, primeras reseñas y rating medio. | Shopify, Amazon Seller Central, GFK (si disponible). |
| **Post-lanzamiento (semanas 5-12)** | Tasa de recompra, evolución de sell-through vs. estimación, feedback cualitativo (reseñas, devoluciones, quejas). | Shopify, Amazon, datos de devoluciones internos. |

### Ciclo de feedback

Cada lanzamiento debe producir un informe post-mortem a las 12 semanas que documente: qué asumimos vs. qué ocurrió, dónde acertamos y dónde fallamos, y qué aprendizajes aplicar al siguiente lanzamiento. Este informe alimenta la Fase 1 del siguiente producto, creando un ciclo de mejora continua.

---

## Resumen: herramienta por fase

| Fase | Herramienta | Para qué | Tipo de dato |
|------|-------------|----------|--------------|
| 1. Mercado | GFK | Tamaño, cuotas, sell-out por canal | Cuantitativo (venta real) |
| 1. Mercado | Helium10 | Volúmenes en Amazon, keywords | Cuantitativo (estimado) |
| 1. Mercado | Google Trends | Tendencia de demanda, estacionalidad | Cuantitativo (relativo) |
| 1. Mercado | Statista / Euromonitor | Sizing macro, previsiones | Cuantitativo (agregado) |
| 1. Mercado | ProQuest (UNIR) | Contexto sectorial, tendencias | Cualitativo (académico) |
| 2. Buyer persona | Minería de reseñas | Drivers de satisfacción/insatisfacción | Cualitativo (consumidor real) |
| 2. Buyer persona | Helium10 / KW Planner | Intención de búsqueda como proxy de lo que valoran | Cuantitativo (búsqueda) |
| 2. Buyer persona | Shopify analytics | Comportamiento real del comprador Garza | Cuantitativo (propio) |
| 2. Buyer persona | Entrevistas comerciales | Conocimiento tácito del equipo | Cualitativo (interno) |
| 3. Competencia | SEMrush / SimilarWeb | Presencia digital, share of voice | Cuantitativo (digital) |
| 3. Competencia | Minería de reseñas | Percepción de competidores por el consumidor | Cualitativo (consumidor) |
| 3. Competencia | Análisis manual | Propuesta de valor, packaging, comunicación | Cualitativo (estratégico) |
| 4. Producto | Síntesis Fases 1-3 | Brief de producto con features, precio, calidad | Decisión estratégica |
| 5. Dimensionamiento | Modelo en Python/Excel | Escenarios de tirada con variables múltiples | Cuantitativo (modelado) |
| 6. Comunicación | Brief creativo | Mensaje, tono, assets, plan de medios | Estratégico + creativo |
| 7. Go-to-market | Shopify + ERP + Amazon | KPIs de lanzamiento y ciclo de feedback | Cuantitativo (seguimiento) |

---

## Anti-patrones: lo que este framework busca evitar

| Práctica actual (reactiva) | Práctica objetivo (data-driven) |
|---------------------------|--------------------------------|
| Pedir coste al proveedor y ajustar precio a bestsellers. | Definir precio objetivo desde el mercado (target costing) y negociar margen con proveedor. |
| Elegir producto por lo que el proveedor puede fabricar barato. | Elegir producto por la intersección de demanda + gap competitivo + capacidad Garza. |
| Dimensionar tirada por intuición o por MOQ del proveedor. | Dimensionar con modelo de escenarios alimentado por datos de mercado y distribución. |
| Crear packaging después de tener el producto. | Definir posicionamiento y mensaje en paralelo con el producto. |
| Lanzar y olvidar. No medir resultados sistemáticamente. | Post-mortem a 12 semanas que alimenta el siguiente lanzamiento. |

---

**Próximos pasos:** este framework es la v1.0. Debería iterarse con cada lanzamiento real. La recomendación es aplicarlo primero a un producto piloto (por ejemplo, la próxima cámara de Garza), documentar rigurosamente qué fases se pudieron ejecutar con datos y cuáles requirieron hipótesis, y ajustar el proceso en función de los aprendizajes.
