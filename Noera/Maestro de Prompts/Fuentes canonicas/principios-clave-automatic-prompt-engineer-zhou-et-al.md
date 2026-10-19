# Principios clave de *Large Language Models Are Human-Level Prompt Engineers*

**Autores:** Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan y Jimmy Ba  
**Método principal:** Automatic Prompt Engineer (APE)  
**Publicación:** ICLR 2023  
**Objetivo de este documento:** extraer las ideas más útiles sobre optimización automática de prompts, búsqueda de instrucciones y evaluación sistemática.

---

# 1. Idea central

El paper plantea una reformulación poderosa:

> **Una instrucción en lenguaje natural puede tratarse como un programa que se optimiza mediante búsqueda.**

En vez de:

```text
humano escribe prompt
→ lo prueba
→ lo reescribe
→ lo prueba
```

APE utiliza:

```text
DEMOSTRACIONES
↓
GENERAR MUCHOS PROMPTS CANDIDATOS
↓
EJECUTARLOS
↓
PUNTUARLOS
↓
SELECCIONAR LOS MEJORES
↓
[OPCIONAL] GENERAR VARIANTES
↓
PROMPT FINAL
```

---

# 2. Prompt engineering como optimización black-box

Los autores argumentan que no comprendemos completamente qué instrucciones son compatibles con un modelo concreto.

Por ello no intentan deducir el prompt perfecto mediante reglas.

Lo tratan como:

```text
ρ* = argmax score(prompt)
```

Es decir:

> **buscar el prompt que maximiza una función de utilidad sobre ejemplos representativos.**

---

# 3. El prompt más intuitivo para humanos no tiene por qué ser el mejor para el modelo

Una idea central del paper:

Los LLMs pueden responder mejor a instrucciones que no serían necesariamente las que elegiría un humano.

Esto implica que:

```text
claridad humana
```

y:

```text
compatibilidad con el modelo
```

están relacionadas, pero no son idénticas.

## Consecuencia

> **La calidad de un prompt debe medirse por su comportamiento, no por lo elegante que suene.**

---

# 4. Separar propuesta y evaluación

APE tiene dos funciones centrales:

## Proposal

Generar instrucciones candidatas.

## Scoring

Determinar cuáles funcionan mejor.

Esto introduce una arquitectura reutilizable:

```text
GENERATOR
+
EVALUATOR
```

que aparece en muchas técnicas posteriores.

---

# 5. Generar candidatos desde demostraciones

APE parte de ejemplos:

```text
Input A → Output A
Input B → Output B
Input C → Output C
```

y pide al modelo inferir qué instrucción podría producir esa relación.

Conceptualmente:

```text
EJEMPLOS
→ inferir tarea
→ redactar instrucciones candidatas
```

Esto es **instruction induction**.

---

# 6. Las demostraciones pueden especificar una tarea mejor que una descripción

A veces el usuario sabe mostrar qué quiere, pero no explicarlo formalmente.

Ejemplo:

```text
input1 → output1
input2 → output2
input3 → output3
```

puede ser suficiente para que el sistema deduzca:

```text
"transforma X de esta manera"
```

## Principio

> **Los ejemplos pueden funcionar como especificación.**

---

# 7. Natural language program synthesis

El paper conecta este proceso con program synthesis.

En programación clásica:

```text
especificación
→ buscar programa
```

En APE:

```text
ejemplos
→ buscar instrucción en lenguaje natural
```

El espacio de programas es prácticamente infinito, por lo que el modelo se utiliza para proponer candidatos plausibles.

---

# 8. Utilizar el LLM para restringir el espacio de búsqueda

Buscar todas las cadenas posibles sería inviable.

APE utiliza el propio LLM como generador priorizado:

```text
espacio de todas las instrucciones
↓
LLM propone subset plausible
↓
evaluación
```

## Idea general

> **Los modelos pueden utilizarse como proposal distributions para problemas de búsqueda.**

---

# 9. Scoring mediante ejecución

Una de las funciones utilizadas por APE es **execution accuracy**.

Proceso:

```text
prompt candidato
+
entrada
→ modelo
→ output

output
vs.
respuesta esperada
→ score
```

Esto es fundamental.

El prompt no se evalúa por:

- estilo;
- longitud;
- impresión subjetiva.

Se evalúa por:

```text
¿hace correctamente la tarea?
```

---

# 10. Optimizar contra resultados, no contra estética

Esta idea merece conservarse para cualquier prompt maestro:

```text
PROMPT A suena mejor
```

no es razón suficiente para preferirlo a:

```text
PROMPT B obtiene mejores resultados en evaluación
```

## Regla

> **El prompt es un componente funcional y debe optimizarse por métricas de comportamiento.**

---

# 11. Log probability como señal alternativa

El paper también estudia utilizar la probabilidad del output deseado como función de scoring.

La intención es obtener una señal más fina cuando muchos candidatos obtienen score exacto bajo.

Sin embargo, en sus análisis execution accuracy correlacionó mejor con rendimiento final y se utilizó como métrica principal.

## Lección

> **La función objetivo elegida determina qué prompt terminas optimizando.**

---

# 12. La métrica debe representar el objetivo real

Si optimizas:

```text
exact match
```

obtendrás prompts optimizados para exact match.

Si optimizas:

```text
truthfulness
```

puedes sacrificar informativeness.

El paper muestra explícitamente este trade-off en TruthfulQA.

---

# 13. Optimización multiobjetivo

En TruthfulQA, algunas instrucciones maximizaban verdad produciendo respuestas poco informativas como rechazos o evasivas.

Esto muestra:

```text
MAXIMIZAR UNA MÉTRICA
```

puede generar soluciones degeneradas.

## Principio

> **Una métrica imperfecta puede crear un prompt que “gana” el benchmark sin cumplir el objetivo real del producto.**

---

# 14. Diseñar varias métricas cuando hay trade-offs

Ejemplo:

```text
truthfulness
+
informativeness
```

en lugar de optimizar una sola.

Para prompts maestros:

```text
accuracy
+
coverage
+
format compliance
+
latency
+
cost
```

pueden ser dimensiones separadas.

---

# 15. Adaptive filtering reduce coste

Evaluar todos los candidatos sobre todo el dataset sería costoso.

APE utiliza una estrategia:

```text
muchos candidatos
↓
evaluación barata con pocos ejemplos
↓
eliminar malos
↓
evaluar supervivientes con más datos
↓
seleccionar
```

## Principio general

> **Gastar más evaluación únicamente en candidatos prometedores.**

---

# 16. Este patrón escala más allá del prompting

Es similar a:

- successive halving;
- bandits;
- hyperparameter optimization;
- search;
- tournament selection.

Aplicación:

```text
100 prompts
→ test rápido
→ 20
→ test medio
→ 5
→ evaluación completa
```

---

# 17. Iterative APE

El paper también prueba:

```text
mejores prompts actuales
↓
pedir variantes semánticamente similares
↓
puntuar
↓
repetir
```

Esto crea una búsqueda local alrededor de soluciones prometedoras.

---

# 18. Más iteración no siempre compensa

Un resultado especialmente importante:

La búsqueda iterativa mejoraba la calidad media del conjunto, pero el mejor prompt tendía a estabilizarse.

Los autores concluyen que el procedimiento simple ya es muy efectivo y utilizan APE no iterativo como default.

## Lección

> **No añadir ciclos de refinamiento si la evaluación no demuestra beneficio.**

---

# 19. Diminishing returns al generar candidatos

Los experimentos muestran que aumentar el número de prompts candidatos mejora la probabilidad de encontrar uno bueno, pero con rendimientos decrecientes.

En su configuración, el rendimiento se acercaba al nivel humano con decenas de candidatos.

## Principio

El tamaño del search budget debe medirse.

---

# 20. Proposal quality importa, pero selección puede rescatar generadores débiles

Modelos pequeños producían distribuciones de candidatos peores.

Sin embargo, si generaban suficientes candidatos y existía buena selección, todavía podían aparecer buenos prompts.

Esto demuestra:

```text
calidad del generador
+
calidad del selector
```

determinan el sistema.

---

# 21. Modelos más potentes pueden resultar más baratos globalmente

En el análisis de coste, modelos más grandes/alineados generaban instrucciones más concisas y de mayor calidad.

Aunque cada token era más caro, reducían costes posteriores de scoring.

## Lección

> **Coste unitario no es coste total del sistema.**

Esto es muy importante para routing de modelos.

---

# 22. Prompt optimization puede ser coste offline

APE puede gastar recursos una vez:

```text
generar
evaluar
seleccionar
```

y después reutilizar el prompt corto en muchas inferencias.

Los autores describen estos prompts como una forma de condensar el contexto de demostraciones.

---

# 23. Prompts como context condensers

En lugar de enviar muchos ejemplos cada vez:

```text
20 demostraciones
```

puedes derivar una instrucción compacta que capture parte del patrón.

Si el prompt se reutiliza millones de veces, un coste offline alto puede compensar ampliamente.

---

# 24. Prompt/model compatibility

Uno de los resultados más valiosos del paper es que los prompts optimizados para un modelo no siempre transferían bien a otro.

Las instrucciones generadas y seleccionadas para InstructGPT funcionaban mejor en ese modelo, y viceversa con GPT-3.

## Principio crítico

> **Un prompt no es independiente del modelo.**

---

# 25. Cambiar de modelo requiere reevaluar prompts

Un prompt optimizado para:

```text
Modelo A
```

no debería desplegarse automáticamente con:

```text
Modelo B
```

Proceso correcto:

```text
cambio de modelo
↓
regression suite
↓
reoptimización si es necesaria
```

---

# 26. Las instrucciones más efectivas pueden ser poco intuitivas

El paper observa que un modelo puede generar instrucciones útiles para sí mismo que un humano no elegiría.

Esto refuerza el enfoque black-box:

```text
medir
>
suponer
```

---

# 27. Meta-prompt importa

La plantilla utilizada para generar prompts candidatos cambia la distribución de candidatos.

El paper encuentra que modificar el meta-prompt puede mejorar ciertas tareas y empeorar otras.

## Consecuencia

APE introduce otro nivel:

```text
meta-prompt
→ prompts candidatos
→ task outputs
```

El meta-prompt también necesita evaluación.

---

# 28. Optimización recursiva

Podemos tener:

```text
PROMPT que genera PROMPTS
```

y optimizar también ese generador.

Esto anticipa sistemas modernos de automatic prompt optimization.

---

# 29. APE descubre mejores triggers de Zero-Shot CoT

Uno de los resultados conocidos del paper es la instrucción:

```text
"Let's work this out in a step by step way to be sure we have the right answer."
```

que superó en MultiArith al trigger humano “Let's think step by step” en el setup estudiado.

Lo importante no es memorizar la frase.

Lo importante es:

> **Incluso pequeñas instrucciones auxiliares pueden optimizarse empíricamente en lugar de elegirse por intuición.**

---

# 30. No convertir una frase optimizada en una ley universal

El mismo paper muestra dependencia del modelo y de la tarea.

Por tanto, copiar un trigger porque obtuvo mejor score en un benchmark concreto contradice parcialmente la propia filosofía de APE.

La filosofía correcta es:

```text
GENERA VARIANTES
→ PRUÉBALAS
→ ELIGE
```

---

# 31. APE como metodología para prompts maestros

Aplicación directa:

```text
PROMPT MAESTRO v1
↓
generar variantes:
  - estructura
  - wording
  - ejemplos
  - orden
↓
evaluation suite
↓
ranking
↓
análisis de errores
↓
v2
```

Esto es mucho más sólido que editar el prompt indefinidamente por intuición.

---

# 32. Qué partes de un prompt pueden optimizarse

No únicamente la instrucción completa.

Se pueden explorar variantes de:

- encabezados;
- orden;
- definición de éxito;
- reglas;
- formato de salida;
- ejemplos;
- wording;
- fallback;
- criterios de evaluación.

Siempre una variable cada vez cuando queramos atribución clara.

---

# 33. Prompt search necesita un conjunto de evaluación representativo

Si el dataset de scoring no representa producción, APE optimizará para el problema equivocado.

Esto es equivalente a overfitting.

## Principio

```text
mala evaluación
→ prompt "óptimo" equivocado
```

---

# 34. Separar train / validation / test conceptualmente

El paper utiliza conjuntos para generar/seleccionar y posteriormente evaluar.

Para prompts de producción deberíamos mantener:

```text
development set
→ iteración

held-out set
→ selección

regression set
→ protección futura
```

---

# 35. Automatización + humanos

APE demuestra que el modelo puede producir prompts al nivel o por encima de los prompts humanos en los benchmarks estudiados.

Pero eso no implica eliminar el papel humano.

Los humanos siguen definiendo:

- objetivo;
- dataset;
- métrica;
- restricciones;
- aceptación;
- riesgos.

## Síntesis

> **Automatizar la búsqueda no automatiza la definición del problema.**

---

# 36. Antipatrones

## Antipatrón 1 — Elegir prompt por preferencia personal

Medir.

## Antipatrón 2 — Optimizar una única métrica mal diseñada

Puede generar soluciones degeneradas.

## Antipatrón 3 — Probar prompts sobre los mismos casos que luego usas para afirmar calidad

Riesgo de sobreajuste.

## Antipatrón 4 — Reutilizar prompt al cambiar de modelo sin regression tests

La transferencia puede ser mala.

## Antipatrón 5 — Búsqueda iterativa infinita

Los rendimientos decrecen.

## Antipatrón 6 — Generar variantes sin scoring

Eso no es optimización; es brainstorming.

---

# 37. Qué merece la pena absorber permanentemente

1. **Prompt engineering puede formularse como optimización.**
2. **Un prompt es un programa de lenguaje natural en el sentido operacional del paper.**
3. **La calidad debe medirse ejecutando el prompt.**
4. **Generator y evaluator son componentes diferentes.**
5. **Los ejemplos pueden utilizarse para inducir instrucciones.**
6. **Generar múltiples candidatos supera depender de una única redacción.**
7. **La función objetivo define qué comportamiento se optimiza.**
8. **Una mala métrica produce un prompt aparentemente bueno pero realmente malo.**
9. **Adaptive filtering puede ahorrar mucho coste.**
10. **Más candidatos ayudan con rendimientos decrecientes.**
11. **Refinamiento iterativo no siempre mejora suficientemente.**
12. **Prompt y modelo forman una pareja; la transferencia no está garantizada.**
13. **Meta-prompts también deben optimizarse.**
14. **El coste offline puede amortizarse con prompts más cortos en producción.**
15. **Cambiar de modelo exige reevaluación.**
16. **Medición > intuición.**

---

# 38. Pipeline recomendado de Automatic Prompt Optimization

```text
1. definir tarea
2. construir ejemplos
3. definir score
4. generar N candidatos
5. evaluación barata
6. filtrar
7. evaluación completa
8. seleccionar top-k
9. analizar fallos
10. opcionalmente mutar/refinar
11. evaluar en held-out
12. desplegar
13. monitorizar
```

---

# 39. Checklist

- [ ] ¿Existe una definición objetiva de éxito?
- [ ] ¿Tenemos casos representativos?
- [ ] ¿Existe held-out set?
- [ ] ¿La métrica se correlaciona con utilidad real?
- [ ] ¿Generamos suficientes candidatos?
- [ ] ¿Hay diversidad real?
- [ ] ¿Se filtran candidatos malos pronto?
- [ ] ¿Comparamos contra prompt humano/base?
- [ ] ¿Medimos coste?
- [ ] ¿Medimos longitud?
- [ ] ¿Probamos transferencia al modelo real?
- [ ] ¿Reoptimizamos cuando cambia el modelo?
- [ ] ¿Vigilamos sobreajuste?
- [ ] ¿La iteración adicional mejora suficientemente?

---

# 40. Síntesis final

La contribución más importante de APE no es que un LLM pueda escribir un prompt.

Eso ya sería poco sorprendente.

La contribución conceptual es:

> **Dejar de tratar el prompt como una pieza de prosa y empezar a tratarlo como una variable optimizable.**

El proceso correcto es:

```text
PROPONER
→ EJECUTAR
→ MEDIR
→ SELECCIONAR
```

y, solo si aporta valor:

```text
→ MUTAR
→ VOLVER A MEDIR
```

Esta idea es especialmente importante para nuestros prompts maestros.

Un prompt maestro no debería declararse “mejor” porque:

- sea más largo;
- tenga más reglas;
- suene más profesional.

Debería considerarse mejor cuando:

> **supera de forma reproducible a su versión anterior sobre una suite representativa y sin introducir regresiones relevantes.**
