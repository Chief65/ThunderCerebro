# Principios clave de *Prompt Engineering for LLMs*

**Libro analizado:** *Prompt Engineering for LLMs: The Art and Science of Building Large Language Model-Based Applications*  
**Autores:** John Berryman y Albert Ziegler  
**Editorial:** O’Reilly Media  
**Objetivo de este documento:** condensar las ideas más útiles, duraderas y aplicables del libro, especialmente para diseñar prompts maestros, sistemas de prompting, agentes y aplicaciones basadas en LLMs.

> Este documento no pretende sustituir al libro ni resumirlo página por página. Se centra en los principios que merece la pena conservar y reutilizar.

---

# 1. Idea central del libro

La idea más importante es que **prompt engineering no consiste únicamente en redactar mejor una pregunta**.

Un prompt forma parte de un sistema que transforma:

1. una necesidad del usuario;
2. en una representación textual que el modelo pueda procesar;
3. acompañada del contexto adecuado;
4. con instrucciones y estructura suficientes;
5. para obtener una salida útil;
6. que posteriormente pueda ser validada, interpretada o convertida en una acción.

Por tanto:

> **Prompt engineering = ingeniería de la interacción completa entre usuario, aplicación, contexto, modelo, herramientas y evaluación.**

Esta idea cambia la forma de diseñar prompts avanzados.

En lugar de preguntarse solamente:

> “¿Cómo redacto esta instrucción?”

conviene preguntarse:

> “¿Qué información necesita realmente el modelo, cómo debo estructurarla, qué debe ignorar, qué herramientas puede usar, qué salida necesito y cómo voy a comprobar que el resultado es correcto?”

---

# 2. Modelo mental fundamental: un LLM continúa texto

Uno de los principios recurrentes del libro es recordar qué hace realmente un modelo de lenguaje.

Un LLM genera texto token a token buscando continuaciones plausibles según los patrones aprendidos durante su entrenamiento y posterior alineamiento.

Aunque un modelo moderno parezca:

- conversar;
- razonar;
- programar;
- buscar información;
- usar herramientas;
- analizar documentos;
- ejecutar flujos de trabajo;

en el fondo sigue operando sobre una representación textual y produciendo una continuación condicionada por su contexto.

## Consecuencia práctica

Al construir un prompt, no hay que pensar únicamente:

> “¿Qué le ordenaría a una persona?”

También hay que pensar:

> “¿Qué contexto textual hace que la continuación correcta sea la continuación más natural?”

Este principio explica por qué funcionan tan bien:

- formatos familiares;
- documentos bien estructurados;
- ejemplos;
- encabezados;
- conversaciones coherentes;
- esquemas;
- delimitadores;
- plantillas;
- salidas claramente especificadas.

---

# 3. Utilizar formatos que el modelo ya reconoce

El libro defiende repetidamente que resulta más fácil obtener comportamientos predecibles cuando el prompt adopta patrones que el modelo ya conoce.

Ejemplos:

- Markdown;
- JSON;
- YAML;
- tablas;
- informes;
- conversaciones;
- especificaciones;
- preguntas y respuestas;
- documentación técnica;
- código;
- listas de requisitos.

## Principio operativo

> **No inventar una gramática innecesariamente exótica cuando existe un formato estándar conocido.**

Un prompt bien diseñado debería parecerse a un documento coherente, no a una acumulación arbitraria de instrucciones.

Por ejemplo, es preferible:

```markdown
## Objetivo

## Contexto

## Restricciones

## Procedimiento

## Formato de salida
```

a una sucesión desordenada de instrucciones mezcladas con datos y excepciones.

---

# 4. Diseñar el prompt como una arquitectura, no como un bloque de texto

Para prompts complejos conviene pensar en **elementos independientes**.

Un prompt maestro puede dividirse, por ejemplo, en:

```text
IDENTIDAD / FUNCIÓN
OBJETIVO
CONTEXTO
FUENTES
REGLAS
RESTRICCIONES
PROCESO
CRITERIOS DE CALIDAD
HERRAMIENTAS
FORMATO DE SALIDA
CASOS ESPECIALES
EJEMPLOS
VALIDACIÓN
```

Cada elemento debería existir por una razón concreta.

Esto permite:

- modificar una parte sin reescribir todo;
- eliminar redundancias;
- detectar contradicciones;
- controlar el presupuesto de contexto;
- evaluar qué instrucciones realmente mejoran el resultado.

---

# 5. Claridad del problema antes que complejidad del prompt

Una idea especialmente importante del libro es que **clarificar la tarea** suele ser más valioso que añadir instrucciones sofisticadas.

Un modelo necesita comprender:

- qué problema debe resolver;
- qué constituye una respuesta correcta;
- qué información puede utilizar;
- qué debe evitar;
- qué nivel de detalle se espera;
- qué formato debe devolver.

La ambigüedad produce variabilidad.

La claridad produce consistencia.

## Aplicación

Antes de añadir nuevas reglas a un prompt, comprobar:

1. ¿Está definido con precisión el objetivo?
2. ¿Hay varios objetivos mezclados?
3. ¿Puede una instrucción interpretarse de dos maneras?
4. ¿Está claro qué tiene prioridad?
5. ¿Está claro cuándo la tarea se considera terminada?

---

# 6. Separar contenido estático y contenido dinámico

El libro distingue dos grandes tipos de información.

## Contenido estático

Permanece relativamente constante entre ejecuciones.

Ejemplos:

- función del modelo;
- reglas;
- criterios;
- instrucciones;
- metodología;
- estructura de salida;
- ejemplos generales.

## Contenido dinámico

Depende de la tarea concreta.

Ejemplos:

- archivos del usuario;
- código;
- resultados de búsqueda;
- conversación actual;
- información recuperada mediante RAG;
- datos de APIs;
- estado de una aplicación.

## Principio operativo

No convertir información dinámica en reglas permanentes.

Y no repetir información estática en múltiples lugares si puede existir una única fuente de verdad.

Una arquitectura limpia suele parecerse a:

```text
[INSTRUCCIONES ESTABLES]

[CONTEXTO DE LA TAREA ACTUAL]

[DATOS / FUENTES RECUPERADAS]

[PETICIÓN DEL USUARIO]

[FORMATO DE RESPUESTA]
```

---

# 7. El contexto debe seleccionarse, no acumularse

Una ventana de contexto grande no implica que debamos llenarla.

El libro insiste en que introducir información irrelevante puede perjudicar el resultado aunque todavía quede espacio disponible.

Por tanto, el proceso correcto es aproximadamente:

```text
RECUPERAR
   ↓
FRAGMENTAR
   ↓
PUNTUAR / PRIORIZAR
   ↓
FILTRAR
   ↓
ORDENAR
   ↓
ENSAMBLAR
```

## 7.1 Recuperar

Encontrar información potencialmente relevante.

## 7.2 Fragmentar

Dividir documentos grandes en fragmentos suficientemente específicos.

## 7.3 Priorizar

Determinar qué información aporta más valor para la pregunta actual.

## 7.4 Filtrar

Eliminar ruido, duplicados o contexto marginal.

## 7.5 Ordenar

Colocar cada pieza donde tenga sentido semántico.

## 7.6 Ensamblar

Construir finalmente el prompt dentro del presupuesto disponible.

---

# 8. Relevancia supera a volumen

Una regla práctica derivada del libro:

> **Más contexto no significa necesariamente más conocimiento útil.**

Un prompt enorme puede:

- diluir instrucciones importantes;
- introducir información contradictoria;
- aumentar latencia;
- incrementar coste;
- dificultar que el modelo identifique qué es relevante;
- hacer menos reproducible el comportamiento.

Por eso, al optimizar prompts maestros, hay que buscar **densidad informativa**, no longitud.

Cada sección debería justificar sus tokens.

---

# 9. Importancia, posición y dependencia son conceptos distintos

El libro propone pensar en varias relaciones entre elementos del prompt.

## Posición

Dónde debe aparecer una información.

Ejemplo:

- una conclusión no debería aparecer antes de los datos que la sustentan;
- los eventos cronológicos deberían conservar su secuencia.

## Importancia

Cuánto valor aporta una pieza de información.

Una instrucción puede ser extremadamente importante aunque aparezca al principio.

## Dependencia

Una pieza puede necesitar otra para tener sentido.

Ejemplo:

```text
A: El proyecto utiliza Next.js 16.
B: Usa el App Router para implementar la nueva ruta.
```

B depende parcialmente de A.

## Aplicación a prompts maestros

Al construir un prompt largo, no ordenar simplemente por el orden en que se escribieron las reglas.

Ordenar por:

1. función lógica;
2. dependencia;
3. prioridad;
4. relevancia.

---

# 10. Tratar el contexto como un presupuesto

El prompt tiene recursos limitados:

- tokens;
- atención;
- tiempo;
- coste;
- complejidad.

Conviene tratar cada fragmento como si tuviera:

```text
valor
relevancia
coste en tokens
prioridad
dependencias
```

La construcción del prompt se convierte así en un pequeño problema de optimización:

> incluir la combinación de información que maximiza la utilidad sin introducir ruido innecesario.

---

# 11. Los ejemplos son extremadamente potentes

El libro destaca el valor del **few-shot prompting**.

Un ejemplo puede enseñar simultáneamente:

- interpretación;
- estilo;
- estructura;
- nivel de detalle;
- formato;
- criterios implícitos.

En muchas situaciones, mostrar un patrón resulta más eficaz que describirlo durante varios párrafos.

## Pero los ejemplos tienen riesgos

### 11.1 Consumen contexto

Cada ejemplo ocupa tokens.

### 11.2 Introducen sesgos

El modelo puede copiar características accidentales del ejemplo.

### 11.3 Pueden crear patrones falsos

Si todos los ejemplos comparten accidentalmente una propiedad, el modelo puede interpretar esa propiedad como una regla.

## Principio operativo

Usar ejemplos cuando realmente enseñen algo difícil de expresar con instrucciones.

No utilizarlos como decoración.

---

# 12. Los ejemplos deben representar diversidad real

Cuando se utilicen ejemplos, conviene incluir:

- caso normal;
- caso límite;
- entrada incompleta;
- entrada ambigua;
- situación que debe rechazarse;
- ejemplo donde falte información;
- ejemplo con salida especialmente estructurada.

Esto reduce la posibilidad de que el modelo aprenda una regla accidental.

---

# 13. Retrieval-Augmented Generation: aportar conocimiento externo

El libro presenta RAG como una arquitectura para incorporar información que no está disponible de forma fiable en los pesos del modelo.

El flujo esencial es:

```text
pregunta
   ↓
recuperación
   ↓
selección de fragmentos
   ↓
contexto
   ↓
modelo
   ↓
respuesta
```

## Usos

Especialmente útil para:

- documentación privada;
- información reciente;
- manuales;
- bases de conocimiento;
- archivos del usuario;
- documentación técnica;
- repositorios;
- información empresarial.

## Lección fundamental

No pedir al modelo que “recuerde” información que puede proporcionársele directamente.

---

# 14. Retrieval y summarization resuelven problemas diferentes

El libro distingue implícitamente dos operaciones importantes.

## Retrieval

Hace zoom **hacia dentro**.

Selecciona pequeñas partes de un conjunto enorme.

## Summarization

Hace zoom **hacia fuera**.

Reduce una gran cantidad de información a una representación compacta.

Ambas pueden combinarse.

Ejemplo:

```text
100 documentos
      ↓
retrieval
      ↓
12 fragmentos relevantes
      ↓
resumen
      ↓
contexto compacto
```

---

# 15. Resumen jerárquico para cantidades enormes de información

Cuando un documento supera ampliamente la ventana disponible:

```text
documento
   ↓
secciones
   ↓
resúmenes de sección
   ↓
resúmenes de bloques
   ↓
resumen global
```

Este enfoque evita intentar comprimir todo en una única llamada.

También introduce una idea útil para prompts maestros:

> **Los problemas grandes deben descomponerse antes de pedir una respuesta global.**

---

# 16. Diseñar también la salida, no solamente la entrada

Un prompt profesional debe especificar cómo debe ser una buena respuesta.

Esto puede incluir:

- formato;
- secciones;
- granularidad;
- campos obligatorios;
- longitud aproximada;
- nivel técnico;
- criterios de calidad;
- qué información debe omitirse;
- cómo representar incertidumbre.

Ejemplo:

```markdown
## Formato de salida

Devuelve:

1. Diagnóstico
2. Evidencia
3. Severidad
4. Recomendación
5. Cambio mínimo propuesto
6. Riesgos
```

El modelo tiene mucha más facilidad para producir una salida útil cuando conoce exactamente la estructura esperada.

---

# 17. Hacer reconocibles el inicio y el final de la respuesta

Para aplicaciones programáticas conviene que la respuesta sea fácil de identificar y parsear.

Ejemplos:

- JSON válido;
- XML delimitado;
- una sección Markdown concreta;
- campos explícitos;
- un esquema de salida.

Una salida ambigua obliga posteriormente a utilizar heurísticas frágiles.

## Regla

> Cuando la salida vaya a ser consumida por software, debe diseñarse primero para máquinas y después para humanos.

---

# 18. Evitar preámbulos y epílogos innecesarios

Los modelos conversacionales tienden a producir texto social como:

- introducciones;
- confirmaciones;
- explicaciones previas;
- conclusiones repetitivas.

En una aplicación, esos tokens pueden ser:

- innecesarios;
- caros;
- difíciles de parsear;
- generadores de latencia.

Si una salida debe ser estructurada, indicarlo explícitamente.

Ejemplo:

```text
Devuelve únicamente el objeto JSON final.
No añadas comentarios antes ni después.
```

---

# 19. Chat sigue siendo una estructura de contexto

El salto de “completion” a “chat” no elimina las ideas anteriores.

Una conversación puede verse como un documento estructurado con distintos participantes.

Esto permite diseñar la interacción como si fuese una obra:

- sistema/desarrollador → define reglas y escenario;
- usuario → plantea la necesidad;
- asistente → responde;
- herramientas → aportan observaciones externas.

## Consecuencia

Los roles no deberían mezclarse arbitrariamente.

La información debe colocarse en el lugar que represente correctamente su naturaleza.

---

# 20. No confundir la conversación visible con el contexto interno

Una aplicación puede contener información que el usuario nunca escribió literalmente.

Por ejemplo:

```text
Usuario:
"¿Puedes corregir este archivo?"

Contexto interno:
- archivo actual
- framework
- versión
- errores del compilador
- convenciones del repositorio
```

El sistema necesita transformar la petición humana en un contexto mucho más completo.

Este principio es central para agentes y asistentes profesionales.

---

# 21. Herramientas: menos es normalmente mejor

Cuando un modelo puede utilizar herramientas, el libro recomienda limitar la cantidad disponible simultáneamente.

Demasiadas herramientas producen:

- confusión;
- selección incorrecta;
- mayor superficie de error;
- más tokens;
- herramientas redundantes.

## Diseño recomendado

Las herramientas deberían:

- cubrir claramente el dominio;
- evitar solapamientos;
- tener nombres autoexplicativos;
- utilizar pocos parámetros;
- definir claramente qué hacen;
- devolver solamente información relevante.

---

# 22. Una herramienta debe ser fácil de comprender

Una definición de herramienta debe responder claramente:

```text
¿Qué hace?
¿Cuándo debo usarla?
¿Qué argumentos necesita?
¿Qué devuelve?
¿Qué errores pueden ocurrir?
```

Evitar descripciones estilo contrato legal.

Si una API real es enorme, es preferible exponer al modelo una interfaz simplificada que una copia completa de la API.

---

# 23. Los nombres forman parte del prompt

Nombres de:

- herramientas;
- funciones;
- parámetros;
- campos;
- variables;

influyen en la comprensión del modelo.

Preferir:

```text
searchDocumentation
repositoryName
startDate
```

frente a nombres ambiguos como:

```text
run
data
arg1
x
```

La semántica del nombre funciona como información adicional.

---

# 24. Las salidas de herramientas también necesitan diseño

No basta con definir bien la entrada.

La información devuelta por una herramienta debe ser:

- relevante;
- compacta;
- comprensible;
- coherente con su definición.

Evitar devolver enormes estructuras “por si acaso”.

El exceso de datos externos puede distraer al modelo exactamente igual que el exceso de contexto en el prompt.

---

# 25. Los errores deben ayudar al modelo a recuperarse

Un error útil debe explicar:

- qué ocurrió;
- qué entrada era incorrecta;
- qué puede cambiarse;
- si tiene sentido volver a intentarlo.

Ejemplo malo:

```text
ERROR 422
```

Ejemplo mejor:

```text
No se encontró el repositorio solicitado.
El argumento repository debe contener owner/repository.
```

Esto permite que el agente corrija su siguiente acción.

---

# 26. Nunca confiar únicamente en una instrucción para acciones peligrosas

Uno de los principios de ingeniería más importantes del libro:

> Las acciones irreversibles o de alto impacto deben protegerse en la capa de aplicación.

No basta con escribir:

```text
Antes de borrar algo, pide permiso.
```

El modelo puede equivocarse.

La aplicación debería interceptar operaciones sensibles y solicitar confirmación de forma determinista.

Ejemplos:

- eliminar datos;
- realizar pagos;
- enviar mensajes;
- publicar contenido;
- modificar producción;
- ejecutar cambios irreversibles.

---

# 27. Separar razonamiento de acción

Para tareas complejas resulta útil permitir un ciclo del tipo:

```text
observar
   ↓
analizar
   ↓
decidir
   ↓
usar herramienta
   ↓
observar resultado
   ↓
continuar
```

El libro conecta esta arquitectura con enfoques de razonamiento y acción como ReAct.

La idea duradera no es una sintaxis concreta, sino:

> **Los problemas multietapa se resuelven mejor mediante iteraciones de información y acción que mediante una única generación gigante.**

---

# 28. Descomponer trabajos complejos en tareas pequeñas

El libro dedica un capítulo entero a workflows.

Una tarea grande debería transformarse en unidades con:

- entrada definida;
- objetivo definido;
- salida definida;
- criterios de éxito definidos.

Ejemplo:

```text
OBJETIVO GRANDE
    ↓
investigar
    ↓
clasificar
    ↓
analizar
    ↓
generar propuesta
    ↓
verificar
    ↓
formatear resultado
```

Esto mejora:

- fiabilidad;
- trazabilidad;
- evaluación;
- depuración;
- reutilización.

---

# 29. No utilizar un LLM cuando software determinista funciona mejor

Este es otro principio especialmente valioso.

Los LLMs son:

- probabilísticos;
- más caros;
- más lentos;
- menos predecibles.

Si una tarea puede resolverse perfectamente mediante:

- una expresión regular;
- un parser;
- una consulta SQL;
- una función;
- una API;
- una regla determinista;
- un algoritmo clásico;

normalmente debería utilizarse esa solución.

## Regla práctica

> **Usar el LLM para ambigüedad, lenguaje y juicio; usar software tradicional para lógica determinista.**

---

# 30. Preferir workflows deterministas antes que agentes completamente autónomos

Según el libro, proporcionar más autonomía aumenta flexibilidad pero también:

- imprevisibilidad;
- dificultad de depuración;
- errores;
- complejidad de evaluación.

Por tanto, el orden recomendable es:

```text
1. Software determinista
2. Workflow determinista con algunas tareas LLM
3. Workflow dirigido parcialmente por LLM
4. Agente altamente autónomo
```

Escalar hacia mayor autonomía solamente cuando exista una razón real.

---

# 31. Evaluar tareas individualmente

Cuando un workflow falla, resulta mucho más sencillo localizar el problema si cada tarea tiene sus propias pruebas.

Para cada módulo:

```text
entrada
↓
resultado esperado
↓
resultado obtenido
↓
evaluación
```

No esperar a evaluar solamente el resultado global.

---

# 32. La evaluación debe existir desde el principio

El libro considera la evaluación como parte central del desarrollo.

Optimizar un prompt mediante intuición solamente produce mejoras difíciles de demostrar.

Un ciclo correcto es:

```text
hipótesis
   ↓
cambio de prompt
   ↓
suite de ejemplos
   ↓
medición
   ↓
comparación
   ↓
decisión
```

---

# 33. Mantener una suite de ejemplos

Una práctica recomendada es disponer de un conjunto representativo de entradas.

Debe contener:

- casos normales;
- casos frecuentes;
- extremos;
- entradas ambiguas;
- casos problemáticos;
- fallos históricos.

Cuando se modifica el prompt:

```text
Prompt A → suite
Prompt B → misma suite
```

y se comparan resultados.

Esto convierte el prompt engineering en una disciplina reproducible.

---

# 34. Tres grandes tipos de evaluación offline

El libro presenta tres enfoques principales.

## Gold standard

Comparar con una respuesta conocida.

Adecuado cuando existe una salida correcta clara.

## Testing funcional

Comprobar propiedades objetivas.

Ejemplos:

- JSON parseable;
- código que compila;
- función existente;
- argumentos válidos;
- esquema correcto.

## Evaluación mediante LLM

Útil cuando la calidad es semántica y difícil de medir mediante reglas exactas.

Debe hacerse con criterios cuidadosamente definidos.

---

# 35. SOMA: una buena estructura para evaluadores LLM

El libro propone una metodología denominada **SOMA**:

- **S — Specific questions**
- **O — Ordinal scaled answers**
- **MA — Multi-aspect coverage**

En términos prácticos:

## Preguntas específicas

En vez de:

```text
¿Es buena esta respuesta?
```

usar:

```text
¿La respuesta aborda explícitamente el requisito X?
```

## Escala ordinal

En vez de solo sí/no:

```text
1 = incumple completamente
2 = incumple parcialmente
3 = aceptable
4 = bueno
5 = excelente
```

## Varios aspectos

Evaluar por separado:

- exactitud;
- cobertura;
- relevancia;
- formato;
- seguridad;
- claridad.

Esto reduce la ambigüedad del evaluador.

---

# 36. La evaluación online completa la evaluación offline

Una respuesta puede comportarse bien en laboratorio y mal con usuarios reales.

El libro recomienda observar métricas reales como:

1. feedback directo;
2. corrección funcional;
3. aceptación por parte del usuario;
4. impacto conseguido;
5. métricas incidentales como latencia.

## Lección

No confundir “al usuario le gustó” con “la tarea produjo el resultado correcto”.

Ambas cosas pueden medirse de forma independiente.

---

# 37. Optimizar varias dimensiones, no una sola

Un prompt puede mejorar precisión y empeorar:

- latencia;
- coste;
- longitud;
- estabilidad;
- tasa de errores.

Por tanto, la calidad debería verse como algo multidimensional.

Ejemplo:

```text
Calidad =
    precisión
  + cumplimiento
  + robustez
  + consistencia
  + utilidad
  - coste
  - latencia
  - errores
```

No hace falta utilizar literalmente esta fórmula; sirve como modelo mental.

---

# 38. Ideas del libro que conviene tratar como dependientes de época

Algunas secciones describen APIs, modelos y limitaciones concretas del periodo en que fue escrito el libro.

Estas ideas sirven como contexto histórico, pero no deben convertirse automáticamente en reglas permanentes:

- nombres concretos de modelos;
- versiones específicas de APIs;
- limitaciones antiguas de context window;
- detalles concretos de esquemas de function calling;
- comportamiento exacto de modelos de 2023;
- frameworks específicos;
- recomendaciones ligadas a implementaciones de aquella generación.

## Qué conservar

Conservar el principio subyacente.

Por ejemplo:

```text
NO:
"El modelo X soporta exactamente este modificador."

SÍ:
"Verifica qué partes del esquema de herramientas entiende realmente el modelo actual."
```

---

# 39. Marco práctico para construir un prompt maestro

A partir de los principios del libro, una arquitectura robusta podría ser:

```markdown
# 1. FUNCIÓN
Quién es el sistema y qué responsabilidad tiene.

# 2. OBJETIVO
Resultado final que debe conseguir.

# 3. ALCANCE
Qué entra y qué no entra en la tarea.

# 4. CONTEXTO
Información necesaria para entender el problema.

# 5. FUENTES
Qué información puede utilizar y con qué prioridad.

# 6. REGLAS
Comportamientos obligatorios.

# 7. RESTRICCIONES
Acciones o conclusiones que deben evitarse.

# 8. METODOLOGÍA
Proceso general para resolver la tarea.

# 9. HERRAMIENTAS
Cuándo usar cada herramienta y qué propósito tiene.

# 10. GESTIÓN DE INCERTIDUMBRE
Qué hacer si falta información o existen contradicciones.

# 11. CRITERIOS DE CALIDAD
Propiedades que debe cumplir una buena respuesta.

# 12. FORMATO DE SALIDA
Estructura exacta de la respuesta.

# 13. EJEMPLOS
Solo cuando aporten patrones difíciles de especificar.

# 14. VALIDACIÓN FINAL
Comprobaciones antes de entregar la respuesta.
```

---

# 40. Jerarquía recomendada dentro de un prompt maestro

Una buena jerarquía debe distinguir entre:

## Nivel 1 — objetivo

Qué debe conseguirse.

## Nivel 2 — invariantes

Reglas que nunca deberían incumplirse.

## Nivel 3 — proceso

Cómo abordar normalmente el problema.

## Nivel 4 — criterios

Cómo distinguir una buena respuesta de una mediocre.

## Nivel 5 — contexto

Datos concretos de la ejecución actual.

## Nivel 6 — presentación

Cómo entregar el resultado.

Esto evita que reglas críticas queden enterradas dentro de detalles secundarios.

---

# 41. Principio de mínima instrucción suficiente

No incluir una regla únicamente porque “quizá ayude”.

Cada regla adicional:

- compite por atención;
- puede interactuar con otras;
- introduce nuevas posibilidades de contradicción;
- aumenta coste y mantenimiento.

Proceso recomendado:

```text
añadir regla
↓
evaluar
↓
¿mejora resultados?
  ├─ sí → mantener
  └─ no → eliminar
```

---

# 42. Evitar contradicciones

Los prompts maestros suelen deteriorarse cuando se van acumulando instrucciones con el tiempo.

Ejemplo:

```text
Sé extremadamente conciso.
```

y más adelante:

```text
Explica exhaustivamente todos los detalles.
```

Ambas pueden tener sentido en contextos distintos, pero necesitan una condición.

Mejor:

```text
Por defecto, responde de forma concisa.
Cuando el usuario solicite un análisis exhaustivo, prioriza profundidad sobre brevedad.
```

---

# 43. Las excepciones necesitan condiciones explícitas

Evitar:

```text
Nunca hagas X.
También puedes hacer X si es necesario.
```

Preferir:

```text
No hagas X salvo cuando se cumpla alguna de estas condiciones:
1. ...
2. ...
```

Las reglas condicionales son mucho más fáciles de interpretar.

---

# 44. Diseñar comportamiento ante información insuficiente

Un prompt profesional debería definir qué ocurre cuando:

- falta contexto;
- una fuente no está disponible;
- los datos se contradicen;
- una herramienta falla;
- no existe suficiente evidencia;
- el usuario pide algo fuera de alcance.

Una política útil puede ser:

```text
1. No inventar datos.
2. Utilizar primero las fuentes disponibles.
3. Diferenciar hechos de inferencias.
4. Indicar explícitamente incertidumbre material.
5. Solicitar información adicional solo cuando sea imprescindible.
```

---

# 45. Diseñar para fallos

No asumir que todo funcionará en el camino ideal.

Preguntar:

- ¿Qué pasa si retrieval devuelve cero resultados?
- ¿Qué pasa si aparecen fuentes contradictorias?
- ¿Qué pasa si una herramienta falla?
- ¿Qué pasa si la salida no cumple el esquema?
- ¿Qué pasa si la entrada es enorme?
- ¿Qué pasa si una tarea se repite sin progreso?

Un sistema robusto incluye estrategias de recuperación.

---

# 46. El prompt debe poder evolucionar

Un prompt maestro debería tratarse como software:

```text
versionar
probar
medir
refactorizar
documentar
comparar
```

No como un texto sagrado que nunca se modifica.

Idealmente:

```text
v1
↓
suite de evaluación
↓
hallazgos
↓
v2
↓
regresión
↓
comparación
```

---

# 47. Principios que merece la pena “absorber” permanentemente

Si hubiera que reducir todo el libro a unas pocas reglas de trabajo, conservaría estas:

1. **Un LLM genera continuaciones condicionadas por contexto.**
2. **Prompt engineering es ingeniería de sistemas, no solo redacción.**
3. **Clarifica primero el problema.**
4. **Utiliza formatos familiares y estructuras previsibles.**
5. **Separa instrucciones de contexto dinámico.**
6. **Introduce solo información relevante.**
7. **Prioriza contexto en lugar de acumularlo.**
8. **Utiliza ejemplos para enseñar patrones, no para rellenar espacio.**
9. **Diseña explícitamente la salida esperada.**
10. **Mantén simples las herramientas y sus interfaces.**
11. **Protege acciones sensibles fuera del modelo.**
12. **Descompón problemas complejos en tareas pequeñas.**
13. **Utiliza software determinista cuando sea suficiente.**
14. **Prefiere workflows controlados antes que autonomía innecesaria.**
15. **Evalúa cada cambio con ejemplos representativos.**
16. **Mide varias dimensiones: precisión, utilidad, coste, latencia y estabilidad.**
17. **Diseña mecanismos de recuperación ante fallos.**
18. **Refactoriza prompts igual que refactorizarías código.**

---

# 48. Checklist para revisar un prompt avanzado

## Problema

- [ ] ¿El objetivo está perfectamente definido?
- [ ] ¿Está claro qué significa “éxito”?
- [ ] ¿El alcance está delimitado?

## Contexto

- [ ] ¿Toda la información incluida es relevante?
- [ ] ¿Existe información duplicada?
- [ ] ¿Hay datos contradictorios?
- [ ] ¿El contexto dinámico está separado de las instrucciones?

## Instrucciones

- [ ] ¿Las reglas críticas son fáciles de encontrar?
- [ ] ¿Existen contradicciones?
- [ ] ¿Hay reglas redundantes?
- [ ] ¿Las excepciones están condicionadas explícitamente?

## Ejemplos

- [ ] ¿Cada ejemplo enseña algo necesario?
- [ ] ¿Hay diversidad suficiente?
- [ ] ¿Alguna característica accidental podría convertirse en un patrón falso?

## Herramientas

- [ ] ¿Cada herramienta tiene una finalidad única?
- [ ] ¿Los nombres son autoexplicativos?
- [ ] ¿Los argumentos son simples?
- [ ] ¿Las respuestas contienen solo información útil?
- [ ] ¿Los errores permiten recuperación?
- [ ] ¿Las acciones sensibles tienen confirmación externa?

## Salida

- [ ] ¿El formato está definido?
- [ ] ¿Puede parsearse de forma estable?
- [ ] ¿Se evita texto innecesario?
- [ ] ¿Se especifica cómo expresar incertidumbre?

## Evaluación

- [ ] ¿Existe una suite de casos?
- [ ] ¿Incluye casos límite?
- [ ] ¿Puede compararse contra la versión anterior?
- [ ] ¿Se miden calidad, coste y latencia?
- [ ] ¿Se revisan regresiones?

---

# 49. Antipatrones a evitar

## Antipatrón 1 — Prompt kilométrico sin jerarquía

Mucho texto no equivale a buenas instrucciones.

## Antipatrón 2 — Repetir la misma regla diez veces

La repetición puede introducir inconsistencias y gastar contexto.

## Antipatrón 3 — Confiar en “actúa como experto” como sustituto de especificaciones

El rol ayuda, pero no reemplaza criterios, contexto ni formato.

## Antipatrón 4 — Meter todos los documentos disponibles

Retrieval debe seleccionar, no volcar.

## Antipatrón 5 — Utilizar un agente para operaciones deterministas

Si una función normal resuelve el problema, usar la función.

## Antipatrón 6 — Dar acceso directo a acciones peligrosas

La autorización debe implementarse fuera del modelo.

## Antipatrón 7 — Modificar prompts sin evaluación

Sin una suite, no se sabe si el cambio mejoró realmente el sistema.

## Antipatrón 8 — Añadir reglas para arreglar cada fallo aislado

Primero hay que identificar la causa raíz:

- problema de contexto;
- ambigüedad;
- ejemplo incorrecto;
- herramienta mal definida;
- modelo inadecuado;
- output mal especificado.

---

# 50. Síntesis final

El aprendizaje más importante del libro puede resumirse así:

> **No intentes controlar un LLM mediante una montaña de instrucciones. Construye un entorno textual y operacional en el que producir la respuesta correcta sea el comportamiento más natural, fácil y verificable.**

Un buen prompt maestro no es el que contiene más reglas.

Es el que:

- representa correctamente el problema;
- proporciona exactamente el contexto necesario;
- elimina ambigüedad;
- organiza prioridades;
- utiliza herramientas simples;
- descompone tareas complejas;
- especifica salidas;
- anticipa fallos;
- y dispone de un mecanismo de evaluación.

Ese enfoque convierte el prompt engineering de ensayo y error en una disciplina de ingeniería.

---

# 51. Cómo aplicar estas ideas a futuros prompts maestros

Cuando revise o construya un prompt maestro, estas ideas deberían traducirse en el siguiente proceso:

```text
1. Entender el objetivo real.
2. Identificar entradas, fuentes y restricciones.
3. Eliminar reglas redundantes o contradictorias.
4. Separar instrucciones estables y contexto dinámico.
5. Definir una jerarquía clara.
6. Elegir formatos familiares.
7. Diseñar retrieval/contexto solo si aporta valor.
8. Añadir ejemplos únicamente cuando enseñen un patrón útil.
9. Diseñar herramientas pequeñas y semánticamente claras.
10. Descomponer tareas grandes.
11. Definir el formato exacto de salida.
12. Añadir validación y manejo de errores.
13. Construir casos de prueba.
14. Comparar versiones.
15. Mantener únicamente las instrucciones que produzcan mejoras verificables.
```

---

## Nota final

Este documento separa deliberadamente los **principios duraderos** de los detalles tecnológicos concretos del periodo del libro. APIs, modelos, ventanas de contexto y mecanismos de tool calling evolucionan rápidamente; los principios de claridad, selección de contexto, modularidad, seguridad y evaluación son mucho más estables.
