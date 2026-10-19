# Revisión de Noera — v1.3.0

Fecha: 15 de octubre de 2026.

## Alcance y criterio

Se revisaron los siete archivos del ZIP original: lanzador, servidor PowerShell, JavaScript, CSS, HTML, metadatos y changelog. El texto adjunto se titula «Experto Tebex Webstore — Sistema Router + Especialistas Tebex (v1)». Noera es una aplicación local con HttpListener y JavaScript sin dependencias, no una tienda Twig. Se aplican sus criterios de evidencia, implementación completa y validación; sus reglas específicas de checkout y Minecraft no corresponden a este software.

Los hallazgos de la tabla son **[OBSERVADO] [EDITABLE]**, con confianza ALTA en la evidencia de código. Las líneas de origen se refieren al ZIP recibido; las referencias de solución se refieren al código entregado. Implementar un cambio no demuestra por sí mismo que funciona en Windows.

## Hallazgos y correcciones

| Prioridad | Evidencia en el original | Consecuencia | Cambio entregado |
|---|---|---|---|
| Crítica | `_app/app.js:505`: `else v.append(fileView());`; no existe ninguna declaración de `fileView` en el archivo | Abrir un archivo termina en ReferenceError | `_app/app.js`, función `fileView`: lector Markdown, lector literal y textarea con estado de cambios |
| Alta | `_app/app.js:36`: `Object.entries(attrs)`; hay llamadas como `el('div', null, ...)` en el visor del código | TypeError al construir ese apartado | `el`: usa `Object.entries(attrs || {})` |
| Crítica | `_app/server.ps1:516`: `... Remove-Item -Recurse -Force`, seguido de movimientos desde la extracción | Un fallo tras borrar puede dejar un proyecto incompleto | Endpoint `POST /api/folder/update-zip`: staging, backup, movimiento del original a reserva y recuperación ante excepciones previas al commit |
| Alta | `_app/server.ps1:158` y siguientes: el backup filtra por `$AllowedExt`; línea 169: `catch { }` | Imágenes, fuentes, archivos ocultos o archivos ilegibles pueden faltar en la copia anterior | `Write-FolderToZip` incluye todos los archivos internos, crea entradas de directorio y propaga errores; copia por streams |
| Alta | `_app/server.ps1:109`, `Resolve-Rel`: comprueba prefijo textual sin recorrer atributos de los componentes | Una unión o enlace dentro de la raíz puede atravesar el límite lógico | `Assert-NoReparse` comprueba cada componente; se aplica a rutas de trabajo, copias, papelera e historial |
| Alta | `_app/server.ps1:508`: extracción directa sin validación propia de entradas o tamaño expandido | No hay límites de expansión ni política explícita de colisiones y nombres Windows | `Expand-ValidatedZip`: rechaza traversal, rutas absolutas, dispositivos, alias, duplicados y symlinks; límites declarados y efectivos durante la extracción |
| Alta | `_app/app.js:697`: `c.dirty = false` al finalizar la petición | Puede marcar como guardada una edición posterior al inicio del PUT | `save` captura el texto enviado y compara con el texto actual; evita guardados simultáneos y conserva cambios pendientes |
| Alta | `_app/app.js`, `select`: asigna `S.cur` tras `await api(...)` sin validar la selección vigente | Una respuesta tardía puede mostrar el archivo anterior bajo otra selección | Contador `selectionSeq` para descartar respuestas obsoletas |
| Media | `_app/app.js:18`: `JSON.parse(localStorage.getItem(...))` al iniciar | Un valor corrupto impide arrancar toda la interfaz | `readExpanded` valida tipo y captura errores; persistencia opcional |
| Alta | `_app/server.ps1:31` oculta errores al leer metadatos; línea 38 escribe directamente sobre el JSON | Historial vacío ante corrupción o JSON truncado si falla una escritura | Lectura que informa del error y `Write-AtomicText` con temporal y reemplazo |
| Media | Endpoints originales rename y move mueven carpetas sin remapear `taggedFolders` | Se pierden visualmente etiquetas e historial al cambiar ruta | `Move-FolderMeta` remapea claves y conserva `backupRel` original; fallo de metadatos intenta revertir movimiento |
| Media | `_app/app.js:417,464`: render vuelve a cargar cuando la lista está vacía; catch devuelve lista vacía | Reintentos automáticos indefinidos ante fallo o historial vacío | Estados de carga completada/error y botón de reintento; pestañas siguen accesibles |
| Media | `_app/app.js`, `inline`: crea enlaces HTML antes de aplicar regex de formato a toda la cadena | `**` o `~~` dentro de una URL pueden alterar el atributo href | Enlaces y código se aíslan en tokens antes del formato; se escapan texto y atributos |
| Media | `_app/server.ps1:58`: CSP solo permite estilos de `self`; la interfaz usa atributos `style` | Se bloquean estilos inline de la propia aplicación | CSP permite estilos inline; mantiene scripts solo de `self` y no permite scripts inline |
| Media | `_app/app.js`, cola: 25 MB en interfaz; servidor admite 150 MB para subida individual | Límites incoherentes y revalidación incompleta al editar un nombre inválido | Límite backend individual de 25 MB y revalidación del tamaño al subir |
| Media | `_app/server.ps1`, guardado: vuelve a escribir UTF-8 sin mantener la marca BOM; no hay implementación de editor en el original | Pérdida de convención de codificación; faltaba controlar EOL al restaurar el editor | Se mantiene BOM UTF-8 existente; el editor conserva la convención CRLF predominante |
| Media | `_app/server.ps1`, descarga del código: enumera todos los archivos de `_app` | Puede empaquetar temporales de una operación fallida | Lista explícita de fuente, documentación y pruebas; ZIP temporal en disco |

El servidor conserva la validación de Host y token por cabecera. Se elimina el token por query string y se rechazan orígenes externos en API. Los nombres de descarga usan `filename*` UTF-8. Los ZIP de carpetas, del código y los respaldos se envían por streams, reduciendo la duplicación del archivo completo en memoria. Las subidas siguen almacenándose en memoria hasta sus límites; el servidor mantiene su arquitectura secuencial.

## Función solicitada

**[OBSERVADO]** El menú del árbol original ya permitía descargar carpetas ZIP, pero no archivos; el panel central no tenía ese menú. Se añade descarga individual mediante `GET /api/download`, menú contextual a tarjetas y filas, descarga en barra del archivo y acceso por teclado. La descarga usa la versión guardada en disco. No se amplía la lista de extensiones del editor.

## Validación realizada

**[OBSERVADO] Ejecutado:**

- `node --check` sobre `app.js` y el archivo de pruebas del frontend.
- Parser Tree-sitter de PowerShell sobre `server.ps1` y las pruebas: sin nodos de error ni tokens faltantes. No equivale al parser oficial de Windows PowerShell.
- Chromium real con HTML, CSS y JS entregados y API simulada: arranque con localStorage inválido; descargas desde tarjeta, lista y árbol; lector y editor; cambios durante guardado; CRLF; respuestas de selección fuera de orden; HTML escapado y URLs con marcadores de formato; fallo sin bucle de solicitudes; historial vacío; reintento de carga del código; menú por teclado y ajuste a pantalla de 390 × 700. Sin excepciones JavaScript observadas durante esos escenarios.
- Integridad del ZIP final y de los JSON; se conserva byte a byte el metadata.json aportado.

**[NO PROBADO] [POR VERIFICAR]:** ejecución de HttpListener, rutas NTFS, permisos, File.Replace, enlaces y uniones reales, descargas mediante el servidor PowerShell y ciclo completo de actualización/recuperación en Windows. El entorno de revisión no dispone de PowerShell ni Windows. `_tests/backend.Tests.ps1` usa las funciones reales extraídas con el parser de PowerShell y prepara casos temporales de rutas, ZIP y metadatos; queda pendiente ejecutarlo allí.

## Límites y recuperación

- La sustitución usa varias operaciones de filesystem; **no es una transacción atómica frente a corte de corriente o cierre forzado del proceso**. Si se interrumpe entre movimientos, el directorio anterior puede quedar en `.history/<ruta>/original_<id>`. Con Noera cerrado, consérvalo y muévelo de vuelta a su ruta si esta falta, o recupera el ZIP `backup_<id>_<carpeta>.zip`. No sobrescribas una versión existente sin comparar.
- La recuperación por excepciones está implementada, pero puede fallar si cambian permisos, quedan archivos bloqueados o hay errores de disco. No se ha probado inyección de esos fallos en Windows.
- Los cambios realizados por programas externos durante una copia o la ventana final de reemplazo no están bloqueados de forma transaccional. Cierra editores externos durante despliegues ZIP y conserva una copia independiente de proyectos importantes.
- El servidor es secuencial: empaquetar o extraer un proyecto grande bloquea otras peticiones hasta terminar. El streaming reduce memoria, no convierte estas operaciones en asíncronas.
- Los backups ahora preservan el contenido de archivos y directorios, incluidos recursos y archivos ocultos internos. No son imágenes de disco ni garantizan ACL, alternate data streams u otros metadatos NTFS.
- Se conserva sin inventar ni reparar el registro histórico que venía en metadata.json. Los archivos reales que ese registro referencia no se incluyeron en el ZIP recibido.
- Las marcas de commits antiguas se conservan del changelog original. `local-v1.3.0` es un identificador de revisión local, no un hash Git.
