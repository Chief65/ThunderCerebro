# 🛡️ WorldGuard - Documentación Técnica

- **Categoría**: Protección Espacial / Motor de Regiones y Flags
- **Versión Core Soportada**: Minecraft 1.20.x - 1.21.x (Paper / Purpur)
- **Desarrollador**: EngineHub (sk89q, wizjany, me4502)
- **Dependencias**: WorldEdit / FastAsyncWorldEdit (FAWE) (Obligatoria)
- **Ruta de Configuración**: `plugins/WorldGuard/`

---

## 🏛️ 1. Arquitectura y Funcionamiento Interno

WorldGuard es el estándar de la industria para la gestión de regiones volumétricas (Cuboide / Poligonal) en servidores Minecraft, utilizando un árbol de prioridades e índices espaciales en memoria (R-Tree / Spatial Index) para resolver instantáneamente intersecciones de eventos de bloques, entidades y jugadores.

```mermaid
flowchart TD
    A[Evento Bukkit: BlockBreak, EntityDamage, Move, Interact] --> B[WorldGuard Spatial Index: Query(Location)]
    B --> C{¿Hay Regiones en las Coordenadas?}
    C -- No --> D[Aplicar Flags de la Región Global '__global__']
    C -- Sí --> E[Ordenar Regiones por Prioridad Numérica Descendente]
    E --> F[Evaluar Flags de Mayor Prioridad: allow / deny]
    F --> G{¿El Jugador es Dueño / Miembro / Tiene Bypass?}
    G -- Sí --> H[Permitir Acción]
    G -- No --> I[Aplicar Denegación & Cancelar Evento Bukkit]
```

### Conceptos Clave:
1. **Región `__global__`**:
   - Aplica reglas para todo el mundo si no hay regiones locales específicas presentes.
2. **Jerarquía y Herencia de Regiones**:
   - Propiedad `parent` para heredar configuraciones de regiones madre (ej: distrito comercial dentro de una ciudad protegida).
3. **Prioridad Numérica**:
   - Números enteros superiores ganan frente a prioridades menores ante conflictos de flags.

---

## ⚙️ 2. Configuración Crítica (`worlds/world/regions.yml`)

Ejemplo de configuración de región de Spawn:

```yaml
regions:
  spawn_principal:
    min: {x: -150, y: -64, z: -150}
    max: {x: 150, y: 320, z: 150}
    members: {}
    flags:
      pvp: deny
      mob-spawning: deny
      creeper-explosion: deny
      tnt: deny
      fire-spread: deny
      other-explosion: deny
      lava-flow: deny
      water-flow: allow
      chest-access: deny
      use: allow
      greeting: "&aBienvenido al Spawn Principal de ThunderMC"
      farewell: "&cHas salido de la zona protegida del Spawn"
    owners:
      groups:
        - "admin"
    type: "cuboid"
    priority: 100
```

---

## 💻 3. Comandos y Jerarquía de Permisos

### Comandos Principales:
| Comando | Descripción | Permiso |
| :--- | :--- | :--- |
| `/rg define <nombre>` | Define una nueva región a partir de la selección de WorldEdit. | `worldguard.region.define` |
| `/rg redefine <nombre>` | Actualiza las dimensiones de una región existente. | `worldguard.region.redefine` |
| `/rg flag <nombre> <flag> <valor>` | Modifica una regla o flag en la región indicada. | `worldguard.region.flag` |
| `/rg addowner <nombre> <jugador>` | Asigna un propietario a la región. | `worldguard.region.addowner` |
| `/rg addmember <nombre> <jugador>` | Asigna un miembro colaborador. | `worldguard.region.addmember` |
| `/rg info [nombre]` | Muestra coordenadas, dueños, miembros y flags activas. | `worldguard.region.info` |
| `/rg remove <nombre>` | Elimina la región permanentemente. | `worldguard.region.remove` |
| `/rg reload` | Recarga las regiones y configuraciones desde el disco. | `worldguard.reload` |

### Jerarquía de Permisos:
- `worldguard.admin`: Control total y bypass ilimitado.
- `worldguard.region.bypass.<mundo>`: Ignora todas las protecciones en un mundo específico.

---

## 🧩 4. Integración con PlaceholderAPI (PAPI)

| Placeholder | Descripción |
| :--- | :--- |
| `%worldguard_region_name%` | Nombre de la región principal donde se encuentra el jugador. |
| `%worldguard_region_owner%` | Propietario registrado de la región actual. |
| `%worldguard_region_flag_<flag>%` | Estado de una flag en la ubicación del jugador (`allow`/`deny`). |

---

## 🛡️ 5. Modos de Fallo, Exploits y Rendimiento

> [!CAUTION]
> **Exploits de Proyectiles y Daño Indirecto (Splash Potions / Cristales de End)**:
> Si las flags `potion-splash` o `damage-animals` no están denegadas en spawn, los jugadores pueden arrojar pociones dañinas a entidades pasivas o activar cristales de End con flechas.
> **Mitigación**: Denegar explícitamente `enderpearl: deny`, `splash-potion: deny` y `interact: deny` en spawns.

> [!TIP]
> **Optimización del Spatial Index**:
> Evitar crear miles de regiones individuales sin indexación espacial optimizada; delegar claims de jugadores a plugins como ProtectionStones que optimizan el ciclo de vida de las regiones.
