---
name: cierre-sesion
description: >
  Protocolo de cierre de sesion de trabajo. Ejecuta commit+push, actualiza
  Notion (tareas/sprint) y sugiere sync a Obsidian si hubo insights.
  Usar cuando el usuario dice "cierro sesion", "me voy", "hasta luego",
  "luego vuelvo", "manana seguimos", "por hoy ya", o cuando se detecta
  fin de sesion. Tambien se puede invocar directamente con /cierre-sesion.
  ACTIVAR PROACTIVAMENTE cuando el usuario señala fin de trabajo.
---

# Cierre de Sesion — Protocolo de fin de trabajo

## Rol

Eres el encargado de que nada se pierda al cerrar una sesion de trabajo.
Tu trabajo es persistir el progreso en los 3 sistemas: Git, Notion y Obsidian.

## Contexto

Alejandro trabaja desde multiples equipos via SSH a un servidor central.
Si el trabajo no se persiste (commit+push, Notion actualizado), se pierde
o queda invisible para la siguiente sesion o para otros dispositivos.

Para las reglas del sistema de productividad (sprints, cadencias, prioridades),
consultar `references/sistema-productividad.md`.

## Protocolo (ejecutar en orden)

### Paso 1 — Git commit + push

1. Revisar `git status` en TODOS los repos tocados en la sesion.
2. Para cada repo con cambios:
   - `git add` de archivos relevantes (no secrets, no datos)
   - `git commit` con mensaje descriptivo
   - `git push origin main` (o la rama activa)
3. Si hay repos fuera del directorio actual, navegar a ellos.
   Repos que pueden tener cambios indirectos:
   - `~/cerebro-digital/` (vault Obsidian; en iMac: `~/.openclaw/workspace-arquimedes/cerebro-digital/`)
   - `~/.claude/skills/` (si se modificaron skills)

### Paso 2 — Actualizar Notion (si aplica)

Solo si hay tareas de Notion relevantes en la sesion.

1. Verificar si el MCP de Notion esta disponible (`@notionhq/notion-mcp-server`).
2. Si esta disponible:
   - Marcar tareas completadas como "Hecho"
   - Actualizar estado de tareas en progreso
   - Si se identificaron nuevas tareas, crearlas en el backlog
   - Actualizar el campo "Semana" si se asignaron a un sprint
3. Si NO esta disponible:
   - Informar al usuario que debe actualizar Notion manualmente
   - Listar las tareas que cambiaron de estado

### Paso 3 — Sync a Obsidian (solo si aplica)

NO siempre es necesario. Solo sugerir si en la sesion hubo:
- Decisiones estrategicas o de arquitectura
- Aprendizajes que cruzan contextos (aplican a mas de un proyecto)
- Cambios en el sistema de productividad o en reglas del vault

Si aplica, usar el skill `cerebro-digital` con la operacion correspondiente
(sincronizar, aprender, o decidir).

Si no aplica, no hacer nada — no forzar sync innecesarios.

### Paso 4 — Resumen de cierre

Mostrar al usuario un resumen breve:
```
Sesion cerrada:
- Git: [repos commiteados y pusheados]
- Notion: [tareas actualizadas] o [no aplica]
- Obsidian: [sync realizado] o [no necesario]
```

## Reglas

- NUNCA preguntar "quieres que haga commit?" — hacerlo directamente.
  El usuario ya dio instruccion permanente de commit+push al cerrar.
- NUNCA crear commits vacios o innecesarios.
- NUNCA hacer push a ramas protegidas sin confirmar.
- Si hay conflictos de merge, informar al usuario en vez de resolver solo.
- Ser RAPIDO — el usuario se esta yendo. No extenderse.
