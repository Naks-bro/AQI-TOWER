#!/usr/bin/env bash
# Run from WSL Ubuntu; never installs software or deletes previous results.
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case_dir="${1:-$project_dir/cfd/V00}"
cd "$case_dir"
if [[ -e logs/foamRun.log ]]; then
    echo 'Existing run log protected. Use a fresh case directory for a new run.' >&2
    exit 2
fi
mkdir -p logs
foamVersion > logs/openfoam-version.log
blockMesh > logs/blockMesh.log 2>&1
checkMesh -allTopology -allGeometry > logs/checkMesh.log 2>&1
grep -q 'Mesh OK' logs/checkMesh.log
foamRun > logs/foamRun.log 2>&1
echo 'Solver exited; inspect residuals and mass balance before claiming convergence.'
