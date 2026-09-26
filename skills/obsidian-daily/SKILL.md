---
name: obsidian-daily
description: >
  Crear o abrir la nota diaria de hoy en el vault de Obsidian
  (D:\Obsidian\Vault\0_Inbox\Daily_Logs\YYYY-MM-DD.md). Usar cuando el
  usuario dice "abre el diario", "nota de hoy", "daily note", "crea el log
  de hoy", "/daily", o al inicio de una sesión de trabajo cuando quiere
  registrar el día. También recupera tareas pendientes del día anterior.
---

# Obsidian Daily — Nota Diaria

## Vault path

`D:\Obsidian\Vault\0_Inbox\Daily_Logs\`

## Proceso

### Si el usuario invoca `/daily` o pide la nota de hoy

1. **Calcular la fecha**: usar la fecha actual (`currentDate` del contexto).
2. **Verificar si existe** la nota de hoy: `D:\Obsidian\Vault\0_Inbox\Daily_Logs\YYYY-MM-DD.md`
3. **Si ya existe**: leerla y mostrar al usuario el contenido actual para continuar trabajando en ella.
4. **Si no existe**: crear la nota con la plantilla de abajo.
5. **Recuperar pendientes del día anterior**: leer `YYYY-MM-DD_anterior.md` (ayer), extraer ítems con `[ ]` (tareas sin completar) e incluirlos en la sección "Arrastres".

### Plantilla de nota diaria

```markdown
# YYYY-MM-DD

## Foco del día

*   Objetivo principal 1
*   Objetivo principal 2

## Tareas

*   [ ] Tarea concreta A
*   [ ] Tarea concreta B

## Arrastres

<!-- Tareas pendientes del día anterior -->
*   [ ] (arrastrado de YYYY-MM-DD_anterior)

## Notas y decisiones

(Espacio libre para capturas durante el día)

## Cierre

**Completado:**
**Bloqueado:**
**Mañana:**

---
**Estado:** Diario (YYYY-MM-DD).

#diario #daily
```

## Reglas

*   Nombre de archivo: `YYYY-MM-DD.md` exacto. Sin texto adicional.
*   Ruta fija: `0_Inbox/Daily_Logs/`
*   No usar YAML frontmatter.
*   Consultar `obsidian-syntax` para convenciones de formato.
*   Las tareas completadas se marcan `[x]`, no se borran — son historial.

## Flujo de tareas entre días

Al crear la nota de hoy:
1. Leer la nota de ayer si existe.
2. Extraer líneas con `- [ ]` o `*   [ ]` sin completar.
3. Añadirlas bajo `## Arrastres` con referencia al día origen.
4. No duplicar si ya están en la nota de hoy.

## Activación proactiva

Si el usuario empieza una sesión sin daily note creada y menciona que va a trabajar en algo, sugerir:
"No tienes daily note de hoy. ¿Creo una para registrar la sesión? (`/daily`)"
