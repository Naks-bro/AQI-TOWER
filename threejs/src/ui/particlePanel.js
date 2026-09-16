import { SIZE_TAGS, SIZE_LABELS, PARTICLE_SUMMARY, OUTCOME_COLORS, OUTCOME_LABELS } from '../../data/particleData.js';

const panel = document.getElementById('particle-panel');

let _onSizeChange    = null;
let _onOutcomeChange = null;

const _outcomeState = {
  FILTER_ARRIVAL: true,
  FRAME_DEPOSIT:  true,
  WALL_DEPOSIT:   true,
  RECIRCULATION:  false,  // none exist in Phase 12B — hidden by default
};
let _activeSize = null;  // null = all sizes

export function setupParticlePanel(onSizeChange, onOutcomeChange, isRealData) {
  _onSizeChange    = onSizeChange;
  _onOutcomeChange = onOutcomeChange;

  panel.innerHTML = '';

  // Data mode badge
  const badge = document.createElement('div');
  badge.className = 'p-badge ' + (isRealData ? 'p-badge-real' : 'p-badge-schematic');
  badge.textContent = isRealData
    ? 'REAL TRAJECTORY DATA LOADED'
    : 'SCHEMATIC MODE — run tools/export_particle_trajectories.py for real trajectories';
  panel.appendChild(badge);

  // Warning
  const warn = document.createElement('div');
  warn.className = 'p-warn';
  warn.innerHTML = '⚠ FILTER ARRIVAL ≠ FILTER CAPTURE<br>OUTLET = 0 does NOT prove downstream capture';
  panel.appendChild(warn);

  // Size filter heading
  const h3a = document.createElement('div');
  h3a.className = 'p-heading';
  h3a.textContent = 'PARTICLE DIAMETER';
  panel.appendChild(h3a);

  // Size buttons
  const sizeRow = document.createElement('div');
  sizeRow.className = 'p-size-row';

  const allBtn = _makeSizeBtn('ALL', null);
  allBtn.classList.add('active');
  sizeRow.appendChild(allBtn);

  for (const tag of SIZE_TAGS) {
    sizeRow.appendChild(_makeSizeBtn(SIZE_LABELS[tag], tag));
  }
  panel.appendChild(sizeRow);

  // Outcome filter heading
  const h3b = document.createElement('div');
  h3b.className = 'p-heading';
  h3b.textContent = 'OUTCOME FILTER';
  panel.appendChild(h3b);

  // Outcome rows
  for (const [outcome, label] of Object.entries(OUTCOME_LABELS)) {
    panel.appendChild(_makeOutcomeRow(outcome, label));
  }

  // Stats heading
  const h3c = document.createElement('div');
  h3c.className = 'p-heading';
  h3c.textContent = 'PHASE 12B SUMMARY';
  panel.appendChild(h3c);

  // Stats table
  panel.appendChild(_makeStatsTable());
}

function _makeSizeBtn(label, tag) {
  const btn = document.createElement('button');
  btn.className   = 'p-size-btn';
  btn.textContent = label;
  btn.dataset.tag = tag ?? 'ALL';

  btn.addEventListener('click', () => {
    panel.querySelectorAll('.p-size-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    _activeSize = tag;
    _onSizeChange?.(tag);
  });
  return btn;
}

function _makeOutcomeRow(outcome, label) {
  const hexToCSS = h => '#' + h.toString(16).padStart(6, '0');
  const col = hexToCSS(OUTCOME_COLORS[outcome]);

  const row = document.createElement('div');
  row.className = 'p-outcome-row';

  const toggle = document.createElement('div');
  toggle.className = 'p-outcome-toggle' + (_outcomeState[outcome] ? ' active' : '');
  toggle.style.borderColor = col;
  if (_outcomeState[outcome]) toggle.style.background = col;

  const dot = document.createElement('span');
  dot.style.cssText = `display:inline-block;width:7px;height:7px;border-radius:50%;background:${col};margin-right:6px;flex-shrink:0`;

  const lbl = document.createElement('span');
  lbl.textContent = label;

  row.append(toggle, dot, lbl);

  row.addEventListener('click', () => {
    _outcomeState[outcome] = !_outcomeState[outcome];
    toggle.classList.toggle('active', _outcomeState[outcome]);
    toggle.style.background = _outcomeState[outcome] ? col : '';

    const active = Object.entries(_outcomeState).filter(([, v]) => v).map(([k]) => k);
    _onOutcomeChange?.(active);
  });
  return row;
}

function _makeStatsTable() {
  const tbl = document.createElement('table');
  tbl.className = 'p-stats-tbl';

  const head = tbl.createTHead().insertRow();
  ['Size', 'Filter', 'Frame', 'Wall'].forEach(h => {
    const th = document.createElement('th');
    th.textContent = h;
    head.appendChild(th);
  });

  const body = tbl.createTBody();
  for (const tag of SIZE_TAGS) {
    const d = PARTICLE_SUMMARY[tag];
    const tr = body.insertRow();
    [
      SIZE_LABELS[tag],
      `${d.n_filter} (${(d.n_filter/d.n_total*100).toFixed(1)}%)`,
      `${d.n_frame} (${(d.n_frame/d.n_total*100).toFixed(1)}%)`,
      `${d.n_wall} (${(d.n_wall/d.n_total*100).toFixed(1)}%)`,
    ].forEach(v => { tr.insertCell().textContent = v; });
  }
  return tbl;
}
