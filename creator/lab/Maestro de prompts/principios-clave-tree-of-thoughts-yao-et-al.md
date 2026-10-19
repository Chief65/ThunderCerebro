# Principios clave de *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*

**Autores:** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao y Karthik Narasimhan  
**Publicación:** NeurIPS 2023  
**Objetivo de este documento:** condensar las ideas útiles de Tree of Thoughts para búsqueda, planificación, selección de alternativas y resolución deliberada de problemas con LLMs.

---

# 1. Idea central

Chain-of-Thought recorre normalmente una sola trayectoria:

```text
entrada
→ pensamiento 1
→ pensamiento 2
→ pensamiento 3
→ respuesta
```

Tree of Thoughts plantea:

```text
                    opción A
                  ↗
entrada → opciones → opción B → ...
                  ↘
                    opción C
```

El sistema:

1. genera varias continuaciones;
2. evalúa cuáles parecen prometedoras;
3. conserva algunas;
4. explora más;
5. puede descartar;
6. puede volver atrás.

La idea central:

> **Algunos problemas no deberían resolverse como una única secuencia irreversible, sino como búsqueda sobre alternativas.**

---

# 2. Limitación de la generación left-to-right

Un modelo autoregresivo toma decisiones token a token.

En problemas con decisiones tempranas importantes, un error inicial puede condenar toda la solución.

CoT mejora el proceso, pero normalmente sigue siendo una sola trayectoria.

ToT introduce:

- branching;
- evaluación;
- lookahead;
- pruning;
- backtracking.

---

# 3. Pensar en términos de search space

El paper conecta LLMs con algoritmos clásicos de búsqueda.

Un problema se representa como:

```text
ESTADO ACTUAL
↓
CANDIDATOS
↓
EVALUACIÓN
↓
EXPANSIÓN DE LOS MEJORES
↓
NUEVO ESTADO
```

Esto convierte el problema en búsqueda sobre soluciones parciales.

---

# 4. Qué es un “thought” en ToT

Un thought no tiene tamaño fijo.

Puede ser:

- unas palabras;
- una ecuación;
- un plan;
- un párrafo.

Los autores dan una regla conceptual excelente:

> Un thought debe ser suficientemente pequeño para poder generar alternativas diversas, pero suficientemente grande para poder evaluar si conduce hacia una buena solución.

Esto es uno de los principios más útiles del paper.

---

# 5. Granularidad correcta

Demasiado pequeño:

```text
token
```

es difícil de evaluar semánticamente.

Demasiado grande:

```text
solución completa
```

reduce la capacidad de corregir decisiones intermedias.

Por tanto:

```text
unidad intermedia significativa
```

es la granularidad deseada.

---

# 6. ToT tiene cuatro decisiones de diseño

El paper estructura una implementación de ToT alrededor de cuatro preguntas:

```text
1. ¿Cómo dividir el problema en thoughts?
2. ¿Cómo generar candidatos?
3. ¿Cómo evaluar estados?
4. ¿Cómo buscar entre ellos?
```

Esta descomposición es extremadamente útil incluso fuera de ToT.

---

# 7. Thought decomposition depende del problema

Ejemplos del paper:

## Game of 24

Un thought = una ecuación intermedia.

## Creative Writing

Un thought = un plan de escritura.

## Crosswords

Un thought = una palabra candidata.

## Lección

> **La arquitectura de razonamiento debe adaptarse a la estructura natural de la tarea.**

No existe una unidad de razonamiento universal.

---

# 8. Generación de candidatos: sampling independiente

Cuando el espacio de soluciones es rico, se pueden generar varias propuestas independientes.

Ejemplo:

```text
Plan A
Plan B
Plan C
Plan D
Plan E
```

Esto busca diversidad.

---

# 9. Generación secuencial de propuestas

Cuando el espacio es más restringido, el paper utiliza un “propose prompt” que genera candidatos diferentes dentro del mismo contexto.

Esto reduce duplicados.

## Principio

> **La estrategia de diversidad también debe adaptarse al espacio de soluciones.**

---

# 10. El evaluador funciona como heurística

Una vez generadas soluciones parciales, hay que decidir cuáles seguir explorando.

ToT utiliza el propio modelo como una heurística.

Puede producir:

```text
sure
maybe
impossible
```

o una puntuación.

## Importante

El evaluador no necesita ser perfecto.

Necesita ser suficientemente informativo para descartar caminos malos y promover caminos prometedores.

---

# 11. Value evaluation

Una estrategia evalúa cada estado de forma independiente.

Ejemplo:

```text
Estado A → 0.8
Estado B → 0.2
Estado C → 0.6
```

Puede utilizar:

- lookahead;
- restricciones;
- sentido común;
- posibilidad de completar la solución.

---

# 12. Vote evaluation

Cuando es difícil puntuar de forma absoluta, el paper propone comparar alternativas.

```text
A vs B vs C
→ elegir la más prometedora
```

Esto es útil para problemas subjetivos como coherencia de escritura.

## Principio

> **Comparar candidatos puede ser más fácil que asignarles scores absolutos.**

---

# 13. El evaluador también puede samplearse varias veces

Igual que con Self-Consistency, el valor o voto puede agregarse sobre múltiples ejecuciones.

Esto permite intercambiar:

```text
coste
↔
robustez
```

---

# 14. Search algorithm debe adaptarse a la estructura

El paper utiliza:

- BFS;
- DFS.

## BFS

Adecuado cuando:

- profundidad pequeña;
- quieres conservar varios candidatos simultáneamente.

## DFS

Adecuado cuando:

- buscas una ruta profunda;
- puedes detectar pronto estados imposibles;
- el backtracking es útil.

---

# 15. Pruning es esencial

Explorar todas las ramas es inviable.

Por eso ToT necesita eliminar estados poco prometedores.

```text
generar 10
→ evaluar
→ conservar 3
→ expandir
```

## Principio

> **La inteligencia del sistema no está solo en generar ideas, sino en abandonar malas ideas pronto.**

---

# 16. Backtracking corrige decisiones tempranas

CoT normalmente continúa hacia adelante aunque una decisión temprana haya sido mala.

ToT permite:

```text
ruta A
→ bloqueo
→ volver
→ probar B
```

Esto es especialmente valioso cuando:

- una decisión inicial condiciona fuertemente el resultado;
- existe feedback parcial;
- se puede identificar un callejón sin salida.

---

# 17. Lookahead evita comprometerse demasiado pronto

En Game of 24, el modelo evalúa si un estado parcial todavía puede alcanzar la solución.

Esto es una forma de lookahead.

## Aplicación general

Antes de aceptar un plan:

```text
¿qué consecuencias tiene?
¿puede cumplir las restricciones restantes?
¿crea un callejón sin salida?
```

---

# 18. ToT generaliza otros métodos como casos especiales

Los autores presentan:

- input-output;
- CoT;
- Self-Consistency;
- self-refinement;

como configuraciones más restringidas dentro de la idea general de un árbol.

Conceptualmente:

```text
CoT
= profundidad > 1, anchura ≈ 1

Self-Consistency
= varias cadenas completas sin exploración local

ToT
= anchura + profundidad + evaluación + search
```

---

# 19. Modularity es una gran ventaja

ToT separa componentes:

```text
MODEL
THOUGHT DECOMPOSITION
GENERATOR
EVALUATOR
SEARCH
```

Esto permite cambiar uno sin cambiar los demás.

## Principio de ingeniería

> **Separar generación, evaluación y búsqueda mejora experimentación y depuración.**

---

# 20. Adaptabilidad

Distintos problemas pueden utilizar:

- diferentes thoughts;
- diferentes evaluadores;
- diferentes search algorithms;
- diferente anchura;
- diferente profundidad.

No existe una configuración ToT universal.

---

# 21. Game of 24 muestra el problema de decisiones tempranas

En el experimento principal:

- IO: 7.3%;
- CoT: 4%;
- CoT-SC: 9%;
- ToT con breadth 5: 74%.

Los autores observan que aproximadamente el 60% de muestras CoT ya habían tomado un camino inviable tras el primer paso.

## Lección

> **Si un error temprano destruye la solución, explorar alternativas localmente puede ser mucho más útil que generar muchas soluciones completas.**

---

# 22. Best-of-many no equivale a search

El paper compara ToT con tomar el mejor de muchas cadenas completas.

Incluso con 100 samples, CoT best-of-100 quedó por debajo de ToT en Game of 24.

Esto ilustra:

```text
100 intentos independientes
```

no es necesariamente equivalente a:

```text
explorar sistemáticamente
+
reutilizar progreso
+
podar
+
retroceder
```

---

# 23. Creative Writing muestra que search también puede ser semántico

No todas las búsquedas son matemáticas.

El paper genera planes alternativos para construir un texto coherente.

Después compara planes y desarrolla los más prometedores.

## Lección

> **La búsqueda puede operar sobre unidades semánticas de alto nivel, no solo estados formalizables.**

---

# 24. Refinement puede verse como otra forma de generación

En Creative Writing, los autores estudian refinar outputs anteriores.

Esto sugiere una tercera forma de explorar:

```text
generar nuevo candidato
```

vs.

```text
modificar candidato existente
```

Ambas pueden formar parte del espacio de búsqueda.

---

# 25. Crosswords muestra la necesidad de backtracking

Los crucigramas exigen decisiones que se condicionan mutuamente.

El sistema utiliza DFS:

```text
rellenar palabra
→ evaluar restricciones
→ continuar
→ si inconsistente
→ retroceder
```

Es una demostración clara de que ciertos problemas son naturalmente árboles, no cadenas.

---

# 26. Elegir ToT solo cuando el problema lo necesita

El propio paper señala que búsqueda deliberada puede ser innecesaria en tareas que el modelo ya resuelve bien con CoT.

En experimentos adicionales, las mejoras en GSM8K y StrategyQA fueron pequeñas cuando GPT-4 + CoT ya tenía buen rendimiento.

## Regla crítica

> **No usar ToT porque sea más sofisticado. Usarlo cuando exista un problema real de search/planning.**

---

# 27. Coste significativamente mayor

El paper cuantifica el coste.

En sus experimentos ToT requiere mucho más cómputo que IO o CoT.

Por ejemplo, en Creative Writing utilizó aproximadamente cinco veces más tokens/coste.

## Consecuencia

ToT es un mecanismo de **test-time compute**.

Debe justificarse.

---

# 28. Performance-cost tradeoff

Los parámetros principales incluyen:

```text
breadth
depth
# candidates
# evaluations
search strategy
```

Todos modifican:

```text
calidad
coste
latencia
```

Por tanto deben tratarse como hiperparámetros.

---

# 29. Modelos diferentes para generación y evaluación

El paper realiza una exploración interesante combinando GPT-4 y GPT-3.5 para distintos componentes.

En Game of 24, los resultados sugieren que la calidad de la **generación** era un cuello de botella importante.

Esto demuestra:

> **El generador y el evaluador no necesariamente necesitan ser el mismo modelo.**

---

# 30. Routing por componente

Una arquitectura moderna podría usar:

```text
modelo potente → generar candidatos difíciles
modelo barato → evaluación preliminar
código → verificar restricciones
search algorithm → organizar exploración
```

Esto puede reducir coste.

---

# 31. Evaluadores deterministas cuando sea posible

En Game of 24, la validez final de una ecuación puede verificarse exactamente.

Para un sistema práctico:

```text
LLM → propone
código → verifica
```

puede ser más robusto que pedir al modelo que juzgue todo.

---

# 32. ToT como arquitectura, no como prompt único

Un error conceptual sería intentar convertir ToT en una frase dentro de un único prompt.

El paper realmente describe un **framework de inferencia** con múltiples llamadas y un algoritmo de búsqueda.

## Principio

> **Algunas mejoras no pertenecen al texto del prompt; pertenecen al orquestador.**

---

# 33. Aplicación a prompts maestros

Un prompt maestro puede definir cuándo activar búsqueda:

```markdown
## Planificación deliberada

Activa exploración de alternativas cuando:

- una decisión temprana pueda bloquear la solución;
- existan múltiples planes plausibles;
- la tarea requiera optimización;
- se pueda evaluar progreso parcial.

Proceso:

1. genera varios candidatos;
2. descarta los que violen restricciones;
3. puntúa los restantes;
4. expande los mejores;
5. retrocede si un camino se vuelve inviable;
6. detente cuando exista una solución verificada.
```

---

# 34. Diferencia entre Self-Consistency y ToT

## Self-Consistency

```text
generar varias soluciones completas
→ votar
```

## ToT

```text
generar alternativas parciales
→ evaluar
→ elegir
→ expandir
→ retroceder
```

Por tanto:

> Self-Consistency explora principalmente **entre trayectorias completas**; ToT explora **dentro del proceso de construcción de la trayectoria**.

---

# 35. Antipatrones

## Antipatrón 1 — Tree of Thoughts para tareas sencillas

Coste sin beneficio.

## Antipatrón 2 — Branching sin evaluador

Generar opciones sin poder descartarlas solo multiplica ruido.

## Antipatrón 3 — Evaluador no calibrado

Si la heurística es mala, el search puede podar la respuesta correcta.

## Antipatrón 4 — Thoughts demasiado grandes

Pierdes capacidad de corregir.

## Antipatrón 5 — Thoughts demasiado pequeños

No puedes evaluarlos.

## Antipatrón 6 — No limitar breadth/depth

Explosión combinatoria.

---

# 36. Qué merece la pena absorber permanentemente

1. **Algunos problemas son espacios de búsqueda, no cadenas.**
2. **Una decisión inicial incorrecta puede justificar branching.**
3. **Generación, evaluación y búsqueda son componentes distintos.**
4. **La granularidad de los estados intermedios importa.**
5. **Un buen estado debe ser generable y evaluable.**
6. **La diversidad local puede ser más útil que muchas soluciones completas.**
7. **Pruning es tan importante como generación.**
8. **Backtracking permite corregir compromisos tempranos.**
9. **Lookahead reduce callejones sin salida.**
10. **Comparar candidatos puede ser más fácil que puntuarlos absolutamente.**
11. **El algoritmo de search debe adaptarse al problema.**
12. **ToT es una arquitectura de inferencia, no una frase mágica.**
13. **Más búsqueda significa mayor coste.**
14. **Usar ToT únicamente cuando el problema tenga estructura de planificación/search.**

---

# 37. Checklist

- [ ] ¿El problema realmente necesita búsqueda?
- [ ] ¿Existen decisiones tempranas de alto impacto?
- [ ] ¿Cuál es la unidad correcta de thought?
- [ ] ¿Cómo se generan alternativas?
- [ ] ¿Cómo se garantiza diversidad?
- [ ] ¿Cómo se evalúan estados parciales?
- [ ] ¿Existe verificador determinista?
- [ ] ¿BFS o DFS?
- [ ] ¿Cuál es el breadth?
- [ ] ¿Cuál es la profundidad máxima?
- [ ] ¿Cuándo se poda?
- [ ] ¿Cuándo se retrocede?
- [ ] ¿Cuál es el criterio de finalización?
- [ ] ¿Cuánto cuesta frente a CoT?
- [ ] ¿La mejora compensa el coste?

---

# 38. Síntesis final

Tree of Thoughts aporta una idea diferente a “razonar más”.

La idea real es:

> **Explorar, evaluar y revisar decisiones antes de comprometerse con una única solución.**

Esto convierte un LLM de generador lineal en componente de una arquitectura de búsqueda.

La versión más útil del principio para sistemas modernos es:

```text
GENERATE
→ EVALUATE
→ PRUNE
→ EXPAND
→ BACKTRACK
→ VERIFY
```

Pero solamente cuando el problema lo justifique.

La sofisticación no es el objetivo.

El objetivo es utilizar búsqueda deliberada cuando una trayectoria lineal no sea suficiente.
