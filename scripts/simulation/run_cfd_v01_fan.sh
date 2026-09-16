#!/usr/bin/env bash
# Compatibility entry point: the 300 Pa placeholder is archived and never run.
set -eo pipefail
exec bash "$(dirname "${BASH_SOURCE[0]}")/run_kvo250_v01.sh" "$@"
