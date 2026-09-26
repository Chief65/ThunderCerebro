# Convenciones del Vault cerebro-digital

Referencia rápida para crear/editar notas consistentes.

## Ruta

`~/.openclaw/workspace-arquimedes/cerebro-digital` (servidor iMac)
`~/cerebro-digital` (otros equipos — canónico)
`~/Proyectos/cerebro-digital` (legacy, transición)

**Fuente unica de verdad para reglas completas:** `_Sistema/00_Reglas_Vault.md`
Este archivo es una referencia rapida. Si hay conflicto, el archivo de reglas manda.

## Estructura de carpetas

```
_Sistema/             Reglas, metodo. Infraestructura del vault.
0_Inbox/              Capturas sin procesar. Procesado semanal.
  Daily_Logs/         Diarios: YYYY-MM-DD.md
  assets/             Imágenes: assets/YYYY-MM-DD/
1_Proyectos/          Fichas indice ligeras (tracking operativo en Notion)
2_Areas/              Responsabilidades continuas sin fecha fin
  Arquitectura_Agentes/
  Negocio/
  Tecnologia/
3_Recursos/           Biblioteca de referencia
  Mentalidad/
  Herramientas/
  Formacion_Continua/
4_Archivo/            Proyectos terminados, notas superseded
archive/              Legacy (migrar a 4_Archivo)
```

## Formato de archivo

```markdown
# Título descriptivo largo

Descripción en una o dos frases (sin encabezado propio).

## Sección 1
*   Contenido con bullets (asterisco, no guión)

## Sección 2
...

---
**Estado:** Vivo (vX.X - Mes YYYY).

#tag1 #tag2 #tag3
```

## Reglas de formato

| Elemento | Convención | Ejemplo |
|----------|-----------|---------|
| Frontmatter | NO usar | — |
| Nombre archivo | PascalCase_Con_Guiones_Bajos | `Plan_Carrera_IA.md` |
| Enlaces | `[[Nombre_Archivo]]` o `[[Nombre_Archivo\|Texto visible]]` | `[[Vertice_Data]]` |
| MOCs/Índices | Prefijo `00_` | `00_Index_Formacion.md` |
| Tags | Al pie del archivo, sin frontmatter | `#consultoria #rag` |
| Bullets | Asterisco `*` con 4 espacios para nested | `*   Item` |
| Estado | Línea de texto al pie | `**Estado:** Vivo (v1.0 - Marzo 2026).` |
| Daily logs | `YYYY-MM-DD.md` en `0_Inbox/Daily_Logs/` | `2026-03-14.md` |

## Tags

**Lista autoritativa en `_Sistema/00_Reglas_Vault.md`.** Leer siempre antes de asignar.
Referencia rapida por dominio:

- Negocio: `#vertice #consultoria #fmcg #negocio`
- Técnico: `#python #infraestructura #stack #ia #rag`
- Formación: `#aprendizaje #formacion #roadmap`
- Meta: `#sistema #meta #vault #mindset #recursos`

## Notas clave (para enlazar)

No fiarse de esta lista — puede estar desactualizada. Usar `Glob` + `Grep`
en el vault para encontrar notas existentes antes de crear nuevas.

Referencia rapida:
- `[[Vertice_Data]]` — Consultoria de datos, perfil, roadmap
- `[[TFM_Master_UNIR]]` — Trabajo fin de master (proyecto con deadlines)
- `[[Plan_Entrenamiento_Python]]` — Slots de entrenamiento tecnico (Area)
- `[[Plan_Carrera_IA]]` — Ruta formativa a largo plazo (Recurso)
- `[[RAG_Learning_Path]]` — RAG como skill vendible (Recurso)

## Principio fundamental

Las notas valen por sus CONEXIONES, no por su contenido aislado.
Una nota sin `[[enlaces]]` es una nota muerta.
