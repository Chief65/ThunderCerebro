# Principios clave de *Self-Consistency Improves Chain of Thought Reasoning in Language Models*

**Autores:** Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery y Denny Zhou  
**Publicación:** ICLR 2023  
**Objetivo de este documento:** extraer las ideas más útiles del paper sobre generación de múltiples soluciones, agregación, incertidumbre y mejora de razonamiento.

---

# 1. Idea central

El paper parte de una limitación sencilla:

```text
Chain-of-Thought
+
greedy decoding
=
una sola trayectoria
```

Pero un problema complejo puede tener múltiples formas válidas de llegar a la misma respuesta.

Self-Consistency propone:

```text
PROBLEMA
↓
GENERAR VARIAS TRAYECTORIAS DIVERSAS
↓
EXTRAER RESPUESTAS FINALES
↓
AGREGAR
↓
ELEGIR LA RESPUESTA MÁS CONSISTENTE
```

La intuición central es:

> **Si distintas rutas independientes convergen en la misma respuesta, esa convergencia puede aportar una señal útil de fiabilidad.**

---

# 2. No confiar demasiado en una única generación

Una llamada a un modelo es una muestra de una distribución.

Puede resultar:

- correcta;
- parcialmente correcta;
- equivocada;
- atrapada en un error local.

Self-Consistency utiliza la variabilidad del modelo como recurso en lugar de tratarla únicamente como defecto.

## Principio operativo

> **Para problemas difíciles, varias soluciones independientes pueden ser más informativas que una sola solución aparentemente óptima.**

---

# 3. Diversidad primero, agregación después

El mecanismo necesita dos propiedades:

```text
DIVERSIDAD
+
CONVERGENCIA
```

Si todas las generaciones son prácticamente idénticas, no obtenemos mucha información nueva.

Si todas son completamente diferentes, tampoco existe señal clara de consenso.

El valor aparece cuando:

```text
rutas diferentes
→ misma respuesta final
```

---

# 4. Por qué no utilizar greedy decoding

Greedy decoding selecciona en cada paso la continuación local más probable.

Esto puede conducir a:

- soluciones repetitivas;
- óptimos locales;
- una única interpretación;
- errores tempranos que se propagan.

Self-Consistency sustituye esa única trayectoria por sampling.

---

# 5. La diversidad es parte del algoritmo

El paper compara Self-Consistency con beam search.

Un resultado importante es que beam search produce menos diversidad y rindió peor en los experimentos comparables.

## Lección

> **Cuando el objetivo es obtener evidencia mediante consenso, necesitas diversidad real, no múltiples variantes casi idénticas.**

Esto puede trasladarse a:

- brainstorming;
- análisis de hipótesis;
- debugging;
- planificación;
- generación de alternativas.

---

# 6. El consenso se realiza sobre la respuesta, no sobre el texto completo

Dos razonamientos pueden expresarse de forma diferente y llegar a la misma conclusión.

Por eso Self-Consistency marginaliza las trayectorias y agrega las respuestas finales.

Ejemplo:

```text
Ruta A → 18
Ruta B → 18
Ruta C → 26
Ruta D → 18

Resultado agregado → 18
```

## Principio

Separar:

```text
PROCESO
```

de:

```text
RESULTADO CANÓNICO
```

Esto requiere que la respuesta final pueda extraerse de forma fiable.

---

# 7. Answer extraction es parte crítica del sistema

Para agregar resultados hay que identificar cuál es la respuesta de cada trayectoria.

Por tanto:

```text
GENERACIÓN
↓
EXTRACCIÓN
↓
NORMALIZACIÓN
↓
AGREGACIÓN
```

Si la extracción es frágil, la agregación también lo será.

Aplicación:

```text
"The answer is 18."
"18"
"$18"
```

deben poder mapearse al mismo valor si semánticamente son equivalentes.

---

# 8. Más muestras pueden aumentar precisión

Los autores estudian 1, 5, 10, 20 y 40 trayectorias.

En sus experimentos, aumentar el número de muestras tendía a mejorar el rendimiento, aunque con rendimientos decrecientes.

## Idea práctica

> **El número de muestras es un presupuesto de inferencia.**

Puedes intercambiar:

```text
más coste
↔
más robustez
```

---

# 9. Rendimientos decrecientes

El propio paper señala que en muchos casos gran parte de la mejora aparece con un número relativamente pequeño de trayectorias.

En la discusión recomiendan considerar 5 o 10 como punto de partida práctico cuando el coste importa.

## Arquitectura adaptativa

```text
generar 3-5 respuestas
↓
¿consenso alto?
├─ sí → aceptar
└─ no → generar más / verificar
```

Esto puede ser más eficiente que generar siempre 40.

---

# 10. El método funciona como un “self-ensemble”

A diferencia de un ensemble tradicional:

```text
modelo A
modelo B
modelo C
→ voto
```

Self-Consistency utiliza:

```text
un mismo modelo
+
múltiples samples
→ voto
```

Por eso los autores lo describen como una forma de **self-ensemble**.

---

# 11. Varios modelos no son necesariamente mejores

El paper compara con ensembles de modelos.

Una observación interesante es que introducir modelos más débiles puede arrastrar hacia abajo la calidad final.

## Principio general

> **Diversidad no significa mezclar componentes de cualquier calidad.**

Una señal adicional solo ayuda si contiene información útil.

---

# 12. Self-Consistency superó sample-and-rank

Otra alternativa estudiada consiste en:

```text
generar muchas respuestas
→ elegir la de mayor probabilidad
```

En los experimentos del paper, Self-Consistency produjo mejoras superiores.

Esto sugiere:

> **La probabilidad interna de una secuencia no es necesariamente un buen sustituto de la corrección.**

---

# 13. La respuesta más probable no siempre es la más correcta

Este principio es especialmente importante.

Un modelo puede asignar alta probabilidad a:

- patrones frecuentes;
- errores recurrentes;
- soluciones superficiales.

El consenso de trayectorias diversas explota una señal diferente:

```text
cuántas rutas independientes convergen aquí
```

---

# 14. Robustez a distintas estrategias de sampling

Los autores prueban diferentes:

- temperaturas;
- top-k;
- configuraciones de sampling.

Self-Consistency mantiene mejoras en una variedad de configuraciones.

## Lección

El concepto parece depender menos de una configuración exacta que de:

```text
producir diversidad suficiente
+
agregar de forma razonable
```

---

# 15. Robustez ante diferentes prompts

El paper también evalúa distintos conjuntos de prompts Chain-of-Thought.

Las mejoras se mantienen.

Esto es importante porque indica que el método no dependía únicamente de un único prompt afortunado.

---

# 16. Self-Consistency puede rescatar configuraciones donde CoT solo empeora

Los autores prueban tareas NLP en las que añadir Chain-of-Thought podía reducir el rendimiento frente a prompting estándar.

Self-Consistency mitigó ese problema y produjo mejoras robustas en el conjunto estudiado.

## Lección

Una sola trayectoria de razonamiento puede introducir ruido.

La agregación puede reducir parte de esa varianza.

---

# 17. Aplicación más allá de matemáticas

La idea de Self-Consistency puede abstraerse:

```text
GENERAR ALTERNATIVAS
→ NORMALIZAR
→ BUSCAR CONVERGENCIA
```

Esto puede resultar útil cuando existen respuestas relativamente discretas o criterios claros.

Ejemplos:

- clasificación;
- estimación;
- diagnóstico técnico con conjunto limitado de causas;
- selección entre opciones;
- resolución de problemas;
- verificación de hipótesis.

---

# 18. No confundir consenso con verdad

Cinco respuestas pueden coincidir y seguir siendo incorrectas.

Si el modelo comparte el mismo sesgo o desconocimiento en todas las muestras:

```text
5 × mismo error
=
consenso incorrecto
```

## Regla

> **Self-Consistency reduce varianza; no elimina errores sistemáticos.**

---

# 19. El método funciona mejor cuando las rutas incorrectas son menos consistentes

La intuición del paper supone que:

```text
rutas correctas diversas
→ tienden a converger

rutas erróneas
→ tienden a dispersarse
```

Esto no tiene por qué cumplirse siempre.

Si existe un error muy atractivo o un misconception dominante, las rutas erróneas también pueden converger.

---

# 20. Útil como señal de incertidumbre

Los autores señalan que la distribución de respuestas puede utilizarse para estimar incertidumbre.

Ejemplo:

```text
10 samples

A: 10
→ consenso alto

A: 4
B: 3
C: 3
→ incertidumbre alta
```

## Aplicación

La dispersión puede servir como trigger:

```text
si desacuerdo > umbral
→ escalar
→ buscar fuente
→ usar herramienta
→ pedir revisión
```

---

# 21. Consenso como routing

Una aplicación avanzada:

```text
problema
↓
3 samples
↓
consenso
├─ alto → terminar
└─ bajo → proceso más caro
          ↓
          retrieval / tool / modelo superior / humano
```

Esto convierte la incertidumbre en una señal operativa.

---

# 22. Más inferencia en lugar de más entrenamiento

Una propiedad destacada del método es que no necesita:

- fine-tuning;
- anotaciones nuevas;
- modelo auxiliar;
- verificador entrenado.

La mejora se obtiene en inferencia.

## Trade-off

```text
menos entrenamiento
↔
más coste por consulta
```

---

# 23. Compute-time scaling

Aunque el paper no utiliza la terminología moderna de forma central, conceptualmente Self-Consistency muestra una idea poderosa:

> **Puedes mejorar un resultado gastando más computación durante inferencia.**

En lugar de:

```text
modelo → respuesta
```

usar:

```text
modelo × N
→ agregador
→ respuesta
```

---

# 24. Cuándo merece la pena

Especialmente cuando:

- la tarea es difícil;
- el coste de equivocarse es significativo;
- existe una respuesta canónica;
- generar varias soluciones es barato comparado con el error;
- no existe un verificador determinista perfecto.

---

# 25. Cuándo probablemente no merece la pena

- tareas triviales;
- redacción abierta sin criterio de consenso;
- latencia muy estricta;
- coste extremadamente limitado;
- tareas donde todas las muestras comparten el mismo sesgo;
- tareas con un verificador determinista barato.

Ejemplo:

```text
¿2 + 2?
```

No necesitas 40 trayectorias.

---

# 26. Verificador determinista sigue siendo superior cuando existe

Si una operación puede comprobarse con:

- código;
- test;
- base de datos;
- solver;
- fuente autoritativa;

esa comprobación es normalmente una señal más fuerte que el voto de un modelo.

Self-Consistency es especialmente útil cuando la validación directa es difícil.

---

# 27. Agregación semántica para outputs libres

El paper trabaja principalmente con respuestas que pueden agruparse.

Para texto libre, el principio requiere una etapa adicional:

```text
generaciones
↓
cluster / evaluación / extracción de conclusiones
↓
agregación
```

No basta con contar cadenas exactas.

---

# 28. Enseñanza para prompts maestros

Un prompt maestro puede incorporar una política de “múltiples candidatos” sin obligarla siempre.

Ejemplo:

```markdown
## Verificación de problemas difíciles

Cuando una decisión sea difícil y no exista una verificación directa:

1. genera varias soluciones independientes;
2. evita que una solución copie automáticamente a la anterior;
3. compara las conclusiones;
4. identifica puntos de consenso y desacuerdo;
5. utiliza evidencia adicional cuando el desacuerdo sea material;
6. entrega una única respuesta final.
```

---

# 29. Separar generación y selección

Una lección muy potente:

```text
GENERADOR
```

y

```text
SELECTOR
```

son funciones distintas.

Un sistema puede mejorar aunque el generador sea el mismo si cambia cómo se seleccionan sus outputs.

Esto conecta con:

- reranking;
- evaluadores;
- best-of-N;
- search;
- voting;
- reward models.

---

# 30. No pedir a cada muestra que vea las anteriores

Para maximizar diversidad, las trayectorias deberían ser suficientemente independientes.

Si mostramos:

```text
respuesta A
```

antes de pedir B, B puede anclarse en A.

## Principio

> **Independencia de muestras mejora el valor informativo del consenso.**

---

# 31. Diseño de presupuesto dinámico

Una estrategia eficiente:

```text
N = 3
↓
si 3/3 coinciden → terminar

si 2/3 → generar 2 más

si sigue dividido → verificar externamente
```

Este enfoque utiliza más cómputo solamente cuando el problema lo necesita.

---

# 32. Coste como principal limitación

El paper declara explícitamente que Self-Consistency requiere más computación.

Si cada respuesta cuesta `C` y generamos `N`:

```text
coste ≈ N × C
```

más la agregación.

También aumenta latencia si las llamadas no pueden paralelizarse.

---

# 33. Razonamientos no factuales siguen siendo posibles

Los autores observan trayectorias:

- incorrectas;
- absurdas;
- no factuales.

Por tanto Self-Consistency no soluciona la grounding problem.

Para conocimiento factual:

```text
Self-Consistency
+
retrieval / fuentes
```

puede ser conceptualmente más robusto que Self-Consistency solo.

---

# 34. Qué merece la pena absorber permanentemente

1. **Una sola generación es una muestra, no una verdad.**
2. **La diversidad puede convertirse en señal de calidad.**
3. **Convergencia entre rutas independientes puede aumentar confianza.**
4. **La selección del output es una parte independiente del sistema.**
5. **Greedy decoding puede quedar atrapado en una trayectoria mediocre.**
6. **Diversity matters cuando se utiliza voting.**
7. **Más muestras mejoran resultados hasta cierto punto, pero con rendimientos decrecientes.**
8. **El número de muestras debe tratarse como presupuesto de inferencia.**
9. **El desacuerdo puede utilizarse como señal de incertidumbre.**
10. **Consenso no equivale a verdad.**
11. **Los errores sistemáticos sobreviven al voto.**
12. **Utiliza verificación determinista cuando exista.**
13. **No es necesario aplicar multipath a tareas fáciles.**
14. **La agregación necesita outputs normalizables o un extractor fiable.**

---

# 35. Checklist de implementación

- [ ] ¿La tarea es suficientemente difícil?
- [ ] ¿Existe una respuesta final comparable entre samples?
- [ ] ¿Las muestras son realmente diversas?
- [ ] ¿Pueden ejecutarse en paralelo?
- [ ] ¿Se normalizan las respuestas?
- [ ] ¿Está definido el mecanismo de agregación?
- [ ] ¿Existe un umbral de consenso?
- [ ] ¿Existe fallback para desacuerdo?
- [ ] ¿Se mide el beneficio frente a greedy?
- [ ] ¿Se mide coste y latencia?
- [ ] ¿Se han probado 3/5/10 samples antes de usar números grandes?
- [ ] ¿Existe una alternativa determinista más barata?

---

# 36. Síntesis final

El principio más valioso de Self-Consistency es muy simple:

> **No siempre deberíamos pedirle al modelo que encuentre una única trayectoria; a veces deberíamos pedirle que explore varias y utilizar la convergencia como evidencia.**

Esto convierte la aleatoriedad del modelo en una herramienta.

Pero debe recordarse:

```text
variabilidad → puede reducirse mediante consenso
sesgo sistemático → no
```

La versión práctica más robusta del concepto es:

```text
GENERAR VARIOS
→ AGREGAR
→ MEDIR CONSENSO
→ VERIFICAR SI ES NECESARIO
```

y utilizar más compute únicamente cuando el riesgo o la dificultad lo justifiquen.

