#!/usr/bin/env bash
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case_name="${1:?Usage: run_phase8_geometry_case.sh GEO_A|GEO_B|GEO_C|GEO_C_CONFIRM}"
case_dir="$project_dir/cfd/$case_name"
if [[ ! -d "$case_dir" ]]; then
    echo "Case does not exist: $case_dir" >&2
    exit 2
fi
cd "$case_dir"
if [[ -e logs/foamRun_initial.log ]]; then
    echo "Existing Phase 8 run protected: $case_name" >&2
    exit 2
fi
blockMesh > logs/blockMesh.log 2>&1
checkMesh -allTopology -allGeometry > logs/checkMesh.log 2>&1
grep -q 'Mesh OK' logs/checkMesh.log
foamRun > logs/foamRun_initial.log 2>&1
echo "$case_name initial run ended; assess every convergence criterion."
