# Guía: CLAUDE.md de Proyecto (Capa 2)

## Principio

La Capa 1 (global) define QUIÉN eres y CÓMO trabajas.
La Capa 2 (proyecto) define EN QUÉ estás trabajando y QUÉ necesita Claude saber
para ayudarte en ESTE contexto específico.

**Regla de oro**: El CLAUDE.md del proyecto NO repite nada del global.
No poner identidad, tono, principios ni metodología — eso ya se carga
automáticamente desde `~/.claude/CLAUDE.md` y los skills globales.

---

## Plantilla base

```markdown
# [Nombre del Proyecto]

## Propósito
[UNA frase: qué problema resuelve]

## Modo por defecto: [modo-estudio | modo-productivo]

## Estado actual
[En qué fase está: investigación, desarrollo, testing, producción]
[Si tiene subproyectos, tabla con el estado de cada uno]

## Contexto técnico
- Stack: [tecnologías]
- Base de datos: [esquema, tablas clave]
- APIs/servicios: [integraciones]
- MCPs útiles: [cuáles de los MCPs del usuario aplican aquí]

## Archivos clave
| Archivo | Descripción | Estado |
|---------|-------------|--------|
| ... | ... | ✅ / 🔄 / ⬜ |

## Decisiones tomadas
[Decisiones de diseño YA tomadas y su justificación.
Esto evita que Claude re-proponga algo que ya se descartó.]

## Próximos pasos
- [ ] [Lo más inmediato]

## Deuda técnica conocida
[Problemas que se saben que existen pero no se van a resolver ahora]
```

---

## Qué poner y qué NO poner

### SÍ poner:
- **Modo por defecto**: Cada proyecto tiene su ritmo.
- **Estado actual**: Claude necesita saber dónde estamos, no empezar de cero.
- **Decisiones tomadas**: Lo más valioso. Evita que Claude re-proponga lo que ya se descartó.
- **Archivos clave con su estado**: Claude puede navegar por el proyecto.
- **Deuda técnica**: Para que Claude la señale cuando sea relevante, no la ignore.
- **Dependencias entre subproyectos**: Si hay múltiples líneas de trabajo, indicar cuál bloquea a cuál.

### NO poner:
- **Especificaciones técnicas completas**: Van en archivos separados. El CLAUDE.md apunta a ellos.
- **Identidad, tono, principios**: Ya están en la Capa 1.
- **Historial completo del proyecto**: Solo el estado actual. Para historial usar un archivo separado tipo `CONTEXTO_CONVERSACION.md`.
- **Código**: El CLAUDE.md es prosa, no código. Referencia archivos de código.

---

## Cuándo añadir skills de proyecto

Los skills de proyecto van en `.claude/skills/` dentro del repo.
Solo crearlos cuando hay un procedimiento ESPECÍFICO de este proyecto
que no tiene sentido como skill global.

**Es de proyecto si** solo tiene sentido en este repo (flujo de deploy específico,
reglas de validación propias del dominio, procedimiento de testing particular).

**Es global si** te serviría en otro proyecto (metodología de estudio, cómo
documentar decisiones, cómo investigar problemas).

---

## Ejemplos por tipo de proyecto

### Proyecto de estudio
```markdown
# Análisis de Datos Masivos en R

## Propósito
Prácticas y estudio de la asignatura de Análisis de Datos en R del Máster BI.

## Modo por defecto: modo-estudio

## Estado actual
Semana 3: Regresión lineal y clasificación.

## Contexto técnico
- Stack: R, RStudio
- Librerías: dplyr, ggplot2, caret
- Materiales: en ./materiales/ (transcripciones y PDFs)

## Temario y progreso
| Tema | Estado |
|------|--------|
| R y RStudio básico | ✅ |
| Limpieza de datos | ✅ |
| Análisis descriptivo | ✅ |
| Regresión lineal | 🔄 |
| Clasificación | ⬜ |
| Clustering | ⬜ |
| Series temporales | ⬜ |
```

### Proyecto profesional
```markdown
# Diagnóstico de Rentabilidad por Cliente

## Propósito
Identificar clientes no rentables y proponer acciones comerciales.

## Modo por defecto: modo-productivo

## Estado actual
Fase de exploración: queries SQL para extraer datos de margen por cliente.

## Contexto técnico
- Stack: SQL (Oracle), Python (pandas), PowerBI
- Esquema: REPORTING (tablas VENTAS, CLIENTES, COSTES)
- MCP oracle-db: usar para validar queries contra datos reales
```

### Proyecto de consultoría
```markdown
# Portafolio y Propuesta Comercial

## Propósito
Crear materiales de venta para servicios de consultoría de datos.

## Modo por defecto: modo-productivo
En brainstorming cambiar a investigacion-problemas.

## Estado actual
Definiendo estructura del PDF de diagnóstico de rentabilidad.
```

---

## Flujo de carga

```
Claude CLI abre en ~/Proyectos/mi-proyecto/
         │
         ▼
Carga automática:
  1. ~/.claude/CLAUDE.md              ← Capa 1: quién eres
  2. ~/.claude/skills/*/SKILL.md      ← Capa 1: qué sabe hacer (descriptions)
  3. ~/Proyectos/mi-proyecto/CLAUDE.md ← Capa 2: en qué trabajas
         │
         ▼
Claude ya tiene todo el contexto. No necesitas explicar nada.
```

---

## Error común: CLAUDE.md como especificación técnica

Si el CLAUDE.md de un proyecto contiene algoritmos, diagramas de arquitectura,
definiciones de tablas SQL o código — eso NO es un CLAUDE.md, es una especificación.
Mover ese contenido a un archivo de documentación separado y crear un CLAUDE.md
real que apunte a él.

Señales de que un CLAUDE.md es realmente una spec:
- Tiene secciones tipo "Arquitectura de Datos", "Lógica del Motor".
- Tiene definiciones de tablas SQL o código.
- No tiene "Modo por defecto", "Estado actual" ni "Próximos pasos".
- Si lo leyera un empleado nuevo, sabría cómo funciona el sistema pero no qué hacer primero.
