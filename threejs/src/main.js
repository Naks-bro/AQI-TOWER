import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { createTower, getComponents } from './scene/createTower.js';
import { createAirflow } from './scene/createAirflow.js';
import {
  createParticles, isRealDataLoaded,
  setParticleGroupVisible, filterBySize, filterByOutcome,
} from './scene/createParticles.js';
import {
  initCfdPlane, showCfdField, hideCfdPlane,
  setCfdColorRange,
} from './scene/createCfdPlane.js';
import { setupInfoPanel, showInfo, hideInfo } from './ui/infoPanel.js';
import { setupLayerControls } from './ui/layerControls.js';
import { setupParticlePanel } from './ui/particlePanel.js';
import { setupProvenancePanel, setProvenance } from './ui/provenancePanel.js';
import { setupModeSelector } from './ui/modeSelector.js';
import { setupCfdFieldPanel, updateCfdPanelStatus } from './ui/cfdFieldPanel.js';

// ── renderer ──────────────────────────────────────────────────────────────────
const canvas = document.getElementById('viewer-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setClearColor(0x0a0e14, 1);
renderer.setSize(window.innerWidth, window.innerHeight);

// ── scene ─────────────────────────────────────────────────────────────────────
const scene = new THREE.Scene();

// ── camera ────────────────────────────────────────────────────────────────────
const camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.01, 30);
camera.position.set(1.8, 1.0, 2.2);
camera.lookAt(0, 0, 0);

const controls = new OrbitControls(camera, canvas);
controls.enableDamping  = true;
controls.dampingFactor  = 0.07;
controls.minDistance    = 0.4;
controls.maxDistance    = 8;
controls.target.set(0, 0, 0);

// ── lighting ──────────────────────────────────────────────────────────────────
scene.add(new THREE.AmbientLight(0x1a2840, 2.0));
const key = new THREE.DirectionalLight(0x4080c0, 2.5);
key.position.set(3, 4, 2);
scene.add(key);
const fill = new THREE.DirectionalLight(0x203050, 1.0);
fill.position.set(-2, 1, -3);
scene.add(fill);

// ── grid ──────────────────────────────────────────────────────────────────────
const gridHelper = new THREE.GridHelper(4, 20, 0x1a2840, 0x111a28);
gridHelper.position.y = -0.926;
scene.add(gridHelper);

// ── geometry ──────────────────────────────────────────────────────────────────
createTower(scene);
const airflowGroup = createAirflow(scene);
const components   = getComponents();
initCfdPlane(scene);

// Particles are async (attempts real data fetch)
let particleGroup = null;
(async () => {
  particleGroup = await createParticles(scene);
  setupParticlePanel(
    (tag) => filterBySize(tag),
    (outcomes) => filterByOutcome(outcomes),
    isRealDataLoaded(),
  );
})();

// ── mode state ────────────────────────────────────────────────────────────────
let currentMode = 'ARCHITECTURE';

const layerPanel    = document.getElementById('layer-panel');
const particlePanel = document.getElementById('particle-panel');
const sourceLegend  = document.getElementById('source-legend');
const cfdOverlay    = document.getElementById('cfd-overlay');
const cfdFieldPanel = document.getElementById('cfd-field-panel');
const explodeWrap   = document.getElementById('explode-wrap');

function applyMode(mode) {
  currentMode = mode;

  const isArch    = mode === 'ARCHITECTURE';
  const isPart    = mode === 'PARTICLE';
  const isCfdSum  = mode === 'CFD_SUMMARY';
  const isCfdFld  = mode === 'CFD_FIELD';

  // Panel visibility
  layerPanel.style.display    = isArch    ? '' : 'none';
  particlePanel.style.display = isPart    ? '' : 'none';
  sourceLegend.style.display  = isArch    ? '' : 'none';
  cfdOverlay.classList.toggle('visible',    isCfdSum);
  if (cfdFieldPanel) cfdFieldPanel.style.display = isCfdFld ? '' : 'none';

  // Explode slider — disabled in CFD_FIELD (spatial data must stay in place)
  if (explodeWrap) {
    explodeWrap.style.opacity       = isCfdFld ? '0.35' : '';
    explodeWrap.style.pointerEvents = isCfdFld ? 'none' : '';
  }
  const cfdNote = document.getElementById('explode-cfd-note');
  if (cfdNote) cfdNote.style.display = isCfdFld ? '' : 'none';
  if (isCfdFld && explodeFactor !== 0) {
    explodeFactor = 0;
    document.getElementById('explode-slider').value = 0;
    document.getElementById('explode-pct').textContent = '0%';
    applyExplode();
  }

  // CFD field plane — hide when leaving CFD_FIELD mode
  if (!isCfdFld) hideCfdPlane();

  // Particle geometry
  setParticleGroupVisible(isPart);

  // Airflow arrows — only in architecture mode; hidden in CFD_FIELD to avoid clutter
  if (airflowGroup) airflowGroup.visible = isArch && layers.airflow;

  // Tower opacity
  for (const mesh of Object.values(components)) {
    if (!mesh.material) continue;
    if (isPart) {
      if (mesh.userData.layer !== 'filter' && mesh.userData.layer !== 'enclosure') {
        mesh.material.opacity = Math.min(mesh.material.opacity ?? 1, 0.08);
        mesh.material.transparent = true;
      }
    } else if (isCfdFld) {
      // Ghost the enclosure so the plane inside is visible; keep filter opaque for context
      if (mesh.userData.layer === 'enclosure') {
        mesh.material.opacity = 0.08;
        mesh.material.transparent = true;
      } else {
        mesh.visible = layers[mesh.userData.layer] !== false;
      }
    } else {
      mesh.visible = layers[mesh.userData.layer] !== false;
    }
  }

  hideInfo();

  setProvenance(
    isArch ? 'ARCHITECTURE' : isPart ? 'PARTICLE' : 'CFD_SUMMARY',
    isRealDataLoaded(),
  );
}

// ── CFD field change handler ──────────────────────────────────────────────────
function onCfdFieldChange(caseId, fieldId, planeId, autoRange, manualMin, manualMax) {
  hideCfdPlane();
  const statusEl = document.getElementById('cf-status');
  if (statusEl) statusEl.textContent = 'Loading…';

  showCfdField(caseId, fieldId, planeId, (dataset) => {
    if (dataset.error) {
      updateCfdPanelStatus(null, dataset.error);
      return;
    }
    if (autoRange) {
      setCfdColorRange(dataset.data_min, dataset.data_max, true);
    } else {
      setCfdColorRange(manualMin, manualMax, false);
    }
    updateCfdPanelStatus(dataset, null);
  });
}

// ── layer state ───────────────────────────────────────────────────────────────
const layers = {
  enclosure: true, structure: true, filter: true,
  fan: true, schematic: true, airflow: true,
};

function applyLayers() {
  for (const mesh of Object.values(components)) {
    const ly = mesh.userData.layer;
    if (ly) mesh.visible = layers[ly] !== false;
  }
  if (airflowGroup) airflowGroup.visible = layers.airflow && currentMode === 'ARCHITECTURE';
}

// ── explode ───────────────────────────────────────────────────────────────────
const EXPLODE_OFFSETS = {
  WATER_STAGE:  new THREE.Vector3(-1.0, 0,    0),
  CARBON_STAGE: new THREE.Vector3(-0.6, 0,    0),
  HEPA_FILTER:  new THREE.Vector3(-0.3, 0,    0),
  CLEAN_PLENUM: new THREE.Vector3( 0.2, -0.3, 0),
  TURN_STEP_01: new THREE.Vector3( 0.3,  0.2, 0),
  TURN_STEP_02: new THREE.Vector3( 0.5,  0.1, 0),
  CLEAN_RISER:  new THREE.Vector3( 0.5,  0.3, 0),
  FAN_KVO250:   new THREE.Vector3( 0,    0.8, 0),
};

let explodeFactor = 0;

function applyExplode() {
  for (const [key, mesh] of Object.entries(components)) {
    const base   = mesh.userData.basePosition;
    const offset = EXPLODE_OFFSETS[key];
    if (base && offset) mesh.position.copy(base).addScaledVector(offset, explodeFactor);
  }
}

document.getElementById('explode-slider').addEventListener('input', e => {
  if (currentMode === 'CFD_FIELD') return;
  explodeFactor = e.target.value / 100;
  document.getElementById('explode-pct').textContent = e.target.value + '%';
  applyExplode();
});

// ── selection ─────────────────────────────────────────────────────────────────
const raycaster = new THREE.Raycaster();
const mouse     = new THREE.Vector2();
let selected    = null;

canvas.addEventListener('click', e => {
  if (currentMode !== 'ARCHITECTURE') return;
  const rect = canvas.getBoundingClientRect();
  mouse.x =  ((e.clientX - rect.left) / rect.width)  * 2 - 1;
  mouse.y = -((e.clientY - rect.top)  / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObjects(
    Object.values(components).filter(m => m.visible && m.isMesh),
  );

  if (hits.length > 0) {
    select(hits[0].object);
  } else {
    deselect(); hideInfo();
  }
});

function select(mesh) {
  deselect();
  selected = mesh;
  if (mesh.material?.emissive) {
    mesh.userData._prevEmissive = mesh.material.emissive.getHex();
    mesh.material.emissive.setHex(0x1a3a6a);
  }
  showInfo(mesh.userData);
}

function deselect() {
  if (!selected) return;
  if (selected.material?.emissive) {
    selected.material.emissive.setHex(selected.userData._prevEmissive ?? 0x000000);
  }
  selected = null;
}

// ── UI wiring ─────────────────────────────────────────────────────────────────
setupInfoPanel();
setupModeSelector(applyMode);
setupLayerControls(layers, components, (key, active) => {
  layers[key] = active;
  applyLayers();
});
setupProvenancePanel();
setProvenance('ARCHITECTURE', false);
setupCfdFieldPanel(onCfdFieldChange);

// ── resize ────────────────────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

// ── render loop ───────────────────────────────────────────────────────────────
(function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
})();
