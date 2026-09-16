const panel = document.getElementById('layer-panel');

const LAYER_DEFS = [
  { key: 'enclosure', label: 'Enclosure',               color: '#1e4a7f' },
  { key: 'structure', label: 'Structure / CFD Zones',   color: '#2060a0' },
  { key: 'filter',    label: 'HEPA Filter',             color: '#4a9eff' },
  { key: 'fan',       label: 'Fan (Schematic)',         color: '#e0c040' },
  { key: 'schematic', label: 'Provisional / Concept',  color: '#c07830' },
  { key: 'airflow',   label: 'Airflow (Schematic)',    color: '#2ad4a0' },
];

export function setupLayerControls(layers, _components, onChange) {
  const h3 = document.createElement('h3');
  h3.textContent = 'LAYERS';
  panel.appendChild(h3);

  for (const def of LAYER_DEFS) {
    const row    = document.createElement('div');
    row.className = 'layer-row';

    const toggle = document.createElement('div');
    toggle.className = 'layer-toggle active';

    const dot = document.createElement('div');
    dot.className = 'layer-dot';
    dot.style.background = def.color;

    const span = document.createElement('span');
    span.textContent = def.label;

    row.append(toggle, dot, span);
    panel.appendChild(row);

    row.addEventListener('click', () => {
      const active = toggle.classList.toggle('active');
      onChange(def.key, active);
    });
  }
}
