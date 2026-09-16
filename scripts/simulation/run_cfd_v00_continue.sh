#!/usr/bin/env bash
# Continuation run: starts from the latest written timestep with revised
# fvSolution relaxation. Does NOT re-run blockMesh or checkMesh.
# Appends solver output to a separate log so the original is preserved.
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case_dir="${1:-$project_dir/cfd/V00}"
cd "$case_dir"
mkdir -p logs
echo "=== Continuation run: $(date) ===" >> logs/foamRun_continue.log
foamRun >> logs/foamRun_continue.log 2>&1
echo "Solver exited; inspect residuals and mass balance before claiming convergence."
