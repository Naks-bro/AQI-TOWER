#!/usr/bin/env bash
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case_name="${1:?Usage: run_filter_h13_case.sh CASE_L|CASE_M|CASE_H}"
case "$case_name" in CASE_L|CASE_M|CASE_H) ;; *) echo "Invalid Phase 9 case: $case_name" >&2; exit 2 ;; esac
case_dir="$project_dir/cfd/FILTER_H13/$case_name"
if [[ ! -d "$case_dir" ]]; then
    echo "Case does not exist: $case_dir" >&2
    exit 2
fi
cd "$case_dir"
if [[ -e logs/foamRun_initial.log ]]; then
    echo "Existing Phase 9 run protected: $case_name" >&2
    exit 2
fi
blockMesh > logs/blockMesh.log 2>&1
createBaffles > logs/createBaffles.log 2>&1
checkMesh -allTopology -allGeometry > logs/checkMesh.log 2>&1
grep -q 'Mesh OK' logs/checkMesh.log
foamRun > logs/foamRun_initial.log 2>&1
echo "$case_name initial run ended; assess every convergence criterion."
