# Principios clave de *AI Engineering: Building Applications with Foundation Models*

**Autora:** Chip Huyen  
**Editorial:** O’Reilly Media  
**Edición analizada:** 2024  
**Objetivo de este documento:** extraer y condensar las ideas más duraderas, útiles y operativas del libro para construir aplicaciones con foundation models, diseñar prompts avanzados, sistemas RAG, agentes, pipelines de evaluación y arquitecturas de producción.

> Este documento no intenta sustituir al libro ni resumir cada capítulo de forma lineal. Prioriza los principios que merece la pena reutilizar en proyectos reales y, especialmente, en el diseño de prompts maestros y sistemas basados en LLMs.

---

# 1. Idea central del libro

La tesis práctica del libro puede resumirse así:

> **Construir una buena aplicación de IA no consiste en encontrar un modelo excelente ni en escribir un prompt excelente, sino en diseñar un sistema completo alrededor de modelos probabilísticos.**

Ese sistema incluye:

```text
PROBLEMA
   ↓
DATOS / CONTEXTO
   ↓
PROMPT
   ↓
MODELO
   ↓
HERRAMIENTAS / RAG / AGENTES
   ↓
GUARDRAILS
   ↓
SALIDA
   ↓
EVALUACIÓN
   ↓
MONITORIZACIÓN
   ↓
FEEDBACK REAL
   ↓
ITERACIÓN
```

Esta perspectiva es especialmente importante porque muchos problemas atribuidos al modelo son en realidad problemas de:

- contexto;
- datos;
- evaluación;
- arquitectura;
- retrieval;
- instrucciones;
- observabilidad;
- latencia;
- seguridad;
- experiencia de usuario.

La unidad de optimización real no debería ser únicamente el prompt ni el modelo.

> **La unidad de optimización es el sistema completo.**

---

# 2. AI engineering no es simplemente machine learning

El libro presenta **AI engineering** como la disciplina de construir aplicaciones utilizando foundation models ya existentes.

La diferencia fundamental respecto al ML tradicional es que muchos equipos ya no necesitan:

```text
recopilar dataset
→ entrenar modelo desde cero
→ desplegar modelo
```

Ahora pueden comenzar con:

```text
foundation model
→ adaptar mediante contexto, prompting, RAG o fine-tuning
→ integrar en producto
→ evaluar
→ desplegar
```

Esto desplaza gran parte del trabajo desde el entrenamiento hacia:

- selección de modelos;
- diseño de prompts;
- evaluación;
- construcción de contexto;
- pipelines;
- herramientas;
- UX;
- observabilidad;
- seguridad;
- coste y latencia.

---

# 3. Antes de construir una aplicación de IA, preguntar si debería existir

Una de las ideas más útiles del primer capítulo es no asumir que utilizar IA es automáticamente una buena decisión.

Antes de desarrollar una solución hay que analizar:

```text
¿Existe un problema real?
¿La IA aporta una ventaja frente a software tradicional?
¿Qué papel desempeñará la IA?
¿Qué papel conservarán los humanos?
¿Qué nivel de error es aceptable?
¿Qué ocurre cuando el sistema falla?
¿Existe una ventaja competitiva sostenible?
¿Puede mantenerse el sistema a largo plazo?
```

## Principio operativo

> **No comenzar por “¿qué puedo hacer con este modelo?”, sino por “¿qué problema merece la pena resolver y qué parte de él necesita realmente IA?”**

---

# 4. Definir explícitamente el papel de humanos e IA

No todas las tareas deben automatizarse por completo.

Una arquitectura puede adoptar distintos niveles:

```text
IA propone → humano decide
IA ejecuta → humano revisa
IA clasifica → humano resuelve excepciones
IA actúa automáticamente → humano audita
IA completamente autónoma
```

Cuanto mayor sea:

- el impacto;
- la irreversibilidad;
- el coste del error;
- la sensibilidad de los datos;

más importante es diseñar participación humana o controles deterministas.

Esto conecta directamente con los agentes: dar más autonomía aumenta capacidad, pero también aumenta el radio de daño potencial.

---

# 5. La ventaja competitiva rara vez será “usar el mismo modelo que todos”

Los foundation models son cada vez más accesibles.

Por eso, utilizar un modelo potente no constituye necesariamente una ventaja sostenible.

La diferenciación suele aparecer en:

- datos propios;
- feedback de usuarios;
- experiencia de producto;
- contexto específico;
- integración con workflows;
- conocimiento de dominio;
- distribución;
- evaluación;
- infraestructura;
- velocidad de aprendizaje.

## Regla práctica

> **El modelo puede ser una dependencia; el sistema y los datos pueden convertirse en la ventaja.**

---

# 6. Diseñar expectativas realistas desde el inicio

Los foundation models son probabilísticos.

Una aplicación no debería diseñarse suponiendo que:

```text
misma entrada = misma salida
```

ni que:

```text
respuesta convincente = respuesta correcta
```

El libro insiste en comprender propiedades como:

- variabilidad;
- inconsistencia;
- alucinación;
- sensibilidad a la entrada;
- cambios entre versiones de modelos.

## Consecuencia

La aplicación debe diseñarse **alrededor de la incertidumbre**, no fingir que esta no existe.

---

# 7. El comportamiento del modelo empieza en sus datos

Para entender por qué un modelo funciona bien o mal en una tarea, hay que pensar en aquello a lo que estuvo expuesto durante entrenamiento y post-training.

Un modelo puede tener capacidades muy desiguales según:

- idioma;
- dominio;
- tipo de documento;
- código;
- estilo;
- conocimiento;
- formato;
- tarea.

## Lección

> Un foundation model “generalista” no implica competencia uniforme en todos los dominios.

Por eso, cuando un modelo falla, las soluciones posibles incluyen:

```text
mejor contexto
mejor prompt
mejor retrieval
otro modelo
fine-tuning
herramientas
software determinista
```

No todas las deficiencias deben resolverse aumentando el tamaño del prompt.

---

# 8. Modelo más grande no significa automáticamente mejor sistema

La capacidad del modelo es solamente una dimensión.

También existen:

- coste;
- latencia;
- privacidad;
- control;
- disponibilidad;
- capacidad de fine-tuning;
- contexto disponible;
- estabilidad;
- facilidad de despliegue.

Un modelo pequeño especializado puede superar a un modelo grande generalista en una tarea concreta.

## Aplicación

Seleccionar el modelo **por requisitos del sistema**, no por prestigio o tamaño.

---

# 9. El sampling forma parte del comportamiento del sistema

La generación no depende solamente del prompt.

También depende de parámetros y estrategias de sampling.

Entre ellos:

- temperatura;
- top-k;
- top-p;
- condiciones de parada.

La temperatura afecta especialmente a la diversidad de las salidas.

## Consecuencia importante

Cuando se comparan prompts o modelos, los parámetros de generación deberían controlarse.

De lo contrario puede confundirse:

```text
efecto del prompt
```

con:

```text
efecto del sampling
```

---

# 10. La naturaleza probabilística no es únicamente un defecto

La variabilidad es problemática para:

- clasificación;
- extracción;
- cálculos;
- decisiones deterministas;
- sistemas que necesitan reproducibilidad.

Pero puede ser positiva para:

- brainstorming;
- generación creativa;
- búsqueda de alternativas;
- síntesis;
- redacción.

Por tanto:

> **La cantidad de variabilidad deseable depende del objetivo.**

No existe una configuración universalmente óptima.

---

# 11. Diseñar outputs estructurados de forma deliberada

El libro analiza varias formas de conseguir salidas estructuradas:

```text
prompting
post-procesamiento
constrained sampling
fine-tuning
```

Esto es importante porque el output de una aplicación puede ser consumido por:

- humanos;
- otra llamada de modelo;
- una API;
- una base de datos;
- una herramienta;
- código.

## Regla práctica

Si la respuesta alimentará software:

```text
define esquema
→ restringe formato
→ valida
→ reintenta o corrige
```

No confiar en que el modelo produzca espontáneamente una estructura estable.

---

# 12. Evaluation-driven development

Una de las ideas centrales del libro es desarrollar sistemas de IA guiados por evaluación.

En vez de:

```text
construir
→ mirar unas cuantas respuestas
→ decidir que parece funcionar
```

utilizar:

```text
definir criterios
→ construir conjunto de evaluación
→ establecer baseline
→ modificar sistema
→ volver a evaluar
→ comparar
→ desplegar
→ monitorizar
```

## Principio

> **La evaluación no es el último paso del proyecto. Es parte del ciclo de desarrollo.**

---

# 13. Evaluar foundation models es más difícil que evaluar ML tradicional

En tareas tradicionales pueden existir métricas claras:

```text
accuracy
precision
recall
F1
```

Pero muchas tareas generativas tienen múltiples respuestas válidas.

Ejemplo:

```text
"Resume este documento."
```

No existe necesariamente una única respuesta correcta.

Esto obliga a combinar:

- métricas exactas;
- tests funcionales;
- similitud;
- evaluación humana;
- AI-as-a-judge;
- señales de producto.

---

# 14. Utilizar evaluación exacta siempre que sea posible

La evaluación subjetiva es necesaria en muchos problemas, pero las métricas exactas suelen ser:

- más reproducibles;
- más baratas;
- más rápidas;
- más fáciles de depurar.

Ejemplos:

```text
¿El JSON parsea?
¿El código compila?
¿La función pasa los tests?
¿El dato existe?
¿La consulta SQL devuelve el resultado correcto?
¿El campo obligatorio está presente?
```

## Principio

> **Transformar la mayor cantidad posible de calidad subjetiva en propiedades verificables.**

---

# 15. Functional correctness puede ser más valiosa que similitud textual

Dos respuestas pueden utilizar palabras completamente distintas y ser funcionalmente equivalentes.

En programación, por ejemplo, comparar el texto generado con una solución de referencia es menos útil que ejecutar tests.

Esto conduce a una regla general:

> **Evalúa el efecto de la respuesta cuando puedas, no solo su apariencia.**

---

# 16. AI-as-a-judge es útil, pero no constituye ground truth

Utilizar modelos para evaluar otros outputs permite escalar evaluaciones subjetivas.

Pero introduce problemas:

- inconsistencia;
- sesgos;
- sensibilidad al prompt;
- preferencia por determinados estilos;
- coste;
- latencia;
- cambios al actualizar el juez.

Por tanto:

```text
AI judge ≠ verdad absoluta
```

## Buena práctica

Combinarlo con:

- criterios objetivos;
- humanos;
- tests funcionales;
- muestras auditadas.

---

# 17. Un juez también necesita ser evaluado

Una idea fundamental:

> **Si una métrica está producida por otro modelo, ese sistema de evaluación también necesita validación.**

Preguntas útiles:

```text
¿Coincide con evaluadores humanos?
¿Es consistente?
¿Favorece outputs largos?
¿Favorece cierto estilo?
¿Cambian sus resultados según el orden?
¿Entiende la rúbrica?
```

---

# 18. La evaluación comparativa puede ser más fácil que la absoluta

En muchas tareas resulta difícil responder:

```text
"¿Esta respuesta merece 7.3/10?"
```

pero más sencillo:

```text
"¿A o B es mejor?"
```

Las comparaciones por pares pueden ser útiles para:

- selección de modelos;
- experimentos A/B;
- preferencias;
- ranking de outputs.

Sin embargo también pueden sufrir:

- sesgos de posición;
- escalabilidad;
- inconsistencia;
- ausencia de una escala absoluta.

---

# 19. Los benchmarks públicos sirven para filtrar, no para elegir automáticamente

Un benchmark puede ayudar a descartar modelos claramente insuficientes.

Pero el mejor modelo en un leaderboard puede no ser el mejor para tu producto.

Problemas:

- contaminación de datos;
- tareas diferentes a las tuyas;
- agregaciones arbitrarias;
- métricas que no representan negocio;
- configuraciones diferentes.

## Regla práctica

> **Tu conjunto de evaluación privado debe representar tu aplicación real.**

---

# 20. Construir una evaluación interna específica del producto

El libro propone una lógica muy cercana a:

```text
1. definir criterios
2. crear rúbricas
3. añadir ejemplos
4. elegir métodos de evaluación
5. obtener datos representativos
6. validar la evaluación
7. iterar
```

La evaluación debe incluir los casos que realmente importan.

Por ejemplo:

```text
casos comunes
casos difíciles
edge cases
errores históricos
entradas ambiguas
entradas adversariales
formatos inesperados
```

---

# 21. Vincular métricas técnicas con métricas de negocio

Una mejora en un benchmark interno no importa si no mejora el producto.

Ejemplos:

```text
mejor relevancia
→ mayor resolución de consultas

menos alucinaciones
→ menos escalaciones

menor latencia
→ mayor conversión

mejor extracción
→ menor intervención manual
```

## Principio

> **Una métrica debe existir porque ayuda a tomar una decisión.**

---

# 22. Prompt engineering es comunicación, no magia

El libro trata el prompting como comunicación humano–IA.

Un buen prompt busca reducir la diferencia entre:

```text
lo que quieres
```

y:

```text
lo que el modelo interpreta que quieres
```

La facilidad para empezar a escribir prompts puede crear una falsa sensación de sencillez.

Es fácil escribir prompts.

Es mucho más difícil construir prompts:

- robustos;
- mantenibles;
- evaluables;
- seguros;
- transferibles.

---

# 23. Anatomía práctica de un prompt

Los prompts modernos suelen incluir distintas capas:

```text
SYSTEM / DEVELOPER INSTRUCTIONS
USER REQUEST
CONTEXT
EXAMPLES
OUTPUT REQUIREMENTS
TOOL INFORMATION
CONVERSATION HISTORY
```

Estas piezas no deberían mezclarse indiscriminadamente.

## Aplicación a prompts maestros

Separar claramente:

```markdown
# OBJETIVO

# CONTEXTO

# REGLAS

# DATOS DE ENTRADA

# HERRAMIENTAS

# PROCEDIMIENTO

# FORMATO DE SALIDA

# CRITERIOS DE VALIDACIÓN
```

---

# 24. In-context learning permite adaptar sin modificar pesos

Zero-shot y few-shot permiten especificar tareas mediante el contexto.

Esto hace posible modificar comportamientos rápidamente sin fine-tuning.

## Zero-shot

```text
instrucción
+
entrada
```

## Few-shot

```text
instrucción
+
ejemplo 1
+
ejemplo 2
+
entrada real
```

Los ejemplos pueden comunicar:

- formato;
- clasificación;
- estilo;
- razonamiento;
- casos límite;
- criterios.

---

# 25. Escribir instrucciones claras y explícitas

Las instrucciones deberían reducir ambigüedad.

Evitar:

```text
"Analiza esto bien."
```

Preferir algo como:

```text
Analiza el documento buscando:
- contradicciones
- requisitos ausentes
- riesgos
- información no respaldada

Para cada hallazgo indica evidencia y severidad.
```

## Principio

> **Lo que no se especifica queda abierto a interpretación.**

---

# 26. Una persona o rol puede ayudar, pero no sustituye una especificación

Pedir al modelo que adopte una función determinada puede influir en:

- vocabulario;
- estilo;
- perspectiva;
- profundidad.

Pero:

```text
"Actúa como experto"
```

no sustituye:

- objetivos;
- criterios;
- contexto;
- fuentes;
- restricciones;
- formato.

Los roles deben complementar el diseño, no ocultar su ausencia.

---

# 27. Los ejemplos suelen ser una de las formas más densas de instrucción

Un ejemplo correcto puede comunicar simultáneamente:

```text
qué interpretar
cómo responder
qué formato usar
qué granularidad usar
qué omitir
```

Pero los ejemplos deben seleccionarse con cuidado.

Un ejemplo incorrecto o poco representativo puede enseñar un comportamiento indeseado.

---

# 28. Especificar el formato de salida

Si necesitas:

- JSON;
- YAML;
- Markdown;
- tabla;
- lista;
- esquema;

indícalo.

Cuando la estructura sea crítica, no limitarse a pedirla: validar posteriormente que se cumple.

La arquitectura robusta es:

```text
GENERAR
↓
VALIDAR
↓
CORREGIR / REINTENTAR
↓
CONSUMIR
```

---

# 29. Un modelo necesita contexto además de instrucciones

Puedes dar instrucciones perfectas, pero si la respuesta depende de información que el modelo no tiene, fallará.

La calidad depende de dos grandes elementos:

```text
INSTRUCCIÓN
+
INFORMACIÓN RELEVANTE
```

Por eso el libro conecta prompt engineering directamente con RAG.

---

# 30. Restringir al modelo a un corpus mediante prompts no ofrece garantías absolutas

Instrucciones como:

```text
"Responde únicamente utilizando el contexto proporcionado."
```

pueden ayudar.

También puede ayudar exigir:

- citas;
- fragmentos de evidencia;
- referencias concretas;
- respuesta “no encontrado” cuando falte información.

Pero el libro advierte que una instrucción por sí sola no garantiza que conocimiento externo no influya en la respuesta.

## Principio

> **Una política importante no debería depender exclusivamente de obediencia probabilística.**

---

# 31. Descomponer tareas complejas

Una de las recomendaciones más útiles del capítulo de prompting es dividir procesos complejos en subtareas.

En lugar de:

```text
PROMPT GIGANTE
→ RESULTADO
```

usar:

```text
clasificar intención
→ recuperar información
→ analizar
→ generar
→ verificar
→ formatear
```

## Beneficios

### Monitorización

Puedes inspeccionar outputs intermedios.

### Depuración

Puedes localizar exactamente dónde falla el sistema.

### Paralelización

Tareas independientes pueden ejecutarse simultáneamente.

### Simplicidad

Cada prompt tiene una responsabilidad más clara.

---

# 32. La granularidad óptima de la descomposición debe medirse

Dividir una tarea demasiado poco puede reducir fiabilidad.

Dividirla demasiado puede aumentar:

- latencia;
- coste;
- complejidad;
- puntos de fallo.

Por tanto:

> **La descomposición es un trade-off que debe evaluarse experimentalmente.**

---

# 33. Dar más computación a problemas difíciles

El libro aborda técnicas como Chain-of-Thought y self-critique como formas de dedicar más pasos de inferencia a una tarea.

La idea duradera es:

```text
problema sencillo
→ respuesta directa

problema complejo
→ planificación / pasos / verificación
```

No todas las preguntas requieren el mismo presupuesto de razonamiento.

## Advertencia

Más razonamiento también puede significar:

- más tokens;
- más latencia;
- mayor coste.

---

# 34. Self-critique puede mejorar, pero tampoco es un verificador perfecto

Pedir al modelo que revise una respuesta puede encontrar errores.

Ejemplo conceptual:

```text
GENERACIÓN
↓
CRÍTICA
↓
REVISIÓN
```

Pero el mismo modelo puede:

- no detectar su propio error;
- inventar uno;
- cambiar una respuesta correcta por una peor.

Por ello, cuando existan comprobaciones deterministas, deben preferirse.

---

# 35. Prompt engineering debe ser iterativo y experimental

No existe garantía de que un prompt que parece mejor lingüísticamente produzca mejores resultados.

Proceso recomendado:

```text
PROMPT A
↓
EVALUACIÓN

MODIFICACIÓN
↓
PROMPT B
↓
MISMA EVALUACIÓN

COMPARACIÓN
```

## Regla

> **No aceptar una mejora de prompt sin medirla.**

---

# 36. Evaluar cada prompt dentro del sistema completo

Una modificación puede mejorar una subtarea y empeorar el resultado final.

Ejemplo:

```text
prompt de clasificación
↑ accuracy local

pero
↓ distribución correcta hacia módulos posteriores
```

Esto significa que deben existir:

- métricas de componente;
- métricas end-to-end.

---

# 37. Versionar prompts como código

El libro recomienda separar prompts del código y versionarlos.

Ventajas:

- reutilización;
- tests independientes;
- mejor lectura;
- colaboración con expertos de dominio;
- rollback;
- trazabilidad.

Cada prompt puede incluir metadatos como:

```text
modelo
versión
fecha
aplicación
autor
parámetros
input schema
output schema
```

## Principio importante

> **Un prompt de producción es un artefacto de software.**

No debería vivir como un string anónimo disperso por el código.

---

# 38. Mantener un catálogo de prompts

Cuando existen muchos sistemas y aplicaciones, un catálogo central puede permitir:

```text
buscar prompts
versionarlos
identificar dependencias
comparar versiones
asociar modelos
asociar evaluaciones
notificar cambios
```

Esto es especialmente importante para prompts maestros reutilizados por varios sistemas.

---

# 39. La seguridad de prompts es un problema de sistema

El libro analiza:

- prompt extraction;
- jailbreaking;
- prompt injection;
- indirect prompt injection.

La conclusión práctica es clara:

> **No existe una cadena de texto capaz de garantizar por sí sola la seguridad del sistema.**

La seguridad debe implementarse en varias capas.

---

# 40. Utilizar defensa en profundidad

Las defensas pueden existir a nivel:

```text
MODELO
PROMPT
SISTEMA
```

Ejemplos de sistema:

- validación de inputs;
- aislamiento de datos;
- permisos;
- allowlists;
- confirmación;
- sandboxing;
- separación de privilegios;
- filtros;
- detección;
- validación de outputs.

## Principio

> **Las capacidades que el modelo no necesita no deberían estar disponibles.**

---

# 41. Medir seguridad y utilidad simultáneamente

Un sistema que rechaza absolutamente todo puede ser muy “seguro” y completamente inútil.

El libro propone considerar al menos dos dimensiones:

```text
VIOLATION RATE
FALSE REFUSAL RATE
```

La seguridad requiere equilibrar:

- bloquear acciones peligrosas;
- permitir solicitudes legítimas.

---

# 42. RAG es principalmente un problema de retrieval

RAG suele representarse así:

```text
consulta
↓
recuperación
↓
contexto
↓
modelo
↓
respuesta
```

Pero la calidad del generador no puede compensar indefinidamente un mal retriever.

Si se recupera información:

- irrelevante;
- incompleta;
- incorrecta;
- desactualizada;

la respuesta probablemente sufrirá.

> **La calidad del RAG depende enormemente de la calidad del retrieval.**

---

# 43. Empezar retrieval con baselines sencillos

El libro recuerda que soluciones clásicas como:

- BM25;
- Elasticsearch;
- búsqueda por términos;

pueden ser baselines muy fuertes.

Embeddings añaden recuperación semántica, pero también:

- infraestructura;
- cálculo;
- complejidad.

## Regla

> **No utilizar vector search únicamente porque sea moderno. Compararlo con alternativas simples.**

---

# 44. Sparse y dense retrieval capturan señales diferentes

## Sparse / term-based

Excelente cuando importan términos exactos.

Ejemplos:

- nombres;
- IDs;
- errores;
- símbolos;
- palabras específicas.

## Dense / embeddings

Excelente cuando importan similitudes semánticas.

Ejemplo:

```text
"cancelar mi suscripción"
```

puede relacionarse con:

```text
"dar de baja el plan"
```

aunque no compartan exactamente las mismas palabras.

## Enfoque práctico

Los sistemas híbridos pueden combinar ambas señales.

---

# 45. Chunking es una decisión de producto, no un detalle trivial

Dividir documentos demasiado grandes:

- introduce ruido;
- consume contexto.

Dividirlos demasiado pequeños:

- elimina relaciones;
- pierde significado.

La estrategia debería considerar:

- estructura del documento;
- tipo de preguntas;
- tamaño del modelo;
- solapamiento;
- metadatos;
- coste.

---

# 46. Recuperar no significa utilizar directamente

Después de retrieval puede existir:

```text
RETRIEVE
↓
RERANK
↓
FILTER
↓
ASSEMBLE CONTEXT
```

El reranking permite utilizar un mecanismo más caro sobre un conjunto pequeño de candidatos.

Esto ayuda a maximizar relevancia sin pagar el coste sobre todo el corpus.

---

# 47. Reescribir consultas puede mejorar retrieval

La consulta del usuario puede no ser la mejor query de búsqueda.

Por tanto:

```text
pregunta del usuario
↓
query rewriting
↓
retrieval
```

La reescritura puede:

- eliminar ambigüedad;
- generar sinónimos;
- expandir conceptos;
- convertir conversación en consulta independiente.

---

# 48. Evaluar retrieval por separado del generador

Cuando RAG falla hay que distinguir:

```text
¿falló la recuperación?
```

de:

```text
¿el documento correcto estaba presente pero el modelo lo utilizó mal?
```

Si no se separan esas métricas, se puede intentar arreglar el componente equivocado.

---

# 49. Context construction equivale aproximadamente a feature engineering para foundation models

Una de las analogías más útiles del libro:

> **Construir el contexto correcto para un foundation model cumple un papel parecido al feature engineering de ML tradicional.**

El sistema decide qué información tendrá disponible el modelo en el momento de tomar una decisión.

Esto convierte context engineering en una disciplina central.

---

# 50. RAG no está limitado a texto

El contexto puede provenir de:

- texto;
- imágenes;
- tablas;
- SQL;
- APIs;
- bases de datos;
- búsqueda web;
- logs.

Esto amplía la idea de RAG hacia sistemas que recuperan cualquier información necesaria antes de generar.

---

# 51. Un agente es modelo + entorno + herramientas + planificación

El libro define agentes en términos de la interacción del modelo con sistemas externos.

Un agente típico tiene:

```text
OBJETIVO
↓
OBSERVACIÓN
↓
PLAN
↓
ACCIÓN
↓
NUEVA OBSERVACIÓN
↓
ACTUALIZACIÓN DEL PLAN
```

El modelo actúa como planificador.

Las herramientas convierten texto en acciones reales.

---

# 52. Las herramientas determinan la capacidad real del agente

Un agente sin herramientas solamente genera información.

Un agente con herramientas puede:

- buscar;
- consultar;
- calcular;
- editar;
- enviar;
- comprar;
- desplegar;
- modificar estado.

## Principio

> **La superficie de herramientas define tanto la capacidad como el riesgo del agente.**

---

# 53. Cuantas más herramientas, más difícil el tool selection

Más herramientas pueden permitir resolver problemas más amplios.

Pero también aumentan:

- confusión;
- errores de selección;
- superficie de ataque;
- espacio de planificación;
- coste.

Diseñar herramientas:

- específicas;
- semánticamente claras;
- no redundantes;
- con esquemas simples.

---

# 54. Separar herramientas de lectura y herramientas de escritura

No todas las acciones tienen el mismo riesgo.

### Lectura

```text
search
get
list
fetch
```

### Escritura

```text
send
delete
purchase
deploy
update
```

Las acciones de escritura deberían recibir controles superiores:

- autorización;
- confirmación;
- validación;
- límites;
- auditoría.

---

# 55. La planificación es uno de los principales cuellos de botella de agentes

Un agente puede tener todas las herramientas correctas y fallar porque:

- descompone mal el objetivo;
- ejecuta pasos en orden incorrecto;
- se atasca;
- repite acciones;
- interpreta mal una observación;
- no reconoce que terminó.

Por eso la evaluación de agentes debe estudiar trayectorias, no solo la respuesta final.

---

# 56. Reflection y memory ayudan, pero añaden complejidad

Un agente puede:

```text
ejecutar
→ observar error
→ reflexionar
→ modificar plan
```

También puede conservar información anterior mediante memoria.

Pero la memoria necesita gestión.

No debería convertirse simplemente en:

```text
"guardar todo para siempre"
```

Sino en:

```text
qué recordar
qué recuperar
cuándo recuperar
qué olvidar
cómo priorizar
```

---

# 57. Mayor autonomía implica mayor potencial de fallo

Esta es una de las ideas más importantes del capítulo de agentes.

A medida que un agente puede:

```text
leer
→ decidir
→ modificar
→ ejecutar
```

sus errores dejan de ser únicamente respuestas malas.

Pueden convertirse en:

- cambios incorrectos;
- pérdida de datos;
- gasto;
- acciones externas;
- vulnerabilidades.

## Regla

> **La autonomía debe ganarse mediante evaluación y controles.**

---

# 58. Fine-tuning debería llegar después de explorar métodos basados en prompts

El libro recomienda generalmente probar primero:

- prompting;
- contexto;
- RAG;
- herramientas.

Fine-tuning requiere más:

- datos;
- hardware;
- experiencia ML;
- mantenimiento.

Eso no significa que fine-tuning sea malo, sino que tiene un coste de entrada superior.

---

# 59. Fine-tuning y prompting no son excluyentes

Una aplicación real puede utilizar:

```text
modelo fine-tuned
+
system prompt
+
RAG
+
herramientas
```

Cada capa resuelve problemas diferentes.

No plantear siempre:

```text
RAG vs fine-tuning
```

como una elección binaria.

---

# 60. RAG y fine-tuning solucionan problemas distintos

Simplificando:

## RAG

Útil cuando necesitas que el modelo disponga de:

- conocimiento actualizado;
- documentos privados;
- información recuperable;
- datos que cambian.

## Fine-tuning

Útil cuando quieres modificar:

- comportamiento;
- especialización;
- estilo;
- formato;
- capacidad específica;
- eficiencia mediante un modelo más pequeño.

Una regla útil:

> **RAG modifica lo que el modelo sabe en el contexto actual; fine-tuning modifica cómo se comporta el modelo.**

Es una simplificación, pero sirve como excelente modelo mental.

---

# 61. Fine-tuning puede degradar capacidades

Optimizar un modelo para una tarea puede empeorarlo en otras.

Esto significa que la evaluación debe medir:

```text
objetivo que quieres mejorar
+
capacidades que no quieres perder
```

Es decir, tests de:

- mejora;
- regresión.

---

# 62. Modelos pequeños especializados pueden ser extremadamente valiosos

Una vez fine-tuned, un modelo pequeño puede:

- costar menos;
- responder más rápido;
- ser más sencillo de alojar;
- superar a uno grande en una tarea concreta.

Esto permite arquitecturas de routing:

```text
tarea simple/específica → modelo pequeño
tarea compleja → modelo grande
```

---

# 63. La dificultad del fine-tuning suele estar en los datos

Las herramientas modernas pueden simplificar el proceso técnico de entrenamiento.

El problema más difícil suele ser:

```text
¿Qué comportamiento quiero enseñar?
¿Qué ejemplos lo representan?
¿Son correctos?
¿Cubren los casos importantes?
```

Esto conduce directamente a dataset engineering.

---

# 64. Tres dimensiones fundamentales de un dataset

El libro destaca:

```text
CALIDAD
COBERTURA
CANTIDAD
```

La cantidad por sí sola es insuficiente.

Una colección pequeña de ejemplos excelentes puede superar a grandes cantidades de datos ruidosos.

---

# 65. Calidad de datos significa utilidad para la tarea

El libro identifica características importantes:

```text
relevantes
alineados con requisitos
consistentes
correctamente formateados
suficientemente únicos
compliant
```

Esto se aplica no solo a fine-tuning.

También se aplica a:

- ejemplos few-shot;
- datasets de evaluación;
- documentación RAG;
- prompts de referencia.

---

# 66. Las guidelines de anotación son parte del producto

Si los propios humanos no pueden ponerse de acuerdo sobre cómo etiquetar algo, el modelo tendrá dificultades para aprenderlo.

Por eso hay que invertir en:

- definiciones;
- criterios;
- ejemplos;
- contraejemplos;
- edge cases;
- resolución de ambigüedad.

## Aplicación directa a prompts maestros

Una buena sección de criterios puede funcionar como una mini guideline de anotación.

---

# 67. Coverage importa tanto como correctness

Un dataset puede ser perfectamente correcto y aun así resultar malo si solo representa una fracción mínima del mundo real.

Debe cubrir:

- tipos de usuarios;
- expresiones distintas;
- casos difíciles;
- formatos;
- longitudes;
- idiomas;
- excepciones.

---

# 68. Datos sintéticos son poderosos, pero necesitan verificación

Los modelos pueden generar:

- ejemplos;
- instrucciones;
- variaciones;
- casos adversariales;
- datos de entrenamiento.

Pero los datos sintéticos pueden contener:

- errores;
- sesgos;
- homogeneidad;
- artefactos del modelo generador.

Por tanto:

```text
GENERAR
≠
ACEPTAR
```

Hay que verificar.

---

# 69. La verificación suele ser más difícil que la generación

Crear miles de ejemplos es fácil.

Confirmar que miles de ejemplos son:

- correctos;
- diversos;
- útiles;
- seguros;

es mucho más difícil.

Este principio se generaliza a outputs de IA:

> **Generar es barato; demostrar calidad es el verdadero trabajo.**

---

# 70. Dataset engineering y prompt engineering están más relacionados de lo que parece

Un conjunto de ejemplos few-shot es, esencialmente, un dataset diminuto introducido en contexto.

Por tanto, principios como:

- calidad;
- diversidad;
- cobertura;
- consistencia;

también deberían aplicarse al diseñar ejemplos en prompts maestros.

---

# 71. Latencia y coste forman parte de la calidad

Una respuesta perfecta que tarda demasiado puede ser un mal producto.

Por eso el libro distingue métricas como:

```text
TTFT — time to first token
TPOT — time per output token
throughput
goodput
```

## Principio

> **La calidad de un sistema de IA no es solamente semántica.**

También incluye:

- velocidad;
- precio;
- disponibilidad;
- estabilidad.

---

# 72. TTFT y TPOT son problemas diferentes

En modelos autoregresivos existen dos grandes fases:

```text
PREFILL
→ procesar input

DECODE
→ generar output token a token
```

Esto significa que:

- prompts enormes pueden afectar TTFT;
- respuestas enormes afectan decode y TPOT.

## Aplicación a prompts maestros

La longitud del prompt tiene un coste real.

No hay que conservar instrucciones inútiles “por si acaso”.

---

# 73. Existe un trade-off entre latencia y throughput

Procesar más solicitudes conjuntamente puede mejorar eficiencia y coste, pero puede aumentar cuánto espera cada usuario.

No existe una configuración universal.

Depende de:

- experiencia requerida;
- SLA;
- precio;
- volumen;
- hardware.

---

# 74. Prompt caching puede cambiar la economía de prompts grandes

Si muchas solicitudes comparten grandes prefijos:

```text
system prompt
documentación estable
few-shot examples
```

el caching puede evitar reprocesarlos completamente.

Esto hace especialmente importante estructurar prompts con bloques estables reutilizables.

---

# 75. La arquitectura debe crecer por necesidad, no por anticipación

El libro presenta una progresión desde la arquitectura más sencilla:

```text
USER
↓
MODEL
↓
RESPONSE
```

hacia sistemas con más capas.

Una evolución posible:

```text
1. modelo
2. context augmentation
3. guardrails
4. model router / gateway
5. cache
6. agent patterns
7. monitoring
```

## Principio

> **Añadir componentes cuando resuelvan un problema observado.**

Cada componente adicional crea:

- capacidad;
- complejidad;
- nuevos fallos.

---

# 76. Arquitectura de referencia práctica

Una arquitectura moderna puede verse así:

```text
                    ┌──────────────┐
                    │    USER      │
                    └──────┬───────┘
                           ↓
                  ┌────────────────┐
                  │ INPUT GUARDRAIL│
                  └──────┬─────────┘
                         ↓
                ┌───────────────────┐
                │ CONTEXT BUILDER   │
                │ RAG / APIs / DB   │
                └────────┬──────────┘
                         ↓
                 ┌───────────────┐
                 │ MODEL ROUTER  │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │ MODEL / AGENT │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │TOOLS / ACTIONS│
                 └───────┬───────┘
                         ↓
                ┌────────────────┐
                │OUTPUT GUARDRAIL│
                └───────┬────────┘
                        ↓
                    RESPONSE
```

Todo ello instrumentado mediante:

```text
logs
traces
metrics
evaluations
feedback
```

---

# 77. Los guardrails deben existir en varias partes del sistema

Puede haber controles sobre:

## Input

- prompt injection;
- PII;
- contenido no permitido;
- tamaño;
- estructura.

## Tool calls

- autorización;
- parámetros;
- permisos;
- límites.

## Output

- formato;
- seguridad;
- evidencia;
- datos sensibles.

No existe necesidad de que todos vivan en el mismo componente.

---

# 78. Model routing permite optimizar calidad, coste y latencia

No todas las solicitudes requieren el mismo modelo.

Un router puede decidir:

```text
simple → modelo barato
complejo → modelo potente
coding → modelo especializado
imagen → modelo multimodal
```

Esto permite construir un sistema heterogéneo.

## Aplicación

Un prompt maestro puede definir criterios de routing, pero la decisión crítica puede implementarse de forma determinista fuera del modelo cuando sea posible.

---

# 79. Un model gateway centraliza preocupaciones transversales

Un gateway puede encargarse de:

- autenticación;
- proveedores;
- retries;
- rate limits;
- logging;
- costes;
- fallback;
- políticas.

Esto evita repetir lógica en cada aplicación.

---

# 80. Cachear respuestas cuando el problema lo permita

Dos grandes enfoques:

## Exact caching

Misma entrada → reutilizar salida.

## Semantic caching

Entradas suficientemente similares → reutilizar resultado.

El caching puede reducir:

- coste;
- latencia;
- carga.

Pero requiere estudiar cuándo dos solicitudes son realmente equivalentes.

---

# 81. Observabilidad debe diseñarse desde el principio

No basta con saber que el sistema falló.

Un sistema observable debería permitir responder:

```text
¿Qué ocurrió?
¿Dónde?
¿Con qué prompt?
¿Con qué modelo?
¿Qué documentos recuperó?
¿Qué herramienta llamó?
¿Qué devolvió?
¿Qué versión estaba desplegada?
¿Cuánto costó?
¿Cuánto tardó?
```

---

# 82. Monitorizar fallos, no métricas por costumbre

No recopilar métricas solamente porque son estándar.

Primero:

```text
¿Cuáles son nuestros failure modes?
```

Después:

```text
¿Qué señales permiten detectarlos?
```

Ejemplo:

```text
RIESGO: alucinación
MÉTRICA: soporte de la respuesta en contexto

RIESGO: coste excesivo
MÉTRICA: tokens / request

RIESGO: RAG irrelevante
MÉTRICA: retrieval relevance

RIESGO: herramienta fallida
MÉTRICA: tool error rate
```

---

# 83. Evaluación y monitorización deben formar un ciclo

Los fallos detectados en producción deberían convertirse en nuevos tests.

```text
PRODUCCIÓN
↓
FALLO
↓
CASO DE EVALUACIÓN
↓
FIX
↓
REGRESSION TEST
↓
DEPLOY
```

Esto produce una suite cada vez más representativa.

---

# 84. User feedback es una fuente de datos

La interfaz conversacional permite recopilar señales como:

- correcciones;
- reformulaciones;
- abandono;
- regeneraciones;
- thumbs up/down;
- respuestas posteriores;
- acciones tomadas.

Pero hay que interpretar estas señales con cuidado.

---

# 85. Feedback explícito no siempre representa satisfacción real

Pocos usuarios proporcionan feedback.

Quienes lo hacen pueden no representar al conjunto de usuarios.

Además:

```text
sin queja ≠ éxito
```

Por eso conviene combinar:

- feedback explícito;
- comportamiento;
- métricas de tarea;
- evaluaciones.

---

# 86. Diseñar un data flywheel

Una aplicación madura puede crear este ciclo:

```text
USO REAL
↓
FEEDBACK
↓
CASOS DIFÍCILES
↓
DATOS
↓
EVALUACIÓN / FINE-TUNING / PROMPTS
↓
MEJOR SISTEMA
↓
MÁS USO
```

Esto puede constituir una ventaja competitiva mucho más fuerte que cambiar constantemente al modelo más nuevo.

---

# 87. Principio sistémico: resolver el problema en la capa correcta

Cuando aparece un fallo, preguntar primero dónde debería solucionarse.

Ejemplo:

```text
problema factual
→ RAG / fuente / verificación

problema de formato
→ constrained output / validator

problema de comportamiento
→ prompt / fine-tuning

problema determinista
→ código

problema de autorización
→ permisos del sistema

problema de coste
→ routing / cache / modelo menor

problema de seguridad
→ guardrails / arquitectura
```

## Regla

> **No utilizar prompt engineering para resolver problemas que pertenecen a otra capa.**

---

# 88. Marco para elegir técnica de adaptación

Antes de añadir complejidad:

```text
¿Puede resolverlo mejor una instrucción?
        ↓ no
¿Necesita información externa?
        ↓ sí → RAG / tools

¿Necesita comportamiento especializado persistente?
        ↓ sí → considerar fine-tuning

¿La tarea es determinista?
        ↓ sí → software tradicional

¿Necesita actuar en sistemas externos?
        ↓ sí → agente + controles
```

---

# 89. Orden de intervención recomendado

Como síntesis práctica del libro:

```text
1. DEFINIR PROBLEMA
2. DEFINIR EVALUACIÓN
3. ELEGIR MODELO BASE
4. CREAR PROMPT SIMPLE
5. AÑADIR CONTEXTO
6. AÑADIR RAG SI ES NECESARIO
7. AÑADIR HERRAMIENTAS
8. AÑADIR GUARDRAILS
9. OPTIMIZAR COSTE/LATENCIA
10. CONSIDERAR FINE-TUNING
11. MONITORIZAR PRODUCCIÓN
12. CONVERTIR FEEDBACK EN DATOS
13. ITERAR
```

El orden exacto puede variar, pero el principio es:

> **Empezar sencillo y complejizar solo cuando existe evidencia de que hace falta.**

---

# 90. Arquitectura recomendada para un prompt maestro

Aplicando las ideas del libro, un prompt maestro robusto puede estructurarse así:

```markdown
# 1. FUNCIÓN
Responsabilidad concreta del modelo.

# 2. OBJETIVO
Qué resultado debe conseguir.

# 3. DEFINICIÓN DE ÉXITO
Cómo saber si el trabajo es correcto.

# 4. CONTEXTO
Información necesaria para la tarea.

# 5. FUENTES
Qué fuentes puede utilizar y su prioridad.

# 6. RESTRICCIONES
Qué no debe hacer.

# 7. PROCEDIMIENTO
Proceso de alto nivel.

# 8. DESCOMPOSICIÓN
Subtareas cuando el problema lo requiera.

# 9. HERRAMIENTAS
Qué herramienta sirve para qué.

# 10. POLÍTICA DE HERRAMIENTAS
Cuándo leer, cuándo escribir y qué requiere autorización.

# 11. GESTIÓN DE INCERTIDUMBRE
Qué hacer si faltan datos.

# 12. OUTPUT CONTRACT
Formato exacto.

# 13. VALIDACIÓN
Comprobaciones antes de responder.

# 14. EJEMPLOS
Solo cuando aporten información útil.

# 15. FALLBACKS
Qué hacer cuando una etapa falla.
```

---

# 91. Añadir definición explícita de éxito

Muchos prompts especifican:

```text
haz X
```

pero no:

```text
X es correcto cuando...
```

Un prompt avanzado debería incluir criterios evaluables.

Ejemplo:

```markdown
## Criterios de éxito

La respuesta debe:
- responder completamente a la solicitud;
- separar hechos de inferencias;
- citar evidencia cuando exista;
- no inventar datos ausentes;
- cumplir el esquema de salida;
- señalar incertidumbre material.
```

---

# 92. Añadir una política de evidencia

Especialmente en RAG:

```text
afirmación
→ evidencia
```

Si no existe evidencia suficiente:

```text
indicar desconocimiento
```

en lugar de completar huecos.

Esto reduce el espacio permitido para alucinaciones.

---

# 93. Añadir una política de escalado de esfuerzo

Un prompt maestro puede diferenciar:

```text
TAREA SIMPLE
→ respuesta directa

TAREA MEDIA
→ análisis breve

TAREA COMPLEJA
→ descomponer + verificar

TAREA CON DATOS EXTERNOS
→ recuperar fuentes primero

TAREA DE ALTO RIESGO
→ exigir evidencia / confirmación
```

Esto evita utilizar el mismo workflow para todo.

---

# 94. Herramientas como capacidades explícitas

En lugar de decir simplemente:

```text
"usa herramientas si hace falta"
```

definir:

```markdown
## Política de herramientas

- Búsqueda: para información actual o desconocida.
- Archivos: para responder sobre documentos del usuario.
- Código: para cálculos y transformaciones deterministas.
- APIs: para datos autoritativos.
```

La descripción debe enseñar:

```text
CUÁNDO
POR QUÉ
QUÉ ESPERAR
```

---

# 95. Preferir evidencia externa a introspección

Si algo puede verificarse mediante:

- código;
- búsqueda;
- base de datos;
- archivo;
- test;

es preferible comprobarlo a pedir al modelo que simplemente “esté seguro”.

## Principio

```text
VERIFICACIÓN EXTERNA > CONFIANZA DECLARADA
```

---

# 96. Antipatrón: solucionar todo añadiendo texto al prompt

Ejemplos de problemas que probablemente necesiten otra capa:

```text
"El modelo inventa precios."
→ fuente de datos / RAG

"El JSON a veces se rompe."
→ constrained output / parser

"Ejecuta acciones incorrectas."
→ permisos / validación

"Es demasiado caro."
→ routing / caching / modelo menor

"No sabemos si mejoró."
→ evaluación

"No sabemos qué falló."
→ observabilidad
```

---

# 97. Antipatrón: aumentar contexto sin evaluar relevancia

Ventanas de contexto enormes pueden tentar a:

```text
meterlo todo
```

Pero más información puede significar:

- más coste;
- mayor latencia;
- ruido;
- distracciones;
- conflictos.

El contexto debe construirse.

No simplemente acumularse.

---

# 98. Antipatrón: utilizar fine-tuning para conocimiento cambiante

Si la información cambia continuamente, incorporarla mediante fine-tuning puede resultar:

- lenta;
- cara;
- difícil de actualizar.

Retrieval suele ser más apropiado para conocimiento dinámico.

---

# 99. Antipatrón: construir un agente cuando un workflow basta

Si una secuencia es conocida:

```text
A → B → C
```

un workflow determinista suele ser:

- más controlable;
- más barato;
- más depurable.

Utilizar planificación autónoma cuando realmente existe incertidumbre sobre qué pasos realizar.

---

# 100. Antipatrón: evaluar únicamente la respuesta final

Para sistemas compuestos hay que evaluar:

```text
retrieval
routing
tool selection
tool arguments
intermediate outputs
final output
latency
cost
```

La evaluación end-to-end es necesaria, pero insuficiente para depurar.

---

# 101. Antipatrón: depender de un único score

Un sistema puede tener:

```text
alta precisión
pero
latencia inaceptable

o

alta satisfacción
pero
mucha alucinación

o

alta seguridad
pero
demasiados falsos rechazos
```

Por tanto, la evaluación debe ser multidimensional.

---

# 102. Antipatrón: cambiar modelo sin regression tests

Una nueva versión puede:

- mejorar razonamiento;
- empeorar formato;
- cambiar estilo;
- romper herramientas;
- reaccionar distinto a prompts.

Cada actualización debería pasar la misma suite antes de producción.

---

# 103. Antipatrón: prompts sin propietario ni versión

Si no sabes:

```text
quién cambió un prompt
qué versión está desplegada
qué aplicaciones dependen de ella
qué evaluación pasó
```

el sistema será difícil de mantener.

---

# 104. Qué merece la pena absorber permanentemente

Si hubiera que reducir todo el libro a un conjunto de principios duraderos, conservaría estos:

1. **Optimiza el sistema, no únicamente el modelo.**
2. **Define el problema antes de seleccionar tecnología.**
3. **La evaluación debe existir desde el principio.**
4. **Utiliza métricas exactas cuando sean posibles.**
5. **AI-as-a-judge ayuda, pero necesita validación.**
6. **Los benchmarks públicos no sustituyen una evaluación propia.**
7. **La claridad del prompt importa, pero el contexto importa tanto como la instrucción.**
8. **Descompón tareas complejas cuando mejore observabilidad y fiabilidad.**
9. **Versiona prompts y evalúalos sistemáticamente.**
10. **No intentes resolver seguridad únicamente mediante prompts.**
11. **La calidad de RAG depende principalmente del retrieval.**
12. **Compara sparse, dense e híbrido antes de elegir.**
13. **Evalúa retrieval y generation por separado.**
14. **Construir contexto es una forma de feature engineering.**
15. **Las herramientas determinan la capacidad y el riesgo del agente.**
16. **Más autonomía exige más controles.**
17. **Fine-tuning debería justificar su coste frente a prompting/RAG.**
18. **RAG y fine-tuning resuelven problemas diferentes y pueden combinarse.**
19. **Calidad y cobertura de datos importan tanto como cantidad.**
20. **Los datos sintéticos necesitan verificación.**
21. **Latencia y coste forman parte de la calidad.**
22. **La longitud del prompt tiene un coste operativo.**
23. **Añade componentes arquitectónicos solo cuando solucionen un problema real.**
24. **Diseña observabilidad antes de tener incidentes.**
25. **Convierte fallos de producción en regression tests.**
26. **Utiliza feedback real para alimentar un data flywheel.**
27. **Resuelve cada problema en la capa adecuada.**
28. **Un buen sistema combina componentes probabilísticos con controles deterministas.**

---

# 105. Checklist para revisar un sistema LLM

## Problema

- [ ] ¿Existe una necesidad clara?
- [ ] ¿IA es realmente apropiada?
- [ ] ¿Está definido el nivel de autonomía?
- [ ] ¿Está definido qué ocurre cuando falla?

## Modelo

- [ ] ¿El modelo tiene capacidad suficiente?
- [ ] ¿Existe una alternativa más pequeña/barata?
- [ ] ¿Se controlan los parámetros de sampling?
- [ ] ¿Las actualizaciones están versionadas?

## Prompt

- [ ] ¿La instrucción es explícita?
- [ ] ¿El objetivo está separado del contexto?
- [ ] ¿El output está especificado?
- [ ] ¿Los ejemplos son necesarios?
- [ ] ¿El prompt está versionado?
- [ ] ¿Existe una suite para evaluarlo?

## Contexto / RAG

- [ ] ¿El sistema recupera información relevante?
- [ ] ¿Se ha probado un baseline lexical?
- [ ] ¿Embeddings aportan una mejora real?
- [ ] ¿El chunking está justificado?
- [ ] ¿Existe reranking?
- [ ] ¿Retrieval se evalúa independientemente?

## Agentes

- [ ] ¿Cada herramienta es necesaria?
- [ ] ¿Las descripciones son claras?
- [ ] ¿Lectura y escritura están diferenciadas?
- [ ] ¿Acciones peligrosas requieren validación?
- [ ] ¿Se detectan loops?
- [ ] ¿Existe límite de pasos/coste?
- [ ] ¿Las trayectorias se registran?

## Fine-tuning

- [ ] ¿Se agotaron primero alternativas más simples?
- [ ] ¿Existe suficiente data de calidad?
- [ ] ¿Se evalúan regresiones?
- [ ] ¿La mejora justifica mantenimiento adicional?

## Datos

- [ ] ¿Son relevantes?
- [ ] ¿Están alineados?
- [ ] ¿Son consistentes?
- [ ] ¿Tienen cobertura?
- [ ] ¿Hay duplicados?
- [ ] ¿Se verifican datos sintéticos?
- [ ] ¿Cumplen políticas y privacidad?

## Evaluación

- [ ] ¿Hay evaluación offline?
- [ ] ¿Existen tests funcionales?
- [ ] ¿Hay casos límite?
- [ ] ¿Se evalúan componentes?
- [ ] ¿Se evalúa end-to-end?
- [ ] ¿Los jueces automáticos están calibrados?
- [ ] ¿Las métricas conectan con negocio?

## Producción

- [ ] ¿Se mide coste?
- [ ] ¿Se mide TTFT?
- [ ] ¿Se mide latencia completa?
- [ ] ¿Existe caching cuando tiene sentido?
- [ ] ¿Existe routing?
- [ ] ¿Existen retries y fallbacks?

## Seguridad

- [ ] ¿Se han modelado amenazas?
- [ ] ¿Hay input guardrails?
- [ ] ¿Hay output guardrails?
- [ ] ¿Hay permisos de herramienta?
- [ ] ¿Se prueban ataques?
- [ ] ¿Se mide false refusal además de violation rate?

## Observabilidad

- [ ] ¿Se guarda modelo y versión?
- [ ] ¿Se guarda prompt y versión?
- [ ] ¿Se guarda contexto recuperado?
- [ ] ¿Se registran tool calls?
- [ ] ¿Existen traces?
- [ ] ¿Los fallos alimentan la suite de evaluación?

---

# 106. Plantilla operativa para futuros proyectos

```markdown
# AI SYSTEM SPEC

## 1. PROBLEMA
Qué necesidad real se intenta resolver.

## 2. ÉXITO
Métricas de producto y técnicas.

## 3. RIESGOS
Principales failure modes y coste del error.

## 4. MODELO
Modelo seleccionado y razón.

## 5. PROMPT
Instrucciones estables y versionadas.

## 6. CONTEXT ENGINEERING
Fuentes, retrieval y estrategia de selección.

## 7. TOOLS
Herramientas disponibles y permisos.

## 8. WORKFLOW / AGENT
Secuencia determinista o política de planificación.

## 9. OUTPUT CONTRACT
Formato y validación.

## 10. GUARDRAILS
Protecciones de input, herramientas y output.

## 11. EVALUATION
Datasets, criterios, métricas y baselines.

## 12. PERFORMANCE
Coste, TTFT, TPOT, throughput y caching.

## 13. OBSERVABILITY
Logs, traces, alertas y debugging.

## 14. FEEDBACK
Señales de usuario y data flywheel.

## 15. RELEASE
Regression tests y criterios de despliegue.
```

---

# 107. Cómo cambia este libro nuestra forma de crear prompts maestros

Los dos errores más frecuentes al crear un prompt maestro son:

```text
1. creer que todo debe solucionarse dentro del prompt;
2. creer que cuanto más completo sea el prompt, mejor será el sistema.
```

La perspectiva de *AI Engineering* sugiere algo más sofisticado.

El prompt maestro debería ser únicamente la parte del sistema que corresponde a:

- instrucciones;
- contexto operativo;
- política de herramientas;
- criterios;
- contratos de salida;
- gestión de incertidumbre.

Otros problemas deberían delegarse a:

```text
RAG
validators
código
herramientas
permisos
routers
guardrails
evaluadores
monitorización
```

Por tanto:

> **El mejor prompt maestro no es el que intenta hacerlo todo. Es el que encaja limpiamente dentro de una arquitectura bien diseñada.**

---

# 108. Síntesis final

*AI Engineering* aporta una perspectiva particularmente valiosa porque conecta técnicas que a menudo se estudian por separado.

La cadena completa es:

```text
PROBLEMA
   ↓
EVALUACIÓN
   ↓
MODELO
   ↓
PROMPT
   ↓
CONTEXTO / RAG
   ↓
HERRAMIENTAS / AGENTES
   ↓
FINE-TUNING CUANDO SEA NECESARIO
   ↓
DATOS
   ↓
INFERENCIA EFICIENTE
   ↓
ARQUITECTURA DE PRODUCCIÓN
   ↓
OBSERVABILIDAD
   ↓
FEEDBACK
   ↓
NUEVA EVALUACIÓN
```

La gran lección es que los foundation models deben tratarse como **componentes probabilísticos dentro de sistemas de ingeniería**.

No basta con que el modelo sea inteligente.

Un producto robusto necesita:

- contexto correcto;
- instrucciones claras;
- datos adecuados;
- herramientas limitadas;
- evaluación fiable;
- controles deterministas;
- seguridad;
- observabilidad;
- eficiencia;
- feedback.

Y, sobre todo:

> **Cada nueva capa de sofisticación debe justificar su existencia mediante una mejora observable del sistema.**

Ese principio debería guiar tanto la construcción de aplicaciones con LLMs como la creación y revisión de cualquier prompt maestro avanzado.
