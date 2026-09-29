# 🛡️ Diagnóstico Técnico y Plan de Optimización Survival (Minecraft 1.21.11)
**Fecha**: 2 de septiembre de 2026  
**Servidor**: ThunderMC Survival (`MIA-251006.bloom.host:2022`)  
**Objetivo**: Resolver colapso de MSPT (13ms → 33ms) y sobrecarga de entidades generadas por macro-granjas de spawners.

---

## 1. Diagnóstico del Setup Actual (Causas Críticas)

1. **Inexistencia de plugin de Stacking de Mobs / Spawners**:
   - Actualmente solo opera `SilkSpawners_v2.jar` (solo maneja picar/colocar spawners sin control de chunks ni apilado).
   - Los jugadores colocan hasta 8+ spawners en la intersección de 4 chunks y canalizan todo a un solo punto de caída. Cada spawner genera entidades vanilla individuales (hasta 50+ mobs simultáneos con colisiones, pathfinding e IA activa).
2. **Inconsistencia entre Spigot y Paper (`spigot.yml` vs `paper-world-defaults.yml`)**:
   - En `spigot.yml`: `nerf-spawner-mobs: true`.
   - En `paper-world-defaults.yml`: `spawner-nerfed-mobs-should-jump: true` (los mobs en corrientes de agua siguen ejecutando cálculos de física, colisiones y saltos por tick).
3. **`player-idle-timeout=0` en `server.properties`**:
   - AFK Kick totalmente deshabilitado. Los jugadores mantienen cuentas 24/7 en las macro-granjas, acumulando entidades y manteniendo chunks cargados permanentemente (el tiempo AFK subió al 41% del playtime).
4. **Rangos de Tracking y Activation elevados (+100 CCU)**:
   - `entity-tracking-range` de monstruos y animales en 48 bloques.
   - `entity-activation-range` de monstruos en 24, y raiders/flying en 48.
   - `item-despawn-rate` en 4000 ticks (3.3 min) sin limpieza rápida (`alt-item-despawn-rate`) para basura de granjas (huesos, flechas, podredumbre).
5. **`hopper.disable-move-event: false` en `paper-world-defaults.yml`**:
   - Disparo constante de eventos `InventoryMoveItemEvent` en las tolvas de recolección de granjas.

---

## 2. Plan de Cambios y Configuración a Desplegar

### A. Migración de Spawners & Mob Stacking (Modelo DiosesMC)
* **Recomendación**: Instalar **RoseStacker** (o **StackMob**).
* **Mecánica**:
  - Spawners apilables en 1 solo bloque físico (ej. `Generador de Esqueletos x8`).
  - Mobs generados apilados en 1 sola entidad (ej. `[x35] Esqueleto`).
  - Muerte en lote / muerte instantánea de stacks al recibir daño masivo.
  - Reemplazo definitivo de `SilkSpawners_v2`.

### B. `config/paper-world-defaults.yml`
```yaml
entities:
  behavior:
    spawner-nerfed-mobs-should-jump: false
    mobs-can-always-pick-up-loot:
      skeletons: false
      zombies: false

  spawning:
    alt-item-despawn-rate:
      enabled: true
      items:
        rotten_flesh: 1200      # 1 min
        bone: 1200
        arrow: 600              # 30 seg
        string: 1200
        spider_eye: 1200
        gunpowder: 2400

hopper:
  disable-move-event: true
  ignore-occluding-blocks: true
```

### C. `spigot.yml`
```yaml
world-settings:
  default:
    merge-radius:
      item: 4.5       # Actual: 3.5
      exp: 6.0        # Actual: 4.0
    item-despawn-rate: 3000   # Actual: 4000

    entity-activation-range:
      animals: 12     # Actual: 16
      monsters: 16    # Actual: 24
      raiders: 24     # Actual: 48
      misc: 6         # Actual: 8
      water: 6        # Actual: 8
      villagers: 12   # Actual: 16
      flying-monsters: 24  # Actual: 48

    entity-tracking-range:
      monsters: 32    # Actual: 48
      animals: 32     # Actual: 48
      misc: 16        # Actual: 32
      other: 32       # Actual: 64
```

### D. `server.properties`
```properties
player-idle-timeout=30
```

---

## 3. Tareas Pendientes para Mañana

- [ ] Probar configs y plugin de stacking en Sandbox / Servidor de Pruebas (`ymykh9qy.274758bd`).
- [ ] Aplicar configuraciones en `paper-world-defaults.yml`, `spigot.yml` y `server.properties` en el Survival.
- [ ] Decidir plugin de Stacking (RoseStacker vs StackMob) e instalar.
- [ ] Auditar in-game las granjas de los jugadores top kills (`jackp121`, `davidg4mer99H`, `ThunggThungg`).

---

## Referencias Cruzadas
- [[wiki/synthesis/thundermc-master-synthesis|SÃ­ntesis Maestra ThunderMC]]
- [[wiki/entities/thundermc/infraestructura-hardware|Infraestructura Hardware]]
- [[wiki/entities/thundermc/core-infrastructure/plan|Plan (Player Analytics)]]
- [[wiki/sources/smartspawner/desglose_smartspawner_v1_6_6|Desglose SmartSpawner]]
- [[wiki/concepts/mercadothunder|Mercado Thunder]]
