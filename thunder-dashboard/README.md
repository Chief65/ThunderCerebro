# ⚡ Thunder Telemetry & Market Intelligence Dashboard

Cuadro de mando local y privado para el **Sr Ramos**, diseñado para contrastar la telemetría real del servidor Minecraft contra los benchmarks y umbrales definidos en el estudio de mercado.

---

## 🚀 Arranque Rápido

1. **Doble clic en `iniciar_dashboard.bat`** (en esta carpeta).
2. Se abrirá automáticamente su navegador en `http://localhost:3838`.
3. El dashboard funciona 100% de forma local en su PC sin depender de servicios externos ni comprometer credenciales.

---

## 📊 Módulos y Pestañas del Cuadro de Mando

1. **Semáforo Global de Salud (Health Score)**:
   - Diagnóstico en tiempo real sobre los 5 cuadrantes operativos (Adquisición, Retención, Engagement, Rendimiento y Monetización).
2. **Tráfico & Demografía**:
   - Evolución semanal de concurrencia (CCU) vs nuevos registros.
   - Desglose por plataforma (Bedrock Android APK, Java No-Premium, Java Oficial, Consolas).
   - Mapa de demanda geográfica (México, España, Argentina, Colombia, Chile...).
3. **Retención & Cohortes**:
   - Curva de vida del jugador (D1 a D30) superpuesta contra el **Benchmark Óptimo** y el **Mínimo de Supervivencia**.
   - Medición de tiempo de sesión y tasa de rebote (*Bounce Rate*).
4. **Estrés Técnico (MSPT / TPS)**:
   - Correlación gráfica entre número de jugadores concurrentes y carga mononúcleo de CPU.
   - Umbrales de advertencia para prevenir lag antes de llegar a los 50.0 ms.
5. **Monetización & Pasarelas**:
   - Impacto de métodos de pago en efectivo y billeteras locales de LATAM (Mercado Pago, OXXO, Pago Fácil).
   - Ticket medio y tasa de conversión de tienda.
6. **Calculadora Financiera & Escalado de Red**:
   - Slider reactivo para simular de 30 a 1.500 CCU.
   - Conmutador entre **Mercado España/LATAM** y **Mercado Anglosajón (US/UK)**.
   - Cálculo automático de costes fijos de servidores (OPEX), facturación bruta y margen neto mensual.

---

## 🔄 Conexión con Datos Reales de Producción

* **Plugin Plan**: Cuando descargue el archivo `database.db` del servidor con el skill `analisisdelmes`, el script `full_analysis.js` genera el resumen de telemetría que actualiza `data/current_metrics.json`.
* **API REST Local**:
  - `GET http://localhost:3838/api/metrics`: Devuelve los datos actuales en formato JSON.
  - `POST http://localhost:3838/api/metrics`: Actualiza las métricas con nuevos datos.
  - `POST http://localhost:3838/api/metrics/reset`: Restablece los datos a los valores base del estudio de mercado.
