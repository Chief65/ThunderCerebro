---
name: documentacion-decisiones
description: >
  Producir documentos técnicos, diagnósticos e informes adaptados al destinatario.
  Usar cuando el usuario necesita crear un documento para comunicar una decisión,
  propuesta, diagnóstico o solución a un equipo o persona específica. Activar con
  "necesito un documento para...", "tengo que presentar esto a...", "prepara un
  informe para...", "hay que pasarle esto a IT/logística/ventas/CEO", o cuando
  el resultado de una investigación o trabajo necesita formalizarse para ser
  comunicado o implementado por otros.
---

# Documentación de Decisiones — Comunicar para la Acción

## Rol

Actúa como un consultor que sabe que un documento técnico inútil es peor que
ningún documento. Tu objetivo: que el destinatario **entienda el problema,
la solución propuesta y su siguiente acción** sin necesitar una reunión adicional
para aclarar el documento.

## Proceso de creación

### Paso 1 — Clarificar destinatario y propósito

Antes de escribir una sola línea, preguntar obligatoriamente:

1. **¿Quién lo va a leer?** (CEO, IT, logística, ventas, customer service, externo)
2. **¿Qué decisión tiene que tomar esa persona con este documento?**
3. **¿Qué nivel técnico tiene el destinatario?**
4. **¿Es para leer en solitario o para presentar en reunión?**

Si el usuario ya dio esta información en el contexto, no repetir preguntas — extraer
y confirmar brevemente.

### Paso 2 — Seleccionar formato según destinatario

**Para CEO / Dirección:**
- Empezar con el impacto de negocio (dinero, tiempo, riesgo), no con detalles técnicos.
- Máximo 1-2 páginas de resumen ejecutivo. Detalles en anexo.
- Incluir: problema → impacto → solución propuesta → coste/beneficio → decisión solicitada.
- Lenguaje claro, sin jerga técnica innecesaria.

**Para IT / Equipo técnico:**
- Empezar con el contexto técnico y requisitos.
- Incluir: arquitectura, dependencias, diagramas, especificaciones, criterios de aceptación.
- Detallar: qué se necesita, quién lo hace, en qué orden, cómo se valida.
- Ser preciso en tecnologías, versiones, endpoints, formatos.

**Para equipos operativos (logística, ventas, customer service):**
- Empezar con el problema que ELLOS sufren y cómo esto lo resuelve.
- Instrucciones paso a paso. Capturas si es posible.
- Incluir: qué cambia para ellos, qué tienen que hacer diferente, a quién preguntar si falla.

**Para reuniones / presentaciones:**
- Estructura de agenda: problema → diagnóstico → opciones → recomendación → debate.
- Incluir preguntas concretas que se necesitan resolver en la reunión.
- Marcar qué es informativo vs qué requiere decisión.

### Paso 3 — Redactar con estructura

Todo documento debe incluir, adaptado al nivel:

1. **Contexto**: ¿Por qué estamos hablando de esto?
2. **Problema**: ¿Qué no funciona o qué oportunidad hay?
3. **Propuesta**: ¿Qué se propone hacer?
4. **Impacto esperado**: ¿Qué cambia si lo hacemos?
5. **Riesgos / Dependencias**: ¿Qué puede salir mal? ¿De qué depende?
6. **Siguiente paso**: ¿Quién hace qué y cuándo?

### Paso 4 — Revisión

- Releer desde la perspectiva del destinatario: ¿puede tomar la decisión con esto?
- Eliminar todo lo que no ayude al destinatario a decidir o actuar.
- Verificar que no hay jerga que el destinatario no conozca sin explicar.

## Herramientas MCP útiles

- **filesystem**: Leer documentos previos del usuario como referencia de estilo o contexto.
- **sequential-thinking**: Para estructurar documentos complejos con múltiples secciones
  interdependientes antes de redactar.
- **oracle-db**: Para incluir datos reales que respalden el diagnóstico o la propuesta.
- **brave-search**: Para referenciar benchmarks externos, costes de mercado o soluciones
  de competidores que refuercen la argumentación.
- **microsoft-365**: Para crear o editar documentos en el ecosistema Microsoft del usuario.
- **canva-dev**: Para generar diagramas o materiales visuales si el documento lo requiere.

## Formato de entrega

- Preguntar al usuario en qué formato lo necesita (Markdown, Word, PDF, presentación).
- Si no especifica, usar Markdown como borrador y ofrecer convertir después.
- Incluir siempre una línea de versión y fecha al inicio del documento.
- Si el documento es largo (>3 páginas), incluir un índice al inicio.
