# Noera v1.3.0

## Actualizar una instalación existente

1. Cierra la ventana de PowerShell de Noera.
2. Haz una copia de tu carpeta de Noera antes de actualizar.
3. Copia `iniciar-noera.bat`, los archivos de `_app` y, si los quieres, `_tests`, `_LEEME.md` y `_REVISION.md` a tu instalación. **Conserva tu propio `_app/metadata.json`** para mantener etiquetas e historial. El ZIP incluye el mismo metadata.json aportado, sin modificar.
4. Ejecuta `iniciar-noera.bat` y recarga el navegador. No necesita instalar paquetes para funcionar.

Requiere Windows con Windows PowerShell 5.1 y un navegador moderno. El servidor sigue escuchando exclusivamente en `127.0.0.1`, empezando por el puerto 7710.

## Descargar con clic derecho

- En un archivo: **Descargar archivo**.
- En una carpeta: **Descargar como ZIP**.
- Disponible en el árbol lateral, tarjetas y filas del panel central.
- Teclado: enfoca un elemento y pulsa **Shift+F10** o la tecla de menú contextual; usa flechas y Enter.
- También hay un botón de descarga en la barra del archivo abierto. Descarga la versión en disco; guarda primero si quieres incluir cambios pendientes del editor.

Noera conserva su enfoque de editor de texto: se muestran y gestionan las extensiones de la lista original. Un archivo no UTF-8 o demasiado grande para editar se puede descargar si su extensión está permitida. Los ZIP de carpetas incluyen también sus recursos binarios, archivos ocultos y carpetas vacías; en la exportación de la raíz se excluyen las carpetas reservadas y los elementos cuyo nombre empieza por punto o guion bajo.

## Actualizar un proyecto con ZIP

El ZIP debe llamarse igual que la carpeta. Admite contenido directamente o una única carpeta contenedora con ese mismo nombre. Se valida y extrae en una ubicación temporal antes de sustituir el original. La versión anterior se respalda completa en `.history` y se conserva como directorio durante la sustitución. Si falla antes de confirmar metadatos, se intenta recuperar el directorio original.

Límites: 25 MB por subida individual, 150 MB por ZIP recibido, 1 GB descomprimido y 20 000 entradas. Un ZIP vacío, rutas peligrosas, nombres duplicados sin distinguir mayúsculas y enlaces simbólicos se rechazan. Un proyecto con enlaces o uniones requiere quitarlos antes de exportarlo o actualizarlo: el backup falla de forma explícita para no guardar una copia incompleta.

## Pruebas

Para ejecutar las pruebas del backend en Windows, desde la carpeta de Noera:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\_tests\backend.Tests.ps1
```

No inicia Noera ni modifica tus proyectos: crea y elimina una carpeta temporal. Estas pruebas se incluyen para ejecutar en Windows; **no se ejecutaron en el entorno de esta revisión**.

Las pruebas del frontend se ejecutaron en Chromium con API simulada. Para repetirlas necesitas Node.js y Playwright, instalados en una carpeta de pruebas:

```text
npm install playwright
npx playwright install chromium
node _tests/frontend.Tests.cjs
```

Puedes indicar un Chromium existente mediante la variable `NOERA_BROWSER_PATH`. El archivo de prueba sirve la interfaz original y simula las respuestas HTTP; no sustituye las pruebas del servidor real.

Consulta `_REVISION.md` para ver evidencia, correcciones y límites de validación.
