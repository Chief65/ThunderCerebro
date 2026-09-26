# Perfil y Patrones de Diseño Visual: Sr Ramos (Thunderverse UI/UX)

Documento maestro de directrices estilísticas y heurísticas de decisión para diseño de GUIs, chats, broadcasts y tipografía.

---

## 1. Filosofía de Diseño y Reglas Estéticas Clave

1. **Compacidad y Proporción Cuadrada:**
   * Las estructuras deben ser visualmente cuadradas y simétricas (relación 1:1 real en píxeles de Minecraft).
   * Para bloques sólidos █, la resolución de oro es **7 bloques de ancho x 7 líneas de alto**, ya que el ancho impar (7) permite un eje/centro matemático perfecto de 1 bloque.
2. **Textura Sólida y Limpia:**
   * Prohibido el uso de símbolos con espacios intermedios o líneas finas (■, ─, │, /, \) que generen ruido o se deformen con fuentes no monospace.
   * Uso exclusivo de bloques completos █ (U+2588) para conseguir superficies continuas sin fisuras.
3. **Tipografía y Legibilidad:**
   * **Títulos:** Texto limpio sin negrita estridente (<bold>), utilizando colores *flat* hexadecimales con personalidad y de alto contraste (ej: Ámbar #FFB800, Blurple #5865F2, Cian #00e5ff, Oro #FFD700) acompañados de un símbolo o emoji acorde (✦, 👥, ☠, ⛏, 👑).
   * **Cuerpo de Información:** Texto corto, conciso y directo en **blanco puro** (<white>), evitando párrafos largos que desborden horizontalmente.
   * **Llamadas a la Acción (CTA):** Sutiles, discretos y en color gris (<gray>Click para abrir enlace</gray>), situados inmediatamente encima del comando/enlace sin corchetes ni estridencias.
   * **Enlaces y Comandos:** Siempre destacados en color **amarillo** (<yellow><u>enlace</u></yellow>), con eliminación de subtítulos redundantes en la base.
4. **Acústica y Feedback:**
   * Sonidos no invasivos, sutiles y elegantes para notificaciones (lock.note_block.chime en lugar de fanfare/levelup/orbs estridentes).
5. **Figuración Simbólica Directa:**
   * Las ilustraciones en pixel-art deben representar el concepto canónico directo del juego o servicio (ej: Cofre de madera con pestillo central, Calavera Bad Omen de 3 patas, Cueva con viga de madera y diamante, Corona imperial ancha con gemas).