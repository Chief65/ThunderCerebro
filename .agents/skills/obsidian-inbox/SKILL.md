---
name: obsidian-inbox
description: >
  Procesar y organizar el inbox del vault de Obsidian
  (D:\Obsidian\Vault\0_Inbox\). Usar cuando el usuario dice "procesa el
  inbox", "organiza el inbox", "clasifica las capturas", "/inbox", "limpia
  el inbox", "procesa lo que tengo pendiente", o cuando el inbox tiene
  acumulación de entradas sin procesar. Transforma capturas crudas en notas
  permanentes bien enlazadas en las carpetas correctas del vault.
---

# Obsidian Inbox — Procesar y Organizar

## Principio

El inbox es temporal. Su único propósito es capturar rápido. Todo lo que
esté ahí más de una semana es deuda de conocimiento. Este skill la paga.

## Vault path

`D:\Obsidian\Vault\0_Inbox\`

## Proceso completo

### Fase 1 — Auditoría (qué hay en el inbox)

1. Listar todos los archivos en `0_Inbox/` excepto `Daily_Logs/` y `assets/`.
2. Para cada archivo, contar entradas marcadas con `<!-- pendiente procesar -->`.
3. Mostrar resumen al usuario:
   ```
   Inbox: X archivos, Y entradas pendientes
   - Ideas_Sueltas.md: N entradas
   - Recursos_Pendientes.md: N entradas
   - ...
   ```
4. Preguntar: "¿Proceso todo o empezamos por un archivo específico?"

### Fase 2 — Clasificación de cada entrada

Para cada entrada pendiente, determinar:

| Pregunta | Si SÍ → acción |
|----------|---------------|
| ¿Es una tarea accionable? | Añadir a daily note o sugerir Notion |
| ¿Es conocimiento reutilizable? | Crear nota en `2_Areas/` o `3_Recursos/` |
| ¿Es referencia a herramienta/tecnología? | Crear/actualizar nota en `3_Recursos/Herramientas/` |
| ¿Es relacionada con un proyecto activo? | Enlazar a la nota del proyecto en `1_Proyectos/` |
| ¿Es una decisión ya tomada? | Añadir bajo `## Decisiones` en la nota relevante |
| ¿Es efímera / ya no relevante? | Descartar (con confirmación del usuario) |

### Fase 3 — Ejecución

Para cada entrada procesada:

1. **Buscar** si ya existe una nota relevante en el vault (`Grep` + `Glob`).
2. **Si existe**: añadir la información bajo la sección correcta.
3. **Si no existe**: crear nota nueva siguiendo convenciones de `obsidian-syntax`.
4. **Siempre**: añadir `[[wikilinks]]` a notas relacionadas.
5. **Marcar como procesada**: cambiar `<!-- pendiente procesar -->` por `<!-- procesado YYYY-MM-DD -->`.

### Fase 4 — Limpieza final

Después de procesar todas las entradas de un archivo:
1. Si el archivo solo contiene entradas procesadas, proponer archivarlo o vaciarlo.
2. Nunca borrar sin confirmar con el usuario.

## Reglas de creación de notas permanentes

Seguir `obsidian-syntax` para todo. Resumen:
*   Nombre: `PascalCase_Con_Guiones_Bajos.md`
*   Sin YAML frontmatter
*   Tags al pie
*   Bullets con asterisco + 4 espacios
*   Estado al pie: `**Estado:** Vivo (vX.X - Mes YYYY).`

### Dónde va cada nota nueva

| Contenido | Carpeta |
|-----------|---------|
| Concepto técnico, tecnología, framework | `3_Recursos/Herramientas/` |
| Aprendizaje formativo (curso, libro) | `3_Recursos/Formacion_Continua/` |
| Herramienta mental, metodología | `3_Recursos/Mentalidad/` |
| Responsabilidad continua (proyecto largo, área de vida) | `2_Areas/Tecnologia/` o `2_Areas/Negocio/` |
| Proyecto con deadline | `1_Proyectos/` (ficha índice ligera — tracking en Notion) |

## Gestión de conexiones

Al procesar cada entrada, buscar activamente notas relacionadas:

1. `Grep` en el vault por términos clave del contenido.
2. Enlazar la nota nueva/actualizada a lo que encuentres.
3. Si la nota encontrada se beneficia del enlace inverso, añadirlo también.

**Meta**: el grafo de Obsidian debe reflejar cómo se conecta el conocimiento,
no solo acumular notas aisladas.

## Modo rápido vs modo profundo

El usuario puede pedir:
*   **Rápido** (`/inbox rapido`): procesar solo primeras 5-10 entradas, sin crear notas nuevas — solo clasificar y enlazar a notas existentes.
*   **Profundo** (`/inbox profundo`): proceso completo, crear notas nuevas, revisar conexiones, proponer MOCs si hay clusters temáticos.

Default: modo rápido si hay ≤5 entradas, modo profundo si hay >5.

## Activación proactiva

Al final de sesiones largas o al invocar `cierre-sesion`, verificar si hay
entradas en inbox sin procesar. Si las hay, sugerir:
"Tienes X entradas en inbox sin procesar. ¿Las proceso ahora o las dejamos para después?"
