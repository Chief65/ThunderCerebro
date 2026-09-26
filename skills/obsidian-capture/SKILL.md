---
name: obsidian-capture
description: >
  Captura rápida de ideas, recursos, enlaces o pensamientos al inbox del
  vault (D:\Obsidian\Vault\0_Inbox\) sin organizar ni clasificar. Usar
  cuando el usuario dice "apunta esto", "guarda esto en obsidian", "capture",
  "/capture", "añade al inbox", "no quiero perder esto", "anota rápido", o
  cuando hay que preservar algo sin interrumpir el flujo de trabajo. Velocidad
  máxima — sin estructura ni clasificación en el momento de la captura.
---

# Obsidian Capture — Captura Rápida al Inbox

## Principio

La captura rápida sirve para NO PERDER IDEAS sin interrumpir el trabajo actual.
Velocidad > Perfección. El inbox se procesa después con `obsidian-inbox`.

## Vault path

`D:\Obsidian\Vault\0_Inbox\`

## Proceso

1. **Recibir el contenido** a capturar del usuario.
2. **Determinar el tipo** (idea, recurso/URL, decisión, tarea, referencia, extracto).
3. **Crear o appendar** en el archivo correcto (ver abajo).
4. **No clasificar, no enlazar, no estructurar** — eso es trabajo del inbox.
5. **Confirmar** al usuario: "Capturado en `0_Inbox/NOMBRE.md`."

## Destinos de captura

| Tipo de contenido | Archivo destino |
|-------------------|-----------------|
| Idea suelta / pensamiento | `0_Inbox/Ideas_Sueltas.md` |
| Recurso / URL / herramienta | `0_Inbox/Recursos_Pendientes.md` |
| Tarea / acción futura | `0_Inbox/Tareas_Inbox.md` |
| Decisión tomada | `0_Inbox/Decisiones_Rapidas.md` |
| Extracto / cita / fragmento | `0_Inbox/Extractos.md` |
| Captura de sesión de trabajo | Daily note del día (`0_Inbox/Daily_Logs/YYYY-MM-DD.md`) |

Si el archivo no existe, crearlo con cabecera mínima.

## Formato de entrada en el archivo

```markdown
## YYYY-MM-DD HH:MM — [contexto breve]

[Contenido capturado tal cual]

<!-- pendiente procesar -->
```

El separador `<!-- pendiente procesar -->` permite al skill `obsidian-inbox` identificar qué entradas no han sido procesadas.

## Plantilla inicial para archivos de inbox

Si el archivo destino no existe:

```markdown
# [Nombre del archivo]

Inbox de capturas rápidas. Procesar con `/inbox`.

---
```

## Reglas

*   NO crear notas permanentes durante la captura — solo apuntar en inbox.
*   NO añadir tags, enlaces ni estructura — eso es post-procesado.
*   NO preguntar al usuario dónde va la captura — inferirlo del contenido.
*   SÍ añadir timestamp (fecha + hora) a cada entrada.
*   Si el usuario da varias ideas de golpe, capturarlas todas en la misma sesión.

## Activación implícita

Si durante una conversación el usuario dice algo como "Oye, apunta que también quiero..." o "Luego miro esto...", capturar sin interrumpir el flujo principal:
1. Hacer la captura silenciosamente.
2. Confirmar en una línea: "Capturado en inbox."
3. Continuar con el tema principal.
