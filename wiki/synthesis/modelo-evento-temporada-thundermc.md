---
title: "Modelo de Evento de Temporada: Auditoría Multidisciplinar, Red Teaming y Hito Comunitario"
type: synthesis
created: 2026-10-05
updated: 2026-10-05
tags:
  - sintesis
  - thundermc
  - eventos
  - economia
  - red-teaming
  - monetizacion
  - bosses
sources:
  - "[[wiki/entities/thundermc|ThunderMC]]"
  - "[[wiki/concepts/economia-servidor-minecraft|Economía Servidor Minecraft]]"
  - "[[wiki/concepts/monetizacion-modelo-negocio|Modelo de Negocio & Monetización]]"
  - "[[wiki/concepts/estandar-calidades-items|Estándar Oficial de Calidades]]"
---

# Modelo de Evento de Temporada: Auditoría Multidisciplinar, Red Teaming y Hito Comunitario

Documento maestro que compila la arquitectura integral, prompts profesionales de agentes, diagnóstico de riesgos fatales (Red Teaming), blueprint del hito comunitario y modelo de monetización para las temporadas competitivas en **[[wiki/entities/thundermc|ThunderMC]]** (Minecraft 1.21.11).

---

## 1. El Bucle Central de la Temporada (Core Loop)

```text
       [ PASE DE BATALLA ]            [ BOSSES (1H / 24H) ]            [ KOTH DE EVENTO ]
      (Misiones Estacionales)        (Daño por Umbrales)            (PvP Ventana Prime)
                 │                             │                              │
                 ▼                             ▼                              ▼
                 └──────────────────────► [ BANCO DE TOKENS ] ◄─────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
       [ CONSUMO INDIVIDUAL ]                                        [ HITO COMUNITARIO ]
    - Caja de Temporada (Pity 20x)                                    "El Altar de la Falla"
    - Runa de Evolución (Tier I -> II)                               (Donación Colectiva)
    - Llaves Regulares (Cap Semanal)                                           │
                                                                               ▼
                                                                     [ FASES DE DESBLOQUEO ]
                                                                     F1: Boss Horario + Pase
                                                                     F2: Boss 24h (+15% Tokens)
                                                                     F3: Runa en Crate Global
                                                                     F4: Clímax Caos x2 Tokens
```

---

## 2. Prompts de Liderazgo Técnico (Mesa Multidisciplinar)

### A. Systems & Economy Designer (Economía y Sinks)
```markdown
[ROL]: Eres el Lead Economy & Systems Designer de una network competitiva de Minecraft versión 1.21.11.
[OBJETIVO]: Diseñar y balancear el loop económico de una temporada compuesta por: Pase de Batalla, Caja de Temporada, Tokens de Evento, Bosses (1h y 24h), KOTH y un Kit Evolutivo (1 nivel de mejora).
[CONTEXTO TÉCNICO]: 
- Entorno de juego: Survival RPG con economía mixta y PvP activo.
- Moneda estacional: "Tokens de Evento" (no transferibles para evitar multicuentas/boosting).
- Vías de gasto (Sinks): Llaves de caja de temporada, llaves regulares, runas de evolución de armadura, cosméticos.
[TAREAS ESPECÍFICAS]:
1. Modelar la tasa de inflación: Calcula la cantidad exacta de tokens que un jugador Casual (1h/día), Hardcore (5h/día) y un Clan Dominante generarán a lo largo de una temporada de 45 días.
2. Curva del Pase de Batalla: Estructura 50 niveles con progresión no-lineal (curva exponencial suave) para evitar que los jugadores lo completen en la primera semana.
3. Pricing & Sumideros: Fija el coste en tokens para:
   - Llave de evento.
   - Runa de evolución (debe exigir un grind significativo de al menos 3 semanas de juego activo o rendimiento sobresaliente en bosses).
4. Matriz de Conversión: Garantiza que la economía de temporada no devalúe la economía persistente del servidor Survival al finalizar el evento.
[OUTPUT OBLIGATORIO]: Tablas matemáticas con tasas de ganancia horaria, probabilidades de drop estimadas, costes de compra y sumideros obligatorios para drenar el exceso de tokens.
```

### B. Combat & Encounter Designer (Bosses, Oleadas y KOTH)
```markdown
[ROL]: Eres el Lead Combat & Encounter Designer especializado en Minecraft 1.21.11 (usando MythicMobs, ModelEngine o plugins de combate equivalentes).
[OBJETIVO]: Diseñar los encuentros de combate de temporada: Boss Horario (1h), Boss Diario con oleadas (24h) y Arena KOTH de Temporada.
[RESTRICCIONES TÉCNICAS Y DE RENDIMIENTO]:
- Servidor en 1.21.11 con picos de 40 a 80 jugadores en el mismo sector.
- Restricción estricta de MSPT: El boss no puede saturar el tick del servidor con IA redundante o cálculo de pathfinding masivo.
- Cero "cheese": Prevenir safe-spotting (disparar desde alturas inaccesibles, encerrar con bloques, abusar de vallas/bloques transparentes).
[TAREAS ESPECÍFICAS]:
1. Boss Horario (Simple): Diseña un jefe con 3 habilidades telegrafiadas (indicadores visuales con partículas), invulnerable a arcos a larga distancia y con una duración de combate objetivo de 3 a 5 minutos para un grupo de 3-5 jugadores.
2. World Boss Diario (24h - Oleadas): 
   - Fase 1: 100% a 66% HP (Ataques en área y control de masas).
   - Fase 2: 66% a 33% HP (Invulnerabilidad y Spawn de Oleada de Adds con límite estricto de entidades; la siguiente oleada no inicia hasta limpiar la anterior).
   - Fase 3: 33% a 0% HP (Enrage, incremento de daño y proyectiles de esquiva activa).
3. Arena KOTH: Distribución de coberturas y líneas de visión para garantizar dinamismo PvP e impedir la dominación estática por arqueros/snipers.
4. Sistema de Drops Anti-Monopolio: Diseña la fórmula de botín (garantizar recompensas por umbral de daño mínimo para jugadores casuales, y bonus exclusivo al top 3 damagers).
```

### C. Minecraft Technical Lead & Config Architect (Paper 1.21.11, NBT y Seguridad)
```markdown
[ROL]: Eres el Principal Minecraft Systems Architect (Paper/Purpur 1.21.11).
[OBJETIVO]: Configurar e interconectar la infraestructura de plugins para la temporada (Pase, Cajas, KOTH, Bosses, NBT de Items) garantizando 20.0 TPS y 0 dupes.
[RESTRICCIONES]:
- Arquitectura libre de exploits económicos, bucles de desync o duplicación por items personalizados.
- Manejo estricto de NBT en items evolutivos y runas de mejora.
[TAREAS ESPECÍFICAS]:
1. Puente Técnico de Plugins: Define el flujo de datos entre el plugin de misiones (BattlePass), el de tokens y el de cajas (CrazyCrates/ExcellentCrates).
2. Seguridad de Items Evolutivos: Especifica cómo validar la aplicación de la "Runa de Evolución" (ej. verificación por CustomModelData + NBT persistente) para evitar que los jugadores apliquen runas en armaduras vanilla o no autorizadas.
3. Optimización de Entidades y Chunks: 
   - Configuración de flags de WorldGuard para la arena del boss y el KOTH.
   - Parámetros de purga de proyectiles y partículas excesivas durante el boss de 24h para mantener el MSPT por debajo de 40 ms.
4. Protocolo de Fallbacks: Procedimiento automático si el boss diario se glitchea o si el servidor reinicia a mitad de una oleada.
```

### D. LiveOps, Monetization & Community Lead (Conversión EULA y Retención)
```markdown
[ROL]: Eres el Director de LiveOps y Monetización para servidores de Minecraft multijugador con foco en monetización ética, retención y cumplimiento de la EULA de Mojang.
[OBJETIVO]: Maximizar el Life-Time Value (LTV) y el Daily Active Users (DAU) de la temporada a través del Pase de Batalla, la Caja de Temporada y el Hito Comunitario.
[TAREAS ESPECÍFICAS]:
1. Diseño de Pase Freemium: Estructura del Track Gratuito vs Track Premium (El Free debe ser satisfactorio para retener; el Premium debe ofrecer cosméticos de alto valor, boosts cosméticos de tokens y conveniencia sin caer en Pay-To-Win tóxico).
2. Mecánica de la Caja de Temporada:
   - Pity System (Sistema de piedad): Garantizar que cada X aperturas sin el kit evolutivo entregue un fragmento garantizado o pieza para evitar frustración absoluta.
   - Drops de relleno atractivos (Keys comunes, boosters temporales de pase, tags/títulos).
3. Hito Comunitario (Server Milestone): Diseñar el calendario de revelación de fases para generar hype semanal en Discord y dentro del juego.
4. Monitoreo y KPI: Definir las 5 métricas críticas a medir en Grafana/Plan durante la primera semana.
```

---

## 3. Red Teaming: Diagnóstico de Fallas Fatales y Mitigación Técnica

| # | Área | Falla Fatal / Modo de Fallo | Impacto en Producción | Mitigación Técnica Innegociable |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Economía** | **Inflación por Boss de 1h**: Farmeo 24/7 de bosses menores desborda sumideros en 4 días. | Hiperinflación de tokens; devaluación del Pase y la Crate. | **Soft-Cap Diario**: Rendimientos decrecientes (100% en kills 1-4, 50% en 5-8, 15% posteriores). Reinicio diario a las 00:00. |
| **2** | **Economía** | **Arbitraje a Cajas Vanilla**: Conversión irrestricta de tokens a llaves de cajas regulares. | Inyección desmedida de liquidez ($ y items) en la economía del Survival. | **Límites Semanales**: Cooldown de compra (máx. 2 llaves por semana) o llaves ligadas al jugador (*soulbound*). |
| **3** | **Combate** | **Colapso de MSPT en Boss 24h**: Spawn simultáneo de 20-30 adds con 40+ jugadores lanzando flechas y partículas. | TPS cae a < 8; congelaciones, caídas de paquetes y desincronización de clientes. | **Límite Estricto de Adds (4-6 máx)** o sustitución por **Pilares de Energía** interactivos (`block_display`/interacción). |
| **4** | **Combate** | **Monopolio y "Last Hit"**: Drops arrojados al suelo físico o premiar solo el último golpe. | Clanes dominantes acaparan todo; abandono del 90% de la comunidad casual. | **Loot Instanciado por Tiers de Daño** (Bronce 1-5%, Plata 6-15%, Oro >15% / Top 3) inyectado directamente al inventario. |
| **5** | **Seguridad** | **Duplicación en Runa de Evolución**: Desyncs al aplicar la runa en yunques o GUIs no atómicas. | Multiplicación de runas o aplicación infinita de stats sobre la armadura. | **Transacción Atómica vía ExecutableItems**: Chequeo NBT `ThunderSeasonTier: 1`, consumo de ítem (`-1`) y posterior mutación a `Tier: 2`. |
| **6** | **PvP / KOTH**| **Capturas Fantasma**: Clanes capturando el KOTH en horas muertas (04:00 - 06:00 AM) sin oposición. | Progresión desbalanceada sin riesgo competitivo real. | **Condición de Conexión y Horario**: KOTH condicionado a `%server_online% >= 25` o ventanas fijas de *Prime Time*. |
| **7** | **Monetización**| **El Abismo P2W del "Kit Roto"**: Armadura de temporada donadora indestructible en PvP vanilla. | Salida masiva de jugadores F2P en la semana 2; clanes no donadores se retiran. | **Dual-Stat Balancing**: Atributos masivos contra mobs/bosses estacionales (PvE), pero capados a Netherite Protección IV en combate contra jugadores (PvP). |
| **8** | **Persistencia**| **Pérdida de Datos en Hito Comunitario**: Variables en memoria plana borradas por reinicio inesperado. | Descontento general y pérdida de confianza en la network. | **Persistencia SQL**: Registro transaccional en base de datos unificada (MySQL/SQLite) para el conteo de donaciones. |

---

## 4. Blueprint del Hito Comunitario: El Altar de la Falla

### Arquitectura de Datos y Flujo
1. **Punto de Interacción:** NPC o estructura central en el Spawn principal (`/altar` o clic derecho).
2. **Insumos de Donación:**
   - Tokens de Evento sobrantes.
   - Drops de bosses estacionales (**"Fragmentos de Falla"**).
3. **Incentivo Dual (Colectivo + Individual):**
   - **Colectivo:** Al alcanzar metas globales de puntos acumulados en la network, se transiciona de Fase.
   - **Individual:** Cada aporte suma "Puntos de Devoción" a un Leaderboard público.
     - *Top 1:* Estatua con su skin en el Spawn + Título único de temporada.
     - *Top 2-3:* Título exclusivo + Cosmético animado intransferible.
     - *Top 4-10:* Paquete de Llaves de Crate de Temporada.

### Fases de Desbloqueo Progresivo
* **Fase 1 (0% - 25% Meta Global):**
  - Acceso habilitado a Boss Horario (Simple).
  - Pase de Batalla: Niveles 1 a 25 activos.
* **Fase 2 (25% - 50% Meta Global):**
  - Desbloqueo del **World Boss Diario de 24 Horas**.
  - Activación del **KOTH de Temporada**.
  - Buff pasivo permanente: **+15% de tokens** en todas las misiones y bosses para todo el servidor.
* **Fase 3 (50% - 75% Meta Global):**
  - La Caja de Temporada incorpora en su loot pool la **Runa de Evolución** y cosméticos avanzados.
  - Pase de Batalla: Niveles 26 a 50 desbloqueados.
* **Fase 4 (100% Meta Global - Clímax de Temporada):**
  - Fin de semana de **Caos Dimensional**: Multiplicador **x2 de Tokens** para toda la network.
  - Spawn del Jefe Final de Cierre y apertura del cofre comunal de temporada.

---

## 5. Modelo de Monetización Ética (Rating 8.5/10)

Para maximizar ingresos sin infringir la EULA ni alienar a los jugadores F2P:

1. **BattlePass Premium ($5.99 - $9.99 USD):**
   - Track Gratuito completo y recompensante (llaves, tokens, consumibles).
   - Track Premium enfocado en:
     - Cosméticos estacionales (cascos con `HeadAnimator`, mochilas, partículas).
     - Títulos y prefijos de chat exclusivos.
     - Multiplicador de tokens de misión (+20%).
2. **Saltos de Nivel (Tier Skips):**
   - Packs de niveles (5, 10 o 25 tiers) para jugadores ocupados que desean completar el pase sin disponer de horas de juego diarias.
3. **Booster Global de Temporada ($3.50 USD):**
   - Donación comunitaria celebrada: Activa **+25% de tokens para toda la network** durante 2 horas. Anuncio sonoro global en chat y bossbar.
4. **Pity System en la Caja de Temporada:**
   - Si tras 20 aperturas consecutivas el jugador no obtiene una pieza de la armadura estacional o un cosmético legendario, la apertura 21 tiene 100% de probabilidad de entrega, reseteando el contador. Esto elimina la sensación de estafa y aumenta la tasa de conversión en la tienda web.

---

## 6. Lo que sé vs. Lo que asumo

* **Lo que sé:**
  * Motor: Paper / Purpur 1.21.11 con PacketEvents y plugins avanzados (ExecutableItems, ExcellentCrates, DeluxeMenus, MythicMobs).
  * Estructura base propuesta: Pase de batalla, Boss 1h, Boss 24h, KOTH, Tokens, Crate de temporada, Kit evolutivo y Altar comunitario.
* **Lo que asumo:**
  * Asumo que el plugin de Pase de Batalla soporta ejecución de comandos de consola al subir de nivel (compatibilidad estándar con BattlePass / AdvancedBattlePass).
  * Asumo que la arena del Boss 24h dispone de protección WorldGuard con `pvp: deny` para asegurar que el combate sea 100% cooperativo.
  * Asumo que la tienda web utiliza Tebex o CraftingStore con inyección de comandos en tiempo real.

---

## Enlaces Relacionados
- **[[wiki/entities/thundermc|ThunderMC]]**
- **[[wiki/concepts/economia-servidor-minecraft|Economía Servidor Minecraft]]**
- **[[wiki/concepts/monetizacion-modelo-negocio|Modelo de Negocio & Monetización]]**
- **[[wiki/concepts/estandar-calidades-items|Estándar Oficial de Calidades]]**
- **[[wiki/entities/thundermc/evento-halloween-mobs|Mobs Evento Halloween]]**
