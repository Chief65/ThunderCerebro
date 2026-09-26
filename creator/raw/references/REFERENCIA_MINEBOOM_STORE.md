# Ingesta y Análisis Técnico: MineBoom Store (tienda.mineboom.org)

## 1. Identidad y Componentes Extraídos

### A. Botón de Selección de Categoría (`categorySelector`)
* **Ubicación**: En la parte superior de la columna de navegación / sidebar.
* **Comportamiento**: Disparador de modal/menú interactivo para seleccionar categorías con tarjetas visuales.
* **Estructura Visual**:
  * Icono de cofre/tienda destacado a la izquierda.
  * Texto en 2 líneas:
    * Línea 1 (Subtítulo): *"HAZ CLIC AQUÍ PARA"*
    * Línea 2 (Título): *"SELECCIONAR CATEGORÍA"*
  * Micro-hover suave con acento de color amarillo.

### B. Slider / Banner de Descuento Activo
* **Formato**: Carrusel animado / ticker horizontal en cabecera que muestra:
  * Porcentaje de descuento activo (ej: `⚡ -30% DE DESCUENTO EN TODA LA TIENDA`).
  * Contador regresivo de expiración de oferta (*"Finaliza en 02d 14h 22m"*).
  * Botón directo de acción ("Aprovechar Descuento").
