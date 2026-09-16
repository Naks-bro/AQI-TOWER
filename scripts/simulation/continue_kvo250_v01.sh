#!/usr/bin/env bash
# One documented tighter-linear-solve diagnostic. Never remeshes or resets fields.
set -eo pipefail
source /opt/openfoam14/etc/bashrc
project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$project_dir/cfd/V01_fan"
if [[ -e logs/foamRun_kvo_continue.log ]]; then
    echo 'Existing continuation protected.' >&2
    exit 2
fi
foamRun > logs/foamRun_kvo_continue.log 2>&1
echo 'Diagnostic ended. Evaluate criteria; do not infer physical unsteadiness from residual cycles.'
