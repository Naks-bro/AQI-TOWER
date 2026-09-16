/**
 * Particle tracking data for Three.js viewer.
 *
 * Source: results/PARTICLE_CFD/particle_arrival_fractions.json
 *         scripts/simulation/phase12b_particle_tracking.py
 *
 * ─── CRITICAL ───────────────────────────────────────────────────────────────
 *  FILTER ARRIVAL ≠ FILTER CAPTURE.
 *  No capture efficiency η(d_p) applied. These are arrival fractions only.
 *  OUTLET = 0 in this tracking topology does NOT prove downstream capture;
 *  it means no particle crossed an outlet plane before reaching a terminal state.
 * ────────────────────────────────────────────────────────────────────────────
 *
 * Trajectory path coordinates: NOT stored in Phase 12B.
 * Only terminal positions were tracked in-memory; no path history was saved.
 * Run tools/export_particle_trajectories.py (pvpython, WSL) to generate
 * actual trajectory JSON at threejs/public/data/particleTrajectories.json.
 *
 * Seed positions below are exact — computed from Phase 12B script constants.
 * Terminal positions are SCHEMATIC — derived from geometry constants only.
 */

// ── Phase 12B script geometry constants (exact) ─────────────────────────────
export const TRACKING_PARAMS = {
  seed_x_cad:      0.010,    // m — injection plane (CAD x)
  n_seed_y:        18,
  n_seed_z:        18,
  seed_y_start:    0.08,     // m — CAD y
  seed_y_end:      0.82,     // m — CAD y
  seed_z_start:    0.12,     // m — CAD z
  seed_z_end:      0.88,     // m — CAD z
  n_seeds_total:   224,      // valid seeds (100 rejected near walls)
  n_candidates:    324,      // before wall-distance filter
  filter_x_gate:  0.290,    // m — particles reaching x > this are FILTER region
  filter_y:       [0.1035, 0.6965],  // m — active filter face y bounds (CAD)
  filter_z:       [0.2035, 0.7965],  // m — active filter face z bounds (CAD)
  frame_y:        [0.100,  0.700],   // m — filter frame y extent
  frame_z:        [0.150,  0.850],   // m — filter frame z extent
  bypass_seal_z:  0.850,     // m — bypass seal z-coordinate
  dt_s:           0.004,
  max_time_s:     6.0,
};

// ── Outcome colours (consistent with Phase 12B script) ───────────────────────
export const OUTCOME_COLORS = {
  FILTER_ARRIVAL: 0x22cc44,   // green
  FRAME_DEPOSIT:  0xf0a030,   // orange
  WALL_DEPOSIT:   0xdd2222,   // red
  RECIRCULATION:  0x9966ff,   // purple (none in Phase 12B)
};

export const OUTCOME_LABELS = {
  FILTER_ARRIVAL: 'Filter Arrival',
  FRAME_DEPOSIT:  'Frame / Inactive Area Deposit',
  WALL_DEPOSIT:   'Wall Deposit',
  RECIRCULATION:  'Recirculation (max-time)',
};

// ── Per-size summary (exact from particle_arrival_fractions.json) ────────────
export const SIZE_TAGS  = ['0p3um', '1um', '2p5um', '10um'];
export const SIZE_LABELS = { '0p3um': '0.3 µm', '1um': '1 µm', '2p5um': '2.5 µm', '10um': '10 µm' };

export const PARTICLE_SUMMARY = {
  '0p3um': { n_filter: 139, n_frame: 14, n_wall: 71, n_recirc: 0, n_total: 224 },
  '1um':   { n_filter: 139, n_frame: 14, n_wall: 71, n_recirc: 0, n_total: 224 },
  '2p5um': { n_filter: 139, n_frame: 14, n_wall: 71, n_recirc: 0, n_total: 224 },
  '10um':  { n_filter: 137, n_frame: 17, n_wall: 70, n_recirc: 0, n_total: 224 },
};

// ── Seed position generator (exact from script params) ───────────────────────
// Three.js coords: THREE_x = CAD_x − 0.350, THREE_y = CAD_z − 0.925, THREE_z = CAD_y − 0.400
export function buildSeedPositions() {
  const p = TRACKING_PARAMS;
  const pts = [];
  for (let iz = 0; iz < p.n_seed_z; iz++) {
    const z_cad = p.seed_z_start + iz * (p.seed_z_end - p.seed_z_start) / (p.n_seed_z - 1);
    for (let iy = 0; iy < p.n_seed_y; iy++) {
      const y_cad = p.seed_y_start + iy * (p.seed_y_end - p.seed_y_start) / (p.n_seed_y - 1);
      pts.push([
        p.seed_x_cad - 0.350,  // THREE_x
        z_cad         - 0.925,  // THREE_y
        y_cad         - 0.400,  // THREE_z
      ]);
    }
  }
  // pts contains all 324 candidates; 100 near walls are rejected in the real run
  // We cannot determine which 100 without the mesh; all 324 are shown as "candidates"
  return pts;
}

// ── Schematic terminal position generator ────────────────────────────────────
// Terminal positions are NOT available from particle_arrival_fractions.json.
// Positions below are SCHEMATIC — geometrically derived from script constants.
// They are placed in the correct spatial regions but are NOT the actual tracked positions.
// Label: SCHEMATIC — NOT actual Phase 12B terminal coordinates.

const LCG_A = 1664525, LCG_C = 1013904223, LCG_M = 2 ** 32;
function makeLcg(seed) {
  let s = seed >>> 0;
  return () => { s = (LCG_A * s + LCG_C) >>> 0; return s / LCG_M; };
}

export function buildSchematicTerminals(sizeTag) {
  const d = PARTICLE_SUMMARY[sizeTag];
  const p = TRACKING_PARAMS;
  const rng = makeLcg(sizeTag.charCodeAt(0) * 31 + sizeTag.length * 7);

  const terminals = [];

  // FILTER_ARRIVAL: distributed across active filter face (schematic)
  // CAD: x ≈ 0.290–0.300, y ∈ filter_y, z ∈ filter_z
  for (let i = 0; i < d.n_filter; i++) {
    const y_cad = p.filter_y[0] + rng() * (p.filter_y[1] - p.filter_y[0]);
    const z_cad = p.filter_z[0] + rng() * (p.filter_z[1] - p.filter_z[0]);
    const x_cad = 0.290 + rng() * 0.012;
    terminals.push({ outcome: 'FILTER_ARRIVAL', pos: [x_cad - 0.350, z_cad - 0.925, y_cad - 0.400] });
  }

  // FRAME_DEPOSIT: outside active filter area but within frame extents (schematic)
  for (let i = 0; i < d.n_frame; i++) {
    let y_cad, z_cad;
    if (rng() < 0.5) {
      // outside y range
      y_cad = rng() < 0.5
        ? p.frame_y[0] + rng() * (p.filter_y[0] - p.frame_y[0])
        : p.filter_y[1] + rng() * (p.frame_y[1] - p.filter_y[1]);
      z_cad = p.frame_z[0] + rng() * (p.frame_z[1] - p.frame_z[0]);
    } else {
      // outside z range
      y_cad = p.frame_y[0] + rng() * (p.frame_y[1] - p.frame_y[0]);
      z_cad = rng() < 0.5
        ? p.frame_z[0] + rng() * (p.filter_z[0] - p.frame_z[0])
        : p.filter_z[1] + rng() * (p.frame_z[1] - p.filter_z[1]);
    }
    const x_cad = 0.290 + rng() * 0.010;
    terminals.push({ outcome: 'FRAME_DEPOSIT', pos: [x_cad - 0.350, z_cad - 0.925, y_cad - 0.400] });
  }

  // WALL_DEPOSIT: on tower walls before filter (dirty plenum region) (schematic)
  for (let i = 0; i < d.n_wall; i++) {
    const face = Math.floor(rng() * 4);  // 4 possible wall faces
    let x_cad, y_cad, z_cad;
    switch (face) {
      case 0: // bottom wall (z=0)
        x_cad = 0.010 + rng() * 0.250; y_cad = rng() * 0.8; z_cad = 0.002 + rng() * 0.015;
        break;
      case 1: // left wall (x=0)
        x_cad = 0.002 + rng() * 0.010; y_cad = rng() * 0.8; z_cad = rng() * 0.45;
        break;
      case 2: // front wall (y=0)
        x_cad = 0.010 + rng() * 0.200; y_cad = 0.002 + rng() * 0.015; z_cad = rng() * 0.45;
        break;
      case 3: // back wall (y=0.8)
        x_cad = 0.010 + rng() * 0.200; y_cad = 0.785 + rng() * 0.015; z_cad = rng() * 0.45;
        break;
    }
    terminals.push({ outcome: 'WALL_DEPOSIT', pos: [x_cad - 0.350, z_cad - 0.925, y_cad - 0.400] });
  }

  return terminals;
}

// ── Schematic path segments ──────────────────────────────────────────────────
// Simple 2-segment paths: seed → midpoint → terminal.
// NOT actual tracked paths. Clearly labeled SCHEMATIC in the viewer.
export function buildSchematicPaths(seedPositions, terminals, sizeTag) {
  const p = TRACKING_PARAMS;
  const seeds = seedPositions.slice(0, PARTICLE_SUMMARY[sizeTag].n_total);
  const lines = { FILTER_ARRIVAL: [], FRAME_DEPOSIT: [], WALL_DEPOSIT: [] };

  // Assign seeds to terminals sequentially (schematic matching only)
  let fi = 0, wi = 0, fri = 0;
  const tFilter = terminals.filter(t => t.outcome === 'FILTER_ARRIVAL');
  const tWall   = terminals.filter(t => t.outcome === 'WALL_DEPOSIT');
  const tFrame  = terminals.filter(t => t.outcome === 'FRAME_DEPOSIT');

  for (let i = 0; i < seeds.length; i++) {
    const s = seeds[i];
    // Assign outcome based on known counts: first n_filter → filter, etc.
    const d = PARTICLE_SUMMARY[sizeTag];
    let outcome, term;
    if (i < d.n_filter) {
      outcome = 'FILTER_ARRIVAL';
      term    = tFilter[fi++ % tFilter.length].pos;
    } else if (i < d.n_filter + d.n_frame) {
      outcome = 'FRAME_DEPOSIT';
      term    = tFrame[fri++ % tFrame.length].pos;
    } else {
      outcome = 'WALL_DEPOSIT';
      term    = tWall[wi++ % tWall.length].pos;
    }
    lines[outcome].push(s, term);
  }

  return lines;
}
