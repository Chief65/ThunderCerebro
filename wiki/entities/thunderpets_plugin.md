# ThunderPets - Plugin de Mascotas Cosméticas

**Tipo**: Entidad / Plugin Custom Bukkit-Paper  
**Versión**: 1.0.0 (Build 3 - Egg & Quality System)  
**Compatibilidad**: Minecraft Java 1.21.1+ (Paper / Purpur)  
**Ubicación de Código**: [`creator/lab/thunderpets/`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/lab/thunderpets/)  
**Binario Compilado**: [`creator/output/ThunderPets-1.0.0.jar`](file:///C:/Users/PC/Desktop/ThunderCerebro/creator/output/ThunderPets-1.0.0.jar)  
**Despliegue Remoto**: Servidor de Pruebas (`ymykh9qy.274758bd`) en `/plugins/ThunderPets-1.0.0.jar`

---

## 1. Propósito y Alcance

Plugin cosmético ligero orientado a acompañantes flotantes sin IA ni pathfinding pesado para mitigar impacto en MSPT. Diseñado bajo tres categorías de cosméticos y un sistema de incubación/cuidado de huevos:
1. **Fase 1 (Básica)**: Cabeza flotante pura al costado del jugador sin efectos ni oscilación (ideal para regalo masivo a novatos).
2. **Fase 2 (Exclusiva)**: Cabeza flotante con movimiento senoidal de levitación suave (`sin(t)`) y partículas sutiles de cerezo/aura.
3. **Fase 3 (Medio Personaje / Mini Guardián)**: Medio cuerpo con armadura trim (`ArmorTrim`), cabeza de Baby Yoda en cápsula y objeto sostenido en la mano principal (ej. Tótem de la Inmortalidad) con estela de partículas místicas.

---

## 2. Sistema de Calidades Canónicas y Techos de Nivel

Integrado con el estándar oficial de ThunderMC (`estandar-calidades-items.md`) mediante degradados RGB y barras de estrellas:
- **SUPER** (`&#3CDB10`): `&8⁂ &#4BFD00&lS&#47F504&lU&#44EC08&lP&#40E40C&lE&#3CDB10&lR &e⭐&7⭐⭐⭐⭐` | Techo Nivel 20 (Fase 1)
- **RARA** (`&#1DC8FF`): `&8⁂ &#008DFF&lR&#0AA1FF&lA&#13B4FF&lR&#1DC8FF&lA &e⭐⭐&7⭐⭐⭐` | Techo Nivel 40 (Fase 1)
- **EPICA** (`&#732AE2`): `&8⁂ &#A84EDE&lE&#9B45DF&lP&#8E3CE0&lI&#8033E1&lC&#732AE2&lA &e⭐⭐⭐&7⭐⭐` | Techo Nivel 60 (Fase 2)
- **MITICA** (`&#D02626`): `&8⁂ &#B01111&lM&#B61515&lI&#BD1919&lT&#C31E1E&lI&#CA2222&lC&#D02626&lA &e⭐⭐⭐⭐&7⭐` | Techo Nivel 80 (Fase 2 / Fase 3 básica)
- **DIVINA** (`&#EFFF00`): `&8⁂ &#FD9A00&lD&#FAAE00&lI&#F7C200&lV&#F5D700&lI&#F2EB00&lN&#EFFF00&lA &e⭐⭐⭐⭐⭐` | Techo Nivel 100 (Fase 3)
- **LIMITED** (`&#5489FF`): `&8⁂ &#FF4B4B&l¡&#FF8B2D&lL&#FFD031&lI&#DCFF39&lM&#A5FF3F&lI&#6DFF45&lT&#3BFFC7&lE&#58D0FF&lD&#5489FF&l! ...` | Techo Nivel 120 (Fase 3 premium)

---

## 3. Sistema de Huevos y Misiones de Cuidado (*Adopt Me Loop*)

En Crates y recompensas de Tebex se entregan **Huevos de Mascota** sellados con datos persistentes en `PersistentDataContainer` (NBT). Cada huevo exige 3 tareas antes de eclosionar:
1. **Alimentación / Cariño**: Clic derecho con cualquier alimento comestible vanilla en inventario o mano secundaria (consume 1 comida, emite corazones y sonido).
2. **Protección**: Derrotar $X$ monstruos hostiles (zombis, esqueletos, etc.) llevando el huevo en el inventario.
3. **Incubación por Tiempo**: Permanecer $Y$ minutos conectado en el servidor (computado en background cada 60 segundos con cero impacto en tick).

### Prevención y Seguridad (Red Teaming):
- **Anti-Place Estricto**: Cancelación en `PlayerInteractEvent` y `BlockPlaceEvent` para impedir que el huevo sea colocado como bloque en el mundo.
- **Eclosión In-Game**: Al cumplir las 3 tareas, el huevo brilla con encantamiento (`glint`); al hacer clic derecho, se consume, detona fuegos artificiales/tótem y otorga la mascota correspondiente a su calidad.
- **Poción de Incubación Rápida**: Consumible alquímico para usuarios VIP que madura el huevo al 100% de inmediato.

---

## 4. Arquitectura Técnica y Rendimiento

- **Entidad Base**: `ArmorStand` pequeño (`small: true`), invisible (`invisible: true`), sin gravedad (`gravity: false`), sin colisiones y sin hitbox (`marker: true`).
- **Persistencia**: `setPersistent(false)` estricto para evitar entidades huérfanas en disco en reinicios/crashes.
- **Motor Dirty Checking**: Omite el 100% de los paquetes de teletransporte en reposo si el jugador no se ha movido (`delta < 0.02` bloques), ahorrando miles de paquetes de red en áreas de alta densidad.
- **Seguimiento Suave**: Descomposición trigonométrica de `Yaw` con *lerp* 0.25 y teletransporte de seguridad si la distancia supera 20 bloques.

---

## 5. Comandos Administrativos y de Integración con Crates

- `/pets` (alias: `/pet`, `/mascotas`): Abre el menú GUI interactivo.
- `/pets reload`: Recarga configuraciones en memoria.
- `/pets giveegg <jugador> <calidad> [kills] [minutos]`: Otorga un huevo con tareas personalizadas (ideal para configurar comandos en plugins de Crates: `pets giveegg %player% EPICA`).
- `/pets giveaccelerator <jugador>`: Otorga la Poción de Incubación Rápida.
