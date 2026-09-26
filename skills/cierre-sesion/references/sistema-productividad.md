# Sistema de Productividad — Referencia operativa

Documento de referencia para el sistema de productividad de Alejandro.
Diseñado en el proyecto `~/Proyectos/sistema-productividad/`.

## Arquitectura de 3 capas

| Capa | Herramienta | Que guarda |
|------|-------------|-----------|
| Conocimiento | Obsidian (cerebro-digital) | Areas, recursos, reflexiones, aprendizajes |
| Ejecucion | Notion | Proyectos con deadline, sprints, tareas |
| Codigo | Repos Git (CLAUDE.md) | Contexto tecnico, guardrails por proyecto |

## Notion: estructura

- **Hub page**: 31854826-9655-8005-a47d-f658a69ee8a8
- **DB Proyectos**: 32b54826-9655-8113-a707-ce9dcf7ba057
- **DB Tareas**: 32b54826-9655-81bc-9945-c33d3921b18b

### Regla obligatoria: todo proyecto con repo tiene ficha en Notion

Si un repo en `~/Proyectos/` pertenece a Vertice, UNIR, Predictaflow o Aprendizaje → DEBE tener una ficha en DB Proyectos de Notion con el campo Repo apuntando al repo. Sin excepciones. Esto garantiza que ningun proyecto se queda sin seguimiento.

Al crear un proyecto nuevo (skill scaffolding-proyecto) o al detectar un repo sin ficha en cierre-sesion, avisar al usuario.

### DB Proyectos
| Campo | Tipo | Valores |
|-------|------|---------|
| Nombre | Titulo | — |
| Tipo | Select | Proyecto / Area |
| Area de vida | Select | UNIR / Vertice / Predictaflow / Aprendizaje / Salud / Ocio |
| Estado | Select | Activo / Backlog / Pausado / Completado |
| Deadline | Fecha | Solo si hay deadline real |
| Repo | URL | Link a GitHub |
| Nota vault | Texto | Nombre de nota en Obsidian |

### DB Tareas
| Campo | Tipo | Valores |
|-------|------|---------|
| Nombre | Titulo | — |
| Proyecto | Relacion | → DB Proyectos |
| Estado | Select | Backlog / Sprint / En progreso / Hecho / Bloqueado |
| Tipo de trabajo | Select | Deep Work / Shallow / Habito |
| Semana | Select | 2026-W13, 2026-W14... (el sprint = la semana) |
| Prioridad | Select | P1 / P2 / P3 |
| Fecha limite | Fecha | Solo si hay deadline real |
| Tiempo estimado | Numero | Minutos |

### Vistas
- **Sprint de la semana**: Semana = esta semana, agrupado por Proyecto
- **Calendario**: Tareas con fecha limite
- **Kanban por estado**: Todas las tareas activas
- **Backlog**: Sin semana asignada, ordenado por prioridad
- **Habitos**: Tipo = Habito
- **Por area de vida**: Agrupado por Area de vida

## Cadencias

| Cuando | Que | Duracion | Donde |
|--------|-----|----------|-------|
| Lunes | Planificar sprint: revisar backlog, asignar tareas, marcar prioridades | 30 min (shallow) | Vista Backlog + Sprint |
| Cada dia | Elegir foco: 1 deep work + habitos del dia | 5 min | Vista Sprint + Habitos |
| Viernes | Retro: que complete, que se quedo, por que. Mover incompleto a backlog | 15 min (shallow) | Vista Sprint |

## Prioridades

| Nivel | Criterio | Ejemplo actual |
|-------|----------|---------------|
| P1 | Genera ingresos o deadline externo | Clientes, entregas UNIR, crear sociedad |
| P2 | Construye capacidad para ingresos | TFM, cursos Python, infra-lab |
| P3 | Nice to have | Libros, katas exploratorias, Beelink |

Las prioridades se revisan cada lunes. Si aparece un cliente, su trabajo sube a P1.

## Tipos de trabajo (Deep Work)

| Tipo | Que es | Ejemplo |
|------|--------|---------|
| Deep Work | Cognitivamente exigente, requiere concentracion, crea valor | Avanzar TFM, diseñar oferta Vertice, resolver un bug complejo |
| Shallow | Poco exigente, se puede hacer distraido | Emails, admin, configurar herramientas |
| Habito | Mantenimiento diario/recurrente | Katas Python, revision de sprint |

## Guardrails globales

- **Max 2 slots de aprendizaje activos** (definido en Plan_Entrenamiento_Python)
- **Max 3 tareas Deep Work por sprint semanal**
- **El sprint se cierra el viernes** — lo incompleto vuelve a backlog, no se arrastra
- **Habitos NO cuentan como Deep Work** — son mantenimiento
- **Cada proyecto tiene sus propios guardrails** en su CLAUDE.md

## Flujo de sesion de trabajo

```
1. Abrir proyecto → Claude lee CLAUDE.md → conoce contexto + guardrails
2. Trabajar → Claude ayuda, ejecuta, avanza tareas
3. Cerrar sesion (skill cierre-sesion):
   a. Git commit + push
   b. Actualizar Notion (estado tareas, sprint)
   c. Sync Obsidian solo si hubo insights/decisiones
```

## Conexion con otros sistemas

- **Vault Obsidian**: skill `cerebro-digital` sincroniza conocimiento
- **Scaffolding**: skill `scaffolding-proyecto` crea ficha en Obsidian al crear proyecto
- **Arquimedes (futuro)**: brief operativo diario basado en Notion
