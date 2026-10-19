# Principios clave de *Prompt Engineering for Generative AI*

**Título original:** *Prompt Engineering for Generative AI: Future-Proof Inputs for Reliable AI Outputs at Scale*  
**Autores:** James Phoenix y Mike Taylor  
**Editorial:** O’Reilly Media  
**Edición:** Primera edición, 2024  
**Propósito de este documento:** condensar las ideas de mayor valor práctico y duradero del libro para diseñar prompts, workflows y sistemas de IA más fiables, evitando convertir detalles coyunturales de herramientas de 2024 en reglas universales.

---

# 1. Tesis central del libro

El libro parte de una idea sencilla:

> La calidad de una salida generativa depende de la calidad de la información, dirección, ejemplos, estructura y mecanismos de evaluación que rodean a la solicitud.

La ingeniería de prompts no se presenta como una colección de “palabras mágicas”, sino como una disciplina para obtener resultados:

- más útiles;
- más consistentes;
- más fáciles de validar;
- más baratos;
- más rápidos;
- más integrables en software.

El libro insiste en que los trucos concretos envejecen rápido, mientras que determinados principios de ingeniería sobreviven a los cambios de modelo.

Su marco principal son los **Five Principles of Prompting**:

```text
1. Give Direction
2. Specify Format
3. Provide Examples
4. Evaluate Quality
5. Divide Labor
```

La idea más importante no es memorizar estas cinco etiquetas, sino entender que corresponden a cinco clases de fallos muy comunes:

```text
Resultado demasiado genérico
→ falta dirección

Resultado difícil de utilizar
→ falta especificar formato

Modelo no entiende exactamente qué consideramos bueno
→ faltan ejemplos

No sabemos si el prompt realmente funciona
→ falta evaluación

Una sola llamada intenta resolver demasiado
→ falta división del trabajo
```

---

# 2. Principio maestro: un prompt no es prosa decorativa

Uno de los aprendizajes más transferibles del libro es dejar de evaluar un prompt por cómo “suena”.

Un prompt puede parecer:

- sofisticado;
- detallado;
- profesional;
- largo;

y aun así producir resultados peores.

La pregunta correcta es:

```text
¿Este prompt aumenta la probabilidad de obtener el comportamiento que necesito?
```

Por tanto:

```text
CALIDAD DEL PROMPT
≠
LONGITUD
≠
COMPLEJIDAD
≠
ELEGANCIA LINGÜÍSTICA
```

La calidad debe observarse en el comportamiento del sistema.

---

# 3. Los prompts deben optimizarse para calidad, coste y fiabilidad

El libro recuerda que las llamadas a modelos tienen recursos limitados:

- tokens;
- coste;
- latencia;
- context window;
- número de llamadas;
- variabilidad.

Por eso, un prompt profesional no debe optimizar exclusivamente:

```text
"mejor respuesta posible"
```

sino algo parecido a:

```text
utilidad
×
fiabilidad
÷
(coste + latencia + complejidad)
```

No es una fórmula matemática literal, sino una forma útil de pensar.

Dos prompts con calidad similar pueden ser muy distintos en producción si uno:

- consume la mitad de tokens;
- es más fácil de mantener;
- falla menos al parsearse;
- necesita menos llamadas.

---

# 4. Primer principio: Give Direction

## 4.1 Qué significa realmente

El primer principio consiste en reducir la ambigüedad acerca de **qué tipo de respuesta queremos**.

La dirección puede incluir:

- objetivo;
- contexto;
- estilo;
- audiencia;
- criterios;
- restricciones;
- prioridades;
- perspectiva;
- rol.

Una solicitud como:

```text
Escribe nombres para este producto.
```

deja una distribución enorme de outputs posibles.

Una solicitud mejor define:

```text
para quién
qué atributos buscamos
qué queremos evitar
qué criterios distinguen una buena respuesta
qué tono o estilo es adecuado
```

---

# 5. Contexto útil > adjetivos vagos

El libro propone imaginar qué información necesitaría una persona competente para resolver la misma tarea.

Esto genera una regla robusta:

> Si un humano necesitaría contexto para tomar una decisión de calidad, probablemente el modelo también se beneficie de ese contexto.

Ejemplo conceptual:

```text
MALO:
"Recomiéndame una base de datos."

MEJOR:
"Recomiéndame una base de datos teniendo en cuenta:
- estructura de datos;
- volumen;
- consistencia;
- patrón de consultas;
- concurrencia;
- presupuesto;
- experiencia del equipo."
```

El segundo prompt no es mejor porque sea más largo.

Es mejor porque introduce **variables decisorias**.

---

# 6. Ask for Context: no obligar al modelo a adivinar

Una de las tácticas más útiles del libro consiste en permitir al modelo reconocer que la información disponible es insuficiente.

El flujo puede ser:

```text
SOLICITUD
↓
¿HAY CONTEXTO SUFICIENTE?
├─ sí → responder
└─ no → pedir la información decisiva
        ↓
      responder después
```

Esto es especialmente útil en:

- arquitectura de software;
- recomendaciones;
- planificación;
- diagnóstico;
- estrategia;
- decisiones empresariales.

## Regla práctica

```markdown
Si falta información que pueda cambiar materialmente la respuesta,
no inventes una suposición silenciosa.
Identifica únicamente los datos decisivos que faltan.
```

---

# 7. No preguntar por contexto innecesario

El principio anterior también puede abusarse.

Un sistema que siempre responde con diez preguntas provoca fricción.

Por tanto:

```text
¿puedo responder correctamente sin preguntar?
├─ sí → responde
└─ no → pregunta
```

La pregunta debe estar justificada por **impacto sobre la decisión**, no por deseo de obtener todo el contexto imaginable.

---

# 8. Priorizar cuando las instrucciones chocan

El libro muestra que demasiada dirección puede crear combinaciones incompatibles.

Esto ocurre en texto y, de manera muy visible, en generación de imágenes.

Ejemplo conceptual:

```text
"minimalista"
+
"extremadamente recargado"
+
"documental"
+
"fantasía surrealista"
+
"corporativo sobrio"
```

El problema ya no es falta de detalle.

Es conflicto de objetivos.

## Principio

> Más restricciones solo ayudan mientras sean compatibles.

Un prompt maestro debería establecer prioridades:

```text
PRIORIDAD 1 → exactitud
PRIORIDAD 2 → cumplimiento del formato
PRIORIDAD 3 → concisión
PRIORIDAD 4 → estilo
```

Cuando existe conflicto, las prioridades superiores ganan.

---

# 9. Role prompting: útil, pero no mágico

El libro dedica atención a los roles:

```text
"Actúa como..."
```

Los roles pueden orientar:

- tono;
- nivel técnico;
- estructura;
- perspectiva;
- tipo de análisis.

Pero tienen límites.

Un rol no convierte al modelo en una fuente verificable de experiencia real.

```text
"Actúa como experto en seguridad"
```

no significa:

```text
"todo lo que diga será correcto"
```

## Uso correcto

Un rol sirve para definir **marco de trabajo**.

Ejemplo:

```text
Rol: revisor técnico de backend.
Objetivo: detectar problemas reproducibles.
Criterios: seguridad, corrección, rendimiento y mantenibilidad.
```

Eso es mejor que usar el rol como sustituto de especificaciones concretas.

---

# 10. Riesgos del role prompting

El libro señala dos riesgos principales:

- estereotipos o sesgos asociados al personaje/rol;
- deriva del rol en conversaciones largas.

A esto se añade una conclusión práctica:

> El rol debe reforzar el comportamiento deseado, pero las reglas importantes deben expresarse directamente.

No confiar en:

```text
"Eres un experto cuidadoso."
```

cuando realmente necesitamos:

```text
"No afirmes que una función existe si no aparece en el código."
```

---

# 11. Segundo principio: Specify Format

## 11.1 La salida también forma parte de la especificación

Una respuesta puede ser semánticamente correcta y aun así inutilizable.

En software, esto es crítico.

Ejemplo:

```text
esperábamos JSON
→ recibimos una explicación + JSON + comentario final
→ parser falla
```

Por eso el formato no es un detalle cosmético.

Es parte de la interfaz.

---

# 12. Separar contenido y contrato de salida

Conviene definir dos cosas:

```text
QUÉ debe contener
```

y:

```text
CÓMO debe representarse
```

Ejemplo:

```markdown
Contenido:
- título;
- severidad;
- evidencia;
- recomendación.

Formato:
JSON válido con exactamente esas cuatro claves.
```

Esto reduce ambigüedad.

---

# 13. Structured output mejora integración

El libro trabaja con:

- listas;
- estructuras jerárquicas;
- JSON;
- YAML;
- esquemas;
- parsers.

La idea permanente es:

> Cuando otra pieza de software consumirá el resultado, usar una estructura formal suele ser preferible a depender de texto libre.

Ejemplo:

```json
{
  "finding": "...",
  "severity": "high",
  "confidence": 0.91
}
```

es más fácil de:

- validar;
- almacenar;
- filtrar;
- comparar;
- pasar a otra etapa.

---

# 14. Pedir formato no equivale a garantizar formato

El libro advierte expresamente que incluso si pedimos JSON u otra estructura, el modelo puede producir una salida inválida.

Por tanto:

```text
PROMPT
↓
OUTPUT
↓
PARSER / SCHEMA VALIDATION
↓
¿VÁLIDO?
├─ sí → continuar
└─ no → reparar / reintentar / fallar de forma controlada
```

## Principio de producción

> Nunca confíes únicamente en una instrucción textual cuando la estructura puede validarse programáticamente.

---

# 15. Output parsers y schemas pertenecen a la arquitectura

El libro muestra parsers para:

- listas;
- fechas;
- enums;
- JSON/Pydantic;
- XML;
- estructuras compuestas;
- retries;
- autocorrección.

La lección no es “usar LangChain”.

La lección es:

> La validación estructural debe ser una capa del sistema, independiente del texto del prompt.

---

# 16. Function calling: el schema también es prompting

Cuando un modelo puede invocar funciones, la descripción de la herramienta y su schema actúan como parte del contexto de decisión.

El libro destaca que deben definirse claramente:

- nombre;
- descripción;
- parámetros;
- tipos;
- campos requeridos.

Ejemplo conceptual:

```text
search_customer
Descripción:
Busca un cliente por email.

Input:
{
  "email": string
}
```

es mejor que:

```text
tool_1
```

---

# 17. Validar argumentos antes de ejecutar herramientas

Otra idea de producción especialmente importante:

```text
LLM propone argumentos
↓
SCHEMA VALIDATOR
↓
VALIDACIÓN SEMÁNTICA / PERMISOS
↓
EJECUCIÓN
```

No deberíamos interpretar:

```text
"el modelo devolvió JSON"
```

como:

```text
"la acción es válida y segura"
```

La estructura correcta es necesaria, pero no suficiente.

---

# 18. Tercer principio: Provide Examples

Los ejemplos permiten enseñar cosas difíciles de describir con reglas exhaustivas.

Un ejemplo puede comunicar simultáneamente:

- formato;
- tono;
- nivel de detalle;
- relación input/output;
- criterios implícitos.

Por eso pocos ejemplos buenos pueden cambiar mucho el resultado.

---

# 19. Zero-shot, one-shot y few-shot

El libro usa la distinción clásica:

```text
zero-shot  → sin ejemplos
one-shot   → un ejemplo
few-shot   → varios ejemplos
```

El principio importante no es que “más ejemplos siempre sea mejor”.

Es:

> Utiliza ejemplos cuando aporten información que las instrucciones por sí solas no comunican con suficiente precisión.

---

# 20. Un ejemplo debe demostrar éxito, no simplemente rellenar contexto

Los ejemplos deberían ser:

- correctos;
- representativos;
- variados;
- consistentes con el formato;
- relevantes para casos reales.

Ejemplos pobres pueden enseñar:

- sesgos accidentales;
- formatos indeseados;
- respuestas demasiado específicas;
- errores.

---

# 21. Diversidad de ejemplos

Un conjunto útil debería cubrir más de un patrón.

Ejemplo:

```text
caso normal
caso límite
caso ambiguo
caso con ausencia de información
```

Esto enseña comportamiento más generalizable que repetir cinco ejemplos prácticamente idénticos.

---

# 22. Los ejemplos consumen presupuesto de contexto

El libro enfatiza el trade-off:

```text
más ejemplos
→ más contexto usado
→ menos espacio disponible
→ más coste
```

Por tanto la selección de ejemplos puede ser dinámica.

Una arquitectura avanzada:

```text
ENTRADA
↓
seleccionar ejemplos similares/relevantes
↓
construir prompt
↓
inferir
```

---

# 23. Few-shot también puede producir sobreajuste

Los autores advierten que un modelo puede apegarse excesivamente a los ejemplos.

Esto es especialmente problemático si:

- los ejemplos son muy estrechos;
- el nuevo caso difiere;
- el ejemplo mezcla contenido y formato de manera ambigua.

## Solución conceptual

Definir qué debe aprender de los ejemplos:

```text
"Usa estos ejemplos para comprender el formato y criterios,
no para copiar detalles específicos."
```

---

# 24. Prompts como artefactos versionables

El libro recomienda almacenar prompts como recursos independientes, en vez de incrustarlos indiscriminadamente dentro del código.

Esto favorece:

- versionado;
- colaboración;
- testeo;
- reutilización;
- revisión.

## Principio

```text
prompt_v12
modelo
dataset_eval
score
fecha
```

deberían poder asociarse.

Un prompt importante es un artefacto de software.

---

# 25. Cuarto principio: Evaluate Quality

Este es probablemente el principio más importante de todo el libro.

Los autores distinguen entre trabajar por impresión y trabajar con feedback.

Llaman **blind prompting** a ir añadiendo instrucciones sin un sistema de evaluación que permita saber si realmente ayudan.

---

# 26. No optimizar a ojo

Sin evaluación ocurre esto:

```text
v1
→ "parece mejor"

v2
→ "parece más profesional"

v3
→ "tiene más reglas"

v4
→ nadie sabe si realmente mejoró
```

Con evaluación:

```text
v1 → 72%
v2 → 79%
v3 → 75%
```

Ahora existe señal.

---

# 27. Evaluar varias ejecuciones, no una sola

Los modelos son no deterministas.

Por tanto comparar:

```text
Prompt A → una respuesta
Prompt B → una respuesta
```

puede ser engañoso.

Una comparación más robusta:

```text
Prompt A × N
Prompt B × N
↓
evaluación
↓
promedio + fallos + varianza
```

---

# 28. Blind evaluation reduce sesgo

El libro recomienda ocultar qué prompt produjo cada respuesta antes de calificarlas.

Proceso:

```text
generar outputs
→ mezclar
→ evaluar sin conocer la variante
→ agrupar resultados
```

Esto reduce el sesgo de preferir la versión que uno mismo acaba de escribir.

---

# 29. Pequeños experimentos ya revelan mucho

No siempre hace falta construir un benchmark enorme.

Los autores muestran que unos pocos intentos pueden revelar:

- desviaciones;
- diferencias de formato;
- edge cases;
- instrucciones inútiles.

## Principio

> Es mejor una evaluación pequeña pero real que ninguna evaluación.

---

# 30. A/B testing de prompts

Un patrón básico:

```text
PROMPT A
vs.
PROMPT B
↓
mismo conjunto de casos
↓
métrica común
↓
comparación
```

Cambiar pocas variables por experimento mejora la atribución causal.

Por ejemplo:

```text
A = sin ejemplos
B = mismos contenidos + ejemplos
```

permite estimar el valor de esos ejemplos.

---

# 31. No medir solo calidad subjetiva

El libro propone múltiples dimensiones.

Entre ellas:

- coste;
- latencia;
- número de llamadas;
- performance;
- clasificación;
- razonamiento;
- alucinaciones;
- seguridad;
- refusals;
- ataques adversariales;
- similitud.

Podemos generalizar a:

```text
quality
format validity
groundedness
coverage
latency
cost
tool success
retrieval precision
failure rate
```

---

# 32. Ground truth > juez subjetivo cuando existe

Si existe una respuesta verificable:

```text
resultado matemático
test de código
schema
clasificación etiquetada
consulta de base de datos
```

deberíamos preferirla a una evaluación puramente subjetiva.

Ejemplo:

```text
¿el JSON parsea?
→ parser

¿el código pasa tests?
→ test suite

¿el número es correcto?
→ cálculo
```

---

# 33. LLM-as-a-judge puede servir, pero también necesita evaluación

El libro analiza el uso de modelos potentes para evaluar outputs de otros modelos.

La idea puede ahorrar:

- tiempo;
- coste humano;
- latencia de iteración.

Pero el evaluador también puede tener:

- falsos positivos;
- falsos negativos;
- sesgos;
- inconsistencia.

Por tanto:

```text
EVALUADOR
↓
también necesita benchmark
```

---

# 34. Jerarquía útil de evaluadores

De mayor determinismo a mayor flexibilidad:

```text
1. regla exacta / test
2. parser / schema
3. cálculo
4. comparación contra ground truth
5. métrica estadística
6. modelo evaluador
7. revisión humana
```

No siempre el punto 1 es aplicable.

La idea es utilizar la señal más fiable y económica disponible.

---

# 35. Human feedback sigue siendo extremadamente valioso

El libro trata el feedback de usuarios como una de las fuentes más importantes para descubrir edge cases.

Un loop saludable:

```text
usuarios
↓
feedback
↓
casos fallidos
↓
dataset de evaluación
↓
nueva versión
↓
regression test
```

Así se crea un **data flywheel**.

---

# 36. Los fallos reales deben convertirse en tests

Una práctica derivada muy importante:

```text
FALLO EN PRODUCCIÓN
↓
reproducir
↓
añadir a regression suite
↓
arreglar
↓
evitar reintroducción
```

Sin esto, el sistema puede mejorar un caso y romper otro.

---

# 37. La evaluación también encuentra texto inútil en el prompt

Los autores destacan que durante la iteración podemos descubrir instrucciones que:

- no cambian nada;
- empeoran respuestas;
- aumentan coste;
- aumentan latencia.

Por tanto:

> Optimizar un prompt también significa eliminar.

---

# 38. Prompt ablation

Un método profesional:

```text
Prompt completo
↓
eliminar bloque A
↓
evaluar

eliminar bloque B
↓
evaluar

acortar ejemplos
↓
evaluar
```

Esto permite estimar qué partes aportan valor.

---

# 39. Minimal Effective Prompt

El objetivo no debería ser:

```text
el prompt más completo imaginable
```

sino:

```text
el prompt mínimo que cumple de forma fiable los requisitos
```

A esto podemos llamarlo **Minimal Effective Prompt**.

Beneficios:

- menos tokens;
- menos conflicto;
- menor mantenimiento;
- menor latencia;
- más claridad.

---

# 40. Quinto principio: Divide Labor

El libro observa que los prompts grandes pueden intentar resolver demasiadas cosas simultáneamente.

Problema:

```text
investigar
+
analizar
+
escribir
+
validar
+
puntuar
+
formatear
```

en una única llamada.

Esto reduce observabilidad.

---

# 41. Task decomposition

Alternativa:

```text
1. recopilar información
2. estructurarla
3. generar candidatos
4. evaluar
5. seleccionar
6. formatear
```

Cada etapa puede tener:

- input claro;
- output claro;
- criterio de éxito;
- validación.

---

# 42. Chaining mejora observabilidad

Si falla una llamada monolítica:

```text
¿falló investigación?
¿interpretación?
¿redacción?
¿formato?
```

Es difícil saberlo.

Con una cadena:

```text
Etapa 1 ✓
Etapa 2 ✓
Etapa 3 ✗
```

el debugging es mucho más sencillo.

---

# 43. No encadenar por deporte

Más pasos también implican:

- mayor coste;
- más latencia;
- más puntos de fallo;
- más estado;
- más complejidad.

La división del trabajo debe existir cuando cada etapa:

- simplifica una subtarea;
- permite validar;
- utiliza una herramienta diferente;
- reduce ambigüedad;
- mejora calidad de forma medible.

---

# 44. Least-to-Most

El libro presenta **Least to Most** como una cadena progresiva de prompts.

Ejemplo conceptual:

```text
arquitectura
↓
componente A
↓
componente B
↓
tests
```

Cada respuesta sirve como contexto para la siguiente.

Esto es útil para:

- programación;
- investigación;
- planificación;
- generación detallada.

---

# 45. Error propagation en cadenas

El propio libro destaca el problema:

```text
Paso 1 incorrecto
↓
Paso 2 usa Paso 1
↓
Paso 3 usa Paso 2
↓
error amplificado
```

## Regla

> En una cadena, la salida de una etapa crítica debe validarse antes de convertirse en verdad para la siguiente.

---

# 46. Estado explícito > confiar en chat history indefinidamente

Las cadenas largas pueden olvidar:

- objetivo original;
- decisiones anteriores;
- restricciones.

Por tanto, conviene mantener estado explícito.

Ejemplo:

```json
{
  "objective": "...",
  "constraints": [],
  "completed": [],
  "pending": [],
  "verified_facts": []
}
```

Esto es más controlable que depender de una conversación cada vez más larga.

---

# 47. Self-evaluation como etapa separada

El libro utiliza segundos pasos para criticar outputs previos.

Patrón:

```text
GENERAR
↓
CRITICAR
↓
REVISAR
```

Esto puede mejorar:

- cobertura;
- formato;
- coherencia;
- claridad.

Pero hay una limitación importante:

> El mismo modelo puede conservar el mismo error.

Por tanto:

```text
self-critique
≠
verificación independiente
```

---

# 48. Razonamiento y “thinking time”

El libro recoge la idea de dar más espacio al modelo para derivar soluciones antes de emitir un veredicto.

La lección durable no es exponer necesariamente un monólogo interno.

La lección es:

> Los problemas complejos pueden beneficiarse de una fase deliberativa anterior a la respuesta final.

En sistemas modernos puede implementarse mediante:

- descomposición;
- llamadas intermedias;
- planificación;
- herramientas;
- búsqueda;
- validadores.

---

# 49. Hallucination control mediante referencia

Una de las tácticas más fuertes del libro:

```text
FUENTE
+
PREGUNTA
+
REGLA DE ABSTENCIÓN
```

Ejemplo conceptual:

```text
Responde solamente con información presente en la fuente.
Si la fuente no contiene la respuesta, devuelve:
"Información insuficiente".
```

Esto es mejor que pedir:

```text
"no alucines"
```

---

# 50. Abstenerse es una capacidad

Un sistema fiable necesita poder decir:

```text
no tengo evidencia suficiente
```

En muchos dominios esto es mejor que completar huecos plausiblemente.

## Diseño

```text
¿evidencia suficiente?
├─ sí → responder
└─ no → abstenerse / buscar / preguntar
```

---

# 51. Citas como mecanismo de trazabilidad

El libro también propone devolver evidencia junto con respuestas.

Esto permite:

- inspección humana;
- matching contra fuente;
- debugging;
- groundedness evaluation.

La versión abstracta:

```text
CLAIM
→ SOURCE SPAN
```

---

# 52. RAG como extensión natural de Give Direction + Provide Examples

Cuando la información relevante no cabe estáticamente en el prompt:

```text
QUERY
↓
RETRIEVAL
↓
CONTEXT RELEVANTE
↓
LLM
```

Esto es Retrieval-Augmented Generation.

El libro dedica un capítulo completo a:

- embeddings;
- FAISS;
- Pinecone;
- chunking;
- vector search;
- retrievers.

---

# 53. RAG no debe utilizarse automáticamente

Un punto muy útil del libro es que vector search añade:

- coste;
- latencia;
- infraestructura.

A veces basta con:

- contexto estático;
- ejemplos;
- keyword search;
- una base de datos estructurada.

## Regla

> Retrieval debe resolver un problema real, no añadirse por moda.

---

# 54. Retrieval y generación son subsistemas distintos

Aunque el libro no lo formaliza como una tesis única, sus ejemplos dejan clara esta separación:

```text
RETRIEVAL
→ ¿trajo información correcta?

GENERATION
→ ¿usó correctamente esa información?
```

Por tanto deben evaluarse por separado.

---

# 55. Chunking es una decisión de información

Dividir documentos afecta lo que puede recuperarse.

Un chunk demasiado pequeño:

- pierde contexto.

Un chunk demasiado grande:

- introduce ruido;
- consume tokens.

El solapamiento puede preservar continuidad, pero también aumenta volumen.

## Principio

> Chunking debe optimizarse sobre la unidad semántica necesaria para responder.

---

# 56. Estrategias de documentos

El libro resume cuatro patrones principales.

## Stuff

```text
todos los documentos
→ una llamada
```

Bueno cuando caben y son pocos.

## Refine

```text
doc 1 → borrador
doc 2 + borrador → revisión
doc 3 + revisión → ...
```

Útil para refinamiento progresivo, pero más lento.

## Map-Reduce

```text
doc A → resultado A
doc B → resultado B
doc C → resultado C
↓
combinar
```

Escala mejor, aunque añade complejidad y puede perder orden global.

## Map-Rerank

```text
cada documento → respuesta + score
↓
elegir mejor
```

Depende de que el scoring sea bueno.

---

# 57. Diferentes retrievers resuelven problemas distintos

El libro menciona:

- multi-query retrieval;
- contextual compression;
- ensemble retrieval;
- parent document retrieval;
- time-weighted retrieval;
- self-querying con metadata.

Principio:

> “Buscar documentos” no es una sola operación.

Puede requerir:

```text
semantic similarity
metadata filters
freshness
diversity
compression
hybrid search
```

---

# 58. Self-querying + metadata

Si los documentos contienen atributos estructurados:

```text
autor
fecha
tipo
idioma
categoría
```

no todo debería resolverse mediante similitud vectorial.

Una consulta puede convertirse en:

```text
semantic_query
+
metadata_filter
```

Esto mejora precisión cuando el usuario expresa restricciones explícitas.

---

# 59. Multi-query retrieval para ampliar cobertura

Un solo query puede representar mal la intención.

El patrón:

```text
consulta original
↓
varias reformulaciones
↓
retrieval
↓
fusionar resultados
```

puede aumentar recall.

Trade-off:

- más coste;
- duplicados;
- contradicciones.

---

# 60. Contextual compression

Otra idea:

```text
documento recuperado
↓
eliminar partes irrelevantes para la consulta
↓
pasar contexto condensado al modelo
```

Beneficio:

- menos tokens;
- más densidad informativa.

Riesgo:

- el compresor puede descartar algo importante.

---

# 61. Retrieval también debe demostrar ROI

El libro recomienda comprobar si la mejora de contexto justifica:

- prompts más largos;
- embeddings;
- almacenamiento;
- latencia.

Esto conecta con la tesis general:

```text
ARQUITECTURA
→ se valida empíricamente
```

---

# 62. Agentes: del prompt al ciclo de decisión

El capítulo de agentes cambia el modelo mental:

```text
LLM → texto
```

a:

```text
LLM
→ decide
→ usa herramienta
→ recibe observación
→ actualiza
→ decide de nuevo
```

---

# 63. Componentes de un agente

El libro organiza un agente alrededor de:

- inputs;
- objetivo/reward;
- acciones disponibles.

Para LLMs añade:

- tools;
- memory;
- retrieval;
- planning/execution strategy.

Una forma útil de representarlo:

```text
OBJECTIVE
+
STATE
+
OBSERVATIONS
+
ACTION SPACE
+
POLICY
```

---

# 64. ReAct

El libro explica el patrón:

```text
OBSERVE
→ INTERPRET
→ ACT
→ OBSERVE
→ ...
```

y la necesidad de detenerse cuando:

- se encuentra una solución;
- se alcanza un máximo de iteraciones.

Esto introduce una regla de producción imprescindible:

> Todo loop de agente necesita una condición de parada.

---

# 65. Nunca inventar resultados de una herramienta

El libro especifica que el agente debe emitir la acción y esperar el resultado real.

Correcto:

```text
Action: search(...)
↓
tool devuelve X
↓
modelo utiliza X
```

Incorrecto:

```text
"Voy a buscar..."
↓
modelo imagina lo que habría devuelto
```

---

# 66. Tool descriptions influyen en tool selection

Nombre y descripción deben ser:

- distintos;
- expresivos;
- específicos.

Ejemplo:

```text
get_invoice_by_id
```

es mejor que:

```text
lookup
```

si el propósito real es obtener facturas.

## Principio

> Las herramientas también necesitan diseño semántico.

---

# 67. Tools con inputs estructurados

En herramientas complejas, el modelo debe producir argumentos que pasan por validación.

```text
tool choice
↓
structured args
↓
schema validation
↓
business validation
↓
permission check
↓
execute
```

Esto transforma acciones probabilísticas en interfaces más controladas.

---

# 68. Function calling vs. agentes iterativos

El libro plantea una distinción práctica:

## Acción definida y acotada

```text
extraer datos
buscar algo
llamar una API concreta
```

→ function/tool calling suele ser más sencillo y estable.

## Objetivo multietapa

```text
hacer A
luego usar el resultado en B
decidir C según lo observado
```

→ un loop tipo ReAct puede tener sentido.

## Regla

> No uses un agente autónomo cuando una función estructurada resuelve la tarea.

---

# 69. Separar planificación y ejecución

El libro presenta plan-and-execute:

```text
PLANNER
→ lista/prioriza tareas

EXECUTOR
→ ejecuta tareas
```

Esto permite usar:

- modelos distintos;
- permisos distintos;
- métricas distintas.

También mejora depuración.

---

# 70. Tree of Thoughts como búsqueda

El libro introduce ToT para problemas donde:

- las decisiones tempranas importan;
- hay varias rutas plausibles;
- se necesita backtracking.

La enseñanza durable:

```text
generar varias opciones
→ evaluar
→ explorar las prometedoras
→ retroceder si es necesario
```

No debe usarse en tareas simples debido a su coste.

---

# 71. Memory

El libro distingue varios mecanismos de memoria conversacional.

La idea generalizable:

```text
toda la conversación
```

no siempre es la mejor memoria.

Puede utilizarse:

- ventana reciente;
- resumen;
- límite por tokens;
- retrieval de memoria relevante.

La elección depende de qué información necesita conservarse.

---

# 72. Memoria no es un vertedero de contexto

Si guardamos todo indefinidamente:

- aumenta coste;
- aumenta ruido;
- pueden persistir errores;
- disminuye relevancia.

## Principio

> Memory debe seleccionar estado útil, no simplemente acumular historial.

---

# 73. Observability en agentes

El libro dedica espacio a callbacks y logging.

Eventos importantes:

- inicio/fin de modelo;
- inicio/fin de chain;
- tool call;
- tool result;
- errores;
- finalización del agente.

En producción deberíamos poder reconstruir:

```text
qué entrada recibió
qué prompt se construyó
qué tool eligió
qué argumentos usó
qué devolvió la herramienta
cuánto costó
cuánto tardó
qué versión se ejecutó
```

---

# 74. Token accounting es observabilidad

El libro muestra seguimiento de:

- requests;
- coste;
- prompt tokens;
- completion tokens;
- total tokens.

Esto permite detectar:

- prompts inflados;
- loops;
- respuestas demasiado largas;
- cambios de coste tras una versión.

---

# 75. Coste y latencia forman parte de calidad

Si una solución:

- tarda 30 segundos;
- cuesta diez veces más;

puede ser peor para producción aunque su respuesta sea ligeramente superior.

Por tanto:

```text
quality benchmark
+
cost benchmark
+
latency benchmark
```

deberían convivir.

---

# 76. Imagen: los mismos principios, distinta interfaz

Los capítulos 7–9 trasladan los cinco principios a modelos visuales.

Aunque muchas herramientas concretas del libro son de 2024, las ideas generales siguen siendo útiles.

---

# 77. Give Direction en imágenes

Una imagen se controla mediante variables como:

- sujeto;
- entorno;
- composición;
- iluminación;
- cámara;
- materiales;
- época;
- estética;
- nivel de detalle.

Pero, igual que con texto:

> Demasiadas instrucciones conflictivas introducen ruido.

---

# 78. Format modifiers

En imagen, “formato” puede significar:

- fotografía;
- ilustración;
- póster;
- pintura;
- aspect ratio;
- tipo de plano.

Esto refuerza una idea:

> El formato es parte del contrato de salida, incluso en medios no textuales.

---

# 79. Negative prompts y restricciones

Indicar lo que no queremos puede ayudar cuando el modelo tiende persistentemente hacia ciertos elementos.

Pero la regla general es:

```text
positiva y clara dirección primero
+
restricciones negativas cuando resuelven un fallo observado
```

No llenar el prompt de prohibiciones preventivas sin evidencia.

---

# 80. Weighted terms y prioridades

Algunos sistemas permiten ponderar conceptos.

Aunque la sintaxis cambia entre herramientas, el principio permanece:

> Cuando varias instrucciones compiten, el sistema necesita saber cuáles son más importantes.

En prompts de texto esto puede expresarse semánticamente mediante prioridades.

---

# 81. Prompt analysis y pruning

Una de las ideas visuales más transferibles del libro:

> Cada palabra adicional puede perturbar la salida.

Los autores muestran herramientas que intentan detectar palabras con poca influencia.

La abstracción para cualquier prompt es:

```text
¿esta instrucción aporta?
├─ sí → conservar
└─ no → eliminar
```

---

# 82. Meme unbundling: describir propiedades en vez de nombres

El libro propone descomponer un estilo en rasgos:

```text
paleta
composición
atmósfera
textura
formas
iluminación
```

en lugar de depender únicamente del nombre de un artista.

Ventajas:

- mayor control;
- mayor originalidad;
- posibilidad de mezclar atributos;
- menor dependencia de una etiqueta.

Esto es aplicable también al texto:

```text
"escribe como X"
```

puede sustituirse por:

```text
frases cortas
argumentación analítica
tono conversacional
ejemplos concretos
estructura con subtítulos
```

---

# 83. Style unbundling como patrón general

Podemos formalizar:

```text
REFERENCIA
↓
EXTRAER ATRIBUTOS
↓
REPRESENTACIÓN DE ESTILO
↓
GENERAR CONTENIDO NUEVO
```

Esto es más controlable que imitación nominal.

---

# 84. Meme mapping: aprender de patrones exitosos

El libro recomienda observar prompts que producen buenos resultados y extraer patrones recurrentes.

En términos profesionales:

```text
coleccionar ejemplos
→ etiquetar
→ detectar patrones
→ formular hipótesis
→ probarlas
```

Esto es investigación empírica, no copiar ciegamente.

---

# 85. Herramientas de control > más palabras

En imagen, técnicas como:

- img2img;
- inpainting;
- masks;
- ControlNet;
- fine-tuning;

pueden proporcionar control que un prompt textual no consigue.

La lección general es muy importante:

> No intentes solucionar con lenguaje un problema que tiene una capa de control mejor.

---

# 86. Elegir la capa correcta

```text
problema de formato
→ schema/parser

problema de factualidad
→ retrieval/fuente

problema de cálculo
→ código

problema de acción
→ tool/API

problema de composición visual
→ conditioning/control

problema de estilo persistente
→ ejemplos/fine-tuning

problema de calidad desconocida
→ evals
```

Este es uno de los aprendizajes más importantes que podemos derivar del libro como sistema completo.

---

# 87. Divide Labor también existe en generación visual

El libro utiliza SDXL base + refiner como ejemplo:

```text
modelo base
→ composición global

refiner
→ detalle fino
```

La idea abstracta:

> Las etapas pueden especializarse.

No necesitamos que una sola llamada resuelva simultáneamente todos los niveles de la tarea.

---

# 88. Building AI-Powered Applications: integrar los principios

El capítulo final construye un sistema end-to-end.

El valor del capítulo no está en la app concreta, sino en mostrar que un producto de IA real mezcla:

- research;
- contexto;
- retrieval;
- prompts;
- memoria;
- schemas;
- generación;
- evaluación;
- imágenes;
- feedback.

Esto confirma la tesis:

> Prompt engineering profesional es system engineering alrededor de modelos generativos.

---

# 89. El flujo de producción no termina al escribir el prompt

Un ciclo más realista:

```text
DEFINIR OBJETIVO
↓
CREAR DATASET
↓
PROMPT v1
↓
EVALUAR
↓
DIAGNOSTICAR
↓
DECIDIR CAPA DEL ARREGLO
├─ prompt
├─ ejemplos
├─ retrieval
├─ tool
├─ parser
├─ código
├─ modelo
└─ fine-tuning
↓
RE-EVALUAR
↓
DESPLEGAR
↓
RECOGER FEEDBACK
↓
REGRESSION TESTS
```

---

# 90. Blind prompting es uno de los mayores antipatrones

El capítulo final vuelve sobre esta idea:

```text
"añadir más instrucciones"
```

sin comprobar su efecto puede:

- no cambiar nada;
- empeorar la calidad;
- aumentar tokens;
- aumentar latencia.

## Regla

> Cada bloque importante del prompt debería poder justificar su existencia mediante comportamiento observado.

---

# 91. Métricas específicas para cada tarea

El libro utiliza distintas evaluaciones según el objetivo.

Esto es correcto.

No existe una métrica universal.

Ejemplos:

```text
clasificación
→ accuracy / F1

formato
→ parse rate

estilo
→ preferencias humanas / distancia de representación

retrieval
→ relevancia / recall

agente
→ success rate / pasos / tool errors

texto creativo
→ pairwise preference
```

---

# 92. Automatic prompt optimization

El libro menciona sistemas que, dada una métrica:

```text
prueban instrucciones
+
prueban ejemplos
+
seleccionan combinación
```

La idea importante:

> Una vez que existe una función de evaluación, parte del prompt engineering puede automatizarse.

Esto conecta directamente con APE y otros trabajos de optimización automática.

---

# 93. El cuello de botella se desplaza hacia la evaluación

Si podemos generar mil prompts automáticamente pero no sabemos medirlos:

```text
1000 candidatos
+
0 señal
=
0 optimización
```

Por eso:

> La evaluación es la infraestructura que permite automatizar la mejora.

---

# 94. La métrica incorrecta puede optimizar lo equivocado

Un sistema puede maximizar el score sin maximizar la utilidad real.

Ejemplo:

```text
métrica: concisión
→ respuesta "sí"
→ muy concisa
→ inútil
```

Por tanto cada métrica debe cuestionarse:

```text
¿este score representa lo que el usuario realmente considera bueno?
```

---

# 95. Selección del modelo forma parte del diseño

El libro insiste en comparar modelos con la tarea real.

No asumir:

```text
modelo más grande = siempre mejor
```

La elección depende de:

- calidad;
- instrucciones;
- latencia;
- coste;
- contexto;
- multimodalidad;
- privacidad;
- despliegue local.

---

# 96. Los detalles de modelos del libro son históricos

El libro se publicó en 2024 y menciona:

- GPT-4;
- Claude 3;
- Llama 3;
- Gemini;
- Midjourney v6;
- Stable Diffusion XL;
- precios y context windows de entonces.

Esos datos no deben absorberse como reglas actuales.

Sí debemos conservar:

> **comparar modelos con evals propias y no asumir transferencia de prompts.**

---

# 97. Prompts no transfieren perfectamente entre modelos

El libro señala que una plantilla que funciona bien con un modelo puede no comportarse igual con otro.

Por tanto:

```text
cambio de modelo
↓
regression suite
↓
recalibrar prompt
```

Nunca:

```text
cambio de modelo
↓
asumir equivalencia
```

---

# 98. Privacy forma parte del sistema

El libro también advierte sobre datos sensibles y políticas de uso de los proveedores.

Regla general:

```text
antes de enviar datos
→ entender dónde se procesan
→ políticas de retención
→ permisos
→ sensibilidad
```

Prompt engineering no sustituye governance.

---

# 99. Antipatrones que debemos evitar

## 99.1 Prompt gigante

```text
si añadimos otra regla quizá mejore
```

sin medición.

## 99.2 “Actúa como experto” como sustituto de contexto

El rol no reemplaza datos ni evidencia.

## 99.3 Ejemplos arbitrarios

Pueden sesgar más de lo que ayudan.

## 99.4 Formato sin validación

“Devuelve JSON” no es un parser.

## 99.5 Self-critique como verdad

El mismo modelo puede repetir su error.

## 99.6 RAG por moda

Añade coste si no existe necesidad real.

## 99.7 Agente para una función simple

Añade autonomía y riesgo innecesarios.

## 99.8 Historial infinito como memoria

Añade ruido y coste.

## 99.9 Evaluar una sola ejecución

No representa variabilidad.

## 99.10 Cambiar cinco variables a la vez

Impide saber qué produjo la mejora.

## 99.11 Confiar en una métrica no validada

Puede optimizar un proxy equivocado.

## 99.12 No convertir fallos en tests

Los errores reaparecen.

---

# 100. Arquitectura recomendada para prompts maestros

Una síntesis inspirada en el libro:

```markdown
# 1. Objetivo
Qué resultado final se busca.

# 2. Contexto
Información necesaria para tomar decisiones correctas.

# 3. Alcance
Qué sí debe hacer y qué queda fuera.

# 4. Prioridades
Qué criterio gana cuando existen conflictos.

# 5. Reglas
Restricciones operativas concretas.

# 6. Fuentes
Qué información debe utilizar y qué hacer si no encuentra evidencia.

# 7. Ejemplos
Casos representativos cuando aporten señal real.

# 8. Procedimiento
Subtareas únicamente si la tarea necesita descomposición.

# 9. Herramientas
Qué tools puede utilizar y cuándo.

# 10. Validación
Qué debe comprobar antes de finalizar.

# 11. Output contract
Schema o estructura exacta.

# 12. Fallbacks
Qué hacer ante información insuficiente, error de herramienta o salida inválida.
```

---

# 101. Política de contexto recomendada

```text
1. Leer solicitud.
2. Identificar decisión requerida.
3. Identificar variables que pueden cambiar la decisión.
4. Compararlas con el contexto disponible.
5. Si falta una variable decisiva:
      preguntar o recuperar.
6. Si el contexto es suficiente:
      continuar.
```

Esto evita dos extremos:

```text
adivinar demasiado
vs.
preguntar demasiado
```

---

# 102. Política de fuentes recomendada

```markdown
- Prioriza las fuentes proporcionadas.
- No inventes información ausente.
- Distingue evidencia de inferencia.
- Si falta una evidencia crítica, indícalo.
- Cuando exista retrieval, cita la fuente utilizada.
```

---

# 103. Política de herramientas recomendada

```markdown
- Utiliza herramientas solamente cuando aporten información o acciones necesarias.
- Elige la herramienta más específica.
- No simules resultados de tools.
- Valida argumentos antes de ejecutar.
- Comprueba el resultado antes de continuar.
- Evita repetir la misma acción sin nueva información.
```

---

# 104. Política de descomposición recomendada

```text
TAREA SIMPLE
→ una etapa

TAREA MULTIETAPA
→ pipeline

TAREA CON BÚSQUEDA
→ retrieval + síntesis

TAREA CON ACCIONES
→ tool calling

TAREA CON INCERTIDUMBRE
→ candidatos + evaluación

TAREA CON DECISIONES TEMPRANAS CRÍTICAS
→ search / branching
```

---

# 105. Política de validación recomendada

Antes de entregar:

```text
¿cumplí objetivo?
¿seguí restricciones?
¿usé fuentes correctas?
¿hay afirmaciones sin soporte?
¿formato válido?
¿cálculos verificables?
¿faltan casos?
¿se puede comprobar con código?
```

Pero evitar convertir esta comprobación en verbosidad visible innecesaria.

---

# 106. Evaluation-driven prompt development

Pipeline recomendado:

```text
1. definir casos reales
2. definir criterio de éxito
3. guardar baseline
4. modificar una hipótesis
5. correr ambos
6. evaluar varias muestras
7. medir calidad + coste + latencia
8. analizar fallos
9. conservar cambio solo si mejora
10. añadir nuevos fallos al regression set
```

---

# 107. Evals mínimas para un prompt maestro

Un conjunto inicial debería incluir:

```text
happy path
input ambiguo
input incompleto
input largo
input contradictorio
caso límite
caso sin respuesta
caso con formato difícil
caso adversarial
caso donde una tool falla
```

---

# 108. Métricas mínimas

```text
task success
format success
groundedness
coverage
hallucination rate
refusal errors
latency
token usage
cost
tool error rate
```

No todas aplicarán a todas las tareas.

---

# 109. Error taxonomy

En vez de “respuesta mala”, clasificar:

```text
CONTEXT_ERROR
INSTRUCTION_ERROR
FORMAT_ERROR
RETRIEVAL_ERROR
REASONING_ERROR
TOOL_SELECTION_ERROR
TOOL_EXECUTION_ERROR
GROUNDING_ERROR
VALIDATION_ERROR
MODEL_CAPABILITY_ERROR
```

Esto permite arreglar el problema en la capa correcta.

---

# 110. Regla de escalado

Una arquitectura eficiente puede aumentar esfuerzo según dificultad:

```text
Nivel 1
direct answer

Nivel 2
más contexto / ejemplos

Nivel 3
descomposición

Nivel 4
retrieval / tool

Nivel 5
múltiples candidatos / evaluación

Nivel 6
modelo superior / revisión humana
```

No gastar Nivel 6 en cada solicitud.

---

# 111. Cómo decidir entre prompt, RAG, tool y fine-tuning

## Mejorar prompt

Cuando falla:

- dirección;
- formato;
- interpretación;
- ejemplos.

## RAG

Cuando falta conocimiento externo o dinámico.

## Tool

Cuando necesitamos:

- cálculo;
- ejecución;
- estado real;
- API;
- acción.

## Fine-tuning

Cuando necesitamos un patrón persistente a gran escala y tenemos datos suficientes.

## Código

Cuando la operación es determinista y puede programarse.

---

# 112. Regla: no solucionar todo con prompt engineering

Una de las conclusiones más importantes al integrar todo el libro es:

> Prompt engineering es solo una capa del sistema.

No utilizar un prompt para solucionar:

```text
validación determinista
permisos
autorización
cálculos exactos
schema enforcement
database constraints
```

si existe una herramienta mejor.

---

# 113. Qué conceptos del libro son especialmente útiles para nuestros prompts maestros

## Nivel S — imprescindibles

1. **Give Direction**
2. **Specify Format**
3. **Provide Examples**
4. **Evaluate Quality**
5. **Divide Labor**
6. preguntar por contexto cuando realmente falte;
7. grounded answers con referencias;
8. fallback explícito cuando no hay información;
9. outputs estructurados;
10. validación fuera del prompt;
11. test A/B;
12. prompt ablation;
13. versionado;
14. coste + latencia como métricas;
15. errores reales → regression tests.

## Nivel A — muy útiles según tarea

16. few-shot dinámico;
17. least-to-most;
18. self-critique;
19. RAG;
20. multi-query retrieval;
21. contextual compression;
22. tool calling;
23. ReAct;
24. plan/execution split;
25. memory selectiva;
26. automatic prompt optimization.

## Nivel B — específicos

27. Tree of Thoughts para búsqueda deliberada;
28. estilos visuales;
29. weighted terms;
30. inpainting/outpainting;
31. ControlNet;
32. fine-tuning visual.

---

# 114. Qué NO debemos absorber literalmente

Algunas partes del libro están ancladas a herramientas de 2024.

No debemos convertir en doctrina:

- precios históricos;
- tamaños de contexto históricos;
- sintaxis antigua de APIs;
- clases concretas de versiones antiguas de LangChain;
- rankings de modelos de 2024;
- nombres de agentes experimentales como arquitectura obligatoria;
- comandos específicos de una interfaz visual.

Debemos conservar el **principio subyacente**.

Ejemplo:

```text
DETALLE TEMPORAL:
"usa determinada clase de LangChain"

PRINCIPIO DURABLE:
"separa prompt → modelo → parser y observa cada etapa"
```

---

# 115. Lo que este libro añade frente a papers aislados

Los papers suelen demostrar una técnica concreta.

Este libro aporta una visión más operativa:

```text
prompt
+
formato
+
ejemplos
+
evals
+
chaining
+
RAG
+
tools
+
agents
+
observability
+
feedback
```

Lo valioso es verlo como un **sistema continuo de mejora**.

---

# 116. Formula condensada

Podemos comprimir el libro en una fórmula conceptual:

```text
RESULTADO FIABLE =
    DIRECCIÓN CLARA
  + CONTEXTO SUFICIENTE
  + EJEMPLOS ADECUADOS
  + OUTPUT CONTRACT
  + DESCOMPOSICIÓN CUANDO SEA NECESARIA
  + GROUNDING
  + VALIDACIÓN
  + EVALUACIÓN CONTINUA
```

---

# 117. Checklist maestro de creación de prompts

## Objetivo

- [ ] ¿Está claro qué debe conseguirse?
- [ ] ¿Está claro qué NO debe hacerse?
- [ ] ¿Existe una definición de éxito?

## Contexto

- [ ] ¿Tiene la información decisiva?
- [ ] ¿Debe pedir más contexto?
- [ ] ¿Debe recuperar información externa?
- [ ] ¿Existe información irrelevante que podamos eliminar?

## Dirección

- [ ] ¿Se ha definido audiencia?
- [ ] ¿Se ha definido estilo si importa?
- [ ] ¿Se han definido prioridades?
- [ ] ¿Se han eliminado instrucciones contradictorias?

## Ejemplos

- [ ] ¿Realmente hacen falta?
- [ ] ¿Son correctos?
- [ ] ¿Cubren variación?
- [ ] ¿Incluyen edge cases?
- [ ] ¿Consumen demasiado contexto?

## Formato

- [ ] ¿Está definido el output contract?
- [ ] ¿Es machine-readable cuando debe serlo?
- [ ] ¿Existe schema?
- [ ] ¿Existe parser?
- [ ] ¿Existe fallback ante formato inválido?

## Razonamiento / proceso

- [ ] ¿La tarea necesita descomposición?
- [ ] ¿Las etapas están aisladas?
- [ ] ¿Se valida la salida antes de pasar a la siguiente?
- [ ] ¿Puede resolverse algo de forma determinista?

## Fuentes

- [ ] ¿Debe responder solo desde referencias?
- [ ] ¿Existe política de abstención?
- [ ] ¿Se necesitan citas?
- [ ] ¿Se valida retrieval?

## Tools

- [ ] ¿La herramienta tiene nombre y descripción claros?
- [ ] ¿Los argumentos tienen schema?
- [ ] ¿Se validan antes de ejecutar?
- [ ] ¿Hay permisos?
- [ ] ¿Existe timeout/límite de iteraciones?

## Evaluación

- [ ] ¿Existe dataset?
- [ ] ¿Existe baseline?
- [ ] ¿Se prueban varias generaciones?
- [ ] ¿Se usa blind evaluation cuando procede?
- [ ] ¿La métrica representa utilidad real?
- [ ] ¿Se evalúa el evaluator?
- [ ] ¿Se mide coste?
- [ ] ¿Se mide latencia?

## Producción

- [ ] ¿El prompt está versionado?
- [ ] ¿Las trazas permiten debugging?
- [ ] ¿Los fallos entran al regression set?
- [ ] ¿Existe feedback de usuario?
- [ ] ¿Cambio de modelo dispara reevaluación?

---

# 118. Plantilla conceptual de prompt robusto

```markdown
# ROLE
Define solamente el marco profesional que ayude a orientar la tarea.

# OBJECTIVE
Explica con precisión el resultado que se necesita.

# CONTEXT
Incluye únicamente información relevante para la decisión.

# PRIORITIES
1. Corrección
2. Evidencia
3. Cumplimiento de formato
4. Cobertura
5. Estilo

# RULES
- Regla verificable 1
- Regla verificable 2
- Regla verificable 3

# SOURCES
Define qué fuentes puede utilizar.
Si falta evidencia, no inventar.

# EXAMPLES
Incluye solo si comunican comportamiento que las reglas no expresan bien.

# PROCESS
Descompón solo cuando el problema lo requiera.

# VALIDATION
Verifica restricciones, fuente y estructura antes de finalizar.

# OUTPUT
Define schema o estructura exacta.

# FAILURE BEHAVIOR
Especifica cómo actuar si:
- falta contexto;
- falta evidencia;
- una tool falla;
- el output no puede validarse.
```

---

# 119. Método de optimización de un prompt existente

Cuando revisemos un prompt maestro:

```text
PASO 1
identificar propósito de cada bloque

PASO 2
clasificarlo:
direction / format / examples / evaluation / labor

PASO 3
detectar:
redundancia / contradicción / ambigüedad

PASO 4
separar:
prompt-level vs architecture-level

PASO 5
crear baseline

PASO 6
hacer cambios incrementales

PASO 7
evaluar

PASO 8
eliminar partes sin beneficio

PASO 9
convertir fallos en tests

PASO 10
versionar
```

---

# 120. Principios absorbibles en una línea cada uno

1. **Da dirección suficiente, no decoración.**
2. **Si falta contexto decisivo, pregunta.**
3. **El output es una interfaz y debe tener contrato.**
4. **Valida estructuras programáticamente.**
5. **Los ejemplos enseñan mejor que muchas reglas, cuando están bien elegidos.**
6. **Más ejemplos no siempre es mejor.**
7. **Un prompt importante debe versionarse.**
8. **No mejores prompts a ciegas: mide.**
9. **Evalúa múltiples ejecuciones.**
10. **Haz comparaciones ciegas cuando sea posible.**
11. **Ground truth vence a opinión cuando existe.**
12. **Un LLM evaluator también necesita evaluación.**
13. **Calidad, coste y latencia deben optimizarse juntas.**
14. **Eliminar instrucciones puede mejorar un prompt.**
15. **Divide tareas complejas en etapas observables.**
16. **Valida cada etapa antes de propagarla.**
17. **No confundas self-critique con verificación.**
18. **Grounding + abstención reduce invención.**
19. **Retrieval es una herramienta, no una obligación.**
20. **Evalúa retrieval y generation por separado.**
21. **El chunking determina qué conocimiento puede recuperarse.**
22. **Usa metadata cuando la restricción es estructurada.**
23. **Function calling es preferible a un agente cuando la acción es simple.**
24. **Las tools necesitan schemas y validación.**
25. **No inventes tool results.**
26. **Todo agente necesita stop conditions.**
27. **Memory debe seleccionar, no acumular.**
28. **Observability debe existir desde el diseño.**
29. **Las técnicas visuales demuestran que no todo problema se resuelve con más texto.**
30. **Optimiza la capa correcta.**
31. **Cambiar de modelo exige regression tests.**
32. **Los datos de feedback deben alimentar el siguiente ciclo de evaluación.**

---

# 121. Síntesis final

*Prompt Engineering for Generative AI* es más útil cuando se lee no como un catálogo de trucos, sino como una introducción a una forma de ingeniería.

Los cinco principios forman una secuencia lógica:

```text
GIVE DIRECTION
→ ¿sabe qué queremos?

SPECIFY FORMAT
→ ¿sabemos cómo debe entregarlo?

PROVIDE EXAMPLES
→ ¿hemos mostrado qué consideramos correcto?

EVALUATE QUALITY
→ ¿sabemos si realmente funciona?

DIVIDE LABOR
→ ¿hemos puesto cada problema en una etapa manejable?
```

A partir de ahí, el libro expande estos principios hacia:

```text
prompt templates
→ parsers
→ evals
→ chains
→ retrieval
→ tools
→ memory
→ agents
→ multimodal workflows
```

La idea que más merece la pena conservar para futuros prompts maestros es:

> **Un buen prompt no es el que contiene más instrucciones; es el que forma parte de un sistema donde objetivo, contexto, ejemplos, formato, validación y evaluación están claramente definidos.**

Y la segunda idea más importante:

> **Cuando una mejora puede resolverse mejor mediante código, retrieval, schemas, herramientas, evaluación o arquitectura, no deberíamos intentar esconder toda esa complejidad dentro de un único prompt.**

En forma compacta:

```text
NO:
prompt gigantesco
→ esperar que todo salga bien

SÍ:
objetivo claro
→ contexto adecuado
→ prompt mínimo efectivo
→ output estructurado
→ validación
→ evaluación
→ feedback
→ mejora continua
```

Ese es el núcleo realmente durable del libro.
