import * as THREE from 'three';

// ── Turbo colormap (6-stop linear approximation) ──────────────────────────
const TURBO_STOPS = [
  [0.188, 0.071, 0.232],  // t=0.00 dark purple
  [0.188, 0.690, 0.969],  // t=0.20 cyan
  [0.482, 0.871, 0.427],  // t=0.40 green
  [0.851, 0.882, 0.094],  // t=0.60 yellow
  [1.000, 0.482, 0.161],  // t=0.80 orange
  [0.478, 0.016, 0.012],  // t=1.00 dark red
];

function turboColor(t) {
  const clamped = Math.max(0, Math.min(1, t));
  const scaled  = clamped * (TURBO_STOPS.length - 1);
  const lo      = Math.floor(scaled);
  const hi      = Math.min(lo + 1, TURBO_STOPS.length - 1);
  const frac    = scaled - lo;
  const a = TURBO_STOPS[lo], b = TURBO_STOPS[hi];
  return [
    a[0] + (b[0] - a[0]) * frac,
    a[1] + (b[1] - a[1]) * frac,
    a[2] + (b[2] - a[2]) * frac,
  ];
}

// ── Module state ──────────────────────────────────────────────────────────
let _scene       = null;
let _planeMesh   = null;
let _dataset     = null;
let _colorMin    = 0;
let _colorMax    = 1;
let _useAutoRange = true;

// ── CAD → Three.js coordinate transforms ─────────────────────────────────
// THREE_x = CAD_x − 0.350
// THREE_y = CAD_z − 0.925  (vertical axis)
// THREE_z = CAD_y − 0.400  (depth axis)

function longitudinalPoint(ix, iz, grid) {
  const xa = grid.axis1_range[0], xb = grid.axis1_range[1];
  const za = grid.axis2_range[0], zb = grid.axis2_range[1];
  const cad_x = xa + (xb - xa) * ix / (grid.n_axis1 - 1);
  const cad_z = za + (zb - za) * iz / (grid.n_axis2 - 1);
  return [cad_x - 0.350, cad_z - 0.925, 0.0];   // Three.js (x, y, z)
}

function filterXsecPoint(iy, iz, grid) {
  const ya = grid.axis1_range[0], yb = grid.axis1_range[1];
  const za = grid.axis2_range[0], zb = grid.axis2_range[1];
  const cad_y = ya + (yb - ya) * iy / (grid.n_axis1 - 1);
  const cad_z = za + (zb - za) * iz / (grid.n_axis2 - 1);
  // plane is at CAD_x = 0.305 → THREE_x = -0.045
  return [-0.045, cad_z - 0.925, cad_y - 0.400];
}

// ── Build BufferGeometry from dataset ────────────────────────────────────
function buildPlaneMesh(dataset, colorMin, colorMax) {
  const { grid, values } = dataset;
  const n1 = grid.n_axis1;
  const n2 = grid.n_axis2;

  const isLong = grid.type === 'longitudinal';
  const ptFn   = isLong ? longitudinalPoint : filterXsecPoint;

  const positions = [];
  const colors    = [];

  const idx = (i, j) => i * n2 + j;
  const val = (i, j) => values[idx(i, j)];

  for (let i = 0; i < n1 - 1; i++) {
    for (let j = 0; j < n2 - 1; j++) {
      const v00 = val(i,   j  );
      const v10 = val(i+1, j  );
      const v01 = val(i,   j+1);
      const v11 = val(i+1, j+1);

      // Skip quads where any corner is NaN (null from JSON → null in JS)
      if (v00 == null || v10 == null || v01 == null || v11 == null) continue;

      const p00 = ptFn(i,   j,   grid);
      const p10 = ptFn(i+1, j,   grid);
      const p01 = ptFn(i,   j+1, grid);
      const p11 = ptFn(i+1, j+1, grid);

      const range = colorMax - colorMin || 1;
      const c00 = turboColor((v00 - colorMin) / range);
      const c10 = turboColor((v10 - colorMin) / range);
      const c01 = turboColor((v01 - colorMin) / range);
      const c11 = turboColor((v11 - colorMin) / range);

      // Triangle 1: 00, 10, 01
      positions.push(...p00, ...p10, ...p01);
      colors.push(...c00, ...c10, ...c01);

      // Triangle 2: 10, 11, 01
      positions.push(...p10, ...p11, ...p01);
      colors.push(...c10, ...c11, ...c01);
    }
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute('color',    new THREE.Float32BufferAttribute(colors,    3));

  const mat  = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide });
  return new THREE.Mesh(geo, mat);
}

// ── Rebuild colors on existing geometry when range changes ────────────────
function rebuildColors(mesh, dataset, colorMin, colorMax) {
  const { grid, values } = dataset;
  const n1 = grid.n_axis1, n2 = grid.n_axis2;
  const range = colorMax - colorMin || 1;
  const colorAttr = mesh.geometry.attributes.color;
  let vtxIdx = 0;

  for (let i = 0; i < n1 - 1; i++) {
    for (let j = 0; j < n2 - 1; j++) {
      const v00 = values[i*n2+j], v10 = values[(i+1)*n2+j];
      const v01 = values[i*n2+j+1], v11 = values[(i+1)*n2+j+1];
      if (v00 == null || v10 == null || v01 == null || v11 == null) continue;
      const verts = [v00, v10, v01, v10, v11, v01];
      for (const v of verts) {
        const [r, g, b] = turboColor((v - colorMin) / range);
        colorAttr.setXYZ(vtxIdx++, r, g, b);
      }
    }
  }
  colorAttr.needsUpdate = true;
}

// ── Public API ────────────────────────────────────────────────────────────
export function initCfdPlane(scene) {
  _scene = scene;
}

export async function showCfdField(caseId, fieldId, planeId, onLoaded) {
  hideCfdPlane();

  const url = `./data/cfd/${caseId}_${fieldId}_${planeId}.json`;
  let data;
  try {
    const resp = await fetch(url);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    data = await resp.json();
  } catch (err) {
    console.warn('[CFD] fetch failed:', url, err.message);
    onLoaded?.({ error: `Data not available: ${url}` });
    return;
  }

  _dataset  = data;
  if (_useAutoRange) {
    _colorMin = data.data_min;
    _colorMax = data.data_max;
  }

  _planeMesh = buildPlaneMesh(data, _colorMin, _colorMax);
  _scene.add(_planeMesh);

  onLoaded?.(data);
}

export function hideCfdPlane() {
  if (_planeMesh) {
    _scene.remove(_planeMesh);
    _planeMesh.geometry.dispose();
    _planeMesh.material.dispose();
    _planeMesh = null;
  }
  _dataset = null;
}

export function setCfdColorRange(min, max, auto) {
  _useAutoRange = !!auto;
  if (!auto) { _colorMin = min; _colorMax = max; }
  else if (_dataset) { _colorMin = _dataset.data_min; _colorMax = _dataset.data_max; }
  if (_planeMesh && _dataset) rebuildColors(_planeMesh, _dataset, _colorMin, _colorMax);
}

export function getCfdDataset()   { return _dataset; }
export function getCfdColorMin()  { return _colorMin; }
export function getCfdColorMax()  { return _colorMax; }
export function isCfdPlaneVisible() { return !!_planeMesh; }
export function getTurboColor(t)  { return turboColor(t); }
