# Desglose de Fuente: SmartSpawner v1.6.6

**Fuente**: Documentación oficial (`https://docs.smartspawner.site/docs/`) y archivos de configuración extraídos del Sandbox (`plugins/SmartSpawner/`).  
**Fecha de Ingesta**: 2026-09-13  
**Entorno**: Paper 1.21.11 (Java compatible, versión 1.6.6).

---

## 1. Arquitectura Técnica de SmartSpawner

SmartSpawner sustituye el spawning y cálculo de entidades vivas de Minecraft vanilla por un **modelo de Spawner Virtual / Almacenamiento Interno (GUI)**:
1. **Zero Entity Lag**: Los spawners no generan entidades físicas en el mundo si no se desea; acumulan drops y experiencia directamente en un inventario interno paginado de 45 slots.
2. **Apilamiento (Stacking)**: Permite concentrar hasta `max_stack_size: 10000` spawners en un solo bloque, multiplicando la tasa de generación sin multiplicar el número de bloques ni el tick de chunks.
3. **Mecánica de Recolección (Breaking)**:
   - Requiere herramientas específicas (Hierro, Oro, Diamante, Netherite).
   - Requiere encantamiento Toque de Seda (`silk_touch.required: true`, nivel 1).
   - Auto-venta y reclamo de XP automático al romper el spawner si se retira por completo.
4. **Venta Integrada (Economy Integration)**:
   - Modos de precio: `SHOP_PRIORITY`, `SHOP_ONLY`, `CUSTOM_ONLY`, `CUSTOM_PRIORITY`.
   - Compatible nativamente con Vault, ShopGUI+ y precios manuales en `item_prices.yml`.
   - Soporte Bedrock nativo mediante FormUI a través de Floodgate.

---

## 2. Archivos Clave del Plugin

| Archivo | Función Principal |
|---|---|
| [`config.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/raw/thunderia/SmartSpawner/config.yml) | Parámetros globales de spawn (delays, almacenamiento, Silk Touch, economía, hologramas, base de datos). |
| [`spawners_settings.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/raw/thunderia/SmartSpawner/spawners_settings.yml) | Tabla de drops y experiencia generada por mob (Allay hasta Zombie). |
| [`item_spawners_settings.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/raw/thunderia/SmartSpawner/item_spawners_settings.yml) | Spawners especiales de bloques/minerales (Iron, Gold, etc.). |
| [`item_prices.yml`](file:///C:/Users/tecno/Desktop/ThunderCerebro/raw/thunderia/SmartSpawner/item_prices.yml) | Lista de precios fijos de venta para el botón "Sell All" del GUI. |
| `spawners_data.yml` / `spawners.db` | Persistencia de coordenadas, dueños, niveles y drops almacenados de cada spawner. |

---

## 3. Comandos y Permisos Principales

- `/smartspawner give <jugador> <mob> [cantidad]`: Comando vital para entregar spawners desde DeluxeMenus o cajas.
- `/smartspawner reload`: Recarga de configuraciones y tablas de precios.
- `/smartspawner list`: Visor administrativo de spawners colocados por mundo/chunk.
- Permisos:
  - `smartspawner.use`: Abrir GUI e interactuar con el spawner.
  - `smartspawner.break`: Romper y recuperar el spawner.
  - `smartspawner.stack`: Apilar spawners con la mano o mediante GUI.
  - `smartspawner.sellall`: Vender drops directamente desde la interfaz.

---

## Referencias Cruzadas
- [[wiki/synthesis/optimizacion-granjas-survival|OptimizaciÃ³n Granjas Survival]]
- [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra ThunderMC]]
- [[wiki/entities/thundermc/ecosistema-plugins|Ecosistema Plugins]]
