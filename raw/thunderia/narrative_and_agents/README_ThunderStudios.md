# ThunderStudios

Este repositorio es el **estudio de producción** de Thunder: contiene toda la
narrativa, el lore y la documentación de producción de la serie **UnderDog**
(universo THUNDERVERSE), además de futuros proyectos de ThunderStudios.

## Regla de oro

Todo lo que hay dentro de `UnderDog/` se considera **canon** salvo que el
propio documento indique lo contrario (ver `01_Lore/Canon_Levels.md`).

Al editar cualquier documento:

1. Preserva la continuidad. Revisa `02_Timeline/` y las fichas de
   `03_Characters/` antes de cambiar un hecho ya establecido.
2. Respeta las personalidades ya definidas.
3. Ante la duda entre inventar algo nuevo o expandir algo existente,
   **expande** lo existente.
4. Si una idea nueva contradice el canon, no se descarta: se mueve a
   `01_Lore/Canon_Levels.md` bajo "Ideas" hasta que se decida integrarla.

## Estructura

```
ThunderStudios/
├── AGENTS.md              ← instrucciones que Antigravity CLI lee automáticamente
├── .agents/skills/         ← skills especializadas del proyecto
├── Core/                    ← Laboratorio de datos, economía y métricas del servidor
├── UnderDog/                ← la serie (esto es lo que se enlaza en Obsidian)
│   ├── 00_Bible/
│   ├── 01_Lore/
│   ├── 02_Timeline/
│   ├── 03_Characters/
│   ├── 04_Factions/
│   ├── 05_Locations/
│   ├── 06_Powers/
│   ├── 07_Items/
│   ├── 08_Story_Arcs/
│   ├── 09_Episodes/
│   ├── 10_Scripts/
│   ├── 11_Cinematics/
│   ├── 12_Music/
│   ├── 13_References/
│   ├── 14_Content/
│   └── 15_Assets/
└── _setup/                 ← plantillas de configuración (MCP, symlink, etc.)
```

## Otros proyectos

Si en el futuro ThunderStudios produce algo que no sea UnderDog, ese proyecto
va en una carpeta hermana de `UnderDog/` (p. ej. `OtraSerie/`), nunca dentro
de ella, para que el grafo de Obsidian y el canon no se mezclen.
