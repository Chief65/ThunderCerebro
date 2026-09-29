/**
 * ===============================================================================
 * BEACON LATENCY ESTIMATOR & PROGRESS ENGINE (v2.0)
 * ===============================================================================
 * Herramienta de alta precisión para el cálculo empírico y adaptación dinámica del
 * tiempo estimado de respuesta en Beacon (ThunderCerebro Control Center).
 *
 * Variables de inferencia:
 * 1. Proceso CLI bootstrap de Antigravity (Node/PowerShell en Windows).
 * 2. Perfil arquitectónico del modelo (TTFT base y ratio tokens/segundo).
 * 3. Complejidad sintáctica e intención del prompt (estimación de tokens de salida).
 * 4. Overhead de razonamiento interno (--effort high).
 * 5. Latencia de invocación de herramientas (filesystem, comandos shell).
 * 6. Factor de autocalibración adaptativa (aprendizaje continuo con historial real).
 * ===============================================================================
 */

(function (window) {
  'use strict';

  const STORAGE_KEY = 'beacon_latency_calibration_v2';

  // Perfiles empíricos de modelos disponibles (con overhead de CLI Antigravity real)
  const MODEL_PROFILES = {
    'gemini-3.8-flash': {
      name: 'Gemini 3.8 Flash',
      cliBootstrap: 3.6,      // Arranque del entorno Antigravity CLI + Node en Windows
      baseTtft: 1.8,          // Time-To-First-Token en segundos
      tokensPerSec: 55,       // Velocidad promedio de generación de tokens capturados
      reasoningHigh: 2.8,     // Overhead por razonamiento extendido (--effort high)
      toolExecLatency: 2.4    // Latencia esperada si invoca herramientas
    },
    'gemini-3.8-pro': {
      name: 'Gemini 3.8 Pro',
      cliBootstrap: 3.6,
      baseTtft: 3.2,
      tokensPerSec: 32,
      reasoningHigh: 4.8,
      toolExecLatency: 3.5
    },
    'gemini-flash-lite': {
      name: 'Gemini Flash-Lite',
      cliBootstrap: 3.2,
      baseTtft: 1.2,
      tokensPerSec: 75,
      reasoningHigh: 1.2,
      toolExecLatency: 1.8
    },
    'claude-3.7-sonnet': {
      name: 'Claude 3.7 Sonnet',
      cliBootstrap: 3.6,
      baseTtft: 3.6,
      tokensPerSec: 28,
      reasoningHigh: 5.5,
      toolExecLatency: 3.5
    },
    'default': {
      name: 'Gemini 3.8 Flash (Default)',
      cliBootstrap: 3.6,
      baseTtft: 1.8,
      tokensPerSec: 55,
      reasoningHigh: 2.8,
      toolExecLatency: 2.4
    }
  };

  class BeaconLatencyEstimator {
    constructor() {
      this.historySamples = this.loadHistory();
      this.calibrationFactor = this.computeCalibrationFactor();
    }

    loadHistory() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          const parsed = JSON.parse(stored);
          if (Array.isArray(parsed)) return parsed.slice(-25); // Últimos 25 registros
        }
      } catch (e) {
        console.warn('No se pudo cargar la calibración de latencia previa:', e);
      }
      return [];
    }

    saveHistory() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(this.historySamples));
      } catch (e) {
        console.warn('Error guardando historial de calibración:', e);
      }
    }

    computeCalibrationFactor() {
      if (this.historySamples.length === 0) return 1.0;
      // Mediana de los ratios actual / estimado crudo para evitar outliers
      const ratios = this.historySamples.map(s => s.ratio).filter(r => r > 0.3 && r < 3.5);
      if (ratios.length === 0) return 1.0;
      ratios.sort((a, b) => a - b);
      const mid = Math.floor(ratios.length / 2);
      const median = ratios.length % 2 !== 0 ? ratios[mid] : (ratios[mid - 1] + ratios[mid]) / 2;
      // Factor acotado entre 0.65 y 2.0 para estabilidad
      return Math.max(0.65, Math.min(2.0, median));
    }

    /**
     * Analiza el prompt para deducir la cantidad esperada de tokens de salida
     */
    analyzePromptComplexity(promptText) {
      if (!promptText) return { outputTokens: 120, requiresTool: false, isCode: false };

      const text = promptText.toLowerCase();
      let outputTokens = 220;
      let requiresTool = false;
      let isCode = false;

      // Detección de peticiones de código o artefactos estructurados
      if (/\b(código|script|yaml|json|plugin|config|función|powershell|java|clase|programa|deluxemenus|itemedit)\b/i.test(text)) {
        outputTokens = 550;
        isCode = true;
      }
      // Detección de análisis profundos, tablas, matrices o comparativas
      else if (/\b(analiza|diseña|compara|audita|resumen|informe|red teaming|diagnóstico|rendimiento|tokens|balance)\b/i.test(text)) {
        outputTokens = 420;
      }
      // Preguntas directas, saludos o consultas rápidas
      else if (/\b(hola|buenos días|qué es|qué hora|ayuda|test|ping|quién eres|ok|gracias)\b/i.test(text) && text.length < 80) {
        outputTokens = 70;
      }

      // Detección de comandos que invocan herramientas del sistema o de la wiki
      if (/\b(lee|leer|busca|buscar|archivo|directorio|carpeta|wiki|obsidian|servidor|catamines|shopgui|spawner|ejecuta)\b/i.test(text)) {
        requiresTool = true;
      }

      return { outputTokens, requiresTool, isCode };
    }

    /**
     * Calcula la estimación precisa de segundos para una consulta
     */
    estimate({ prompt, model = 'default', effort = 'high', historyCount = 0 }) {
      const profile = MODEL_PROFILES[model] || MODEL_PROFILES['default'];
      const complexity = this.analyzePromptComplexity(prompt);

      // 1. Latencia de arranque CLI + Base del modelo (TTFT)
      let rawSeconds = (profile.cliBootstrap || 3.6) + profile.baseTtft;

      // 2. Tiempo de generación basado en tokens esperados
      rawSeconds += (complexity.outputTokens / profile.tokensPerSec);

      // 3. Overhead de razonamiento
      if (effort === 'high' || effort === 'max') {
        rawSeconds += profile.reasoningHigh;
      }

      // 4. Invocación de herramientas (lectura/escritura)
      if (complexity.requiresTool) {
        rawSeconds += profile.toolExecLatency;
      }

      // 5. Overhead por profundidad del historial
      if (historyCount > 4) {
        rawSeconds += Math.min(2.0, (historyCount - 4) * 0.12);
      }

      // 6. Aplicar factor de calibración adaptativa empírica
      const calibrated = rawSeconds * this.calibrationFactor;
      const finalEstimate = Math.max(2.5, Math.round(calibrated * 10) / 10);

      return {
        estimatedSeconds: finalEstimate,
        minSeconds: Math.max(1.5, Math.round((finalEstimate * 0.8) * 10) / 10),
        maxSeconds: Math.round((finalEstimate * 1.3) * 10) / 10,
        expectedOutputTokens: complexity.outputTokens,
        modelName: profile.name,
        calibrationFactor: Math.round(this.calibrationFactor * 100) / 100,
        rawSeconds: Math.round(rawSeconds * 10) / 10
      };
    }

    /**
     * Registra el resultado real devuelto para auto-calibrar futuras estimaciones
     */
    recordExecution({ prompt, model = 'default', estimatedSeconds, actualSeconds }) {
      if (!actualSeconds || actualSeconds <= 0.2) return;

      const profile = MODEL_PROFILES[model] || MODEL_PROFILES['default'];
      const complexity = this.analyzePromptComplexity(prompt);
      let raw = (profile.cliBootstrap || 3.6) + profile.baseTtft + (complexity.outputTokens / profile.tokensPerSec);
      if (complexity.requiresTool) raw += profile.toolExecLatency;

      const ratio = actualSeconds / Math.max(1.0, raw);

      this.historySamples.push({
        timestamp: Date.now(),
        model,
        estimated: estimatedSeconds,
        actual: actualSeconds,
        ratio: Math.round(ratio * 1000) / 1000
      });

      if (this.historySamples.length > 30) {
        this.historySamples.shift();
      }

      this.saveHistory();
      this.calibrationFactor = this.computeCalibrationFactor();
    }

    /**
     * Crea un controlador dinámico y continuo de animación para la barra de progreso
     */
    createProgressController({
      estimatedSeconds,
      onProgress,    // callback(percent, elapsedSec, phaseText, estimatedSeconds)
      onDone         // callback(totalElapsedSec)
    }) {
      const startTime = performance.now();
      const targetSec = Math.max(3.0, estimatedSeconds || 9.5);
      const targetDurationMs = targetSec * 1000;
      let isCompleted = false;
      let isCanceled = false;
      let timerId = null;

      // Emitir frame inicial inmediato (3.5%) para respuesta visual instantánea
      if (onProgress) {
        onProgress(3.5, 0.0, '⚡ Conectando Beacon y cargando contexto...', targetSec);
      }

      function tick() {
        if (isCanceled || isCompleted) return;

        const now = performance.now();
        const elapsedMs = now - startTime;
        const elapsedSec = Math.round((elapsedMs / 100)) / 10;

        let pct = 3.5;
        let phase = '⚡ Conectando y analizando workspace...';

        if (elapsedMs < targetDurationMs) {
          // Curva fluida sostenida de 3.5% a 92% a lo largo del tiempo estimado
          const t = elapsedMs / targetDurationMs;
          const easedRatio = 1 - Math.pow(1 - t, 2.0);
          pct = 3.5 + (easedRatio * 88.5);

          if (pct < 22) {
            phase = '⚡ Conectando motor y cargando contexto...';
          } else if (pct < 55) {
            phase = '🧠 Razonando y evaluando contexto (effort: high)...';
          } else if (pct < 80) {
            phase = '📝 Generando y estructurando tokens...';
          } else {
            phase = '⚡ Sintetizando y verificando respuesta...';
          }
        } else {
          // Ha superado el tiempo estimado: avance continuo asintótico de 92% a 99%
          // NUNCA se detiene ni da sensación de bloqueo
          const overdueSec = (elapsedMs - targetDurationMs) / 1000;
          const overdueAdvance = 7.0 * (1 - Math.exp(-overdueSec / 7.0));
          pct = 92.0 + overdueAdvance;
          phase = `✨ Finalizando respuesta técnica en curso (~${elapsedSec}s)...`;
        }

        pct = Math.min(99.0, Math.max(3.5, Math.round(pct * 10) / 10));

        if (onProgress) {
          onProgress(pct, elapsedSec, phase, targetSec);
        }

        timerId = setTimeout(tick, 40); // 25 fps para movimiento ultrasuave
      }

      // Iniciar el loop de animación
      timerId = setTimeout(tick, 40);

      return {
        complete: (actualBackendSeconds) => {
          if (isCompleted || isCanceled) return;
          isCompleted = true;
          if (timerId) clearTimeout(timerId);
          const totalSec = actualBackendSeconds || Math.round(((performance.now() - startTime) / 1000) * 10) / 10;
          if (onProgress) {
            onProgress(100, totalSec, '✅ ¡Respuesta generada con éxito!', targetSec);
          }
          if (onDone) {
            onDone(totalSec);
          }
        },
        cancel: () => {
          isCanceled = true;
          if (timerId) clearTimeout(timerId);
        }
      };
    }
  }

  // Instancia global en el scope del navegador
  window.BeaconLatencyEstimator = new BeaconLatencyEstimator();

})(window);
