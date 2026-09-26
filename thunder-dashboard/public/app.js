let currentMetrics = null;
let charts = {};
let currentMarketMode = 'es'; // 'es' or 'en'

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', async () => {
    lucide.createIcons();
    setupTabs();
    setupCalculator();
    setupActionButtons();
    await loadMetrics();
});

// Cargar métricas de la API local
async function loadMetrics() {
    try {
        const response = await fetch('/api/metrics');
        if (!response.ok) throw new Error('Error al obtener datos');
        currentMetrics = await response.json();
        renderDashboard(currentMetrics);
    } catch (err) {
        console.error('Fallo al cargar métricas:', err);
    }
}

// Renderizar todo el cuadro de mando
function renderDashboard(data) {
    if (!data) return;

    // Actualizar KPIs superiores
    document.getElementById('val-current-ccu').innerText = data.kpis.currentCcu;
    document.getElementById('val-peak-ccu').innerText = data.kpis.peakCcuToday;
    document.getElementById('val-retention-d1').innerText = `${data.kpis.retentionD1}%`;
    document.getElementById('val-retention-d7').innerText = `${data.kpis.retentionD7}%`;
    document.getElementById('val-tps').innerText = data.kpis.currentTps.toFixed(2);
    document.getElementById('val-mspt').innerText = `${data.kpis.avgMspt} ms`;
    document.getElementById('val-revenue').innerText = `${data.kpis.monthlyRevenueEur.toLocaleString('es-ES')} €`;
    document.getElementById('val-arppu').innerText = `${data.kpis.arppuEur.toFixed(2)} €`;

    // Renderizar gráficos con paleta clara
    renderWeeklyTrafficChart(data.weeklyTrend);
    renderPlatformBreakdownChart(data.platformBreakdown);
    renderGeographyCards(data.geography);
    renderRetentionChart(data.retentionCurve);
    renderTechnicalStressChart(data.stressTestProfile);
    renderPaymentMethodsChart(data.paymentMethods);
    renderPaymentBars(data.paymentMethods);

    // Actualizar calculadora
    updateCalculator();
    lucide.createIcons();
}

// Configuración de pestañas y enlaces de la barra lateral
function setupTabs() {
    const buttons = document.querySelectorAll('.sidebar-item-bold, .sidebar-item-clean, .sidebar-plan-link, .sidebar-link-yellow, .sidebar-link');
    const panes = document.querySelectorAll('.tab-pane');

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            if (!targetTab) return;

            buttons.forEach(b => {
                b.classList.remove('active');
            });
            btn.classList.add('active');

            panes.forEach(pane => {
                if (pane.id === targetTab) {
                    pane.classList.remove('hidden');
                } else {
                    pane.classList.add('hidden');
                }
            });

            // Forzar resize de Chart.js si se redibuja pestaña
            window.dispatchEvent(new Event('resize'));
        });
    });
}

// Botones de acción
function setupActionButtons() {
    document.getElementById('btn-refresh').addEventListener('click', async () => {
        const btn = document.getElementById('btn-refresh');
        btn.innerHTML = `<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> Cargando...`;
        await loadMetrics();
        btn.innerHTML = `<i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Actualizar Datos`;
        lucide.createIcons();
    });

    document.getElementById('btn-reset').addEventListener('click', async () => {
        if (confirm("¿Desea restablecer todas las métricas al benchmark original del estudio de mercado?")) {
            await fetch('/api/metrics/reset', { method: 'POST' });
            await loadMetrics();
        }
    });
}

// Chart.js Opciones Globales de Modo Claro
const lightChartOptions = {
    gridColor: '#e2e8f0',
    tickColor: '#64748b',
    tooltipBg: '#ffffff',
    tooltipTitle: '#0f172a',
    tooltipBody: '#334155',
    tooltipBorder: '#cbd5e1'
};

// Gráfico 1: Evolución de Tráfico Semanal
function renderWeeklyTrafficChart(weeklyTrend) {
    const ctx = document.getElementById('chartWeeklyTraffic').getContext('2d');
    if (charts.weeklyTraffic) charts.weeklyTraffic.destroy();

    charts.weeklyTraffic = new Chart(ctx, {
        type: 'line',
        data: {
            labels: weeklyTrend.map(w => w.day),
            datasets: [
                {
                    label: 'Pico CCU (Simultáneos)',
                    data: weeklyTrend.map(w => w.peakCcu),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.08)',
                    borderWidth: 2.5,
                    tension: 0.35,
                    fill: true,
                    yAxisID: 'y'
                },
                {
                    label: 'Nuevos Registros Diarios',
                    data: weeklyTrend.map(w => w.newPlayers),
                    borderColor: '#10b981',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    tension: 0.2,
                    yAxisID: 'y'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { labels: { color: '#334155', font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 } } },
                tooltip: { 
                    backgroundColor: lightChartOptions.tooltipBg, 
                    titleColor: lightChartOptions.tooltipTitle, 
                    bodyColor: lightChartOptions.tooltipBody,
                    borderColor: lightChartOptions.tooltipBorder, 
                    borderWidth: 1,
                    padding: 10,
                    boxPadding: 4
                }
            },
            scales: {
                x: { grid: { color: lightChartOptions.gridColor }, ticks: { color: lightChartOptions.tickColor, font: { weight: 500 } } },
                y: { grid: { color: lightChartOptions.gridColor }, ticks: { color: lightChartOptions.tickColor, font: { weight: 500 } } }
            }
        }
    });
}

// Gráfico 2: Desglose por Plataforma
function renderPlatformBreakdownChart(breakdown) {
    const ctx = document.getElementById('chartPlatformBreakdown').getContext('2d');
    if (charts.platformBreakdown) charts.platformBreakdown.destroy();

    charts.platformBreakdown = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Bedrock Móvil', 'Java No-Premium', 'Java Premium', 'Bedrock Consolas'],
            datasets: [{
                data: [breakdown.bedrockMobile, breakdown.javaNoPremium, breakdown.javaPremium, breakdown.bedrockConsole],
                backgroundColor: ['#2563eb', '#10b981', '#f59e0b', '#7c3aed'],
                borderColor: '#ffffff',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '72%',
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: lightChartOptions.tooltipBg,
                    titleColor: lightChartOptions.tooltipTitle,
                    bodyColor: lightChartOptions.tooltipBody,
                    borderColor: lightChartOptions.tooltipBorder,
                    borderWidth: 1,
                    callbacks: {
                        label: ctx => ` ${ctx.label}: ${ctx.parsed}% del total`
                    }
                }
            }
        }
    });
}

// Renderizar Tarjetas de Geografía
function renderGeographyCards(geography) {
    const container = document.getElementById('geo-cards-container');
    container.innerHTML = '';

    geography.forEach(g => {
        const div = document.createElement('div');
        div.className = 'p-3 rounded-lg bg-slate-50 border border-slate-200 text-center space-y-1';
        div.innerHTML = `
            <p class="text-xs text-slate-500 font-medium">${g.country}</p>
            <p class="text-base font-extrabold font-mono text-slate-900">${g.share}%</p>
            <p class="text-[11px] text-blue-600 font-mono font-semibold">~${g.ccuAvg} CCU med.</p>
        `;
        container.appendChild(div);
    });
}

// Gráfico 3: Curva de Retención
function renderRetentionChart(retentionCurve) {
    const ctx = document.getElementById('chartRetentionCurve').getContext('2d');
    if (charts.retention) charts.retention.destroy();

    charts.retention = new Chart(ctx, {
        type: 'line',
        data: {
            labels: retentionCurve.map(r => r.day),
            datasets: [
                {
                    label: 'Retención Real de la Red (%)',
                    data: retentionCurve.map(r => r.actual),
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.12)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.3
                },
                {
                    label: 'Benchmark Óptimo de Mercado (%)',
                    data: retentionCurve.map(r => r.benchmarkOptimal),
                    borderColor: '#2563eb',
                    borderDash: [4, 4],
                    borderWidth: 2,
                    tension: 0.3
                },
                {
                    label: 'Mínimo de Supervivencia (%)',
                    data: retentionCurve.map(r => r.benchmarkMin),
                    borderColor: '#e11d48',
                    borderDash: [6, 4],
                    borderWidth: 1.5,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#334155', font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 } } },
                tooltip: { 
                    backgroundColor: lightChartOptions.tooltipBg, 
                    titleColor: lightChartOptions.tooltipTitle, 
                    bodyColor: lightChartOptions.tooltipBody,
                    borderColor: lightChartOptions.tooltipBorder, 
                    borderWidth: 1 
                }
            },
            scales: {
                x: { grid: { color: lightChartOptions.gridColor }, ticks: { color: lightChartOptions.tickColor, font: { weight: 500 } } },
                y: {
                    grid: { color: lightChartOptions.gridColor },
                    ticks: { color: lightChartOptions.tickColor, font: { weight: 500 }, callback: v => `${v}%` }
                }
            }
        }
    });
}

// Gráfico 4: Correlación Técnica CCU vs MSPT
function renderTechnicalStressChart(profile) {
    const ctx = document.getElementById('chartTechnicalStress').getContext('2d');
    if (charts.technicalStress) charts.technicalStress.destroy();

    charts.technicalStress = new Chart(ctx, {
        type: 'line',
        data: {
            labels: profile.map(p => `${p.ccu} CCU`),
            datasets: [
                {
                    label: 'MSPT Estimado (ms)',
                    data: profile.map(p => p.mspt),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.08)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.25
                },
                {
                    label: 'Límite de 20 TPS (50.0 ms)',
                    data: profile.map(() => 50.0),
                    borderColor: '#e11d48',
                    borderDash: [6, 6],
                    borderWidth: 2,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#334155', font: { family: 'Plus Jakarta Sans', size: 12, weight: 600 } } },
                tooltip: {
                    backgroundColor: lightChartOptions.tooltipBg,
                    titleColor: lightChartOptions.tooltipTitle,
                    bodyColor: lightChartOptions.tooltipBody,
                    borderColor: lightChartOptions.tooltipBorder,
                    borderWidth: 1,
                    callbacks: {
                        afterLabel: ctx => ` Estado: ${profile[ctx.dataIndex].status}`
                    }
                }
            },
            scales: {
                x: { grid: { color: lightChartOptions.gridColor }, ticks: { color: lightChartOptions.tickColor, font: { weight: 500 } } },
                y: {
                    grid: { color: lightChartOptions.gridColor },
                    ticks: { color: lightChartOptions.tickColor, font: { weight: 500 }, callback: v => `${v} ms` },
                    max: 60
                }
            }
        }
    });
}

// Gráfico 5: Métodos de Pago
function renderPaymentMethodsChart(paymentMethods) {
    const ctx = document.getElementById('chartPaymentMethods').getContext('2d');
    if (charts.payments) charts.payments.destroy();

    charts.payments = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: paymentMethods.map(p => p.method),
            datasets: [{
                data: paymentMethods.map(p => p.share),
                backgroundColor: ['#10b981', '#f59e0b', '#2563eb', '#7c3aed', '#94a3b8'],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: lightChartOptions.tooltipBg,
                    titleColor: lightChartOptions.tooltipTitle,
                    bodyColor: lightChartOptions.tooltipBody,
                    borderColor: lightChartOptions.tooltipBorder,
                    borderWidth: 1,
                    callbacks: {
                        label: ctx => ` ${ctx.label}: ${ctx.parsed}%`
                    }
                }
            }
        }
    });
}

// Barras de progreso de métodos de pago
function renderPaymentBars(paymentMethods) {
    const container = document.getElementById('payment-bars-container');
    container.innerHTML = '';

    paymentMethods.forEach(p => {
        const div = document.createElement('div');
        div.className = 'p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5';
        div.innerHTML = `
            <div class="flex justify-between text-xs">
                <span class="font-semibold text-slate-800">${p.method}</span>
                <span class="font-mono text-amber-600 font-bold">${p.volumeEur.toFixed(2)} € (${p.share}%)</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2">
                <div class="bg-amber-500 h-2 rounded-full" style="width: ${p.share}%"></div>
            </div>
        `;
        container.appendChild(div);
    });
}

// Setup del Simulador Financiero
function setupCalculator() {
    const slider = document.getElementById('calc-slider-ccu');
    const modeEs = document.getElementById('calc-mode-es');
    const modeEn = document.getElementById('calc-mode-en');

    slider.addEventListener('input', updateCalculator);

    modeEs.addEventListener('click', () => {
        currentMarketMode = 'es';
        modeEs.className = "px-3.5 py-1.5 rounded-md font-extrabold bg-thunderYellow text-slate-900 border border-amber-400 shadow-xs transition";
        modeEn.className = "px-3.5 py-1.5 rounded-md font-medium text-slate-600 hover:text-slate-900 transition";
        updateCalculator();
    });

    modeEn.addEventListener('click', () => {
        currentMarketMode = 'en';
        modeEn.className = "px-3.5 py-1.5 rounded-md font-extrabold bg-thunderYellow text-slate-900 border border-amber-400 shadow-xs transition";
        modeEs.className = "px-3.5 py-1.5 rounded-md font-medium text-slate-600 hover:text-slate-900 transition";
        updateCalculator();
    });
}

function updateCalculator() {
    const ccu = parseInt(document.getElementById('calc-slider-ccu').value);
    document.getElementById('calc-label-ccu').innerText = `${ccu} CCU`;

    // Parámetros según mercado
    const isEn = currentMarketMode === 'en';
    const currency = isEn ? '$' : '€';

    // Ratios de mercado
    const monthlyUniqueMultiplier = 110;
    const uniquePlayers = ccu * monthlyUniqueMultiplier;

    // Tasa de conversión y gasto medio
    const convRate = isEn ? 0.038 : 0.018;
    const arppu = isEn ? 18.00 : 4.50;

    // Cálculo de Costes de Infraestructura (OPEX)
    let opex = 140;
    if (ccu > 200) opex = 210;
    if (ccu > 450) opex = 360;
    if (ccu > 800) opex = 580;
    if (ccu > 1200) opex = 890;

    // Ingresos Brutos
    const payingPlayers = Math.round(uniquePlayers * convRate);
    const grossRevenue = Math.round(payingPlayers * arppu);

    // Margen Neto
    const netProfit = Math.max(0, grossRevenue - opex);
    const marginPct = grossRevenue > 0 ? ((netProfit / grossRevenue) * 100).toFixed(1) : 0;

    // Actualizar UI
    document.getElementById('calc-unique-players').innerText = `~${uniquePlayers.toLocaleString('es-ES')} únicos/mes`;
    document.getElementById('calc-conv-rate').innerText = `${(convRate * 100).toFixed(1)}%`;
    document.getElementById('calc-arppu-val').innerText = `${arppu.toFixed(2)} ${currency}`;

    document.getElementById('calc-opex').innerText = `~${opex} ${currency} / mes`;
    document.getElementById('calc-gross').innerText = `~${grossRevenue.toLocaleString('es-ES')} ${currency} / mes`;
    document.getElementById('calc-net-profit').innerText = `~${netProfit.toLocaleString('es-ES')} ${currency} / mes`;
    document.getElementById('calc-margin-pct').innerText = `Margen: ${marginPct}%`;
}
