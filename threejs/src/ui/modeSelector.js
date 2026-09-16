const MODES = ['ARCHITECTURE', 'PARTICLE', 'CFD_SUMMARY', 'CFD_FIELD'];

let _onChange = null;
let _active   = 'ARCHITECTURE';

export function setupModeSelector(onChange) {
  _onChange = onChange;

  const container = document.getElementById('mode-selector');
  for (const mode of MODES) {
    const btn = document.createElement('button');
    btn.className   = 'mode-btn' + (mode === _active ? ' active' : '');
    btn.dataset.mode = mode;
    btn.textContent  = mode.replace('_', ' ');
    btn.addEventListener('click', () => {
      container.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      _active = mode;
      _onChange?.(mode);
    });
    container.appendChild(btn);
  }
}

export function getActiveMode() { return _active; }
