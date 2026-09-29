// Beacon AI // ThunderCerebro Control Center App Logic

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initChat();
  initPerformance();
  initLauncher();
  initSkills();
  initSubagents();
  initLogs();
  initGraph();
});

// State
const state = {
  activeView: 'chat',
  activeModel: 'gemini-3.8-flash',
  tokenTelemetry: {
    sessionTotal: 1500,
    sessionInput: 1500,
    sessionOutput: 0,
    maxContext: 1048576,
    percent: 0.14,
    model: 'gemini-3.8-flash'
  },
  topic: 'minecraft',
  topicName: 'Minecraft Survival',
  model: '',
  modelName: 'Gemini 3.8 Flash',
  effort: 'high',
  mode: 'default',
  prompt: '',
  skills: [],
  subagents: [],
  graphData: null
};

// 1. Navigation Controller
function initNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  const viewContents = document.querySelectorAll('.view-content');
  const breadcrumb = document.getElementById('viewTitleBreadcrumb');

  const titles = {
    chat: 'Chat Beacon',
    performance: 'Rendimiento & Tokens',
    launcher: 'Centro de Mando & Lanzador',
    graph: 'Grafo Obsidian Interactivo',
    skills: 'Catálogo de Habilidades (Skills)',
    subagents: 'Subagentes de ThunderStudios',
    servers: 'Servidores & Infraestructura',
    logs: 'Bitácora Histórica (log.md)',
    terminal: 'Terminal & Consola Antigravity'
  };

  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const targetView = item.getAttribute('data-view');
      
      navItems.forEach(n => n.classList.remove('active'));
      item.classList.add('active');

      viewContents.forEach(v => {
        if (v.id === `view-${targetView}`) {
          v.classList.add('active');
        } else {
          v.classList.remove('active');
        }
      });

      state.activeView = targetView;
      if (breadcrumb) breadcrumb.textContent = titles[targetView] || 'Control';

      if (targetView === 'graph' && window.resizeGraphCanvas) {
        window.resizeGraphCanvas();
      }

      if (targetView === 'performance') {
        refreshPerformanceMetrics();
      }
    });
  });
}

// ==========================================================
// 2. Chat Controller (ChatGPT Clean Style)
// ==========================================================
function initChat() {
  const chatInputText = document.getElementById('chatInputText');
  const btnSendMessage = document.getElementById('btnSendMessage');
  const chatModelSelect = document.getElementById('chatModelSelect');
  const btnTopClearChat = document.getElementById('btnTopClearChat');
  const suggestionCards = document.querySelectorAll('.suggestion-card');

  // Auto-resize textarea
  if (chatInputText) {
    chatInputText.addEventListener('input', () => {
      chatInputText.style.height = 'auto';
      const newHeight = Math.min(chatInputText.scrollHeight, 180);
      chatInputText.style.height = (newHeight > 24 ? newHeight : 24) + 'px';
      
      if (btnSendMessage) {
        if (chatInputText.value.trim().length > 0) {
          btnSendMessage.classList.add('active');
        } else {
          btnSendMessage.classList.remove('active');
        }
      }
    });

    chatInputText.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        submitChatMessage();
      }
    });
  }

  if (btnSendMessage) {
    btnSendMessage.addEventListener('click', (e) => {
      e.preventDefault();
      submitChatMessage();
    });
  }

  // Suggestion prompt cards
  suggestionCards.forEach(card => {
    card.addEventListener('click', () => {
      const prompt = card.getAttribute('data-prompt');
      if (prompt && chatInputText) {
        chatInputText.value = prompt;
        chatInputText.dispatchEvent(new Event('input'));
        submitChatMessage();
      }
    });
  });

  // Clear chat action
  if (btnTopClearChat) {
    btnTopClearChat.addEventListener('click', () => {
      clearChatSession();
    });
  }

  // Model switch
  if (chatModelSelect) {
    chatModelSelect.addEventListener('change', async () => {
      state.activeModel = chatModelSelect.value;
      try {
        const res = await fetch('/api/model', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ model: state.activeModel })
        });
        const data = await res.json();
        if (data.success) {
          state.tokenTelemetry.maxContext = data.maxContext;
          state.tokenTelemetry.percent = data.percent;
          updateTokenBadges();
        }
      } catch (err) {
        console.error('Error cambiando modelo:', err);
      }
    });
  }

  // Load chat history & telemetry on startup
  loadChatHistory();
}

// Confirmation Modal for Delicate Operations
function showConfirmDialog({ title, subtitle, message, preview, confirmText = 'Confirmar y Proceder', confirmClass = '' }) {
  return new Promise((resolve) => {
    const modal = document.getElementById('confirmActionModal');
    if (!modal) {
      resolve(confirm(message ? message.replace(/<[^>]*>/g, '') : '¿Confirmar operación?'));
      return;
    }

    const titleEl = document.getElementById('confirmModalTitle');
    const subtitleEl = modal.querySelector('.modal-subtitle');
    const bodyEl = document.getElementById('confirmModalBody');
    const previewEl = document.getElementById('confirmModalPreview');
    const btnCancel = document.getElementById('btnConfirmCancel');
    const btnConfirm = document.getElementById('btnConfirmExecute');

    if (titleEl) titleEl.textContent = title || 'Confirmar Acción Delicada';
    if (subtitleEl && subtitle) subtitleEl.textContent = subtitle;
    if (bodyEl) bodyEl.innerHTML = message || '¿Deseas continuar con esta acción?';

    if (previewEl) {
      if (preview) {
        previewEl.textContent = preview;
        previewEl.style.display = 'block';
      } else {
        previewEl.style.display = 'none';
      }
    }

    if (btnConfirm) {
      btnConfirm.textContent = confirmText;
      btnConfirm.className = 'btn-modal-confirm ' + confirmClass;
    }

    modal.style.display = 'flex';

    function cleanup(result) {
      modal.style.display = 'none';
      btnCancel.removeEventListener('click', onCancel);
      btnConfirm.removeEventListener('click', onConfirm);
      modal.removeEventListener('click', onBackdrop);
      window.removeEventListener('keydown', onKey);
      resolve(result);
    }

    function onCancel() { cleanup(false); }
    function onConfirm() { cleanup(true); }
    function onBackdrop(e) { if (e.target === modal) cleanup(false); }
    function onKey(e) {
      if (e.key === 'Escape') cleanup(false);
      else if (e.key === 'Enter') cleanup(true);
    }

    btnCancel.addEventListener('click', onCancel);
    btnConfirm.addEventListener('click', onConfirm);
    modal.addEventListener('click', onBackdrop);
    window.addEventListener('keydown', onKey);
  });
}

function isDelicateInstruction(text) {
  if (!text) return false;
  const delicatePatterns = [
    /\b(borra|borrar|elimina|eliminar|suprime|suprimir|delete|remove|rm|del)\b/i,
    /\b(modifica|modificar|edita|editar|cambia|cambiar|sobrescribe|overwrite|actualiza|actualizar)\b/i,
    /\b(crea|crear|genera|generar|escribe|escribir|añade|anadir)\b/i,
    /\b(ejecuta|ejecutar|corre|correr|run|powershell|cmd|bash|sh|script)\b/i,
    /\b(instala|instalar|sube|subir|despliega|deploy|sftp|ssh)\b/i,
    /\b(reinicia|restart|reload|kill|detén|detener|stop)\b/i,
    /\b(git reset|git clean|git push|format|drop|wipe|truncate)\b/i,
    /\b(survival|produccion|production)\b/i
  ];
  return delicatePatterns.some(pattern => pattern.test(text));
}

async function submitChatMessage() {
  const chatInputText = document.getElementById('chatInputText');
  const messagesStream = document.getElementById('messagesStream');
  const chatWelcomeState = document.getElementById('chatWelcomeState');
  const chatScrollContainer = document.getElementById('chatScrollContainer');
  const chatTypingIndicator = document.getElementById('chatTypingIndicator');
  const btnSendMessage = document.getElementById('btnSendMessage');

  if (!chatInputText) return;
  const text = chatInputText.value.trim();
  if (!text) return;

  const checkRequireConfirm = document.getElementById('checkRequireConfirm');
  const requireConfirm = checkRequireConfirm ? checkRequireConfirm.checked : true;

  if (requireConfirm && isDelicateInstruction(text)) {
    const userConfirmed = await showConfirmDialog({
      title: '⚠️ Confirmar Cambio Delicado',
      subtitle: 'Permisos autónomos activos (--dangerously-skip-permissions)',
      message: 'Esta instrucción puede realizar modificaciones en el sistema o archivos sin solicitar confirmación interactiva por consola. ¿Deseas confirmar la ejecución?',
      preview: text,
      confirmText: 'Confirmar y Enviar'
    });

    if (!userConfirmed) {
      return;
    }
  }

  // Clear input
  chatInputText.value = '';
  chatInputText.style.height = 'auto';
  if (btnSendMessage) btnSendMessage.classList.remove('active');

  // Hide welcome state
  if (chatWelcomeState) chatWelcomeState.style.display = 'none';

  // Append user message
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  appendMessageToDOM('user', text, timeStr);

  // 1. Calculate Estimated Response Time using our tool
  let estimateData = { estimatedSeconds: 9.5 };
  if (window.BeaconLatencyEstimator) {
    try {
      estimateData = window.BeaconLatencyEstimator.estimate({
        prompt: text,
        model: state.activeModel,
        effort: 'high',
        historyCount: state.tokenTelemetry ? (state.tokenTelemetry.sessionTotal > 1500 ? 5 : 0) : 0
      });
    } catch (e) {
      console.warn('Error al calcular estimación de latencia:', e);
    }
  }

  // 2. Prepare UI elements and reset states
  const progressFill = document.getElementById('typingProgressFill');
  const typingStatusText = document.getElementById('typingStatusText');
  const typingTimeText = document.getElementById('typingTimeText');
  const typingEstimatePill = document.getElementById('typingEstimatePill');

  if (progressFill) {
    progressFill.classList.remove('completed');
    progressFill.style.width = '3.5%';
  }
  if (typingEstimatePill) {
    typingEstimatePill.classList.remove('completed');
  }
  if (typingTimeText) {
    typingTimeText.textContent = `0.0s / ~${estimateData.estimatedSeconds}s (3%)`;
  }
  if (typingStatusText) {
    typingStatusText.textContent = '⚡ Conectando Beacon y cargando contexto...';
  }

  // Show thinking indicator immediately so layout dimensions are active
  if (chatTypingIndicator) {
    chatTypingIndicator.style.display = 'flex';
  }
  if (chatScrollContainer) {
    chatScrollContainer.scrollTop = chatScrollContainer.scrollHeight;
  }

  // 3. Setup Progress Controller with fallback guarantee
  let progressController = null;
  const onProgressCallback = (percent, elapsedSec, phaseText, estSec) => {
    const targetEst = estSec || estimateData.estimatedSeconds;
    if (progressFill) progressFill.style.width = `${percent}%`;
    if (typingStatusText) typingStatusText.textContent = phaseText;
    if (typingTimeText) {
      typingTimeText.textContent = `${elapsedSec}s / ~${targetEst}s (${Math.round(percent)}%)`;
    }
  };

  const onDoneCallback = (totalSec) => {
    if (progressFill) {
      progressFill.classList.add('completed');
      progressFill.style.width = '100%';
    }
    if (typingEstimatePill) {
      typingEstimatePill.classList.add('completed');
    }
    if (typingTimeText) {
      typingTimeText.textContent = `Listo (${totalSec}s)`;
    }
  };

  if (window.BeaconLatencyEstimator && typeof window.BeaconLatencyEstimator.createProgressController === 'function') {
    progressController = window.BeaconLatencyEstimator.createProgressController({
      estimatedSeconds: estimateData.estimatedSeconds,
      onProgress: onProgressCallback,
      onDone: onDoneCallback
    });
  } else {
    // Robust fallback si el script externo no estuviera disponible
    const fallbackEst = estimateData.estimatedSeconds || 9.5;
    const fallbackStart = performance.now();
    let fbTimer = null;
    let fbCompleted = false;

    function runFallbackTick() {
      if (fbCompleted) return;
      const elMs = performance.now() - fallbackStart;
      const elSec = Math.round(elMs / 100) / 10;
      let pct = 3.5;
      if (elMs < fallbackEst * 1000) {
        pct = 3.5 + ((elMs / (fallbackEst * 1000)) * 88.5);
      } else {
        pct = Math.min(99, 92 + ((elMs - (fallbackEst * 1000)) / 2500));
      }
      onProgressCallback(pct, elSec, '⚡ Procesando respuesta técnica con Beacon...', fallbackEst);
      fbTimer = setTimeout(runFallbackTick, 40);
    }
    fbTimer = setTimeout(runFallbackTick, 40);

    progressController = {
      complete: (sec) => {
        fbCompleted = true;
        clearTimeout(fbTimer);
        onDoneCallback(sec || (Math.round((performance.now() - fallbackStart) / 100) / 10));
      },
      cancel: () => {
        fbCompleted = true;
        clearTimeout(fbTimer);
      }
    };
  }

  const clientStartTime = performance.now();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        model: state.activeModel
      })
    });

    const data = await res.json();
    const actualClientSeconds = Math.round(((performance.now() - clientStartTime) / 1000) * 10) / 10;
    const finalSeconds = data.executionSeconds || actualClientSeconds;

    // Record sample in our tool to improve future calibration accuracy
    if (window.BeaconLatencyEstimator && typeof window.BeaconLatencyEstimator.recordExecution === 'function') {
      window.BeaconLatencyEstimator.recordExecution({
        prompt: text,
        model: state.activeModel,
        estimatedSeconds: estimateData.estimatedSeconds,
        actualSeconds: finalSeconds
      });
    }

    // Complete progress animation smoothly
    if (progressController) {
      progressController.complete(finalSeconds);
    }

    // Brief smooth pause for visual feedback of completed progress bar
    await new Promise(r => setTimeout(r, 450));

    if (chatTypingIndicator) chatTypingIndicator.style.display = 'none';

    if (data.reply) {
      const turnTokens = data.tokens ? data.tokens.turnOutput : null;
      appendMessageToDOM('assistant', data.reply, data.timestamp || timeStr, turnTokens, finalSeconds);
    } else if (data.error) {
      appendMessageToDOM('assistant', `⚠️ **Error en respuesta**: ${data.error}`, timeStr);
    }

    if (data.tokens) {
      state.tokenTelemetry = data.tokens;
      updateTokenBadges();
    }
  } catch (err) {
    if (progressController) progressController.cancel();
    if (chatTypingIndicator) chatTypingIndicator.style.display = 'none';
    appendMessageToDOM('assistant', `⚠️ **Error de conexión**: No se pudo comunicar con el backend local (${err.message}).`, timeStr);
  }

  if (chatScrollContainer) {
    chatScrollContainer.scrollTop = chatScrollContainer.scrollHeight;
  }
}

function appendMessageToDOM(role, content, timeStr, turnTokens, execSeconds) {
  const messagesStream = document.getElementById('messagesStream');
  if (!messagesStream) return;

  const row = document.createElement('div');
  row.className = `chat-message-row ${role}`;

  if (role === 'user') {
    row.innerHTML = `
      <div class="message-content-wrapper">
        <div class="message-body">${escapeHtml(content)}</div>
      </div>
    `;
  } else {
    const parsedHtml = formatMarkdown(content);
    const tokenBadge = turnTokens ? `<span class="token-pill">⚡ ~${turnTokens} tokens</span>` : '';
    const timeBadge = execSeconds ? `<span class="token-pill" style="color: #b45309; background: #fef3c7; border: 1px solid #fde68a;">⏱️ ${execSeconds}s</span>` : '';

    row.innerHTML = `
      <div class="avatar-badge">⚡</div>
      <div class="message-content-wrapper">
        <div class="message-author-tag">
          <span>Beacon</span>
          <span class="timestamp">${timeStr || ''}</span>
        </div>
        <div class="message-body">${parsedHtml}</div>
        <div class="message-toolbar">
          <button class="btn-copy-response" onclick="copyMessageResponse(this)">
            <span>📋</span>
            <span>Copiar respuesta</span>
          </button>
          ${timeBadge}
          ${tokenBadge}
        </div>
      </div>
    `;
  }

  messagesStream.appendChild(row);
}

function formatMarkdown(content) {
  if (!content) return '';

  // Protect code blocks first
  const codeBlocks = [];
  let processed = content.replace(/```([a-zA-Z0-9_\-\.]*)\r?\n([\s\S]*?)```/g, (match, lang, code) => {
    const idx = codeBlocks.length;
    codeBlocks.push({ lang: lang || 'code', code: code.trim() });
    return `###CODE_BLOCK_${idx}###`;
  });

  // Escape HTML in the regular text
  processed = escapeHtml(processed);

  // Bold **text**
  processed = processed.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // Headings
  processed = processed.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  processed = processed.replace(/^## (.*$)/gim, '<h2>$1</h2>');

  // Blockquotes
  processed = processed.replace(/^> (.*$)/gim, '<blockquote>$1</blockquote>');

  // Markdown links [text](url)
  processed = processed.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

  // Line breaks
  processed = processed.replace(/\n/g, '<br>');

  // Restore code blocks with styled wrapper and copy button
  codeBlocks.forEach((block, idx) => {
    const escapedCode = escapeHtml(block.code);
    const replacement = `
      <div class="code-block-wrapper">
        <div class="code-header">
          <span>${block.lang}</span>
          <button class="btn-copy-code" onclick="copyCodeBlock(this)">
            <span>📋</span>
            <span>Copiar</span>
          </button>
        </div>
        <pre class="code-content"><code>${escapedCode}</code></pre>
      </div>
    `;
    processed = processed.replace(`###CODE_BLOCK_${idx}###`, replacement);
  });

  // Inline code `code`
  processed = processed.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');

  return processed;
}

window.copyCodeBlock = function(btn) {
  const wrapper = btn.closest('.code-block-wrapper');
  if (!wrapper) return;
  const code = wrapper.querySelector('code');
  if (code) {
    navigator.clipboard.writeText(code.innerText).then(() => {
      const originalText = btn.innerHTML;
      btn.innerHTML = '<span>✓</span><span>Copiado</span>';
      btn.style.color = '#10b981';
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.color = '';
      }, 2000);
    });
  }
};

window.copyMessageResponse = function(btn) {
  const row = btn.closest('.chat-message-row');
  if (!row) return;
  const body = row.querySelector('.message-body');
  if (body) {
    navigator.clipboard.writeText(body.innerText).then(() => {
      const originalText = btn.innerHTML;
      btn.innerHTML = '<span>✓</span><span>Copiado</span>';
      setTimeout(() => {
        btn.innerHTML = originalText;
      }, 2000);
    });
  }
};

async function loadChatHistory() {
  try {
    const res = await fetch('/api/chat/history');
    const data = await res.json();
    if (data.tokens) {
      state.tokenTelemetry = data.tokens;
      if (data.tokens.model) {
        state.activeModel = data.tokens.model;
        const select = document.getElementById('chatModelSelect');
        if (select) select.value = data.tokens.model;
      }
      updateTokenBadges();
    }
    if (data.messages && data.messages.length > 0) {
      const welcome = document.getElementById('chatWelcomeState');
      if (welcome) welcome.style.display = 'none';

      const stream = document.getElementById('messagesStream');
      if (stream) {
        stream.innerHTML = '';
        data.messages.forEach(msg => {
          appendMessageToDOM(msg.role, msg.content, msg.timestamp, msg.tokens);
        });
      }
      const container = document.getElementById('chatScrollContainer');
      if (container) container.scrollTop = container.scrollHeight;
    }
  } catch (err) {
    console.warn('No se pudo cargar historial del chat:', err);
  }
}

async function clearChatSession() {
  if (!confirm('¿Desea limpiar la conversación activa y restablecer el contexto de tokens?')) {
    return;
  }
  try {
    const res = await fetch('/api/chat/clear', { method: 'POST' });
    const data = await res.json();
    if (data.tokens) {
      state.tokenTelemetry = data.tokens;
      updateTokenBadges();
    }
    const stream = document.getElementById('messagesStream');
    if (stream) stream.innerHTML = '';
    const welcome = document.getElementById('chatWelcomeState');
    if (welcome) welcome.style.display = 'flex';
    refreshPerformanceMetrics();
  } catch (err) {
    console.error('Error limpiando sesión:', err);
  }
}

function updateTokenBadges() {
  const pct = state.tokenTelemetry.percent || 0.14;
  const total = state.tokenTelemetry.sessionTotal || 1500;
  const max = state.tokenTelemetry.maxContext || 1048576;

  const usagePercentText = document.getElementById('usagePercentText');
  const usageTokensCounter = document.getElementById('usageTokensCounter');
  const usageDot = document.getElementById('usageDot');
  const perfNavBadge = document.getElementById('perfNavBadge');

  if (usagePercentText) {
    usagePercentText.textContent = `${pct}% uso`;
  }
  if (usageTokensCounter) {
    usageTokensCounter.textContent = `(${formatTokens(total)} / ${formatTokens(max)} tok)`;
  }
  if (perfNavBadge) {
    perfNavBadge.textContent = `${pct}%`;
  }
  if (usageDot) {
    usageDot.classList.remove('warning', 'danger');
    if (pct >= 60) {
      usageDot.classList.add('danger');
    } else if (pct >= 30) {
      usageDot.classList.add('warning');
    }
  }
}

// ==========================================================
// 3. Rendimiento & Tokens Controller
// ==========================================================
function initPerformance() {
  const btnRefreshPerf = document.getElementById('btnRefreshPerf');
  const btnPurgePerf = document.getElementById('btnPurgePerf');

  if (btnRefreshPerf) {
    btnRefreshPerf.addEventListener('click', () => {
      refreshPerformanceMetrics();
    });
  }

  if (btnPurgePerf) {
    btnPurgePerf.addEventListener('click', () => {
      clearChatSession();
    });
  }

  // Initial fetch
  refreshPerformanceMetrics();
}

async function refreshPerformanceMetrics() {
  try {
    const res = await fetch('/api/performance');
    const data = await res.json();

    const kpiTotalTokens = document.getElementById('kpiTotalTokens');
    const kpiTokensSub = document.getElementById('kpiTokensSub');
    const kpiUsagePct = document.getElementById('kpiUsagePct');
    const kpiContextSub = document.getElementById('kpiContextSub');
    const kpiRatio = document.getElementById('kpiRatio');
    const kpiHealth = document.getElementById('kpiHealth');

    if (kpiTotalTokens) kpiTotalTokens.textContent = Number(data.totalTokens).toLocaleString();
    if (kpiTokensSub) kpiTokensSub.textContent = `${Number(data.inputTokens).toLocaleString()} prompt / ${Number(data.outputTokens).toLocaleString()} salida`;
    if (kpiUsagePct) kpiUsagePct.textContent = `${data.usagePercent}%`;
    if (kpiContextSub) kpiContextSub.textContent = `De ${formatTokens(data.maxContext)} tokens (${data.activeModel})`;

    if (kpiRatio && data.totalTokens > 0) {
      const inPct = Math.round((data.inputTokens / data.totalTokens) * 100);
      const outPct = 100 - inPct;
      kpiRatio.textContent = `${inPct}% / ${outPct}%`;
    }

    if (kpiHealth) {
      kpiHealth.classList.remove('status-optimal', 'status-warning', 'status-danger');
      if (data.usagePercent < 30) {
        kpiHealth.textContent = 'Óptimo';
        kpiHealth.classList.add('status-optimal');
      } else if (data.usagePercent < 60) {
        kpiHealth.textContent = 'Moderado';
        kpiHealth.classList.add('status-warning');
      } else {
        kpiHealth.textContent = 'Alerta';
        kpiHealth.classList.add('status-danger');
      }
    }

    // Process breakdown
    if (data.breakdown) {
      const b = data.breakdown;
      setBar('Files', b.files);
      setBar('Hist', b.history);
      setBar('Shell', b.shell);
      setBar('Output', b.output);
      setBar('Sys', b.system);
    }

    // Heavy files table
    const tableBody = document.getElementById('heavyFilesTableBody');
    if (tableBody && data.heavyFiles && data.heavyFiles.length > 0) {
      tableBody.innerHTML = '';
      data.heavyFiles.forEach(file => {
        let badgeClass = 'badge-risk low';
        let directive = 'Lectura segura';

        if (file.risk === 'Peligro Crítico') {
          badgeClass = 'badge-risk critical';
          directive = 'Prohibido cargar en contexto';
        } else if (file.risk === 'Alto Consumo') {
          badgeClass = 'badge-risk high';
          directive = 'Lectura por cortes (StartLine)';
        } else if (file.risk === 'Moderado') {
          badgeClass = 'badge-risk moderate';
          directive = 'Uso segmentado';
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${escapeHtml(file.name)}</strong></td>
          <td style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${escapeHtml(file.path)}</td>
          <td style="font-family: var(--font-mono);">${file.sizeKB} KB</td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: var(--text-main);">${Number(file.tokens).toLocaleString()}</td>
          <td><span class="${badgeClass}">${file.risk}</span></td>
          <td style="font-size: 12px; color: var(--text-muted);">${directive}</td>
        `;
        tableBody.appendChild(tr);
      });
    }

    // Sync header token telemetry
    state.tokenTelemetry.percent = data.usagePercent;
    state.tokenTelemetry.sessionTotal = data.totalTokens;
    state.tokenTelemetry.maxContext = data.maxContext;
    updateTokenBadges();

  } catch (err) {
    console.error('Error refrescando métricas de rendimiento:', err);
  }
}

function setBar(id, val) {
  const pctEl = document.getElementById(`barPct${id}`);
  const fillEl = document.getElementById(`barFill${id}`);
  if (pctEl) pctEl.textContent = `${val}%`;
  if (fillEl) fillEl.style.width = `${val}%`;
}

function formatTokens(num) {
  if (!num) return '0';
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
  return num.toString();
}

function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}


// 2. Launcher & Configurator
function initLauncher() {
  const topicCards = document.querySelectorAll('.topic-card');
  const selectModel = document.getElementById('selectModel');
  const selectEffort = document.getElementById('selectEffort');
  const selectMode = document.getElementById('selectMode');
  const inputPrompt = document.getElementById('inputPrompt');
  const cmdPreview = document.getElementById('cmdPreview');
  const btnLaunchHero = document.getElementById('btnLaunchHero');
  const btnTopLaunch = document.getElementById('btnTopLaunch');
  const chips = document.querySelectorAll('.prompt-chip');

  // Topic click
  topicCards.forEach(card => {
    card.addEventListener('click', () => {
      topicCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      state.topic = card.getAttribute('data-topic');
      state.topicName = card.querySelector('.topic-title').textContent;
      document.getElementById('summaryTopic').textContent = state.topicName;
      updateCmdPreview();
    });
  });

  // Model change
  selectModel.addEventListener('change', () => {
    state.model = selectModel.value;
    state.modelName = selectModel.options[selectModel.selectedIndex].text.split('(')[0].trim();
    document.getElementById('summaryModel').textContent = state.modelName;
    updateCmdPreview();
  });

  // Effort change
  selectEffort.addEventListener('change', () => {
    state.effort = selectEffort.value;
    document.getElementById('summaryEffort').textContent = selectEffort.options[selectEffort.selectedIndex].text.split('(')[0].trim();
    updateCmdPreview();
  });

  // Mode change
  selectMode.addEventListener('change', () => {
    state.mode = selectMode.value;
    updateCmdPreview();
  });

  // Input prompt
  inputPrompt.addEventListener('input', () => {
    state.prompt = inputPrompt.value;
    updateCmdPreview();
  });

  // Chips
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      inputPrompt.value = chip.getAttribute('data-chip');
      state.prompt = inputPrompt.value;
      updateCmdPreview();
    });
  });

  function updateCmdPreview() {
    let cmd = 'agy --dangerously-skip-permissions';
    if (state.model) cmd += ` --model ${state.model}`;
    if (state.effort) cmd += ` --effort ${state.effort}`;
    if (state.mode === 'plan') cmd += ` --mode plan`;
    
    let p = state.prompt.trim();
    if (!p) {
      if (state.topic === 'minecraft') p = 'Hola Beacon. Iniciamos sesión en ThunderMC Survival (1.21.11).';
      else if (state.topic === 'obsidian') p = 'Hola Beacon. Gestionemos notas y el grafo en Obsidian.';
      else if (state.topic === 'studio') p = 'Hola Beacon. Trabajemos en el universo THUNDERVERSE.';
      else if (state.topic === 'negocio') p = 'Hola Beacon. Revisemos monetización y tienda Tebex.';
      else if (state.topic === 'dev') p = 'Hola Beacon. Revisemos arquitectura de código y plugins.';
      else p = 'Hola Beacon. ¿En qué trabajamos hoy?';
    }
    cmd += ` -i "${p.substring(0, 45)}${p.length > 45 ? '...' : ''}"`;

    if (cmdPreview) cmdPreview.textContent = cmd;
  }

  // Launch handler
  async function triggerLaunch() {
    const cmdText = cmdPreview ? cmdPreview.textContent.trim() : 'agy --dangerously-skip-permissions';

    const userConfirmed = await showConfirmDialog({
      title: '⚡ Confirmar Lanzamiento de Antigravity',
      subtitle: 'Auto-aprobación activa (--dangerously-skip-permissions)',
      message: 'Se abrirá una consola interactiva con auto-aprobación de herramientas. Todas las operaciones de comandos y mutaciones de archivos se ejecutarán de forma autónoma. ¿Confirmas el inicio de la sesión?',
      preview: cmdText,
      confirmText: 'Confirmar e Iniciar Terminal'
    });

    if (!userConfirmed) return;

    const origText = btnLaunchHero.innerHTML;
    btnLaunchHero.innerHTML = '<span>⏳</span><span>Lanzando Terminal...</span>';
    btnLaunchHero.disabled = true;

    try {
      const res = await fetch('/api/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: state.topic,
          model: state.model,
          effort: state.effort,
          mode: state.mode,
          prompt: state.prompt
        })
      });
      const data = await res.json();
      if (data.success) {
        btnLaunchHero.innerHTML = '<span>✅</span><span>¡Terminal Lanzada!</span>';
        setTimeout(() => {
          btnLaunchHero.innerHTML = origText;
          btnLaunchHero.disabled = false;
        }, 2500);
      }
    } catch (err) {
      console.error(err);
      btnLaunchHero.innerHTML = '<span>❌</span><span>Error al Lanzar</span>';
      setTimeout(() => {
        btnLaunchHero.innerHTML = origText;
        btnLaunchHero.disabled = false;
      }, 2500);
    }
  }

  if (btnLaunchHero) btnLaunchHero.addEventListener('click', triggerLaunch);
  if (btnTopLaunch) btnTopLaunch.addEventListener('click', triggerLaunch);

  updateCmdPreview();
}

// 3. Skills Catalog
async function initSkills() {
  const grid = document.getElementById('skillsGrid');
  const badge = document.getElementById('skillsCountBadge');
  if (!grid) return;

  try {
    const res = await fetch('/api/skills');
    const skills = await res.json();
    state.skills = skills;
    if (badge) badge.textContent = skills.length;

    grid.innerHTML = skills.map(s => `
      <div class="catalog-card">
        <div class="catalog-card-header">
          <span class="catalog-title">${s.name}</span>
          <span class="category-tag">${s.category}</span>
        </div>
        <p class="catalog-desc">${s.description || 'Habilidad técnica y operativa integrada.'}</p>
        <div style="font-family: var(--font-mono); font-size: 10px; color: var(--text-dim); margin-top: auto;">
          ${s.file}
        </div>
      </div>
    `).join('');
  } catch (e) {
    grid.innerHTML = '<p style="color: var(--text-dim);">No se pudieron cargar las skills.</p>';
  }
}

// 4. Subagents
async function initSubagents() {
  const grid = document.getElementById('subagentsGrid');
  if (!grid) return;

  try {
    const res = await fetch('/api/subagents');
    const subagents = await res.json();
    state.subagents = subagents;

    grid.innerHTML = subagents.map(sub => `
      <div class="catalog-card">
        <div class="catalog-card-header">
          <span class="catalog-title">${sub.name}</span>
          <span class="category-tag">${sub.type}</span>
        </div>
        <div style="font-size: 11.5px; font-weight: 600; color: var(--text-muted);">${sub.role}</div>
        <p class="catalog-desc">${sub.description}</p>
        <div style="font-family: var(--font-mono); font-size: 10px; color: var(--text-dim); margin-top: auto;">
          Dominio: ${sub.domain}
        </div>
      </div>
    `).join('');
  } catch (e) {
    grid.innerHTML = '<p style="color: var(--text-dim);">No se pudieron cargar los subagentes.</p>';
  }
}

// 5. Logs Timeline
async function initLogs() {
  const container = document.getElementById('logsTimeline');
  if (!container) return;

  try {
    const res = await fetch('/api/logs');
    const logs = await res.json();

    container.innerHTML = logs.map(l => `
      <div class="timeline-item">
        <div class="timeline-header">
          <span class="timeline-date">[${l.date}]</span>
          <span class="timeline-tag">${l.tag}</span>
        </div>
        <div class="timeline-title">${l.title}</div>
        <div class="timeline-body">${l.body}</div>
      </div>
    `).join('');
  } catch (e) {
    container.innerHTML = '<p style="color: var(--text-dim);">No se pudo cargar la bitácora.</p>';
  }
}

// 6. Interactive Obsidian Graph (Canvas Physics Engine)
async function initGraph() {
  const canvas = document.getElementById('graphCanvas');
  const container = document.querySelector('.graph-view-container');
  if (!canvas || !container) return;

  const ctx = canvas.getContext('2d');
  let width, height;

  function resize() {
    width = container.clientWidth;
    height = container.clientHeight;
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
  }
  window.resizeGraphCanvas = resize;
  resize();

  // Color mapping for minimalist light theme
  const categoryColors = {
    'Core': '#18181b',          // Deep carbon
    'Economía': '#27272a',      // Charcoal
    'Gameplay & RPG': '#3f3f46',// Slate dark
    'Protección': '#52525b',    // Zinc 600
    'Social & Chat': '#71717a', // Zinc 500
    'Conceptos': '#94a3b8',     // Slate 400
    'Síntesis': '#64748b',      // Slate 500
    'Fuentes': '#a1a1aa',       // Slate 300
    'General': '#71717a'
  };

  let nodes = [];
  let links = [];
  let nodeMap = {};

  // Fetch graph data
  try {
    const res = await fetch('/api/graph');
    const data = await res.json();
    state.graphData = data;

    document.getElementById('graphCountBadge').textContent = data.nodes.length;

    // Initialize positions in a circle/disk
    const radius = Math.min(width, height) * 0.35;
    nodes = data.nodes.map((n, i) => {
      const angle = (i / data.nodes.length) * 2 * Math.PI;
      const r = radius * (0.3 + 0.7 * Math.random());
      return {
        ...n,
        x: width / 2 + r * Math.cos(angle),
        y: height / 2 + r * Math.sin(angle),
        vx: 0,
        vy: 0,
        radius: Math.min(14, Math.max(5, 5 + (n.inDegree + n.outDegree) * 0.8)),
        color: categoryColors[n.category] || categoryColors['General']
      };
    });

    nodeMap = {};
    nodes.forEach(n => { nodeMap[n.id] = n; });

    links = data.links.map(l => ({
      source: nodeMap[l.source],
      target: nodeMap[l.target]
    })).filter(l => l.source && l.target);

  } catch (err) {
    console.error('Error cargando grafo:', err);
    return;
  }

  // Camera & Interaction
  let transform = { x: 0, y: 0, scale: 1 };
  let isDragging = false;
  let dragNode = null;
  let lastMouse = { x: 0, y: 0 };
  let hoveredNode = null;
  let selectedNode = null;

  // Physics loop
  function tickPhysics() {
    const kRepel = 2400;
    const kSpring = 0.04;
    const springLength = 85;
    const kCenter = 0.015;
    const damping = 0.86;

    // 1. Repulsion between all nodes
    for (let i = 0; i < nodes.length; i++) {
      const n1 = nodes[i];
      for (let j = i + 1; j < nodes.length; j++) {
        const n2 = nodes[j];
        const dx = n2.x - n1.x;
        const dy = n2.y - n1.y;
        const distSq = dx * dx + dy * dy || 1;
        const dist = Math.sqrt(distSq);

        if (dist < 400) {
          const force = kRepel / distSq;
          const fx = (dx / dist) * force;
          const fy = (dy / dist) * force;
          n1.vx -= fx;
          n1.vy -= fy;
          n2.vx += fx;
          n2.vy += fy;
        }
      }
    }

    // 2. Spring attraction along links
    for (let i = 0; i < links.length; i++) {
      const l = links[i];
      const dx = l.target.x - l.source.x;
      const dy = l.target.y - l.source.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const force = (dist - springLength) * kSpring;
      const fx = (dx / dist) * force;
      const fy = (dy / dist) * force;
      l.source.vx += fx;
      l.source.vy += fy;
      l.target.vx -= fx;
      l.target.vy -= fy;
    }

    // 3. Center gravity and apply velocity
    const cx = width / 2;
    const cy = height / 2;

    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      if (n === dragNode) continue;

      n.vx += (cx - n.x) * kCenter;
      n.vy += (cy - n.y) * kCenter;

      n.vx *= damping;
      n.vy *= damping;

      n.x += n.vx;
      n.y += n.vy;
    }
  }

  // Render loop
  function draw() {
    tickPhysics();

    ctx.save();
    ctx.clearRect(0, 0, width, height);

    // Apply transform (pan & zoom)
    ctx.translate(transform.x, transform.y);
    ctx.scale(transform.scale, transform.scale);

    // Draw links
    ctx.lineWidth = 1;
    for (let i = 0; i < links.length; i++) {
      const l = links[i];
      const isHighlighted = hoveredNode && (l.source === hoveredNode || l.target === hoveredNode);
      
      ctx.beginPath();
      ctx.moveTo(l.source.x, l.source.y);
      ctx.lineTo(l.target.x, l.target.y);

      if (isHighlighted) {
        ctx.strokeStyle = '#eab308';
        ctx.lineWidth = 2;
      } else {
        ctx.strokeStyle = '#e4e4e7';
        ctx.lineWidth = 1;
      }
      ctx.stroke();
    }

    // Draw nodes
    for (let i = 0; i < nodes.length; i++) {
      const n = nodes[i];
      const isHovered = n === hoveredNode;
      const isSelected = n === selectedNode;

      ctx.beginPath();
      ctx.arc(n.x, n.y, n.radius, 0, 2 * Math.PI);
      if (isHovered || isSelected) {
        ctx.fillStyle = '#eab308'; // Active/Hovered node in surgical yellow
      } else {
        ctx.fillStyle = n.color;
      }
      ctx.fill();

      // White ring
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();

      if (isHovered || isSelected) {
        ctx.strokeStyle = '#ca8a04';
        ctx.lineWidth = 2;
        ctx.stroke();

        ctx.shadowColor = 'rgba(234, 179, 8, 0.35)';
        ctx.shadowBlur = 10;
      } else {
        ctx.shadowBlur = 0;
      }

      // Draw label if hovered, selected or high scale
      if (transform.scale > 0.85 || isHovered || isSelected || n.radius > 9) {
        ctx.font = `${isHovered || isSelected ? 'bold 12px' : '500 11px'} Inter, sans-serif`;
        ctx.fillStyle = isHovered || isSelected ? '#09090b' : '#52525b';
        ctx.textAlign = 'center';
        ctx.fillText(n.label, n.x, n.y + n.radius + 14);
      }
    }

    ctx.restore();
    requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);

  // Mouse Coordinates to Graph Coordinates
  function toGraphCoords(clientX, clientY) {
    const rect = canvas.getBoundingClientRect();
    const mx = clientX - rect.left;
    const my = clientY - rect.top;
    return {
      x: (mx - transform.x) / transform.scale,
      y: (my - transform.y) / transform.scale
    };
  }

  // Find node under mouse
  function findNode(coords) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const dx = n.x - coords.x;
      const dy = n.y - coords.y;
      if (dx * dx + dy * dy <= (n.radius + 4) * (n.radius + 4)) {
        return n;
      }
    }
    return null;
  }

  // Event Listeners for Canvas
  canvas.addEventListener('mousedown', (e) => {
    const coords = toGraphCoords(e.clientX, e.clientY);
    dragNode = findNode(coords);

    if (dragNode) {
      selectedNode = dragNode;
      showInspector(dragNode);
    } else {
      isDragging = true;
    }
    lastMouse = { x: e.clientX, y: e.clientY };
  });

  window.addEventListener('mousemove', (e) => {
    const coords = toGraphCoords(e.clientX, e.clientY);

    if (dragNode) {
      dragNode.x = coords.x;
      dragNode.y = coords.y;
      dragNode.vx = 0;
      dragNode.vy = 0;
    } else if (isDragging) {
      const dx = e.clientX - lastMouse.x;
      const dy = e.clientY - lastMouse.y;
      transform.x += dx;
      transform.y += dy;
    } else {
      hoveredNode = findNode(coords);
    }
    lastMouse = { x: e.clientX, y: e.clientY };
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
    dragNode = null;
  });

  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.88;
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    transform.x = mx - (mx - transform.x) * zoomFactor;
    transform.y = my - (my - transform.y) * zoomFactor;
    transform.scale *= zoomFactor;
  });

  // Controls
  const btnReset = document.getElementById('btnGraphReset');
  const btnZoomIn = document.getElementById('btnGraphZoomIn');
  const btnZoomOut = document.getElementById('btnGraphZoomOut');
  const inputSearch = document.getElementById('inputGraphSearch');

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      transform = { x: 0, y: 0, scale: 1 };
    });
  }

  if (btnZoomIn) {
    btnZoomIn.addEventListener('click', () => {
      transform.scale *= 1.25;
    });
  }

  if (btnZoomOut) {
    btnZoomOut.addEventListener('click', () => {
      transform.scale *= 0.8;
    });
  }

  if (inputSearch) {
    inputSearch.addEventListener('input', () => {
      const query = inputSearch.value.trim().toLowerCase();
      if (!query) {
        selectedNode = null;
        return;
      }
      const match = nodes.find(n => n.label.toLowerCase().includes(query));
      if (match) {
        selectedNode = match;
        showInspector(match);
        // Center camera on match
        transform.x = width / 2 - match.x * transform.scale;
        transform.y = height / 2 - match.y * transform.scale;
      }
    });
  }

  // Inspector Sidebar
  function showInspector(n) {
    const inspector = document.getElementById('graphInspector');
    if (!inspector) return;
    inspector.style.display = 'block';
    document.getElementById('inspectorNodeTitle').textContent = n.label;
    document.getElementById('inspectorCategory').textContent = `Categoría: ${n.category}`;
    document.getElementById('inspectorStats').textContent = `Conexiones: ${n.inDegree} entrantes, ${n.outDegree} salientes`;
    document.getElementById('inspectorFile').textContent = n.file;
  }
}
