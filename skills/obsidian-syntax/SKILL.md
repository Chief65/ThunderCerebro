---
name: obsidian-syntax
description: >
  Referencia de sintaxis Obsidian específica para el vault de Ramos
  (D:\Obsidian\Vault). Cargar SIEMPRE antes de crear o editar cualquier
  nota en el vault. Garantiza que Claude usa wikilinks, callouts, embeds
  y formato de archivo correctamente según las convenciones del vault.
  NO es un skill de usuario — es una referencia interna que otros skills
  invocan implícitamente cuando trabajan con el vault.
---

# Obsidian Syntax — Referencia del Vault

## Vault path

`D:\Obsidian\Vault`

## Reglas absolutas (nunca romper)

| Regla | Correcto | Incorrecto |
|-------|----------|------------|
| Sin YAML frontmatter | — | `---\ntitle: X\n---` |
| Nombre de archivo | `PascalCase_Con_Guiones_Bajos.md` | `mi nota.md`, `mi-nota.md` |
| Bullets | `*   Item` (asterisco + 4 espacios) | `- Item` |
| Tags | Al pie del archivo: `#tag1 #tag2` | En YAML o en medio del texto |
| Estado | Al pie: `**Estado:** Vivo (v1.0 - Abril 2026).` | — |

## Estructura interna de una nota

```markdown
# Título Descriptivo Largo

Descripción de una o dos frases que resume la nota. Sin encabezado propio.

## Sección 1

*   Contenido con bullets
*   Más contenido
    *   Nested con 4 espacios adicionales

## Sección 2

Texto libre.

---
**Estado:** Vivo (v1.0 - Abril 2026).

#tag1 #tag2 #tag3
```

## Estructura de carpetas del vault

```
_Sistema/             Reglas e infraestructura del vault
0_Inbox/              Capturas sin procesar — procesado semanal
  Daily_Logs/         Diarios: YYYY-MM-DD.md
  assets/             Imágenes agrupadas por fecha: assets/YYYY-MM-DD/
1_Proyectos/          Fichas índice ligeras (tracking en Notion)
2_Areas/              Responsabilidades continuas sin fecha fin
  Negocio/
  Tecnologia/
  Arquitectura_Agentes/
3_Recursos/           Biblioteca de referencia
  Herramientas/
  Formacion_Continua/
  Mentalidad/
4_Archivo/            Proyectos terminados, notas superseded
```

## Sintaxis Obsidian específica

### Wikilinks (SIEMPRE usar en lugar de links Markdown)

```markdown
[[Nombre_Archivo]]                     # link básico
[[Nombre_Archivo|Texto visible]]       # link con alias
[[Carpeta/Nombre_Archivo]]             # link con ruta si hay ambigüedad
```

### Embeds

```markdown
![[Nombre_Archivo]]                    # embed de nota completa
![[Nombre_Archivo#Sección]]            # embed de sección específica
![[imagen.png]]                        # embed de imagen
```

### Callouts (bloques informativos)

```markdown
> [!note] Título opcional
> Contenido del callout.

> [!warning] Atención
> Algo importante a tener en cuenta.

> [!tip] Consejo
> Sugerencia práctica.

> [!important]
> Decisión crítica o punto de no retorno.
```

Tipos disponibles: `note`, `tip`, `warning`, `danger`, `info`, `success`, `question`, `quote`, `abstract`, `todo`, `example`, `bug`, `important`.

### Tags

```markdown
#tag-simple
#dominio/subtag          # jerarquía con /
```

Tags al pie del archivo, nunca en YAML. Lista autoritativa en `_Sistema/00_Reglas_Vault.md`.

### MOCs / Índices

Archivos de índice usan prefijo `00_`:
```
00_Index_Formacion.md
00_Index_Proyectos_Activos.md
```

## Nombres de archivo — reglas de nomenclatura

*   PascalCase con guiones bajos: `Plan_Carrera_IA.md`
*   Sin espacios, sin acentos, sin caracteres especiales
*   Daily logs: `YYYY-MM-DD.md` (en `0_Inbox/Daily_Logs/`)
*   MOCs/Índices: prefijo `00_` seguido de nombre PascalCase

## Convenciones de enlazado

Una nota sin `[[enlaces]]` es una nota muerta. Al crear o editar una nota:

1. Buscar en el vault notas relacionadas (`Grep` + `Glob`).
2. Enlazar hacia ellas con `[[Nombre_Archivo]]`.
3. Considerar si las notas enlazadas deberían también enlazar de vuelta.

Notas clave del vault (verificar existencia antes de enlazar):
*   `[[Erbe_Connect]]` o similar — TFG actual
*   `[[Jarvis]]` — asistente personal IA
*   `[[Plan_Carrera_IA]]` — ruta formativa
*   `[[Stack_Tecnico]]` o similar — herramientas y stack

## Qué NO hacer

*   No crear subcarpetas nuevas sin consenso del usuario
*   No duplicar contenido del CLAUDE.md de repos — las notas del vault son resúmenes + conexiones
*   No usar Markdown links `[texto](url)` para enlaces internos — solo `[[wikilinks]]`
*   No crear notas largas — preferir 3 notas atómicas enlazadas
*   No usar YAML frontmatter bajo ningún concepto
