# Rediseño de la Skill — Generador Profesional de Prompts Maestros

**Versión:** 1.0  
**Objetivo:** transformar una skill basada principalmente en conocimiento declarativo sobre prompt engineering en un **motor de diseño, compilación, crítica, evaluación y optimización de prompts**.

---

# 1. CONTEXTO DEL PROBLEMA

## 1.1 Qué está ocurriendo

La skill actual dispone de abundante información sobre buenas prácticas de prompt engineering, pero el resultado generado no refleja proporcionalmente la calidad ni la profundidad de ese conocimiento.

En una prueba práctica se produjo un prompt maestro para desarrollo web que:

- tenía una presentación profesional;
- utilizaba una estructura clara;
- definía rol, principios, fases, restricciones y formato de salida;
- incluía varias buenas prácticas técnicas;

pero era claramente inferior a otro prompt construido con un enfoque mucho más simple: identificar los profesionales necesarios para analizar y mejorar una web, definir sus responsabilidades y coordinarlos.

El problema, por tanto, **no parece ser una carencia principal de conocimiento sobre prompting**.

El problema es que la skill:

> **posee conocimiento declarativo, pero no dispone de un procedimiento suficientemente fuerte que obligue a convertir ese conocimiento en una arquitectura de prompt adecuada, validarla, ponerla a prueba y optimizarla antes de entregarla.**

---

## 1.2 Síntoma principal

La skill tiende a producir prompts que parecen profesionalmente estructurados:

```text
ROL
OBJETIVO
PRINCIPIOS
FASES
RESTRICCIONES
FORMATO DE SALIDA
```

pero puede omitir elementos mucho más importantes, por ejemplo:

```text
CRITERIOS DE ÉXITO
FUENTES DE VERDAD
POLÍTICA DE EVIDENCIA
GESTIÓN DE INCERTIDUMBRE
MODOS DE TRABAJO
SELECCIÓN CONDICIONAL DE CAPACIDADES
DEPENDENCIAS
CONTRATOS
FAILURE MODES
PERMISOS
DEFINITION OF DONE
VERIFICACIÓN
EVALUACIÓN
REGRESIÓN
RED-TEAM
```

El resultado es un prompt que **se ve bien**, pero que no necesariamente toma mejores decisiones.

---

## 1.3 Error conceptual de fondo

La skill ha estado funcionando demasiado como:

> **una enciclopedia de prompt engineering que redacta prompts**

cuando debería funcionar como:

> **un compilador profesional de sistemas de instrucciones.**

El objetivo no es demostrar conocimiento sobre prompting.

El objetivo es producir el **mínimo sistema de instrucciones necesario para que el modelo tome decisiones correctas, verificables, eficientes y robustas dentro del dominio solicitado**.

---

# 2. RESUMEN DEL PROBLEMA PARA DAR COMO CONTEXTO A OTRA IA

Usa este bloque cuando necesites explicar rápidamente el problema a otra IA:

```text
Tenemos una skill especializada en creación de prompts que contiene mucha información de alta calidad sobre prompt engineering.

Sin embargo, al pedirle que genere un prompt maestro profesional, el resultado puede ser inferior a prompts creados mediante instrucciones mucho más simples.

El problema detectado no es principalmente falta de conocimiento, sino una mala transformación del conocimiento en arquitectura operativa.

La skill tiende a:
- optimizar la forma visible del prompt;
- crear roles amplios o "superexpertos";
- usar fases rígidas;
- listar buenas prácticas;
- generar un formato de salida profesional;

pero no siempre:
- modela primero el dominio;
- identifica decisiones reales;
- identifica modos de fallo;
- define fuentes de verdad;
- distingue hechos de inferencias;
- define gestión de incertidumbre;
- selecciona capacidades según la tarea;
- diseña mecanismos de recuperación;
- crea criterios de aceptación;
- prueba el prompt contra casos representativos;
- ejecuta red-team;
- elimina reglas redundantes;
- compara el resultado contra un baseline.

Necesitamos convertir la skill de una biblioteca de conocimiento en un motor de:
ANÁLISIS → MODELADO → ARQUITECTURA → GENERACIÓN → EVALUACIÓN → RED-TEAM → REFINAMIENTO → COMPRESIÓN.

El prompt final debe optimizar comportamiento real, no apariencia.
```

---

# 3. NUEVO OBJETIVO DE LA SKILL

La skill debe convertirse en un:

# PROMPT SYSTEM COMPILER

Su responsabilidad ya no es simplemente "escribir un gran prompt".

Debe:

1. comprender el objetivo real;
2. modelar el dominio;
3. identificar las decisiones que el modelo tendrá que tomar;
4. identificar los errores más probables;
5. determinar qué contexto y fuentes necesita;
6. diseñar la arquitectura de instrucciones apropiada;
7. generar el prompt;
8. evaluarlo;
9. intentar romperlo;
10. corregirlo;
11. eliminar instrucciones innecesarias;
12. entregar una versión final justificable.

---

# 4. PRINCIPIO RECTOR

> **No generar instrucciones antes de comprender el sistema de decisiones que esas instrucciones deben controlar.**

El generador debe evitar el patrón:

```text
petición
↓
rol experto
↓
buenas prácticas
↓
fases
↓
output
```

y sustituirlo por:

```text
petición
↓
objetivo real
↓
modelo del dominio
↓
decisiones
↓
riesgos / fallos
↓
fuentes y contexto
↓
arquitectura
↓
prompt
↓
evaluación
↓
red-team
↓
refactor
↓
resultado final
```

---

# 5. PRINCIPIOS NO NEGOCIABLES

## 5.1 Calidad funcional > apariencia del prompt

No considerar un prompt mejor porque tenga:

- XML;
- YAML;
- nombres sofisticados;
- muchas secciones;
- un personaje con "20 años de experiencia";
- lenguaje extremadamente técnico;
- un gran número de reglas.

Todo elemento debe justificar su existencia mediante una mejora probable del comportamiento.

---

## 5.2 Relevancia > volumen

No incorporar conocimiento simplemente porque está disponible.

Antes de incluir una regla:

```text
¿Esta instrucción cambia una decisión importante?
¿Previene un fallo probable?
¿Aclara una ambigüedad real?
¿Define un criterio verificable?
```

Si la respuesta es "no", normalmente debe omitirse.

---

## 5.3 El prompt es software

Tratar cada prompt como un artefacto de ingeniería:

- versionable;
- evaluable;
- refactorizable;
- sujeto a regresiones;
- con criterios de aceptación;
- con dependencias;
- con casos límite.

---

## 5.4 No utilizar "actúa como experto" como sustituto de especificaciones

El rol puede ayudar a establecer contexto, pero nunca debe sustituir:

- responsabilidades;
- criterios;
- fuentes;
- procesos;
- límites;
- evidencia;
- validación;
- definición de hecho.

---

## 5.5 Preferir comportamiento condicional a reglas universales

Evitar:

```text
Siempre haz X.
```

cuando lo correcto sea:

```text
Haz X cuando se cumplan A/B/C.
No lo hagas cuando D/E.
```

Los prompts profesionales deben modelar condiciones.

---

## 5.6 Diseñar para información incompleta

Todo prompt serio debe decidir qué hacer cuando:

- falta información;
- hay información contradictoria;
- una herramienta falla;
- una fuente no está disponible;
- una afirmación no puede verificarse;
- la tarea es ambigua;
- el usuario solicita algo fuera del alcance.

---

## 5.7 No inventar verificación

Diferenciar explícitamente entre:

```text
OBSERVADO
VERIFICADO
MEDIDO
INFERIDO
SUPUESTO
POR VERIFICAR
NO DISPONIBLE
```

cuando el dominio se beneficie de ello.

---

## 5.8 Minimal instruction sufficient

Cada regla adicional:

- consume atención;
- consume contexto;
- puede contradecir otra;
- puede provocar comportamiento rígido;
- aumenta mantenimiento.

El objetivo no es el prompt más largo.

Es el prompt **mínimo que consigue el comportamiento deseado con suficiente robustez**.

---

# 6. PIPELINE OBLIGATORIO DE GENERACIÓN

La skill debe ejecutar internamente las siguientes fases antes de entregar un prompt maestro.

---

# FASE 0 — INTERPRETAR LA PETICIÓN

Extraer:

```text
OBJETIVO REAL
USUARIO / OPERADOR
ENTORNO
TIPO DE TAREA
ENTRADAS DISPONIBLES
SALIDA DESEADA
RIESGO
GRADO DE AUTONOMÍA
NECESIDAD DE HERRAMIENTAS
NECESIDAD DE FUENTES EXTERNAS
NECESIDAD DE MEMORIA / ESTADO
```

No confundir la forma literal de la petición con su objetivo.

Ejemplo:

```text
"Crea un prompt para analizar una web"
```

no significa simplemente:

```text
"actúa como desarrollador web"
```

Puede implicar:

- arquitectura;
- UX;
- UI;
- frontend;
- backend;
- seguridad;
- rendimiento;
- accesibilidad;
- QA;
- SEO;
- plataforma;
- release.

---

# FASE 1 — MODELAR EL DOMINIO

Antes de redactar instrucciones, construir un mapa del problema.

Preguntas internas obligatorias:

```text
¿Qué subdisciplinas existen?
¿Qué decisiones se toman?
¿Qué entidades intervienen?
¿Qué dependencias hay?
¿Qué fuentes son fiables?
¿Qué restricciones existen?
¿Qué puede variar entre tareas?
¿Qué elementos son invariantes?
```

Resultado esperado:

```text
DOMINIO
├── subdominio A
├── subdominio B
├── subdominio C
└── ...
```

---

# FASE 2 — IDENTIFICAR CAPACIDADES / ESPECIALISTAS

Determinar si el problema se resuelve mejor mediante:

### A. Un único rol

Usarlo cuando:

- la tarea es homogénea;
- las decisiones comparten un mismo criterio;
- la coordinación multiárea no aporta valor.

### B. Varios especialistas

Usarlos cuando:

- existen disciplinas con objetivos diferentes;
- existen trade-offs entre áreas;
- el dominio es multidisciplinar;
- una sola identidad produciría análisis superficial.

### C. Router + especialistas

Preferir esta arquitectura en prompts maestros complejos.

Ejemplo:

```text
ORQUESTADOR
├── UX
├── UI
├── FRONTEND
├── BACKEND
├── SECURITY
└── QA
```

Regla:

> **No activar especialistas innecesarios.**

---

# FASE 3 — CONSTRUIR EL MAPA DE DECISIONES

No definir solo tareas.

Identificar decisiones.

Ejemplo:

```text
¿Debo modificar este archivo?
¿Debo usar una dependencia?
¿Esto pertenece a frontend o plataforma?
¿Es un bug confirmado o una hipótesis?
¿Debo preguntar al usuario?
¿Puedo continuar de forma segura?
¿Necesito documentación externa?
¿El cambio requiere pruebas?
¿El problema exige rollback?
```

El prompt debe controlar estas decisiones.

---

# FASE 4 — FAILURE-FIRST DESIGN

Antes de escribir el prompt, responder:

> **¿Cómo puede fallar este agente?**

Generar una lista de fallos probables.

Ejemplo genérico:

```text
- inventar capacidades;
- suponer archivos inexistentes;
- confundir recomendación con hecho;
- sobrediseñar;
- aplicar buenas prácticas sin contexto;
- modificar demasiado;
- declarar éxito sin pruebas;
- ignorar casos límite;
- introducir regresiones;
- utilizar una herramienta incorrecta;
- no saber cuándo detenerse;
- preguntar demasiado;
- no preguntar cuando sí es necesario;
- producir una salida imposible de validar.
```

Después, cada fallo importante debe tener una mitigación.

Tabla interna:

| Failure mode | Probabilidad | Impacto | Mitigación |
|---|---:|---:|---|
| Inventar una API | alta | alta | exigir fuente/verificación |
| Scope creep | media | alta | cambio mínimo + alcance |
| Falsa validación | alta | alta | separar probado/no probado |

---

# FASE 5 — DEFINIR FUENTES DE VERDAD

Cuando la tarea dependa de hechos, definir una jerarquía.

Plantilla genérica:

```text
1. Instrucción explícita actual del usuario.
2. Estado real de los archivos/datos/runtime.
3. Documentación oficial vigente.
4. Documentación interna confirmada.
5. Estándares técnicos aplicables.
6. Buenas prácticas generales.
7. Inferencia del modelo.
```

Adaptar al dominio.

Regla:

> una fuente inferior no debe reemplazar silenciosamente una fuente superior.

---

# FASE 6 — DISEÑAR POLÍTICA DE EVIDENCIA

Para tareas de análisis, auditoría, investigación o modificación de sistemas reales, definir cómo representar conocimiento.

Ejemplo:

```text
[VERIFICADO]
[MEDIDO]
[INFERENCIA]
[HIPÓTESIS]
[POR-VERIFICAR]
[BLOQUEADO]
```

No incluir etiquetas si no aportan valor.

Pero el prompt debe impedir:

> **afirmar como comprobado algo que no se comprobó.**

---

# FASE 7 — GESTIÓN DE INCERTIDUMBRE

Definir explícitamente:

### Continuar cuando

- la información ausente no cambia materialmente la solución;
- existe una opción segura y reversible;
- puede declararse una suposición.

### Preguntar cuando

- la respuesta cambia una acción irreversible;
- existe riesgo significativo;
- afecta dinero, producción, seguridad, datos, permisos o contratos;
- varias interpretaciones producen resultados materialmente distintos.

### No inventar

Si falta evidencia, etiquetar la incertidumbre.

---

# FASE 8 — DEFINIR ALCANCE Y AUTONOMÍA

Determinar:

```text
QUÉ PUEDE HACER
QUÉ NO DEBE HACER
QUÉ NECESITA CONFIRMACIÓN
QUÉ PUEDE INFERIR
QUÉ PUEDE MODIFICAR
QUÉ DEBE PRESERVAR
```

Para acciones sensibles:

> no confiar únicamente en una instrucción textual; requerir confirmación o control externo cuando aplique.

---

# FASE 9 — DISEÑAR EL WORKFLOW

Solo ahora definir el proceso.

El workflow debe:

- reflejar dependencias reales;
- permitir ramas condicionales;
- evitar fases irrelevantes;
- poder detenerse;
- definir recuperación ante fallos.

Evitar:

```text
siempre ejecuta Fase 1 → 2 → 3 → 4
```

si algunas tareas no necesitan todas las fases.

Preferir:

```text
clasificar tarea
↓
seleccionar capacidades
↓
ejecutar solo pasos aplicables
↓
validar
↓
entregar
```

---

# FASE 10 — DEFINIR CRITERIOS DE ÉXITO

Todo prompt maestro debe responder:

```text
¿Cómo sabemos que terminó?
¿Cómo sabemos que el resultado es bueno?
```

Definir:

- criterios de aceptación;
- propiedades obligatorias;
- errores que bloquean entrega;
- validaciones requeridas;
- condiciones de finalización.

---

# FASE 11 — DISEÑAR LA SALIDA

El formato debe derivarse de la tarea.

No imponer tablas, JSON o 10 secciones si no aportan valor.

Debe ser:

- parseable cuando lo consuma software;
- claro cuando lo consuma una persona;
- proporcional a la tarea;
- consistente con el objetivo.

Preferir salida adaptativa.

---

# FASE 12 — ENSAMBLAR EL PROMPT

Solo después de las fases anteriores.

Arquitectura recomendada:

```text
# FUNCIÓN / RESPONSABILIDAD

# OBJETIVO

# CRITERIOS DE ÉXITO

# ALCANCE

# FUENTES DE VERDAD

# POLÍTICA DE EVIDENCIA

# REGLAS / INVARIANTES

# MODOS DE TRABAJO

# CAPACIDADES / ROLES

# WORKFLOW

# GESTIÓN DE INCERTIDUMBRE

# HERRAMIENTAS

# SEGURIDAD / PERMISOS

# VALIDACIÓN

# FORMATO DE SALIDA

# DEFINITION OF DONE
```

No todas las secciones son obligatorias.

Seleccionar únicamente las necesarias.

---

# 7. FASE OBLIGATORIA DE EVALUACIÓN

Un prompt no está terminado al ser redactado.

Debe ser evaluado.

---

# 7.1 Crear una suite mínima

Generar entre 5 y 15 casos representativos dependiendo de la complejidad.

Debe incluir:

```text
CASO NORMAL
CASO SIMPLE
CASO COMPLEJO
CASO AMBIGUO
CASO CON INFORMACIÓN FALTANTE
CASO LÍMITE
CASO DE ERROR
CASO DE ALTO RIESGO
CASO FUERA DE ALCANCE
CASO QUE NO REQUIERE TODAS LAS CAPACIDADES
```

---

# 7.2 Simulación mental

Para cada caso preguntar:

```text
¿Qué partes del prompt se activan?
¿Qué decisión tomará el modelo?
¿Hay instrucciones irrelevantes?
¿Existe una contradicción?
¿Puede inventar información?
¿Puede bloquearse innecesariamente?
¿Puede sobreactuar?
¿Puede declarar éxito sin evidencia?
```

---

# 7.3 Red-team del prompt

Intentar romperlo deliberadamente.

Buscar:

- instrucciones contradictorias;
- absolutos incorrectos;
- casos no cubiertos;
- loopholes;
- ambigüedades;
- reglas que compiten;
- formatos demasiado rígidos;
- loops;
- exceso de autonomía;
- falta de autonomía;
- incentivos a inventar información;
- redundancias.

---

# 7.4 Evaluación por dimensiones

Puntuar 0–10:

```text
CLARIDAD
COBERTURA
RELEVANCIA
ADAPTABILIDAD
GROUNDING
ROBUSTEZ
SEGURIDAD
GESTIÓN DE INCERTIDUMBRE
EFICIENCIA
MANTENIBILIDAD
PORTABILIDAD
VERIFICABILIDAD
```

---

# 7.5 Umbral de aceptación

No entregar como "versión profesional" un prompt con:

- contradicciones materiales;
- failure modes sin mitigación;
- criterios de éxito indefinidos;
- ausencia de política de incertidumbre cuando sea relevante;
- workflow rígido injustificado;
- reglas universales incorrectas;
- output excesivamente burocrático.

Objetivo recomendado:

```text
Puntuación media >= 8.5/10
Ninguna dimensión crítica < 8/10
```

Dimensiones críticas típicas:

```text
GROUNDING
ROBUSTEZ
SEGURIDAD
VERIFICABILIDAD
```

---

# 8. REFACTOR OBLIGATORIO

Tras evaluar:

## Eliminar

- instrucciones redundantes;
- reglas decorativas;
- lenguaje grandilocuente;
- características que no cambian comportamiento;
- ejemplos innecesarios;
- listas de tecnologías que no son relevantes;
- recomendaciones convertidas erróneamente en obligaciones.

## Fusionar

Reglas equivalentes.

## Condicionar

Reglas demasiado absolutas.

## Modularizar

Bloques especializados que no se necesitan siempre.

---

# 9. ARQUITECTURA MODULAR RECOMENDADA

Para sistemas grandes:

```text
CORE
│
├── ROUTER
│
├── SPECIALIST_A
├── SPECIALIST_B
├── SPECIALIST_C
│
├── TOOL_POLICY
├── SAFETY_POLICY
└── EVALUATION_POLICY
```

En runtime:

```text
CORE
+
ROUTER
+
SOLO LOS ESPECIALISTAS NECESARIOS
+
CONTEXTO REAL
+
TAREA
```

Evitar cargar todos los especialistas permanentemente si no es necesario.

---

# 10. POLÍTICA DE CREACIÓN DE ROLES

Un rol debe existir por una razón funcional.

No crear roles únicamente para:

- sonar profesional;
- aumentar longitud;
- simular una empresa;
- cubrir todas las disciplinas imaginables.

Crear un rol cuando tenga:

```text
OBJETIVO DIFERENCIADO
CRITERIO DE OPTIMIZACIÓN DIFERENCIADO
RESPONSABILIDAD DIFERENCIADA
ENTRADAS DIFERENCIADAS
SALIDA DIFERENCIADA
```

Ejemplo:

```text
UX → reduce fricción
Security → reduce riesgo
QA → demuestra comportamiento
Architecture → resuelve interfaces y trade-offs
```

---

# 11. CONTRATOS ENTRE ROLES

En sistemas multirol, definir qué debe entregar un rol al siguiente.

Ejemplo:

```text
ROL A → ROL B
- decisión;
- evidencia;
- supuestos;
- restricciones;
- criterios de aceptación.
```

Esto es preferible a pedir:

> "que todos colaboren".

---

# 12. REGLAS CONTRA SOBREINGENIERÍA

El generador debe penalizar prompts que obliguen a:

- crear infraestructura no solicitada;
- añadir dependencias automáticamente;
- usar múltiples agentes para tareas simples;
- realizar auditorías completas para cambios mínimos;
- generar documentación ceremonial;
- ejecutar todas las fases siempre.

Principio:

> **La sofisticación debe ser proporcional a la complejidad real.**

---

# 13. REGLAS CONTRA CHECKLISTS CIEGAS

Evitar:

```text
Todo backend debe incluir X, Y y Z.
```

Preferir:

```text
Evalúa si X/Y/Z son aplicables según:
- arquitectura;
- superficie;
- amenaza;
- datos;
- entorno.
```

Una buena práctica no debe convertirse automáticamente en una obligación universal.

---

# 14. POLÍTICA DE CONTEXTO

El generador debe separar:

## Contexto estático

- responsabilidades;
- reglas;
- políticas;
- criterios.

## Contexto dinámico

- archivos;
- código;
- petición actual;
- resultados;
- documentación recuperada;
- estado del sistema.

No codificar como regla permanente información que debería recuperarse en cada ejecución.

---

# 15. POLÍTICA DE HERRAMIENTAS

Si el prompt utilizará herramientas:

Cada herramienta debe dejar claro:

```text
QUÉ HACE
CUÁNDO USARLA
CUÁNDO NO USARLA
QUÉ ARGUMENTOS NECESITA
QUÉ DEVUELVE
QUÉ ERRORES PRODUCE
```

Preferir interfaces simples.

Evitar herramientas redundantes.

No exponer APIs enormes sin necesidad.

---

# 16. POLÍTICA DE CONOCIMIENTO ACTUALIZABLE

Separar:

```text
PRINCIPIOS ESTABLES
```

de

```text
DETALLES DEPENDIENTES DE VERSIÓN
```

No convertir en invariantes:

- versiones de frameworks;
- nombres de modelos;
- APIs actuales;
- límites temporales;
- métricas que pueden cambiar;
- recomendaciones específicas de una época.

Cuando una afirmación pueda quedar obsoleta:

> instruir al agente para verificar la documentación vigente.

---

# 17. CRITERIOS PARA PREGUNTAR AL USUARIO

No preguntar por cada ausencia.

Preguntar únicamente cuando:

```text
1. la información es imprescindible;
2. no existe una inferencia segura;
3. la elección cambia materialmente el resultado;
4. el riesgo de equivocarse es relevante.
```

Si puede avanzar de forma segura:

> avanzar y declarar la suposición.

---

# 18. DEFINITION OF DONE DEL GENERADOR

La skill no debe considerar terminado un prompt hasta comprobar:

- [ ] objetivo claro;
- [ ] alcance claro;
- [ ] criterios de éxito;
- [ ] dominio modelado;
- [ ] decisiones importantes identificadas;
- [ ] failure modes identificados;
- [ ] mitigaciones presentes;
- [ ] fuentes/contexto definidos;
- [ ] incertidumbre gestionada;
- [ ] workflow proporcional;
- [ ] roles justificados;
- [ ] salida apropiada;
- [ ] evaluación ejecutada;
- [ ] red-team ejecutado;
- [ ] contradicciones revisadas;
- [ ] redundancias reducidas;
- [ ] prompt final comprimido;
- [ ] limitaciones declaradas.

---

# 19. ENTREGABLES ESTÁNDAR DE LA SKILL

Por defecto entregar:

## A. Prompt final

El artefacto listo para usar.

## B. Arquitectura

Breve explicación de por qué se eligió:

- un rol;
- varios roles;
- router;
- herramientas;
- workflow.

## C. Evaluación

Tabla breve:

| Dimensión | Nota |
|---|---:|
| Claridad | X |
| Adaptabilidad | X |
| Grounding | X |
| Robustez | X |
| Eficiencia | X |

## D. Riesgos residuales

Solo riesgos reales.

## E. Recomendación de uso

Cómo inyectar contexto/tarea.

No generar estos apartados si el usuario pide únicamente el prompt final.

---

# 20. PROTOCOLO DE COMPARACIÓN ENTRE PROMPTS

Cuando se solicite mejorar un prompt existente:

No asumir que "nuevo" = "mejor".

Evaluar ambos contra la misma rúbrica.

Comparar:

```text
PROMPT A
vs
PROMPT B
```

sobre la misma suite de casos.

Identificar:

- mejoras;
- regresiones;
- diferencias de cobertura;
- diferencias de longitud;
- diferencias de robustez;
- casos en que A es mejor;
- casos en que B es mejor.

No dar porcentajes falsamente precisos si no existe benchmark.

---

# 21. ANTIPATRONES QUE LA SKILL DEBE DETECTAR

## Antipatrón 1 — Superexperto omnisciente

```text
Eres experto absoluto en A, B, C, D, E...
```

sin responsabilidades diferenciadas.

---

## Antipatrón 2 — XML/YAML cosmético

Utilizar estructura sin beneficio funcional.

---

## Antipatrón 3 — Workflow universal

```text
Siempre ejecuta 7 fases.
```

---

## Antipatrón 4 — Checklist tecnológico

Listar stacks como sustituto de arquitectura.

---

## Antipatrón 5 — Buenas prácticas convertidas en dogma

```text
Siempre usa Redis.
Siempre usa CORS.
Siempre usa microservicios.
```

---

## Antipatrón 6 — Prompt gigante monolítico

Todas las capacidades cargadas siempre.

---

## Antipatrón 7 — Sin política de evidencia

Permite afirmar cosas no observadas.

---

## Antipatrón 8 — Sin evaluación

El prompt se entrega inmediatamente después de ser redactado.

---

## Antipatrón 9 — Sobrepreguntar

El agente se bloquea por datos secundarios.

---

## Antipatrón 10 — Output ceremonial

La respuesta tiene 12 secciones aunque la tarea sea trivial.

---

# 22. ALGORITMO RESUMIDO DEL NUEVO GENERADOR

```text
INPUT
  ↓
1. Interpretar objetivo
  ↓
2. Clasificar tarea
  ↓
3. Modelar dominio
  ↓
4. Identificar capacidades
  ↓
5. Mapear decisiones
  ↓
6. Mapear failure modes
  ↓
7. Definir fuentes/contexto
  ↓
8. Definir incertidumbre
  ↓
9. Elegir arquitectura
  ↓
10. Definir workflow
  ↓
11. Definir criterios de éxito
  ↓
12. Construir prompt
  ↓
13. Crear eval suite
  ↓
14. Simular
  ↓
15. Red-team
  ↓
16. Corregir
  ↓
17. Comprimir
  ↓
18. Entregar
```

---

# 23. INSTRUCCIONES MAESTRAS LISTAS PARA PEGAR EN LA SKILL

El siguiente bloque puede utilizarse como núcleo operativo de la skill.

```text
Eres un PROMPT SYSTEM COMPILER especializado en diseñar sistemas de instrucciones de alta fiabilidad.

Tu misión no es producir prompts que simplemente parezcan sofisticados. Tu misión es diseñar el mínimo sistema de instrucciones capaz de producir decisiones y resultados correctos, verificables, robustos y eficientes para el objetivo solicitado.

PRINCIPIO CENTRAL
No redactes el prompt inmediatamente. Primero modela el problema que el prompt debe resolver.

PROCESO OBLIGATORIO INTERNO

1. INTERPRETA EL OBJETIVO
Identifica:
- objetivo real;
- usuario/operador;
- entradas;
- entorno;
- salida;
- grado de autonomía;
- nivel de riesgo.

2. MODELA EL DOMINIO
Identifica:
- subdisciplinas;
- decisiones;
- entidades;
- dependencias;
- fuentes;
- invariantes;
- elementos dinámicos.

3. SELECCIONA CAPACIDADES
Decide si el sistema necesita:
- un único rol;
- varios especialistas;
- un router/orquestador;
- herramientas.
No crees roles que no tengan una responsabilidad y criterio de optimización diferenciados.

4. MAPEA LAS DECISIONES
Identifica las decisiones que el modelo tendrá que tomar durante la tarea.
Diseña instrucciones para esas decisiones, no únicamente listas de acciones.

5. DISEÑA DESDE LOS FALLOS
Antes de construir el prompt, enumera los failure modes más probables.
Para cada fallo importante añade una mitigación apropiada.
Prioriza fallos de alta probabilidad o alto impacto.

6. DEFINE LAS FUENTES DE VERDAD
Si la tarea depende de hechos, establece una jerarquía de fuentes.
No permitas que buenas prácticas generales sustituyan silenciosamente evidencia del sistema real.

7. DEFINE EVIDENCIA E INCERTIDUMBRE
Cuando sea relevante, distingue:
- observado;
- verificado;
- medido;
- inferido;
- supuesto;
- por verificar;
- bloqueado.
Nunca permitas afirmar que algo fue comprobado si no se comprobó.

8. DEFINE ALCANCE Y AUTONOMÍA
Especifica:
- qué puede hacer;
- qué no debe hacer;
- cuándo necesita confirmación;
- qué debe preservar;
- qué acciones son sensibles.

9. DISEÑA UN WORKFLOW ADAPTATIVO
No impongas fases universales salvo que sean realmente necesarias.
Selecciona únicamente las fases y especialistas pertinentes para la tarea actual.

10. DEFINE CRITERIOS DE ÉXITO
Todo prompt maestro debe definir cuándo una tarea está terminada y cómo puede verificarse su calidad.

11. DISEÑA LA SALIDA
El formato debe estar subordinado a la tarea.
No generes tablas, JSON, XML ni grandes estructuras por estética.

12. CONSTRUYE EL PROMPT
Utiliza únicamente las secciones necesarias.
Prioriza claridad, jerarquía y densidad informativa.

13. EVALÚA EL PROMPT
Crea una suite representativa de casos:
- normal;
- simple;
- complejo;
- ambiguo;
- incompleto;
- límite;
- fallo;
- alto riesgo;
- fuera de alcance.

14. RED-TEAM
Intenta encontrar:
- contradicciones;
- loops;
- reglas absolutas incorrectas;
- lagunas;
- sobreingeniería;
- hallucination paths;
- formatos rígidos;
- instrucciones innecesarias.

15. REFACTORIZA
Elimina redundancias.
Condiciona absolutos.
Modulariza capacidades.
Reduce tokens sin perder comportamiento.

16. ENTREGA
Entrega la versión final solamente después de esta revisión.

REGLAS DE CALIDAD

- Calidad funcional > apariencia.
- Relevancia > volumen.
- Comportamiento condicional > reglas universales.
- Evidencia > confianza retórica.
- Cambio mínimo > sobreingeniería.
- Contexto seleccionado > acumulación.
- Evaluación > intuición.
- Roles funcionales > personajes decorativos.
- Prompt modular > monolito cuando el dominio sea complejo.
- Principios estables separados de detalles dependientes de versión.

NO HAGAS

- No uses "actúa como experto" como sustituto de responsabilidades.
- No añadas tecnologías simplemente para sonar moderno.
- No conviertas recomendaciones en obligaciones universales.
- No obligues a ejecutar todas las fases para todas las tareas.
- No inventes capacidades, archivos, herramientas o hechos.
- No declares un prompt profesional sin evaluarlo.
- No aumentes longitud si una instrucción no cambia comportamiento.
- No ocultes limitaciones reales.

CRITERIO FINAL
El mejor prompt no es el que contiene más instrucciones.
Es el que construye el entorno de decisiones más claro, verificable, adaptable y robusto con el menor contexto necesario.
```

---

# 24. PLANTILLA DE ENCARGO PARA LA SKILL

Para mejorar la calidad de entrada, permitir este formato:

```text
TIPO DE PROMPT:
OBJETIVO:
USUARIO FINAL:
ENTORNO:
ENTRADAS DISPONIBLES:
RESULTADO ESPERADO:
HERRAMIENTAS DISPONIBLES:
FUENTES DISPONIBLES:
RESTRICCIONES:
RIESGO:
GRADO DE AUTONOMÍA:
FORMATO DE ENTREGA:
```

Los campos pueden ser opcionales.

Si faltan datos no críticos, el generador debe inferir de forma conservadora.

---

# 25. RÚBRICA PROFESIONAL DEL GENERADOR

Puntuar cada prompt:

| Dimensión | Pregunta |
|---|---|
| Objetivo | ¿Está inequívocamente definido? |
| Alcance | ¿Evita scope creep? |
| Arquitectura | ¿La estructura corresponde al problema? |
| Decisiones | ¿Controla decisiones reales? |
| Grounding | ¿Sabe de dónde obtiene sus hechos? |
| Incertidumbre | ¿Sabe qué hacer cuando no sabe? |
| Adaptabilidad | ¿Se adapta al tipo de tarea? |
| Fallos | ¿Anticipa failure modes relevantes? |
| Herramientas | ¿Define herramientas de forma clara? |
| Seguridad | ¿Controla acciones sensibles? |
| Verificación | ¿Puede demostrar éxito? |
| Eficiencia | ¿Evita instrucciones innecesarias? |
| Mantenibilidad | ¿Puede evolucionar sin contradicciones? |
| Output | ¿La salida está bien diseñada? |

---

# 26. ESCALA DE MADUREZ

## Nivel 1 — Prompt básico

Rol + tarea.

## Nivel 2 — Prompt estructurado

Rol + objetivo + restricciones + output.

## Nivel 3 — Prompt profesional

Añade:

- contexto;
- criterios;
- workflow;
- incertidumbre;
- validación.

## Nivel 4 — Sistema de prompting

Añade:

- modularidad;
- fuentes;
- herramientas;
- failure handling;
- evaluación.

## Nivel 5 — Prompt system engineered

Añade:

- router;
- capacidades condicionales;
- eval suite;
- red-team;
- regresión;
- optimización de contexto;
- versionado;
- feedback loop.

El generador debe aspirar al nivel apropiado para la tarea.

No convertir automáticamente cada petición en Nivel 5.

---

# 27. MECANISMO DE AUTOCRÍTICA

Antes de finalizar, responder internamente:

```text
1. ¿He creado algo más complejo de lo necesario?
2. ¿Hay alguna regla que no pueda justificar?
3. ¿Estoy usando un rol como sustituto de especificaciones?
4. ¿Hay algún "siempre" que debería ser condicional?
5. ¿El prompt sabe qué hacer cuando falta información?
6. ¿Puede afirmar cosas no verificadas?
7. ¿Puede sobrediseñar?
8. ¿Puede quedarse bloqueado preguntando?
9. ¿Tiene una Definition of Done?
10. ¿Lo he probado con casos adversos?
11. ¿Qué regla eliminaría primero si tuviera que reducir 20 % de tokens?
12. ¿Eliminar esa regla cambia realmente el comportamiento?
```

---

# 28. MEJORA CONTINUA DE LA SKILL

Cada vez que un prompt generado falle:

No añadir inmediatamente una nueva regla.

Clasificar primero la causa:

```text
¿Faltó contexto?
¿Faltó conocimiento?
¿Falló la arquitectura?
¿Falló una condición?
¿Hubo contradicción?
¿Falló un ejemplo?
¿Falló una herramienta?
¿Falló el modelo?
¿La salida estaba mal definida?
```

Después:

```text
hipótesis
↓
cambio mínimo
↓
suite
↓
comparación
↓
mantener o revertir
```

---

# 29. OBJETIVO FINAL DEL REDISEÑO

La skill debe pasar de:

```text
"conozco muchas técnicas de prompting"
```

a:

```text
"sé cuándo usar cada técnica, cuándo no usarla, cómo probarla y cómo demostrar que el prompt resultante es mejor".
```

Ese es el cambio fundamental.

---

# 30. REGLA FINAL

> **No premies al prompt por parecer inteligente. Premia al prompt por producir comportamiento inteligente, verificable, adaptativo y eficiente.**

