const panel    = document.getElementById('info-panel');
const content  = document.getElementById('info-content');
const closeBtn = document.getElementById('info-close');

export function setupInfoPanel() {
  closeBtn.addEventListener('click', hideInfo);
}

export function hideInfo() {
  panel.classList.remove('visible');
}

export function showInfo(userData) {
  const { label = '—', source = '—', info = {} } = userData;

  const sourceColor = {
    ENGINEERING: '#4a9eff',
    CAD:         '#4a9eff',
    SIMULATED:   '#2ad4a0',
    SCHEMATIC:   '#c07830',
    PROVISIONAL: '#c07830',
    CONCEPT:     '#a050c0',
  }[source] || '#8a9ab0';

  let html = `
    <div class="comp-name" style="color:${sourceColor}">${label}</div>
    <div class="irow">
      <span class="ilabel">SOURCE</span>
      <span class="ivalue" style="color:${sourceColor}">${source}</span>
    </div>`;

  const SKIP = new Set(['description', 'warning', 'source_cfd', 'source', 'status']);

  for (const [k, v] of Object.entries(info)) {
    if (SKIP.has(k) || v === null || v === undefined) continue;
    html += `<div class="irow">
      <span class="ilabel">${k.replace(/_/g, ' ').toUpperCase()}</span>
      <span class="ivalue">${v}</span>
    </div>`;
  }

  if (info.status) {
    html += `<div><span class="sbadge ${statusClass(info.status)}">${info.status}</span></div>`;
  }
  if (info.warning) {
    html += `<div class="info-warn">⚠ ${info.warning}</div>`;
  }
  if (info.description) {
    html += `<div class="info-desc">${info.description}</div>`;
  }
  if (info.source_cfd) {
    html += `<div class="info-src">CFD source: ${info.source_cfd}</div>`;
  }

  content.innerHTML = html;
  panel.classList.add('visible');
}

function statusClass(status = '') {
  const s = status.toUpperCase();
  if (s.includes('SIMULATED'))                           return 's-sim';
  if (s.includes('SELECTED') || s.includes('CONTROL'))  return 's-sel';
  if (s.includes('CONCEPT'))                             return 's-con';
  if (s.includes('PENDING'))                             return 's-pend';
  return 's-prov';
}
