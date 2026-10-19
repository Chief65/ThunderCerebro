# Principios clave de *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*

**Autores:** Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le y Denny Zhou  
**Trabajo:** *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*  
**Publicación:** NeurIPS 2022  
**Objetivo de este documento:** condensar las ideas verdaderamente reutilizables del paper para el diseño de prompts, sistemas de razonamiento y workflows con LLMs.

> Este documento no reproduce el paper. Separa sus resultados empíricos concretos de los principios de diseño que merece la pena conservar.

---

# 1. Idea central

El paper introduce una idea extremadamente sencilla pero fundamental:

> En tareas que requieren varios pasos, enseñar al modelo ejemplos que incluyan **pasos intermedios** puede producir resultados muy superiores a enseñarle únicamente entrada → respuesta.

La estructura estudiada es:

```text
ENTRADA
→ PASOS INTERMEDIOS
→ RESPUESTA
```

en lugar de:

```text
ENTRADA
→ RESPUESTA
```

Los autores denominan a esos pasos intermedios **chain of thought**.

La contribución importante no es únicamente la frase “pensar paso a paso”, sino el principio de que el **espacio de salida puede utilizarse como espacio de trabajo intermedio** antes de llegar a la respuesta final.

---

# 2. Qué problema intenta resolver

El few-shot prompting tradicional demuestra al modelo pares del tipo:

```text
Pregunta → Respuesta
```

Esto funciona bien en muchas tareas sencillas.

Pero existen tareas en las que la transformación entre entrada y respuesta requiere operaciones intermedias:

```text
comprender
→ descomponer
→ calcular
→ combinar
→ responder
```

Si únicamente se muestran respuestas finales, el modelo debe inferir internamente toda esa estructura.

Chain-of-Thought Prompting modifica los ejemplos para mostrar:

```text
Pregunta
→ secuencia de pasos
→ respuesta final
```

La hipótesis es que proporcionar esa estructura facilita que el modelo produzca soluciones multietapa.

---

# 3. La unidad útil no es solamente la respuesta: también el procedimiento

Este paper introduce una lección general para prompts avanzados:

> Cuando la calidad depende del procedimiento, enseñar solamente el resultado puede ser insuficiente.

Esto puede aplicarse a muchos contextos.

En vez de:

```text
Entrada:
código

Salida:
"hay un bug"
```

puede ser más informativo demostrar:

```text
Entrada:
código

Análisis:
- identificar flujo
- revisar estado
- comprobar condición
- localizar contradicción

Salida:
bug + evidencia
```

El principio transferible es:

> **Si una tarea tiene estructura interna importante, representar esa estructura en los ejemplos puede ayudar al modelo a aprender el tipo de transformación deseada.**

---

# 4. Chain-of-Thought es especialmente útil en problemas multietapa

Los resultados del paper muestran beneficios especialmente grandes en:

- problemas matemáticos;
- razonamiento aritmético;
- razonamiento de sentido común;
- manipulación simbólica;
- tareas donde deben realizarse varias operaciones consecutivas.

Una observación particularmente importante es que la mejora fue mucho menor en problemas simples de un solo paso.

## Principio operativo

No añadir deliberación compleja a todas las tareas.

```text
TAREA SIMPLE
→ respuesta directa

TAREA MULTIETAPA
→ descomposición / procedimiento intermedio
```

Esto evita gastar tokens y complejidad cuando no aportan valor.

---

# 5. El beneficio aumenta cuando el problema es realmente difícil

En los experimentos aritméticos, las ganancias fueron mayores en datasets difíciles y mucho menores —o incluso negativas— en algunos problemas muy sencillos.

Esto sugiere:

> **La cantidad de estructura de razonamiento debería ser proporcional a la dificultad de la tarea.**

Un prompt maestro puede implementar una política como:

```text
Si la tarea es trivial:
    responde directamente.

Si requiere múltiples dependencias:
    descompón el problema.

Si además es susceptible a errores:
    añade una fase de comprobación.
```

---

# 6. Few-shot + procedimiento puede enseñar una estrategia

Los ejemplos del paper no enseñan únicamente respuestas.

Enseñan patrones como:

```text
identificar cantidades
→ aplicar operación
→ actualizar estado
→ aplicar siguiente operación
→ producir respuesta
```

Esto convierte los ejemplos en una especie de **demostración de procedimiento**.

## Aplicación a prompts maestros

Un ejemplo debería utilizarse cuando queramos enseñar:

- cómo interpretar;
- qué pasos efectuar;
- qué evidencia considerar;
- cómo resolver casos ambiguos;
- qué estructura producir.

No basta con seleccionar ejemplos “bonitos”.

Los mejores ejemplos son aquellos que comunican una estrategia útil.

---

# 7. La descomposición aumenta el presupuesto de computación de la respuesta

Una de las propiedades destacadas por los autores es que los pasos intermedios permiten asignar más generación a problemas que necesitan más operaciones.

Conceptualmente:

```text
Problema sencillo
→ pocos pasos

Problema complejo
→ más pasos
```

Esto permite que la longitud de la solución se adapte a la complejidad.

## Idea generalizable

> **No obligar a todos los problemas a atravesar exactamente la misma profundidad de razonamiento.**

---

# 8. Los pasos intermedios pueden ayudar a localizar errores

Otra ventaja señalada por el paper es que una secuencia intermedia hace más fácil observar dónde se desvía una solución.

Ejemplo conceptual:

```text
Paso 1 ✓
Paso 2 ✓
Paso 3 ✗
Paso 4 depende del error anterior
```

Esto mejora:

- debugging;
- evaluación;
- análisis de errores;
- diseño de mejores ejemplos.

## Importante

El propio paper deja claro que una cadena generada no demuestra necesariamente cuáles fueron los mecanismos internos reales de la red.

Por tanto, debe interpretarse como una **secuencia de solución generada**, no como acceso garantizado a los procesos internos del modelo.

---

# 9. La cadena puede ser correcta y la respuesta incorrecta, o viceversa

Los autores observaron varios tipos de fallo.

Entre ellos:

```text
razonamiento casi correcto + error aritmético
razonamiento con un paso omitido
error semántico
error de mapeo de símbolos
alucinación
repetición
respuesta final difícil de parsear
```

También encontraron algunos casos en que el modelo llegaba accidentalmente a una respuesta correcta mediante pasos incorrectos.

## Consecuencia

> **Una explicación plausible no constituye una prueba de corrección.**

Por tanto:

```text
razonamiento textual
≠
verificación
```

Cuando sea posible deben añadirse:

- tests;
- cálculos;
- validadores;
- herramientas;
- fuentes externas.

---

# 10. La utilidad dependía fuertemente de la escala en los modelos estudiados

Uno de los resultados principales del paper es que el efecto aparecía de forma especialmente clara en modelos grandes.

En los experimentos originales, modelos pequeños no solo obtenían menos beneficio: en varios casos Chain-of-Thought empeoraba el rendimiento.

Los autores describen esta capacidad como **emergente con la escala**.

## Qué merece la pena conservar

No convertir el resultado histórico en una regla numérica eterna.

El principio duradero es:

> **Una técnica de prompting puede depender fuertemente de las capacidades del modelo utilizado.**

Por tanto:

```text
"Técnica X funcionó en el paper"
```

no significa:

```text
"Técnica X mejorará cualquier modelo actual."
```

Hay que evaluarla con el modelo real.

---

# 11. El prompt estándar puede subestimar la capacidad del modelo

Una conclusión interesante del paper es que evaluar un modelo únicamente mediante prompting directo puede ofrecer una imagen incompleta de sus capacidades.

En algunos problemas, el modelo parecía incapaz mediante:

```text
pregunta → respuesta
```

pero rendía mucho mejor cuando se le permitía producir pasos intermedios.

## Principio

> **La capacidad observada depende parcialmente de la interfaz de inferencia utilizada.**

Esto es importante para benchmarkear modelos.

Un benchmark debería distinguir:

- rendimiento directo;
- rendimiento con ejemplos;
- rendimiento con descomposición;
- rendimiento con herramientas;
- rendimiento con búsqueda.

---

# 12. Robustez frente al estilo de las demostraciones

El paper estudia cadenas escritas por diferentes anotadores y una versión más concisa.

Aunque existe variación, las distintas versiones superaron ampliamente al baseline estándar en los experimentos correspondientes.

## Lección

El efecto no parecía depender de una redacción mágica concreta.

Eso es importante:

> **La estructura del procedimiento puede importar más que copiar exactamente unas palabras determinadas.**

---

# 13. Robustez frente a diferentes ejemplos

Los autores también probaron conjuntos diferentes de ejemplos few-shot.

El beneficio se mantuvo.

Asimismo reportan robustez ante:

- orden distinto de ejemplos;
- cantidad diferente de ejemplos;
- diferentes modelos;
- diferentes anotadores.

## Aplicación

En vez de buscar un ejemplo “mágico”, buscar un conjunto de demostraciones que:

- representen bien la tarea;
- cubran las operaciones necesarias;
- sean correctas;
- no introduzcan patrones accidentales.

---

# 14. La concisión del procedimiento puede funcionar

El estudio incluye versiones más concisas de las cadenas y sigue observando beneficios.

Esto es útil porque significa que:

> **“Más razonamiento” no equivale necesariamente a “más palabras”.**

Un procedimiento puede ser:

```text
breve
+
estructurado
+
suficiente
```

y seguir cumpliendo su función.

Para prompts maestros esto sugiere evitar procedimientos artificialmente verbosos.

---

# 15. Chain-of-Thought no consiste únicamente en activar conocimiento

Los autores realizan ablations para estudiar si las mejoras proceden simplemente de producir más texto o activar conocimiento relevante.

Sus resultados apoyan que la **secuencia de razonamiento** aporta valor más allá de incluir información adicional de forma desordenada.

## Principio

La estructura importa.

```text
hechos relevantes sin conexión
```

no son necesariamente equivalentes a:

```text
hecho A
→ implica B
→ permite calcular C
→ respuesta
```

---

# 16. Generalización a secuencias más largas

En las tareas simbólicas, los ejemplos mostraban secuencias cortas y posteriormente se evaluaban secuencias más largas.

Con modelos suficientemente grandes, CoT ayudó a generalizar a longitudes no vistas en los ejemplos.

## Idea transferible

Una demostración puede enseñar **un algoritmo o patrón repetible**, no solamente memorizar el tamaño exacto del ejemplo.

Por ello los ejemplos deberían intentar transmitir:

```text
REGLA
```

en vez de:

```text
CASO CONCRETO
```

---

# 17. Aritmética, sentido común y simbolismo comparten una idea

Aunque las tareas son distintas, todas pueden representarse como transformaciones sucesivas.

Esto lleva a una idea más amplia:

> **CoT es útil cuando una tarea puede factorizarse en estados intermedios semánticamente significativos.**

No tiene por qué tratarse de matemáticas.

Puede aplicarse a:

```text
diagnóstico técnico
análisis documental
planificación
comparación
resolución de dependencias
investigación
```

siempre que exista una secuencia útil de subtareas.

---

# 18. No aplicar Chain-of-Thought por reflejo

El propio trabajo muestra que las mejoras dependen de:

- dificultad;
- modelo;
- tipo de tarea;
- capacidad de generar pasos coherentes.

Por tanto, un antipatrón sería:

```text
Añadir "piensa paso a paso" a absolutamente todo.
```

La alternativa correcta:

```text
¿La tarea requiere descomposición?
        ↓
      sí/no
```

Si no, evitar complejidad innecesaria.

---

# 19. El coste de producir procedimientos también importa

Los autores identifican como limitación que el método incrementa:

- longitud de la generación;
- coste;
- requisitos de modelos capaces;
- coste de preparar demostraciones si se necesitan muchas.

En el contexto de few-shot, producir algunas demostraciones manuales resulta manejable.

Pero escalar grandes cantidades de racionales para entrenamiento puede ser costoso.

---

# 20. No existe garantía de razonamiento correcto

Esta es una de las limitaciones más importantes explicitadas en el paper.

Un modelo puede producir una cadena:

- fluida;
- plausible;
- bien redactada;

y aun así equivocarse.

Por tanto:

> **CoT mejora la capacidad de resolver ciertos problemas, pero no convierte la generación en un procedimiento formalmente fiable.**

---

# 21. Regla práctica derivada: separar generación de verificación

Una arquitectura más robusta sería:

```text
PROBLEMA
↓
DESCOMPOSICIÓN
↓
SOLUCIÓN
↓
VERIFICACIÓN EXTERNA
↓
RESPUESTA
```

En matemáticas:

```text
modelo propone operaciones
→ calculadora verifica
```

En código:

```text
modelo propone implementación
→ tests verifican
```

En investigación:

```text
modelo propone conclusión
→ fuentes verifican
```

---

# 22. Qué enseñan los errores analizados

En una muestra de respuestas incorrectas, muchos fallos estaban cerca de la solución y consistían en errores locales.

Otros eran errores mucho más fundamentales de comprensión.

Esto sugiere distinguir:

```text
ERROR LOCAL
→ puede resolverse con verificación

ERROR DE REPRESENTACIÓN DEL PROBLEMA
→ requiere reinterpretación / mejor contexto
```

No todos los fallos se solucionan pidiendo “razona más”.

---

# 23. Aplicación a prompts maestros

Un prompt maestro puede incorporar esta idea sin convertir todas las respuestas en monólogos.

Por ejemplo:

```markdown
## Resolución de tareas complejas

Cuando la solicitud requiera varias dependencias:

1. identifica las subtareas necesarias;
2. resuélvelas en orden lógico;
3. conserva los resultados intermedios relevantes;
4. comprueba dependencias y restricciones;
5. entrega una respuesta final coherente.

Para tareas triviales, evita descomposición innecesaria.
```

La idea que queremos conservar es el **proceso**, no una frase ritual.

---

# 24. Ejemplos de procedimiento > descripción vaga

Si queremos enseñar al modelo una auditoría:

```text
NO:
"Analiza profundamente."
```

Podemos demostrar:

```text
HALLAZGO
→ EVIDENCIA
→ IMPACTO
→ CAUSA
→ CAMBIO PROPUESTO
```

Si queremos enseñar comparación:

```text
CRITERIO
→ opción A
→ opción B
→ diferencia
→ decisión
```

Esto aplica la intuición de CoT a tareas profesionales.

---

# 25. Un ejemplo debería contener solamente pasos útiles

Los pasos intermedios del ejemplo deberían:

- contribuir a la solución;
- reflejar el proceso deseado;
- evitar relleno;
- no introducir reglas accidentales.

Un ejemplo excesivamente largo puede enseñar verbosidad en lugar de razonamiento.

---

# 26. Principio de complejidad adaptativa

Una arquitectura inspirada en el paper:

```text
CLASIFICAR DIFICULTAD
        ↓
┌──────────────────────────────┐
│ simple → resolver directo    │
│ media  → descomponer         │
│ alta   → descomponer + check │
└──────────────────────────────┘
```

Esto es más eficiente que imponer el mismo tratamiento a todas las entradas.

---

# 27. Antipatrones

## Antipatrón 1 — “Piensa paso a paso” como magia

La técnica estudiada originalmente se basa en demostraciones de cadenas, no en la idea de que una frase específica resuelva cualquier problema.

## Antipatrón 2 — Razonar sobre tareas triviales

Puede añadir coste sin mejorar calidad.

## Antipatrón 3 — Confundir explicación con verdad

Una secuencia convincente puede contener errores.

## Antipatrón 4 — Copiar resultados de modelos antiguos como reglas universales

Los efectos dependen del modelo y deben reevaluarse.

## Antipatrón 5 — Ejemplos incorrectos

Una demostración defectuosa enseña un procedimiento defectuoso.

## Antipatrón 6 — Hacer el procedimiento innecesariamente largo

La utilidad procede de la estructura, no del número de palabras.

---

# 28. Qué merece la pena absorber permanentemente

1. **Las tareas multietapa pueden beneficiarse de estados intermedios explícitos.**
2. **Los ejemplos pueden enseñar procedimientos, no solo formatos.**
3. **El beneficio del razonamiento estructurado aumenta con la complejidad de la tarea.**
4. **No todas las tareas necesitan descomposición.**
5. **La capacidad observada depende de cómo se solicita la tarea.**
6. **Un procedimiento intermedio facilita debugging y análisis de errores.**
7. **Una explicación generada no es garantía de corrección.**
8. **La estructura del procedimiento importa más que una redacción mágica específica.**
9. **Los ejemplos deben transmitir reglas generalizables.**
10. **La eficacia de una técnica debe comprobarse en el modelo y tarea reales.**
11. **Verificación externa sigue siendo necesaria cuando la exactitud importa.**
12. **Más texto no implica mejor razonamiento.**

---

# 29. Checklist para aplicar estas ideas

- [ ] ¿La tarea requiere realmente varios pasos?
- [ ] ¿Existen estados intermedios útiles?
- [ ] ¿Los ejemplos enseñan el procedimiento correcto?
- [ ] ¿El procedimiento es suficientemente corto?
- [ ] ¿Los ejemplos cubren diferentes variantes?
- [ ] ¿Se ha comparado contra respuesta directa?
- [ ] ¿Se ha evaluado con el modelo actual?
- [ ] ¿Existe una forma externa de verificar el resultado?
- [ ] ¿Se distinguen errores locales de errores de comprensión?
- [ ] ¿La mejora justifica los tokens y la latencia adicionales?

---

# 30. Síntesis final

El valor histórico de este paper no está simplemente en popularizar la expresión *chain of thought*.

Su contribución más duradera es demostrar que:

> **La interfaz de inferencia puede transformar radicalmente la capacidad observada de un modelo.**

Cuando una tarea necesita una secuencia de operaciones, pedir únicamente la respuesta final puede ser una representación pobre del problema.

Mostrar o construir estados intermedios puede:

- facilitar descomposición;
- asignar más computación a problemas difíciles;
- mejorar generalización;
- permitir inspección;
- mejorar resultados en determinadas tareas.

Pero el paper también deja claro que:

```text
procedimiento generado
≠
garantía de verdad
```

Por eso, la versión más robusta de esta idea para sistemas modernos es:

> **descomponer cuando aporte valor, mantener el procedimiento compacto y verificar externamente aquello que pueda verificarse.**
