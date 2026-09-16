import * as THREE from 'three';

/**
 * Schematic airflow path through GEO_C.
 * Arrows represent FLOW DIRECTION ONLY — not CFD velocities or magnitudes.
 * All positions are in Three.js coordinates (y = vertical / up).
 *
 * SCHEMATIC — NOT CFD OUTPUT.
 */

// Approximate centreline waypoints through GEO_C
const PATH_POINTS = [
  [-0.340, -0.700, 0],   // Inlet face
  [-0.210, -0.700, 0],   // Mid dirty-plenum
  [-0.074, -0.700, 0],   // Filter entry (HEPA upstream face)
  [ 0.080, -0.700, 0],   // Filter exit (HEPA downstream face)
  [ 0.150, -0.700, 0],   // Clean plenum
  [ 0.195, -0.500, 0],   // Turn step 1
  [ 0.250, -0.175, 0],   // Turn step 2 apex
  [ 0.125,  0.100, 0],   // Riser base
  [ 0.125,  0.600, 0],   // Riser mid
  [ 0.125,  0.775, 0],   // Fan inlet
  [ 0.340,  0.800, 0],   // Outlet face (fan discharge)
];

const ARROW_COLOR   = 0x2ad4a0;
const ARROW_OPACITY = 0.50;

export function createAirflow(scene) {
  const group = new THREE.Group();
  group.name  = 'AirflowGroup';

  const mat = new THREE.MeshBasicMaterial({ color: ARROW_COLOR, opacity: ARROW_OPACITY, transparent: true });

  for (let i = 0; i < PATH_POINTS.length - 1; i++) {
    const from = new THREE.Vector3(...PATH_POINTS[i]);
    const to   = new THREE.Vector3(...PATH_POINTS[i + 1]);
    addArrow(group, from, to, mat);
  }

  scene.add(group);
  return group;
}

function addArrow(group, from, to, mat) {
  const dir    = new THREE.Vector3().subVectors(to, from);
  const length = dir.length();
  if (length < 0.001) return;
  dir.normalize();

  const up = Math.abs(dir.y) > 0.99
    ? new THREE.Vector3(1, 0, 0)
    : new THREE.Vector3(0, 1, 0);
  const quat = new THREE.Quaternion().setFromUnitVectors(up, dir);

  const shaftLen = length * 0.72;
  const headLen  = length * 0.22;
  const shaftR   = 0.005;
  const headR    = 0.016;

  const shaftGeo = new THREE.CylinderGeometry(shaftR, shaftR, shaftLen, 6);
  const shaft    = new THREE.Mesh(shaftGeo, mat);
  shaft.position.copy(from).addScaledVector(dir, shaftLen / 2);
  shaft.setRotationFromQuaternion(quat);

  const headGeo = new THREE.ConeGeometry(headR, headLen, 8);
  const head    = new THREE.Mesh(headGeo, mat);
  head.position.copy(from).addScaledVector(dir, shaftLen + headLen / 2);
  head.setRotationFromQuaternion(quat);

  group.add(shaft);
  group.add(head);
}
