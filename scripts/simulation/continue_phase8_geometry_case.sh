#!/usr/bin/env bash
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
case_name="${1:?Usage: continue_phase8_geometry_case.sh GEO_A|GEO_B|GEO_C|GEO_C_CONFIRM}"
case_dir="$project_dir/cfd/$case_name"
cd "$case_dir"
if [[ ! -e logs/foamRun_initial.log ]] || ! grep -q '^End$' logs/foamRun_initial.log; then
    echo "Clean initial run required before continuation: $case_name" >&2
    exit 2
fi
if [[ -e logs/foamRun_tight.log ]]; then
    echo "Existing Phase 8 continuation protected: $case_name" >&2
    exit 2
fi
cp system/fvSolution.tight system/fvSolution
foamDictionary system/controlDict -entry startFrom -set latestTime
foamDictionary system/controlDict -entry endTime -set 4000
foamRun > logs/foamRun_tight.log 2>&1
echo "$case_name bounded tighter-linear-solve diagnostic ended."
