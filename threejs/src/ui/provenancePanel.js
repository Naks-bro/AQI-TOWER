const btn  = document.getElementById('prov-btn');
const body = document.getElementById('prov-body');

export function setupProvenancePanel() {
  btn.addEventListener('click', () => body.classList.toggle('visible'));
}

export function setProvenance(mode, isRealParticles) {
  const rows = _getRows(mode, isRealParticles);
  body.innerHTML = rows.map(([k, v]) => `
    <div class="prov-row">
      <span class="prov-label">${k}</span>
      <span class="prov-value">${v}</span>
    </div>`).join('');
}

function _getRows(mode, isReal) {
  if (mode === 'ARCHITECTURE') {
    return [
      ['Mode',        'ARCHITECTURE'],
      ['Geometry',    'GEO_C — cad/parametric/PHASE8_GEOMETRY_AUDIT.json'],
      ['CFD zones',   'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json'],
      ['Filter data', 'results/FILTER_H13/bypass_analysis_sealed.json'],
      ['Data type',   'Structural geometry + CFD simulation'],
      ['Status',      'SIMULATION ONLY — NOT PHYSICALLY VALIDATED'],
      ['Caveats',     'All CFD values from partial non-converged RANS (SIMPLEC). Not measured.'],
    ];
  }

  if (mode === 'PARTICLE') {
    return [
      ['Mode',         'PARTICLE TRACKING'],
      ['Source',       'results/PARTICLE_CFD/particle_arrival_fractions.json'],
      ['Script',       'scripts/simulation/phase12b_particle_tracking.py'],
      ['Case',         'CASE_M_SEALED (Phase 10B, timestep 5000)'],
      ['Data type',    isReal ? 'Actual trajectory coordinates (pvpython export)' : 'SCHEMATIC — seed positions exact; terminal positions geometry-derived'],
      ['Seeds',        '224 valid of 324 candidates at x=0.010 m'],
      ['Model',        'Equilibrium-slip Euler, dt=0.004 s, no turbulent dispersion'],
      ['Status',       'SIMULATION POST-PROCESSING ONLY — NOT PHYSICALLY VALIDATED'],
      ['WARNING',      'FILTER ARRIVAL ≠ FILTER CAPTURE. η(d_p) not available. OUTLET=0 does not prove downstream capture.'],
    ];
  }

  if (mode === 'CFD_SUMMARY') {
    return [
      ['Mode',         'CFD SUMMARY'],
      ['Cases',        'results/GEOMETRY_OPTIMIZATION/comparison_metrics.json'],
      ['GEO_C',        'results/GEOMETRY_OPTIMIZATION/GEO_C/metrics.json'],
      ['CASE_M_SEALED','results/FILTER_H13/bypass_analysis_sealed.json'],
      ['Data type',    'CFD simulation metrics (mass-conserved integrals)'],
      ['Status',       'SIMULATION ONLY — NOT PHYSICALLY VALIDATED'],
      ['Caveats',      'All GEO_C cases reached RANS residual plateau; integrated quantities accepted for screening.'],
    ];
  }
  return [];
}
