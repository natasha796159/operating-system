// Configuration
const REFRESH_RATE = 1500; // 1.5 seconds
const CPU_WARN = 50;
const CPU_CRIT = 80;
const MEM_WARN = 60;
const MEM_CRIT = 80;

// State Data
let processData = [];
let sortCol = 'cpu_percent';
let sortDesc = true;
let searchTerm = '';

let cpuHistory = Array(30).fill(0);
let memHistory = Array(30).fill(0);
let netHistory = Array(30).fill(0);
let startTime = Date.now();

// DOM Elements
const eValCpu = document.getElementById('val-cpu');
const eValCpuCores = document.getElementById('val-cpu-cores');
const eValCpuFreq = document.getElementById('val-cpu-freq');
const eBarCpu = document.getElementById('bar-cpu');
const eGraphCpu = document.getElementById('graph-cpu');

const eValMem = document.getElementById('val-mem');
const eBarMem = document.getElementById('bar-mem');
const eGraphMem = document.getElementById('graph-mem');

const eValDisk = document.getElementById('val-disk');
const eBarDisk = document.getElementById('bar-disk');

const eValNetUp = document.getElementById('val-net-up');
const eValNetDown = document.getElementById('val-net-down');
const eGraphNet = document.getElementById('graph-net');

const eProcessList = document.getElementById('process-list');
const eProcCount = document.getElementById('proc-count');
const eSearch = document.getElementById('search-input');
const eHeaders = document.querySelectorAll('th[data-sort]');
const eThemeToggle = document.getElementById('theme-toggle');

const eUptime = document.getElementById('uptime');
const eHealthScore = document.getElementById('health-score-val');
const eHealthRing = document.getElementById('health-ring');
const eRecommendation = document.getElementById('recommendation-text');

// Initialization
function init() {
    setupTheme();
    setupEventListeners();
    fetchSystemStats();
    fetchProcesses();
    setInterval(fetchSystemStats, REFRESH_RATE);
    setInterval(fetchProcesses, REFRESH_RATE);
    setInterval(updateUptime, 1000);
}

// Event Listeners
function setupEventListeners() {
    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.style.display = 'none');
            
            btn.classList.add('active');
            const target = btn.getAttribute('data-target');
            document.getElementById(target).style.display = 'block';
        });
    });

    // Process Search
    eSearch.addEventListener('input', (e) => {
        searchTerm = e.target.value.toLowerCase();
        renderTable();
    });

    // Process Sort
    eHeaders.forEach(th => {
        th.addEventListener('click', () => {
            const col = th.getAttribute('data-sort');
            if (sortCol === col) {
                sortDesc = !sortDesc;
            } else {
                sortCol = col;
                sortDesc = true;
                eHeaders.forEach(h => h.classList.remove('active-sort'));
                th.classList.add('active-sort');
            }
            renderTable();
        });
    });

    // Theme Toggle
    eThemeToggle.addEventListener('click', () => {
        const currentTh = document.documentElement.getAttribute('data-theme');
        const newTh = currentTh === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTh);
        localStorage.setItem('omniwatch_theme', newTh);
    });

    // Speedtest Action
    const btnSpeed = document.getElementById('btn-speedtest');
    if (btnSpeed) {
        btnSpeed.addEventListener('click', async () => {
            btnSpeed.textContent = "Testing...";
            btnSpeed.disabled = true;
            try {
                const res = await fetch('/api/speedtest');
                const result = await res.json();
                if (result.success) {
                    showToast(`Speedtest Done!\nDownload: ${formatBytes(result.download)}/s\nUpload: ${formatBytes(result.upload)}/s`, 'success');
                } else {
                    showToast(`Speedtest failed: ${result.error}`, 'danger');
                }
            } catch (err) {
                showToast(`Unable to run test. Server not responding.`, 'danger');
            }
            btnSpeed.textContent = "Run Speedtest";
            btnSpeed.disabled = false;
        });
    }
}

function setupTheme() {
    const savedTheme = localStorage.getItem('omniwatch_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

let systemBootTime = null;

function updateUptime() {
    if (!systemBootTime) {
        eUptime.textContent = `Uptime: Loading...`;
        return;
    }
    const diff = Math.floor((Date.now() / 1000) - systemBootTime);
    const d = Math.floor(diff / 86400);
    const h = Math.floor((diff % 86400) / 3600);
    const m = Math.floor((diff % 3600) / 60);
    const s = diff % 60;
    
    if (d > 0) {
        eUptime.textContent = `OS Uptime: ${d}d ${h}h ${m}m ${s}s`;
    } else {
        eUptime.textContent = `OS Uptime: ${h}h ${m}m ${s}s`;
    }
}

// Formatting Utils
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024, dm = 1, sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function getColorClass(percent, type) {
    let warn = type === 'cpu' ? CPU_WARN : MEM_WARN;
    let crit = type === 'cpu' ? CPU_CRIT : MEM_CRIT;
    if (percent >= crit) return 'danger';
    if (percent >= warn) return 'warning';
    return '';
}

// Fetch API Data
async function fetchSystemStats() {
    try {
        const res = await fetch('/api/system');
        const data = await res.json();
        updateSystemUI(data);
    } catch (err) {
        console.error("System Fetch Error:", err);
    }
}

async function fetchProcesses() {
    try {
        const res = await fetch('/api/processes');
        processData = await res.json();
        renderTable();
    } catch (err) {
        console.error("Process Fetch Error:", err);
    }
}

// Update UI
function updateSystemUI(data) {
    // Health Banner
    eHealthScore.textContent = data.health_score;
    eRecommendation.textContent = data.recommendation;
    let hColor = 'var(--success)';
    if(data.health_score < 50) hColor = 'var(--danger)';
    else if(data.health_score < 80) hColor = 'var(--warning)';
    eHealthRing.style.background = `conic-gradient(${hColor} ${data.health_score}%, var(--bg-main) 0)`;

    // Setup boot time if not set
    if (data.system && data.system.boot_time && !systemBootTime) {
        systemBootTime = data.system.boot_time;
    }

    // CPU
    const cCpu = data.cpu.percent;
    eValCpu.textContent = `Usage: ${cCpu}%`;
    const ecStatus = document.getElementById('cpu-status');
    if (ecStatus) ecStatus.textContent = `Status: ${data.cpu.status}`;
    
    if (eValCpuCores) eValCpuCores.textContent = `${data.cpu.cores_physical} / ${data.cpu.cores_logical}`;
    if (eValCpuFreq) eValCpuFreq.textContent = `${data.cpu.freq_current} MHz`;
    
    eBarCpu.style.width = `${cCpu}%`;
    eBarCpu.className = `progress-fill ${getColorClass(cCpu, 'cpu')}`;
    updateGraph(cpuHistory, cCpu, eGraphCpu, getColorClass(cCpu, 'cpu'));
    
    // Memory
    const truePercent = data.memory.true_percent;
    const trueUsed = formatBytes(data.memory.true_used);
    const cached = formatBytes(data.memory.cached + (data.memory.buffers || 0));
    const avail = formatBytes(data.memory.available);
    
    eValMem.textContent = `True Usage: ${truePercent}%`;
    document.getElementById('mem-true').textContent = trueUsed;
    document.getElementById('mem-cached').textContent = cached;
    document.getElementById('mem-avail').textContent = avail;
    document.getElementById('mem-status').textContent = data.memory.status;
    
    eBarMem.style.width = `${truePercent}%`;
    eBarMem.className = `progress-fill ${getColorClass(truePercent, 'mem')}`;
    updateGraph(memHistory, truePercent, eGraphMem, getColorClass(truePercent, 'mem'));

    // Network
    const upSpeed = data.network.upload_speed;
    const downSpeed = data.network.download_speed;
    eValNetUp.textContent = `${formatBytes(upSpeed)}/s`;
    eValNetDown.textContent = `${formatBytes(downSpeed)}/s`;
    
    // Convert highest speed relative to 10MB/s (10485760 bytes) for graph percentage scaling
    const maxSpeed = Math.max(upSpeed, downSpeed);
    const netPercent = Math.min(100, (maxSpeed / 10485760) * 100);
    updateGraph(netHistory, netPercent, eGraphNet, '');

    // Disk
    const cDiskActivity = data.disk.activity_percent || 0;
    const cDiskCapacity = data.disk.percent || 0;
    const readSpd = data.disk.read_speed || 0;
    const writeSpd = data.disk.write_speed || 0;

    eValDisk.textContent = `${cDiskActivity.toFixed(1)}% Active | ${formatBytes(readSpd)}/s R | ${formatBytes(writeSpd)}/s W`;
    eBarDisk.style.width = `${cDiskActivity}%`;
    eBarDisk.className = `progress-fill ${getColorClass(cDiskActivity, 'disk')}`;
    
    const infoDisk = document.querySelector('#card-disk .disk-info');
    if (infoDisk) {
        infoDisk.textContent = `Storage space: ${formatBytes(data.disk.used)} / ${formatBytes(data.disk.total)} (${cDiskCapacity}%) used`;
    }

    checkAlerts(cCpu, truePercent);
}

// Graph Drawing (Canvas API)
function updateGraph(historyArray, newValue, canvasElement, colorClass) {
    historyArray.push(newValue);
    historyArray.shift(); // keep length constant
    
    const ctx = canvasElement.getContext('2d');
    const w = canvasElement.width;
    const h = canvasElement.height;
    
    ctx.clearRect(0, 0, w, h);
    
    // Determine color
    let strokeColor = '#10b981'; // success
    if (colorClass === 'warning') strokeColor = '#f59e0b';
    if (colorClass === 'danger') strokeColor = '#ef4444';
    
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    if (isLight) {
        if (colorClass === '') strokeColor = '#059669';
        if (colorClass === 'warning') strokeColor = '#d97706';
        if (colorClass === 'danger') strokeColor = '#dc2626';
    }

    ctx.beginPath();
    const step = w / (historyArray.length - 1);
    
    let region = new Path2D();
    
    for (let i = 0; i < historyArray.length; i++) {
        const val = historyArray[i];
        const x = i * step;
        const y = h - (val / 100 * h); // scale to 0-100
        
        if (i === 0) {
            ctx.moveTo(x, y);
            region.moveTo(x, y);
        } else {
            const prevX = (i - 1) * step;
            const prevY = h - (historyArray[i - 1] / 100 * h);
            const cpX = (prevX + x) / 2;
            
            ctx.bezierCurveTo(cpX, prevY, cpX, y, x, y);
            region.bezierCurveTo(cpX, prevY, cpX, y, x, y);
        }
    }
    
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = strokeColor;
    ctx.lineJoin = 'round';
    ctx.stroke();

    // Fill area under curve with linear gradient
    region.lineTo(w, h);
    region.lineTo(0, h);
    region.closePath();
    
    const gradient = ctx.createLinearGradient(0, 0, 0, h);
    gradient.addColorStop(0, strokeColor + '50'); // 31% opacity
    gradient.addColorStop(1, strokeColor + '00'); // 0% opacity
    
    ctx.fillStyle = gradient;
    ctx.fill(region);
}

// Process rendering
function renderTable() {
    let filtered = processData.filter(p => {
        const pName = p.name ? p.name.toLowerCase() : '';
        const pPid = p.pid.toString();
        return pName.includes(searchTerm) || pPid.includes(searchTerm);
    });

    // Custom sort based on sortCol
    filtered.sort((a, b) => {
        let valA = a[sortCol] || 0;
        let valB = b[sortCol] || 0;
        
        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();
        
        if (valA < valB) return sortDesc ? 1 : -1;
        if (valA > valB) return sortDesc ? -1 : 1;
        return 0;
    });

    eProcCount.textContent = processData.length;

    // Use fragment for performance
    const fragment = document.createDocumentFragment();
    
    filtered.forEach(p => {
        const tr = document.createElement('tr');
        
        let rowClass = "";
        let cp = p.cpu_percent || 0;
        if (cp > 50) rowClass = "critical-cpu";
        else if (cp > 20) rowClass = "high-cpu";
        
        if (rowClass) tr.className = rowClass;

        tr.innerHTML = `
            <td>${p.pid}</td>
            <td><strong>${p.name || 'Unknown'}</strong></td>
            <td>${cp.toFixed(1)}%</td>
            <td>${(p.memory_percent || 0).toFixed(1)}%</td>
            <td>
                <button class="btn-kill" onclick="requestKill(${p.pid}, '${p.name}')">Kill</button>
            </td>
        `;
        fragment.appendChild(tr);
    });

    eProcessList.innerHTML = '';
    eProcessList.appendChild(fragment);
}

// action handlers
async function requestKill(pid, name) {
    if(confirm(`Are you sure you want to kill process: ${name} (PID: ${pid})?\nWarning: This may cause system instability.`)) {
        try {
            const res = await fetch(`/api/kill/${pid}`, { method: 'POST' });
            const data = await res.json();
            
            if (data.success) {
                showToast(`Successfully terminated process '${name}'`, 'success');
                fetchProcesses(); // Refresh immediately
            } else {
                showToast(data.error || 'Failed to kill process.', 'danger');
            }
        } catch (err) {
            showToast('API request failed.', 'danger');
        }
    }
}

// Insights and Alerts
let lastAlertTime = 0;
function checkAlerts(cpu, mem) {
    const now = Date.now();
    if (now - lastAlertTime < 10000) return; // Alert coercion (10s)

    if (cpu >= CPU_CRIT) {
        showToast(`CRITICAL: CPU usage at ${cpu}%`, 'danger');
        lastAlertTime = now;
    } else if (mem >= MEM_CRIT) {
        showToast(`CRITICAL: Memory usage at ${mem}%`, 'danger');
        lastAlertTime = now;
    }
}

// Toasts
function showToast(message, type = 'danger') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    // Auto remove
    setTimeout(() => {
        if(toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

// Start
document.addEventListener('DOMContentLoaded', init);
