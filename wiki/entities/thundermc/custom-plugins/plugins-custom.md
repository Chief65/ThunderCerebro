# 🧩 Plugins Custom — ThunderMC Survival

Documentación de los plugins desarrollados a medida para la network de ThunderMC.

---

## 1. EnderChestPlus (EnderChestPlus-1.0.jar)
- **Tipo**: Custom
- **Propósito**: Extensión del cofre de ender vanilla mediante páginas múltiples asignadas por rangos/permisos (enderchestplus.page.1, enderchestplus.page.2, etc.).
- **Puntos Críticos de Auditoría**:
  - **Serialización NBT**: Al combinarse con `ExecutableItems` e `ItemEdit`, el método de guardado debe preservar todas las tags compuestas (PersistentDataContainer y NBT crudo) para evitar reseteos de habilidades o duplicación de ítems en caídas de servidor.
  - **Bloqueo durante combate**: Integración con `PvPManager` para evitar apertura de baúles en estado de combate.

---

## 2. RankUp / Ranks (RankUp-1.0.jar)
- **Tipo**: Custom
- **Propósito**: Progresión de rangos de supervivencia mediante pago de moneda (Vault) y cumplimiento de requisitos de estadísticas (tiempo jugado, bloques minados, etc.).
- **Puntos Críticos de Auditoría**:
  - **Concurrencia en compra**: Debe existir un bloqueo tras pulsar el botón de ascenso para prevenir que transacciones simultáneas cobren dos veces o asignen permisos de forma errática en `LuckPerms`.
  - **Sincronización con LuckPerms**: Invocación de API interna o comandos seguros `lp user %player% parent add/set`.

---

## 3. ValyrTutorial (ValyrTutorial-3.0.jar)
- **Tipo**: Custom
- **Propósito**: Sistema de bienvenida guiado para nuevos jugadores (onboarding/spawn interactivo).
- **Puntos Críticos de Auditoría**:
  - **Compatibilidad Bedrock (Floodgate)**: Validar que los diálogos, títulos o bloqueos de cámara no congelen al cliente de móvil o consola de Bedrock al ingresar.
  - **Reingreso seguro**: Comprobar que tras completar el tutorial o reconectarse a mitad de flujo, el jugador sea enviado siempre a la coordenada del spawn seguro sin bypass de regiones.

---

## 4. ThunderMines (ThunderMines-1.9.dis)
- **Estado**: Desactivado / Archivado.
- **Motivo**: Reemplazado íntegramente por `CataMines-2.5.11` debido al rendimiento superior de reseteo asíncrono y soporte de zonas PvP/regiones WorldGuard.
