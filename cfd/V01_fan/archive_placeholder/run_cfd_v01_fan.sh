#!/usr/bin/env bash
# V01_fan: pressure-driven run with placeholder fan totalPressure BC.
# Runs blockMesh + checkMesh fresh (new case, no prior fields).
# PLACEHOLDER: fan ΔP = 300 Pa. Replace 0/p p0 and constant/fanProperties
# when real fan curve data is available.
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case_dir="${1:-$project_dir/cfd/V01_fan}"
cd "$case_dir"
mkdir -p logs

echo "=== V01_fan blockMesh: $(date) ===" | tee -a logs/blockMesh.log
blockMesh >> logs/blockMesh.log 2>&1
echo "blockMesh done."

echo "=== V01_fan checkMesh: $(date) ===" | tee -a logs/checkMesh.log
checkMesh -allTopology -allGeometry >> logs/checkMesh.log 2>&1
echo "checkMesh done."

echo "=== V01_fan foamRun: $(date) ===" | tee -a logs/foamRun.log
foamRun >> logs/foamRun.log 2>&1
echo "Solver exited. Inspect logs/foamRun.log for residuals and mass balance."
echo "REMINDER: results are PLACEHOLDER — 300 Pa fan BC, empty tower, no filters."
