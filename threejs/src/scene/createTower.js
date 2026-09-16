import * as THREE from 'three';
import { TOWER } from '../../data/towerConfig.js';

const components = {};

export function getComponents() {
  return components;
}

// ── materials ────────────────────────────────────────────────────────────────

function solidMat(color, opacity) {
  return new THREE.MeshPhongMaterial({
    color,
    opacity,
    transparent: opacity < 1,
    depthWrite:  opacity >= 0.5,
    side:        THREE.DoubleSide,
    emissive:    new THREE.Color(0x000000),
    shininess:   15,
  });
}

function edgeMat(color, opacity = 0.6) {
  return new THREE.LineBasicMaterial({ color, opacity, transparent: opacity < 1 });
}

function addEdges(mesh, geo, color, opacity) {
  const eg = new THREE.EdgesGeometry(geo);
  mesh.add(new THREE.LineSegments(eg, edgeMat(color, opacity)));
}

// ── helpers ──────────────────────────────────────────────────────────────────

function registerMesh(key, mesh, zone) {
  mesh.userData = Object.assign(mesh.userData || {}, {
    key,
    label:        zone.label,
    source:       zone.source,
    layer:        zone.layer,
    info:         zone.info || {},
    basePosition: mesh.position.clone(),
  });
  components[key] = mesh;
}

// ── face marker (inlet / outlet planes) ──────────────────────────────────────

function makeFaceMarker(cfg, group) {
  const geo  = new THREE.PlaneGeometry(cfg.planeH, cfg.planeW);
  const mat  = new THREE.MeshBasicMaterial({ color: cfg.color, opacity: 0.35, transparent: true, side: THREE.DoubleSide });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.position.set(...cfg.center);
  mesh.rotation.y = Math.PI / 2;   // face perpendicular to x-axis
  mesh.userData = {
    key:          cfg.label,
    label:        cfg.label,
    source:       cfg.source,
    layer:        cfg.layer,
    info:         { description: cfg.label },
    basePosition: mesh.position.clone(),
  };
  group.add(mesh);
  components[cfg.label] = mesh;
}

// ── main export ───────────────────────────────────────────────────────────────

export function createTower(scene) {
  const group = new THREE.Group();
  group.name  = 'TowerGroup';

  // Outer enclosure (semi-transparent shell + edges)
  const encGeo  = new THREE.BoxGeometry(...TOWER.enclosure.size);
  const encMat  = new THREE.MeshBasicMaterial({ color: 0x1e3a5f, opacity: 0.05, transparent: true, side: THREE.BackSide });
  const encMesh = new THREE.Mesh(encGeo, encMat);
  encMesh.position.set(...TOWER.enclosure.center);
  encMesh.userData = {
    key:          'ENCLOSURE',
    label:        'Tower Enclosure (GEO_C)',
    source:       'CAD',
    layer:        'enclosure',
    info: {
      description: 'GEO_C outer bounding box. DESIGN EXPERIMENT PARAMETER — NOT PRODUCT REQUIREMENT.',
      size_mm:     '700 × 1850 × 800 mm (flow × height × depth)',
      sha256:      TOWER.cad_sha256,
    },
    basePosition: encMesh.position.clone(),
  };
  addEdges(encMesh, encGeo, 0x1e3a5f, 0.45);
  group.add(encMesh);
  components['ENCLOSURE'] = encMesh;

  // Zone boxes
  for (const [key, zone] of Object.entries(TOWER.zones)) {
    if (zone.isCylinder) {
      // Fan — cylinder
      const cGeo  = new THREE.CylinderGeometry(zone.cylinderRadius, zone.cylinderRadius, zone.cylinderHeight, 32);
      const cMat  = solidMat(zone.color, zone.opacity);
      const cMesh = new THREE.Mesh(cGeo, cMat);
      cMesh.position.set(...zone.center);
      addEdges(cMesh, cGeo, zone.color, 0.8);
      group.add(cMesh);
      registerMesh(key, cMesh, zone);
    } else {
      const geo  = new THREE.BoxGeometry(...zone.size);
      const mat  = solidMat(zone.color, zone.opacity);
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(...zone.center);

      const edgeOpacity = (zone.source === 'ENGINEERING') ? 0.8
                        : (zone.source === 'SCHEMATIC')    ? 0.4
                        : 0.5;
      addEdges(mesh, geo, zone.color, edgeOpacity);
      group.add(mesh);
      registerMesh(key, mesh, zone);
    }
  }

  // Inlet / outlet face markers
  makeFaceMarker(TOWER.inlet,  group);
  makeFaceMarker(TOWER.outlet, group);

  scene.add(group);
  return group;
}
