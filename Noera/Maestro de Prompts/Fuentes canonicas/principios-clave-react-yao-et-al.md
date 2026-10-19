# Principios clave de *ReAct: Synergizing Reasoning and Acting in Language Models*

**Autores:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan y Yuan Cao  
**Publicación:** ICLR 2023  
**Objetivo de este documento:** condensar las ideas útiles del paradigma ReAct para diseño de agentes, tool use, RAG interactivo, workflows y prompts maestros.

---

# 1. Idea central

El paper parte de una separación habitual:

```text
RAZONAR
```

por un lado y:

```text
ACTUAR
```

por otro.

ReAct combina ambos dentro de una trayectoria intercalada:

```text
THOUGHT
↓
ACTION
↓
OBSERVATION
↓
THOUGHT
↓
ACTION
↓
OBSERVATION
...
↓
FINAL
```

La idea fundamental:

> **El modelo puede razonar para decidir qué información o acción necesita y utilizar las observaciones externas para corregir el razonamiento posterior.**

---

# 2. Razonamiento sin mundo externo tiene una limitación

Un modelo puede producir una secuencia lógica coherente basada en:

- memoria interna;
- suposiciones;
- conocimientos aprendidos.

Pero si uno de esos hechos es incorrecto, el error puede propagarse por toda la cadena.

ReAct introduce acciones para obtener información desde el entorno.

Ejemplo:

```text
Necesito saber X
→ search[X]
→ observación
→ ahora puedo decidir Y
```

---

# 3. Acción sin razonamiento también tiene una limitación

El paper compara ReAct con métodos de “Act-only”.

Un agente que únicamente reacciona a observaciones puede:

- perder el objetivo global;
- ejecutar acciones irrelevantes;
- no descomponer el problema;
- perder el estado;
- repetir acciones.

El razonamiento intermedio ayuda a mantener:

```text
objetivo
subobjetivo
estado actual
siguiente acción
```

---

# 4. ReAct = bucle cerrado

La diferencia conceptual clave frente a una respuesta puramente generativa es el feedback del entorno.

```text
modelo
→ acción
→ mundo
→ observación
→ modelo
```

Esto crea un **closed-loop system**.

La siguiente decisión no depende solo del texto inicial, sino del resultado real de la acción anterior.

---

# 5. Las observaciones pueden corregir al modelo

Si el modelo piensa:

```text
"X debería estar aquí"
```

y la herramienta devuelve:

```text
"X no está aquí"
```

el agente puede modificar su plan.

Esta capacidad es crítica en entornos donde:

- la información es desconocida;
- el estado cambia;
- las acciones pueden fallar;
- el modelo no puede conocer todo de antemano.

---

# 6. El razonamiento puede cumplir varias funciones

El paper identifica usos distintos de los “thoughts”:

- descomponer la tarea;
- crear planes;
- incorporar conocimiento de sentido común;
- extraer elementos importantes de una observación;
- llevar registro del progreso;
- modificar planes;
- manejar excepciones;
- decidir nuevas búsquedas.

Esto es importante:

> **El razonamiento de un agente no tiene una única función.**

---

# 7. Acción y observación introducen grounding

En HotpotQA y FEVER, ReAct utiliza una API simple de Wikipedia.

Las acciones incluyen:

```text
search[entity]
lookup[string]
finish[answer]
```

Esto obliga al modelo a buscar información externa en vez de depender únicamente de memoria paramétrica.

## Principio

> **Cuando una afirmación puede obtenerse del entorno, una observación externa puede ser más fiable que seguir elaborando memoria interna.**

---

# 8. ReAct redujo alucinaciones frente a CoT en el análisis manual

En el análisis de HotpotQA, los autores encontraron que las alucinaciones constituían una fuente de fallo mucho mayor para CoT.

ReAct producía trayectorias más:

- grounded;
- basadas en hechos;
- inspeccionables.

La razón era precisamente el acceso a información externa.

---

# 9. Pero retrieval deficiente puede destruir la trayectoria

El paper también muestra el reverso.

En ReAct, una búsqueda poco informativa podía desviar la resolución y dificultar la recuperación posterior.

En su análisis, las búsquedas no informativas representaban una fracción importante de los errores.

## Lección crucial

> **Dar acceso a búsqueda no resuelve el problema si el agente no sabe formular buenas consultas.**

Necesitamos evaluar:

```text
query formulation
retrieval quality
observation interpretation
```

---

# 10. Reasoning y retrieval forman un ciclo

La arquitectura correcta no siempre es:

```text
retrieve once
→ answer
```

ReAct demuestra un patrón más dinámico:

```text
razonar
→ detectar hueco
→ buscar
→ observar
→ razonar de nuevo
→ buscar otra cosa
```

Esto es especialmente útil para preguntas multi-hop.

---

# 11. ReAct anticipa agentes tool-using modernos

El principio general es:

```text
LLM como policy / planner
+
tools como action space
+
resultados de tools como observations
```

No importa si la herramienta es:

- Wikipedia;
- navegador;
- calculadora;
- API;
- base de datos;
- filesystem;
- ejecución de código.

La arquitectura conceptual es la misma.

---

# 12. El action space debe diseñarse

En el paper, el espacio de acciones está deliberadamente limitado.

Eso ofrece una enseñanza clave:

> **Un agente no debería recibir todas las acciones imaginables; debe recibir un conjunto de capacidades relevantes y controladas.**

Cada herramienta adicional aumenta:

- posibilidades;
- errores;
- superficie de búsqueda;
- riesgos.

---

# 13. Tool descriptions forman parte del comportamiento

Para que el modelo elija correctamente una acción, debe poder distinguir:

```text
qué hace
cuándo usarla
qué devuelve
```

Aunque el paper trabaja con acciones sencillas, la extrapolación arquitectónica es directa:

```text
search
lookup
finish
```

son comandos semánticamente claros.

---

# 14. Pensamiento → acción → observación debe conservar estado

Cada nueva decisión utiliza el historial:

```text
observaciones anteriores
acciones anteriores
resultados
progreso
```

El contexto funciona como memoria de trabajo.

## Riesgo

Si la trayectoria se hace demasiado larga:

- crece el contexto;
- aumenta ruido;
- puede perderse información importante.

Por eso agentes largos necesitan gestión de memoria y estado.

---

# 15. ReAct puede caer en loops

Los autores observan un patrón de fallo específico:

```text
Thought A
Action A
Observation
Thought A
Action A
...
```

El modelo puede repetir pensamientos y acciones anteriores sin reconocer que debe cambiar de estrategia.

## Principio de producción

Todo agente necesita mecanismos de:

- detección de repetición;
- límite de pasos;
- timeout;
- presupuesto;
- fallback.

---

# 16. Reasoning puede reducir flexibilidad

El paper señala un trade-off.

La estructura intercalada:

```text
thought → action → observation
```

mejora grounding, pero puede restringir la flexibilidad de razonamiento y producir más errores de reasoning en algunos contextos que CoT puro.

## Lección

No existe un paradigma dominante para todas las tareas.

---

# 17. ReAct + CoT-SC obtuvo los mejores resultados de prompting en QA

En HotpotQA y FEVER, combinaciones de ReAct con CoT + Self-Consistency rindieron mejor que usar únicamente uno de los enfoques.

Esto respalda una idea sistémica:

```text
conocimiento interno
+
información externa
+
agregación
```

puede ser mejor que cualquiera de los tres de forma aislada.

---

# 18. Internal knowledge y external knowledge son complementarios

CoT puede ser bueno estructurando razonamiento, pero susceptible a hechos inventados.

ReAct puede estar mejor grounded, pero fallar si retrieval o tool use son deficientes.

Por tanto:

```text
internal reasoning
↔
external evidence
```

deben trabajar juntos.

---

# 19. Sparse reasoning puede ser suficiente

En tareas interactivas largas, el paper no exige un thought antes de absolutamente cada acción.

Utiliza razonamiento más esporádico para:

- descomponer;
- revisar progreso;
- reajustar.

## Principio práctico

> **El agente no necesita “razonar” con la misma intensidad en cada paso.**

Puede utilizarse deliberación en puntos de decisión.

---

# 20. Los resultados en ALFWorld muestran la importancia del estado

Act-only tenía problemas para:

- descomponer objetivos;
- recordar qué había ocurrido;
- determinar siguiente subobjetivo.

ReAct mejoraba esos aspectos mediante reasoning traces.

Esto es relevante para cualquier workflow largo.

---

# 21. Los resultados en WebShop muestran el valor de conectar observaciones con objetivos

En WebShop, ReAct podía razonar sobre si:

- el producto;
- las opciones;
- los atributos;

encajaban con la petición.

La idea general es:

```text
OBSERVACIÓN RUIDOSA
↓
INTERPRETAR RESPECTO AL OBJETIVO
↓
ACCIÓN
```

---

# 22. Fine-tuning de comportamiento puede ser más valioso que memorizar hechos

Una de las observaciones interesantes del paper:

Fine-tuning de ReAct/Act podía enseñar al modelo **cómo acceder a información**, en vez de intentar memorizar todos los hechos necesarios.

Eso sugiere una distinción:

```text
enseñar conocimiento
vs.
enseñar procedimiento para adquirir conocimiento
```

En dominios cambiantes, lo segundo puede generalizar mejor.

---

# 23. Demostraciones ReAct son trayectorias completas

Los few-shot examples contienen:

```text
Thought
Action
Observation
Thought
Action
...
Final
```

Por tanto, el ejemplo enseña simultáneamente:

- política de decisión;
- formato;
- cuándo buscar;
- cómo interpretar observaciones;
- cuándo detenerse.

## Consecuencia

En agentes, un ejemplo de trayectoria puede ser mucho más informativo que una descripción abstracta de comportamiento.

---

# 24. Más ejemplos no siempre ayudan

En el setup de HotpotQA/FEVER, los autores indican que añadir más ejemplos no mejoró el rendimiento.

## Lección

> **Contexto adicional debe demostrar valor, no asumirse útil por defecto.**

Las trayectorias ReAct son largas, por lo que cada ejemplo tiene un coste significativo de contexto.

---

# 25. Limitación: large action spaces + in-context learning

El paper señala que tareas complejas con grandes espacios de acción pueden requerir más demostraciones de las que caben cómodamente en contexto.

Esto crea una razón para considerar:

- fine-tuning;
- retrieval de ejemplos;
- políticas especializadas;
- jerarquías de herramientas.

---

# 26. Los agentes reales introducen riesgos reales

El ethics statement del paper destaca que conectar un LLM con un entorno puede permitir:

- acceder a información inapropiada o privada;
- ejecutar acciones dañinas.

Los experimentos limitan deliberadamente la capacidad de actuación.

## Principio fundamental

> **La seguridad de un agente depende en gran medida de su action space.**

---

# 27. Capacidad mínima necesaria

Una regla práctica derivada:

```text
si el agente solo necesita leer
→ no darle escritura

si solo necesita buscar
→ no darle ejecución

si solo necesita una API
→ no darle navegador completo
```

Reducir privilegios reduce riesgo.

---

# 28. Confirmaciones y permisos fuera del modelo

ReAct demuestra que el modelo puede decidir acciones.

Pero en sistemas de producción, las acciones de alto impacto deberían estar protegidas por:

- autorización;
- permisos;
- validación;
- human-in-the-loop;
- límites.

No confiar únicamente en la planificación del modelo.

---

# 29. Evaluar la trayectoria, no solamente el resultado

Un agente puede llegar a una respuesta correcta mediante:

- acciones innecesarias;
- búsquedas arriesgadas;
- razonamiento frágil.

Por eso conviene medir:

```text
success
+
tool selection
+
query quality
+
number of steps
+
loops
+
cost
+
evidence quality
```

---

# 30. Diagnosability es una ventaja importante

Las trayectorias ReAct permiten inspeccionar:

```text
qué pensaba hacer
qué herramienta usó
qué observó
por qué cambió
```

Esto ayuda a localizar fallos.

En sistemas complejos, esa trazabilidad puede ser tan importante como mejorar unos puntos de accuracy.

---

# 31. Arquitectura ReAct generalizada

```text
OBJECTIVE
↓
STATE
↓
DECIDE
├─ need information → TOOL
├─ need action      → TOOL
└─ enough evidence  → FINAL
↓
OBSERVATION
↓
UPDATE STATE
↓
repeat
```

---

# 32. Aplicación a prompts maestros

Una sección útil sería:

```markdown
## Política de interacción con herramientas

Antes de responder:

1. determina si la información disponible es suficiente;
2. si falta una pieza verificable, utiliza la herramienta adecuada;
3. incorpora la observación al estado actual;
4. actualiza el plan;
5. evita repetir una acción que ya produjo el mismo resultado;
6. termina cuando exista evidencia suficiente.
```

---

# 33. Separar "decidir" de "actuar"

Un agente robusto necesita que la acción sea resultado de una decisión explícita.

```text
OBJETIVO
→ EVALUAR ESTADO
→ SELECCIONAR ACCIÓN
→ VALIDAR
→ EJECUTAR
```

No:

```text
OBJETIVO
→ ejecutar impulsivamente
```

---

# 34. Antipatrones

## Antipatrón 1 — Agente sin límite de pasos

Riesgo de loops y coste infinito.

## Antipatrón 2 — Herramientas redundantes

Complica tool selection.

## Antipatrón 3 — Confiar en memoria paramétrica para datos verificables

Si existe fuente autoritativa, úsala.

## Antipatrón 4 — Retrieval de una sola vez para preguntas multi-hop

Puede faltar información descubierta durante el proceso.

## Antipatrón 5 — Exponer acciones peligrosas innecesariamente

El action space debe seguir mínimo privilegio.

## Antipatrón 6 — Evaluar solo el answer

Hay que evaluar el camino.

---

# 35. Qué merece la pena absorber permanentemente

1. **Razonar y actuar son capacidades complementarias.**
2. **Las observaciones externas pueden corregir conocimiento interno erróneo.**
3. **El razonamiento ayuda a elegir acciones y mantener el objetivo.**
4. **Los agentes deben operar en bucle cerrado.**
5. **Retrieval puede ser iterativo.**
6. **La calidad de una query de búsqueda importa muchísimo.**
7. **Un mal retrieval puede desviar toda la trayectoria.**
8. **El contexto del agente funciona como memoria de trabajo.**
9. **Los loops son un failure mode explícito que debe controlarse.**
10. **Más herramientas implican mayor complejidad y riesgo.**
11. **El action space debe limitarse.**
12. **Leer y escribir no deberían tener los mismos permisos.**
13. **Las trayectorias completas son excelentes ejemplos few-shot.**
14. **Internal knowledge y external evidence deben combinarse.**
15. **El comportamiento para adquirir información puede ser más generalizable que memorizar hechos.**
16. **Los agentes necesitan observabilidad y evaluación de trayectoria.**

---

# 36. Checklist para un agente inspirado en ReAct

- [ ] ¿Está definido el objetivo?
- [ ] ¿Está definido el estado?
- [ ] ¿Cada herramienta tiene función única?
- [ ] ¿El modelo sabe cuándo utilizarla?
- [ ] ¿Las observaciones vuelven al contexto?
- [ ] ¿Existe query reformulation?
- [ ] ¿Existe detección de loops?
- [ ] ¿Existe límite de pasos?
- [ ] ¿Existe límite de coste?
- [ ] ¿Las acciones de escritura están protegidas?
- [ ] ¿Existe criterio explícito de finalización?
- [ ] ¿Se registran acciones y observaciones?
- [ ] ¿Se evalúa retrieval?
- [ ] ¿Se evalúa tool selection?
- [ ] ¿Se evalúa el resultado final?

---

# 37. Síntesis final

La aportación más duradera de ReAct es cambiar el modelo mental desde:

```text
LLM = generador de respuesta
```

hacia:

```text
LLM = componente que decide dentro de un ciclo de interacción
```

El patrón:

```text
DECIDIR
→ ACTUAR
→ OBSERVAR
→ ACTUALIZAR
```

es una de las bases de los agentes modernos.

Pero el paper también muestra claramente sus límites:

- retrieval puede fallar;
- el modelo puede entrar en loops;
- demasiadas acciones complican la tarea;
- contextos largos limitan few-shot;
- grounding y flexibilidad tienen trade-offs.

Por tanto:

> **Un buen agente no es el que puede hacer más cosas, sino el que dispone exactamente de las acciones necesarias, sabe cuándo utilizarlas y recibe feedback suficiente para corregirse.**
