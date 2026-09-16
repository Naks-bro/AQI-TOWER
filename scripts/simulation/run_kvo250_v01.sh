#!/usr/bin/env bash
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$project_dir/cfd/V01_fan"
if [[ -e logs/foamRun_kvo.log ]]; then
    echo 'Existing KVO run protected; no automatic overwrite.' >&2
    exit 2
fi
checkMesh -allTopology -allGeometry > logs/checkMesh_kvo.log 2>&1
grep -q 'Mesh OK' logs/checkMesh_kvo.log
foamRun > logs/foamRun_kvo.log 2>&1
echo 'KVO solve ended; assess convergence and curve closure before interpretation.'
