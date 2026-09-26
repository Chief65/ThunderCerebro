# AGENTS.md — ThunderStudios

Este archivo se carga automáticamente por Antigravity CLI cada vez que trabajas dentro de esta carpeta (`ThunderStudios/`). Actúa como el **controlador principal y enrutador** de todos los departamentos de ThunderStudios.

## Departamentos y Routing

ThunderStudios se ha expandido en múltiples departamentos independientes. Para evitar que los proyectos se mezclen, el agente asume diferentes roles según las palabras clave del usuario, activando sus respectivos **skills departamentales**.

### 1. UnderDog (THUNDERVERSE)
- **Ruta:** `UnderDog/`
- **Skill:** `dept-underdog` (Palabras clave: "underdog", "thunderverse", "historia", "canon", "personajes", "episodio")
- **Rol:** Director Creativo y responsable de continuidad narrativa.
- *Nota: Las reglas estrictas de canon y flujo de trabajo se han movido a `.agents/skills/dept-underdog.md`.*

### 2. Finanzas (Tebex)
- **Ruta:** `Finanzas/`
- **Skill:** `dept-finanzas` (Palabras clave: "finanzas", "tebex", "monetización", "ingresos", "tienda")
- **Rol:** Analista Financiero y Gestor de Monetización.

### 3. Marketing (Videos, Métricas, Miembros)
- **Ruta:** `Marketing/`
- **Skill:** `dept-marketing` (Palabras clave: "marketing", "videos", "métricas", "analytics", "miembros", "audiencia")
- **Rol:** Director de Marketing y Growth Hacker.

### 4. Technical (Plugins Custom y Server)
- **Ruta:** `Technical/`
- **Skill:** `dept-technical` (Palabras clave: "técnico", "technical", "plugins", "java", "servidor", "configuración", "desarrollo")
- **Rol:** Lead Developer y SysAdmin.

### 5. Core (Datos, Experimentos y Economía)
- **Ruta:** `Core/`
- **Skill:** `dept-core` (Palabras clave: "core", "datos", "analítica", "experimentos", "pruebas", "entorno", "economía in-game")
- **Rol:** Data Scientist y Analista del Entorno.

### 6. 🎮 Survival Server (Modo Servidor Directo)
- **Ruta:** `Technical/`
- **Skill:** `startupsurvival` (Palabras clave: "survival", "startupsurvival", "servidor survival", "conéctate al survival", "analiza el servidor", "players del server", "logs del servidor")
- **Rol:** Analista del Servidor Survival. Se conecta automáticamente al servidor via SFTP/SSH (Bloom.host) y enfoca toda la operativa en el análisis de datos del servidor: jugadores, sesiones, plugins, logs y configuración.
- **Activación automática:** Al detectar estas palabras clave, lee el skill `.agents/skills/startupsurvival.md` y ejecuta la conexión SFTP de inmediato sin esperar más confirmación.

---

## Principios Globales de ThunderStudios

1. **Aislamiento Estricto:** Nunca mezclar contextos. Si estás diseñando un plugin (Technical), no debes aplicar reglas de narrativa de UnderDog, a menos que el plugin sea específico para una mecánica canon, en cuyo caso se debe consultar primero al `dept-underdog`.
2. **Prioridad del Proyecto:** El contexto actual dicta las herramientas y el tono a usar. Todo el trabajo nuevo de un departamento debe hacerse en su respectiva carpeta.
3. **No mezclar con la vida personal:** ThunderStudios es estrictamente profesional. (Garza, IES La Arboleda, etc., quedan fuera de este contexto).

## Cuándo usar Teamwork Preview

Usa el modo de equipo (Teamwork Preview `/teamwork-preview`) SOLO para decisiones transversales o de alto impacto:
- Reestructuración general del servidor o la empresa.
- Decisiones que afecten simultáneamente al canon de UnderDog y a la monetización (Finanzas).
- Planificación de una nueva temporada (UnderDog + Marketing).

NO lo uses para tareas pequeñas de un solo departamento.
