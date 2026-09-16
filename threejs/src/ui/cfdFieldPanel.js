import { getTurboColor } from '../scene/createCfdPlane.js';

const panel = document.getElementById('cfd-field-panel');

let _onChange = null;

const _state = {
  caseId:  'GEO_C',
  fieldId: 'U_MAGNITUDE',
  planeId: 'longitudinal',
  autoRange: true,
  manualMin: 0,
  manualMax: 5,
};

const CASES = [
  { id: 'GEO_C',         label: 'GEO_C',         status: 'CONVERGED',           ts: '926' },
  { id: 'GEO_C_CONFIRM', label: 'GEO_C_CONFIRM',  status: 'CONVERGED',           ts: '926' },
  { id: 'CASE_M_SEALED', label: 'CASE_M_SEALED',  status: 'PARTIALLY CONVERGED', ts: '5000' },
];

const FIELDS = [
  { id: 'U_MAGNITUDE', label: '|U| Velocity magnitude', units: 'm/s' },
  { id: 'P_STATIC',    label: 'P Static pressure',       units: 'Pa (gauge)' },
];

const PLANES = [
  { id: 'longitudinal', label: 'Longitudinal (y=0.400 m)' },
  { id: 'filter_xsec',  label: 'Filter cross-section (x=0.305 m)' },
];

export function setupCfdFieldPanel(onChange) {
  _onChange = onChange;
  panel.innerHTML = '';

  // ── Title
  _row('CFD FIELD VISUALIZATION', 'cf-heading');

  // ── Case selector
  _row('CASE', 'cf-sublabel');
  const caseWrap = _el('div', 'cf-btn-group');
  for (const c of CASES) {
    const btn = _el('button', 'cf-btn' + (c.id === _state.caseId ? ' active' : ''));
    btn.textContent = c.label;
    btn.title = `Status: ${c.status} | Timestep: ${c.ts}`;
    btn.addEventListener('click', () => {
      caseWrap.querySelectorAll('.cf-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      _state.caseId = c.id;
      _fire();
    });
    caseWrap.appendChild(btn);
  }
  panel.appendChild(caseWrap);

  // ── Field selector
  _row('FIELD', 'cf-sublabel');
  const fieldWrap = _el('div', 'cf-btn-group');
  for (const f of FIELDS) {
    const btn = _el('button', 'cf-btn' + (f.id === _state.fieldId ? ' active' : ''));
    btn.textContent = f.label;
    btn.title = `Units: ${f.units}`;
    btn.addEventListener('click', () => {
      fieldWrap.querySelectorAll('.cf-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      _state.fieldId = f.id;
      _fire();
    });
    fieldWrap.appendChild(btn);
  }
  panel.appendChild(fieldWrap);

  // ── Plane selector
  _row('PLANE', 'cf-sublabel');
  const planeWrap = _el('div', 'cf-btn-group');
  for (const pl of PLANES) {
    const btn = _el('button', 'cf-btn' + (pl.id === _state.planeId ? ' active' : ''));
    btn.textContent = pl.label;
    btn.addEventListener('click', () => {
      planeWrap.querySelectorAll('.cf-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      _state.planeId = pl.id;
      _fire();
    });
    planeWrap.appendChild(btn);
  }
  panel.appendChild(planeWrap);

  // ── Range control
  _row('COLOR RANGE', 'cf-sublabel');
  const rangeWrap = _el('div', 'cf-range-row');

  const autoBtn = _el('button', 'cf-btn cf-range-auto active');
  autoBtn.textContent = 'AUTO';
  autoBtn.addEventListener('click', () => {
    _state.autoRange = true;
    autoBtn.classList.add('active');
    minInput.disabled = maxInput.disabled = true;
    _fireRange();
  });

  const minInput = _el('input', 'cf-range-input');
  minInput.type = 'number'; minInput.step = '0.1';
  minInput.value = _state.manualMin; minInput.disabled = true;
  minInput.placeholder = 'min';

  const maxInput = _el('input', 'cf-range-input');
  maxInput.type = 'number'; maxInput.step = '0.1';
  maxInput.value = _state.manualMax; maxInput.disabled = true;
  maxInput.placeholder = 'max';

  const manualBtn = _el('button', 'cf-btn cf-range-manual');
  manualBtn.textContent = 'MANUAL';
  manualBtn.addEventListener('click', () => {
    _state.autoRange = false;
    autoBtn.classList.remove('active');
    minInput.disabled = maxInput.disabled = false;
    _fireRange();
  });

  minInput.addEventListener('change', () => {
    _state.manualMin = parseFloat(minInput.value) || 0;
    if (!_state.autoRange) _fireRange();
  });
  maxInput.addEventListener('change', () => {
    _state.manualMax = parseFloat(maxInput.value) || 1;
    if (!_state.autoRange) _fireRange();
  });

  rangeWrap.append(autoBtn, manualBtn, minInput, _el_text('–'), maxInput);
  panel.appendChild(rangeWrap);

  // ── Legend canvas
  const legendWrap = _el('div', 'cf-legend-wrap');
  const canvas = _el('canvas', 'cf-legend-canvas');
  canvas.id = 'cf-legend-canvas';
  canvas.width = 200; canvas.height = 18;
  legendWrap.appendChild(canvas);
  panel.appendChild(legendWrap);

  // ── Legend labels
  const lblWrap = _el('div', 'cf-legend-labels');
  lblWrap.id = 'cf-legend-labels';
  panel.appendChild(lblWrap);

  // ── Status area
  const statusEl = _el('div', 'cf-status');
  statusEl.id = 'cf-status';
  statusEl.textContent = 'Loading...';
  panel.appendChild(statusEl);

  // ── Provenance area
  const provEl = _el('div', 'cf-provenance');
  provEl.id = 'cf-provenance';
  panel.appendChild(provEl);

  // ── Warning
  const warnEl = _el('div', 'cf-warn');
  warnEl.textContent = 'SIMULATION ONLY — NOT PHYSICALLY VALIDATED';
  panel.appendChild(warnEl);

  _drawLegend(0, 1, 'm/s');
  _fire();
}

export function updateCfdPanelStatus(dataset, error) {
  const statusEl  = document.getElementById('cf-status');
  const provEl    = document.getElementById('cf-provenance');
  const lblEl     = document.getElementById('cf-legend-labels');

  if (error || !dataset) {
    if (statusEl) statusEl.textContent = error || 'No data loaded.';
    if (provEl)   provEl.innerHTML = '';
    return;
  }

  const units    = dataset.units || '';
  const dmin     = dataset.data_min;
  const dmax     = dataset.data_max;
  const convBadge = dataset.convergence_status === 'CONVERGED'
    ? '✔ CONVERGED'
    : '⚠ PARTIALLY CONVERGED';

  if (statusEl) statusEl.textContent =
    `${convBadge} | iter ${dataset.source_timestep} | ${dataset.n_valid}/${dataset.n_total} grid pts`;

  _drawLegend(dmin, dmax, units);

  if (lblEl) {
    lblEl.innerHTML =
      `<span>${_fmt(dmin, units)}</span><span>${_fmt((dmin+dmax)/2, units)}</span><span>${_fmt(dmax, units)}</span>`;
  }

  if (provEl) {
    provEl.innerHTML = _provRows(dataset);
  }
}

function _provRows(d) {
  const rows = [
    ['Case',         d.case_id],
    ['Source path',  d.case_path],
    ['Timestep',     d.source_timestep],
    ['Field',        d.field_description],
    ['Derivation',   d.derivation],
    ['Units',        d.units],
    ['Plane',        d.grid?.description ?? d.plane],
    ['Grid',         `${d.grid?.n_axis1}×${d.grid?.n_axis2}`],
    ['Interpolation',d.grid?.interpolation ?? 'see data'],
    ['Convergence',  d.convergence_status],
    ['Validation',   d.validation_status],
    ['ρ (density)',  d.provenance?.rho_kg_m3 ? `${d.provenance.rho_kg_m3} kg/m³` : '—'],
    ['Pressure note',d.provenance?.pressure_note ?? '—'],
    ['Export script',d.provenance?.export_script ?? '—'],
  ];
  return rows.map(([k, v]) =>
    `<div class="cf-prov-row"><span class="cf-prov-key">${k}</span><span class="cf-prov-val">${v}</span></div>`
  ).join('');
}

function _drawLegend(min, max, units) {
  const canvas = document.getElementById('cf-legend-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width, h = canvas.height;
  for (let x = 0; x < w; x++) {
    const t = x / (w - 1);
    const [r, g, b] = getTurboColor(t);
    ctx.fillStyle = `rgb(${Math.round(r*255)},${Math.round(g*255)},${Math.round(b*255)})`;
    ctx.fillRect(x, 0, 1, h);
  }
}

function _fmt(v, units) {
  if (v == null || isNaN(v)) return '—';
  return `${v.toFixed(2)} ${units}`;
}

function _fire() {
  _onChange?.(_state.caseId, _state.fieldId, _state.planeId, _state.autoRange, _state.manualMin, _state.manualMax);
}

function _fireRange() {
  _onChange?.(_state.caseId, _state.fieldId, _state.planeId, _state.autoRange, _state.manualMin, _state.manualMax);
}

function _el(tag, cls) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  return el;
}

function _el_text(t) {
  const s = document.createElement('span');
  s.textContent = t;
  s.style.margin = '0 4px';
  return s;
}

function _row(text, cls) {
  const d = document.createElement('div');
  d.className = cls;
  d.textContent = text;
  panel.appendChild(d);
}

export function getActiveCfdState() { return { ..._state }; }
